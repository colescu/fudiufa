import { simplifier } from "@shared/cjk";
import { commonCharactersCache } from "@shared/cjk/cache";
import { fetchFile } from "@shared/cache";
import type { Language } from "@shared/lang";
import {
  getMCQueryUtils,
  mcCache,
  type MCEntry,
  type MCInfo,
} from "@shared/mc";
import { FULL_FINALS } from "@shared/mc/constants";
import {
  normalizeFinal,
  normalizeInitial,
  normalizePinyin,
  normalizeShe,
  normalizeTone,
  shortFinal,
  type FieldInput,
  type FieldKey,
} from "./aliases";

export type AnswerMode = "pinyin" | "fields";
export type MCQuizCard = { char: string; entries: MCEntry[] };
export type GradeResult = {
  correct: boolean;
  fields?: Record<FieldKey, boolean>;
  entryKeys?: string[];
};

export const HINT_LANGUAGES = [
  "PM",
  "GC",
  "SW",
  "JP",
  "KR",
  "VN",
] as const satisfies readonly Language[];
export type HintLanguage = (typeof HINT_LANGUAGES)[number];
export const HINT_LABELS: Record<HintLanguage, string> = {
  PM: "北京",
  GC: "廣州",
  SW: "上海",
  JP: "日本",
  KR: "朝鮮",
  VN: "越南",
};

type RawLangEntry = {
  字頭: string | null;
  小韻號: number | null;
  記錄讀音: string | null;
};
type RawHintMap = {
  byIndex: Map<number, string[]>;
  byChar: Map<string, string[]>;
};
const dictionaryHints = new Map<Language, RawHintMap>();
const entryIndexes = new WeakMap<MCEntry, number>();
const hanziIndex = new Map<string, number[]>();

export async function loadQuizCards(limit = 1200): Promise<MCQuizCard[]> {
  await Promise.all([
    mcCache.load(),
    commonCharactersCache.load(),
    loadHanziIndex(),
    loadDictionaryHints(),
  ]);

  const common = new Map(
    Array.from(commonCharactersCache.get()).map((char, index) => [char, index]),
  );
  const grouped = new Map<string, { rank: number; entries: MCEntry[] }>();

  for (const [char, indexes] of hanziIndex) {
    if (Array.from(char).length !== 1) continue;

    const rank = common.get(simplifier(char)) ?? common.get(char);
    if (rank === undefined) continue;

    const entries = indexes
      .map((index) => [index, getMCQueryUtils().entryAt(index)] as const)
      .filter((item): item is readonly [number, MCEntry] => !!item[1])
      .map(([index, entry]) => {
        entryIndexes.set(entry, index);
        return entry;
      });
    if (entries.length) grouped.set(char, { rank, entries });
  }

  return [...grouped.entries()]
    .sort((a, b) => a[1].rank - b[1].rank)
    .slice(0, limit)
    .map(([char, value]) => ({ char, entries: value.entries }));
}

export function randomCard(cards: MCQuizCard[], previous?: MCQuizCard | null) {
  let card = cards[Math.floor(Math.random() * cards.length)]!;
  for (
    let i = 0;
    previous && cards.length > 1 && card.char === previous.char && i < 5;
    i++
  ) {
    card = cards[Math.floor(Math.random() * cards.length)]!;
  }
  return card;
}

export function cardForChar(char: string): MCQuizCard | undefined {
  const chars = Array.from(char.trim());
  if (chars.length !== 1) return;
  const zi = chars[0]!;

  const indexes = hanziIndex.get(zi) ?? [];

  const entries = indexes
    .map((index) => [index, getMCQueryUtils().entryAt(index)] as const)
    .filter((item): item is readonly [number, MCEntry] => !!item[1])
    .map(([index, entry]) => {
      entryIndexes.set(entry, index);
      return entry;
    });

  return entries.length ? { char: zi, entries } : undefined;
}

export function getFinalCandidates(she: string) {
  const normalizedShe = normalizeShe(she);
  return unique(
    FULL_FINALS.filter(
      (item) =>
        !normalizedShe || normalizeShe(Array.from(item)[0]!) === normalizedShe,
    ).map(shortFinal),
  );
}

export function gradePinyin(
  input: string,
  card: MCQuizCard,
  excluded: Iterable<string> = [],
): GradeResult {
  const answer = normalizePinyin(input);
  const excludedKeys = new Set(excluded);
  const matched = card.entries.find(
    (entry) =>
      !excludedKeys.has(entryKey(entry)) &&
      !!answer &&
      Object.values(entry.MC.拼音).some(
        (value) => normalizePinyin(value) === answer,
      ),
  );

  return {
    correct: !!matched,
    entryKeys: matched ? [entryKey(matched)] : [],
  };
}

