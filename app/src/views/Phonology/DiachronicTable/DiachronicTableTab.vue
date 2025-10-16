<script setup lang="ts">
import { defineAsyncComponent } from "vue";
import { useRoute } from "vue-router";
import { ROUTES_MAP } from "@/router/routes";

import DiachronicTableSettings from "./DiachronicTableSettings.vue";
const DiachronicTable = defineAsyncComponent(
  () => import("@/modules/DiachronicTable/DiachronicTable.vue")
);
import SuspenseWrapper from "@/components/wrapper/SuspenseWrapper.vue";

const route = useRoute();
</script>

<template>
  <p style="margin-bottom: 1.5em">下圖展示中古音對應的撫州話理論推導音。</p>

  <DiachronicTableSettings />

  <SuspenseWrapper>
    <DiachronicTable
      group-initials
      filter-codas
      ignore-voicing
      set-stratum
      highlight-stratum
      language="FG"
    />
  </SuspenseWrapper>

  <Teleport to="#help">
    <template v-if="route.path === ROUTES_MAP.diachronicTable">
      聲母以類劃分，例如「幫滂並」爲「幫」類。<br />
      因此圖中推導音無視送氣（見<Reference to="characteristics#全濁送氣"
        >全濁送氣</Reference
      >）。<br />
      可拖動調整韻母各列的排序優先級。<br />
      點擊攝可篩選韻尾。<br />
      推導白讀音只考慮主流白讀層。<br />
      點擊圖中的單元格可查看對應的收錄字及例外音。<br />
      例外指不符合任何層次推導音的非普化音。<br />
      <span class="gray">灰色</span>表示無收錄字。<br />
      <span class="table-highlight">背景色</span>表示與默認推導音不同。<br />
      <span class="exception">波浪線</span>表示有例外。
    </template>
  </Teleport>
</template>

<style scoped></style>
