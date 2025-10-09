from abc import ABC, abstractmethod
from dataclasses import dataclass, fields
from typing import Type, TypeVar


T = TypeVar("T", bound="Syllable")


@dataclass(frozen=True)
class Syllable(ABC):
    initial: str
    medial: str
    nucleus: str
    coda: str

    NAME = ""

    PARTS = ["initial", "medial", "nucleus", "coda"]

    IPA_STRICT_MAP = {
        "syllabic_nasal": {
            "m": "m̩",
            "n": "n̩",
            "ŋ": "ŋ̍",
        },
        "initial": {
            "ts": "t͡s",
            "tsʰ": "t͡sʰ",
            "tɕ": "t͡ɕ",
            "tɕʰ": "t͡ɕʰ",
            "ʈʂ": "ʈ͡ʂ",
            "ʈʂʰ": "ʈ͡ʂʰ",
        },
        "nucleus": {
            "ɿ": "ɨ",  # z̩
        },
        "coda": {
            "i": "ɪ",  # i̯
            "u": "ʊ",  # u̯
            "p": "p̚",
            "t": "t̚",
            "k": "k̚",
            "ʔ": "ʔ̚",
        },
    }

    @property
    def tuple(self) -> tuple[str, ...]:
        return tuple(getattr(self, f.name) for f in fields(self))

    @property
    def ipa_raw(self) -> str:
        return "".join(self.tuple)

    @property
    def rhyme(self) -> str:
        return self.nucleus + self.coda

    @property
    def final(self) -> str:
        return self.medial + self.rhyme

    @property
    def is_syllabic_nasal(self) -> bool:
        return self.final == "" and self.initial in list("mnŋ")

    @property
    def is_checked_tone(self) -> bool:
        return self.coda in list("ptkʔl")

    @abstractmethod
    def __post_init__(self):
        """
        Checks that all parts are in the corresponding inventories and
        the tone number is legal (if exists).
        """
        pass

    @property
    def _list_ipa_strict(self) -> list[str]:
        # preliminary conversion
        return [
            self.IPA_STRICT_MAP["initial"].get(self.initial, self.initial),
            self.medial,
            self.IPA_STRICT_MAP["nucleus"].get(self.nucleus, self.nucleus),
            self.IPA_STRICT_MAP["coda"].get(self.coda, self.coda),
        ]

    @property
    def ipa_strict_no_tone(self) -> str:
        """
        For display in frontend. Saved in syllables.json.
        """
        if self.is_syllabic_nasal:
            return self.IPA_STRICT_MAP["syllabic_nasal"][self.initial]
        return "".join(self._list_ipa_strict)

    @abstractmethod
    def pinyin(self) -> str:
        """
        Gets preferred representation.
        """
        pass

    @classmethod
    @abstractmethod
    def parse_pinyin(cls: Type[T], text: str) -> T:
        """
        Constructs from preferred representation.
        """
        pass


@dataclass(frozen=True)
class TonedSyllable(Syllable):
    tone: str

    @property
    def toned_final(self) -> str:
        return self.final + self.tone

    @property
    @abstractmethod
    def MC_tone(self) -> str:
        pass

    @staticmethod
    def sup_to_normal(text: str) -> str:
        return text.translate(str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789"))
