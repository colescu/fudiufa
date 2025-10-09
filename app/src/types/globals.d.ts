export {};

declare global {
  // settings
  type Format = "ipaRaw" | "ipaStrict" | "pinyin";
  type PinyinToneNotation = "ordinal" | "diacritic";
  type IpaToneNotation = "ordinal" | "letter" | "number";
}
