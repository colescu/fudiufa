<script setup lang="ts">
import { useHistoryStore } from "@/stores/history";

import { NCard, NSpace, NTag, NRadioGroup, NRadioButton } from "naive-ui";

const history = useHistoryStore();

const STRATA_OPTIONS = Object.entries({
  "": "默認",
  白: "白讀",
  新: "新派",
}).map(([value, label]) => ({ value, label }));
</script>

<template>
  <n-card class="card">
    <n-space vertical :style="{ gap: '1em' }">
      <n-space align="center">
        <n-tag>設定層次</n-tag>
        <n-radio-group
          v-model:value="history.phonology.diachronicTable.stratum"
          name="stratum"
          size="small"
        >
          <n-radio-button
            v-for="option of STRATA_OPTIONS"
            :key="option.value"
            :value="option.value"
            :label="option.label"
          />
        </n-radio-group>
      </n-space>
    </n-space>
  </n-card>
</template>

<style scoped></style>
