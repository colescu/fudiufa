import { getFormUtils } from "./form-utils";
import { MC_CATEGORIES, getMCQueryUtils, MCInfo } from "@shared/mc";
import { fromEntriesConst } from "@shared/common/object";
import { createSortComparerFromArray } from "@shared/common/sort";

const ITEMS = [
  "聲母",
  "清濁",
  "音",
  "組",
  "攝",
  "韻系",
  "等",
  "呼",
  "聲調",
] as const;
type Item = (typeof ITEMS)[number];
type MC = Record<Item, string>;

export function getFormMCUtils() {
  return getFormUtils<MC, MCInfo>(
    getMCQueryUtils()
      .select((_) => true)
      .map((entry) => entry.MC),
    fromEntriesConst(
      ITEMS.map((item) => [item, (syllable: MCInfo) => syllable[item]])
    ),
    fromEntriesConst(
      ITEMS.map((item) => [
        item,
        createSortComparerFromArray([...MC_CATEGORIES[item]]),
      ])
    )
  );
}
