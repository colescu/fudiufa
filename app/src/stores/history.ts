import { defineStore } from "pinia";
import { ValidPredictForm } from "@/views/Phonology/Predict/types";
import { Language, LANGUAGES } from "@shared/lang";
import { CODAS } from "@shared/mc";
import { VariantSettings } from "@shared/fg/variant";
import { ProtoSettings } from "@shared/fg/proto";
import { fromEntriesConst } from "@shared/common/object";

export const useHistoryStore = defineStore("history", {
  state: () => ({
    phonology: {
      tab: "sangyntiau",
      subtabs: {
        sangyntiau: "sangmu",
        nienjiu: "tehdin",
        bigau: "PM" as Exclude<Language, "FG">,
      },
      rhymeTable: {
        filter: {
          老: false,
          新: false,
          官: false,
        },
      },
      diachronicTable: {
        itemOrdering: ["攝", "等", "韻", "呼"],
        filterCodas: Object.fromEntries(CODAS.map((coda) => [coda, true])),
        stratum: "",
      },
      predict: {
        form: null as ValidPredictForm | null,
        show: {
          comment: true,
          frequency: true,
        },
      },
    },
    vocabulary: {
      tab: "fongnienci",
      subtabs: {
        ci: "揇" as string,
        diun: "diji",
      },
    },
    search: {
      tab: "ci",
      langMode: 0,
      resultsMap: fromEntriesConst(
        LANGUAGES.map((language) => [language, null])
      ) as Record<Language, number[] | null>,
      page: 1,
    },
    pronounce: {
      input: "" as string,
      outputChoicesMap: fromEntriesConst(
        LANGUAGES.map((language) => [language, []])
      ) as Record<Language, (number | undefined)[]>,
      style: "interlinear",
      prefer: {
        新: false,
        文: false,
      },
      includePredicted: true,
      variant: {
        enable: true,
        settings: {
          ɥon: false,
          jau: false,
          jo: false,
          kɛ: false,
          tsɛ: false,
          y: false,
          ən: false,
          fɿn: false,
        } as VariantSettings,
      },
      proto: {
        enable: false,
        settings: {
          閉口韻尾: true,
          尖團: true,
          陽去: true,
          泥來: true,
          疑影: true,
          前後鼻音: true,
        } as ProtoSettings,
      },
    },
    languageOrdering: [...LANGUAGES] as Language[],
  }),
  persist: true,
});
