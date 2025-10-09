<script setup lang="ts">
import { inject } from "vue";
import { useHistoryStore } from "@/stores/history";

import { NCard, NSpace, NTag, NCheckbox } from "naive-ui";

const history = useHistoryStore();

const hasComment = inject("hasComment");
</script>

<template>
  <n-card class="center" style="width: fit-content; margin: auto">
    <n-space align="center">
      <n-tag size="small">顯示信息</n-tag>
      <div>
        <n-checkbox
          v-model:checked="history.phonology.predict.show.frequency"
          style="margin-right: 0.3em"
        >
          頻度
        </n-checkbox>
        <n-checkbox
          v-model:checked="history.phonology.predict.show.comment"
          :disabled="!hasComment"
          style="margin-right: -0.8em"
        >
          注釋
        </n-checkbox>
      </div>
    </n-space>
  </n-card>
</template>

<style scoped></style>
