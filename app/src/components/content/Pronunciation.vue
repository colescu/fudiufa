<script setup lang="ts">
import { computed, ref } from "vue";
import { useSettingsStore } from "@/stores/settings";
import { useHistoryStore } from "@/stores/history";
import { useAudio } from "@/composables/useAudio";
import { syllableUtils, separate } from "@shared/syllable";
import { simulateProtoPronunciation } from "@shared/fg/proto-fg";
import { MCInfo } from "@shared/mc";
import { Language } from "@shared/lang";

const settings = useSettingsStore();
const history = useHistoryStore();

export type DefaultProps = {
  sourceFormat?: Format;
  language?: Language;
  noAudio?: boolean;
};

const {
  pronunciation,
  format,
  sourceFormat = "pinyin",
  language = "FG",
  noAudio = false,
  separate: isSeparate = false,
  proto = false,
  mcInfo = null,
} = defineProps<
  {
    pronunciation: string; // with ordinal tone notation (!)
    format?: Format; // of output
    separate?: boolean; // different colors for initial and final
    proto?: boolean; // only for FG
    mcInfo?: MCInfo | null; // for proto FG
  } & DefaultProps
>();

const displayedFormat = computed<Format>(() =>
  proto ? "ipaStrict" : format ?? settings.format
);

const show = computed(() => syllableUtils[language].show);

const displayedPronunciation = computed<string>(() => {
  return proto && language === "FG" && mcInfo != undefined
    ? simulateProtoPronunciation(
        show.value(
          pronunciation,
          "ipaStrict",
          settings.ipaToneNotation,
          sourceFormat
        ),
        mcInfo,
        history.pronounce.proto.settings
      )
    : show.value(
        pronunciation,
        displayedFormat.value,
        displayedFormat.value === "pinyin"
          ? ["FG", "PM"].includes(language)
            ? settings.pinyinToneNotation
            : "ordinal"
          : settings.ipaToneNotation,
        sourceFormat
      );
});

const parts = computed(() =>
  separate(displayedPronunciation.value, displayedFormat.value, language)
);

// for the moment, only for FG
const audioControls = computed(() => {
  if (noAudio || language !== "FG") {
    return { play: undefined, isPlaying: ref(false) };
  }

  let rawPronunciation = show.value(
    pronunciation,
    "ipaRaw",
    "ordinal",
    sourceFormat
  );
  if (proto && language === "FG" && mcInfo != undefined) {
    rawPronunciation = simulateProtoPronunciation(
      rawPronunciation,
      mcInfo,
      history.pronounce.proto.settings
    );
  }
  return useAudio(rawPronunciation);
});
</script>

<template>
  <span
    :class="[
      displayedFormat === 'pinyin' ? 'pinyin' : 'ipa',
      { clickable: audioControls.play !== undefined },
      { playing: audioControls.isPlaying.value },
    ]"
    style="font-weight: normal; transition: color 0.3s"
    @click="audioControls.play"
  >
    <template v-if="!isSeparate">
      {{ displayedPronunciation }}
    </template>
    <template v-else>
      <span class="initial">{{ parts[0] }}</span>
      <span class="final">{{ parts[1] }}</span>
      <span v-if="parts[2]" class="tone">{{ parts[2] }}</span>
    </template>
  </span>
</template>

<style scoped>
.initial {
  color: #1e90ff;
}

.final {
  color: #e74c3c;
}

.tone {
  color: #f1c40f;
}

.initial,
.final {
  font-variant-ligatures: none;
}
</style>
