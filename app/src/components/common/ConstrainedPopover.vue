<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch, nextTick } from "vue";
import { usePopoverZIndex } from "@/composables/usePopoverZIndex";
import { isMobile } from "@/library/config";

import { NPopover, type PopoverTrigger } from "naive-ui";

const {
  trigger = "manual",
  whitelist = [],
  blacklist = [],
  className,
  baseZIndex,
} = defineProps<{
  trigger?: PopoverTrigger;
  whitelist?: string[];
  blacklist?: string[];
  className?: string;
  baseZIndex?: number;
}>();
const showPopover = defineModel<boolean>("show", {
  default: false,
});

const target = ref<HTMLElement | null>(null);

// do not trigger if click on whitelist

const WHITELIST = [".n-popover", ".n-float-button", ".popover-target"];
function handleClick(e: MouseEvent) {
  const clicked = e.target as HTMLElement;

  if (target.value?.contains(clicked)) {
    showPopover.value = !showPopover.value;
    e.stopPropagation();
    return;
  }

  const el = clicked.closest([...WHITELIST, ...whitelist].join(", "));
  if (!!el && (!blacklist.length || !el.matches(blacklist.join(", ")))) return;

  showPopover.value = false;
}

if (trigger === "manual") {
  onMounted(() => {
    document.addEventListener("click", handleClick, true);
  });
  onBeforeUnmount(() => {
    document.removeEventListener("click", handleClick, true);
  });
}

// close popover if target gets covered

function getIsVisible(el: HTMLElement): boolean {
  const rect = el.getBoundingClientRect();

  if (
    rect.bottom < 0 ||
    rect.top > window.innerHeight ||
    rect.right < 0 ||
    rect.left > window.innerWidth
  ) {
    return false;
  }

  const x = rect.left + rect.width / 2;
  const y = rect.top + rect.height / 2;
  const topElement = document.elementFromPoint(x, y);

  // skip popovers
  if (
    Array.from(document.querySelectorAll(".n-popover")).some((popover) =>
      popover.contains(topElement)
    )
  ) {
    return true;
  }

  return topElement === el || el.contains(topElement);
}

function checkVisibility() {
  if (!target.value) return;
  if (!getIsVisible(target.value)) {
    showPopover.value = false;
  }
}

onMounted(() => {
  window.addEventListener("scroll", checkVisibility, true);
  window.addEventListener("resize", checkVisibility);
});
onBeforeUnmount(() => {
  window.removeEventListener("scroll", checkVisibility, true);
  window.removeEventListener("resize", checkVisibility);
});

// raise z-index

const { popoverId } = usePopoverZIndex(showPopover, baseZIndex);
</script>

<template>
  <n-popover
    v-model:show="showPopover"
    :popover-id="popoverId"
    :trigger="trigger === 'hover' && isMobile ? 'click' : trigger"
    :class="[className ? `${className}__popover` : null]"
    v-bind="$attrs"
  >
    <template #trigger>
      <span
        ref="target"
        class="popover-target"
        :class="[className ? `${className}__popover-target` : null]"
      >
        <slot name="trigger" />
      </span>
    </template>

    <slot />
  </n-popover>
</template>

<style scoped></style>
