import { Language, LANGUAGES } from "../lang";
import { syllableDataCache } from "./cache";

function normalizeTone(
  tone: string,
  syllable: string,
  language: Language
): string {
  switch (language) {
    // case "FG":
    // FIXME cannot tell apart 1 6
    case "GC":
      if (
        ["p", "p̚", "t", "t̚", "k", "k̚"].some((coda) => syllable.endsWith(coda))
      ) {
        for (const [舒, 入] of ["17", "38", "69"]) {
          if (tone === 舒) {
            tone = 入;
            break;
          }
        }
      }
      break;
    // case 'MH':
  }
  return tone;
}

export let toneUtils = {} as Record<
  Language,
  ReturnType<typeof createToneUtils>
>;

function createToneUtils(
  TONES: {
    [tone: string]: { [label: string]: string };
  },
  language: Language
) {
  type Tone = keyof typeof TONES;
  type ToneNotation = keyof (typeof TONES)[Tone];

  function parse(value: string): [string, string] {
    value = value.normalize("NFD");
    let tone = "";
    for (const [ordinal, data] of Object.entries(TONES)) {
      for (const toneValue of [ordinal, ...Object.values(data)]) {
        if (toneValue === "") continue;
        const index = value.lastIndexOf(toneValue);
        if (index !== -1) {
          value = value.slice(0, index) + value.slice(index + toneValue.length);
          tone = normalizeTone(ordinal, value, language);
          break;
        }
      }
      if (tone !== "") break;
    }
    return [value.normalize("NFC"), tone];
  }

  function show(value: string, toneNotation: ToneNotation): string {
    let [syllable, tone] = parse(value);

    if (toneNotation === "diacritic") {
      const diacritic = TONES[tone]?.["diacritic"];
      if (diacritic == undefined) {
        throw new Error("Diacritic tone notation does not exist.");
      }

      // syllabic nasals
      if (["m", "n", "ng"].includes(syllable)) {
        return (syllable[0] + diacritic).normalize("NFC") + syllable.slice(1);
      }

      // Ad hoc algorithm for finding diacritic pivot
      // priority of vowels to put the diacritic
      // LATER fix for VN
      const NUCLEUS = "aoêeüuiy";

      let position = syllable.length - 1;
      while (position >= 0 && !NUCLEUS.includes(syllable[position]!)) {
        position--;
      }
      if (position > 0) {
        const current = syllable[position]!,
          previous = syllable[position - 1]!;
        if (
          NUCLEUS.includes(previous) &&
          NUCLEUS.indexOf(previous) < NUCLEUS.indexOf(current) &&
          !(previous === "u" && current === "i")
        ) {
          position--;
        }
      }
      return (
        syllable.slice(0, position + 1) +
        diacritic +
        syllable.slice(position + 1)
      ).normalize("NFC");
    }

    return syllable + (TONES[tone]?.[toneNotation] ?? tone);
  }

  return { parse, show };
}

export function initToneUtils() {
  const TONES = syllableDataCache.get("tones");

  LANGUAGES.forEach((language) => {
    toneUtils[language] = createToneUtils(TONES[language], language);
  });
}
