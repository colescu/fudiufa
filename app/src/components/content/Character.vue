<script setup lang="ts">
import { computed } from "vue";
import { getMCQueryUtils } from "@shared/mc";
import { getLangEntries } from "@/views/Search/typescript/search";
import { getPredictedPronunciationsByEntry } from "@shared/fg/predict";
import { isChineseCharacter } from "@shared/cjk/utils";
import { Language } from "@shared/lang";

import ConstrainedPopover from "@/components/common/ConstrainedPopover.vue";
import MCInfo from "./MCInfo.vue";
import { NSpace } from "naive-ui";

const {
  character: characterProp,
  hint: hintProp,
  language = "FG",
} = defineProps<{
  character: string;
  hint?: string | number | number[]; // pronunciation or MC indices
  language?: Language;
}>();

const character = computed(() => [...characterProp][0] ?? "");

const mcIndices = computed<number[]>(() => {
  // MAYBE CLEANUP hint in characterProp to avoid parsing in md
  // priortize this
  let character = characterProp,
    hint = hintProp;
  if (character.includes(":")) {
    [character = "", hint] = character.split(":");
    if (!isNaN(Number(hint))) {
      hint = Number(hint);
    }
  }

  const recordedMCIndices = [
    ...new Set(
      getLangEntries(character, language)
        .filter((entry) => entry.記錄讀音 != null && entry.小韻號 != null)
        .map((entry) => entry.小韻號!)
    ),
  ].sort();

  let filteredMCIndices = [...recordedMCIndices];
  if (hint) {
    if (hint === "N/A") {
      filteredMCIndices = [];
    } else if (typeof hint === "string") {
      // filter by matching predicted pronunciations
      const { entryAt } = getMCQueryUtils();
      const matches = filteredMCIndices.filter((index) => {
        const entry = entryAt(index)!;
        const pronunciations =
          language === "FG"
            ? getPredictedPronunciationsByEntry(entry)
            : [entry.reflex[language]];
        return pronunciations.includes(hint as string);
      });
      if (matches.length > 0) {
        filteredMCIndices = matches;
      }
    } else {
      // specify indices manually
      if (typeof hint === "number") {
        hint = [hint];
      }
      filteredMCIndices = hint;
    }
  }

  return filteredMCIndices;
});

const isDev = __IS_DEV__;
</script>

<template>
  <span v-if="!isChineseCharacter(character)" class="char">
    {{ character }}
  </span>

  <ConstrainedPopover v-else v-bind="$attrs" style="min-width: max-content">
    <template #trigger>
      <!-- MAYBE DESIGN 突出顯示例字 -->
      <span
        class="char clickable"
        :class="{ highlight: isDev && mcIndices.length !== 1 }"
      >
        {{ character }}
      </span>
    </template>

    <n-space v-if="mcIndices.length > 0" vertical style="gap: 0em">
      <div v-for="(mcIndex, index) in mcIndices" :key="index" :value="index">
        <MCInfo :mc-entry="mcIndex" 反切 />
      </div>
    </n-space>

    <div v-else>中古音韻未知</div>

    <!-- MAYBE 顯示所有記錄讀音
     But it gets too complicated, also can look up in Search or Pronounce.
     Should only show in situation where no pronunciation or MC is provided.
     -->
  </ConstrainedPopover>
</template>

<style scoped>
.n-tag {
  margin-right: -0.3em;
}

.highlight {
  background-color: yellow;
}
</style>
