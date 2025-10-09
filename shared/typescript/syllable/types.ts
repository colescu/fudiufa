export type PartNoTone = "聲母" | "介音" | "韻腹" | "韻尾";
export type Part = PartNoTone | "聲調";
export type AllPart = keyof Syllable | "韻" | "韻母";
export type Syllable = Record<Part, string>;

export type Format =
  | "ipaRaw" // tɕʰjaʔ
  | "ipaStrict" // t͡ɕʰjaʔ
  | "pinyin"; // qiah

export type ToneNotation =
  | "ordinal" // a3
  | "diacritic" // â
  | "letter" // a˦˥
  | "number"; // a⁴⁵
