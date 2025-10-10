<script setup lang="ts">
import { computed, ref, toRef } from "vue";
import { useSettingsStore } from "@/stores/settings";
import { useHistoryStore } from "@/stores/history";
import { useDraggable } from "@/composables/useDraggable";
import { useProvideDiachronicTableState } from "../DiachronicTable/useDiachronicTableState";
import { rhymeTableCache } from "./cache";
import { searchFilter } from "@/views/Search/typescript/search";
import { dictionaryCache, LangEntry, Language } from "@shared/lang";
import { syllableUtils } from "@shared/syllable";
import { getPart, partsUtils, renderParts } from "@shared/syllable";
import { computeOrdering } from "@shared/common/sort";
import { computeRowSpan } from "@/library/dom/pure";

import StickyTable from "@/components/common/StickyTable.vue";
import RhymeTableCell from "./RhymeTableCell.vue";
import DiachronicTable from "@/modules/DiachronicTable/DiachronicTable.vue";

const settings = useSettingsStore();
const history = useHistoryStore();

const {
  filter,
  noRedundant = false,
  partsColumns = false,
  language = "FG",
} = defineProps<{
  filter?: (entry: LangEntry, index: number) => boolean;
  noRedundant?: boolean;
  partsColumns?: boolean;
  language?: Language;
  blacklist?: string[];
  fullscreenZIndex?: number;
}>();

function rhymeTableFilter(entry: LangEntry): boolean {
  if (!searchFilter(entry)) return false;

  if (language === "FG") {
    for (const [key, excluded] of Object.entries(
      history.phonology.rhymeTable.filter
    )) {
      if (!isNaN(Number(key))) {
        // tone
        if (excluded && entry.讀音.at(-1) === String(key)) {
          return false;
        }
      } else {
        // stratum
        if (excluded && entry.層?.[0] === key) {
          return false;
        }
      }
    }
  }

  return true;
}

const { parse } = syllableUtils[language];
const { show, comparer } = partsUtils[language];

function showPart(value: string, part: any): string {
  return renderParts(show(value, part, settings.format), settings.format);
}

// LATERFIX only implemented for FG
// can compute ALL_... from dictionary
type Initial = string;
type Final = string;
const TABLE: Record<
  Initial,
  Record<Final, string | null>
> = rhymeTableCache.get();
const ALL_INITIALS = computed<Initial[]>(() =>
  Object.keys(TABLE).sort(comparer("聲母"))
);
const ZERO_FINAL: Final = JSON.stringify(["", "", ""]);
const ALL_FINALS = computed<Final[]>(() => [
  ...Object.keys(TABLE[""]!)
    .filter((final) => final != ZERO_FINAL)
    .sort(comparer("韻母", settings.finalOrdering as any)),
  ZERO_FINAL,
]);

// precompute once for all cells
const langIndicesMap = computed<Record<Initial, Record<Final, number[]>>>(
  () => {
    const result = Object.fromEntries(
      ALL_INITIALS.value.map((initial) => [
        initial,
        Object.fromEntries(
          ALL_FINALS.value.map((final) => [final, [] as number[]])
        ),
      ])
    );
    const usedFilter = filter ?? rhymeTableFilter;
    dictionaryCache.get(language).forEach((entry, index) => {
      if (!usedFilter(entry, index)) return;
      const syllable = parse(entry.讀音);
      result[syllable.聲母]![getPart(syllable, "韻母")]!.push(index);
    });
    return result;
  }
);

const initials = computed(() =>
  ALL_INITIALS.value.filter(
    noRedundant
      ? (initial) =>
          ALL_FINALS.value.some(
            (final) => langIndicesMap.value[initial]![final]!.length > 0
          )
      : (_) => true
  )
);
const finals = computed(() =>
  ALL_FINALS.value.filter(
    noRedundant
      ? (final) =>
          ALL_INITIALS.value.some(
            (initial) => langIndicesMap.value[initial]![final]!.length > 0
          )
      : (_) => true
  )
);

