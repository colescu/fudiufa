<script setup lang="ts">
import { computed, toRef, toRefs, watch } from "vue";
import { useHistoryStore } from "@/stores/history";
import { useManagedSequentialAudio } from "@/composables/useAudio";
import { usePronounce } from "./usePronounce";
import { Language } from "@shared/lang";

import PronounceSettings from "./PronounceSettings.vue";
import InterlinearBlock from "./InterlinearBlock.vue";
import { NCard, NSpace, NInput, NButton, NIcon, useMessage } from "naive-ui";
import {
  CloseCircle,
  CopyOutline,
  PlayCircleOutline,
  StopCircleOutline,
} from "@vicons/ionicons5";

const message = useMessage();

const { language = "FG" } = defineProps<{ language: Language }>();

const TEXT_LIMIT = 1000 as const;

const history = useHistoryStore();
const { input } = toRefs(history.pronounce);
const outputChoices = toRef(history.pronounce.outputChoicesMap, language);

const { getIndices, getPreferredIndex, getDisplayedPronunciation } =
  usePronounce(language);

const indicesArray = computed<number[][]>(() =>
  [...input.value].map(getIndices)
);

function resetChoices() {
  outputChoices.value = indicesArray.value.map(getPreferredIndex);
}

watch(
  input,
  (newValue, oldValue) => {
    const indices = indicesArray.value.map(getPreferredIndex);

    if (oldValue) {
      let left = 0,
        right = 0;
      while (left < newValue.length && newValue[left] === oldValue[left]) {
        left += 1;
      }
      while (
        right < Math.min(newValue.length, oldValue.length) - left &&
        newValue[newValue.length - 1 - right] ===
          oldValue[oldValue.length - 1 - right]
      ) {
        right += 1;
      }

      outputChoices.value = [
        ...outputChoices.value.slice(0, left),
        ...indices.slice(left, newValue.length - right),
        ...outputChoices.value.slice(oldValue.length - right),
      ];
    } else {
      outputChoices.value = indices;
    }

    if (newValue.length >= TEXT_LIMIT) {
      message.warning("字数已达上限！");
    }
  },
  { immediate: true }
);

watch(
  () => [indicesArray, outputChoices],
  () => {
    indicesArray.value.forEach((indices, index) => {
      if (
        indices.length > 0 &&
        !indices.includes(outputChoices.value[index] as any)
      ) {
        outputChoices.value[index] = getPreferredIndex(indices);
      } else if (indices.length === 0) {
        outputChoices.value[index] = undefined;
      }
    });
  },
  { deep: true, immediate: true }
);

function getPhrase(...args: unknown[]) {
  return [...input.value].map((character, index) => ({
    character,
    pronunciation: getDisplayedPronunciation(
      outputChoices.value[index],
      // @ts-expect-error
      ...args
    ),
  }));
}

const phrase = computed(() => getPhrase("ipaRaw"));
const { toggleAudio, isPlaying, current } =
  language === "FG" ? useManagedSequentialAudio(phrase) : {};

async function copyToClipboard() {
  await window.navigator.clipboard.writeText(
    getPhrase("pinyin", false)
      .map((ruby) =>
        ruby.character === "\n"
          ? ruby.character
          : `[${ruby.character}]{${ruby.pronunciation}}`
      )
      .join("")
  );
  message.success("複製成功！");
}

const isDev = __IS_DEV__;
</script>

<template>
  <n-space vertical style="margin-top: 0.5em">
    <div style="position: relative">
      <n-input
        id="input"
        :input-props="{ name: 'input' }"
        type="textarea"
        :maxlength="TEXT_LIMIT"
        v-model:value="input"
        :placeholder="`請輸入文本（上限 ${TEXT_LIMIT} 字）`"
        :autosize="{ minRows: 5 }"
      />

      <n-button
        class="floating-icon"
        style="bottom: 1em; right: 1em"
        v-if="input"
        @click="input = ''"
        text
      >
        <n-icon :component="CloseCircle" class="clear-icon" />
      </n-button>
    </div>

    <div style="position: relative">
      <n-card id="output">
        <InterlinearBlock
          v-for="(char, index) in input"
          :key="index"
          :char="char"
          :indices="indicesArray[index]!"
          v-model="outputChoices[index]!"
          :language="language"
          :display-style="history.pronounce.style as any"
          :proto="history.pronounce.proto.enable"
          :class="{ playing: current === index }"
          style="transition: color 0.3s"
        />
      </n-card>

      <n-button
        v-if="input && isDev"
        class="floating-icon"
        style="top: 1em; right: 1em"
        @click="copyToClipboard"
        text
      >
        <n-icon :component="CopyOutline" />
      </n-button>
      <n-button
        v-if="input && language === 'FG'"
        class="floating-icon track-phrase"
        style="bottom: 0.85em; right: 0.85em"
        @click="toggleAudio"
        text
      >
        <n-icon
          :component="isPlaying ? StopCircleOutline : PlayCircleOutline"
          size="large"
        />
      </n-button>
    </div>

    <PronounceSettings v-if="language === 'FG'" @reset-choices="resetChoices" />
  </n-space>

  <Teleport to="#help">
    點擊字可查看字條詳情或選擇讀音。<br />
    多音字用<span class="highlight">灰色陰影</span>標出。<br />
    字條中「*」標記未收錄的理论推導音。
  </Teleport>
</template>

<style scoped lang="scss">
#input {
  padding: 1em 1em;
}

.floating-icon {
  position: absolute;
  z-index: 1;
}

.clear-icon {
  :deep(svg) {
    color: #c2c2c2;
    transition: color 0.3s, transform 0.3s;

    &:hover {
      color: #929292;
    }
  }
}
</style>
