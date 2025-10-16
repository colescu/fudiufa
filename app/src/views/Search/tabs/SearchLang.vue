<script setup lang="ts">
import { computed, h, inject, ref, toRef, watch } from "vue";
import { useSettingsStore } from "@/stores/settings";
import { useHistoryStore } from "@/stores/history";
import { renderParts, toneUtils } from "@shared/syllable";
import {
  getFormLangUtils,
  ITEMS_MAP,
} from "@/views/Search/typescript/form-lang";
import { getSearchResultsByFilter } from "@/views/Search/typescript/search";
import { computeGridOffset } from "@/library/dom/pure";
import { Language } from "@shared/lang";

import MultipleSelect from "@/components/common/MultipleSelect.vue";
import {
  NSpace,
  NButton,
  NForm,
  NFormItem,
  NInput,
  NFormItemGi,
  NGrid,
  NSlider,
} from "naive-ui";

const settings = useSettingsStore();
const history = useHistoryStore();
const langMode = toRef(history.search, "langMode");

const { language = "FG" } = defineProps<{ language: Language }>();
const searchWrapper = inject("searchWrapper") as any;

const LANG_MODES = {
  0: { label: "不拆分", value: null },
  1: { label: "聲韻調", value: "final" },
  2: { label: "韻母 = 韻 + 介音", value: "rhyme" },
  3: { label: "韻母 = 介音 + 韻腹 + 韻尾", value: "full" },
} as const;
type LangMode = keyof typeof LANG_MODES;

const formPinyin = ref<string>("");

const searchPinyin = searchWrapper(() => {
  const { parse } = toneUtils[language];
  const [syllable, tone] = parse(formPinyin.value);
  // manually add in 6
  const tones =
    formPinyin.value.normalize("NFD").includes("̄") && tone === "1"
      ? "16"
      : tone;
  return getSearchResultsByFilter((entry) => {
    if (tones === "") {
      return entry.讀音.replace(/\d/g, "") === syllable;
    } else {
      return tones.split("").some((tone) => syllable + tone === entry.讀音);
    }
  }, language);
});

const FormLangUtils = computed(() =>
  getFormLangUtils(
    language,
    LANG_MODES[langMode.value as LangMode].value ?? "full"
  )
);
const formLang = ref(FormLangUtils.value.EMPTY_FORM);
const optionsLang = computed(() =>
  FormLangUtils.value.computeOptions(formLang.value)
);

const searchLang = searchWrapper(() =>
  getSearchResultsByFilter(
    FormLangUtils.value.getChecker(formLang.value),
    language
  )
);

watch(
  langMode,
  () => {
    formLang.value = FormLangUtils.value.EMPTY_FORM;
  },
  { immediate: true }
);

const offset = computed<string>(() => {
  const numItems =
    ITEMS_MAP[LANG_MODES[langMode.value as LangMode].value ?? "full"].length;
  return `${computeGridOffset(numItems, 2)} 600:${computeGridOffset(
    numItems,
    4
  )}`;
});
</script>

<template>
  <n-space align="center" justify="center" style="margin: 1em auto">
    <div>拆分程度：</div>
    <n-slider
      v-model:value="langMode"
      :min="0"
      :max="3"
      :format-tooltip="(key) => LANG_MODES[key as LangMode].label"
      style="width: 12em"
    />
  </n-space>

  <n-space v-if="langMode === 0" align="center" style="margin-top: -1em">
    <n-form inline class="search-input" @submit.prevent="searchPinyin">
      <n-form-item>
        <n-input
          :input-props="{ name: 'pinyin' }"
          v-model:value="formPinyin"
          placeholder="請輸入拼音"
          clearable
        />
      </n-form-item>
      <n-form-item>
        <n-button attr-type="submit" type="primary"> 查詢 </n-button>
      </n-form-item>
    </n-form>
  </n-space>

  <n-form
    v-else
    class="grid-form"
    :model="formLang"
    @submit.prevent="searchLang"
    style="margin-top: 2em"
  >
    <n-grid cols="2 600:4" :x-gap="24">
      <n-form-item-gi
        :label-props="{ for: item }"
        v-for="item of FormLangUtils.ITEMS"
        :key="item"
        :label="item"
        :path="item"
      >
        <MultipleSelect
          :id="item"
          v-model="formLang[item]"
          :options="optionsLang[item]"
          :get-label="FormLangUtils.getOptionLabel![item](settings.format)"
          :render-label="(option) => h('div', {'innerHTML': renderParts(option.label as string, settings.format)})"
          select-all
        />
      </n-form-item-gi>
      <n-form-item-gi :offset="offset" class="submit">
        <n-button attr-type="submit" type="primary"> 查詢 </n-button>
      </n-form-item-gi>
    </n-grid>
  </n-form>

  <Teleport to="#help">
    <template v-if="langMode === 0">
      注意使用变音符時可同時查詢陰平與陽去。
    </template>
    <template v-else>
      表單各項爲「且」關係，自動篩選可選選項。<br />
      如需更精細的查詢，請直接用 SQL 查詢<a
        href="https://github.com/colescu/fudiufa/blob/master/data/manual/hanzi.sqlite3"
        target="_blank"
        rel="noopener noreferrer"
        >數據庫</a
      >。
    </template>
  </Teleport>
</template>

<style scoped></style>
