"""
Korean
朝鮮語

Does not support Middle Korean orthography.

Preferred: 한글
Other: Revised Romanization (RR)

Supports parsing from: hangul, RR
"""

from itertools import product
from functools import lru_cache
from copy import deepcopy

from .syllable import Syllable


# By ChatGPT
class Hangul:
    L_COMPAT = [
        "ㄱ",
        "ㄲ",
        "ㄴ",
        "ㄷ",
        "ㄸ",
        "ㄹ",
        "ㅁ",
        "ㅂ",
        "ㅃ",
        "ㅅ",
        "ㅆ",
        "ㅇ",
        "ㅈ",
        "ㅉ",
        "ㅊ",
        "ㅋ",
        "ㅌ",
        "ㅍ",
        "ㅎ",
    ]
    V_COMPAT = [
        "ㅏ",
        "ㅐ",
        "ㅑ",
        "ㅒ",
        "ㅓ",
        "ㅔ",
        "ㅕ",
        "ㅖ",
        "ㅗ",
        "ㅘ",
        "ㅙ",
        "ㅚ",
        "ㅛ",
        "ㅜ",
        "ㅝ",
        "ㅞ",
        "ㅟ",
        "ㅠ",
        "ㅡ",
        "ㅢ",
        "ㅣ",
    ]
    T_COMPAT = [
        "",
        "ㄱ",
        "ㄲ",
        "ㄳ",
        "ㄴ",
        "ㄵ",
        "ㄶ",
        "ㄷ",
        "ㄹ",
        "ㄺ",
        "ㄻ",
        "ㄼ",
        "ㄽ",
        "ㄾ",
        "ㄿ",
        "ㅀ",
        "ㅁ",
        "ㅂ",
        "ㅄ",
        "ㅅ",
        "ㅆ",
        "ㅇ",
        "ㅈ",
        "ㅊ",
        "ㅋ",
        "ㅌ",
        "ㅍ",
        "ㅎ",
    ]

    SBase = 0xAC00
    LCount = 19
    VCount = 21
    TCount = 28
    NCount = VCount * TCount

    @classmethod
    def decompose(cls, text):
        result = []
        for ch in text:
            code = ord(ch)
            if 0xAC00 <= code <= 0xD7A3:
                SIndex = code - cls.SBase
                L = SIndex // cls.NCount
                V = (SIndex % cls.NCount) // cls.TCount
                T = SIndex % cls.TCount
                result.append(cls.L_COMPAT[L])
                result.append(cls.V_COMPAT[V])
                if T != 0:
                    result.append(cls.T_COMPAT[T])
            else:
                result.append(ch)
        return result

    @classmethod
    def compose(cls, jamo):
        result = []
        i = 0
        while i < len(jamo):
            ch = jamo[i]
            if ch in cls.L_COMPAT and i + 1 < len(jamo) and jamo[i + 1] in cls.V_COMPAT:
                L = cls.L_COMPAT.index(jamo[i])
                V = cls.V_COMPAT.index(jamo[i + 1])
                T = 0
                if i + 2 < len(jamo) and jamo[i + 2] in cls.T_COMPAT:
                    T_candidate = cls.T_COMPAT.index(jamo[i + 2])
                    if T_candidate != 0:
                        T = T_candidate
                        i += 1
                syllable = chr(cls.SBase + (L * cls.NCount) + (V * cls.TCount) + T)
                result.append(syllable)
                i += 2
                if T:
                    i += 1
            else:
                result.append(ch)
                i += 1
        return "".join(result)


