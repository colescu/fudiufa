"""
Meixian Hakka
客語—梅縣話

Preferred: 臺灣式拼音（改動入聲尾）

Supports parsing from: ipa_raw, pinyin
"""

from .syllable import TonedSyllable


class MHSyllable(TonedSyllable):
    NAME = "梅縣話"

    IPA_TO_PINYIN_MAP = {
        "initial": {
            "": "",
            "p": "b",
            "pʰ": "p",
            "m": "m",
            "f": "f",
            "v": "v",
            "t": "d",
            "tʰ": "t",
            "n": "n",
            "l": "l",
            "k": "g",
            "kʰ": "k",
            "ŋ": "ng",
            "h": "h",
            "ts": "z",
            "tsʰ": "c",
            "s": "s",
        },
        "medial": {
            "": "",
            "j": "i",
            "w": "u",
        },
        "nucleus": {
            "a": "a",
            "o": "o",
            "e": "e",
            "i": "i",
            "ɿ": "ii",
            "ə": "ii",
            "u": "u",
        },
        "coda": {
            "": "",
            "i": "i",
            "u": "u",
            "m": "m",
            "n": "n",
            "ŋ": "ng",
            "p": "p",
            "t": "t",
            "k": "k",
        },
    }

    PINYIN_TO_IPA_MAP = {
        part: {pinyin: ipa for ipa, pinyin in dct.items()}
        for part, dct in IPA_TO_PINYIN_MAP.items()
    }

    _PALATALIZATION = {
        "k": "c",
        "kʰ": "cʰ",
        "h": "ç",
        "ŋ": "ɲ",
    }

    TONE_NOTATION_MAP = {
        "0": {"name": "輕聲"},
        "1": {"name": "陰平"},
        "2": {"name": "陽平"},
        "3": {"name": "上聲"},
        "4": {"name": "去聲"},
        "5": {"name": "陰入"},
        "6": {"name": "陽入"},
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
            case "4":
                return "去"
            case "5" | "6":
                return "入"
            case _:
                return ""

    def __post_init__(self):
        if not self.is_syllabic_nasal:
            for part in self.PARTS:
                if getattr(self, part) not in MHSyllable.IPA_TO_PINYIN_MAP[part]:
                    raise ValueError(
                        f"Illegal {part} in Meixian Hakka syllable {self.ipa_raw}: {getattr(self, part)}."
                    )
        if (
            self.tone not in MHSyllable.TONE_NOTATION_MAP
            or (self.is_checked_tone and self.tone not in "056")
            or (not self.is_checked_tone and self.tone in "56")
        ):
            raise ValueError(
                f"Illegal tone number in Meixian Hakka syllable {self.ipa_raw}: {self.tone}."
            )

    @property
    def ipa_strict_no_tone(self):
        if self.is_syllabic_nasal:
            return super().ipa_strict_no_tone
        lst = self._list_ipa_strict
        if self.initial == "v":
            lst[0] = "ʋ"
        if self.medial == "j":
            lst[0] = MHSyllable._PALATALIZATION.get(self.initial, self.initial)
        return "".join(lst)

    def pinyin(self) -> str:
        if self.is_syllabic_nasal:
            return MHSyllable.IPA_TO_PINYIN_MAP["initial"][self.initial] + self.tone
        return (
            "".join(
                MHSyllable.IPA_TO_PINYIN_MAP[part][getattr(self, part)]
                for part in self.PARTS
            )
            + self.tone
        )

    @classmethod
    def parse_ipa(cls, text: str) -> "MHSyllable":
        text = TonedSyllable.sup_to_normal(text)
        tone = text[-1]

        initial_length = 3
        while initial_length > 0:
            if text[:initial_length] in MHSyllable.IPA_TO_PINYIN_MAP["initial"]:
                break
            initial_length -= 1
        initial = text[:initial_length]

        def parse_final(final: str) -> tuple[str, str, str]:
            match len(final):
                case 3:
                    return tuple(final)
                case 2:
                    if final[1] in MHSyllable.IPA_TO_PINYIN_MAP[
                        "coda"
                    ] and final not in ["iu", "ui", "ju", "wi"]:
                        return "", *tuple(final)
                    else:
                        return *tuple(final), ""
                case 1:
                    return "", *tuple(final), ""
            return "", final, ""

        medial, nucleus, coda = parse_final(text[initial_length:-1])

        if medial == "i":
            medial = "j"
        if medial == "u":
            medial = "w"

        if tone == "5":
            tone = "4"
        if tone == "7":
            tone = "5"
        if tone == "8":
            tone = "6"

        return MHSyllable(initial, medial, nucleus, coda, tone)

    @classmethod
    def parse_pinyin(cls, text: str) -> "MHSyllable":
        """
        Examples:
            "ngiap6" -> MHSyllable("ŋ", "j", "a", "p", "6")
            "ngiab6" -> MHSyllable("ŋ", "j", "a", "p", "6")
            "ngiap" -> MHSyllable("ŋ", "j", "a", "p", "0")
        """

        tone = "0"
        if text[-1].isdigit():
            tone = text[-1]
            text = text[:-1]

        initial_length = 2
        while initial_length > 0:
            if text[:initial_length] in MHSyllable.PINYIN_TO_IPA_MAP["initial"]:
                break
            initial_length -= 1
        initial = text[:initial_length]
        final = text[initial_length:]

        def parse_final(final: str) -> tuple[str, str, str]:
            if final[:2] == "ii":
                return "", "ii", final[2:]
            match len(final) if final[-2:] != "ng" else len(final) - 1:
                case 3:
                    return final[0], final[1], final[2:]
                case 2:
                    if final[1:] in MHSyllable.PINYIN_TO_IPA_MAP[
                        "coda"
                    ] and final not in ["iu", "ui"]:
                        return "", final[0], final[1:]
                    else:
                        return final[0], final[1:], ""
                case 1:
                    return "", final, ""
            return "", final, ""

        medial, nucleus, coda = parse_final(final) if final != "" else ("", "", "")

        initial, medial, nucleus, coda = (
            MHSyllable.PINYIN_TO_IPA_MAP[part].get(val, val)
            for part, val in zip(cls.PARTS, [initial, medial, nucleus, coda])
        )

        if nucleus == "ə" and coda == "":
            nucleus = "ɿ"

        return MHSyllable(initial, medial, nucleus, coda, tone)
