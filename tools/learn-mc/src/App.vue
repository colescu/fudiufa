<script setup lang="ts">
import { CheckmarkCircle, CloseCircle } from "@vicons/ionicons5";
import { computed, onMounted, onUnmounted, reactive, ref, watch } from "vue";
import {
  optionFilters,
  normalizeText,
  options,
  placeholders,
  type FieldInput,
  type FieldKey,
} from "./aliases";
import ComboInput from "./ComboInput.vue";
import {
  HINT_LANGUAGES,
  HINT_LABELS,
  cardForChar,
  describeAnswers,
  describeEntry,
  entryKey,
  getFinalCandidates,
  getHint,
  gradeFields,
  gradePinyin,
  loadQuizCards,
  randomCard,
  type AnswerMode,
  type GradeResult,
  type HintLanguage,
  type MCQuizCard,
} from "./quiz";

const modeStorageKey = "learn-mc.answer-mode";
const cards = ref<MCQuizCard[]>([]);
const card = ref<MCQuizCard | null>(null);
const loading = ref(true);
const loadError = ref("");
const mode = ref<AnswerMode>(savedMode());
const lenientFinal = ref(false);
const pinyin = ref("");
const fields = reactive<FieldInput>({
  initial: "",
  she: "",
  final: "",
  tone: "",
});
const result = ref<GradeResult | null>(null);
const revealed = ref(false);
const shownHints = reactive(new Set<string>());
const solvedEntries = reactive(new Set<string>());
const wrongCounted = ref(false);
const continuePrompt = ref(false);
const validationPrompt = ref("");
const stats = reactive({ seen: 0, correct: 0, streak: 0 });

const finalCandidates = computed(() => getFinalCandidates(fields.she));
const answers = computed(() => (card.value ? describeAnswers(card.value) : []));
const solvedAnswers = computed(() =>
  card.value
    ? card.value.entries
        .filter((entry) => solvedEntries.has(entryKey(entry)))
        .map(describeEntry)
    : [],
);
const hasMoreReadings = computed(
  () =>
    !!card.value &&
    card.value.entries.some((entry) => !solvedEntries.has(entryKey(entry))),
);
const solvedCountText = computed(() => numberText(solvedEntries.size));
const remainingCountText = computed(() =>
  numberText(
    card.value
      ? card.value.entries.filter(
          (entry) => !solvedEntries.has(entryKey(entry)),
        ).length
      : 0,
  ),
);

onMounted(async () => {
  try {
    cards.value = await loadQuizCards();
    syncCardFromQuery();
  } catch (error) {
    loadError.value =
      error instanceof Error ? error.message : "Unknown loading error";
    console.error(error);
  } finally {
    loading.value = false;
  }
  window.addEventListener("popstate", syncCardFromQuery);
});

onUnmounted(() => window.removeEventListener("popstate", syncCardFromQuery));

watch(mode, (value) => {
  saveMode(value);
  resetResponse();
});
watch(
  () => fields.she,
  () => {
    if (fields.final && !getFinalCandidates(fields.she).includes(fields.final))
      fields.final = "";
  },
);

function submit() {
  if (!card.value || (result.value?.correct && !hasMoreReadings.value)) return;
  continuePrompt.value = false;
  validationPrompt.value = "";
  if (mode.value === "fields") {
    if (!fieldsAreValid()) {
      result.value = null;
      validationPrompt.value = "輸入格式不正確！";
      return;
    }
  }
  const nextResult =
    mode.value === "pinyin"
      ? gradePinyin(pinyin.value, card.value, solvedEntries)
      : gradeFields(fields, card.value, solvedEntries, lenientFinal.value);
  result.value = nextResult;

  if (nextResult.correct && nextResult.entryKeys?.length) {
    nextResult.entryKeys.forEach((key) => solvedEntries.add(key));
    if (!wrongCounted.value) {
      stats.seen++;
      stats.correct++;
      stats.streak++;
    }
    if (hasMoreReadings.value) {
      revealed.value = false;
      continuePrompt.value = true;
    }
    return;
  }

  if (!wrongCounted.value) {
    wrongCounted.value = true;
    stats.seen++;
    stats.streak = 0;
  }
}

function next() {
  selectCard(randomCard(cards.value, card.value), "push");
}

