<script setup lang="ts">
import { reactive, toRef } from "vue";
import { useHistoryStore } from "@/stores/history";
import { PredictFormUtils } from "./form";
import { PredictForm, ValidPredictForm } from "./types";
import { deepCopy, deepEqual } from "@shared/common/object";

import PredictFormItem from "./PredictFormItem.vue";
import { NCard, NSpace, NForm, NButton, NIcon, useMessage } from "naive-ui";
import { Plus, Minus, X } from "@vicons/tabler";
import { ArrowSwap20Regular as ArrowSwap } from "@vicons/fluent";

const message = useMessage();

const { getEmptyForm, checkForm, getFormActions } = PredictFormUtils;

const history = useHistoryStore();
const savedForm = toRef(history.phonology.predict, "form");

const form = reactive<PredictForm>(deepCopy(savedForm.value) ?? getEmptyForm());

function submitForm() {
  if (!checkForm(form)) {
    message.error("請提交合法表單！");
    return;
  }
  if (form.Xs.some((X) => deepEqual(X, form.Y))) {
    message.error("自變量包含因變量！");
    return;
  }
  if (!form.Xs.map((featureKey) => featureKey.group).includes(form.Y.group)) {
    message.error("自變量與因變量無明顯相關性！");
    return;
  }
  savedForm.value = deepCopy(form) as ValidPredictForm;
}

const { addX, deleteX, clear, reverse } = getFormActions(form);
</script>

<template>
  <n-card class="card">
    <n-form inline :model="form" @submit.prevent="submitForm">
      <n-space vertical :style="{ gap: '0.5em' }">
        <n-space
          v-for="(_, index) of form.Xs"
          :key="index"
          align="start"
          vertical
        >
          <PredictFormItem v-model="form.Xs[index]!" />
        </n-space>

        <div class="center">
          <span style="font-size: 1.5em">↓</span>
          推導
        </div>

        <n-space align="start" vertical>
          <PredictFormItem v-model="form.Y" include-lang />
        </n-space>

        <n-space align="center" justify="end" style="margin-top: 0.5em">
          <n-button v-if="form.Xs.length === 1" @click="reverse" text>
            <n-icon size="large" :component="ArrowSwap" />
          </n-button>
          <n-button
            @click="
              clear!();
              savedForm = null;
            "
            text
          >
            <n-icon size="large" :component="X" />
          </n-button>
          <n-button @click="addX" :disabled="form.Xs.length >= 5" text>
            <n-icon size="large" :component="Plus" />
          </n-button>
          <n-button @click="deleteX" :disabled="form.Xs.length <= 1" text>
            <n-icon size="large" :component="Minus" />
          </n-button>
          &nbsp;
          <n-button attr-type="submit" type="primary">確定</n-button>
        </n-space>
      </n-space>
    </n-form>
  </n-card>
</template>

<style scoped>
.card {
  width: max-content;
}

.n-button {
  vertical-align: middle;
}
</style>
