import { dictionaryCache, LangEntry, Language } from "@shared/lang";
import { syllableUtils, getPart, partsUtils } from "@shared/syllable";
import { getFormUtils } from "./form-utils";
import { fromEntriesConst } from "@shared/common/object";

export const ITEMS_MAP = {
  full: ["聲母", "介音", "韻腹", "韻尾", "聲調"],
  rhyme: ["聲母", "介音", "韻", "聲調"],
  final: ["聲母", "韻母", "聲調"],
} as const;
type Mode = keyof typeof ITEMS_MAP;
type Part<M extends Mode> = (typeof ITEMS_MAP)[M][number];
type Syllable<M extends Mode> = Record<Part<M>, string>;

export function getFormLangUtils<M extends Mode>(language: Language, mode: M) {
  const { parse } = syllableUtils[language];
  const { show, comparer } = partsUtils[language];

  const ITEMS = ITEMS_MAP[mode];

  const formUtils = getFormUtils<Syllable<M>, LangEntry>(
    dictionaryCache.get(language).filter((entry) => entry.記錄讀音 != null),
    fromEntriesConst(
      ITEMS.map((part) => [
        part,
        (entry: LangEntry) => getPart(parse(entry.讀音, "pinyin"), part),
      ])
    ),
    fromEntriesConst(ITEMS.map((part) => [part, comparer(part)]))
  );

  formUtils.getOptionLabel = fromEntriesConst(
    ITEMS.map((part) => [
      part,
      (format: Format) => (option: string) => show(option, part, format),
    ])
  );

  return formUtils;
}
