<script setup lang="ts">
import { computed, ref, toRefs } from "vue";
import { useSettingsStore } from "@/stores/settings";
import { useHistoryStore } from "@/stores/history";
import { getLangQueryUtils, LangEntry, Language } from "@shared/lang";
import { characterComparer } from "@shared/cjk";
import { entriesConst } from "@shared/common/object";

import RhymeTable from "@/modules/RhymeTable/RhymeTable.vue";
import EntryBlock from "./EntryBlock.vue";
import {
  NSpace,
  NCard,
  NGrid,
  NGridItem,
  NPagination,
  NButton,
} from "naive-ui";

const settings = useSettingsStore();

const { language = "FG" } = defineProps<{ language: Language }>();

const history = useHistoryStore();
const { page } = toRefs(history.search);

const searchUtils = computed(() => getLangQueryUtils(language));
const entryAt = computed(() => searchUtils.value.entryAt);

const indices = computed<number[] | null>(
  () => history.search.resultsMap[language]
);
const results = computed<LangEntry[]>(
  () =>
    history.search.resultsMap[language]
      ?.map(entryAt.value)
      .filter((entry) => entry != null)
      .filter(
        (entry) =>
          !entriesConst(settings.dictionary.disable).some(
            ([stratum, disabled]) => disabled && entry.層?.includes(stratum)
          )
      ) ?? []
);

const RESULTS_PER_PAGE = 20 as const;
const paginatedResults = computed<LangEntry[]>(() =>
  results.value == null
    ? []
    : results.value.slice(
        (page.value - 1) * RESULTS_PER_PAGE,
        page.value * RESULTS_PER_PAGE
      )
);

const CHARACTER_LIMIT = 100 as const;
const resultCharacters = computed<string[]>(() => [
  ...new Set(
    results.value
      .map((entry) => entry.字頭)
      .filter((character) => character != null) // □ is ignored
      .sort(characterComparer)
  ),
]);

const showRhymeTable = ref<boolean>(false);

const hook = ref<HTMLElement | null>(null);
defineExpose({ hook });
</script>

<template>
  <n-card>
    <template v-if="indices != null">
      <p style="margin-top: 0em">
        <template v-if="results.length === 0"> 無結果 </template>
        <template v-else>
          共查到 {{ resultCharacters.length }} 字、{{
            results.length
          }}
          個字條（<n-button @click.stop="showRhymeTable = !showRhymeTable" text>
            查看韻圖</n-button
          >）
        </template>
      </p>
      <p ref="hook" v-if="resultCharacters.length > 0" class="no-simplify">
        可能的字：<!--
        --><Character
          v-for="character of resultCharacters.slice(0, CHARACTER_LIMIT)"
          :character="character"
        /><template v-if="resultCharacters.length > CHARACTER_LIMIT"
          >…</template
        >
      </p>

      <RhymeTable
        v-if="language === 'FG' && showRhymeTable"
        v-model:is-fullscreen="showRhymeTable"
        :filter="(_, index) => indices!.includes(index)"
        no-redundant
        show-count
      />

      <n-grid v-if="results.length > 0" cols="1 600:2" style="margin-top: 2em">
        <n-grid-item
          v-for="(entry, index) of paginatedResults"
          :key="index"
          class="center"
        >
          <EntryBlock :entry="entry" :language="language" />
        </n-grid-item>
      </n-grid>

      <n-space
        v-if="results.length > RESULTS_PER_PAGE"
        justify="center"
        style="margin-top: 1.5em"
      >
        <n-pagination
          v-model:page="page"
          :page-size="RESULTS_PER_PAGE"
          :item-count="results.length"
          simple
        />
      </n-space>
    </template>
  </n-card>
</template>

<style scoped></style>
