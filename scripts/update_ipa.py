"""Updates parts parsed from pinyin in hanzi.sqlite3."""

from updater import Updater
from phonology import SYLLABLE_MAP


session = Updater()

for lang_en, syllable_cls in SYLLABLE_MAP.items():
    lang_cn = syllable_cls.NAME

    has_tone = lang_en not in ["JP", "KR"]

    updated, seen = [], set()

    session.cursor.execute(f"SELECT rowid, * FROM {lang_cn}")
    for row in session.data:
        syllable = syllable_cls.parse_pinyin(row["讀音"])
        new = syllable.tuple
        old = (row["聲母"], row["介音"], row["韻腹"], row["韻尾"])
        if has_tone:
            old = (*old, row["聲調"])
        if new != old and not (
            # 普通話入聲不確定聲調
            lang_en == "PM"
            and new[:4] == (row["聲母"], row["介音"], row["韻腹"], row["韻尾"])
            and new[-1] == ""
            and row["聲調"] == "0"
        ):
            session.cursor.execute(
                f"UPDATE {lang_cn} SET 聲母 = ?, 介音 = ?, 韻腹 = ?, 韻尾 = ? WHERE rowid = ?",
                (*new[:4], row["rowid"]),
            )
            if has_tone:
                session.cursor.execute(
                    f"UPDATE {lang_cn} SET 聲調 = ? WHERE rowid = ?",
                    (*new[4], row["rowid"]),
                )
            if new not in seen:
                updated.append(f"{row['讀音']}: {old} -> {new}")
                seen.add(new)

    print(f"更新{lang_cn}音標完成！共更新 {len(updated)} 個音節。")
    for item in updated:
        print("  " + item)
