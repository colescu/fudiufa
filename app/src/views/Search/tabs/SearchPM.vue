<script setup lang="ts">
import { inject, ref } from "vue";
import { fetchCharsByPM } from "@/views/Search/typescript/search-pron";
import { getSearchResultsByChars } from "@/views/Search/typescript/search";
import { LangEntry, Language } from "@shared/lang";

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

const formPM = ref<string>("");

const searchPM = searchWrapper(async () => {
  try {
    const chars = await fetchCharsByPM(formPM.value);
    return getSearchResultsByChars(chars, language);
  } catch (error) {
    console.error("Error fetching the Putonghua dictionary:", error);
    message.error("錯誤：未能獲取普通話字典！");
    return [] as LangEntry[];
  }
});
</script>

<template>
  <n-space align="center">
    <n-form inline class="search-input" @submit.prevent="searchPM">
      <n-form-item>
        <n-input
          :input-props="{ name: 'PM' }"
          v-model:value="formPM"
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
    聲調可用变音符 (<span class="pinyin">āáǎà</span>) 或數字 (1234) 。<br />
    數據來自<a
      href="https://github.com/mozillazg/pinyin-data/blob/master/kXHC1983.txt"
      target="_blank"
      rel="noopener noreferrer"
      >《現代漢語詞典》</a
    >
    。
  </Teleport>
</template>

<style scoped></style>
