import { useSettingsStore } from "@/stores/settings";
import { useHistoryStore } from "@/stores/history";
import { simulateVariantPost, simulateVariantPre } from "@shared/fg/variant";
import { simulateProto } from "@shared/fg/proto";
import { Language } from "@shared/lang";
import { syllableUtils, ToneNotation } from "@shared/syllable";
import { MCInfo } from "@shared/mc";

export function usePronunciation(
  language: Language,
  variant?: boolean,
  proto?: boolean
) {
  const settings = useSettingsStore();
  const history = useHistoryStore();

  const { show: showSyllable } = syllableUtils[language];

  variant ??= history.pronounce.variant.enable;
  proto ??= history.pronounce.proto.enable;

  function show(
    pronunciation: string,
    format: Format,
    sourceFormat: Format = "pinyin",
    mcInfo: MCInfo | null | undefined,
    toneNotation?: ToneNotation
  ): string {
    toneNotation ??=
      format === "pinyin" && !proto
        ? ["FG", "NM", "PM", "VN"].includes(language)
          ? settings.pinyinToneNotation
          : "ordinal"
        : settings.ipaToneNotation;
    const pinyinSettings = (settings.pinyinSettings as any)[language];

    switch (language) {
      case "FG":
        break;
      case "JP":
        return showSyllable(
          pronunciation,
          format === "pinyin" ? pinyinSettings.format : format,
          undefined,
          sourceFormat,
          pinyinSettings.historical
        );
      case "KR":
        return showSyllable(
          pronunciation,
          format === "pinyin" ? pinyinSettings.format : format,
          undefined,
          sourceFormat
        );
    }

    if (language !== "FG") {
      if (settings.unifyOrdinalTone && toneNotation === "ordinal") {
        toneNotation = "unified_ordinal" as any;
      }
      return showSyllable(pronunciation, format, toneNotation, sourceFormat);
    }

    pronunciation = showSyllable(
      pronunciation,
      "pinyin",
      "ordinal",
      sourceFormat
    );

    if (variant) {
      pronunciation = simulateVariantPre(
        pronunciation,
        mcInfo,
        history.pronounce.variant.settings
      );
    }

    if (proto) {
      format = format === "ipaRaw" ? "ipaRaw" : "ipaStrict"; // ignore format
    }

    pronunciation = showSyllable(pronunciation, format, toneNotation, "pinyin");

    if (variant && format !== "pinyin") {
      pronunciation = simulateVariantPost(
        pronunciation,
        mcInfo,
        history.pronounce.variant.settings
      );
    }

    if (proto) {
      pronunciation = simulateProto(
        pronunciation,
        mcInfo,
        history.pronounce.proto.settings
      );
    }

    return pronunciation;
  }

  return { show };
}
