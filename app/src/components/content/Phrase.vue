<script setup lang="ts">
import { computed } from "vue";
import { syllableUtils } from "@shared/syllable";
import { useManagedSequentialAudio } from "@/composables/useAudio";

import CharacterRuby, { RubyData } from "./CharacterRuby.vue";
import { NButton, NIcon, useMessage } from "naive-ui";
import { PlayCircleOutline, StopCircleOutline } from "@vicons/ionicons5";

const message = useMessage();

// only for FG
const { phrase } = defineProps<{
  phrase: RubyData[];
}>();

const rawPhrase = computed<RubyData[]>(() => {
  const { show } = syllableUtils.FG;
  return phrase.map(({ character, pronunciation }) => ({
    character,
    pronunciation: pronunciation
      ? show(pronunciation, "ipaRaw", "ordinal", "pinyin")
      : "",
  }));
});
const { toggleAudio, isPlaying, current } = useManagedSequentialAudio(
  rawPhrase,
  message
);

const playingClass = computed(() => {
  return (index: number) => ({
    playing: current.value === index,
  });
});
</script>

<template>
  <span class="phrase">
    <span style="white-space: nowrap">
      <n-button
        @click="toggleAudio"
        class="float track-phrase"
        size="tiny"
        text
      >
        <n-icon
          :component="isPlaying ? StopCircleOutline : PlayCircleOutline"
        />
      </n-button>
      <span v-if="phrase.length > 0" class="item" :class="playingClass(0)">
        <CharacterRuby
          :character="phrase[0]!.character"
          :pronunciation="phrase[0]!.pronunciation"
          v-bind="$attrs"
        />
      </span>
    </span>

    <template v-for="(ruby, index) of phrase.slice(1)" :key="index">
      <span class="item" :class="playingClass(index + 1)">
        <CharacterRuby
          :character="ruby.character"
          :pronunciation="ruby.pronunciation"
          v-bind="$attrs"
        />
      </span>
    </template>
  </span>
</template>

<style scoped>
.float {
  position: absolute;
  margin-left: -1.05em;
  margin-top: 0.8em;
}

.item {
  display: inline-block;
  transition: color 0.3s;
}
</style>
