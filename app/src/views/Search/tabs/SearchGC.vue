<script setup lang="ts">
import { inject, ref } from "vue";
import { fetchCharsByGC } from "@/views/Search/typescript/search-pron";
import { getSearchResultsByChars } from "@/views/Search/typescript/search";
import { Language } from "@shared/lang";

import {
  NButton,
  NForm,
  NFormItem,
  NInput,
  NSpace,
  useMessage,
} from "naive-ui";

const message = useMessage();

const { language = "FG" } = defineProps<{ language: Language }>();
const searchWrapper = inject("searchWrapper") as any;

const formGC = ref<string>("");

const searchGC = searchWrapper(async () => {
  try {
    const chars = await fetchCharsByGC(formGC.value);
    return getSearchResultsByChars(chars, language);
  } catch (error) {
    console.error("Error fetching the Cantonese dictionary:", error);
    message.error("錯誤：未能獲取廣州話字典！");
  }
});
</script>

<template>
  <n-space align="center">
    <n-form inline class="search-input" @submit.prevent="searchGC">
      <n-form-item>
        <n-input
          :input-props="{ name: 'GC' }"
          v-model:value="formGC"
          placeholder="請輸入拼音"
          clearable
        />
      </n-form-item>
      <n-form-item>
        <n-button attr-type="submit" type="primary"> 查詢 </n-button>
      </n-form-item>
    </n-form>
  </n-space>

  <Teleport to="#help">
    拼音方案爲粵拼。<br />
    數據來自<a
      href="https://github.com/jyutnet/cantonese-books-data/blob/master/2004_%E5%BB%A3%E5%B7%9E%E8%A9%B1%E6%AD%A3%E9%9F%B3%E5%AD%97%E5%85%B8/B01_%E8%B3%87%E6%96%99.json"
      target="_blank"
      rel="noopener noreferrer"
      >《廣州話正音字典》</a
    >
    。
  </Teleport>
</template>

<style scoped></style>