function resetResponse() {
  clearInputs();
  result.value = null;
  revealed.value = false;
  continuePrompt.value = false;
  validationPrompt.value = "";
}

function clearInputs() {
  pinyin.value = "";
  Object.assign(fields, { initial: "", she: "", final: "", tone: "" });
}

function statusClass(key: FieldKey) {
  if (!result.value?.fields) return "";
  return result.value.fields[key] ? "ok" : "bad";
}

function pinyinStatusClass() {
  if (!result.value || result.value.fields) return "";
  return result.value.correct ? "ok" : "bad";
}

function fieldCorrect(key: FieldKey) {
  return result.value?.fields?.[key];
}

function fieldsAreValid() {
  const entries: [FieldKey, readonly string[]][] = [
    ["initial", options.initial],
    ["she", options.she],
    ["final", finalCandidates.value],
    ["tone", options.tone],
  ];
  return entries.every(([key, allowed]) => matchesAllowed(fields[key], allowed));
}

function matchesAllowed(value: string, allowed: readonly string[]) {
  const normalized = normalizeText(value);
  return (
    !!normalized &&
    allowed.some((option) => normalizeText(option) === normalized)
  );
}

function toggleHint(language: HintLanguage) {
  shownHints.add(language);
}

function hintText(language: HintLanguage) {
  return card.value ? getHint(card.value, language) : "";
}

type UrlUpdate = "replace" | "push" | false;

function selectCard(nextCard: MCQuizCard, updateUrl: UrlUpdate = "replace") {
  card.value = nextCard;
  resetResponse();
  shownHints.clear();
  solvedEntries.clear();
  wrongCounted.value = false;
  if (updateUrl) writeZiParam(nextCard.char, updateUrl);
}

function cardFromQuery() {
  const zi = new URLSearchParams(window.location.search).get("zi");
  return zi ? cardForChar(zi) : undefined;
}

function syncCardFromQuery() {
  const nextCard = cardFromQuery();
  if (nextCard) {
    if (nextCard.char !== card.value?.char) selectCard(nextCard, false);
    return;
  }

  selectCard(randomCard(cards.value, card.value), "replace");
}

function writeZiParam(zi: string, mode: Exclude<UrlUpdate, false>) {
  const url = new URL(window.location.href);
  if (url.searchParams.get("zi") === zi) return;
  url.searchParams.set("zi", zi);
  const nextUrl = `${url.pathname}?${url.searchParams}${url.hash}`;
  if (mode === "push") window.history.pushState(null, "", nextUrl);
  else window.history.replaceState(null, "", nextUrl);
}

function savedMode(): AnswerMode {
  try {
    const value = localStorage.getItem(modeStorageKey);
    return value === "fields" || value === "pinyin" ? value : "pinyin";
  } catch {
    return "pinyin";
  }
}

function saveMode(value: AnswerMode) {
  try {
    localStorage.setItem(modeStorageKey, value);
  } catch {
    // Storage can be unavailable in private or restricted browser contexts.
  }
}

function numberText(value: number) {
  return "零一二三四五六七八九十"[value] ?? String(value);
}
</script>

