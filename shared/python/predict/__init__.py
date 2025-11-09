from .fg import 推導撫州話
from .mh import 推導梅縣話
from .jp_kan import 推導日本語漢音
from .jp_go import 推導日本語吳音, 推導日本語層次
from .pm_strata import 推導普通話層次
from .gc_strata import 推導廣州話層次

REFLEX_GETTER_MAP = {
    "FG": 推導撫州話,
    "MH": 推導梅縣話,
    "JP": 推導日本語漢音,
}
STRATA_GETTER_MAP = {
    "PM": 推導普通話層次,
    "GC": 推導廣州話層次,
    "JP": 推導日本語層次,
}

__all__ = [
    "REFLEX_GETTER_MAP",
    "STRATA_GETTER_MAP",
    "推導撫州話",
    "推導梅縣話",
    "推導日本語漢音",
    "推導日本語吳音",
]
