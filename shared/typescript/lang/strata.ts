import { getMCQueryUtils, MCEntry, strataCache } from "../mc";
import { Language } from "./types";

export function getReflexMapByMC(
  mcEntry: MCEntry | number,
  language: Language
): // { stratum: pronunciation }
Record<string, string> {
  const { entryAt, indexOf } = getMCQueryUtils();

  if (typeof mcEntry === "number") {
    const entry = entryAt(mcEntry);
    if (entry === undefined) {
      console.error(`MC entry at index ${mcEntry} not found!`);
      return {};
    }
    mcEntry = entry;
  }

  const defaultReflex = mcEntry.reflex[language];
  const strata =
    (strataCache.get()[language] ?? {})[indexOf(mcEntry) ?? -1] ?? [];

  return Object.fromEntries(
    [["", defaultReflex], ...strata].filter(
      ([stratum, pronunciation]) => !!pronunciation
    )
  );
}
