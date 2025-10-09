import { entriesConst, fromEntriesConst } from "@shared/common/object";
import {
  CODA_MAP,
  CODAS,
  INITIAL_GROUP_MAP,
  MC_CATEGORIES,
} from "@shared/mc/constants";
import { Feature } from "../types";
import { MCEntry } from "@shared/mc";

function asIpaSans(value: string): string {
  return `<span class="ipa-sans">${value}</span>`;
}

export const MC_OPTIONS_MAP = {
  聲母: [
    { value: "聲母" },
    { value: "組" },
    { value: "音" },
    { value: "類" },
    { value: "清濁" },
  ],
  韻母: [
    { value: "攝" },
    { value: "韻系" },
    { value: "等" },
    { value: "呼" },
    { value: "韻尾" },
  ],
  聲調: [
    { value: "聲調" },
    { value: "陰陽調" },
    { value: "平仄" },
    { value: "舒入" },
  ],
} as const;
export const MC_FIELDS = Object.values(MC_OPTIONS_MAP)
  .flat()
  .map((option) => option.value);
export type MCField = (typeof MC_FIELDS)[number];

const MC_FEATURE_MAP: Record<MCField, Feature> = {
  ...fromEntriesConst(
    entriesConst(MC_CATEGORIES).map(([item, values]) => [
      item,
      {
        label: item,
        getter: (entry: MCEntry) => entry.MC[item],
        values,
      },
    ])
  ),
  類: {
    label: "類",
    getter: (entry) => {
      const initial = entry.MC.聲母;
      for (const [initials, group] of entriesConst(INITIAL_GROUP_MAP)) {
        if (initials.includes(initial)) {
          return group;
        }
      }
      return "";
    },
    values: Object.values(INITIAL_GROUP_MAP),
    shower: asIpaSans,
  },
  韻尾: {
    label: "韻尾",
    getter: (entry) => {
      const { 攝: rhymeGroup, 聲調: tone } = entry.MC;
      for (const [rhymeGroups, group] of entriesConst(CODA_MAP)) {
        if (rhymeGroups.includes(rhymeGroup)) {
          return typeof group === "string"
            ? group
            : group[tone === "入" ? 1 : 0];
        }
      }
      return "";
    },
    values: CODAS,
    shower: asIpaSans,
  },
  陰陽調: {
    label: "陰陽調",
    getter: (entry) => {
      const { 清濁: voicing, 聲調: tone } = entry.MC;
      const register = "陰陽"["清濁".indexOf(voicing.at(-1)!)];
      if (tone === "上" && register === "陽") {
        return voicing + tone;
      }
      return register + tone;
    },
    values: [
      "陰平",
      "陽平",
      "陰上",
      "次濁上",
      "全濁上",
      "陰去",
      "陽去",
      "陰入",
      "陽入",
    ],
  },
  平仄: {
    label: "平仄",
    getter: (entry) => "平仄"[entry.MC.聲調 === "平" ? 0 : 1]!,
    values: "平仄".split(""),
  },
  舒入: {
    label: "舒入",
    getter: (entry) => "舒入"[entry.MC.聲調 === "入" ? 1 : 0]!,
    values: "舒入".split(""),
  },
};

export function getMCFeature(field: MCField): Feature {
  return MC_FEATURE_MAP[field];
}

Object.values(MC_OPTIONS_MAP)
  .flat()
  .forEach((option) => {
    (option as any)["label"] =
      ((option as any)?.label ?? option.value) +
      "：" +
      MC_FEATURE_MAP[option.value]!.values.map(
        getMCFeature((option as any)?.value)?.shower ?? ((value) => value)
      ).join(" ");
  });
