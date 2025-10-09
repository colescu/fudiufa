<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from "vue";
import { getColumns } from "@/library/dom/table";

function preprocess(node: Node) {
  // stylize tables
  if (node instanceof Element || node instanceof Document) {
    node.querySelectorAll("table").forEach((table) => {
      // wrap in div.scrollable
      const parent = table.parentNode;
      if (
        parent &&
        parent instanceof Element &&
        !parent.classList.contains("scrollable")
      ) {
        const wrapper = document.createElement("div");
        wrapper.className = "scrollable";
        table.parentNode.insertBefore(wrapper, table);
        wrapper.appendChild(table);
      }

      // add class to header columns
      if (table.hasAttribute("header-columns")) {
        const columns = getColumns(table);
        Array.from({
          length: Number(table.getAttribute("header-columns")),
        }).forEach((_, index) => {
          columns[index]!.forEach((cell) => {
            cell.classList.add("table-header");
          });
        });
      }
    });
  }

  // prevent breaking before punctuation marks
  const walker = document.createTreeWalker(node, NodeFilter.SHOW_TEXT, null);
  while (walker.nextNode()) {
    const node = walker.currentNode;
    if (node.nodeValue) {
      node.nodeValue = node.nodeValue.replace(/ (，|。|、|；|：)/g, "\u00A0$1");
    }
  }
}

const root = ref<HTMLElement | null>(null);

let observer: MutationObserver | null = null;

onMounted(() => {
  if (!root.value) return;
  preprocess(root.value);

  // target tooltips
  observer = new MutationObserver((mutations) => {
    for (const mutation of mutations) {
      mutation.addedNodes.forEach((node) => {
        if (
          node instanceof HTMLElement &&
          ((node.classList.contains("v-binder-follower-container") &&
            node.querySelectorAll(".footnote").length > 0) ||
            node.classList.contains("markdown"))
        ) {
          preprocess(node);
        }
      });
    }
  });
  observer.observe(document.body, {
    childList: true,
    subtree: true,
  });
});

onBeforeUnmount(() => {
  if (observer) {
    observer.disconnect();
  }
});
</script>

<template>
  <div ref="root" class="markdown-wrapper" v-bind="$attrs">
    <slot />
  </div>
</template>

<style scoped>
.markdown-wrapper {
  font-family: var(--char-font-family);
}
</style>
