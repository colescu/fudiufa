<script setup lang="ts">
import { computed, useSlots } from "vue";
import { useSettingsStore } from "@/stores/settings";
import type { DoubleMode } from "@/plugins/vite/markdownPlugins";

const settings = useSettingsStore();

const { mode } = defineProps<{
  mode?: DoubleMode;
}>();

const format = computed<string>(() => {
  switch (mode) {
    case "pinyin":
    case "ipaStrict":
      return mode;
    case "and":
      return "both";
    case "xor":
      return settings.format;
    case "left":
      return settings.format === "pinyin" ? "pinyin" : "both";
    case "right":
      return settings.format === "ipaStrict" ? "ipaStrict" : "both";
  }
  return settings.displayBoth ? "both" : settings.format;
});

const hasPinyin = computed<boolean>(() => {
  const slots = useSlots();
  return !!slots.pinyin && slots.pinyin().length > 0;
});
</script>

<template>
  <span :class="{ 'track-both': mode == undefined }">
    <template v-if="format !== 'ipaStrict'">
      <slot name="pinyin" />
    </template>
    <template v-if="format === 'both' && hasPinyin">&nbsp;</template>
    <template v-if="format === 'both'">[</template>
    <span v-if="format !== 'pinyin'">
      <slot name="ipa" />
    </span>
    <template v-if="format === 'both'">]</template>
  </span>
</template>

<style scoped></style>
