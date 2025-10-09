import { createCache, fetchFile } from "../cache";

const SUB_PAIRS = [
  ["0", "⁰"],
  ["1", "¹"],
  ["2", "²"],
  ["3", "³"],
  ["4", "⁴"],
  ["5", "⁵"],
  ["6", "⁶"],
  ["7", "⁷"],
  ["8", "⁸"],
  ["9", "⁹"],
  ["ʔ", "ˀ"],
] as const;

function toSup(value: string): string {
  return value.replace(/./g, (c) => {
    const pair = SUB_PAIRS.find(([from]) => from === c);
    return pair ? pair[1] : c;
  });
}

export const syllableDataCache = createCache(
  (item: "syllables" | "tones" | "parts" | "all-parts") =>
    fetchFile(item, "json"),
  (object, args) => {
    if (args?.[0] === "tones") {
      Object.values(object).forEach((tones: any) => {
        Object.values(tones).forEach((data: any) => {
          const number = data?.["number"];
          if (number) {
            data["number"] = toSup(number);
          }
        });
      });
    }
    return object;
  }
);
