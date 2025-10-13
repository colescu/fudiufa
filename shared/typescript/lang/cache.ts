import { createCache, fetchFile } from "../cache";
import { getMCQueryUtils, MCEntry } from "../mc";
import { getReflexMapByMC } from "./strata";
import { Language, LangEntry } from "./types";

function getMCEntry(this: Pick<LangEntry, "小韻號">): MCEntry | undefined {
  return getMCQueryUtils().entryAt(this.小韻號 ?? -1);
}

// smart matching stratum for reflex
function getReflex(
  row: Pick<LangEntry, "小韻號" | "層" | "記錄讀音">,
  language: Language
): string | null {
  if (row.小韻號 === null) return null;
  const reflexes = Object.values(getReflexMapByMC(row.小韻號, language));

  if (row.記錄讀音 !== null) {
    if (reflexes.includes(row.記錄讀音)) return row.記錄讀音;

    for (const reflex of reflexes) {
      if (reflex.replace(/\d/g, "") === row.記錄讀音.replace(/\d/g, "")) {
        return reflex;
      }
    }
  }

  return reflexes[0] ?? null;
}

function toLangEntry(
  row: Omit<LangEntry, "讀音" | "推導讀音" | "MC" | "language">,
  language: Language
): LangEntry {
  const 推導讀音 = getReflex(row, language);
  return {
    ...row,
    推導讀音,
    讀音: row.記錄讀音 ?? 推導讀音!,
    釋義: row.釋義?.replace("~", "～") ?? null,
    get MC() {
      return getMCEntry.call(this)?.MC || null;
    },
    language,
  };
}

export const dictionaryCache = createCache(
  (language: Language) => fetchFile(language, "json"),
  (array: Omit<LangEntry, "讀音" | "MC">[], args) =>
    array.map((row) => toLangEntry(row, args![0]))
);
