import { createCache, fetchFile } from "../cache";
import { getMCQueryUtils, MCEntry } from "../mc";
import { Language, LangEntry } from "./types";
import { getPredictedPronunciationsByEntry } from "../fg/predict";

function getMCEntry(this: Pick<LangEntry, "小韻號">): MCEntry | undefined {
  return getMCQueryUtils().entryAt(this.小韻號 ?? -1);
}

function getReflex(
  row: Pick<LangEntry, "小韻號" | "層" | "記錄讀音">,
  language: Language
): string | null {
  let reflex = getMCEntry.call(row)?.reflex[language] ?? null;

  // Ad hoc smart match stratum for reflex
  if (language === "FG" && row.小韻號 != null && row.層) {
    let index = 0;
    if (row.層.includes("白")) {
      index = 1;
    }
    if (row.層.includes("新") || row.層 === "官") {
      index = 2;
    }
    const mcEntry = getMCQueryUtils().entryAt(row.小韻號);
    if (mcEntry) {
      const predictedPronunciations =
        getPredictedPronunciationsByEntry(mcEntry);
      reflex = predictedPronunciations[index]!;
      if (
        row.層.includes("文") &&
        predictedPronunciations[2] === row.記錄讀音
      ) {
        reflex = row.記錄讀音;
      }
    }
  }

  return reflex;
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
