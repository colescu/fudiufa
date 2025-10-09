<script setup lang="ts">
import { nextTick, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { getColumns } from "../../library/dom/table";

import { NButton, NIcon } from "naive-ui";
import { Expand, Contract } from "@vicons/ionicons5";

const {
  headerColumns = 1,
  whitelist = [],
  blacklist = [],
  fullscreenZIndex = 1000,
} = defineProps<{
  headerColumns?: number | number[]; // first n or custom
  whitelist?: string[];
  blacklist?: string[];
  fullscreenZIndex?: number; // for fullscreen
}>();

function makeColumnsStick(
  table: HTMLTableElement,
  headerColumns: number | number[]
) {
  const allColumns = getColumns(table);

  // remove outer borders
  allColumns.forEach((column, colIndex) => {
    column[0]!.style.borderTop = "none";
    column.at(-1)!.style.borderBottom = "none";
    if (colIndex === 0) {
      column.forEach((cell) => {
        cell.style.borderLeft = "none";
      });
    }
    if (colIndex === allColumns.length - 1) {
      column.forEach((cell) => {
        cell.style.borderRight = "none";
      });
    }
  });

  const columns =
    typeof headerColumns === "number"
      ? allColumns.slice(0, headerColumns)
      : (headerColumns.map((index) => allColumns[index]) as HTMLElement[][]);
  const widths = columns.map((column) => column[0]!.offsetWidth);
  columns.forEach((column, colIndex) => {
    const left = widths.slice(0, colIndex).reduce((a, b) => a + b, 0);
    column.forEach((cell, rowIndex) => {
      Object.assign(cell.style, {
        position: "sticky",
        left: left + "px",
        zIndex: rowIndex === 0 ? 7 : 6,
      });
    });
  });
}

const table = ref<HTMLTableElement | null>(null);
let observer: MutationObserver | null = null;

onMounted(() => {
  if (!table.value) return;
  makeColumnsStick(table.value, headerColumns);

  observer = new MutationObserver(async () => {
    await nextTick();
    if (!table.value) return;
    makeColumnsStick(table.value, headerColumns);
  });
  observer.observe(table.value, { childList: true, subtree: true });
});
onBeforeUnmount(() => {
  observer?.disconnect();
});

// resize handle
// ChatGPT

const height = ref(window.innerHeight * 0.6);
const minHeight = window.innerHeight * 0.3;
const maxHeight = window.innerHeight * 0.9;

let startY = 0;
let startHeight = 0;

const startDrag = (e: MouseEvent | TouchEvent) => {
  startY = e instanceof MouseEvent ? e.clientY : e.touches[0]!.clientY;
  startHeight = height.value;

  window.addEventListener("mousemove", onDrag);
  window.addEventListener("mouseup", stopDrag);
  window.addEventListener("touchmove", onDrag, { passive: false });
  window.addEventListener("touchend", stopDrag);
};

const onDrag = (e: MouseEvent | TouchEvent) => {
  e.preventDefault();
  const currentY = e instanceof MouseEvent ? e.clientY : e.touches[0]!.clientY;
  const dy = currentY - startY;
  height.value = Math.min(maxHeight, Math.max(minHeight, startHeight + dy));
};

const stopDrag = () => {
  window.removeEventListener("mousemove", onDrag);
  window.removeEventListener("mouseup", stopDrag);
  window.removeEventListener("touchmove", onDrag);
  window.removeEventListener("touchend", stopDrag);
};

// fullscreen toggle

const isFullscreen = defineModel<boolean>("isFullscreen", {
  default: false,
});

const WHITELIST = [".n-popover", ".n-float-button", ".popover-target"];
function handleClick(e: MouseEvent) {
  const clicked = e.target as HTMLElement;

  let el = clicked.closest([...WHITELIST, ...whitelist].join(", "));
  if (!!el && (!blacklist.length || !el.matches(blacklist.join(", ")))) return;

  el = clicked.closest(".sticky-row-column");
  if (!!el && (!blacklist.length || !el.matches(blacklist.join(", ")))) return;

  isFullscreen.value = false;
}

document.addEventListener("click", handleClick);

watch(isFullscreen, (value) => {
  const overlay = document.querySelector(".fullscreen-overlay") as HTMLElement;
  overlay.style.display = value ? "block" : "none";

  if (value && !history.state?.fullscreen) {
    history.pushState(
      { ...history.state, fullscreen: true },
      "",
      location.href
    );
  }
});

function handleBack() {
  if (isFullscreen.value) {
    isFullscreen.value = false;
    history.replaceState(
      { ...history.state, fullscreen: false },
      "",
      location.href
    );
  }
}
onMounted(() => window.addEventListener("popstate", handleBack));
onBeforeUnmount(() => window.removeEventListener("popstate", handleBack));
</script>

<template>
  <div>
    <div
      class="center"
      style="max-width: fit-content"
      :style="
        isFullscreen
          ? { zIndex: fullscreenZIndex }
          : { position: 'relative', margin: '2em auto' }
      "
      :class="{ fullscreen: isFullscreen }"
    >
      <div
        class="sticky-row-column"
        :style="{ maxHeight: isFullscreen ? 'fit-content' : `${height}px` }"
        :class="$attrs.class"
      >
        <n-button
          @click.stop="isFullscreen = !isFullscreen"
          class="fullscreen-toggle"
          :style="{ zIndex: isFullscreen ? fullscreenZIndex + 1 : 8 }"
          text
        >
          <n-icon :component="isFullscreen ? Contract : Expand" />
        </n-button>

        <table ref="table">
          <slot />
        </table>
      </div>
    </div>

    <div
      v-if="!isFullscreen"
      class="handle"
      @mousedown="startDrag"
      @touchstart.prevent="startDrag"
    />

    <div class="fullscreen-overlay">.</div>
  </div>
</template>

<style lang="scss">
.sticky-row-column {
  overflow: auto;
  max-width: fit-content;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  border: 2px solid var(--border-color);
  z-index: 5;
  background-color: var(--background-color);

  table {
    border-collapse: separate;
    border-spacing: 0;

    th,
    td {
      border: 0.5px solid var(--border-color);
    }

    thead {
      th {
        position: sticky;
        top: 0;
        z-index: 6;
      }
    }

    tbody {
      th {
        position: relative;
      }
    }
  }
}
</style>

<style scoped>
.handle {
  width: 30px;
  height: 20px;
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  cursor: ns-resize;
  touch-action: none;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  user-select: none;

  &::before,
  &::after {
    content: "";
    display: block;
    width: 0;
    height: 0;
    border-left: 6px solid transparent;
    border-right: 6px solid transparent;
  }

  &::before {
    border-bottom: 6px solid #666;
    margin-bottom: 2px;
  }

  &::after {
    border-top: 6px solid #666;
    margin-top: 2px;
  }
}

.fullscreen-toggle {
  position: absolute;
  transform: translate(-0.2em, -0.2em);
}

.fullscreen {
  position: fixed;
  inset: 0;
  margin: auto;
}

.fullscreen-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(5px);
  z-index: 4;
}
</style>
