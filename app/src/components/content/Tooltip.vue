<script setup lang="ts">
import type { CSSProperties } from "vue";

import ConstrainedPopover from "@/components/common/ConstrainedPopover.vue";

const {
  marker = "注",
  triggerStyle,
  clickStop = false,
} = defineProps<{
  marker?: string;
  triggerStyle?: CSSProperties | string;
  clickStop?: boolean;
}>();
</script>

<template>
  <span @click.stop="clickStop && $event.stopPropagation()">
    <ConstrainedPopover trigger="hover">
      <template #trigger>
        <sup :style="triggerStyle">{{ marker }}</sup>
      </template>

      <div class="footnote" style="max-width: 15em">
        <slot />
      </div>
    </ConstrainedPopover>
  </span>
</template>

<style scoped></style>
