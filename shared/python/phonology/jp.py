"""
Japanese
日本語

Supports historical kana orthography and conversion from historical to modern.

Preferred: カタカナ
Other: ひらがな, Nippon-shiki Romaji (NR), Hepburn Romaji (HR)

Supports parsing from: all
"""

from dataclasses import dataclass

from .syllable import Syllable


@dataclass(frozen=True)
class Kana:
    index: int

    FORMATS = ["kata", "hira", "NR", "HR", "ipa_raw"]

    CONVERSION_TABLE = [
        ["", "", ("",), "", ""],
        ["あ", "ア", ("", "", "a"), "a", "a"],
        ["い", "イ", ("", "", "i"), "i", "i"],
        ["う", "ウ", ("", "", "u"), "u", "ʉ"],
        ["え", "エ", ("", "", "e"), "e", "e"],
        ["お", "オ", ("", "", "o"), "o", "o"],
        ["や", "ヤ", ("", "j", "a"), "ya", "ja"],
        ["ゆ", "ユ", ("", "j", "u"), "yu", "jʉ"],
        ["よ", "ヨ", ("", "j", "o"), "yo", "jo"],
        ["か", "カ", ("k", "", "a"), "ka", "ka"],
        ["き", "キ", ("k", "", "i"), "ki", "ki"],
        ["く", "ク", ("k", "", "u"), "ku", "kʉ"],
        ["け", "ケ", ("k", "", "e"), "ke", "ke"],
        ["こ", "コ", ("k", "", "o"), "ko", "ko"],
        ["きゃ", "キャ", ("k", "j", "a"), "kya", "kja"],
        ["きゅ", "キュ", ("k", "j", "u"), "kyu", "kjʉ"],
        ["きょ", "キョ", ("k", "j", "o"), "kyo", "kjo"],
        ["さ", "サ", ("s", "", "a"), "sa", "sa"],
        ["し", "シ", ("s", "", "i"), "shi", "ɕi"],
        ["す", "ス", ("s", "", "u"), "su", "sʉ"],
        ["せ", "セ", ("s", "", "e"), "se", "se"],
        ["そ", "ソ", ("s", "", "o"), "so", "so"],
        ["しゃ", "シャ", ("s", "j", "a"), "sha", "ɕja"],
        ["しゅ", "シュ", ("s", "j", "u"), "shu", "ɕjʉ"],
        ["しょ", "ショ", ("s", "j", "o"), "sho", "ɕjo"],
        ["た", "タ", ("t", "", "a"), "ta", "ta"],
        ["ち", "チ", ("t", "", "i"), "chi", "t͡ɕi"],
        ["つ", "ツ", ("t", "", "u"), "tsu", "t͡sʉ"],
        ["て", "テ", ("t", "", "e"), "te", "te"],
        ["と", "ト", ("t", "", "o"), "to", "to"],
        ["ちゃ", "チャ", ("t", "j", "a"), "cha", "t͡ɕja"],
        ["ちゅ", "チュ", ("t", "j", "u"), "chu", "t͡ɕjʉ"],
        ["ちょ", "チョ", ("t", "j", "o"), "cho", "t͡ɕjo"],
        ["な", "ナ", ("n", "", "a"), "na", "na"],
        ["に", "ニ", ("n", "", "i"), "ni", "ni"],
        ["ぬ", "ヌ", ("n", "", "u"), "nu", "nʉ"],
        ["ね", "ネ", ("n", "", "e"), "ne", "ne"],
        ["の", "ノ", ("n", "", "o"), "no", "no"],
        ["にゃ", "ニャ", ("n", "j", "a"), "nya", "nja"],
        ["にゅ", "ニュ", ("n", "j", "u"), "nyu", "njʉ"],
        ["にょ", "ニョ", ("n", "j", "o"), "nyo", "njo"],
        ["は", "ハ", ("h", "", "a"), "ha", "ha"],
        ["ひ", "ヒ", ("h", "", "i"), "hi", "çi"],
        ["ふ", "フ", ("h", "", "u"), "fu", "ɸʉ"],
        ["へ", "ヘ", ("h", "", "e"), "he", "he"],
        ["ほ", "ホ", ("h", "", "o"), "ho", "ho"],
        ["ひゃ", "ヒャ", ("h", "j", "a"), "hya", "çja"],
        ["ひゅ", "ヒュ", ("h", "j", "u"), "hyu", "çjʉ"],
        ["ひょ", "ヒョ", ("h", "j", "o"), "hyo", "çjo"],
        ["ま", "マ", ("m", "", "a"), "ma", "ma"],
        ["み", "ミ", ("m", "", "i"), "mi", "mi"],
        ["む", "ム", ("m", "", "u"), "mu", "mʉ"],
        ["め", "メ", ("m", "", "e"), "me", "me"],
        ["も", "モ", ("m", "", "o"), "mo", "mo"],
        ["みゃ", "ミャ", ("m", "j", "a"), "mya", "mja"],
        ["みゅ", "ミュ", ("m", "j", "u"), "myu", "mjʉ"],
        ["みょ", "ミョ", ("m", "j", "o"), "myo", "mjo"],
        ["ら", "ラ", ("r", "", "a"), "ra", "ɾa"],
        ["り", "リ", ("r", "", "i"), "ri", "ɾi"],
        ["る", "ル", ("r", "", "u"), "ru", "ɾʉ"],
        ["れ", "レ", ("r", "", "e"), "re", "ɾe"],
        ["ろ", "ロ", ("r", "", "o"), "ro", "ɾo"],
        ["りゃ", "リャ", ("r", "j", "a"), "rya", "ɾja"],
        ["りゅ", "リュ", ("r", "j", "u"), "ryu", "ɾjʉ"],
        ["りょ", "リョ", ("r", "j", "o"), "ryo", "ɾjo"],
        ["わ", "ワ", ("", "w", "a"), "wa", "wa"],
        ["ゐ", "ヰ", ("", "w", "i"), "wi", "wi"],
        ["ゑ", "ヱ", ("", "w", "e"), "we", "we"],
        ["を", "ヲ", ("", "w", "o"), "wo", "wo"],
        ["ゐゃ", "ヰャ", ("", "wj", "a"), "wya", "wja"],
        ["ゐゅ", "ヰュ", ("", "wj", "u"), "wyu", "wjʉ"],
        ["ゐょ", "ヰョ", ("", "wj", "o"), "wyo", "wjo"],
        ["が", "ガ", ("g", "", "a"), "ga", "ga"],
        ["ぎ", "ギ", ("g", "", "i"), "gi", "gi"],
        ["ぐ", "グ", ("g", "", "u"), "gu", "gʉ"],
        ["げ", "ゲ", ("g", "", "e"), "ge", "ge"],
        ["ご", "ゴ", ("g", "", "o"), "go", "go"],
        ["ぎゃ", "ギャ", ("g", "j", "a"), "gya", "gja"],
        ["ぎゅ", "ギュ", ("g", "j", "u"), "gyu", "gjʉ"],
        ["ぎょ", "ギョ", ("g", "j", "o"), "gyo", "gjo"],
        ["ざ", "ザ", ("z", "", "a"), "za", "za"],
        ["じ", "ジ", ("z", "", "i"), "ji", "ʑi"],
        ["ず", "ズ", ("z", "", "u"), "zu", "zʉ"],
        ["ぜ", "ゼ", ("z", "", "e"), "ze", "ze"],
        ["ぞ", "ゾ", ("z", "", "o"), "zo", "zo"],
        ["じゃ", "ジャ", ("z", "j", "a"), "ja", "ʑja"],
        ["じゅ", "ジュ", ("z", "j", "u"), "ju", "ʑjʉ"],
        ["じょ", "ジョ", ("z", "j", "o"), "jo", "ʑjo"],
        ["だ", "ダ", ("d", "", "a"), "da", "da"],
        ["ぢ", "ヂ", ("d", "", "i"), "dji", "d͡ʑi"],
        ["づ", "ヅ", ("d", "", "u"), "dzu", "d͡zʉ"],
        ["で", "デ", ("d", "", "e"), "de", "de"],
        ["ど", "ド", ("d", "", "o"), "do", "do"],
        ["ぢゃ", "ヂャ", ("d", "j", "a"), "dja", "d͡ʑja"],
        ["ぢゅ", "ヂュ", ("d", "j", "u"), "dju", "d͡ʑjʉ"],
        ["ぢょ", "ヂョ", ("d", "j", "o"), "djo", "d͡ʑjo"],
        ["ば", "バ", ("b", "", "a"), "ba", "ba"],
        ["び", "ビ", ("b", "", "i"), "bi", "bi"],
        ["ぶ", "ブ", ("b", "", "u"), "bu", "bʉ"],
        ["べ", "ベ", ("b", "", "e"), "be", "be"],
        ["ぼ", "ボ", ("b", "", "o"), "bo", "bo"],
        ["びゃ", "ビャ", ("b", "j", "a"), "bya", "bja"],
        ["びゅ", "ビュ", ("b", "j", "u"), "byu", "bjʉ"],
        ["びょ", "ビョ", ("b", "j", "o"), "byo", "bjo"],
        ["ぱ", "パ", ("p", "", "a"), "pa", "pa"],
        ["ぴ", "ピ", ("p", "", "i"), "pi", "pi"],
        ["ぷ", "プ", ("p", "", "u"), "pu", "pʉ"],
        ["ぺ", "ペ", ("p", "", "e"), "pe", "pe"],
        ["ぽ", "ポ", ("p", "", "o"), "po", "po"],
        ["ぴゃ", "ピャ", ("p", "j", "a"), "pya", "pja"],
        ["ぴゅ", "ピュ", ("p", "j", "u"), "pyu", "pjʉ"],
        ["ぴょ", "ピョ", ("p", "j", "o"), "pyo", "pjo"],
        ["くわ", "クワ", ("k", "w", "a"), "kwa", "kwa"],
        # nearly no font has small ゐゑを
        ["くゐ", "クヰ", ("k", "w", "i"), "kwi", "kwi"],
        ["くゑ", "クヱ", ("k", "w", "e"), "kwe", "kwe"],
        ["くを", "クヲ", ("k", "w", "o"), "kwo", "kwo"],
        ["くゐゃ", "クヰャ", ("k", "wj", "a"), "kwya", "kwja"],
        ["くゐゅ", "クヰュ", ("k", "wj", "u"), "kwyu", "kwjʉ"],
        ["くゐょ", "クヰョ", ("k", "wj", "o"), "kwyo", "kwjo"],
        ["ぐわ", "グワ", ("g", "w", "a"), "gwa", "gwa"],
        ["ぐゐ", "グヰ", ("g", "w", "i"), "gwi", "gwi"],
        ["ぐゑ", "グヱ", ("g", "w", "e"), "gwe", "gwe"],
        ["ぐを", "グヲ", ("g", "w", "o"), "gwo", "gwo"],
        ["ぐゐゃ", "グヰャ", ("g", "wj", "a"), "gwya", "gwja"],
        ["ぐゐゅ", "グヰュ", ("g", "wj", "u"), "gwyu", "gwjʉ"],
        ["ぐゐょ", "グヰョ", ("g", "wj", "o"), "gwyo", "gwjo"],
        ["ん", "ン", ("n",), "n", "ɴ"],
        ["っ", "ッ", ("q",), "q", "Q"],
    ]

    def __post_init__(self):
        if not (0 <= self.index < len(self.CONVERSION_TABLE)):
            raise ValueError("Kana not found.")

    @property
    def _row(self):
        return self.CONVERSION_TABLE[self.index]

    @property
    def tuple(self) -> tuple[str, ...]:
        return self._row[2]

    @property
    def ipa_raw(self) -> str:
        return "".join(self.tuple)

    @property
    def hira(self) -> str:
        return self._row[0]

    @property
    def kata(self) -> str:
        return self._row[1]

    @property
    def NR(self) -> str:
        return "".join(self.tuple).replace("j", "y")

    @property
    def HR(self) -> str:
        return self._row[3]

    @property
    def ipa_strict(self) -> str:
        return self._row[4]

    def show(self, format: str):
        return getattr(self, format)

    @classmethod
    def parse(cls, text: str, format: str = "") -> "Kana":
        formats = cls.FORMATS if format == "" else [format]
        for i in range(len(cls.CONVERSION_TABLE)):
            kana = Kana(i)
            for format_ in formats:
                if getattr(kana, format_) == text:
                    return kana
        raise ValueError(f"Kana not found: {text}.")

    @staticmethod
    def small_to_normal(text: str) -> str:
        return text.translate(str.maketrans("ゃャゅュょョ", "やヤゆユよヨ"))


