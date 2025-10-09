"""Generates `syllables.json`."""

import json

from env_setup import DATA_PATH
from updater import Updater
from phonology import SYLLABLE_MAP


session = Updater()


ALL_SYLLABLES = {}

for lang_en, syllable_cls in SYLLABLE_MAP.items():
    lang_cn = syllable_cls.NAME

    syllables = set()

    session.cursor.execute(f"SELECT * FROM {lang_cn}")
    for row in session.data:
        syllables.add(syllable_cls.parse_pinyin(row["讀音"]))

    session.cursor.execute("SELECT * FROM 小韻")
    for row in session.data:
        if (pron := row.get(f"推導{lang_cn}", None)) is not None:
            try:
                syllables.add(syllable_cls.parse_pinyin(pron))
            except Exception:
                print(f"Error parsing {lang_cn} {pron}")

    if lang_en == "FG":
        for initial in ["", "t", "n", "tɕ", "tɕʰ", "ɕ"]:
            syllables.add(syllable_cls(initial, "", "y", "", "0"))
        for initial in ["p", "pʰ", "m", "f"]:
            syllables.add(syllable_cls(initial, "w", "i", "", "0"))
        for initial in ["t", "tʰ", "ts", "tsʰ", "s"]:
            syllables.add(syllable_cls(initial, "", "o", "i", "0"))
        for syllable in [
            ["ŋ", "", "ɛ", ""],
            ["h", "", "ɛ", ""],
            ["ŋ", "", "a", "ʔ"],
            ["", "j", "a", "ʔ"],
            ["m", "j", "a", "ʔ"],
            ["", "w", "a", "ʔ"],
            ["k", "w", "a", "ʔ"],
            ["f", "", "ɛ", "t"],
            ["m", "j", "ɛ", ""],
            ["l", "w", "o", "i"],
        ]:
            syllables.add(syllable_cls(*syllable, "0"))

        # URGENT variant syllables
        VARIANT_MAP = {
            "iau": "ieu",
            "yo": "ye",
            "io": "yo",
        }

    # order by pinyin
    syllables = sorted(list(syllables), key=lambda syl: syl.pinyin())

    rows = []
    seen = set()

    for syl in syllables:
        tuple_syl = syl.tuple[:4]
        ipa_strict = syl.ipa_strict_no_tone
        pinyin = syl.pinyin()
        if pinyin[-1].isdigit():
            pinyin = pinyin[:-1]
        if tuple_syl not in seen:
            seen.add(tuple_syl)
            data = {
                "tuple": tuple_syl,
                "ipaRaw": "".join(tuple_syl),
                "ipaStrict": ipa_strict,
            }
            match lang_en:
                case "JP":
                    for format in ["hira", "kata", "NR", "HR"]:
                        data[format] = syl.pinyin(format)
                case "KR":
                    for format in ["hangul", "RR"]:
                        data[format] = syl.pinyin(format)
                case _:
                    data["pinyin"] = pinyin
            rows.append(data)

    # for illustrative purpose
    if lang_en == "FG":
        for initial in ["ts", "tsʰ", "s"]:
            rows.append(
                {
                    "tuple": [initial, "", "ə", "n"],
                    "ipaRaw": initial + "ən",
                    "ipaStrict": initial + "ən",
                    "pinyin": ["z", "c", "s"][["ts", "tsʰ", "s"].index(initial)]
                    + "iin",
                }
            )
        for initial in ["p", "pʰ", "m", "f"]:
            rows.append(
                {
                    "tuple": [initial, "", "ɿ", "t"],
                    "ipaRaw": initial + "ɿt",
                    "ipaStrict": initial + "ɨt̚",
                    "pinyin": ["b", "p", "m", "f"][["p", "pʰ", "m", "f"].index(initial)]
                    + "iit",
                }
            )

    ALL_SYLLABLES[lang_en] = rows


with open(DATA_PATH / "generated" / "syllables.json", "w", encoding="utf-8") as f:
    json.dump(ALL_SYLLABLES, f, separators=(",", ":"), ensure_ascii=False)

print("導出現代方言音節數據完成！")
