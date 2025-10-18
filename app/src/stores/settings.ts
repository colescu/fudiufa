import { defineStore } from "pinia";
import { DEFAULT_MC_INFO_STYLE } from "@shared/mc";
import { PARTIAL_LANGUAGES } from "@shared/lang";

export const useSettingsStore = defineStore("settings", {
  state: () => ({
    isSimplified: true,
    format: "pinyin" as Format, // preferred representation
    displayBoth: true,
    pinyinToneNotation: "diacritic" as PinyinToneNotation,
    ipaToneNotation: "letter" as IpaToneNotation,
    pinyinSettings: {
      JP: {
        historical: true,
        format: "kata",
      },
      KR: {
        format: "hangul",
      },
    },
    playSpeed: 500,
    colorizeChar: false,
    dictionary: {
      disable: {
        官: false,
        新: false,
      },
    },
    mcInfoStyle: DEFAULT_MC_INFO_STYLE,
    finalOrdering: ["韻腹", "介音", "韻尾"],
    languages: [...PARTIAL_LANGUAGES],
  }),
  persist: true,
});
