<script setup lang="ts">
import { computed } from "vue";
import { useHistoryStore } from "@/stores/history";
import { getMCQueryUtils } from "@shared/mc";
import { getPredictedPronunciations } from "@shared/fg/predict";
import { getLangQueryUtils, LangEntry, Language } from "@shared/lang";

import ConstrainedPopover from "@/components/common/ConstrainedPopover.vue";
import EntriesList from "./EntriesList.vue";

// only implemented properly for FG
const {
  initials,
  final,
  indexMap,
  ignoreVoicing = false,
  setStratum = false,
  showCount = false,
  hidePronunciation = false,
  testException,
  highlightExceptions = false,
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
  highlightExceptions?: boolean;
  language?: Language;
  baseZIndex?: number;
}>();

// Ad hoc representative reflex
const basePronunciation = computed<string | undefined>(() => {
  const mcIndices = [...indexMap.keys()];
  if (mcIndices.length === 0) return;
  let pronunciation = getMCQueryUtils().entryAt(mcIndices[0])?.reflex[language];
  if (pronunciation == null) return;
  return pronunciation;
});

const pronunciations = computed<string[] | undefined>(() =>
  basePronunciation.value
    ? language === "FG"
      ? getPredictedPronunciations(
          initials[0]!,
          final,
          basePronunciation.value,
          ignoreVoicing,
          true
        )
      : [basePronunciation.value.replace(/\d/g, "")]
    : undefined
);

const history = useHistoryStore();
const displayedPronunciation = computed<string | undefined>(
  () =>
    pronunciations.value?.[
      language === "FG" && setStratum
        ? ["", "白", "新"].indexOf(history.phonology.diachronicTable.stratum)
        : 0
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
      entry.記錄讀音?.slice(0, -1) === entry.推導讀音?.slice(0, -1)
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
      'table-highlight':
        highlightExceptions && displayedPronunciation !== pronunciations?.[0],
    }"
  >
    <span
      v-if="pronunciations"
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
            推導音：<Pronunciation
              :pronunciation="pronunciations[0]"
              :language="language"
            />
            <template
              v-if="
                pronunciations[1] && pronunciations[1] !== pronunciations[0]
              "
            >
              &nbsp;<Pronunciation
                :pronunciation="pronunciations[1]"
                :language="language"
              /><sub>白</sub>
            </template>
            <template
              v-if="
                pronunciations[2] && pronunciations[2] !== pronunciations[0]
              "
            >
              &nbsp;<Pronunciation
                :pronunciation="pronunciations[2]"
                :language="language"
              /><sub>新</sub>
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
