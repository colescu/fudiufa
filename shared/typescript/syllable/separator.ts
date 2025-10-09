import { Format } from "./types";
import { Language } from "../lang";

// Separates syllable into [initial, final, tone]
const VOWELS = "iyɨʉɯuɪʏʊeøɘɵɤoəɛœɜɞʌɔæɐaɶɑɒɿʅɚɥʮʯ" as const;
const TONES = "0123456789⁰¹²³⁴⁵⁶⁷⁸⁹˥˦˧˨˩" as const;
export function separate(
  value: string,
  format: Format,
  language: Language
): [string, string, string | undefined] {
  value = value.normalize("NFD");

  let i = 0;
  while (i < value.length) {
    const current = value[i]!;
    if (
      (VOWELS.includes(current) &&
        !(
          current === "y" &&
          format === "pinyin" &&
          (language === "PM" || (language === "SW" && i === 0))
        )) ||
      ("jw".includes(current) && format !== "pinyin") ||
      (current === "w" && format === "pinyin" && language === "GC")
    ) {
      break;
    }
    i++;
  }

  let j = i;
  while (j < value.length) {
    if (TONES.includes(value[j]!)) {
      break;
    }
    j++;
  }

  return [
    value.slice(0, i).normalize("NFC"),
    value.slice(i, j).normalize("NFC"),
    j < value.length ? value.slice(j).normalize("NFC") : undefined,
  ];
}
