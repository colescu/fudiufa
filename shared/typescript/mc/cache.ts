import { createCache, fetchFile } from "../cache";
import { showMCInfo } from "./utils";
import { MCEntry, MCInfo } from "./types";

function toMCEntry(row: Omit<MCInfo, "音韻地位">): MCInfo {
  return { ...row, 音韻地位: showMCInfo };
}

// 小韻 data, indexed by 小韻號
export const mcCache = createCache<Record<number, MCEntry>>(
  () => fetchFile("MC", "json"),
  (object: Record<number, Omit<MCEntry, "音韻地位">>) =>
    Object.fromEntries(
      Object.entries(object).map(([index, row]) => [
        index,
        { ...row, MC: toMCEntry(row.MC) },
      ])
    )
);

export const strataCache = createCache(() => fetchFile("strata", "json"));
