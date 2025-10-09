<script setup lang="ts">
import { computed } from "vue";
import { useSettingsStore } from "@/stores/settings";
import { getMCQueryUtils, MCEntry } from "@shared/mc";
import { getPredictedPronunciationsByEntry } from "@shared/fg/predict";
import { entriesConst } from "@shared/common/object";
import { getLangQueryUtils, Language, LANGUAGE_MAP } from "@shared/lang";

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

const otherPredictedPronunciations = computed<Record<string, string>>(() => {
  const [默認, 白讀, 新派] = getPredictedPronunciationsByEntry(mcEntry.value);
  return {
    ...(白讀 !== 默認 && { 白讀 }),
    ...(新派 !== 默認 && { 新派 }),
  };
});

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
      <template
        v-for="[langEN, langCN] of entriesConst(LANGUAGE_MAP)"
        :key="langEN"
      >
        <n-space v-if="settings.languages.includes(langEN)" align="center">
          <n-tag size="small" style="margin-right: -0.5em">
            推導{{ langCN }}
          </n-tag>
          <div>
            <DoublePronunciation
              :pronunciation="mcEntry.reflex[langEN]!"
              :language="langEN"
            />
            <Tooltip
              v-if="
                langEN === 'FG' &&
                Object.keys(otherPredictedPronunciations).length > 0
              "
              marker="…"
              :trigger-style="{ marginLeft: '0.3em' }"
            >
              <n-space vertical style="gap: 0">
                <div
                  v-for="[stratum, pronunciation] of Object.entries(
                    otherPredictedPronunciations
                  )"
                >
                  {{ stratum }}
                  <DoublePronunciation
                    :pronunciation="pronunciation"
                    language="FG"
                    :class="{
                      gray: !allRecordedFGPronunciations.includes(
                        pronunciation
                      ),
                    }"
                  />
                </div>
              </n-space>
            </Tooltip>
            <!-- MAYBE 顯示例外
             But it could be misleading
             -->
          </div>
        </n-space>
      </template>
    </n-space>
  </ConstrainedPopover>
</template>

<style scoped></style>
