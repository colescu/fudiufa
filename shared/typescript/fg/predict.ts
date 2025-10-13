import { MCEntry, MCInfo } from "../mc";

function hasIntersection(group1: string, group2: string): boolean {
  return group1.split("").some((value) => group2.includes(value));
}

export function getFullFinal(mcInfo: MCInfo): string {
  return (["攝", "韻系", "等", "呼"] as const)
    .map((item) => mcInfo[item])
    .join("");
}

// Everything is ad hoc for FG

const 梗攝_MAP = {
  en: "ang",
  eh: "ah",
  in: "iang",
  ih: "iah",
  iung: "iang",
  iuh: "iah",
} as const;

const 知三章_MAP = {
  d: "z",
  t: "c",
  x: "s",
} as const;

function predictStratum(
  initials: string,
  final: string,
  pronunciation: string,
  stratum: "白" | "新"
): string {
  switch (stratum) {
    case "白":
      // 透定
      if (
        hasIntersection(initials, "透定") &&
        pronunciation[1] &&
        (!"iu".includes(pronunciation[1]) || pronunciation.endsWith("ui"))
      ) {
        pronunciation = "h" + pronunciation.slice(1);
      }
      // 匣合
      if (hasIntersection(initials, "匣")) {
        if (pronunciation[0] === "f" && final[0] !== "通") {
          pronunciation = "u" + pronunciation.slice(1);
          if (pronunciation.startsWith("uu")) {
            pronunciation = pronunciation.slice(1);
          }
        }
        if (
          final[0] === "梗" &&
          final[3] === "合" &&
          pronunciation.startsWith("x")
        ) {
          pronunciation = pronunciation.slice(1);
        }
      }
      // 日 ad hoc
      if (hasIntersection(initials, "日")) {
        for (const [key, value] of [
          ["leu", "niau"],
          ["len", "nien"],
          ["let", "niet"],
          ["ien", "nien"],
          ["iet", "niet"],
          ["long", "niong"],
          ["loh", "nioh"],
          ["iung", "niung"],
          ["iuh", "niuh"],
        ] as const) {
          if (pronunciation === key) {
            pronunciation = value;
            break;
          }
        }
      }
      // 梗
      if (final[0] === "梗") {
        for (let [key, value] of Object.entries(梗攝_MAP)) {
          if (pronunciation.endsWith(key)) {
            if (
              initials
                .split("")
                .every((initial) => "知徹澄章昌常書船".includes(initial)) &&
              value[0] === "i"
            ) {
              value = value.slice(1) as any;
              if (pronunciation[0] === "x") {
                pronunciation = "s" + pronunciation.slice(1);
              }
            }
            pronunciation = pronunciation.slice(0, -key.length) + value;
            if (pronunciation.startsWith("ngi")) {
              pronunciation = "ni" + pronunciation.slice(3);
            }
            break;
          }
        }
      }
      // 魚
      if (final[1] === "魚") {
        for (const value of ["ni", "di", "i"]) {
          if (pronunciation === value) {
            pronunciation += "e";
            break;
          }
        }
        if (pronunciation.endsWith("u")) {
          pronunciation = pronunciation.slice(0, -1) + "e";
        }
        for (const [key, value1, value2] of [
          ["ji", "z", "g"],
          ["qi", "c", "k"],
          ["xi", "s", "h"],
        ] as const) {
          if (pronunciation.startsWith(key)) {
            pronunciation =
              (hasIntersection(initials, "精清從心邪") ? value1 : value2) + "e";
            break;
          }
        }
      }
      // 疑模
      if (hasIntersection(initials, "疑") && final[1] === "模") {
        pronunciation = "ng";
      }
      // 蟹一合
      if (
        final[0] === "蟹" &&
        final[2] === "一" &&
        ((final[3] === "合" && !hasIntersection(initials, "見溪羣疑")) ||
          hasIntersection(initials, "幫滂並明"))
      ) {
        pronunciation =
          pronunciation.slice(0, pronunciation.endsWith("ui") ? -2 : -1) + "oi";
        if (pronunciation === "oi") {
          pronunciation = "uoi";
        }
      }
      break;
    case "新":
      // 知三章
      if (hasIntersection(initials, "知徹澄章昌常書船")) {
        for (const [key, value] of Object.entries(知三章_MAP)) {
          if (pronunciation.startsWith(key)) {
            pronunciation = value + pronunciation.slice(key.length);
            break;
          }
        }
      }
      // 日 ad hoc
      if (hasIntersection(initials, "日")) {
        if (pronunciation === "e" && final[0] === "遇") {
          pronunciation = "lu";
        }
        for (const [key, value] of [
          ["in", "len"],
          ["iu", "leu"],
          ["ien", "lan"],
          ["iet", "let"],
          ["iung", "lung"],
          ["iuh", "luh"],
          ["ien", "len"],
          ["nia", "le"],
          ["nin", "len"],
          ["nit", "lit"],
          ["nyon", "lon"],
          ["nyot", "lot"],
          ["leu", "lau"],
          ["len", "lan"],
        ] as const) {
          if (pronunciation === key) {
            pronunciation = value;
            break;
          }
        }
      }
      // 上述情況的韻母
      if (hasIntersection(initials, "知徹澄章昌常書船")) {
        if (pronunciation.endsWith("eu") && final[0] === "效") {
          pronunciation = pronunciation.slice(0, -2) + "au";
        }
        if (pronunciation.endsWith("iu")) {
          pronunciation = pronunciation.slice(0, -2) + "eu";
        }
        if (pronunciation.endsWith("en")) {
          pronunciation = pronunciation.slice(0, -2) + "an";
        }
        if (pronunciation.endsWith("in")) {
          pronunciation = pronunciation.slice(0, -2) + "en";
        }
      }
      // 疑細
      if (
        hasIntersection(initials, "疑") &&
        pronunciation.startsWith("n") &&
        !pronunciation.startsWith("ng")
      ) {
        pronunciation = pronunciation.slice(1);
      }
      // 麻三
      if (final.includes("麻三")) {
        pronunciation = pronunciation.slice(0, -1) + "e";
      }
      // 通三
      if (final[0] === "通" && final[2] === "三") {
        for (const value of ["ni", "di"]) {
          if (pronunciation.startsWith(value) && initials !== "疑") {
            pronunciation = "l" + pronunciation.slice(value.length);
            break;
          }
        }
        for (const [key, value1, value2] of [
          ["ji", "z", "g"],
          ["qi", "c", "k"],
        ] as const) {
          if (pronunciation.startsWith(key)) {
            pronunciation =
              (hasIntersection(initials, "精清從") ? value1 : value2) +
              pronunciation.slice(2);
            break;
          }
        }
        if (
          pronunciation.startsWith("xi") &&
          hasIntersection(initials, "心邪")
        ) {
          pronunciation = "s" + pronunciation.slice(2);
        }
      }
      // 梗曾
      if ("梗曾".includes(final[0]!) && "一二".includes(final[2]!)) {
        if (hasIntersection(initials, "幫滂並明")) {
          for (const [key, value] of [
            ["en", "ung"],
            ["eh", "oh"],
          ] as const) {
            if (pronunciation.endsWith(key)) {
              pronunciation = pronunciation.slice(0, -key.length) + value;
              break;
            }
          }
        }
        if (hasIntersection(initials, "曉匣")) {
          if (pronunciation === "hen") {
            pronunciation = "xin";
          }
        }
        if (hasIntersection(initials, "疑影")) {
          for (const [key, value] of [
            ["ngen", "in"],
            ["ngeh", "ngoh"],
          ] as const) {
            if (pronunciation === key) {
              pronunciation = value;
              break;
            }
          }
        }
        if (
          hasIntersection(initials, "見溪羣疑曉匣") &&
          final[3] === "合" &&
          pronunciation.endsWith("en")
        ) {
          pronunciation = (pronunciation.slice(0, -2) + "ung").replace(
            "uu",
            "u"
          );
        }
      }
      if (
        final[0] === "梗" &&
        "三四".includes(final[2]!) &&
        final[3] === "合"
      ) {
        if (pronunciation.endsWith("iung")) {
          pronunciation = pronunciation.slice(0, -4) + "in";
        }
      }
      // 莊止合
      if (
        hasIntersection(initials, "莊初崇生俟") &&
        final[0] === "止" &&
        final[3] === "合" &&
        pronunciation.endsWith("ai")
      ) {
        pronunciation = pronunciation.slice(0, -2) + "oi";
      }
      // 來山三合
      if (hasIntersection(initials, "來") && pronunciation === "dyn") {
        pronunciation = "lun";
      }
      break;
  }
  return pronunciation;
}

