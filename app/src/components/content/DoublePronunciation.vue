<script setup lang="ts">
import { DoubleMode } from "@/plugins/vite/markdownPlugins";

import Double from "./Double.vue";
import Pronunciation from "./Pronunciation.vue";

const { pronunciation, mode } = defineProps<{
  pronunciation: string;
  mode?: DoubleMode;
}>();
</script>

<template>
  <Double :mode="mode">
    <template #pinyin>
      <Pronunciation
        :pronunciation="pronunciation"
        format="pinyin"
        v-bind="$attrs"
      />
    </template>
    <template #ipa>
      <Pronunciation
        :pronunciation="pronunciation"
        format="ipaStrict"
        v-bind="$attrs"
      />
    </template>
  </Double>
</template>

<style scoped></style>
