<script setup lang="ts">
import { computed, ref, toRef } from "vue";
import { useSettingsStore } from "@/stores/settings";
import { useHistoryStore } from "@/stores/history";
import { useDraggable } from "@/composables/useDraggable";
import { Language, LANGUAGE_MAP, LANGUAGES } from "@shared/lang";
import { MCEntry } from "@shared/mc";

import StickyTable from "@/components/common/StickyTable.vue";

const settings = useSettingsStore();
const history = useHistoryStore();
const languages = toRef(history, "languageOrdering");

const { entries } = defineProps<{ entries: MCEntry[] }>();

const columns = computed<
  {
    title: string;
    key: string;
  }[]
>(() => [
  ...[
    {
      title: "例字",
      key: "char",
    },
    {
      title: "音韻地位",
      key: "MCInfo",
    },
  ],
  ...languages.value.map((language) => ({
    title: LANGUAGE_MAP[language],
    key: language,
  })),
]);

const rows = computed<Record<string, string>[]>(() =>
  entries.map((entry) => ({
    char: entry.MC.字,
    MCInfo: entry.MC.音韻地位(settings.mcInfoStyle),
    ...Object.fromEntries(
      languages.value.map((language) => [language, entry.reflex[language]])
    ),
  }))
);

const header = ref<HTMLElement | null>(null);
useDraggable(header, [
  {
    ordering: languages,
    keyName: "language",
    draggable: ".language",
  },
]);

// PROBLEMS: sort MCInfo; show only one per tone; show all chars; slow
// Replaced by DiachronicTable, can ignore for now
</script>

<template>
  <StickyTable :header-columns="[]">
    <thead>
      <tr ref="header">
        <th
          v-for="column of columns"
          :key="column.key"
          group="language"
          :language="column.key"
          :class="(LANGUAGES as string[]).includes(column.key) ? ['language', 'draggable'] : []"
        >
          {{ column.title }}
        </th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(row, index) of rows" :key="index">
        <td
          v-for="column of columns"
          :key="column.key"
          :class="{ 'align-left': column.key === 'MCInfo' }"
        >
          <template v-if="!(LANGUAGES as string[]).includes(column.key)">
            {{ row[column.key as keyof typeof row] }}
          </template>
          <template v-else>
            <Pronunciation
              :pronunciation="row[column.key]!"
              :language="column.key as Language"
            />
          </template>
        </td>
      </tr>
    </tbody>
  </StickyTable>
</template>

<style scoped>
.align-left {
  text-align: left;
}
</style>
