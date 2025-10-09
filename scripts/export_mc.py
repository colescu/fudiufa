"""Generates `MC.json`."""

import json

from env_setup import DATA_PATH
from updater import Updater
from phonology import SYLLABLE_MAP


COLUMNS = [
    "字",
    "反切",
    "聲母",
    "清濁",
    "音",
    "組",
    "攝",
    "韻系",
    "等",
    "呼",
    "重紐",
    "聲調",
]


def to_mc_entry(row: dict) -> dict:
    上, 下 = row["上字"], row["下字"]
    row["反切"] = f"{上}{下}切" if 上 and 下 else None
    return {key: row.get(key) for key in COLUMNS}


session = Updater()

MC_ENTRY_MAP = {}
session.cursor.execute("""
--sql
SELECT 小韻全.*, COUNT(*) AS 字數
FROM 小韻全
LEFT JOIN 字頭 ON 小韻全.小韻號 = 字頭.小韻號
GROUP BY 小韻全.小韻號;
""")
for row in session.data:
    MC_ENTRY_MAP[row["小韻號"]] = {
        "字數": row["字數"],
        "MC": to_mc_entry(row),
        "reflex": {
            lang: row.get(f"推導{SYLLABLE_MAP[lang].NAME}") for lang in SYLLABLE_MAP
        },
    }


with open(DATA_PATH / "generated" / "MC.json", "w", encoding="utf-8") as f:
    json.dump(MC_ENTRY_MAP, f, separators=(",", ":"), ensure_ascii=False)

print("導出廣韻小韻數據完成！")
