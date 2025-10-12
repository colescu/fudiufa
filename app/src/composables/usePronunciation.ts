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
        ? ["FG", "PM"].includes(language)
          ? settings.pinyinToneNotation
          : "ordinal"
        : settings.ipaToneNotation;

    if (language !== "FG") {
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
        showSyllable(pronunciation, format, toneNotation, "pinyin"),
        mcInfo,
        history.pronounce.proto.settings
      );
    }

    return pronunciation;
  }

  return { show };
}
