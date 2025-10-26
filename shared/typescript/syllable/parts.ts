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
  PARTS: any, // complicated
  ALL_PARTS: Record<PartNoTone, string[]>,
  TONES: {
    [tone: string]: { [label: string]: string };
  },
  language: Language
) {
  // CHECK Ad hoc with minimal parts.json
  // from = "ipaRaw"
  function show(value: string, part: AllPart, format: Format): string {
    if (part !== "韻母") {
      if (part === "韻") {
        const tuple = JSON.parse(value);
        if (language === "KR") {
          const nucleus = show(tuple[0], "韻腹", format);
          const coda = show(tuple[1], "韻尾", format);
          return nucleus + (coda === "無" ? "" : coda);
        }
        value = tuple.join("");
      }
      if (part === "聲調") {
        return ["JP", "KR"].includes(language)
          ? "無"
          : value + " " + TONES[value]!.name; // 例："1 陰平"
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
      // pinyin spelling rules
      if (format === "pinyin") {
        switch (language) {
          case "PM":
            switch (medial + rhyme) {
              case "uen":
                return "un";
              case "uei":
                return "ui";
              case "iou":
                return "iu";
            }
            break;
          case "JP":
            rhyme = rhyme.replace("ii", "ī").replace("uu", "ū");
            break;
          case "KR":
            if (medial.includes("ɰ") && rhyme === "i") {
              return "ui";
            }
            if (medial === "w" && rhyme.startsWith("eo")) {
              rhyme = rhyme.replace("eo", "o");
            }
            break;
          case "VN":
            if (
              medial === "u" &&
              "aă".split("").some((nucleus) => rhyme.startsWith(nucleus))
            ) {
              return "o" + rhyme;
            }
            if (medial === "u" && rhyme.startsWith("i")) {
              return "uy" + rhyme.slice(1);
            }
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
      PARTS,
      ALL_PARTS,
      TONES[language] ?? { "": {} },
      language
    );
  });
}

// Ad hoc HTML enriching
export function renderParts(
  value: string,
  format: Format,
  language: Language
): string {
  if (isChineseCharacter(value.slice(-1))) {
    return value;
  }

  const className =
    format === "pinyin"
      ? ["JP", "KR", "VN"].includes(language)
        ? "pinyin-jkv"
        : "pinyin"
      : "ipa";

  // a (b)
  const regexParenthesis = /^([^\s]+) \(([^()]+)\)$/;
  const matchParenthesis = value.match(regexParenthesis);
  if (matchParenthesis) {
    const [, a, b] = matchParenthesis;
    if (language === "VN" && format === "ipaStrict") {
      return `<span class="${className}">${a}</span> (<span class="pinyin-vn">${b}</span>)`;
    }
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
