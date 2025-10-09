import {
  FeatureKey,
  ValidFeatureKey,
  LangFeatureKey,
} from "@/modules/ReflexTable/types";

export type PredictForm = {
  Xs: FeatureKey[];
  Y: FeatureKey | LangFeatureKey;
};
export type ValidPredictForm = {
  Xs: ValidFeatureKey[];
  Y: ValidFeatureKey | LangFeatureKey;
};
