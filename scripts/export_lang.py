"""Generates `{lang_en}.json`."""

import json

from env_setup import DATA_PATH
from updater import Updater
from phonology import SYLLABLE_MAP


COLUMNS = [
    "字頭",
    "記錄讀音",
    "層",
    "訓作",
    "釋義",
    "小韻號",
]


session = Updater()

for lang_en in SYLLABLE_MAP:
    lang_cn = SYLLABLE_MAP[lang_en].NAME

    seen = {}

    def to_entry(row: dict) -> dict:
        row["記錄讀音"] = row["讀音"] if "讀音" in row else None

        if row["小韻號"] is not None:
            if row["字頭"] not in seen:
                seen[row["字頭"]] = set()
            seen[row["字頭"]].add(row["小韻號"])

        return {key: row.get(key) for key in COLUMNS}

    session.cursor.execute(f"SELECT * FROM {lang_cn}")
    dictionary = [to_entry(row) for row in session.data]

    session.cursor.execute("SELECT * FROM 字頭全")
    for row in session.data:
        if f"推導{lang_cn}" not in row:
            break
        if row["小韻號"] not in seen.get(row["字頭"], set()):
            dictionary.append(to_entry(row))

    with open(DATA_PATH / "generated" / f"{lang_en}.json", "w", encoding="utf-8") as f:
        json.dump(dictionary, f, separators=(",", ":"), ensure_ascii=False)

    print(f"導出{lang_cn}字典完成！")
