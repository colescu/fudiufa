<script setup lang="ts">
import { computed, provide, reactive, ref, toRef, watch } from "vue";
import { useRouter } from "vue-router";
import { useSettingsStore } from "@/stores/settings";
import { useHistoryStore } from "@/stores/history";
import { useDraggable } from "@/composables/useDraggable";
import { Relator } from "./typescript/relator";
import { getFeature } from "./typescript/feature";
import { getComment } from "./typescript/commentator";
import { ColumnData, Feature, ValidFeatureKey } from "./types";
import { ValidPredictForm } from "@/views/Phonology/Predict/types";
import { MCEntry } from "@shared/mc";
import { Language, LANGUAGE_MAP, LANGUAGES } from "@shared/lang";
import {
  cartesianProduct,
  deepEqual,
  fromEntriesConst,
} from "@shared/common/object";
import { computeRowSpan } from "@/library/dom/pure";

import StickyTable from "@/components/common/StickyTable.vue";
import Possibility from "./Possibility.vue";
import DiachronicTable from "@/modules/DiachronicTable/DiachronicTable.vue";
import { DiachronicTableState } from "../DiachronicTable/types";

const router = useRouter();
const settings = useSettingsStore();

const history = useHistoryStore();
const languages = toRef(history, "languageOrdering");

const form = defineProps<ValidPredictForm>();

const featureXs = computed<Feature[]>(() => form.Xs.map(getFeature));
const featureKeyYs = computed<["MC" | Language, ValidFeatureKey][]>(() =>
  form.Y.language === "lang"
    ? languages.value.map((language) => [
        language,
        { ...form.Y, language } as ValidFeatureKey,
      ])
    : [[form.Y.language, form.Y]]
);

const tableData = computed<Partial<Record<"MC" | Language, ColumnData>>>(() =>
  fromEntriesConst(
    featureKeyYs.value
      .filter(([language, featureKeyY]) =>
        form.Xs.every((featureKeyX) => !deepEqual(featureKeyX, featureKeyY))
      )
      .map(([language, featureKeyY]) => [
        language,
        new Relator(
          (entry: MCEntry) =>
            JSON.stringify(
              featureXs.value.map((featureX) => featureX.getter(entry))
            ),
          getFeature(featureKeyY).getter,
          (xs, y) => getComment(form.Xs, featureKeyY, xs, y)
        ).columnData,
      ])
  )
);

const hasComment = computed<boolean>(() =>
  Object.values(tableData.value)
    .map((columnData) => Object.values(columnData))
    .flat()
    .flat()
    .some((possibilityData) => !!possibilityData.comment)
);
provide("hasComment", hasComment);
const emit = defineEmits<{ update: [boolean] }>();
watch(
  form,
  () => {
    emit("update", hasComment.value);
  },
  { immediate: true }
);

const rows = computed<string[][]>(() => {
  const allValues = cartesianProduct(
    ...featureXs.value.map((featureX) => featureX.values)
  );
  const validValueSet = new Set(
    Object.keys(Object.values(tableData.value)[0]!)
  );
  return allValues.filter((value) => validValueSet.has(JSON.stringify(value)));
});
const rowspans = computed(() => computeRowSpan(rows.value));

const columns = computed<{ key: "MC" | Language; label: string }[]>(() => {
  if (form.Y.language === "MC") {
    return [{ key: "MC", label: "中古漢語" }];
  } else {
    return (Object.keys(tableData.value) as Language[]).map((language) => ({
      key: language,
      label: LANGUAGE_MAP[language],
    }));
  }
});

function showPossibility(value: string, featureKey: ValidFeatureKey): string {
  return getFeature(featureKey).shower?.(value, settings) ?? (value || "無");
}

function hashFeatureKey(featureKey: ValidFeatureKey): string {
  return featureKey.field + featureKey.language;
}

function getTableUrl(
  xs: string[],
  y: string,
  languageY: "MC" | Language
): string {
  return router.resolve({
    path: "/xiauynbiau",
    query: {
      tiauqien: JSON.stringify([
        ...form.Xs.map((featureKeyX, index) => ({
          ...featureKeyX,
          value: xs[index],
        })),
        {
          language: languageY,
          field: form.Y.field,
          value: y,
        },
      ]),
    },
  }).href;
}

const header = ref<HTMLElement | null>(null);
useDraggable(header, [
  {
    ordering: toRef(form, "Xs"),
    keyName: "x",
    keyGetter: hashFeatureKey,
    draggable: ".x",
  },
  {
    ordering: languages,
    keyName: "language",
    draggable: ".language",
  },
]);

const diachronicTableState = reactive<DiachronicTableState>({
  isFullscreen: false,
  mcIndices: [],
  langIndices: [],
});
provide("diachronicTableState", diachronicTableState);
</script>

<template>
  <div>
    <StickyTable v-if="rows.length <= 300" :headerColumns="form.Xs.length">
      <thead>
        <tr ref="header">
          <th
            v-for="(featureKeyX, index) of form.Xs"
            :key="hashFeatureKey(featureKeyX)"
            group="x"
            :x="hashFeatureKey(featureKeyX)"
            :class="form.Xs.length > 1 ? ['x', 'draggable'] : []"
          >
            {{
              featureKeyX.language === "MC"
                ? "中古"
                : LANGUAGE_MAP[featureKeyX.language]
            }}<br />
            {{ featureXs[index]!.label }}
          </th>

          <th
            v-for="column of columns"
            :key="column.key"
            group="language"
            :language="column.key"
            :class="(LANGUAGES as string[]).includes(column.key) ? ['language', 'draggable'] : []"
          >
            {{ column.label }}<br />
            {{ getFeature(featureKeyYs[0]![1]).label }}
          </th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="(xs, rowIndex) of rows">
          <template v-for="(rowspan, index) of rowspans[rowIndex]">
            <th
              v-if="rowspan > 0"
              :key="index"
              :rowspan="rowspan"
              v-html="showPossibility(xs[index]!, form.Xs[index]!)"
            />
          </template>

          <td
            v-for="column of columns"
            :key="column.key"
            :language="column.key"
          >
            <Possibility
              v-for="(possibility, index) of tableData[column.key]![JSON.stringify(xs)]"
              :key="index"
              :possibility="{
                ...possibility,
                value: showPossibility(possibility.value, {
                  ...form.Y,
                  language: column.key,
                } as ValidFeatureKey),
              }"
              :mc-indices="diachronicTableState.mcIndices ?? []"
              :table-url="getTableUrl(xs, possibility.value, column.key)"
            />
          </td>
        </tr>
      </tbody>
    </StickyTable>

    <div v-else class="center" style="margin: 2em auto">
      表格過大，請減少自變量的可能取值數。
      <!-- FEATURE filtered ReflexTable -->
    </div>

    <DiachronicTable
      v-if="diachronicTableState.isFullscreen"
      v-model:is-fullscreen="diachronicTableState.isFullscreen"
      :mc-indices="diachronicTableState.mcIndices ?? []"
      :lang-indices="diachronicTableState.langIndices ?? []"
      show-count
      no-redundant
    />
  </div>
</template>

<style scoped>
td {
  max-width: 8em;
}

tr > td:first-of-type:last-of-type {
  max-width: 16em;
}
</style>
