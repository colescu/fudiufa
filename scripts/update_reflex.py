"""Updates 推導{lang} in `hanzi.sqlite3` using `shared/python/predict`."""

from updater import Updater


for lang_en in ["FG", "MH", "JP"]:
    session = Updater(lang_en=lang_en)
    session.update_reflex()
    # session.compare_inventories()
    del session
