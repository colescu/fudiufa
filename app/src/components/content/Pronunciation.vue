<script setup lang="ts">
import { computed, ref } from "vue";
import { useSettingsStore } from "@/stores/settings";
import { usePronunciation } from "@/composables/usePronunciation";
import { useAudio } from "@/composables/useAudio";
import { separate } from "@shared/syllable";
import { Language } from "@shared/lang";
import { MCInfo } from "@shared/mc";

import { useMessage } from "naive-ui";

const settings = useSettingsStore();
const message = useMessage();

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
  variant = false,
  proto = false,
  mcInfo = null,
} = defineProps<
  {
    pronunciation: string; // with ordinal tone notation (!)
    format?: Format; // of output
    separate?: boolean; // different colors for initial and final
    // only for FG
    variant?: boolean;
    proto?: boolean;
    mcInfo?: MCInfo | null;
  } & DefaultProps
>();

const show = computed(() => usePronunciation(language, variant, proto).show);

const displayedFormat = computed<Format>(() =>
  proto ? "ipaStrict" : format ?? settings.format
);

const displayedPronunciation = computed<string>(() =>
  show.value(pronunciation, displayedFormat.value, sourceFormat, mcInfo)
);

const parts = computed(() =>
  separate(displayedPronunciation.value, displayedFormat.value, language)
);

// only for FG for the moment
const audioControls = computed(() => {
  if (noAudio || language !== "FG") {
    return { play: undefined, isPlaying: ref(false) };
  }
  const rawPronunciation = show.value(
    pronunciation,
    "ipaRaw",
    sourceFormat,
    mcInfo,
    "ordinal"
  ).replace(/^([pmf])ɿ/, "$1ɨ");
  return useAudio(rawPronunciation, message);
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
