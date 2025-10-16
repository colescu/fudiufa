<script setup lang="ts">
import { computed } from "vue";
import { useHistoryStore } from "@/stores/history";
import {
  getLangQueryUtils,
  getReflexMapByMC,
  LangEntry,
  Language,
} from "@shared/lang";
import { getReflexes as getFGReflexes } from "@shared/fg/predict";

import ConstrainedPopover from "@/components/common/ConstrainedPopover.vue";
import EntriesList from "./EntriesList.vue";

// IMPROVE for other languages
const {
  initials,
  final,
  indexMap,
  ignoreVoicing = false,
  setStratum = false,
  showCount = false,
  hidePronunciation = false,
  testException,
  highlightStratum = false,
  language = "FG",
} = defineProps<{
  initials: string;
  final: string;
  indexMap: Map<number, number[]>; // precomputed
  ignoreVoicing?: boolean;
  setStratum?: boolean;
  showCount?: boolean;
  hidePronunciation?: boolean;
  testException?: (langEntry: LangEntry) => boolean;
  highlightStratum?: boolean;
  language?: Language;
  baseZIndex?: number;
}>();

const reflexMap = computed<Record<string, string> | undefined>(() => {
  const mcIndices = [...indexMap.keys()];
  if (mcIndices.length === 0) return;
  const baseReflexes = getReflexMapByMC(
    mcIndices[0], // representative MC entry
    language
  );
  if (baseReflexes?.[""] === undefined) return;

  if (language === "FG") {
    const reflexes = getFGReflexes(
      initials[0]!,
      final,
      baseReflexes[""],
      ignoreVoicing,
      true
    );
    return Object.fromEntries(
      ["", "白", "新"].map((stratum, index) => [stratum, reflexes[index]])
    );
  }

  return Object.fromEntries(
    Object.entries(baseReflexes).map(([key, value]) => [
      key,
      value.replace(/\d/g, ""), // only ignore tone
    ])
  );
});

const history = useHistoryStore();
const displayedPronunciation = computed<string | undefined>(
  () =>
    reflexMap.value?.[
      language === "FG" && setStratum
        ? history.phonology.diachronicTable.stratum
        : "" // default stratum
    ]
);

const exceptions = computed<LangEntry[]>(() =>
  (
    [...indexMap.values()]
      .flat()
      .map(getLangQueryUtils(language).entryAt) as LangEntry[]
  ).filter(
    testException ??
      ((entry) => entry.層 !== "官" && entry.記錄讀音 !== entry.推導讀音)
  )
);

const toneExceptions = computed<LangEntry[]>(() =>
  exceptions.value.filter(
    (entry) =>
      !isNaN(Number(entry.讀音.at(-1))) &&
      entry.記錄讀音?.replace(/\d/g, "") === entry.推導讀音?.replace(/\d/g, "")
  )
);
const otherExceptions = computed<LangEntry[]>(() =>
  exceptions.value.filter((entry) => !toneExceptions.value.includes(entry))
);
const showToneExceptions = computed<boolean>(
  () => toneExceptions.value.length > 0 && testException === undefined
);

const characterMap = computed<
  Map<
    number, // MC index
    Record<
      string, // character
      {
        pronunciations: [string, string | null][];
        isException: boolean;
      }
    >
  >
>(() => {
  const { entryAt } = getLangQueryUtils(language);
  return new Map(
    [...indexMap.entries()].map(([mcIndex, langIndices]) => {
      const resultMap = {} as Record<
        string,
        {
          pronunciations: [string, string | null][];
          isException: boolean;
        }
      >;
      for (const langIndex of langIndices) {
        const entry = entryAt(langIndex)!;
        const character = entry.字頭 ?? "□";
        if (!(character in resultMap)) {
          resultMap[character] = {
            isException: false,
            pronunciations: [],
          };
        }
        resultMap[character]!.pronunciations.push([entry.記錄讀音!, entry.層]);
        if (exceptions.value.includes(entry)) {
          resultMap[character]!.isException = true;
        }
      }
      return [mcIndex, resultMap];
    })
  );
});
</script>

