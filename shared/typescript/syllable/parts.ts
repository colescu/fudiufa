import { syllableDataCache } from "./cache";
import {
  computeOrdering,
  createSortComparerFromArray,
  createSortComparerFromArrays,
  precomposeComparer,
} from "../common/sort";
import { isChineseCharacter } from "../cjk";
import { Language, LANGUAGES } from "../lang";
import { AllPart, Format, PartNoTone, Syllable } from "./types";

export function getPart(syllable: Syllable, part: AllPart): string {
  switch (part) {
    // use tuple to avoid parsing
    case "韻":
      return JSON.stringify([syllable.韻腹, syllable.韻尾]);
    case "韻母":
      return JSON.stringify([syllable.介音, syllable.韻腹, syllable.韻尾]);
    default:
      return syllable[part];
  }
}

export let partsUtils = {} as Record<
  Language,
  ReturnType<typeof createPartsUtils>
>;

function createPartsUtils(
  language: Language,
  PARTS: any, // complicated
  ALL_PARTS: Record<PartNoTone, string[]>,
  TONES: {
    [tone: string]: { [label: string]: string };
  }
) {
  // CHECK Ad hoc with minimal parts.json
  // from = "ipaRaw"
  function show(value: string, part: AllPart, format: Format): string {
    if (part !== "韻母") {
      if (part === "韻") {
        const tuple = JSON.parse(value);
        value = tuple.join("");
      }
      if (part === "聲調") {
        return value + " " + TONES[value]!.name; // 例："0 輕聲"
      } else {
        const foundValue = PARTS[format]?.[part]?.[value];
        if (foundValue) {
          if (typeof foundValue === "string") {
            return foundValue;
          } else if (foundValue[language]) {
            return foundValue[language];
          } else if (foundValue["other"]) {
            return foundValue["other"];
          }
        }
        return value;
      }
    } else {
      const tuple = JSON.parse(value);
      const medial = show(tuple[0], "介音", format);
      let rhyme = show(JSON.stringify([tuple[1], tuple[2]]), "韻", format);
      if (tuple[0] != "" || (language === "PM" && format === "pinyin")) {
        rhyme = rhyme.split(/ [([]/)[0]!;
      }
      if (language === "PM" && format === "pinyin") {
        // PM pinyin spelling rules
        switch (medial + rhyme) {
          case "uen":
            return "un";
          case "uei":
            return "ui";
          case "iou":
            return "iu";
        }
      }
      return (medial === "無" ? "" : medial) + rhyme;
    }
  }

  function comparer(
    part: AllPart,
    finalOrdering: PartNoTone[] = ["韻腹", "介音", "韻尾"]
  ) {
    const partsMap = {
      韻: ["韻腹", "韻尾"],
      韻母: ["介音", "韻腹", "韻尾"],
    } as const;
    switch (part) {
      case "聲調":
        return undefined;
      case "韻":
      case "韻母":
        const parts = partsMap[part];
        return precomposeComparer(
          createSortComparerFromArrays(
            parts.map((part) => ALL_PARTS[part]),
            computeOrdering(parts as any, finalOrdering)
          ),
          JSON.parse
        );
      default:
        return createSortComparerFromArray(ALL_PARTS[part]);
    }
  }

  return { show, comparer };
}

export function initPartsUtils() {
  const TONES = syllableDataCache.get("tones");
  const PARTS = syllableDataCache.get("parts");
  const ALL_PARTS = syllableDataCache.get("all-parts");

  LANGUAGES.forEach((language) => {
    partsUtils[language] = createPartsUtils(
      language,
      PARTS,
      ALL_PARTS,
      TONES[language]
    );
  });
}

// Ad hoc HTML enriching
export function renderParts(value: string, format: Format): string {
  if (isChineseCharacter(value.slice(-1))) {
    return value;
  }

  const className = format === "pinyin" ? "pinyin" : "ipa";

  // a (b)
  const regexParenthesis = /^([^\s]+) \(([^()]+)\)$/;
  const matchParenthesis = value.match(regexParenthesis);
  if (matchParenthesis) {
    const [, a, b] = matchParenthesis;
    return `<span class="${className}">${a}</span> (<span class="${className}">${b}</span>)`;
  }

  // a [b]
  const regexSlash = /^([^\s]+) \[([^\]]+)\]$/;
  const matchSlash = value.match(regexSlash);
  if (matchSlash) {
    const [, a, b] = matchSlash;
    return `<span class="pinyin">${a}</span> [<span class="ipa">${b}</span>]`;
  }

  return `<span class="${className}">${value}</span>`;
}