// parts as header columns
const rows = computed(() => {
  const ordering = computeOrdering(
    ["介音", "韻腹", "韻尾"],
    settings.finalOrdering
  );
  return finals.value.map((final) => {
    const tuple = JSON.parse(final);
    return ordering.map((order) => tuple[order]);
  });
});
const rowspans = computed(() => computeRowSpan(rows.value));

const header = ref<HTMLElement | null>(null);
useDraggable(header, [
  {
    ordering: toRef(settings, "finalOrdering"),
    keyName: "part",
    draggable: ".part",
  },
]);

const isFullscreen = defineModel("isFullscreen", { type: Boolean });

function testException(entry: LangEntry): boolean {
  return (
    entry.層 === "官" ||
    entry.記錄讀音!.slice(0, -1) !== entry.推導讀音!.slice(0, -1)
  );
}

const { diachronicTableState } = useProvideDiachronicTableState();
</script>

<template>
  <div>
    <StickyTable
      class="rhyme-table"
      :header-columns="[3]"
      v-model:is-fullscreen="isFullscreen"
      :blacklist="blacklist"
      :fullscreen-z-index="fullscreenZIndex"
      style="white-space: nowrap"
    >
      <thead>
        <tr ref="header">
          <th
            v-show="partsColumns"
            v-for="part of settings.finalOrdering"
            :key="part"
            group="part"
            :part="part"
            class="part draggable"
          >
            {{ part }}
          </th>

          <th>{{ partsColumns ? "韻母" : "" }}</th>
          <th
            v-for="initial of initials"
            :key="initial"
            v-html="initial === '' ? '零' : showPart(initial, '聲母')"
            style="min-width: 1.3rem"
          />
        </tr>
      </thead>

      <tbody>
        <tr v-for="(final, index) of finals" :key="final">
          <template v-for="(rowspan, colIndex) of rowspans[index]">
            <th
              v-show="partsColumns"
              v-if="rowspan > 0"
              :key="index"
              :rowspan="rowspan"
              v-html="rows[index]![colIndex] === '' ? '無' : showPart(rows[index]![colIndex], settings.finalOrdering[colIndex])"
            />
          </template>

          <th v-html="final === ZERO_FINAL ? '零' : showPart(final, '韻母')" />

          <RhymeTableCell
            v-for="initial of initials"
            :key="initial"
            :pronunciation="initial + JSON.parse(final).join('')"
            :char="TABLE[initial]?.[final] ?? null"
            :lang-indices="langIndicesMap[initial]![final]!"
            :language="language"
            :base-z-index="
              fullscreenZIndex ? fullscreenZIndex + 100 : undefined
            "
            v-bind="$attrs"
          />
        </tr>
      </tbody>
    </StickyTable>

    <DiachronicTable
      v-if="diachronicTableState.isFullscreen"
      v-model:is-fullscreen="diachronicTableState.isFullscreen"
      :mc-indices="diachronicTableState.mcIndices"
      :lang-indices="diachronicTableState.langIndices"
      show-count
      no-redundant
      hide-pronunciation
      :test-exception="testException"
      :language="language"
      :blacklist="['.rhyme-table']"
      :fullscreen-z-index="3000"
    />
  </div>
</template>

<style lang="scss">
@use "@/styles/common.scss";
.輕,
.輕 .char {
  @extend .gray;
}

.新,
.新 .char {
  text-decoration: underline;
  text-underline-offset: 0.2em;
  text-decoration-thickness: 0.1em;
}

.官,
.官 .char {
  text-decoration: underline wavy;
  text-underline-offset: 0.1em;
  text-decoration-thickness: 0.1em;
}

.老,
.老 .char {
  text-decoration: underline double;
  text-underline-offset: 0.15em;
  text-decoration-thickness: 0.1em;
}
</style>
