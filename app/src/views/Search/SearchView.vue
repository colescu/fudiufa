<script setup lang="ts">
import { provide, ref, toRef, toRefs, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useHistoryStore } from "@/stores/history";
import { Language, LANGUAGE_MAP } from "@shared/lang";

import SearchChar from "./tabs/SearchChar.vue";
import SearchMC from "./tabs/SearchMC.vue";
import SearchLang from "./tabs/SearchLang.vue";
import SearchPM from "./tabs/SearchPM.vue";
import SearchGC from "./tabs/SearchGC.vue";
import SearchResults from "./SearchResults.vue";
import { NCard, NSpace, NTabPane, NTabs } from "naive-ui";

const { language = "FG" } = defineProps<{ language: Language }>();

const route = useRoute();
const router = useRouter();
const history = useHistoryStore();
const { tab, page } = toRefs(history.search);
const results = toRef(history.search.resultsMap, language);

function clear() {
  results.value = null;
  page.value = 1;
}

function searchWrapper(search: () => number[] | Promise<number[]>) {
  return async () => {
    clear();
    results.value = await search();
  };
}
provide("searchWrapper", searchWrapper);

const resultsContainer = ref<any>(null);
watch(page, () => {
  const el = resultsContainer.value?.hook;
  const navbar = document.getElementById("navbar");
  if (!el || !navbar) return;

  const top =
    el.getBoundingClientRect().top +
    window.scrollY -
    navbar.offsetHeight -
    parseFloat(getComputedStyle(document.documentElement).fontSize); // 1em

  window.scrollTo({
    top,
    behavior: "smooth",
  });
});

watch(
  () => route.query,
  ({ i }) => {
    if (
      typeof i === "string" &&
      ["ci", "fudiufa", "dungguin", "putungfa", "guongdungfa"].includes(i)
    ) {
      tab.value = i;
    }
  },
  { immediate: true, deep: true }
);
watch(
  tab,
  (newTab) => {
    router.push({
      name: "Search",
      query: { i: newTab },
    });
  },
  { immediate: true }
);
</script>

<template>
  <n-space vertical>
    <n-card>
      <n-tabs
        v-model:value="tab"
        @update:value="clear"
        type="card"
        size="small"
        animated
      >
        <n-tab-pane name="ci" tab="依字">
          <SearchChar :language="language" />
        </n-tab-pane>
        <n-tab-pane name="fudiufa" :tab="`依${LANGUAGE_MAP[language]}`">
          <SearchLang :language="language" />
        </n-tab-pane>
        <n-tab-pane name="dungguin" tab="依中古音">
          <SearchMC :language="language" />
        </n-tab-pane>
        <n-tab-pane name="putungfa" tab="依普通話">
          <SearchPM :language="language" />
        </n-tab-pane>
        <n-tab-pane name="guongdiufa" tab="依廣州話">
          <SearchGC :language="language" />
        </n-tab-pane>
      </n-tabs>
    </n-card>

    <SearchResults ref="resultsContainer" :language="language" />
  </n-space>
</template>

<style scoped>
:deep(.char) {
  color: inherit !important;
}

:deep(.grid-form) {
  margin-top: 1em;
}

:deep(.n-form-item-gi) {
  min-width: 5em;
}

:deep(.search-input) {
  max-width: 95%;
}

:deep(.submit) {
  display: flex;
  align-items: flex-end;
  justify-content: flex-end;
}

:deep(.center) {
  height: 100%;
}

:deep(.center) > .block {
  margin: auto -1.5em;
  height: 100%;
  box-sizing: border-box;
  border-top: 0.5px solid var(--border-color);
}
</style>
