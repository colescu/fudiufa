import { getLangQueryUtils, LangEntry, Language } from "@shared/lang";
import { getVariants, isChineseCharacter } from "@shared/cjk";
import { getComparer } from "@shared/common/sort";

const langEntryComparer = getComparer((entry: LangEntry): number[] => {
  return [
    entry.訓作 != null && entry.訓作 !== "？" ? -1 : 1,
    entry.小韻號 ?? Infinity,
    [
      "老",
      null,
      "老白",
      "白",
      "老文",
      "文",
      "新",
      "新文",
      "異",
      "變調",
      "官",
    ].indexOf(entry.層),
    entry.記錄讀音 ? -1 : 1,
  ];
});

// Gets ordered list of entries for character
export function getLangEntries(
  char: string,
  language: Language = "FG"
): LangEntry[] {
  if (!isChineseCharacter(char)) return [];

  const { select } = getLangQueryUtils(language);

  function getEntriesByChars(characters: string[]): LangEntry[] {
    return characters
      .map((character) =>
        select((entry) => entry.字頭 === character).sort(langEntryComparer)
      )
      .flat();
  }

  const traditionalsEntries = getEntriesByChars(
    getVariants(char, "traditional")
  );
  if (traditionalsEntries.filter(searchFilter).length > 0) {
    return traditionalsEntries;
  }

  const variantsEntries = getEntriesByChars(getVariants(char, "variant"));
  return variantsEntries;
}

// IMPORTANT: search only recorded entries
export function searchFilter(entry: LangEntry) {
  return [null, "？"].includes(entry.訓作) && entry.記錄讀音 != null;
}

export function getSearchResultsByChars(
  chars: string[],
  language: Language
): number[] {
  const { indexOf } = getLangQueryUtils(language);
  return [
    ...new Set(chars.map((char) => getLangEntries(char, language)).flat()),
  ]
    .filter(searchFilter)
    .map((entry) => indexOf(entry)!);
  // preserves order of chars
}

export function getSearchResultsByFilter(
  filter: (entry: LangEntry) => boolean,
  language: Language
): number[] {
  const { select } = getLangQueryUtils(language);
  return select((entry) => searchFilter(entry) && filter(entry), true);
  // FEATURE sorter in SearchLang, SearchMC
  // currently using database order
}
