"""Defines Updater class as API for hanzi.sqlite3."""

import sqlite3
import json
import questionary
from collections import defaultdict
from functools import cached_property
from typing import Any

from env_setup import DATA_PATH
from phonology import SYLLABLE_MAP, FGSyllable
from predict import REFLEX_GETTER_MAP


class Updater:
    def __init__(
        self,
        db_name: str = "hanzi.sqlite3",
        lang_en: str = "FG",
    ):
        self._conn = sqlite3.connect(DATA_PATH / "manual" / db_name)
        self._conn.row_factory = sqlite3.Row
        self.cursor = self._conn.cursor()
        self.lang_en = lang_en
        self.lang_cn = SYLLABLE_MAP[lang_en].NAME
        self.Syllable = SYLLABLE_MAP[lang_en]
        self.get_reflex = REFLEX_GETTER_MAP.get(lang_en, None)

    def __del__(self):
        self._conn.commit()
        self._conn.close()

    @property
    def data(self) -> list[dict[str, Any]]:
        """查詢結果"""
        return [dict(row) for row in self.cursor.fetchall()]

    @cached_property
    def mc_entry_map(self) -> dict[int, dict[str, Any]]:
        """廣韻小韻數據"""
        self.cursor.execute("SELECT * FROM 小韻全")
        syllables = {}
        for row in self.data:
            syllables[row["小韻號"]] = row
        return syllables

    @cached_property
    def mc_dictionary(self) -> dict[str, list[dict[str, Any]]]:
        """廣韻字典"""
        self.cursor.execute("SELECT * FROM 字頭全")
        dictionary = defaultdict(list)
        for row in self.data:
            dictionary[row["字頭"]].append(row)
        return dictionary

    def get_dictionary(self, language: str = "") -> dict[str, list[dict[str, Any]]]:
        """現代方言字典

        language: 代號或中文名
        """

        lang_cn = language
        if language == "":
            lang_cn = self.lang_cn
        if language in SYLLABLE_MAP:
            lang_cn = SYLLABLE_MAP[language].NAME

        self.cursor.execute(f"SELECT * FROM {lang_cn}")
        dictionary = defaultdict(list)
        for row in self.data:
            dictionary[row["字頭"]].append(row)
        return dictionary

    @staticmethod
    def show_syllable(row: dict[str, str], include_tone: bool = True) -> str:
        return "".join(
            [
                row["聲母"],
                row["介音"],
                row["韻腹"],
                row["韻尾"],
                row.get("聲調", "") if include_tone else "",
            ]
        )

    def show_mc_entry(self, entry: dict[str, Any]) -> str:
        return " ".join(
            [
                entry["字頭"],
                str(entry["小韻號"]),
                entry["音韻地位"],
                entry[f"推導{self.lang_cn}"],
                entry["釋義"] or "",
            ]
        )

    """utility scripts"""

    def update_reflex(self) -> None:
        """推導所有小韻的現代音"""

        if self.get_reflex is None:
            raise Exception("暫不支持從中古音推導該方言。")

        self.cursor.execute("SELECT * FROM 小韻全")
        updated = []
        for row in self.data:
            expected_reflex = self.Syllable.parse_ipa(
                Updater.show_syllable(self.get_reflex(row))
            ).pinyin()
            self.cursor.execute(
                f"UPDATE 小韻 SET 推導{self.lang_cn} = ? WHERE 小韻號 = ?",
                (expected_reflex, row["小韻號"]),
            )
            if expected_reflex != row[f"推導{self.lang_cn}"]:
                updated.append(
                    f"{row['小韻號']} {row['字']}: {row[f'推導{self.lang_cn}']} -> {expected_reflex}"
                )
        print(f"推導{self.lang_cn}完成！共更新 {len(updated)} 個小韻。")
        for item in updated:
            print("  " + item)
        self.__dict__.pop("dictionary", None)  # dictionary needs update

    def compare_inventories(self) -> None:
        """比較推導音節集與記錄音節集（不計聲調）"""

        self.cursor.execute(
            f"SELECT * FROM 小韻全 WHERE 推導{self.lang_cn} IS NOT NULL"
        )
        推導音節 = set()
        for row in self.data:
            推導音 = row[f"推導{self.lang_cn}"]
            推導音 = 推導音[:-1] if 推導音[-1].isdigit() else 推導音  # 除去聲調
            推導音節.add(推導音)

        with open(DATA_PATH / "generated" / "strata.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            for strata in data.get(self.lang_en, {}).values():
                for [_, pron] in strata:
                    推導音節.add(pron[:-1])

        self.cursor.execute(f"SELECT * FROM {self.lang_cn}")
        收錄音節 = set()
        for row in self.data:
            收錄音節.add(row["讀音"][:-1])

        def show_set(s: set[str]) -> str:
            return ", ".join(sorted(s))

        print(
            "\n".join(
                [
                    f"推導音節數：{len(推導音節)} ；收錄音節數：{len(收錄音節)} （不計聲調）",
                    f"推導出但不存在的音節：{show_set(推導音節.difference(收錄音節))}",
                    f"存在但推導不出的音節：{show_set(收錄音節.difference(推導音節))}",
                ]
            )
        )

    # recheck below

    def _predict_mc(self, row: dict[str, Any]) -> list[dict[str, Any]]:
        """推導字條的廣韻字頭號"""

        def is_match(推導音: str, 收錄音: str) -> bool:
            return (
                self.Syllable.parse_pinyin(推導音).MC_tone
                == self.Syllable.parse_pinyin(收錄音).MC_tone
            )

        字 = row["字頭"]
        收錄音 = row["讀音"]

        entries = [
            entry
            for entry in self.mc_dictionary[字]
            if entry["小韻號"] in self.mc_entry_map
        ]
        if len(entries) == 1:
            return entries

        exact_matches = [
            entry for entry in entries if entry[f"推導{self.lang_cn}"] == 收錄音
        ]
        if len(exact_matches) > 0:
            return exact_matches

        if self.lang_cn not in ["日本語", "朝鮮語"]:
            matches = [
                entry
                for entry in entries
                if is_match(entry[f"推導{self.lang_cn}"], 收錄音)
            ]
            if len(matches) > 0:
                return matches

        return entries

    """以下專爲撫州話"""

    def add_mc_index(self, 字: str) -> None:
        """手動選擇撫州話字條的廣韻小韻號"""

        self.cursor.execute("SELECT rowid, * FROM 撫州話 WHERE 字頭 = ?", (字,))
        data = self.data
        if len(data) == 0:
            print("撫州話字典未收錄該字！")
            return False, "撫州話字典未收錄"

        unsure = False
        updated = False
        for row in data:
            if row["小韻號"] is not None:
                continue

            print(f"{字} 收錄音：{Updater.show_syllable(row)}")

            entries = self._predict_mc(row)
            if len(entries) == 0:
                print("廣韻未收錄該字！")
                return False, "廣韻未收錄"

            choice = questionary.select(
                "請選擇：",
                choices=[
                    {"name": Updater.show_mc_entry(entry), "value": entry}
                    for entry in entries
                ]
                + [{"name": "以上都不對 / 不確定", "value": {}}],
            ).ask()
            if choice is None:
                raise KeyboardInterrupt

            if "小韻號" in choice:
                self.cursor.execute(
                    "UPDATE 撫州話 SET 小韻號 = ? WHERE rowid = ?",
                    (choice["小韻號"], row["rowid"]),
                )
                updated = True
            else:
                unsure = True

        return updated, "不確定" if unsure else "已添加小韻號"

    def add_entry(self, 字: str) -> None:
        """手動錄入撫州話字條"""

        self.cursor.execute("SELECT * FROM 撫州話 WHERE 字頭 = ?", (字,))
        data = self.data
        if len(data) != 0:
            print("已收錄讀音：" + ", ".join(row["讀音"] for row in data))
            if not questionary.confirm("是否要錄入讀音？", default=False).ask():
                return False, "用戶終止"

        MC_index = None
        FG_syllable = None

        entries = self.mc_dictionary[字]
        if len(entries) > 0:
            choice = questionary.select(
                "請選擇廣韻字條：",
                choices=[
                    {"name": self.show_mc_entry(entry), "value": entry}
                    for entry in entries
                ]
                + [{"name": "以上都不是 / 不確定", "value": {}}],
            ).ask()
            if choice is None:
                raise KeyboardInterrupt

            if "小韻號" in choice:
                MC_index = choice["小韻號"]

                if questionary.confirm("是否要使用推導音？").ask():
                    FG_syllable = FGSyllable.parse_pinyin(choice["推導撫州話"])

        if FG_syllable is None:
            text = input("請輸入讀音：")

            try:
                syllable_from_ipa = FGSyllable.parse_ipa(text)
            except ValueError:
                syllable_from_ipa = None

            try:
                syllable_from_pinyin = FGSyllable.parse_pinyin(text)
            except ValueError:
                syllable_from_pinyin = None

            match (syllable_from_ipa is not None, syllable_from_pinyin is not None):
                case (True, True) if syllable_from_ipa != syllable_from_pinyin:
                    choice = questionary.select(
                        "剛才輸入的是音標還是拼音？",
                        choices=[
                            {
                                "name": f"拼音 ({syllable_from_pinyin.ipa_raw})",
                                "value": syllable_from_pinyin,
                            },
                            {
                                "name": f"音標 ({syllable_from_ipa.ipa_raw})",
                                "value": syllable_from_ipa,
                            },
                        ],
                    ).ask()
                    if choice is None:
                        raise KeyboardInterrupt
                    FG_syllable = choice
                case (True, _):
                    FG_syllable = syllable_from_ipa
                case (False, True):
                    FG_syllable = syllable_from_pinyin
                case (False, False):
                    print("請輸入正確讀音！")
                    return False, "用戶輸入錯誤"

            if not text[-1].isnumeric() and FG_syllable.tone == "1":
                choice = questionary.select(
                    "是否是陽去？",
                    choices=[
                        {"name": "陰平 1", "value": "1"},
                        {"name": "陽去 6", "value": "6"},
                    ],
                ).ask()
                if choice is None:
                    raise KeyboardInterrupt
                FG_syllable = FGSyllable(
                    FG_syllable.initial,
                    FG_syllable.medial,
                    FG_syllable.nucleus,
                    FG_syllable.coda,
                    choice,
                )

        print(f"讀音信息：{', '.join(FG_syllable.tuple)}")

        def get_optional_input(label):
            text = input(f"{label}：").strip()
            return text or None

        層 = 訓作 = 釋義 = None
        if questionary.confirm("是否要附加信息？", default=False).ask():
            層, 訓作, 釋義 = map(get_optional_input, ["層", "訓作", "釋義"])

        self.cursor.execute(
            "INSERT INTO 撫州話 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                字,
                FG_syllable.pinyin(tone_diacritic=False),
                *FG_syllable.tuple,
                MC_index,
                層,
                訓作,
                釋義,
            ),
        )
