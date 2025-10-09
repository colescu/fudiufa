import { getLangFeature } from "./feature-lang";
import { getMCFeature } from "./feature-mc";
import { Feature, ValidFeatureKey } from "../types";

export function getFeature(featureKey: ValidFeatureKey): Feature {
  const { language, field } = featureKey;
  return language === "MC"
    ? getMCFeature(field)
    : getLangFeature(language as any, field);
}
