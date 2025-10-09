<script setup lang="ts">
import type { CSSProperties } from "vue";

import ConstrainedPopover from "@/components/common/ConstrainedPopover.vue";

const { marker = "注", triggerStyle } = defineProps<{
  marker?: string;
  triggerStyle?: CSSProperties | string;
}>();
</script>

<template>
  <ConstrainedPopover trigger="hover">
    <template #trigger>
      <sup :style="triggerStyle">{{ marker }}</sup>
    </template>

    <div class="footnote" style="max-width: 15em">
      <slot />
    </div>
  </ConstrainedPopover>
</template>

<style scoped></style>
