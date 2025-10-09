<script setup lang="ts">
import { ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { dictionaryCache, Language, LANGUAGE_MAP } from "@shared/lang";

import { NSpace, NRadioGroup, NRadio } from "naive-ui";

const route = useRoute();
const router = useRouter();

const props = defineProps<{ language?: Language }>();
const language = ref<Language>(props.language || "FG");

const isReady = ref<boolean>(false);

watch(
  language,
  async (newLang) => {
    isReady.value = false;
    await dictionaryCache.load(language.value);
    if (props.language && newLang !== props.language) {
      await router.push({
        name: route.name,
        params: { ...route.params, language: newLang },
        query: { ...route.query },
      });
    }
    isReady.value = true;
  },
  { immediate: true }
);
</script>

<template>
  <div>
    <n-space
      v-if="props.language"
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
