import { createCache, fetchFile } from "../cache";
import { EXTERNAL_URL } from "../config";

export const variantsCache = createCache(
  () => fetchFile("variants", "txt"),
  (text: string) => text.split(/\r?\n/)
);

export const s2tCache = createCache(
  async () => {
    const response = await fetch(
      (EXTERNAL_URL ??
        "https://raw.githubusercontent.com/BYVoid/OpenCC/refs/heads/master/data/dictionary") +
        "/STCharacters.txt"
    );
    const text = await response.text();
    return text;
  },
  (text: string) =>
    Object.fromEntries(
      text
        .trim()
        .split(/\r?\n/)
        .map((row) => {
          const [s, ts, _] = row.split("\t");
          return [s, ts!.split(" ")];
        })
    )
);

export const commonCharactersCache = createCache(() =>
  fetchFile("通用字", "txt")
);

export async function loadCJKData() {
  await Promise.all([
    variantsCache.load(),
    s2tCache.load(),
    commonCharactersCache.load(),
  ]);
}
