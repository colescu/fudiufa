import { createCache, fetchFile } from "@shared/cache";

export const commentsCache = createCache(() => fetchFile("comments", "json"));
