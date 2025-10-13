<script setup lang="ts">
import { computed } from "vue";
import { useSettingsStore } from "@/stores/settings";
import { getMCQueryUtils, MCEntry, strataCache } from "@shared/mc";
import { getLangQueryUtils, Language, LANGUAGE_MAP } from "@shared/lang";
import { entriesConst } from "@shared/common/object";

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

const otherStrata = computed<
  Partial<
    Record<
      Language,
      // { stratum: pronunciation }
      Record<string, string>
    >
  >
>(() => {
  const STRATA = strataCache.get();
  const mcIndex = getMCQueryUtils().indexOf(mcEntry.value)!;
  return Object.fromEntries(
    ["FG", "SW"].map((language) => [
      language,
      ((STRATA[language][mcIndex] as [string, string][]) ?? []).reduce(
        (acc, [stratum, pronunciation]) => {
          if ("白文".includes(stratum)) {
            stratum += "讀";
          }
          if ("新老".includes(stratum)) {
            stratum += "派";
          }
          acc[stratum] = pronunciation;
          return acc;
        },
        {} as Record<string, string>
      ),
    ])
  );
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
                otherStrata[langEN] &&
                Object.keys(otherStrata[langEN]).length > 0
              "
              marker="…"
              :trigger-style="{ marginLeft: '0.3em' }"
            >
              <n-space style="gap: 0" vertical>
                <div
                  v-for="[stratum, pronunciation] of Object.entries(
                    otherStrata[langEN]
                  )"
                >
                  {{ stratum }}
                  <DoublePronunciation
                    :pronunciation="pronunciation"
                    :language="langEN"
                    :class="{
                      gray:
                        langEN === 'FG' &&
                        !allRecordedFGPronunciations.includes(pronunciation),
                    }"
                  />
                </div>
              </n-space>
            </Tooltip>
          </div>
        </n-space>
      </template>
    </n-space>
  </ConstrainedPopover>
</template>

<style scoped></style>
