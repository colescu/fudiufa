<script setup lang="ts">
import { useHistoryStore } from "@/stores/history";

import CrossBox from "@/components/common/CrossBox.vue";
import { NCard, NSpace, NTag } from "naive-ui";

const history = useHistoryStore();
</script>

<template>
  <n-card class="card">
    <n-space vertical :style="{ gap: '1em' }">
      <n-space align="center">
        <n-tag>剔除層次</n-tag>
        <CrossBox
          v-for="stratum of (['老', '新', '官'] as const)"
          :key="stratum"
          v-model:checked="history.phonology.rhymeTable.filter[stratum]"
          class="rhyme-table-settings"
          style="margin-right: -0.5em"
        >
          <span :class="stratum">{{ stratum }}</span>
        </CrossBox>
      </n-space>
    </n-space>
  </n-card>
</template>

<style scoped></style>