"""
Variations:
hira: ちょう ちよう
kata: チョウ チヨウ
NR: tyou tyō
HR: chou chō
ipa_strict: t͡ɕjoː
"""


class JPSyllable(Syllable):
    NAME = "日本語"

    CODAS = ["", "i", "u", "n", "mu", "hu", "tu", "ti", "ku", "ki", "q"]

    _LONG_VOWEL_MAP = {
        "uu": "ū",
        "ou": "ō",
        "ei": "ē",
    }
    _LONG_VOWEL_REVERSE_MAP = {v: k for k, v in _LONG_VOWEL_MAP.items()}

    @property
    def is_checked_tone(self) -> bool:
        return len(self.coda) > 0 and self.coda[0] in "htkq"

    @property
    def _is_long_vowel(self) -> bool:
        return self.nucleus + self.coda in JPSyllable._LONG_VOWEL_MAP

    @property
    def kanas(self) -> tuple[Kana, Kana]:
        return (
            Kana.parse("".join(self.initial + self.medial + self.nucleus), "ipa_raw"),
            Kana.parse(self.coda, "ipa_raw"),
        )

    def __post_init__(self):
        try:
            _ = self.kanas
        except Exception:
            raise ValueError(f"Illegal Japanese syllable: {self.tuple}.")

        if self.kanas[0].ipa_raw == "":
            raise ValueError(
                f"Illegal Japanese syllable {self.ipa_raw}: nucleus cannot be empty."
            )
        if self.coda not in JPSyllable.CODAS:
            raise ValueError(
                f"Illegal coda in Japanese syllable {self.ipa_raw}: {self.coda}."
            )

    def _show(self, format: str) -> str:
        return "".join(map(lambda kana: getattr(kana, format), self.kanas))

    @property
    def ipa_strict_no_tone(self) -> str:
        # always modern pronunciation
        syllable = JPSyllable.old_to_new(self)
        ipa = syllable._show("ipa_strict")
        if syllable._is_long_vowel:
            ipa = ipa[:-1] + "ː"
        return ipa

    @staticmethod
    def _modify_small_kana(text: str, show_small_kana: bool = True) -> str:
        return text if show_small_kana else Kana.small_to_normal(text)

    def kata(self, show_small_kana: bool = True) -> str:
        return self._modify_small_kana(self._show("kata"), show_small_kana)

    def hira(self, show_small_kana: bool = True) -> str:
        return self._modify_small_kana(self._show("hira"), show_small_kana)

    @staticmethod
    def _modify_long_vowel(text: str, show_long_vowel: bool = True) -> str:
        return (
            text
            if not show_long_vowel
            else text[:-2] + JPSyllable._LONG_VOWEL_MAP.get(text[-2:], text[-2:])
        )

    def NR(self, show_long_vowel: bool = True) -> str:
        return self._modify_long_vowel(self._show("NR"), show_long_vowel)

    def HR(self, show_long_vowel: bool = True) -> str:
        return self._modify_long_vowel(self._show("HR"), show_long_vowel)

    def pinyin(self, format: str = "kata", *args):
        return getattr(self, format)(*args)

    @classmethod
    def parse_pinyin(cls, text, format: str = ""):
        text = text[0] + text[1:].translate(
            str.maketrans("やヤゆユよヨ", "ゃャゅュょョ")
        )
        text = text[:-1] + JPSyllable._LONG_VOWEL_REVERSE_MAP.get(text[-1:], text[-1:])

        formats = Kana.FORMATS if format == "" else [format]
        for format_ in formats:
            for coda in cls.CODAS:
                try:
                    coda_form = getattr(Kana.parse(coda, "ipa_raw"), format_)
                    if text.endswith(coda_form):
                        return cls(
                            *Kana.parse(
                                text[: len(text) - len(coda_form)], format_
                            ).tuple,
                            coda,
                        )
                except Exception:
                    continue
        raise ValueError(f"Illegal Japanese syllable: {text}.")

    @classmethod
    def old_to_new(cls, syllable: "JPSyllable") -> "JPSyllable":
        """
        Converts from 歴史的仮名遣 to 現代的仮名遣.

        Example:
            JPSyllable("k", "w", "a", "hu") -> JPSyllable("k", "", "o", "u")
        """

        tuple = list(syllable.tuple)

        if tuple[1] == "w" and not (tuple[:3] == ("", "w", "a")):
            tuple[1] = ""
        if tuple[1] == "wj":
            tuple[1] = "j"

        if tuple[3] == "hu":
            tuple[3] = "u"
        if tuple[3] == "mu":
            tuple[3] = "n"

        if tuple[3] == "u":
            match tuple[2]:
                case "a":
                    tuple[2:4] = list("ou")
                case "e":
                    tuple[1:4] = list("jou")
                case "i":
                    tuple[1:4] = list("juu")

        if tuple[0] == "d" and (
            (tuple[2] == "i" or tuple[1] == "j") or tuple[2] == "u"
        ):
            tuple[0] = "z"

        return cls(*tuple)
