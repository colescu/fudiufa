import { createCache, fetchFile } from "@shared/cache";

export const rhymeTableCache = createCache(() =>
  fetchFile("rhyme-table", "json")
);
