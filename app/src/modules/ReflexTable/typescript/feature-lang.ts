import { mcCache, MCEntry } from "@shared/mc";
import {
  syllableUtils,
  getPart,
  partsUtils,
  renderParts,
} from "@shared/syllable";
import { Language } from "@shared/lang";
import { Feature } from "../types";

const INITIAL_GROUPS = [
  ["", "ʔ"],
  ["p", "pʰ", "b"],
  ["m"],
  ["f", "ɸ"],
  ["v", "ʋ"],
  ["t", "tʰ", "d", "ð"],
  ["n", "ɲ", "ɳ"],
  ["l"],
  ["ʈ", "ʈʰ", "ɖ"],
  ["ts", "tsʰ", "dz"],
  ["s", "z"],
  ["tɕ", "tɕʰ", "dʑ"],
  ["ɕ", "ʑ", "ʝ"],
  ["ʈʂ", "ʈʂʰ", "ɖʐ"],
  ["ʂ", "ʐ"],
  ["ɻ"],
  ["k", "kʰ", "g"],
  ["ŋ"],
  ["h", "ɦ", "ɣ"],
] as const;

export const LANG_OPTIONS_MAP = {
  聲母: [{ value: "聲母" }, { value: "類" }],
  韻母: [
    { value: "韻母" },
    { value: "韻" },
    { value: "介音" },
    { value: "韻腹" },
    { value: "韻尾" },
  ],
  聲調: [{ value: "聲調" }],
} as const;
export const LANG_FIELDS = Object.values(LANG_OPTIONS_MAP)
  .flat()
  .map((option) => option.value);
export type LangField = (typeof LANG_FIELDS)[number];

export function getLangFeature(language: Language, field: LangField): Feature {
  const { parse } = syllableUtils[language];
  const { comparer, show } = partsUtils[language];

  switch (field) {
    case "類":
      return {
        label: "類",
        getter: (entry) => {
          const initial = parse(entry.reflex[language]!).聲母;
          for (const group of INITIAL_GROUPS) {
            if ((group as any).includes(initial)) {
              const representative = group[0];

              // 尖團不分
              if (["FG", "PM", "SW"].includes(language)) {
                switch (representative) {
                  case "ts":
                  case "tɕ":
                    return "ts/tɕ";
                  case "s":
                  case "ɕ":
                    return "s/ɕ";
                }
              }

              return representative;
            }
          }
          return "";
        },
        values: INITIAL_GROUPS.map((group) => group[0]),
        shower: (value) =>
          value ? `<span class="ipa-sans">${value}</span>` : "無",
      };
    default:
      const getter = (entry: MCEntry) =>
        getPart(parse(entry.reflex[language]!), field);
      const values = [
        ...new Set(Object.values(mcCache.get()).map(getter)),
      ].sort(comparer(field));
      return {
        label: field,
        getter,
        values,
        shower: (value, settings) =>
          renderParts(show(value, field, settings.format), settings.format),
      };
  }
}

Object.values(LANG_OPTIONS_MAP)
  .flat()
  .forEach((option) => {
    (option as any)["label"] = option.value;
  });
