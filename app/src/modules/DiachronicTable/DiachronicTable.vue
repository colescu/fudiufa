<script setup lang="ts">
import { computed, ref, toRef } from "vue";
import { useHistoryStore } from "@/stores/history";
import { useDraggable } from "@/composables/useDraggable";
import {
  mcCache,
  FULL_FINALS,
  INITIAL_GROUP_MAP,
  MC_CATEGORIES,
  入舒_MAP,
  CODAS,
  CODA_MAP,
  FINAL_MAP,
} from "@shared/mc";
import { getFullFinal } from "@shared/fg/predict";
import { dictionaryCache, Language } from "@shared/lang";
import { characterComparer } from "@shared/cjk";
import {
  computeOrdering,
  createSortComparerFromArrays,
  precomposeComparer,
} from "@shared/common/sort";
import { computeRowSpan } from "@/library/dom/pure";

import StickyTable from "@/components/common/StickyTable.vue";
import ConstrainedPopover from "@/components/common/ConstrainedPopover.vue";
import DiachronicTableCell from "./DiachronicTableCell.vue";
import { NSpace, NGrid, NGridItem, NCheckbox, NButton, NIcon } from "naive-ui";
import { ArrowSwap20Regular as ArrowSwap } from "@vicons/fluent";

const {
  mcIndices,
  langIndices,
  groupInitials = false,
  filterCodas = false,
  noRedundant = false,
  language = "FG",
} = defineProps<{
  mcIndices?: number[];
  langIndices?: number[];
  groupInitials?: boolean;
  filterCodas?: boolean;
  noRedundant?: boolean;
  language?: Language;
  blacklist?: string[];
  fullscreenZIndex?: number;
}>();

const mcIndexMap = computed<
  // { fullFinal: { initial : { tone : mcIndex[] } } }
  Record<string, Record<string, Record<string, number[]>>>
>(() => {
  const MC_ENTRIES_MAP = mcCache.get();
  const result: Record<string, Record<string, Record<string, number[]>>> = {};
  for (const index of mcIndices ?? Object.keys(MC_ENTRIES_MAP)) {
    const mcInfo = MC_ENTRIES_MAP[Number(index)]!.MC;
    const initial = mcInfo.聲母;
    const fullFinal = getFullFinal(mcInfo);
    const tone = mcInfo.聲調;
    if (!(fullFinal in result)) {
      result[fullFinal] = Object.fromEntries(
        MC_CATEGORIES.聲母.map((initial) => [
          initial,
          Object.fromEntries(
            MC_CATEGORIES.聲調.map((tone) => [tone, [] as number[]])
          ),
        ])
      );
    }
    result[fullFinal]![initial]![tone]!.push(Number(index));
  }
  return result;
});

// { mcIndex: langIndex[] }
type LangIndexMap = Map<number, number[]>;

const fullLangIndexMap = computed<LangIndexMap>(() => {
  const DICTIONARY = dictionaryCache.get(language);
  const result: LangIndexMap = new Map();
  for (const index of langIndices ?? DICTIONARY.keys()) {
    const entry = DICTIONARY[index]!;
    if (entry.記錄讀音 != null && entry.小韻號 != null) {
      if (!result.has(entry.小韻號)) {
        result.set(entry.小韻號, []);
      }
      result.get(entry.小韻號)!.push(index);
    }
  }
  [...result.values()].forEach((indices) =>
    indices.sort(
      precomposeComparer(characterComparer, (index) => DICTIONARY[index]!.字頭)
    )
  );
  return result;
});

function getLangIndexMap(fullFinal: string, initials?: string): LangIndexMap {
  let tones = ["平", "上", "去"];
  if (fullFinal[1] && fullFinal[1] in 入舒_MAP) {
    fullFinal = fullFinal[0] + 入舒_MAP[fullFinal[1]] + fullFinal.slice(2);
    tones = ["入"];
  }
  const mcIndices: number[] = (
    initials ? initials.split("") : MC_CATEGORIES.聲母
  )
    .map((initial) =>
      tones
        .map((tone) => mcIndexMap.value?.[fullFinal]?.[initial]?.[tone] ?? [])
        .flat()
    )
    .flat(); // MC indices sorted by initial, tone
  return new Map(
    mcIndices.map(
      (mcIndex) =>
        [mcIndex, fullLangIndexMap.value.get(mcIndex) ?? []] as [
          number,
          number[]
        ]
    )
  );
}

const history = useHistoryStore();
const itemOrdering = toRef(history.phonology.diachronicTable, "itemOrdering");
const ordering = computed(() =>
  computeOrdering(["攝", "韻", "等", "呼"], itemOrdering.value).map(
    (index) => index
  )
);

// either "幫 p" for group 幫滂並 or just "幫"
const ALL_INITIALS_MAP = computed<Record<string, string | null>>(() =>
  !groupInitials
    ? Object.fromEntries(MC_CATEGORIES.聲母.map((initial) => [initial, null]))
    : history.phonology.diachronicTable.stratum === "白"
    ? Object.entries(INITIAL_GROUP_MAP).reduce((acc, [initials, ipa]) => {
        switch (initials) {
          case "端透定":
            acc["端"] = "t";
            acc["透定"] = "tʰ";
            break;
          case "曉匣":
            acc["曉"] = "h";
            acc["匣"] = "ɦ";
            break;
          default:
            acc[initials] = ipa;
        }
        return acc;
      }, {} as Record<string, string>)
    : { ...INITIAL_GROUP_MAP }
);

