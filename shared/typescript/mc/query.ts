import { mcCache } from "./cache";
import { MCEntry } from "./types";

let mcEntryIndexMap: Map<MCEntry, number> = null as any;
let mcQueryUtils: ReturnType<typeof createMCQueryUtils> = null as any;

function createMCQueryUtils() {
  const MC_ENTRIES_MAP = mcCache.get();

  mcEntryIndexMap ??= new Map(
    Object.entries(MC_ENTRIES_MAP).map(([index, entry]) => [
      entry,
      Number(index),
    ])
  );

  function entryAt(index: number): MCEntry | undefined {
    return MC_ENTRIES_MAP[index];
  }

  function indexOf(entry: MCEntry): number | undefined {
    return mcEntryIndexMap.get(entry);
  }

  function select(filter?: (entry: MCEntry) => boolean): MCEntry[];
  function select(
    filter: ((entry: MCEntry) => boolean) | undefined,
    asIndex: true
  ): number[];
  function select(
    filter?: (entry: MCEntry) => boolean,
    asIndex: boolean = false
  ) {
    return Object.entries(MC_ENTRIES_MAP)
      .filter(([index, entry]) => (filter ? filter(entry) : true))
      .map(([index, entry]) => (asIndex ? Number(index) : entry));
  }

  return { entryAt, indexOf, select };
}

export function getMCQueryUtils() {
  return (mcQueryUtils ??= createMCQueryUtils());
}
