"""
Nanjing Mandarin
官話—南京話

Preferred: uliloewi 式拼音（改動介音）

Supports parsing from: pinyin
"""

from unicodedata import normalize
from copy import deepcopy

from .syllable import TonedSyllable


class NMSyllable(TonedSyllable):
    NAME = "南京話"

    PINYIN_TO_IPA_MAP = {
        "initial": {
            "": "",
            "b": "p",
            "p": "pʰ",
            "m": "m",
            "f": "f",
            "d": "t",
            "t": "tʰ",
            "l": "l",
            "g": "k",
            "k": "kʰ",
            "h": "h",  # x
            "j": "tɕ",
            "q": "tɕʰ",
            "x": "ɕ",
            "zh": "ʈʂ",
            "ch": "ʈʂʰ",
            "sh": "ʂ",
            "r": "ɻ",  # ʐ
            "z": "ts",
            "c": "tsʰ",
            "s": "s",
        },
        "final": {
            "a": ("", "a", ""),  # ɑ, ɒ
            "ia": ("j", "a", ""),
            "ua": ("w", "a", ""),
            "o": ("", "o", ""),
            "io": ("j", "o", ""),
            "e": ("", "e", ""),
            "ie": ("j", "e", ""),
            "üe": ("ɥ", "e", ""),
            "i": ("", "i", ""),
            "y": ("", "ɿ", ""),
            "u": ("", "u", ""),
            "ü": ("", "y", ""),
            "ä": ("", "ɛ", ""),  # æ, aæ
            "iä": ("j", "ɛ", ""),
            "uä": ("w", "ɛ", ""),
            "ei": ("", "ə", "i"),
            "uei": ("w", "ə", "i"),
            "ao": ("", "ɔ", ""),  # ɔo
            "iao": ("j", "ɔ", ""),
            "ou": ("", "ə", "u"),
            "iou": ("j", "ə", "u"),
            "iän": ("j", "e", "ŋ"),
            "üän": ("ɥ", "e", "ŋ"),
            "en": ("", "ə", "ŋ"),
            "uen": ("w", "ə", "ŋ"),
            "in": ("", "i", "ŋ"),
            "üin": ("ɥ", "i", "ŋ"),
            "ang": ("", "a", "ŋ"),
            "iang": ("j", "a", "ŋ"),
            "uang": ("w", "a", "ŋ"),
            "ong": ("", "o", "ŋ"),
            "iong": ("j", "o", "ŋ"),
            "er": ("", "ə", "ɻ"),
        },
    }

    IPA_TO_PINYIN_MAP = {
        part: {ipa: pinyin for pinyin, ipa in dct.items()}
        for part, dct in PINYIN_TO_IPA_MAP.items()
    }

    TONE_NOTATION_MAP = {
        "0": {"name": "輕聲", "diacritic": ""},
        "1": {"name": "陰平", "diacritic": "̀"},
        "2": {"name": "陽平", "diacritic": "́"},
        "3": {"name": "上聲", "diacritic": "̌"},
        "4": {"name": "去聲", "diacritic": "̄"},
        "5": {"name": "入聲", "diacritic": ""},
    }

    IPA_STRICT_MAP = deepcopy(TonedSyllable.IPA_STRICT_MAP)
    IPA_STRICT_MAP["initial"].update(
        {
            "h": "x",
            "ɻ": "ʐ",
        }
    )
    IPA_STRICT_MAP["nucleus"].update(
        {
            "a": "ɑ",  # ɒ̝
        }
    )

    @property
    def is_checked_tone(self) -> bool:
        return self.coda == "ʔ"

    @property
    def MC_tone(self) -> str:
        match self.tone:
            case "1" | "2":
                return "平"
            case "3":
                return "上"
            case "4":
                return "去"
            case "5":
                return "入"
            case _:
                return ""

    def __post_init__(self):
        if not self.is_syllabic_nasal:
            if self.initial not in NMSyllable.PINYIN_TO_IPA_MAP["initial"].values():
                raise ValueError(
                    f"Illegal initial in Nanjing Mandarin syllable {self.ipa_raw}: {self.initial}."
                )
            if (
                self.medial,
                self.nucleus,
                self.coda if self.coda != "ʔ" else "",
            ) not in NMSyllable.PINYIN_TO_IPA_MAP["final"].values():
                raise ValueError(
                    f"Illegal final in Nanjing Mandarin syllable {self.ipa_raw}: {(self.medial, self.nucleus, self.coda)}."
                )
        if self.tone not in NMSyllable.TONE_NOTATION_MAP:
            return ValueError(
                f"Illegal tone number in Nanjing Mandarin syllable {self.ipa_raw}: {self.tone}."
            )

    @property
    def ipa_strict_no_tone(self):
        if self.is_syllabic_nasal:
            return super().ipa_strict_no_tone
        lst = self._list_ipa_strict
        # if "".join(lst[1:4]) == "ɛʔ":
        #     lst[2] = "ə"
        if "".join(lst[2:4]) == "əu":
            lst[3] = "ɯ"
        if lst[3] == "ŋ":
            lst[3] = ""
            lst[2] = normalize("NFC", lst[2] + "̃")
        return "".join(lst)

    def pinyin(self) -> str:
        # no diacritic tone notation
        if self.is_syllabic_nasal:
            return (self.initial if self.initial != "ŋ" else "ng") + self.tone
        initial = NMSyllable.IPA_TO_PINYIN_MAP["initial"][self.initial]
        final = NMSyllable.IPA_TO_PINYIN_MAP["final"][
            (
                self.medial,
                self.nucleus,
                self.coda if not self.is_checked_tone else "",
            )
        ]
        if final == "y":
            if initial in ["zh", "ch", "sh"]:
                final = "r"
            elif initial == "r":
                final = ""
        return initial + final + self.tone

    @classmethod
    def parse_pinyin(cls, text: str) -> "NMSyllable":
        text = normalize("NFC", text)

        tone = ""
        if text[-1].isdigit():
            tone = text[-1]
            text = text[:-1]

        if text in ["m", "n", "ng"]:
            return cls(text if text != "ng" else "ŋ", "", "", "", tone)

        initial_length = 2
        while initial_length > 0:
            if text[:initial_length] in NMSyllable.PINYIN_TO_IPA_MAP["initial"]:
                break
            initial_length -= 1
        initial = NMSyllable.PINYIN_TO_IPA_MAP["initial"].get(
            text[:initial_length], text[:initial_length]
        )

        final = text[initial_length:]
        if (initial == "ɻ" and final == "") or final == "r":
            final = "y"
        medial, nucleus, coda = NMSyllable.PINYIN_TO_IPA_MAP["final"].get(
            final, ("", final, "")
        )
        if tone == "5":
            coda = "ʔ"

        return cls(initial, medial, nucleus, coda, tone)
