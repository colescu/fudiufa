<script setup lang="ts">
import { toRef, defineAsyncComponent, watch, ref, provide } from "vue";
import { useRoute } from "vue-router";
import { useHistoryStore } from "@/stores/history";
import { ROUTES_MAP } from "@/router/routes";

import PredictForm from "./PredictForm.vue";
import ReflexTableSettings from "@/views/Phonology/Predict/ReflexTableSettings.vue";
const ReflexTable = defineAsyncComponent(
  () => import("@/modules/ReflexTable/ReflexTable.vue")
);
import SuspenseWrapper from "@/components/wrapper/SuspenseWrapper.vue";

const route = useRoute();

const history = useHistoryStore();
const form = toRef(history.phonology.predict, "form");

// Ad hoc passing between children
const hasComment = ref<boolean>(false);
provide("hasComment", hasComment);

const key = ref(0);
watch(form, () => {
  key.value++;
});
</script>

<template>
  <PredictForm />

  <ReflexTableSettings v-if="form != null" style="margin-top: 1.5em" />

  <SuspenseWrapper :key="key">
    <ReflexTable
      v-if="form != null"
      @update="(value) => (hasComment = value)"
      v-bind="form"
      :key="key"
    />
  </SuspenseWrapper>

  <Teleport to="#help">
    <template v-if="route.path === ROUTES_MAP.predict">
      推導器只考慮理論推導音，無視例外。<br />
      出現頻度依《廣韻》字數。<br />
      推導普通話、廣州話的數據來自
      <a
        href="https://en.wiktionary.org/wiki/Module:ltc-pron/predict"
        target="_blank"
        rel="noopener noreferrer"
        >Wiktionary</a
      >。<br />
      推導上海話（主流層）的數據來自
      <a
        href="https://zhuanlan.zhihu.com/p/386456940"
        target="_blank"
        rel="noopener noreferrer"
        >Nyoeghau</a
      >。<br />
      其餘推導數據爲筆者本人整理。<br />
      推導撫州話（老文讀）的規則見
      <a
        href="https://raw.githubusercontent.com/colescu/fuzhou-gan-backend/refs/heads/main/src/%E6%8E%A8%E5%B0%8E%E6%92%AB%E5%B7%9E%E8%A9%B1.py"
        target="_blank"
        rel="noopener noreferrer"
        >Python 脚本</a
      >。<br />
      可拖動標題行以調整列的順序。<br />
      點擊單元格內的項可查看對應的中古小韻表。
    </template>
  </Teleport>
</template>

<style scoped></style>