class KRSyllable(Syllable):
    NAME = "朝鮮語"

    PARTS = ["initial", "vowel", "coda"]

    HANGUL_TO_IPA_MAP = {
        "initial": {
            "ㅇ": "",
            "ㅂ": "p",
            "ㅍ": "pʰ",
            "ㅁ": "m",
            "ㄷ": "t",
            "ㅌ": "tʰ",
            "ㄴ": "n",
            "ㄹ": "l",
            "ㅈ": "tɕ",
            "ㅊ": "tɕʰ",
            "ㅅ": "s",
            "ㅆ": "ss",  # rare
            "ㄱ": "k",
            "ㅋ": "kʰ",
            "ㄲ": "kk",  # rare
            "ㅎ": "h",
        },
        "vowel": {
            "ㅏ": ("", "a"),
            "ㅑ": ("j", "a"),
            "ㅘ": ("w", "a"),
            "ㅐ": ("", "ɛ"),
            # "ㅒ": ("j", "ɛ"),
            "ㅙ": ("w", "ɛ"),
            "ㅔ": ("", "e"),
            "ㅖ": ("j", "e"),
            "ㅞ": ("w", "e"),
            "ㅓ": ("", "ʌ"),
            "ㅕ": ("j", "ʌ"),
            "ㅝ": ("w", "ʌ"),
            "ㅗ": ("", "o"),
            "ㅛ": ("j", "o"),
            "ㅜ": ("", "u"),
            "ㅠ": ("j", "u"),
            "ㅣ": ("", "i"),
            "ㅟ": ("w", "i"),
            "ㅡ": ("", "ɯ"),
            "ㅢ": ("ɰ", "i"),
            "ㅚ": ("", "ø"),  # we
        },
        "coda": {
            "": "",
            "ㅁ": "m",
            "ㄴ": "n",
            "ㅇ": "ŋ",
            "ㅂ": "p",
            "ㄹ": "l",
            "ㄱ": "k",
        },
    }

    IPA_TO_HANGUL_MAP = {
        part: {ipa: hangul for hangul, ipa in dct.items()}
        for part, dct in HANGUL_TO_IPA_MAP.items()
    }

    IPA_TO_RR_MAP = {
        "initial": {
            "p": "b",
            "pʰ": "p",
            "t": "d",
            "tʰ": "t",
            "l": "r",
            "tɕ": "j",
            "tɕʰ": "ch",
            "k": "g",
            "kʰ": "k",
        },
        "vowel": {
            ("w", "ʌ"): "wo",  # not weo
            ("ɰ", "i"): "ui",  # not eui
        },
        "medial": {
            "j": "y",
        },
        "nucleus": {
            "ɛ": "ae",
            "ʌ": "eo",
            "ɯ": "eu",
            "ø": "oe",
        },
        "coda": {
            "ŋ": "ng",
        },
    }

    IPA_STRICT_MAP = deepcopy(Syllable.IPA_STRICT_MAP)
    IPA_STRICT_MAP["initial"].update(
        {
            "l": "ɾ",
            "ss": "s͈",
            "kk": "k͈",
        }
    )
    IPA_STRICT_MAP["coda"].update({"l": "ɭ"})

    @property
    def vowel(self) -> tuple[str, str]:
        return (self.medial, self.nucleus)

    def __post_init__(self):
        for part in self.PARTS:
            if getattr(self, part) not in KRSyllable.HANGUL_TO_IPA_MAP[part].values():
                raise ValueError(
                    f"Illegal {part} in Korean syllable {self.ipa_raw}: {getattr(self, part)}."
                )

    @property
    def hangul(self) -> str:
        return Hangul.compose(
            [
                KRSyllable.IPA_TO_HANGUL_MAP[part][getattr(self, part)]
                for part in self.PARTS
            ]
        )

    def _ipa_to_RR(self, part: str) -> str:
        return KRSyllable.IPA_TO_RR_MAP[part].get(
            getattr(self, part), getattr(self, part)
        )

    @property
    def RR(self) -> str:
        initial, (medial, nucleus), coda = (
            self._ipa_to_RR(part) for part in self.PARTS
        )
        if self.vowel not in KRSyllable.IPA_TO_RR_MAP["vowel"]:
            medial, nucleus = self._ipa_to_RR("medial"), self._ipa_to_RR("nucleus")
        return "".join([initial, medial, nucleus, coda])

    def pinyin(self, format: str = "hangul") -> str:
        return getattr(self, format)

    @classmethod
    def parse_hangul(cls, text: str) -> "KRSyllable":
        jamos = Hangul.decompose(text)
        map_ = KRSyllable.HANGUL_TO_IPA_MAP
        initial = map_["initial"][jamos[0]]
        medial, nucleus = map_["vowel"][jamos[1]]
        coda = map_["coda"][jamos[2]] if len(jamos) > 2 else ""
        return KRSyllable(initial, medial, nucleus, coda)

    @classmethod
    @lru_cache(maxsize=None)
    def _RR_parser(cls) -> dict[str, tuple[str, ...]]:
        return {
            cls(initial, *vowel, coda).RR: (initial, *vowel, coda)
            for initial, vowel, coda in product(
                *(KRSyllable.HANGUL_TO_IPA_MAP[part].values() for part in cls.PARTS)
            )
        }

    @classmethod
    def parse_RR(cls, text: str) -> "KRSyllable":
        return cls(cls._RR_parser()[text])

    @classmethod
    def parse_pinyin(cls, text, format: str = "hangul"):
        return getattr(cls, f"parse_{format}")(text)
