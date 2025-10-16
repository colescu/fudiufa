import { AllPart, getPart, syllableUtils } from "../syllable";
import { dictionaryCache } from "./cache";
import { Language } from "./types";

// add more on demand
export function getPhonologicalInventory(language: Language) {
  const { parse } = syllableUtils[language];
  const ALL_SYLLABLES = [
    ...new Set(dictionaryCache.get(language).map((entry) => entry.讀音)),
  ];

  return {
    get(part: AllPart) {
      return [
        ...new Set(
          ALL_SYLLABLES.map((syllable) =>
            getPart(parse(syllable, "pinyin"), part)
          )
        ),
      ]; // unsorted
    },
  };
}
