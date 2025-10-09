"""Updates `last-update.txt`."""

from datetime import date

from env_setup import DATA_PATH


today = date.today()
formatted = f"{today.year} 年 {today.month} 月 {today.day} 日"

with open(DATA_PATH / "generated" / "last-update.txt", "w", encoding="utf-8") as f:
    f.write(formatted)