const valuesArrays = [
  [...new Set(FULL_FINALS.map((final) => final[0]!))],
  [...new Set(FULL_FINALS.map((final) => final[1]!))],
  ["一", "二", "三", "四"],
  ["", "開", "合"],
];
const ALL_FULL_FINALS = computed(() =>
  [...FULL_FINALS].sort(
    precomposeComparer(
      createSortComparerFromArrays(valuesArrays, ordering.value),
      (final: string) =>
        Array.from({ length: 4 }).map((_, index) => final[index] ?? "")
    )
  )
);

const initialsMap = computed(() =>
  Object.fromEntries(
    Object.entries(ALL_INITIALS_MAP.value).filter(
      noRedundant
        ? ([initials, _]) =>
            initials
              .split("")
              .some((initial) =>
                ALL_FULL_FINALS.value.some(
                  (final) =>
                    Object.values(
                      mcIndexMap.value[final]?.[initial] ?? []
                    ).flat().length > 0
                )
              )
        : (_) => true
    )
  )
);
const fullFinals = computed(() =>
  ALL_FULL_FINALS.value
    .filter(
      noRedundant
        ? (final) => [...getLangIndexMap(final).values()].flat().length > 0
        : (_) => true
    )
    .filter(
      filterCodas
        ? (fullFinal) =>
            history.phonology.diachronicTable.filterCodas[getCoda(fullFinal)]
        : (_) => true
    )
);

function getCoda(fullFinal: string): (typeof CODAS)[number] {
  let coda = "";
  for (const [key, value] of Object.entries(CODA_MAP)) {
    if (key.includes(fullFinal[0])) {
      coda = value as any;
    }
  }
  if (typeof coda === "object") {
    coda = coda[fullFinal[1] in FINAL_MAP ? 0 : 1];
  }
  return coda;
}

const rows = computed(() =>
  fullFinals.value.map((items) =>
    ordering.value.map((index) => items[index] ?? "")
  )
);
const rowspans = computed(() => computeRowSpan(rows.value));

const header = ref<HTMLElement | null>(null);
useDraggable(header, [
  {
    ordering: itemOrdering,
    keyName: "item",
    draggable: ".item",
  },
]);

const isFullscreen = defineModel("isFullscreen", { type: Boolean });

function invert() {
  const filterCodas = history.phonology.diachronicTable.filterCodas;
  for (const key in filterCodas) {
    filterCodas[key] = !filterCodas[key];
  }
}
</script>

<template>
  <StickyTable
    :header-columns="4"
    v-model:is-fullscreen="isFullscreen"
    :blacklist="blacklist"
    :fullscreen-z-index="fullscreenZIndex"
    v-bind="$attrs"
  >
    <thead>
      <tr ref="header">
        <th
          v-for="item of itemOrdering"
          :key="item"
          group="item"
          :item="item"
          class="item draggable"
        >
          <template v-if="filterCodas && item === '攝'">
            <ConstrainedPopover trigger="click">
              <template #trigger>攝</template>

              <n-space align="center" style="margin-bottom: 0.5em">
                <span>篩選韻尾</span>
                <n-button @click="invert" class="center" text>
                  <n-icon size="medium" :component="ArrowSwap" />
                </n-button>
              </n-space>
              <n-grid cols="3" :x-gap="3">
                <n-grid-item v-for="coda of CODAS">
                  <n-checkbox
                    v-model:checked="
                      history.phonology.diachronicTable.filterCodas[coda]
                    "
                  >
                    <span class="ipa-sans">{{ coda }}</span>
                  </n-checkbox>
                </n-grid-item>
              </n-grid>
            </ConstrainedPopover>
          </template>

          <template v-else>{{ item }}</template>
        </th>

        <th
          v-for="[initials, ipa] of Object.entries(initialsMap)"
          :key="initials[0]"
        >
          <template v-if="ipa">
            <ConstrainedPopover trigger="hover">
              <template #trigger>{{ initials[0] }}</template>
              {{ initials }} </ConstrainedPopover
            >&nbsp;<span class="ipa-sans">{{ ipa }}</span>
          </template>
          <template v-else>
            {{ initials }}
          </template>
        </th>
      </tr>
    </thead>

    <tbody>
      <tr v-for="(row, index) of rows" :key="fullFinals[index]">
        <template
          v-for="(rowspan, colIndex) of rowspans[index]"
          :key="colIndex"
        >
          <th v-if="rowspan > 0" :rowspan="rowspan">
            {{ row[colIndex] }}
          </th>
        </template>

        <DiachronicTableCell
          v-for="initials of Object.keys(initialsMap)"
          :key="initials"
          :initials="initials"
          :final="fullFinals[index]!"
          :indexMap="getLangIndexMap(fullFinals[index]!, initials)"
          :language="language"
          :base-z-index="fullscreenZIndex ? fullscreenZIndex + 100 : undefined"
          v-bind="$attrs"
        />
      </tr>
    </tbody>
  </StickyTable>
</template>

<style>
.table-highlight {
  background-color: color-mix(in oklab, var(--colescu-light) 20%, white);
}
</style>
