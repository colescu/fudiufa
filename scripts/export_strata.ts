import { readFileSync, writeFileSync } from "fs";
import { getReflexesByEntry } from "../shared/typescript/fg/predict";
import { MCEntry } from "../shared/typescript/mc";

function getReflexes(entry: MCEntry) {
  const pronunciations = getReflexesByEntry(entry);
  return ["白", "新"]
    .map((stratum, index) => {
      const pronunciation = pronunciations[index + 1];
      return (
        pronunciations[0] !== pronunciation && [
          stratum,
          pronunciations[index + 1],
        ]
      );
    })
    .filter(Boolean);
}

const MC_ENTRIES_MAP: Record<number, MCEntry> = JSON.parse(
  readFileSync("./data/generated/MC.json", { encoding: "utf-8" })
);

const FG_REFLEXES = Object.fromEntries(
  Object.entries(MC_ENTRIES_MAP)
    .map(([index, entry]) => [index, getReflexes(entry)])
    .filter(([index, strata]) => strata.length > 0)
);

const STRATA: Record<string, any> = JSON.parse(
  readFileSync("./data/generated/strata.json", { encoding: "utf-8" })
);

STRATA["FG"] = FG_REFLEXES;

writeFileSync("./data/generated/strata.json", JSON.stringify(STRATA), {
  encoding: "utf8",
});

console.log("推導撫州話其他層次完成！");