<template>
  <main class="shell">
    <section class="card">
      <header>
        <h1>反推中古音</h1>
        <span
          >得分 {{ stats.correct }}/{{ stats.seen }} · 連勝
          {{ stats.streak }}</span
        >
      </header>

      <p v-if="loading" class="loading">數據加載中…</p>
      <p v-else-if="loadError" class="loading">數據加載失敗：{{ loadError }}</p>
      <template v-else-if="card">
        <div class="char">{{ card.char }}</div>

        <div class="hints">
          <div
            v-for="language in HINT_LANGUAGES"
            :key="language"
            :class="['hint', { shown: shownHints.has(language) }]"
            role="button"
            tabindex="0"
            @click="toggleHint(language)"
            @keydown.enter.prevent="toggleHint(language)"
            @keydown.space.prevent="toggleHint(language)"
          >
            <span class="hint-label">{{ HINT_LABELS[language] }}</span>
            <strong class="hint-value">
              <span :class="{ masked: !shownHints.has(language) }">{{
                hintText(language)
              }}</span>
            </strong>
          </div>
        </div>

        <div class="tabs" aria-label="Answer mode">
          <button
            :class="{ active: mode === 'fields' }"
            @click="mode = 'fields'"
          >
            音韻地位
          </button>
          <button
            :class="{ active: mode === 'pinyin' }"
            @click="mode = 'pinyin'"
          >
            中古拼音
          </button>
        </div>

        <form @submit.prevent="submit">
          <label v-if="mode === 'pinyin'" class="pinyin-field">
            <span class="pinyin-control">
              <input
                v-model="pinyin"
                :class="pinyinStatusClass()"
                :disabled="result?.correct && !hasMoreReadings"
                :placeholder="'輸入切韻拼音或白一平轉寫'"
                autocomplete="off"
                autofocus
              />
              <component
                :is="result.correct ? CheckmarkCircle : CloseCircle"
                v-if="result && !result.fields"
                :class="['field-mark', pinyinStatusClass()]"
                aria-hidden="true"
              />
            </span>
          </label>

          <template v-else>
            <div class="fields">
              <label>
                <span class="label-title">
                  聲母
                  <component
                    :is="
                      fieldCorrect('initial') ? CheckmarkCircle : CloseCircle
                    "
                    v-if="fieldCorrect('initial') !== undefined"
                    :class="['field-mark', statusClass('initial')]"
                    aria-hidden="true"
                  />
                </span>
                <ComboInput
                  v-model="fields.initial"
                  :state="statusClass('initial')"
                  :options="options.initial"
                  :placeholder="placeholders.initial"
                  :filter="optionFilters.initial"
                />
              </label>
              <label>
                <span class="label-title">
                  攝
                  <component
                    :is="fieldCorrect('she') ? CheckmarkCircle : CloseCircle"
                    v-if="fieldCorrect('she') !== undefined"
                    :class="['field-mark', statusClass('she')]"
                    aria-hidden="true"
                  />
                </span>
                <ComboInput
                  v-model="fields.she"
                  :state="statusClass('she')"
                  :options="options.she"
                  :placeholder="placeholders.she"
                  :filter="optionFilters.she"
                />
              </label>
              <label>
                <span class="label-title">
                  韻母
                  <component
                    :is="fieldCorrect('final') ? CheckmarkCircle : CloseCircle"
                    v-if="fieldCorrect('final') !== undefined"
                    :class="['field-mark', statusClass('final')]"
                    aria-hidden="true"
                  />
                </span>
                <ComboInput
                  v-model="fields.final"
                  :state="statusClass('final')"
                  :options="finalCandidates"
                  :placeholder="placeholders.final"
                  :filter="optionFilters.final"
                />
              </label>
              <label>
                <span class="label-title">
                  聲調
                  <component
                    :is="fieldCorrect('tone') ? CheckmarkCircle : CloseCircle"
                    v-if="fieldCorrect('tone') !== undefined"
                    :class="['field-mark', statusClass('tone')]"
                    aria-hidden="true"
                  />
                </span>
                <ComboInput
                  v-model="fields.tone"
                  :state="statusClass('tone')"
                  :options="options.tone"
                  :placeholder="placeholders.tone"
                  :filter="optionFilters.tone"
                />
              </label>
            </div>
            <label class="leniency">
              <input v-model="lenientFinal" type="checkbox" />
              不分重韻
            </label>
          </template>

          <div class="actions">
            <button
              type="submit"
              :disabled="result?.correct && !hasMoreReadings"
            >
              {{ result && !result.correct ? "重試" : "提交" }}
            </button>
            <button type="button" @click="revealed = true">查看答案</button>
            <button type="button" @click="next">換個字</button>
          </div>
        </form>

        <p
          v-if="result || continuePrompt || validationPrompt"
          :class="[
            'feedback',
            (result && !result.correct) || validationPrompt ? 'wrong' : 'right',
          ]"
        >
          {{
            validationPrompt
              ? validationPrompt
              : continuePrompt
              ? `答對${solvedCountText}音。還有${remainingCountText}個讀音，請繼續。`
              : result?.correct
              ? "全部讀音已答對"
              : "標紅的項目不正確！"
          }}
        </p>

        <ul v-if="revealed || solvedAnswers.length" class="answers">
          <li
            v-for="answer in revealed ? answers : solvedAnswers"
            :key="answer"
          >
            {{ answer }}
          </li>
        </ul>
      </template>
    </section>
  </main>
</template>
