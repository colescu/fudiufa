"""
Shanghai Wu
吳語—上海話

Preferred: 吳語協會式拼音

Supports parsing from: pinyin, ipa_nyoeghau
"""

from itertools import product
from functools import lru_cache
from unicodedata import normalize

from .syllable import TonedSyllable


class SWSyllable(TonedSyllable):
    NAME = "上海話"

    IPA_NYOEGHAU_TO_IPA_MAP = {
        "initial": {
            "ʔ": "",
            "p": "p",
            "pʰ": "pʰ",
            "b": "b",
            "m": "m",
            "f": "f",
            "v": "v",
            "t": "t",
            "tʰ": "tʰ",
            "d": "d",
            "n": "n",
            "ɲ": "n",  # allophone of /n/
            "l": "l",
            "ts": "ts",
            "tsʰ": "tsʰ",
            "s": "s",
            "z": "z",
            "tɕ": "tɕ",
            "tɕʰ": "tɕʰ",
            "dʑ": "dʑ",
            "ɕ": "ɕ",
            "ʑ": "ʑ",
            "k": "k",
            "kʰ": "kʰ",
            "g": "g",
            "ŋ": "ŋ",
            "h": "h",
            "ɦ": "ɦ",
        },
        "final": {
            "a": ("", "a", ""),
            "ã": ("", "a", "ŋ"),  # 打 ã ≠ 黨 ɑ̃
            "ɐʔ": ("", "a", "ʔ"),  # = ɑʔ
            "ɑ̃": ("", "ɑ", "ŋ"),
            "ɑʔ": ("", "a", "ʔ"),  # = ɐʔ
            "ia": ("j", "a", ""),
            "iã": ("j", "a", "ŋ"),  # 同 ã
            "iɑ̃": ("j", "ɑ", "ŋ"),
            "iɐʔ": ("j", "a", "ʔ"),
            "iɑʔ": ("j", "a", "ʔ"),
            "ua": ("w", "a", ""),
            "uã": ("w", "a", "ŋ"),
            "uɑ̃": ("w", "ɑ", "ŋ"),
            "uɐʔ": ("w", "a", "ʔ"),
            "o": ("", "o", ""),
            "ɔ": ("", "ɔ", ""),
            "oŋ": ("", "o", "ŋ"),
            "oʔ": ("", "o", "ʔ"),
            "io": ("j", "o", ""),  # 幾乎無字，例如 瘸
            "ioɲ": ("j", "o", "ŋ"),
            "ioʔ": ("j", "o", "ʔ"),  # 肉 ioʔ ≠ 月 yɪʔ
            "iɔ": ("j", "ɔ", ""),
            "e": ("", "e", ""),
            "ɤ": ("", "ɤ", ""),
            "æ": ("", "æ", ""),  # 來 e ≠ 蘭 æ (x)
            "əŋ": ("", "ə", "ŋ"),
            "əʔ": ("", "ə", "ʔ"),  # 袜 əʔ ≠ 麦 ɑʔ (x)
            "ie": ("j", "e", ""),
            "iɤ": ("j", "ɤ", ""),
            "ue": ("w", "e", ""),
            "uæ": ("w", "æ", ""),
            "uəŋ": ("w", "ə", "ŋ"),  # 困 uəŋ ≠ 孔 oŋ
            "uəʔ": ("w", "ə", "ʔ"),  # 骨 uəʔ ≠ 國 oʔ
            "i": ("", "i", ""),
            "iɪ": ("j", "i", ""),  # 衣 i ≠ 煙 iɪ (x)
            "iɪʔ": ("", "i", "ʔ"),
            "ɪɲ": ("", "i", "ŋ"),
            "u": ("", "u", ""),
            "y": ("", "y", ""),
            "yɪɲ": ("ɥ", "i", "ŋ"),  # 羣 yɪɲ ≠ 窮 ioŋ
            "yɪʔ": ("ɥ", "i", "ʔ"),  # 同 yɪɲ
            "ø": ("", "ø", ""),
            "yø": ("ɥ", "ø", ""),  # 園 yø ≠ 于 y
            "uø": ("w", "ø", ""),  # 官 uø ≠ 干 ø
            "z̩": ("", "ɿ", ""),
        },
    }
    # (x): merged in MCPDict data

    IPA_NYOEGHAU_PARSER = {
        initial_nyoeghau + final_nyoeghau: (initial, *final)
        for ((initial_nyoeghau, initial), (final_nyoeghau, final)) in product(
            IPA_NYOEGHAU_TO_IPA_MAP["initial"].items(),
            IPA_NYOEGHAU_TO_IPA_MAP["final"].items(),
        )
    }

    IPA_TO_PINYIN_MAP = {
        "initial": {
            "": "",
            "tɕ": "c",
            "tɕʰ": "ch",
            "dʑ": "j",
            "ɕ": "sh",
            "ʑ": "zh",
            "ŋ": "ng",
            "ɦ": "gh",
        },
        "medial": {
            "j": "i",
            "w": "u",
            "ɥ": "iu",
        },
        "nucleus": {
            "ɔ": "au",
            "ɑ": "au",
            "ɤ": "eu",
            "ə": "eu",
            "æ": "ae",
            "ø": "oe",
            "ɿ": "y",
            "y": "iu",
        },
        "coda": {
            "ŋ": "n",
            "ʔ": "h",
        },
    }

    TONE_NOTATION_MAP = {
        "0": {"name": "輕聲"},
        "1": {"name": "陰平"},
        "5": {"name": "陰去"},
        "6": {"name": "陽去"},
        "7": {"name": "陰入"},
        "8": {"name": "陽入"},
    }

    @property
    def is_syllabic_nasal(self) -> bool:
        return super().is_syllabic_nasal and self.initial in list("mŋ")

    @property
    def is_checked_tone(self) -> bool:
        return self.coda == "ʔ"

    @property
    def MC_tone(self) -> str:
        match self.tone:
            case "1":
                return "平"
            case "5" | "6":
                return "去"
            case "7" | "8":
                return "入"
            case _:
                return ""

    def __post_init__(self):
        if not self.is_syllabic_nasal and self.tuple[:-1] != ("ɦ", "", "ə", "l"):
            if (
                self.initial
                not in SWSyllable.IPA_NYOEGHAU_TO_IPA_MAP["initial"].values()
            ):
                raise ValueError(
                    f"Illegal initial in Shanghainese syllable {self.ipa_raw}: {self.initial}."
                )
            if (
                self.medial,
                self.nucleus,
                self.coda,
            ) not in SWSyllable.IPA_NYOEGHAU_TO_IPA_MAP["final"].values():
                raise ValueError(
                    f"Illegal final in Shanghainese syllable {self.ipa_raw}: {(self.medial, self.nucleus, self.coda)}."
                )
        if (
            self.tone not in SWSyllable.TONE_NOTATION_MAP
            or (self.is_checked_tone and self.tone not in "078")
            or (not self.is_checked_tone and self.tone in "78")
        ):
            raise ValueError(
                f"Illegal tone number in Shanghainese syllable {self.ipa_raw}: {self.tone}."
            )

    @property
    def ipa_strict_no_tone(self):
        if self.is_syllabic_nasal:
            return super().ipa_strict_no_tone
        lst = self._list_ipa_strict
        if self.coda == "ŋ":
            if self.nucleus in "aɑ":
                lst[2] = normalize("NFC", self.nucleus + "̃")
                lst[3] = ""
            else:
                lst[3] = "ɴ"
        if self.nucleus == "i" and self.coda == "ʔ":
            lst[2] = "ɪ"
        if self.coda == "l":
            lst[3] = "ɭ"
        return "".join(lst)

    def pinyin(self) -> str:
        if self.ipa_raw[:-1] == "ɦəl":
            return "r" + self.tone

        initial, medial, nucleus, coda = (
            SWSyllable.IPA_TO_PINYIN_MAP[part].get(
                getattr(self, part), getattr(self, part)
            )
            for part in self.PARTS
        )

        initial = initial.replace("ʰ", "h")

        if coda != "":
            if nucleus == "au":
                nucleus = "ao"
            if nucleus == "eu":
                nucleus = "e"
        final = medial + nucleus + coda
        if final == "iuoe":
            final = "ioe"

        # apply spelling rules
        if initial == "gh":
            if final[0] == "u":
                initial = "w"
                final = (
                    final[1:] if len(final) > 1 and final[1] in "aeoiu" else final[0:]
                )
            if final[0] == "i":
                initial = "y"
                final = (
                    final[1:] if len(final) > 1 and final[1] in "aeoiu" else final[0:]
                )
        if final in ["iuin", "iuih"] and initial not in "ln":
            final = final[1:]

        tone = self.tone

        return initial + final + tone

    @classmethod
    @lru_cache(maxsize=None)
    def _pinyin_parser(cls) -> dict[str, tuple[str, ...]]:
        return {
            SWSyllable(*syllable_data, "0").pinyin()[:-1]: syllable_data
            for syllable_data in SWSyllable.IPA_NYOEGHAU_PARSER.values()
        }

    @classmethod
    def parse_pinyin(cls, text: str) -> "SWSyllable":
        tone = "0"
        if text[-1].isdigit():
            tone = text[-1]
            text = text[:-1]

        if text in ["m", "n", "ng"]:
            return cls(text if text != "ng" else "ŋ", "", "", "", tone)
        if text == "r":
            return cls("ɦ", "", "ə", "l", tone)

        return cls(*SWSyllable._pinyin_parser()[text], tone)

    @classmethod
    def parse_ipa_nyoeghau(cls, text: str) -> "SWSyllable":
        """
        Constructs SWSyllable from IPA à la Nyoeghau
        (https://zhuanlan.zhihu.com/p/386456940)

        CAUTION: Some rhymes are merged.
        """

        text = TonedSyllable.sup_to_normal(text)
        tone = "0"
        if text[-1].isdigit():
            tone = text[-1]
            text = text[:-1]

        if text[0] in list("mnŋ") and text[1] in "̩":
            return cls(text[0], "", "", "", tone)

        if text == "ɦəɭ":
            return cls("ɦ", "", "ə", "l", tone)

        return cls(*SWSyllable.IPA_NYOEGHAU_PARSER[text], tone)
