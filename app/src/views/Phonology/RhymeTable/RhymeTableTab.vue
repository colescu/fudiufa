<script setup lang="ts">
import { defineAsyncComponent } from "vue";
import { useRoute } from "vue-router";
import { ROUTES_MAP } from "@/router/routes";

import RhymeTableSettings from "./RhymeTableSettings.vue";
const RhymeTable = defineAsyncComponent(
  () => import("@/modules/RhymeTable/RhymeTable.vue")
);
import SuspenseWrapper from "@/components/wrapper/SuspenseWrapper.vue";

const route = useRoute();
</script>

<template>
  <div style="margin-bottom: 1.5em">
    <p>撫州話共計<strong>約五百個音節</strong>（不計聲調）。</p>
  </div>

  <RhymeTableSettings />

  <SuspenseWrapper>
    <RhymeTable parts-columns language="FG" />
  </SuspenseWrapper>

  <Teleport to="#help">
    <template v-if="route.path === ROUTES_MAP.rhymeTable">
      韻母依字典序排列，可拖動調整各部分的優先級。<br />
      點擊韻圖中的單元格可查看該音節的所有收錄字。<br />
      字頭爲數據庫中存储的形式，採用大陸繁體。<br />
      <span class="輕">灰色</span>標記輕聲字。「<span class="char">□</span
      >」表示本字不明。
    </template>
  </Teleport>
</template>

<style scoped></style>
