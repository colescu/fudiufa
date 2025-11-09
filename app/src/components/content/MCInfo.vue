<script setup lang="ts">
import { computed } from "vue";
import { useSettingsStore } from "@/stores/settings";
import { getMCQueryUtils, MCEntry } from "@shared/mc";
import {
  getLangQueryUtils,
  getReflexMapByMC,
  Language,
  LANGUAGE_MAP,
  LANGUAGES,
} from "@shared/lang";
import { entriesConst, fromEntriesConst } from "@shared/common/object";

import ConstrainedPopover from "@/components/common/ConstrainedPopover.vue";
import { NSpace, NTag, type PopoverTrigger } from "naive-ui";

const settings = useSettingsStore();

const {
  mcEntry: mcEntryProp,
  反切 = false,
  trigger,
} = defineProps<{
  mcEntry: MCEntry | number;
  反切?: boolean;
  trigger?: PopoverTrigger;
}>();

const mcEntry = computed<MCEntry>(() =>
  typeof mcEntryProp === "number"
    ? getMCQueryUtils().entryAt(mcEntryProp)!
    : mcEntryProp
);

const strataMap = computed<
  Record<
    Language,
    // { stratum: pronunciation }
    Record<string, string>
  >
>(() =>
  fromEntriesConst(
    LANGUAGES.map((language) => [
      language,
      getReflexMapByMC(mcEntry.value, language),
    ])
  )
);

const allRecordedFGPronunciations = computed<string[]>(() => [
  ...new Set(
    getLangQueryUtils("FG")
      .select(
        (langEntry) =>
          langEntry.記錄讀音 != null && langEntry.MC === mcEntry.value.MC
      )
      .map((langEntry) => langEntry.記錄讀音!)
  ),
]);

const STRATA_LABEL_MAP = {
  白: "白讀",
  文: "文讀",
  新: "新派",
  老: "老派",
  吳: "吳音",
} as const;
</script>

<template>
  <ConstrainedPopover
    :trigger="trigger"
    style="min-width: max-content; padding: 0.8em 1em"
  >
    <template #trigger>
      <span class="char clickable">
        {{ mcEntry.MC.音韻地位(settings.mcInfoStyle) }}
        <template v-if="反切">{{ mcEntry.MC.反切 }}</template>
      </span>
    </template>

    <n-space vertical style="gap: 0.2em">
      <n-space align="center">
        <n-tag size="small" style="margin-right: -0.5em">中古拼音</n-tag>
        <span class="pinyin-mc">
          {{ mcEntry.MC.拼音[settings.mcPinyinFormat] }}
        </span>
      </n-space>

      <template
        v-for="[langEN, langCN] of entriesConst(LANGUAGE_MAP)"
        :key="langEN"
      >
        <n-space
          v-if="
            settings.languages.includes(langEN) &&
            mcEntry.reflex[langEN] != null
          "
          align="center"
        >
          <n-tag size="small" style="margin-right: -0.5em">
            推導{{ langCN }}
          </n-tag>

          <div>
            <DoublePronunciation
              :pronunciation="mcEntry.reflex[langEN]"
              :language="langEN"
            />

            <Tooltip
              v-if="
                strataMap[langEN] && Object.keys(strataMap[langEN]).length > 1
              "
              marker="…"
              :trigger-style="{ marginLeft: '0.3em' }"
            >
              <n-space style="gap: 0" vertical>
                <template
                  v-for="[stratum, pronunciation] of Object.entries(
                    strataMap[langEN]
                  )"
                >
                  <div v-if="stratum !== ''">
                    {{
                      STRATA_LABEL_MAP[stratum as keyof typeof STRATA_LABEL_MAP]
                    }}
                    <DoublePronunciation
                      :pronunciation="pronunciation"
                      :language="langEN"
                      :class="{
                        // disabled
                        gray:
                          false &&
                          langEN === 'FG' &&
                          !allRecordedFGPronunciations.includes(pronunciation),
                      }"
                    />
                  </div>
                </template>
              </n-space>
            </Tooltip>
          </div>
        </n-space>
      </template>
    </n-space>
  </ConstrainedPopover>
</template>

<style scoped></style>
