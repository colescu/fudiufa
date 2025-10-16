import { MCInfo } from "../mc";

export type ProtoSettings = {
  閉口韻尾: boolean;
  尖團: boolean;
  陽去: boolean;
  泥來: boolean;
  疑影: boolean;
  前後鼻音: boolean;
};

const 尖團_MAP = {
  tɕ: "ts",
  t͡ɕ: "t͡s",
  ɕ: "s",
} as const;

const 閉口韻尾_MAP = {
  n: "m",
  t: "p",
  t̚: "p̚",
} as const;

const 陽去_MAP = {
  "²²": "¹¹",
  "˨": "˩",
} as const;

// Ad hoc transformer for proto FG
// pass this on ipa form (any tone notation)
export function simulateProto(
  pronunciation: string,
  mcInfo: MCInfo | null | undefined,
  settings: ProtoSettings
) {
  if (!mcInfo) return pronunciation;

  if (
    settings.閉口韻尾 &&
    "深咸".includes(mcInfo.攝) &&
    !"pmf".split("").some((initial) => pronunciation.startsWith(initial))
  ) {
    for (const [newCoda, protoCoda] of Object.entries(閉口韻尾_MAP)) {
      if (pronunciation.slice(1).includes(newCoda)) {
        pronunciation =
          pronunciation[0] + pronunciation.slice(1).replace(newCoda, protoCoda);
        break;
      }
    }
  }

  if (
    settings.尖團 &&
    !"見影".includes(mcInfo.組) &&
    pronunciation.includes("i") // 韻母 === "i"
  ) {
    for (const [newInitial, protoInitial] of Object.entries(尖團_MAP)) {
      if (pronunciation.startsWith(newInitial)) {
        pronunciation = protoInitial + pronunciation.slice(newInitial.length);
        break;
      }
    }
  }

  if (
    settings.陽去 &&
    mcInfo.清濁.includes("濁") &&
    "上去".includes(mcInfo.聲調)
  ) {
    for (const [newTone, protoTone] of Object.entries(陽去_MAP)) {
      if (pronunciation.endsWith(newTone)) {
        pronunciation = pronunciation.replace(newTone, protoTone);
        break;
      }
    }
  }

  if (settings.泥來 && mcInfo.聲母 === "泥" && pronunciation[0] === "l") {
    pronunciation = "n" + pronunciation.slice(1);
  }

  if (settings.疑影 && mcInfo.聲母 === "影" && pronunciation[0] === "ŋ") {
    pronunciation = pronunciation.slice(1);
  }

  if (settings.前後鼻音 && "梗曾".includes(mcInfo.攝)) {
    pronunciation = pronunciation.replace("ɛn", "ɛŋ").replace("in", "iŋ");
  }

  if (mcInfo.聲母 === "日" && "止遇".includes(mcInfo.攝)) {
    pronunciation = "ɵ" + pronunciation.slice(1);
  }

  return pronunciation;
}
