"""
Vietnamese
越南語

Preferred: standard orthography

Supports parsing from: pinyin
"""

from unicodedata import normalize
from copy import deepcopy

from .syllable import TonedSyllable


class VNSyllable(TonedSyllable):
    NAME = "越南語"

    PINYIN_TO_IPA_MAP = {
        "initial": {
            "": "",
            "b": "b",
            "m": "m",
            "ph": "f",
            "v": "v",
            "t": "t",
            "th": "tʰ",
            "đ": "d",
            "d": "ð",  # z
            "n": "n",
            "nh": "ɲ",
            "l": "l",
            "ch": "tɕ",
            "x": "ɕ",  # s
            "gi": "ʝ",  # z
            "tr": "ʈʂ",  # tɕ
            "s": "ʂ",  # s
            "k": "k",  # before e, ê, i, y
            "q": "k",  # before u
            "c": "k",
            "ngh": "ŋ",  # before e, ê, i, y
            "ng": "ŋ",
            "kh": "x",
            # "gh": "ɣ", # before e, ê, i, y
            # "g": "ɣ",
            "h": "h",
        },
        "rhyme": {
            "ao": ("a", "u"),
            "eo": ("ɛ", "u"),
            "ây": ("ʌ", "i"),
            # "ay": ("ɐ", "i"),
            # "au": ("ɐ", "w"),
        },
        "medial": {
            "": "",
            "i": "j",
            "u": "w",
        },
        "nucleus": {
            "a": "a",
            "ă": "ɐ",  # ă
            "ơ": "ɤ",
            "â": "ʌ",  # ɤ̆, ə̆
            "ư": "ɯ",  # ɨ
            "e": "ɛ",
            "ê": "e",
            "y": "i",
            "i": "i",
            "o": "ɔ",
            "ô": "o",
            "u": "u",
            "iê": "iə",  # ie
            "ươ": "ɯə",  # ɯɤ
            "uô": "uə",  # uo
        },
        "coda": {
            "": "",
            "i": "i",
            "u": "u",
            "m": "m",
            "n": "n",
            "ng": "ŋ",
            "nh": "ɲ",  # ŋ̟
            "p": "p",
            "t": "t",
            "c": "k",
            "ch": "c",  # k̟
        },
    }

    """
    The pronunciation of quô-/qua is tricky.
    Sino-Vietnamese only has qua /kwa/, quôc /kuək/.
    """

    IPA_TO_PINYIN_MAP = {
        part: {ipa: pinyin for pinyin, ipa in dct.items()}
        for part, dct in PINYIN_TO_IPA_MAP.items()
    }

    TONE_NOTATION_MAP = {
        "1": {"name": "陰平", "diacritic": ""},
        "2": {"name": "陽平", "diacritic": "̀"},
        "3": {"name": "陰上", "diacritic": "̉"},
        "4": {"name": "陽上", "diacritic": "̃"},
        "5": {"name": "陰去", "diacritic": "́"},
        "6": {"name": "陽去", "diacritic": "̣"},
    }

    _DIACRITIC_TO_TONE_MAP = {
        info["diacritic"]: tone for tone, info in TONE_NOTATION_MAP.items()
    }

    IPA_STRICT_MAP = deepcopy(TonedSyllable.IPA_STRICT_MAP)
    IPA_STRICT_MAP["initial"].update(
        {
            "b": "ʔɓ",
            "d": "ʔɗ",
            "ɕ": "s",
            "ʂ": "s",
            "ð": "z",
            "ʝ": "z",
            "ʈʂ": "t͡ɕ",
        }
    )
    IPA_STRICT_MAP["coda"].update(
        {
            "ɲ": "ŋ̟",
            "c": "k̟̚",
        }
    )

    @property
    def is_checked_tone(self) -> bool:
        return self.coda in list("ptk") + ["k̟"]

    @property
    def VN_tone(self) -> str:
        if self.is_checked_tone:
            return str(int(self.tone) - 2)
        return self.tone

    @property
    def MC_tone(self) -> str:
        match self.tone:
            case "1" | "2":
                return "平"
            case "3" | "4":
                return "上"
            case "5" | "6":
                return "去"
            case "7" | "8":
                return "入"

    def __post_init__(self):
        for part in self.PARTS:
            if getattr(self, part) not in VNSyllable.PINYIN_TO_IPA_MAP[part].values():
                raise ValueError(
                    f"Illegal {part} in Vietnamese syllable {self.ipa_raw}: {getattr(self, part)}."
                )
        if (
            self.tone not in VNSyllable.TONE_NOTATION_MAP and self.tone not in "78"
        ) or (self.is_checked_tone and self.tone not in "78"):
            raise ValueError(
                f"Illegal tone number in Vietnamese syllable {self.ipa_raw}: {self.tone}."
            )

    @property
    def ipa_strict_no_tone(self) -> str:
        lst = self._list_ipa_strict

        if lst[3] in ["ŋ̟", "k̚"]:
            if lst[2] == "a":
                lst[2] = "ɐɪ"
            if lst[2] == "e":
                lst[2] = "ʌɪ"
        if lst[3] in ["ŋ", "k̟̚"]:
            if lst[2] == "ɔ":
                lst[2] = "ɐʊ"
            if lst[2] == "o":
                lst[2] = "ʌʊ"

        if len(lst[2]) == 2:
            lst[2] = lst[2][0] + "ə̯"

        if lst[2][-1] in "uoɔ":
            if lst[3] == "ŋ":
                lst[3] = "ŋ͡m"  # ŋʷ
            if lst[3] == "k̚":
                lst[3] = "k͡p̚"  # k̚ʷ

        return "".join(lst)  # TODO: strict IPA

    def pinyin(self, tone_diacritic: bool = True) -> str:
        """
        Example:
            VNSyllable("k", "w", "o", "k", "7") -> "quốc" or "quôc5"
        """
        diacritic = VNSyllable.TONE_NOTATION_MAP[self.VN_tone]["diacritic"]

        initial, medial, nucleus, coda = (
            VNSyllable.IPA_TO_PINYIN_MAP[part][getattr(self, part)]
            for part in self.PARTS
        )

        # apply spelling rules

        if initial == "c":
            if medial == "u" or (nucleus == "uô" and coda == "c"):
                initial = "q"
            if (medial + nucleus)[0] in "eêiy":
                initial = "k"
        if initial == "ng" and (medial + nucleus)[0] in "eêiy":
            initial = "ngh"

        if initial == "":
            if medial == "i":
                medial = "y"
            if nucleus[0] == "i" and len(nucleus) > 1:
                nucleus = "y" + nucleus[1:]
        if medial == "u" and nucleus in "aăe" and initial != "q":
            medial = "o"
        if medial == "u" and nucleus[0] == "i":
            nucleus = "y" + nucleus[1:]
        if len(nucleus) == 2 and coda == "":
            nucleus = nucleus[:-1] + "a"

        if coda == "u" and nucleus in "ae":
            coda = "o"
        if coda == "i" and nucleus == "â":
            coda = "y"

        # only in Sino-Vietnamese
        if initial + medial + coda == "" and nucleus == "i":
            nucleus = "y"

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
            else [initial, medial, nucleus, coda, self.VN_tone]
        )

    @classmethod
    def parse_pinyin(cls, text) -> "VNSyllable":
        """
        Examples:
            "quốc" -> VNSyllable("k", "w", "o", "k", "7")
            "quôc5" -> VNSyllable("k", "w", "o", "k", "7")
            "quôcs" -> VNSyllable("k", "w", "o", "k", "7")
        """

        text = normalize("NFD", text)
        tone = "1"
        for i in range(len(text)):
            tmp = VNSyllable._DIACRITIC_TO_TONE_MAP.get(text[i], "")
            if tmp != "":
                tone = tmp
                text = text[:i] + text[i + 1 :]
                break
        if text[-1].isdigit():
            tone = text[-1]
            text = text[:-1]
        if text[-1] in "frxsj":
            tone = str("frxsj".index(text[-1]) + 2)
            text = text[:-1]
        text = normalize("NFC", text)

        map_ = VNSyllable.PINYIN_TO_IPA_MAP

        initial_length = 3
        while initial_length > 0:
            if text[:initial_length] in map_["initial"]:
                break
            initial_length -= 1
        initial = map_["initial"][text[:initial_length]]
        final = text[initial_length:]

        coda_length = min(len(final) - 1, 2)
        while coda_length > 0:
            if final[len(final) - coda_length :] in map_["coda"]:
                break
            coda_length -= 1
        coda = map_["coda"][final[len(final) - coda_length :]]
        vowel = final[: len(final) - coda_length]

        medial, nucleus = "", vowel

        # reverse spelling rules

        if nucleus[0] == "y":
            nucleus = "i" + nucleus[1:]
        if nucleus[:2] == "uy":
            medial, nucleus = "u", "i" + nucleus[2:]
        if coda == "" and nucleus in ["ia", "ưa", "ua"]:
            nucleus = nucleus[0] + "êơô"["iưu".index(nucleus[0])]

        match nucleus:
            case _ if nucleus[-2:] in map_["rhyme"]:
                nucleus, coda = map_["rhyme"][nucleus[-2:]]
            case _ if (
                len(nucleus) > 1 and nucleus[0] == "o" and nucleus[1] in list("aăe")
            ):
                medial, nucleus = "u", nucleus[1:]
            case _ if (
                nucleus not in ["iê", "ươ", "uô"]
                and len(nucleus) > 1
                and nucleus[0] in list("iu")
            ):
                medial, nucleus = nucleus[0], nucleus[1:]

        medial, nucleus = map_["medial"][medial], map_["nucleus"].get(nucleus, nucleus)

        # qua
        if text[:2] == "qu" and nucleus == "uə" and coda == "":
            medial, nucleus = "w", "a"

        if coda in list("ptk") + ["k̟"]:
            tone = str(int(tone) + 2)

        return cls(initial, medial, nucleus, coda, tone)
