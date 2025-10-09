import { commentsCache } from "../cache";
import { deepEqual } from "@shared/common/object";
import { ValidFeatureKey } from "../types";

type Commentator = {
  Xs: ValidFeatureKey[];
  Y: ValidFeatureKey;
  comment: Record<string, string>;
};

export function findCommentator(
  featureKeyXs: ValidFeatureKey[],
  featureKeyY: ValidFeatureKey
): Commentator | null {
  const COMMENTATOR_MAP: Record<string, Commentator> = commentsCache.get();
  for (const [_, commentator] of Object.entries(COMMENTATOR_MAP)) {
    if (
      deepEqual(featureKeyXs, commentator.Xs) &&
      deepEqual(featureKeyY, commentator.Y)
    ) {
      return commentator;
    }
  }
  return null;
}

export function getComment(
  featureKeyXs: ValidFeatureKey[],
  featureKeyY: ValidFeatureKey,
  xs: string,
  y: string
): string {
  return (
    findCommentator(featureKeyXs, featureKeyY)?.comment[
      `${JSON.parse(xs).join("_")}-${y}`
    ] ?? ""
  );
}
