import { createCache } from "@shared/cache";
import { syllableDataCache } from "@shared/syllable/cache";
import { Language } from "@shared/lang";

// Ad hoc
export function normalizePinyin(
  pinyin: string,
  language: Language
): [string, string] {
  if (!["FG", "PM"].includes(language) || !isNaN(Number(pinyin.slice(-1)))) {
    return [pinyin.slice(0, -1).normalize("NFC"), pinyin.slice(-1)];
  }

  const TONE_DATA: Record<string, { diacritic: string }> =
    syllableDataCache.get("tones")[language];
  const DIACRITIC_MAP = Object.fromEntries(
    Object.entries(TONE_DATA).map(([tone, data]) => [data["diacritic"], tone])
  );

  let text = pinyin.normalize("NFD");
  let tone = "";
  for (let i = 0; i < text.length; i++) {
    if (text[i]! in DIACRITIC_MAP) {
      tone = DIACRITIC_MAP[text[i]!]!;
      text = text.slice(0, i) + text.slice(i + 1);
      break;
    }
  }

  if (language === "FG") {
    if (text !== "" && !"th".includes(text.at(-1)!)) {
      if (tone === "8") tone = "3";
      if (tone === "7") tone = "16";
    }
  }

  return [text.normalize("NFC"), tone];
}

const pmDictionaryCache = createCache(
  async () => {
    const response = await fetch(
      (import.meta.env.VITE_EXTERNAL_URL ??
        "https://raw.githubusercontent.com/mozillazg/pinyin-data/refs/heads/master") +
        "/kXHC1983.txt"
    );
    const text = await response.text();
    return text;
  },
  (text: string) => {
    const dictionary = {} as Record<string, string[]>;
    const rows = text.split("\n");
    for (const row of rows) {
      const [_, pinyins, character] = row.split(/[:#]/).map((s) => s.trim());
      if (!character || !pinyins) continue;
      const pronunciations = pinyins.split(",");
      dictionary[character] = pronunciations;
    }
    return dictionary;
  }
);

export async function fetchCharsByPM(pinyin: string): Promise<string[]> {
  const [syllable, tone] = normalizePinyin(pinyin, "PM");

  const chars: string[] = [];

  const DICTIONARY = await pmDictionaryCache.getAsync();
  Object.entries(DICTIONARY).forEach(([character, pronunciations]) => {
    for (const pronunciation of pronunciations) {
      const [currentSyllable, currentTone] = normalizePinyin(
        pronunciation,
        "PM"
      );
      if (
        currentSyllable === syllable &&
        (tone === "" || currentTone === tone)
      ) {
        chars.push(character);
        break;
      }
    }
  });

  return chars;
}

const gcDictionaryCache = createCache(
  async () => {
    const response = await fetch(
      (import.meta.env.VITE_EXTERNAL_URL ??
        "https://raw.githubusercontent.com/jyutnet/cantonese-books-data/refs/heads/master/2004_廣州話正音字典") +
        "/B01_資料.json"
    );
    const json = await response.json();
    return json;
  },
  (json: any) => {
    const entries = [] as [string[], string[]][];
    for (const entry of json) {
      const pronunciations = [] as string[];
      for (const item of entry["義項"]) {
        for (const pronunciation of item["讀音"]) {
          pronunciations.push(pronunciation["粵拼讀音"]);
        }
      }
      entries.push([
        entry["字頭"],
        pronunciations.filter((pronunciation) => pronunciation != null),
      ]);
    }
    return entries;
  }
);

export async function fetchCharsByGC(pinyin: string): Promise<string[]> {
  let tone = "";
  if (!isNaN(Number(pinyin.slice(-1)))) {
    tone = pinyin.slice(-1);
    pinyin = pinyin.slice(0, -1);
  }

  const chars: string[] = [];
  const ENTRIES = await gcDictionaryCache.getAsync();
  for (const [characters, pronunciations] of ENTRIES) {
    if (
      pronunciations.some(
        (pronunciation) =>
          pronunciation.slice(0, -1) === pinyin &&
          (tone === "" || pronunciation.slice(-1) === tone)
      )
    ) {
      chars.push(...characters);
    }
  }

  return chars;
}
