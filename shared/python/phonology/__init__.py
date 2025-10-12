from .syllable import Syllable
from .fg import FGSyllable
from .pm import PMSyllable
from .gc import GCSyllable
from .sw import SWSyllable
from .mh import MHSyllable
from .jp import JPSyllable
from .kr import KRSyllable
from .vn import VNSyllable


# 贛官粵吳客日朝越
SYLLABLE_MAP: dict[str, type[Syllable]] = {
    "FG": FGSyllable,
    "PM": PMSyllable,
    "GC": GCSyllable,
    "SW": SWSyllable,
    "MH": MHSyllable,
    "JP": JPSyllable,
    "KR": KRSyllable,
    "VN": VNSyllable,
}


__all__ = [
    "SYLLABLE_MAP",
    "FGSyllable",
    "PMSyllable",
    "GCSyllable",
    "SWSyllable",
    "MHSyllable",
    "JPSyllable",
    "KRSyllable",
    "VNSyllable",
]
