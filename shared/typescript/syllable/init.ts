import { syllableDataCache } from "./cache";
import { initToneUtils } from "./tone";
import { initPartsUtils } from "./parts";
import { initSyllableUtils } from "./syllable";

export async function initSyllableModule() {
  await syllableDataCache.loadAll([
    ["syllables"],
    ["tones"],
    ["parts"],
    ["all-parts"],
  ]);
  // the order is important
  initToneUtils();
  initPartsUtils();
  initSyllableUtils();
}
