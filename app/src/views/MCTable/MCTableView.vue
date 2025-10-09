<script setup lang="ts">
import { computed, defineAsyncComponent } from "vue";
import { useRoute } from "vue-router";
import { useSettingsStore } from "@/stores/settings";
import { mcCache, MCEntry } from "@shared/mc";
import { Language, LANGUAGE_MAP } from "@shared/lang";

const MCTable = defineAsyncComponent(() => import("./MCTable.vue"));

const settings = useSettingsStore();

const route = useRoute();

type Condition = ValidFeatureKey & { value: string };
const conditions: Condition[] = JSON.parse(route.query.tiauqien as string);

const syllables = computed<MCEntry[]>(() =>
  Object.values(mcCache.get()).filter((entry) =>
    conditions.every(
      (condition) => getFeature(condition).getter(entry) === condition.value
    )
  )
);

function showPossibility(value: string, featureKey: ValidFeatureKey): string {
  return getFeature(featureKey).shower?.(value, settings) ?? (value || "無");
}

function displayCondition(condition: Condition): string {
  const language = condition.language as Language | "MC";
  return [
    language === "MC" ? "中古" : LANGUAGE_MAP[language],
    getFeature(condition).label,
    ` <span class="operator">=</span> `,
    showPossibility(condition.value, { ...condition }),
  ].join("");
}

import { onBeforeMount, onMounted } from "vue";
import SuspenseWrapper from "@/components/wrapper/SuspenseWrapper.vue";
import { ValidFeatureKey } from "@/modules/ReflexTable/types";
import { getFeature } from "@/modules/ReflexTable/typescript/feature";

let start: number;

onBeforeMount(() => {
  start = performance.now();
});

onMounted(() => {
  const end = performance.now();
  console.log(`Mounted in ${end - start} ms`);
});
</script>

<template>
  <div>
    <div
      v-for="condition of conditions"
      class="title"
      v-html="displayCondition(condition)"
    />

    <SuspenseWrapper>
      <MCTable :entries="syllables" />
    </SuspenseWrapper>

    <Teleport to="#help"> 讀音均爲推導音。 </Teleport>
  </div>
</template>

<style scoped>
.title {
  font-size: 1.2em;
  text-align: center;
}
</style>
