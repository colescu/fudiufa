"""
Fuzhou Gan
贛語—撫州話

Preferred: 本人擬定的撫州話拼音

Supports parsing from: ipa_raw, pinyin
"""

from unicodedata import normalize

from .syllable import TonedSyllable


class FGSyllable(TonedSyllable):
    NAME = "撫州話"

    IPA_TO_PINYIN_MAP = {
        "initial": {
            "": "",
            "p": "b",
            "pʰ": "p",
            "m": "m",
            "f": "f",
            "t": "d",
            "tʰ": "t",
            "n": "n",
            "l": "l",
            "k": "g",
            "kʰ": "k",
            "ŋ": "ng",
            "h": "h",
            "tɕ": "j",
            "tɕʰ": "q",
            "ɕ": "x",
            "ts": "z",
            "tsʰ": "c",
            "s": "s",
        },
        "medial": {
            "": "",
            "j": "i",
            "w": "u",
            "ɥ": "y",
        },
        "nucleus": {
            "a": "a",
            "o": "o",
            "ɛ": "e",
            "i": "i",
            "ɿ": "i",
            "u": "u",
            "y": "y",
        },
        "coda": {
            "": "",
            "i": "i",
            "u": "u",
            "n": "n",
            "ŋ": "ng",
            "t": "t",
            "ʔ": "h",
        },
    }

    PINYIN_TO_IPA_MAP = {
        part: {pinyin: ipa for ipa, pinyin in dct.items()}
        for part, dct in IPA_TO_PINYIN_MAP.items()
    }

    TONE_NOTATION_MAP = {
        "0": {"name": "輕聲", "diacritic": ""},
        "1": {"name": "陰平", "diacritic": "̄"},
        "2": {"name": "陽平", "diacritic": "́"},
        "3": {"name": "上聲", "diacritic": "̂"},
        "5": {"name": "陰去", "diacritic": "̀"},
        "6": {"name": "陽去", "diacritic": "̄"},
        "7": {"name": "陰入", "diacritic": "̄"},
        "8": {"name": "陽入", "diacritic": "̂"},
    }

    _DIACRITIC_TO_TONE_MAP = {
        info["diacritic"]: tone
        for tone, info in TONE_NOTATION_MAP.items()
        if tone in "1235"
    }

    @property
    def is_syllabic_nasal(self) -> bool:
        return super().is_syllabic_nasal and self.initial in list("mŋ")

    @property
    def MC_tone(self) -> str:
        match self.tone:
            case "1" | "2":
                return "平"
            case "3":
                return "上"
            case "5" | "6":
                return "去"
            case "7" | "8":
                return "入"
            case _:
                return ""

    def __post_init__(self):
        if not self.is_syllabic_nasal:
            for part in self.PARTS:
                if getattr(self, part) not in FGSyllable.IPA_TO_PINYIN_MAP[part]:
                    raise ValueError(
                        f"Illegal {part} in Fuzhou Gan syllable {self.ipa_raw}: {getattr(self, part)}."
                    )
        if (
            self.tone not in FGSyllable.TONE_NOTATION_MAP
            or (self.is_checked_tone and self.tone not in "078")
            or (not self.is_checked_tone and self.tone in "78")
        ):
            raise ValueError(
                f"Illegal tone number in Fuzhou Gan syllable {self.ipa_raw}: {self.tone}."
            )

    @property
    def ipa_strict_no_tone(self) -> str:
        if self.is_syllabic_nasal:
            return super().ipa_strict_no_tone
        lst = self._list_ipa_strict
        if self.initial == "n" and (self.medial in "jɥ" or self.nucleus in "iy"):
            lst[0] = "ɲ"
        return "".join(lst)

    def pinyin(self, tone_diacritic: bool = False) -> str:
        """
        Gets Pinyin representation.

        Examples:
            FGSyllable("tɕʰ", "j", "a", "ŋ", "3") -> "qiâng" or "qiang3"
            FGSyllable("ŋ", "", "", "", "2") -> "ńg" or "ng2"
        """

        diacritic = FGSyllable.TONE_NOTATION_MAP[self.tone]["diacritic"]

        if self.is_syllabic_nasal:
            initial = FGSyllable.IPA_TO_PINYIN_MAP["initial"][self.initial]
            return (
                normalize("NFC", initial[0] + diacritic) + initial[1:]
                if tone_diacritic
                else initial + self.tone
            )

        initial, medial, nucleus, coda = (
            FGSyllable.IPA_TO_PINYIN_MAP[part][getattr(self, part)]
            for part in self.PARTS
        )
        return "".join(
            [
                initial,
                medial,
                normalize(
                    "NFC",
                    nucleus + diacritic,
                ),
                coda,
            ]
            if tone_diacritic
            else [initial, medial, nucleus, coda, self.tone]
        )

    @classmethod
    def parse_ipa(cls, text: str) -> "FGSyllable":
        """
        Constructs FGSyllable from raw IPA representation.

        CAUTION: Always include the tone number!

        Example:
            "tɕʰjaŋ3" -> FGSyllable("tɕʰ", "j", "a", "ŋ", "3")
        """

        initial_length = 3
        while initial_length > 0:
            if text[:initial_length] in FGSyllable.IPA_TO_PINYIN_MAP["initial"]:
                break
            initial_length -= 1
        initial = text[:initial_length]

        def parse_final(final: str) -> tuple[str, str, str]:
            match len(final):
                case 3:
                    return tuple(final)
                case 2:
                    if final[1] in FGSyllable.IPA_TO_PINYIN_MAP[
                        "coda"
                    ] and final not in ["ju", "wi", "ɥi"]:
                        return "", *tuple(final)
                    else:
                        return *tuple(final), ""
                case 1:
                    return "", *tuple(final), ""
            return "", final, ""

        medial, nucleus, coda = parse_final(text[initial_length:-1])

        tone = text[-1]

        return cls(initial, medial, nucleus, coda, tone)

    @classmethod
    def parse_pinyin(cls, text: str) -> "FGSyllable":
        """
        Constructs FGSyllable from Pinyin representation.

        CAUTION: Tone 6 is indistinguishable from Tone 1 in the diacritic
        notation. Add "6" to disambiguate.

        Examples:
            "qiāng" -> FGSyllable("tɕʰ", "j", "a", "ŋ", "1")
            "qiang" -> FGSyllable("tɕʰ", "j", "a", "ŋ", "0")
            "qiang6" -> FGSyllable("tɕʰ", "j", "a", "ŋ", "6")
            "qiāng6" -> FGSyllable("tɕʰ", "j", "a", "ŋ", "6")
        """

        text = normalize("NFD", text)
        tone = "0"
        for i in range(len(text)):
            tmp = FGSyllable._DIACRITIC_TO_TONE_MAP.get(text[i], "")
            if tmp != "":
                tone = tmp
                text = text[:i] + text[i + 1 :]
                break
        if text[-1].isdigit():
            tone = text[-1]
            text = text[:-1]

        initial_length = 2
        while initial_length > 0:
            if text[:initial_length] in FGSyllable.PINYIN_TO_IPA_MAP["initial"]:
                break
            initial_length -= 1
        initial = text[:initial_length]
        final = text[initial_length:]

        def parse_final(final: str) -> tuple[str, str, str]:
            match len(final) if final[-2:] != "ng" else len(final) - 1:
                case 3:
                    return final[0], final[1], final[2:]
                case 2:
                    if final[1:] in FGSyllable.PINYIN_TO_IPA_MAP[
                        "coda"
                    ] and final not in ["iu", "ui"]:
                        return "", final[0], final[1:]
                    else:
                        return final[0], final[1:], ""
                case 1:
                    return "", final, ""
            return "", final, ""

        medial, nucleus, coda = parse_final(final)

        initial, medial, nucleus, coda = (
            FGSyllable.PINYIN_TO_IPA_MAP[part].get(val, val)
            for part, val in zip(cls.PARTS, [initial, medial, nucleus, coda])
        )

        if nucleus == "ɿ" and not (medial == "" and initial in ["ts", "tsʰ", "s", "l"]):
            nucleus = "i"

        if coda in list("ptkʔ"):
            match tone:
                case "1":
                    tone = "7"
                case "3":
                    tone = "8"

        return cls(initial, medial, nucleus, coda, tone)
