<script setup lang="ts">
import { watch, ref } from "vue";
import { useSettingsStore } from "@/stores/settings";
import { useHistoryStore } from "@/stores/history";
import { getMCQueryUtils, MCInfoStyle, showFinal } from "@shared/mc";
import { LANGUAGE_MAP, LANGUAGES } from "@shared/lang";
import { deepCopy, deepEqual, entriesConst } from "@shared/common/object";

import Sortable from "@/components/common/Sortable.vue";
import CrossBox from "@/components/common/CrossBox.vue";
import { NSpace, NTag, NCheckboxGroup, NCheckbox, NPopselect } from "naive-ui";

const settings = useSettingsStore();
const history = useHistoryStore();

// 禁用新派

watch(
  () => settings.dictionary.disable.官,
  (disabled) => {
    if (!disabled) {
      settings.dictionary.disable.新 = false;
    }
    history.phonology.rhymeTable.filter.官 = disabled;
  }
);
watch(
  () => settings.dictionary.disable.新,
  (disabled) => {
    if (disabled) {
      settings.dictionary.disable.官 = true;
    }
    history.phonology.rhymeTable.filter.新 = disabled;
  }
);

// 音韻地位

const mcExample = getMCQueryUtils().entryAt(1207)!.MC;

const MC_INFO_STYLES = {
  默認格式: {
    comment: "",
    style: {
      ordering: ["聲母", "攝", "韻系", "等", "重紐", "呼", "聲調"],
      show: { 攝: true, 聲調: true },
      final: "韻系",
    },
  },
  "MCPDict 式": {
    comment: `<a
      href="https://github.com/MaigoAkisame/MCPDict"
      target="_blank"
      rel="noopener noreferrer"
    >漢字古今中外讀音查詢</a>`,
    style: {
      ordering: ["聲母", "攝", "韻系", "重紐", "等", "呼", "聲調"],
      show: { 攝: true, 聲調: false },
      final: "韻目",
    },
  },
  "TshetUinh 式": {
    comment: `<a
      href="https://github.com/nk2028/tshet-uinh-js"
      target="_blank"
      rel="noopener noreferrer"
    >TshetUinh.js</a>`,
    style: {
      ordering: ["聲母", "呼", "等", "重紐", "韻系", "聲調", "攝"],
      show: { 攝: false, 聲調: true },
      final: "韻系",
    },
  },
  古今手冊式: {
    comment: "《古今字音對照手冊》(1958)",
    style: {
      ordering: ["攝", "呼", "等", "重紐", "聲調", "韻系", "聲母"],
      show: { 攝: true, 聲調: true },
      final: "韻目",
    },
  },
} as Record<string, { comment: string; style: MCInfoStyle }>;

const FINAL_OPTIONS = [
  {
    label: "韻系：東",
    value: "韻系",
  },
  {
    label: "韻（分舒入）：東屋",
    value: "韻系舒入",
  },
  {
    label: "韻目：東董送屋",
    value: "韻目",
  },
];

function handleClick(item: string) {
  switch (item) {
    case "攝":
      settings.mcInfoStyle.show.攝 = !settings.mcInfoStyle.show.攝;
      break;
    case "聲調":
      settings.mcInfoStyle.show.聲調 = !settings.mcInfoStyle.show.聲調;
      if (!settings.mcInfoStyle.show.聲調) {
        settings.mcInfoStyle.final = "韻目";
      }
      break;
  }
}

watch(
  () => settings.mcInfoStyle.final,
  (final) => {
    if (final !== "韻目") {
      settings.mcInfoStyle.show.聲調 = true;
    }
  }
);

// 比較語言

const comparedLanguages = ref<string[]>([...LANGUAGES]);
watch(comparedLanguages, (value) => {
  settings.languages = LANGUAGES.filter((language) => value.includes(language));
});
</script>

<template>
  <n-space
    style="margin: auto; padding-top: 1em; width: 24em; max-width: 100%"
    vertical
  >
    <n-space align="center">
      <n-tag>禁用新派</n-tag>
      <CrossBox v-model:checked="settings.dictionary.disable.官">
        普化音
      </CrossBox>
      <CrossBox
        v-model:checked="settings.dictionary.disable.新"
        style="margin-left: -0.5em"
      >
        新派音
      </CrossBox>
    </n-space>

    <!-- <n-space align="center">
      <n-tag>例字</n-tag>
      <span>突出<span class="char">顏色</span></span>
      <n-switch v-model:value="settings.colorizeChar" />
    </n-space> -->

    <n-space vertical>
      <n-space align="center">
        <n-tag>音韻地位</n-tag>
        <Sortable v-model="settings.mcInfoStyle.ordering" v-slot="{ item }">
          <ruby
            class="under draggable transition"
            style="padding: 0 0.2em"
            :class="{
              gray: Object.entries(settings.mcInfoStyle.show).some(
                ([part, show]) => item === part && !show
              ),
            }"
            @click="handleClick(item)"
          >
            <rb style="font-size: 1.2em">
              {{
                item === "韻系"
                  ? showFinal(mcExample, settings.mcInfoStyle.final)
                  : mcExample[item as keyof typeof mcExample]
              }}
            </rb>
            <rp>(</rp>
            <rt v-if="item !== '韻系'">{{ item }}</rt>
            <n-popselect
              v-else
              trigger="click"
              placement="bottom-start"
              v-model:value="settings.mcInfoStyle.final"
              :options="FINAL_OPTIONS"
            >
              <rt>韻</rt>
            </n-popselect>
            <rp>)</rp>
          </ruby>
        </Sortable>
      </n-space>

      <n-space align="start">
        <div style="margin-left: 3em; margin-top: -0.05em">預設</div>
        <n-space style="gap: 0.3em" vertical>
          <n-checkbox
            v-for="[label, { comment, style }] of entriesConst(MC_INFO_STYLES)"
            :key="label"
            :checked="deepEqual(settings.mcInfoStyle, style)"
            @click="settings.mcInfoStyle = deepCopy(style)"
          >
            {{ label }}
            <Tooltip v-if="comment" marker="?" trigger-style="margin: -0.1em">
              <span v-html="comment" />
            </Tooltip>
            ：{{ mcExample.音韻地位(style) }}
          </n-checkbox>
        </n-space>
      </n-space>
    </n-space>

    <n-space align="center">
      <n-tag>韻母排序</n-tag>
      <Sortable v-model="settings.finalOrdering" v-slot="{ item }">
        <span
          :key="item"
          class="draggable"
          style="font-size: 1.1em; margin-right: 0.8em"
        >
          {{ item }}
        </span>
      </Sortable>
    </n-space>

    <n-space align="center">
      <n-tag>比較語言</n-tag>
      <n-checkbox-group v-model:value="comparedLanguages">
        <template v-for="[langEN, langCN] of Object.entries(LANGUAGE_MAP)">
          <n-checkbox
            v-if="langEN !== 'FG'"
            :value="langEN"
            :label="langCN"
            style="margin-right: 0.3em"
          />
        </template>
      </n-checkbox-group>
    </n-space>

    <Teleport to="#help">
      可拖動調整音韻地位各部分的順序。<br />
      可點擊隱藏攝或聲調，或選擇韻的格式。<br />
      可拖動調整韻母各部分的排序優先級。
    </Teleport>
  </n-space>
</template>

<style scoped>
.transition {
  transition: color 0.3s ease;
}
</style>
