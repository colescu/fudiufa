"""Updates 推導撫州話 in hanzi.sqlite3.

LATER other langs
"""

from updater import Updater


session = Updater()
session.update_reflex()
session.compare_inventories()
del session
