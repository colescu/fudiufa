import { dictionaryCache } from "./cache";
import { LangEntry, Language } from "./types";

const langEntryIndexMaps: Record<Language, Map<LangEntry, number>> = {} as any;
const langQueryUtils: Record<
  Language,
  ReturnType<typeof createLangQueryUtils>
> = {} as any;

function createLangQueryUtils(language: Language) {
  const DICTIONARY = dictionaryCache.get(language);

  const entryIndexMap = (langEntryIndexMaps[language] ??= new Map(
    DICTIONARY.map((entry, index) => [entry, index])
  ));

  function entryAt(index: number): LangEntry | undefined {
    return DICTIONARY[index];
  }

  function indexOf(entry: LangEntry): number | undefined {
    return entryIndexMap.get(entry);
  }

  function select(filter?: (entry: LangEntry) => boolean): LangEntry[];
  function select(
    filter: ((entry: LangEntry) => boolean) | undefined,
    asIndex: true
  ): number[];
  function select(
    filter?: (entry: LangEntry) => boolean,
    asIndex: boolean = false
  ) {
    return Object.entries(DICTIONARY)
      .filter(([index, entry]) => (filter ? filter(entry) : true))
      .map(([index, entry]) => (asIndex ? Number(index) : entry));
  }

  return { entryAt, indexOf, select };
}

export function getLangQueryUtils(language: Language) {
  return (langQueryUtils[language] ??= createLangQueryUtils(language));
}
