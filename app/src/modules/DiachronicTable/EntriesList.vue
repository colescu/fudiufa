<script setup lang="ts">
import { LangEntry, Language } from "@shared/lang";

const { entries, language } = defineProps<{
  entries: LangEntry[];
  language: Language;
}>();
</script>

<template>
  <template v-for="entry of entries">
    <span style="white-space: nowrap">
      <span class="no-simplify"
        ><Character
          :character="entry.字頭 ?? '□'"
          :hint="entry.小韻號 ?? undefined"
          trigger="click" /></span
      ><sub v-if="entry.層">{{ entry.層 }}</sub
      >&nbsp;<Pronunciation
        :pronunciation="entry.記錄讀音!"
        :language="language"
      /> </span
    >&nbsp;
  </template>
</template>

<style scoped></style>
