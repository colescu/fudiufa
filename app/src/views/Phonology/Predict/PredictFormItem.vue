<script setup lang="ts">
import { computed, h, watch } from "vue";
import { useWindowSize } from "@vueuse/core";
import {
  getFieldOptions,
  getGroup,
  GROUP_OPTIONS,
} from "@/views/Phonology/Predict/form";
import { LANGUAGE_MAP } from "@shared/lang";
import { FeatureKey, LangFeatureKey } from "@/modules/ReflexTable/types";

import { NSpace, NSelect, NIcon } from "naive-ui";
import { CornerDownRight as DownRight } from "@vicons/tabler";

const formItem = defineModel<FeatureKey | LangFeatureKey>({
  required: true,
});

const { includeLang } = defineProps<{
  includeLang?: boolean;
}>();

const languageOptions = computed(() => {
  const options = [
    { value: "MC", label: "中古漢語" },
    ...Object.entries(LANGUAGE_MAP).map(([langEN, langCN]) => ({
      value: langEN,
      label: langCN,
    })),
  ];
  if (includeLang) {
    options.splice(1, 0, { value: "lang", label: "現代方言" });
  }
  return options;
});

const fieldOptions = computed(() => [
  ...getFieldOptions(formItem.value.language, formItem.value.group),
]);

watch(
  formItem,
  () => {
    const options = (
      formItem.value.group == ""
        ? fieldOptions.value.map((option) => (option as any).children).flat()
        : fieldOptions.value
    ).map((option) => (option as any).value);
    if (!options.includes(formItem.value.field)) {
      formItem.value.field = "";
    } else {
      formItem.value.group = getGroup(
        formItem.value.language,
        formItem.value.field
      );
    }
  },
  { immediate: true, deep: true }
);

const { width } = useWindowSize();
const isWide = computed(() => width.value >= 600);
</script>

<template>
  <n-space :vertical="!isWide">
    <n-space align="center">
      <n-select
        v-model:value="formItem.language"
        :options="languageOptions"
        class="select-language"
      />
      <n-select
        v-model:value="formItem.group"
        :options="GROUP_OPTIONS"
        class="select-group"
      />
    </n-space>

    <n-space align="center" :style="{ marginLeft: isWide ? '0' : '1em' }">
      <n-icon v-if="!isWide" :component="DownRight" size="large" />
      <n-select
        v-model:value="formItem.field"
        :options="fieldOptions"
        :render-label="(option: any) => h('span', { innerHTML: String(option.label) })"
        class="select-field"
      >
        <template #empty> 請先選擇語言 </template>
      </n-select>
    </n-space>
  </n-space>
</template>

<style scoped>
.select-language {
  width: 7.5em;
}

.select-group {
  width: 5.5em;
}

.select-field {
  width: 12em;
}
</style>
