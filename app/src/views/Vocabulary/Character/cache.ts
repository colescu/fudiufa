import { createCache, fetchFile } from "@shared/cache";
import yaml from "js-yaml";
import { CharacterData } from "./types";

export const charactersCache = createCache(
  () => fetchFile("characters", "yaml"),
  (text: string) => yaml.load(text) as CharacterData[]
);
