<script setup lang="ts">
import { ref, watch } from "vue";
import { dictionaryCache, Language, LANGUAGE_MAP } from "@shared/lang";

import { NSpace, NRadioGroup, NRadio } from "naive-ui";

const isAuth = localStorage.user === "colescu";
const language = ref<Language>(
  ((isAuth ? localStorage.getItem("lastLanguage") : undefined) ??
    "FG") as Language
);

const isReady = ref<boolean>(false);
watch(
  language,
  async (newLanguage) => {
    isReady.value = false;
    await dictionaryCache.load(newLanguage);
    localStorage.setItem("lastLanguage", newLanguage);
    isReady.value = true;
  },
  { immediate: true, deep: true }
);
</script>

<template>
  <div>
    <n-space
      v-if="isAuth"
      align="center"
      justify="center"
      style="margin-bottom: 1.5em"
    >
      <n-radio-group v-model:value="language" name="language" size="small">
        <n-radio
          v-for="(langCN, langEN) in LANGUAGE_MAP"
          :key="langEN"
          :value="langEN"
          :label="langCN"
        />
      </n-radio-group>
    </n-space>
    <RouterView v-slot="{ Component }">
      <component v-if="isReady" :is="Component" :language="language" />
    </RouterView>
  </div>
</template>

<style scoped></style>
