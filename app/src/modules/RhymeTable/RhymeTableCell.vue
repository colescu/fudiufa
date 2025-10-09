<script setup lang="ts">
import { computed } from "vue";
import { useInjectDiachronicTableState } from "../DiachronicTable/useDiachronicTableState";
import { getLangQueryUtils, LangEntry, Language } from "@shared/lang";
import { syllableDataCache } from "@shared/syllable";
import { characterComparer } from "@shared/cjk";
import { precomposeComparer } from "@shared/common/sort";

import ConstrainedPopover from "@/components/common/ConstrainedPopover.vue";
import { NSpace, NButton } from "naive-ui";

const {
  pronunciation,
  char,
  langIndices,
  showCount = false,
  language = "FG",
} = defineProps<{
  pronunciation: string; // in ipaRaw (may be illegal!)
  char: string | null;
  langIndices: number[];
  showCount?: boolean;
  language?: Language;
  baseZIndex?: number;
}>();
const character = char ?? "□";

const entries = computed<LangEntry[]>(() => {
  const { entryAt } = getLangQueryUtils(language);
  return langIndices.map(entryAt).filter((entry) => entry != undefined);
});

// LATERFIX no tone for JP, KR
const TonesMap = syllableDataCache.get("tones")[language];
type Tone = keyof typeof TonesMap & string;
const entriesByToneMap = computed<Partial<Record<Tone, LangEntry[]>>>(() => {
  const result: Record<Tone, LangEntry[]> = Object.fromEntries(
    Object.keys(TonesMap).map((tone) => [tone, []])
  );
  entries.value.forEach((entry) => {
    const tone = entry.讀音.at(-1) as Tone;
    result[tone]!.push(entry);
  });
  Object.entries(result).forEach(([tone, entries]) => {
    if (entries.length === 0) {
      delete result[tone];
    } else {
      entries.sort(
        precomposeComparer(characterComparer, (entry) => entry.字頭)
      );
    }
  });
  return result;
});

const mcIndices = computed<number[]>(() => [
  ...new Set(
    entries.value
      .map((entry) => entry.小韻號)
      .filter((mcIndex) => mcIndex != null)
  ),
]);
const showDiachronicTable = computed<boolean>(() => mcIndices.value.length > 0);

const { updateDiachronicTable } = useInjectDiachronicTableState(
  mcIndices,
  computed(() => langIndices)
);
</script>

<template>
  <td>
    <ConstrainedPopover
      v-if="char && Object.keys(entriesByToneMap).length > 0"
      class-name="rhyme-table"
      :base-z-index="baseZIndex"
      :whitelist="['.rhyme-table-settings']"
    >
      <template #trigger>
        <span class="clickable">
          <!-- Ad hoc parse "字|層" -->
          <span
            v-if="!showCount"
            class="char"
            :class="{ [[...character].at(-1)!]: character.includes('|') }"
          >
            {{ character.split("|")[0] }}
          </span>

          <template v-else>
            {{ langIndices.length }}
          </template>
        </span>
      </template>

      <div class="grid-container">
        <template
          v-for="[tone, entries] of Object.entries(entriesByToneMap)"
          :key="tone"
        >
          <div>
            {{ TonesMap[tone].name }}
            <DoublePronunciation
              :pronunciation="pronunciation + tone"
              source-format="ipaRaw"
              language="FG"
            />
          </div>

          <div
            :style="showDiachronicTable ? { width: '7.2em' } : {}"
            :class="{ 輕: tone === '0' }"
          >
            <template
              v-for="entry of entries"
              :key="entry.字頭 || '□' + entry.記錄讀音"
            >
              <span style="white-space: nowrap">
                <span :class="entry.層?.[0]" class="no-simplify">
                  <!-- characters sorted by frequency -->
                  <Character
                    :character="entry.字頭 || '□'"
                    :hint="entry.小韻號 ?? 'N/A'"
                    class-name="rhyme-table-char"
                    :blacklist="[
                      '.rhyme-table__popover',
                      '.rhyme-table-char__popover-target',
                    ]"
                    :base-z-index="baseZIndex ? baseZIndex + 100 : undefined"
                  />
                </span>
                <sub v-if="entry.層">
                  {{
                    "老新官".includes(entry.層[0]!)
                      ? entry.層.slice(1)
                      : entry.層
                  }}
                </sub>
              </span>
            </template>
          </div>
        </template>
      </div>

      <n-space
        v-if="showDiachronicTable"
        align="center"
        justify="end"
        style="margin-top: 0.5em"
      >
        <span>
          （<n-button @click="updateDiachronicTable" text> 查看古今圖 </n-button
          >）
        </span>
      </n-space>

      <!-- FIXME UI clicking when isFullscreen always closes popover (only on desktop) -->
    </ConstrainedPopover>
  </td>
</template>

<style scoped>
.grid-container {
  display: grid;
  grid-template-columns: max-content max-content;
  column-gap: 1em;
}
</style>
