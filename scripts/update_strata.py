"""Updates `strata.json` using `shared/typescript/fg/predict`."""

import json

from updater import Updater
from predict import STRATA_GETTER_MAP


with open("data/generated/strata.json", "r", encoding="utf-8") as f:
    data = json.load(f)


def show_strata(strata: list[list[str]]) -> str:
    return "  ".join(" ".join(item) for item in strata)


for lang_en, get_strata in STRATA_GETTER_MAP.items():
    session = Updater(lang_en=lang_en)
    strata_data = data.get(lang_en, {})
    updated = []
    for index, row in session.mc_entries_map.items():
        strata = get_strata(row)
        saved_strata = strata_data.get(str(index), [])
        strata_data[index] = strata
        if len(strata) == 0:
            del strata_data[index]
        if strata != saved_strata:
            updated.append(
                f"{row['小韻號']:5d} {row['音韻地位']} {row['字']}: {show_strata(saved_strata)} -> {show_strata(strata)}"
            )
    data[lang_en] = strata_data
    print(
        f"推導{session.lang_cn}{'層次' if lang_en != 'JP' else '吳音'}完成！共更新 {len(updated)} 個小韻。"
    )
    for item in updated:
        print(item)


with open("data/generated/strata.json", "w", encoding="utf-8") as f:
    json.dump(data, f, separators=(",", ":"), ensure_ascii=False)
