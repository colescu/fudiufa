import { syllableDataCache } from "./cache";
import { createConverter } from "./convert";
import { toneUtils } from "./tone";
import { Language, LANGUAGES } from "../lang";
import { getComparer, getIndexFinder } from "../common/sort";
import { fromEntriesConst } from "../common/object";
import { PartNoTone, Syllable, ToneNotation } from "./types";

function tupleToSyllable([
  聲母,
  介音,
  韻腹,
  韻尾,
  聲調 = "",
]: string[]): Syllable {
  return { 聲母, 介音, 韻腹, 韻尾, 聲調 } as Syllable;
}

// normal for historical, small for modern
const normalToNormalKana = {
  や: "ゃ",
  ゆ: "ゅ",
  よ: "ょ",
  ヤ: "ャ",
  ユ: "ュ",
  ヨ: "ョ",
} as const;
function convertKanaSize(kanas: string, to: "normal" | "small"): string {
  for (const [normal, small] of Object.entries(normalToNormalKana)) {
    const [before, after] = to === "small" ? [normal, small] : [small, normal];
    if (kanas.slice(1).includes(before)) {
      return kanas[0] + kanas.slice(1).replace(before, after);
    }
  }
  return kanas;
}

export let syllableUtils: Record<
  Language,
  ReturnType<typeof createSyllableUtils>
> = {} as any;

function createSyllableUtils(
  syllables: Record<string, string | string[]>[],
  ALL_PARTS: Record<PartNoTone, string[]>,
  language: Language
) {
  type Format = keyof (typeof syllables)[number];

  const convert = createConverter(syllables);
  const langToneUtils = toneUtils[language];

  let defaultPinyinFormat = "pinyin";
  if (language === "JP") {
    defaultPinyinFormat = "kata";
  }
  if (language === "KR") {
    defaultPinyinFormat = "hangul";
  }

  const historicalToModernMap: Record<string, string> = {};
  if (language === "JP") {
    for (const syllableData of syllables) {
      // only normal kanas in syllables.json
      const historical = syllableData.kata as string;
      const modern = syllableData.modern as string;
      if (!(historical in historicalToModernMap) && historical !== modern) {
        historicalToModernMap[historical] = modern;
      }
    }
  }

  function parse(value: string, format: Format = "pinyin"): Syllable {
    if (format === "pinyin") {
      format = defaultPinyinFormat;
    }
    try {
      const [syllable, tone] = langToneUtils.parse(value);
      return tupleToSyllable([...convert(syllable, format, "tuple"), tone]);
    } catch (error) {
      throw new Error(`Error parsing ${value} in format ${format}: ${error}`);
    }
  }

  function show(
    value: string,
    to: Format,
    toneNotation: ToneNotation = "ordinal",
    from: Format = "pinyin",
    historical?: boolean
  ): string {
    if (from === "pinyin") {
      from = defaultPinyinFormat;
    }
    if (toneNotation === "diacritic" && to !== "pinyin") {
      throw new Error("Diacritic tone notation is only for pinyin.");
    }

    let [syllable, tone] = langToneUtils.parse(value);

    if (language === "JP" && !historical && from !== "ipaStrict") {
      syllable = show(syllable, "kata", undefined, from, true);
      syllable = historicalToModernMap[syllable] ?? syllable;
      syllable = show(syllable, from, undefined, "kata", true);
    }

    if (to !== from) {
      try {
        syllable = convert(syllable, from, to) as string;
      } catch (error) {
        console.error(error);
      }
    }

    // fix NM duplicate pinyin
    if (language === "NM" && tone !== "5") {
      syllable = syllable.replace(/(ʔ|ʔ̚)$/, "");
    }

    if (language === "JP" && !historical) {
      syllable = convertKanaSize(syllable, "small");
    }

    if (tone === "") return syllable;

    return langToneUtils.show(syllable + tone, toneNotation);
  }

  const indexFinderMap: Record<PartNoTone, (value: string) => number> =
    fromEntriesConst(
      (["聲母", "介音", "韻腹", "韻尾"] as const).map((part) => [
        part,
        getIndexFinder(ALL_PARTS[part]),
      ])
    );

  function comparer(
    format: Format = "pinyin",
    finalOrdering: PartNoTone[] = ["韻腹", "介音", "韻尾"]
  ): (a: string, b: string) => number {
    if (format === "pinyin") {
      format = defaultPinyinFormat;
    }

    return getComparer((value: string): number[] => {
      const tuple = parse(value, format);
      return [
        ...(["聲母", ...finalOrdering] as PartNoTone[]).map((part) =>
          indexFinderMap[part](tuple[part])
        ),
        Number(tuple.聲調),
      ];
    });
  }

  return { parse, show, comparer };
}

export function initSyllableUtils() {
  const SYLLABLES = syllableDataCache.get("syllables");
  const ALL_PARTS = syllableDataCache.get("all-parts");

  syllableUtils = fromEntriesConst(
    LANGUAGES.map((language) => [
      language,
      createSyllableUtils(SYLLABLES[language], ALL_PARTS, language),
    ])
  );
}