const VOICING_MAP = {
  p: "b",
  t: "d",
  c: "z",
  q: "j",
  k: "g",
} as const;

export function getReflexes(
  initials: string,
  final: string,
  pronunciation: string,
  ignoreVoicing: boolean,
  ignoreTone: boolean
): // 默認, 白, 新
[string, string, string] {
  let tone = "";
  if (!isNaN(Number(pronunciation.at(-1)))) {
    tone = pronunciation.slice(-1);
    pronunciation = pronunciation.slice(0, -1);
  }

  if (ignoreVoicing) {
    for (const [key, value] of Object.entries(VOICING_MAP)) {
      if (pronunciation.startsWith(key)) {
        pronunciation = value + pronunciation.slice(key.length);
        break;
      }
    }
    if (
      initials.split("").every((initial) => "透定".includes(initial)) &&
      pronunciation[0] === "d"
    ) {
      pronunciation = "t" + pronunciation.slice(1);
    }
  }

  let 白_tone = tone;
  if (!ignoreTone) {
    if (hasIntersection(initials, "明泥來娘日疑云以") && tone === "7") {
      白_tone = "8";
    }
  } else {
    tone = "";
    白_tone = "";
  }

  return [
    pronunciation + tone,
    predictStratum(initials, final, pronunciation, "白") + 白_tone,
    predictStratum(initials, final, pronunciation, "新") + tone,
  ];
}

export function getReflexesByEntry(entry: MCEntry) {
  return getReflexes(
    entry.MC.聲母,
    getFullFinal(entry.MC),
    entry.reflex.FG!,
    false,
    false
  );
}
