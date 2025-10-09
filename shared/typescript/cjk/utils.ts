import { commonCharactersCache, s2tCache, variantsCache } from "./cache";
import { getComparer } from "../common/sort";
import { Range } from "./types";

export function isChineseCharacter(char: string): boolean {
  const chineseRegex = /\p{Script=Han}/u; // CJK ideographs
  const punctuationRegex = /[\u3000-\u303F\uFF00-\uFFEF\u2000-\u206F]/; // CJK punctuation marks
  return chineseRegex.test(char) && !punctuationRegex.test(char);
}

import * as OpenCC from "opencc-js/core";
import { from, to } from "opencc-js/preset";
export const simplifier = OpenCC.ConverterFactory(from.hk, to.cn);

// frequency by order in 通用规范汉字表
function getFrequency(char: string): number {
  const commonCharacters = commonCharactersCache.get();
  const index = commonCharacters.indexOf(simplifier(char));
  return index === -1 ? Infinity : index;
}

export const characterComparer = getComparer(
  (char: string | null | undefined) => getFrequency(char ?? "□")
);

export function getVariants(char: string, range: Range = "variant"): string[] {
  if (range === null) return [char];

  const S2T = s2tCache.get();
  const traditionals = S2T[char] ?? [char];
  if (range === "traditional") return traditionals;

  const VARIANTS = variantsCache.get();
  const variants = traditionals;
  for (const row of VARIANTS) {
    if (row.includes(char)) {
      for (const c of [...row].sort(characterComparer)) {
        if (!variants.includes(c)) {
          variants.push(c);
        }
      }
      break;
    }
  }
  return variants;
}
