<script setup lang="ts">
import { computed, type VNodeChild } from "vue";

import { NSelect, type SelectOption } from "naive-ui";

const { modelValue, options, getLabel, selectAll } = defineProps<{
  modelValue: string[];
  options: string[];
  getLabel?: (option: string) => string;
  renderLabel?: (option: SelectOption) => VNodeChild;
  selectAll?: boolean;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: string[]): void;
}>();

const allSelectOptions = computed<SelectOption[]>(() => {
  const selectOptions = options.map((option: string) => ({
    label: getLabel ? getLabel(option) : option,
    value: option,
  }));
  if (selectAll) {
    return [
      ...selectOptions,
      {
        label: "全選",
        value: "__all__",
      },
    ];
  } else {
    return selectOptions;
  }
});

function handleSelect(value: string[]) {
  emit(
    "update:modelValue",
    value.includes("__all__")
      ? options
      : value.filter((option) => options.includes(option))
  );
}

// IMPROVE DESIGN better option UI
</script>

<template>
  <n-select
    :value="modelValue"
    :options="allSelectOptions"
    :render-label="renderLabel"
    @update:value="handleSelect"
    placeholder=""
    multiple
    clearable
  />
</template>

<style scoped></style>
