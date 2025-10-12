<script setup lang="ts">
import { LangEntry } from "@shared/lang";
import { PronounceProps } from "./types";

const { entry, ...rest } = defineProps<
  {
    entry: LangEntry;
  } & PronounceProps
>();
</script>

<template>
  <span>
    <span class="char no-simplify">{{ entry.字頭 || "□" }}</span>
    <span
      >&nbsp;<template v-if="!entry.記錄讀音">*</template>
      <DoublePronunciation
        v-if="!rest.proto || language !== 'FG'"
        :pronunciation="entry.讀音"
        v-bind="rest"
        :mc-info="entry.MC"
      />
      <Pronunciation
        v-else
        :pronunciation="entry.讀音"
        v-bind="rest"
        :mc-info="entry.MC"
      />
    </span>
    <sub v-if="entry.層">&nbsp;{{ entry.層 }}</sub>
    <span v-if="entry.訓作"
      >&ensp;<template v-if="entry.訓作 === '？'">本字存疑</template
      ><template v-else
        >訓作「<span class="char no-simplify">{{ entry.訓作 }}</span
        >」</template
      ></span
    >
    <span v-if="entry.訓作 == null && entry.MC">
      &nbsp;<MCInfo :mc-entry="entry.小韻號!" />
    </span>
    <span v-if="entry.釋義"> &nbsp;{{ entry.釋義 }}</span>
  </span>
</template>

<style scoped></style>
