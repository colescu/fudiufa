"""Updates 推導{lang} in hanzi.sqlite3 using `shared/python/predict`."""

from updater import Updater


for lang_en in ['FG', 'MH']:
    session = Updater(lang_en=lang_en)
    session.update_reflex()
    if lang_en == 'FG':
        session.compare_inventories()
    del session
