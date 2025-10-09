<script setup lang="ts">
import { NCheckbox } from "naive-ui";

const checked = defineModel<boolean>("checked", {
  default: false,
});

const RED = "#e04345";
const crossBoxThemeOverrides = {
  colorChecked: RED,
  common: {
    primaryColor: RED,
  },
  checkMarkColor: "transparent",
};
</script>

<template>
  <n-checkbox
    v-model:checked="checked"
    class="cross-box"
    :theme-overrides="crossBoxThemeOverrides"
    :class="{ 'show-x': checked }"
    v-bind="$attrs"
  >
    <slot />
  </n-checkbox>
</template>

<style scoped lang="scss">
.cross-box {
  :deep(.n-checkbox-box) {
    &::after {
      content: "×";
      color: white;
      font-size: 14px;
      font-weight: bold;
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%) scale(0);
      opacity: 0;
      transition: transform 0.3s ease, opacity 0.3s ease;
      pointer-events: none;
    }
  }

  &.show-x {
    :deep(.n-checkbox-box) {
      &::after {
        transform: translate(-50%, -50%) scale(1);
        opacity: 1;
      }
    }
  }
}
</style>
