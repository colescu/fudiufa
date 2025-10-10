<script setup lang="ts">
import { computed, inject, reactive } from "vue";
import { getFormMCUtils } from "@/views/Search/typescript/form-mc";
import { getSearchResultsByFilter } from "@/views/Search/typescript/search";
import { Language } from "@shared/lang";

import MultipleSelect from "@/components/common/MultipleSelect.vue";
import { NButton, NForm, NFormItemGi, NGrid } from "naive-ui";

const { language = "FG" } = defineProps<{ language: Language }>();
const searchWrapper = inject("searchWrapper") as any;

const FormMCUtils = getFormMCUtils();
const formMC = reactive(FormMCUtils.EMPTY_FORM);
const optionsMC = computed(() => FormMCUtils.computeOptions(formMC));

const searchMC = searchWrapper(() =>
  getSearchResultsByFilter((entry) => {
    const checker = FormMCUtils.getChecker(formMC);
    return entry?.MC != null && checker(entry.MC);
  }, language)
);
</script>

<template>
  <n-form class="grid-form" :model="formMC" @submit.prevent="searchMC">
    <n-grid cols="2 600:4" :x-gap="24">
      <n-form-item-gi
        v-for="item of FormMCUtils.ITEMS"
        :key="item"
        :label-props="{ for: item }"
        :label="item"
        :path="item"
      >
        <MultipleSelect
          :id="item"
          v-model="formMC[item]"
          :options="optionsMC[item]"
          :getLabel="
            (value) => (item === '呼' && value === '' ? '不分開合' : value)
          "
          select-all
        />
      </n-form-item-gi>
      <n-form-item-gi offset="0 600:2" class="submit">
        <n-button attr-type="submit" type="primary"> 查詢 </n-button>
      </n-form-item-gi>
    </n-grid>
  </n-form>

  <Teleport to="#help">
    表單各項爲「且」關係，54篩選可選選項。<br />
    如需更精細的查詢，請直接用 SQL 查詢<a
      href="https://github.com/colescu/fudiufa/blob/master/data/manual/hanzi.sqlite3"
      target="_blank"
      rel="noopener noreferrer"
      >數據庫</a
    >。
  </Teleport>
</template>

<style scoped></style>
