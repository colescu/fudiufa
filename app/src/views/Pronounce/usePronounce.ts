import { useSettingsStore } from "@/stores/settings";
import { useHistoryStore } from "@/stores/history";
import { usePronunciation } from "@/composables/usePronunciation";
import { getLangQueryUtils, Language } from "@shared/lang";
import { syllableUtils } from "@shared/syllable";
import { simulateProto } from "@shared/fg/proto";
import { getLangEntries } from "../Search/typescript/search";

const OPPOSITE_STRATUM_MAP = {
  新: "老",
  文: "白",
} as const;

export function usePronounce(language: Language) {
  const settings = useSettingsStore();
  const history = useHistoryStore();

  const { entryAt, indexOf } = getLangQueryUtils(language);

  function getIndices(char: string): number[] {
    const allEntries = getLangEntries(char, language);

    let entries = allEntries.filter(
      (entry) =>
        !Object.entries(settings.dictionary.disable).some(
          ([stratum, disabled]) =>
            (disabled || history.pronounce.proto.enable) &&
            entry.層?.includes(stratum)
        ) && entry.記錄讀音 != null
    );

    if (entries.length === 0 && history.pronounce.includePredicted) {
      entries = allEntries.filter((entry) => entry.記錄讀音 == null);
    }
    return entries.map(indexOf) as number[];
  }

  function getPreferredIndex(indices: number[]): number | undefined {
    if (language !== "FG") return indices?.[0];

    const prefer = history.pronounce.prefer;

    const entries = indices.map(entryAt).filter((entry) => entry != undefined);
    let preferredEntry = undefined;

    for (const entry of entries) {
      if (
        (entry.訓作 != null && entry.訓作 !== "？") ||
        Object.entries(prefer).every(
          ([stratum, preferred]) => preferred && entry.層?.includes(stratum)
        )
      ) {
        preferredEntry = entry;
        break;
      }
    }

    if (preferredEntry === undefined) {
      for (const entry of entries) {
        if (
          Object.entries(prefer).some(
            ([stratum, preferred]) => preferred && entry.層?.includes(stratum)
          )
        ) {
          preferredEntry = entry;
          break;
        }
      }
    }

    if (preferredEntry === undefined) {
      for (const entry of entries) {
        if (
          !Object.entries(prefer).some(
            ([stratum, preferred]) =>
              preferred &&
              entry.層?.includes(
                OPPOSITE_STRATUM_MAP[
                  stratum as keyof typeof OPPOSITE_STRATUM_MAP
                ]
              )
          )
        ) {
          preferredEntry = entry;
          break;
        }
      }
    }

    if (preferredEntry === undefined) {
      preferredEntry = entries?.[0];
    }

    return preferredEntry ? indexOf(preferredEntry) : undefined;
  }

  function getDisplayedPronunciation(
    langIndex: number | null | undefined,
    format: Format
  ) {
    if (langIndex == null) return "";

    const entry = entryAt(langIndex);
    if (entry == null) return "";

    const { show } = usePronunciation(language);
    return show(entry.讀音, format, "pinyin", entry.MC, "ordinal");
  }

  return { getIndices, getPreferredIndex, getDisplayedPronunciation };
}
