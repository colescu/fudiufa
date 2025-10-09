<script setup lang="ts">
import { ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useSettingsStore } from "@/stores/settings";
import { isMobile } from "@/library/config";
import { ROUTES_MAP } from "@/router/routes";

import App from "@/App.vue";
import {
  zhCN,
  NConfigProvider,
  NMessageProvider,
  NModalProvider,
  type GlobalThemeOverrides,
} from "naive-ui";

// CSS

function getCSSVariable(name: string) {
  return getComputedStyle(document.documentElement)
    .getPropertyValue(`--${name}`)
    .trim();
}
const themeOverrides: GlobalThemeOverrides = {
  common: {
    primaryColor: getCSSVariable("colescu"),
    primaryColorHover: getCSSVariable("colescu-light"),
    primaryColorPressed: getCSSVariable("colescu-dark"),
  },
};

const settings = useSettingsStore();
watch(
  () => settings.colorizeChar,
  (value) => {
    document.documentElement.style.setProperty(
      "--char-color",
      getCSSVariable(value ? "colescu-dark" : "text-color")
    );
  },
  { immediate: true }
);

// swipe

const route = useRoute();
const router = useRouter();

const ignoreSwipe = ref<boolean | "left" | "right">(false);
function getIsIgnoreSwipe(e: TouchEvent) {
  if (!isMobile) return true;

  const target = e.target as HTMLElement | null;
  if (!target) return false;

  if (target.closest(".n-button")) {
    return true;
  }

  const scrollable = target.closest(
    ".scrollable, .sticky-row-column"
  ) as HTMLElement | null;
  if (scrollable && scrollable.scrollWidth > scrollable.clientWidth + 1) {
    if (scrollable.parentElement?.classList.contains("fullscreen")) {
      return true;
    }
    if (scrollable.scrollLeft === 0) {
      return "left";
    }
    if (
      scrollable.scrollLeft + scrollable.clientWidth + 1 >=
      scrollable.scrollWidth
    ) {
      return "right";
    }
    return true;
  }

  return false;
}
function onTouchStart(e: TouchEvent) {
  ignoreSwipe.value = getIsIgnoreSwipe(e);
}

const ROUTES = Object.values(ROUTES_MAP) as string[];
function onSwipe(direction: string) {
  if (ignoreSwipe.value === true || ignoreSwipe.value === direction) return;
  if (!["left", "right"].includes(direction)) return;

  const index = ROUTES.indexOf(route.path);
  const newIndex = index + (direction === "left" ? 1 : -1);
  if (
    0 <= index &&
    index <= ROUTES.length - 1 &&
    0 <= newIndex &&
    newIndex <= ROUTES.length - 1
  ) {
    router.push(ROUTES[newIndex]!);
  }
}
</script>

<template>
  <n-config-provider
    :locale="zhCN"
    :theme-overrides="themeOverrides"
    @click="onTouchStart"
    @touchstart="onTouchStart"
    v-touch:swipe="onSwipe"
  >
    <n-message-provider>
      <n-modal-provider>
        <App />
      </n-modal-provider>
    </n-message-provider>
  </n-config-provider>
</template>

<style scoped></style>
