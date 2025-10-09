<script setup lang="ts">
import Double from "./Double.vue";
import Pronunciation, { type DefaultProps } from "./Pronunciation.vue";
import type { DoubleMode } from "@/plugins/vite/markdownPlugins";

const { pronunciation, mode, ...rest } = defineProps<
  {
    pronunciation: string;
    mode?: DoubleMode;
  } & DefaultProps
>();
</script>

<template>
  <Double :mode="mode">
    <template #pinyin>
      <Pronunciation
        :pronunciation="pronunciation"
        v-bind="rest"
        format="pinyin"
      />
    </template>
    <template #ipa>
      <Pronunciation
        :pronunciation="pronunciation"
        v-bind="rest"
        format="ipaStrict"
      />
    </template>
  </Double>
</template>

<style scoped></style>