<template>
  <td
    :class="{
      // highlight cells different from default reflex
      'table-highlight':
        highlightStratum && displayedPronunciation !== reflexMap?.[''],
    }"
  >
    <span
      v-if="reflexMap"
      :class="{ gray: [...indexMap.values()].flat().length === 0 }"
    >
      <ConstrainedPopover
        :base-z-index="baseZIndex ? baseZIndex + 100 : undefined"
        style="max-width: 16em"
      >
        <template #trigger>
          <span
            class="clickable"
            :class="{
              exception: showToneExceptions
                ? otherExceptions.length > 0
                : exceptions.length > 0,
            }"
          >
            <Pronunciation
              v-if="!showCount"
              :pronunciation="displayedPronunciation!"
              :language="language"
              no-audio
              separate
            />
            <template v-else>
              {{ [...indexMap.values()].flat().length || "" }}
            </template>
          </span>
        </template>

        <template v-if="[...indexMap.values()].flat().length > 0">
          <div class="diachronic-table-popover grid-container">
            <template
              v-for="[mcIndex, characters] of characterMap.entries()"
              :key="mcIndex"
            >
              <template v-if="Object.keys(characters).length > 0">
                <div>
                  <MCInfo :mc-entry="mcIndex" 反切 trigger="click" />
                </div>
                <div style="max-width: 8em">
                  <!-- characters sorted by frequency in fullLangIndexMap -->
                  <template
                    v-for="[character, data] of Object.entries(characters)"
                    :key="character"
                  >
                    <span
                      v-if="hidePronunciation"
                      class="char no-simplify"
                      :class="{ exception: data.isException }"
                    >
                      {{ character }}
                    </span>

                    <ConstrainedPopover
                      v-else
                      trigger="hover"
                      :base-z-index="baseZIndex ? baseZIndex + 200 : undefined"
                    >
                      <template #trigger>
                        <span
                          class="char no-simplify"
                          :class="{ exception: data.isException }"
                        >
                          {{ character }}
                        </span>
                      </template>

                      <span
                        v-for="[pronunciation, stratum] of data.pronunciations"
                        class="pronunciations"
                        style="white-space: nowrap"
                      >
                        <Pronunciation
                          :pronunciation="pronunciation"
                          :language="language"
                        /><sub v-if="stratum">{{ stratum }}</sub
                        >&nbsp;
                      </span>
                    </ConstrainedPopover>
                  </template>
                </div>
              </template>
            </template>
          </div>

          <hr />
          <div class="block pronunciations">
            推導音：<template
              v-for="([stratum, pronunciation], index) of Object.entries(
                reflexMap
              )"
            >
              <template v-if="index === 0 || pronunciation !== reflexMap['']">
                <template v-if="index !== 0">&nbsp;&nbsp;</template
                ><Pronunciation
                  :pronunciation="pronunciation"
                  :language="language"
                /><sub v-if="stratum !== ''">{{ stratum }}</sub>
              </template>
            </template>
          </div>

          <template v-if="exceptions.length > 0">
            <hr />
            <template v-if="showToneExceptions">
              <div class="block">
                聲調例外：<EntriesList
                  :entries="toneExceptions"
                  :language="language"
                />
              </div>
              <div
                v-if="otherExceptions.length > 0"
                class="block"
                style="margin-top: 0.3em"
              >
                其他例外：<EntriesList
                  :entries="otherExceptions"
                  :language="language"
                />
              </div>
            </template>

            <div v-else class="block">
              例外：<EntriesList :entries="exceptions" :language="language" />
            </div>
          </template>
        </template>

        <template v-else> 無收錄字 </template>
      </ConstrainedPopover>
    </span>
  </td>
</template>

<style scoped>
.gray * {
  color: var(--gray-text) !important;
}

.grid-container {
  display: grid;
  grid-template-columns: max-content max-content;
  column-gap: 1em;
}

.block {
  max-width: 16em;
}

.pronunciations sub {
  margin-left: 0.1em;
}

.exception {
  text-decoration: underline wavy;
  text-underline-offset: 0.1em;
  text-decoration-thickness: 0.1em;
  text-decoration-skip-ink: none;
}
</style>
