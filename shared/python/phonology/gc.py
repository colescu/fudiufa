"""
Guangzhou Cantonese
粵語—廣州話

Preferred: 粵拼

Supports parsing from: pinyin
"""

from itertools import product

from .syllable import TonedSyllable


class GCSyllable(TonedSyllable):
    NAME = "廣州話"

    PINYIN_TO_IPA_MAP = {
        "initial": {
            "": "",
            "b": "p",
            "p": "pʰ",
            "m": "m",
            "f": "f",
            "d": "t",
            "t": "tʰ",
            "n": "n",
            "l": "l",
            "z": "ts",
            "c": "tsʰ",
            "s": "s",
            "g": "k",
            "k": "kʰ",
            "ng": "ŋ",
            "h": "h",
        },
        "medial": {
            "": "",
            "j": "j",
            "w": "w",
        },
        "nucleus": {
            "aa": "a",
            "a": "ɐ",
            "e": "ɛ",  # e before i
            "i": "i",  # ɪ before ŋ, k
            "o": "ɔ",  # o before u
            "u": "u",  # ʊ before ŋ, k
            "oe": "œ",
            "eo": "œ",  # before i, n, t
            "yu": "y",
        },
        "coda": {
            "": "",
            "i": "i",
            "u": "u",
            "m": "m",
            "n": "n",
            "ng": "ŋ",
            "p": "p",
            "t": "t",
            "k": "k",
        },
    }

    IPA_TO_PINYIN_MAP = {
        part: {ipa: pinyin for pinyin, ipa in dct.items()}
        for part, dct in PINYIN_TO_IPA_MAP.items()
    }

    _FINAL_MAP = {
        nucleus_pinyin + coda_pinyin: (nucleus_ipa, coda_ipa)
        for ((nucleus_pinyin, nucleus_ipa), (coda_pinyin, coda_ipa)) in product(
            PINYIN_TO_IPA_MAP["nucleus"].items(), PINYIN_TO_IPA_MAP["coda"].items()
        )
    }

    TONE_NOTATION_MAP = {
        "0": {"name": "輕聲"},
        "1": {"name": "陰平"},
        "2": {"name": "陰上"},
        "3": {"name": "陰去"},
        "4": {"name": "陽平"},
        "5": {"name": "陽上"},
        "6": {"name": "陽去"},
        "7": {"name": "高陰入"},
        "8": {"name": "低陰入"},
        "9": {"name": "陽入"},
    }

    _CHECKED_TONE_MAP = {
        "0": "0",
        "1": "7",
        "3": "8",
        "6": "9",
    }

    @property
    def is_syllabic_nasal(self) -> bool:
        return super().is_syllabic_nasal and self.initial in list("mŋ")

    @property
    def MC_tone(self) -> str:
        match self.tone:
            case "1" | "4":
                return "平"
            case "2" | "5":
                return "上"
            case "3" | "6":
                return "去"
            case "7" | "8" | "9":
                return "入"
            case _:
                return ""

    def __post_init__(self):
        if not self.is_syllabic_nasal:
            for part in self.PARTS:
                if (
                    getattr(self, part)
                    not in GCSyllable.PINYIN_TO_IPA_MAP[part].values()
                ):
                    raise ValueError(
                        f"Illegal {part} in Cantonese syllable {self.ipa_raw}: {getattr(self, part)}."
                    )
        if (
            self.tone not in GCSyllable.TONE_NOTATION_MAP
            or (self.is_checked_tone and self.tone not in "0789")
            or (not self.is_checked_tone and self.tone in "789")
        ):
            raise ValueError(
                f"Illegal tone number in Cantonese syllable {self.ipa_raw}: {self.tone}."
            )

    @property
    def ipa_strict_no_tone(self) -> str:
        if self.is_syllabic_nasal:
            return super().ipa_strict_no_tone
        lst = self._list_ipa_strict
        if self.nucleus != "ɐ":
            lst[2] += "ː"
        match self.nucleus:
            case "ɛ":
                if self.coda == "i":
                    lst[2] = "e"
            case "ɔ":
                if self.coda == "u":
                    lst[2] = "o"
            case "i":
                if self.coda in list("ŋk"):
                    lst[2] = "ɪ"
            case "u":
                if self.coda in list("ŋk"):
                    lst[2] = "ʊ"
            case "œ":
                if self.coda in list("int"):
                    lst[2] = "ɵ"
                if self.coda == "i":
                    lst[3] = "ʏ"
        return "".join(lst)

    def pinyin(self, separate_checked_tone: bool = False) -> str:
        """
        Example:
            GCSyllable("k", "w", "a", "ŋ", "2") -> "gwaang2"
        """

        initial, medial, nucleus, coda = (
            GCSyllable.IPA_TO_PINYIN_MAP[part].get(
                getattr(self, part), getattr(self, part)
            )
            for part in self.PARTS
        )

        tone = (
            self.tone
            if separate_checked_tone or not self.is_checked_tone
            else next(
                k for k, v in GCSyllable._CHECKED_TONE_MAP.items() if v == self.tone
            )
        )

        if self.is_syllabic_nasal:
            return initial + tone

        if initial == "" and medial == "":
            if nucleus == "i":
                medial = "j"
            if nucleus == "u" and coda not in ["ng", "k"]:  # ung, uk
                medial = "w"
        if nucleus == "eo" and coda not in list("int"):
            nucleus = "oe"

        return initial + medial + nucleus + coda + tone

    @classmethod
    def parse_pinyin(cls, text: str) -> "GCSyllable":
        """
        Example:
            "gwaang2" -> GCSyllable("k", "w", "a", "ŋ", "2")
            "gwaang" -> GCSyllable("k", "w", "a", "ŋ", "0")
        """

        tone = "0"
        if text[-1].isdigit():
            tone = text[-1]
            text = text[:-1]

        if text == "m":
            return cls("m", "", "", "", tone)
        if text == "ng":
            return cls("ŋ", "", "", "", tone)

        initial_length = 2
        while initial_length > 0:
            if text[:initial_length] in GCSyllable.PINYIN_TO_IPA_MAP["initial"]:
                break
            initial_length -= 1
        initial = GCSyllable.PINYIN_TO_IPA_MAP["initial"][text[:initial_length]]
        final = text[initial_length:]

        medial = ""
        if final[0] in list("jw"):
            medial = GCSyllable.PINYIN_TO_IPA_MAP["medial"][final[0]]
            final = final[1:]

        nucleus, coda = GCSyllable._FINAL_MAP.get(final, (final, ""))

        if (medial == "j" and nucleus == "i") or (medial == "w" and nucleus == "u"):
            medial = ""

        if coda in list("ptk"):
            tone = GCSyllable._CHECKED_TONE_MAP.get(tone, tone)

        return cls(initial, medial, nucleus, coda, tone)
