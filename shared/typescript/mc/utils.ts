import { FINAL_MAP, MC_CATEGORIES } from "./constants";
import {
  computeOrdering,
  createSortComparerFromArrays,
  precomposeComparer,
} from "../common/sort";
import { MCEntry, MCInfo, MCInfoStyle } from "./types";

export function showFinal(
  mcInfo: Pick<MCInfo, "韻系" | "聲調">,
  finalStyle: MCInfoStyle["final"]
) {
  const finals = FINAL_MAP[mcInfo.韻系 as keyof typeof FINAL_MAP];
  switch (finalStyle) {
    case "韻系":
      return mcInfo.韻系;
    case "韻":
      return mcInfo.聲調 === "入"
        ? finals.at(-1)
        : [...finals].find((final) => final !== ".");
    case "韻目":
      return finals["平上去入".indexOf(mcInfo.聲調)];
  }
}

export const DEFAULT_MC_INFO_STYLE: MCInfoStyle = {
  ordering: ["聲母", "攝", "韻系", "等", "呼", "重紐", "聲調"],
  show: { 攝: true, 聲調: true },
  final: "韻系",
};

export function showMCInfo(
  this: Omit<MCInfo, "音韻地位">,
  style: MCInfoStyle = DEFAULT_MC_INFO_STYLE
): string {
  return style.ordering
    .filter((part) => !((style.show as any)[part] === false))
    .map((part) =>
      part === "韻系" ? showFinal(this, style.final) : this[part]
    )
    .join("");
}

// FEATURE use MC sorter
const ITEMS = ["聲母", "攝", "韻系", "等", "呼", "聲調"] as const;
export function getMCInfoComparer(itemOrdering: string[]) {
  const ordering = computeOrdering([...ITEMS], itemOrdering);
  return precomposeComparer(
    createSortComparerFromArrays(
      ITEMS.map((item) => [...MC_CATEGORIES[item]]),
      ordering
    ),
    (entry: MCEntry) => ITEMS.map((item) => entry.MC[item] as any)
  );
}
