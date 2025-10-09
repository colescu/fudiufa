import { MCField } from "./typescript/feature-mc";
import { LangField } from "./typescript/feature-lang";
import { MCEntry } from "@shared/mc";
import { Language } from "@shared/lang";

// reflex table

export type PossibilityData = {
  value: string;
  frequency: number;
  comment: string;
  mcIndices?: number[];
};

export type ColumnData = {
  // { valueX: possibilityY[] }
  [value: string]: PossibilityData[];
};

// feature

export type Feature = {
  label: string; // displayed
  getter: (entry: MCEntry) => string;
  values: string[];
  shower?: (value: string, settings?: any) => string;
};

export type FeatureGroup = "聲母" | "韻母" | "聲調";

export type EmptyFeatureKey = { language: ""; group: ""; field: "" };
export type ValidFeatureKey =
  | { language: "MC"; group: FeatureGroup; field: MCField }
  | { language: Language; group: FeatureGroup; field: LangField };
export type FeatureKey = ValidFeatureKey | EmptyFeatureKey;

export type LangFeatureKey = {
  language: "lang";
  group: FeatureGroup;
  field: LangField;
};
