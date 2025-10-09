"""
Putonghua Mandarin
官話—普通話

Preferred representation: 拼音

Supports parsing from: pinyin
"""

from unicodedata import normalize

from .syllable import TonedSyllable


class PMSyllable(TonedSyllable):
    NAME = "普通話"

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
            "g": "k",
            "k": "kʰ",
            "h": "h",  # x
            "j": "tɕ",
            "q": "tɕʰ",
            "x": "ɕ",
            "zh": "ʈʂ",
            "ch": "ʈʂʰ",
            "sh": "ʂ",
            "r": "ɻ",
            "z": "ts",
            "c": "tsʰ",
            "s": "s",
        },
        "final": {
            "a": ("", "a", ""),
            "ia": ("j", "a", ""),
            "ua": ("w", "a", ""),
            "o": ("", "o", ""),
            "uo": ("w", "o", ""),
            "e": ("", "ɤ", ""),
            "ie": ("j", "e", ""),
            "üe": ("ɥ", "e", ""),
            "i": ("", "i", ""),  # or ɿ
            "u": ("", "u", ""),
            "ü": ("", "y", ""),
            "ai": ("", "a", "i"),
            "uai": ("w", "a", "i"),
            "ei": ("", "e", "i"),
            "ui": ("w", "e", "i"),
            "uei": ("w", "e", "i"),  # wei vs kui
            "ao": ("", "a", "u"),
            "iao": ("j", "a", "u"),
            "ou": ("", "o", "u"),
            "iu": ("j", "o", "u"),
            "iou": ("j", "o", "u"),  # you vs qiu
            "an": ("", "a", "n"),
            "ian": ("j", "e", "n"),
            "uan": ("w", "a", "n"),
            "üan": ("ɥ", "e", "n"),
            "en": ("", "ə", "n"),
            "un": ("w", "ə", "n"),
            "uen": ("w", "ə", "n"),  # wen vs kun
            "in": ("", "i", "n"),
            "ün": ("", "y", "n"),
            "ang": ("", "a", "ŋ"),
            "iang": ("j", "a", "ŋ"),
            "uang": ("w", "a", "ŋ"),
            "eng": ("", "ə", "ŋ"),
            "ueng": ("w", "ə", "ŋ"),  # only weng
            "ing": ("", "i", "ŋ"),
            "ong": ("", "ʊ", "ŋ"),
            "iong": ("j", "ʊ", "ŋ"),
            "er": ("", "ə", "ɻ"),
        },
    }

    IPA_TO_PINYIN_MAP = {
        part: {ipa: pinyin for pinyin, ipa in dct.items()}
        for part, dct in PINYIN_TO_IPA_MAP.items()
    }

    TONE_NOTATION_MAP = {
        "0": {"name": "輕聲", "diacritic": ""},
        "1": {"name": "陰平", "diacritic": "̄"},
        "2": {"name": "陽平", "diacritic": "́"},
        "3": {"name": "上聲", "diacritic": "̌"},
        "4": {"name": "去聲", "diacritic": "̀"},
    }

    _DIACRITIC_TO_TONE_MAP = {
        info["diacritic"]: tone
        for tone, info in TONE_NOTATION_MAP.items()
        if tone in "1234"
    }

    @property
    def is_syllabic_nasal(self) -> bool:
        return super().is_syllabic_nasal and self.initial == "ŋ"

    @property
    def MC_tone(self) -> str:
        match self.tone:
            case "1" | "2":
                return "平"
            case "3":
                return "上"
            case "4":
                return "去"
            case _:
                return ""

    def __post_init__(self):
        if not self.is_syllabic_nasal:
            if self.initial not in PMSyllable.PINYIN_TO_IPA_MAP["initial"].values():
                raise ValueError(
                    f"Illegal initial in Putonghua syllable {self.ipa_raw}: {self.initial}."
                )
            if (
                self.medial,
                self.nucleus if self.nucleus != "ɿ" else "i",
                self.coda,
            ) not in PMSyllable.PINYIN_TO_IPA_MAP["final"].values():
                raise ValueError(
                    f"Illegal final in Putonghua syllable {self.ipa_raw}: {(self.medial, self.nucleus, self.coda)}."
                )
        if self.tone not in "01234":  # tone == "" is allowed in expected reflexes
            return ValueError(
                f"Illegal tone number in Putonghua syllable {self.ipa_raw}: {self.tone}."
            )

    @property
    def ipa_strict_no_tone(self):
        if self.is_syllabic_nasal:
            return super().ipa_strict_no_tone
        lst = self._list_ipa_strict
        if self.initial == "h":
            lst[0] = "x"
        if self.nucleus == "u" and self.coda == "ŋ":
            lst[2] = "ʊ"
        if "".join(lst[1:4]) in ["jen", "ɥen"]:
            lst[2] = "ɛ"
        return "".join(lst)

    def pinyin(self, tone_diacritic: bool = False) -> str:
        """
        Example:
            PMSyllable("tɕʰ", "j", "o", "u", "1") -> "qiū" or "qiu1"
        """

        diacritic = (
            PMSyllable.TONE_NOTATION_MAP[self.tone]["diacritic"]
            if self.tone != ""
            else ""
        )

        if self.is_syllabic_nasal:
            return (
                (normalize("NFC", "n" + diacritic) + "g")
                if tone_diacritic
                else "ng" + self.tone
            )

        initial = PMSyllable.IPA_TO_PINYIN_MAP["initial"][self.initial]
        final = PMSyllable.IPA_TO_PINYIN_MAP["final"][
            (self.medial, self.nucleus if self.nucleus != "ɿ" else "i", self.coda)
        ]

        # apply spelling rules
        if initial == "":
            if final[0] == "i":
                if len(final) == 1 or final[1] not in "aoeiu":
                    final = "yi" + final[1:]
                else:
                    final = "y" + final[1:]
            if final[0] == "u":
                if len(final) == 1 or final[1] not in "aoeiu":
                    final = "wu"
                else:
                    final = "w" + final[1:]
            if final[0] == "ü":
                final = "yu" + final[1:]
        if initial in list("jqx") and final[0] == "ü":
            final = "u" + final[1:]
        if initial != "":
            if final == "uei":
                final = "ui"
            if final == "iou":
                final = "iu"
            if final == "uen":
                final = "un"

        if not tone_diacritic:
            return initial + final + self.tone

        position = len(final) - 1
        while position >= 0 and final[position] not in "aoeiuü":
            position -= 1
        if position > 0 and final[position] in "iu" and final[position - 1] in "aoe":
            position -= 1
        if final[-2:] == "ao":
            position -= 1
        final = normalize(
            "NFC", final[: position + 1] + diacritic + final[position + 1 :]
        )

        return initial + final

    @classmethod
    def parse_pinyin(cls, text: str) -> "PMSyllable":
        """
        CAUTION: tone == "" is allowed. Add "0" for 輕聲.

        Examples:
            "qiu" -> PMSyllable("tɕʰ", "j", "o", "u", "")
            "qiū" -> PMSyllable("tɕʰ", "j", "o", "u", "1")
            "qiu0" -> PMSyllable("tɕʰ", "j", "o", "u", "0")
        """

        text = normalize("NFD", text)
        tone = ""
        if text[-1].isdigit():
            tone = text[-1]
            text = text[:-1]
        else:
            for i in range(len(text)):
                if text[i] in PMSyllable._DIACRITIC_TO_TONE_MAP:
                    tone = PMSyllable._DIACRITIC_TO_TONE_MAP[text[i]]
                    text = text[:i] + text[i + 1 :]
                    break
        text = normalize("NFC", text)  # for ü

        if text == "ng":
            return cls("ŋ", "", "", "", tone)

        # reverse spelling rules
        if text[:2] == "yu":
            text = "ü" + text[2:]
        if text[0] == "y":
            if text[1] == "i":
                text = text[1:]
            else:
                text = "i" + text[1:]
        if text[0] == "w":
            if text[1] == "u":
                text = text[1:]
            else:
                text = "u" + text[1:]
        if text[0] in "jqx" and text[1] == "u":
            text = text[0] + "ü" + text[2:]

        initial_length = 2
        while initial_length > 0:
            if text[:initial_length] in PMSyllable.PINYIN_TO_IPA_MAP["initial"]:
                break
            initial_length -= 1
        initial = PMSyllable.PINYIN_TO_IPA_MAP["initial"].get(
            text[:initial_length], text[:initial_length]
        )
        final = text[initial_length:]
        medial, nucleus, coda = PMSyllable.PINYIN_TO_IPA_MAP["final"].get(
            final, ("", final, "")
        )

        if nucleus == "i" and initial in ["ts", "tsʰ", "s", "ʈʂ", "ʈʂʰ", "ʂ", "ɻ"]:
            nucleus = "ɿ"

        return cls(initial, medial, nucleus, coda, tone)
