import { PredictForm } from "./types";
import {
  MC_FIELDS,
  MC_OPTIONS_MAP,
} from "@/modules/ReflexTable/typescript/feature-mc";
import {
  LANG_FIELDS,
  LANG_OPTIONS_MAP,
} from "@/modules/ReflexTable/typescript/feature-lang";
import { EmptyFeatureKey, FeatureGroup } from "@/modules/ReflexTable/types";
import { Language } from "@shared/lang";

const GROUPS = ["聲母", "韻母", "聲調"] as const;

export const GROUP_OPTIONS = GROUPS.map((group) => ({
  value: group,
  label: group,
}));

export function getFieldOptions(language: string, group: FeatureGroup | "") {
  if (language == "") return [];
  const allOptions = language === "MC" ? MC_OPTIONS_MAP : LANG_OPTIONS_MAP;
  return group === ""
    ? Object.entries(allOptions).map(([group, options]) => ({
        type: "group",
        key: `group-${group}`,
        label: group,
        children: options,
      }))
    : allOptions[group];
}

export function getGroup(language: string, field: string): FeatureGroup | "" {
  if (language == "") return "";
  const allOptions = language === "MC" ? MC_OPTIONS_MAP : LANG_OPTIONS_MAP;
  for (const [group, options] of Object.entries(allOptions)) {
    if (options.map((option: any) => option.value).includes(field)) {
      return group as FeatureGroup;
    }
  }
  return "";
}

function getEmptyFeatureKey(): EmptyFeatureKey {
  return { language: "", group: "", field: "" };
}

function isFeatureKey({
  language,
  field,
}: {
  language: "MC" | Language | "lang" | "";
  field: string;
}): boolean {
  if (language == "") return false;
  return ((language === "MC" ? MC_FIELDS : LANG_FIELDS) as string[]).includes(
    field
  );
}

function getEmptyForm(): PredictForm {
  return {
    Xs: [getEmptyFeatureKey()],
    Y: getEmptyFeatureKey(),
  };
}

function checkForm(form: PredictForm): boolean {
  return form.Xs.length > 0 && [...form.Xs, form.Y].every(isFeatureKey);
}

function getFormActions(form: PredictForm): Record<string, () => void> {
  return {
    addX: () => {
      form.Xs.push(getEmptyFeatureKey());
    },
    deleteX: () => {
      form.Xs.pop();
    },
    clear: () => {
      form.Xs = [getEmptyFeatureKey()];
      form.Y = getEmptyFeatureKey();
    },
    reverse: () => {
      const { Xs, Y } = JSON.parse(JSON.stringify(form));
      if (Y.language === "lang") {
        Y.language = "";
      }
      form.Xs = [Y];
      form.Y = Xs[0];
    },
  };
}

export const PredictFormUtils = {
  getEmptyForm,
  checkForm,
  getFormActions,
};