export function gradeFields(
  input: FieldInput,
  card: MCQuizCard,
  excluded: Iterable<string> = [],
  lenientFinal = false,
): GradeResult {
  const excludedKeys = new Set(excluded);
  const entries = card.entries.filter(
    (entry) => !excludedKeys.has(entryKey(entry)),
  );
  const candidates = (entries.length ? entries : card.entries).map((entry) => {
    const mc = entry.MC;
    const fields: Record<FieldKey, boolean> = {
      initial: matchInitial(input.initial, mc.聲母),
      she: matchShe(input.she, mc.攝),
      final: matchFinal(input.final, mc.攝, mc, lenientFinal),
      tone: matchTone(input.tone, mc.聲調),
    };
    return {
      entry,
      fields,
      score: Object.values(fields).filter(Boolean).length,
    };
  });
  const best = candidates.sort((a, b) => b.score - a.score)[0]!;
  const matched = lenientFinal
    ? candidates.filter((candidate) => candidate.score === 4)
    : best.score === 4
      ? [best]
      : [];

  return {
    fields: best.fields,
    correct: matched.length > 0,
    entryKeys: matched.map((item) => entryKey(item.entry)),
  };
}

export function getHint(card: MCQuizCard, language: HintLanguage) {
  const raw = dictionaryHints.get(language);
  const byIndex =
    raw &&
    card.entries.flatMap(
      (entry) => raw.byIndex.get(indexOfEntry(entry) ?? -1) ?? [],
    );
  const byChar = raw?.byChar.get(card.char) ?? [];
  return unique([...(byIndex ?? []), ...byChar]).join(", ") || "—";
}

export function describeAnswers(card: MCQuizCard) {
  return unique(card.entries.map(describeEntry));
}

export function describeEntry(entry: MCEntry) {
  const mc = entry.MC;
  return `${mc.音韻地位()} · ${mc.反切 ?? "缺少反切"}`;
}

export function entryKey(entry: MCEntry) {
  return String(indexOfEntry(entry) ?? describeEntry(entry));
}

function finalLabels(mc: MCInfo) {
  return [`${mc.攝}${mc.韻系}${mc.等}${mc.呼}`];
}

function matchInitial(input: string, expected: string) {
  return (
    !!input.trim() && normalizeInitial(input) === normalizeInitial(expected)
  );
}

function matchShe(input: string, expected: string) {
  return !!input.trim() && normalizeShe(input) === normalizeShe(expected);
}

function matchTone(input: string, expected: string) {
  return !!input.trim() && normalizeTone(input) === normalizeTone(expected);
}

function matchFinal(input: string, she: string, mc: MCInfo, lenient = false) {
  const answer = normalizeFinal(input, she);
  return (
    !!input.trim() &&
    finalLabels(mc).some((value) => {
      const expected = normalizeFinal(value);
      return (
        expected === answer ||
        (lenient && sameFinalExceptFirst(answer, expected))
      );
    })
  );
}

function sameFinalExceptFirst(answer: string, expected: string) {
  const answerChars = Array.from(answer);
  const expectedChars = Array.from(expected);
  return (
    answerChars.length === expectedChars.length &&
    answerChars[0] === expectedChars[0] &&
    answerChars.slice(2).join("") === expectedChars.slice(2).join("") &&
    answerChars[1] !== expectedChars[1]
  );
}

function unique<T>(items: T[]) {
  return [...new Set(items)];
}

function indexOfEntry(entry: MCEntry) {
  return entryIndexes.get(entry) ?? getMCQueryUtils().indexOf(entry);
}

async function loadHanziIndex() {
  if (hanziIndex.size) return;
  const response = await fetch(
    `${import.meta.env.BASE_URL}data/hanzi-index.json`,
  );
  if (!response.ok) {
    throw new Error(
      `HTTP error ${response.status} when fetching hanzi-index.json`,
    );
  }
  const data = (await response.json()) as Record<string, number[]>;
  for (const [char, indexes] of Object.entries(data)) {
    hanziIndex.set(char, unique(indexes));
  }
}

async function loadDictionaryHints() {
  await Promise.all(
    HINT_LANGUAGES.map(async (language) => {
      if (dictionaryHints.has(language)) return;
      try {
        const rows = (await fetchFile(language, "json")) as RawLangEntry[];
        const map: RawHintMap = {
          byIndex: new Map(),
          byChar: new Map(),
        };

        for (const row of rows) {
          if (!row.記錄讀音) continue;
          if (row.小韻號 != null)
            addHint(map.byIndex, row.小韻號, row.記錄讀音);
          if (row.字頭) addHint(map.byChar, row.字頭, row.記錄讀音);
        }

        dictionaryHints.set(language, map);
      } catch (error) {
        console.warn(`No raw hint data for ${language}`, error);
        dictionaryHints.set(language, {
          byIndex: new Map(),
          byChar: new Map(),
        });
      }
    }),
  );
}

function addHint<K, V>(map: Map<K, V[]>, key: K, value: V) {
  map.set(key, unique([...(map.get(key) ?? []), value]));
}
