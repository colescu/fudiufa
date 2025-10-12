import { MCInfo } from "../mc";

export type VariantSettings = {
  ɥon: boolean;
  jau: boolean;
  jo: boolean;
  kɛ: boolean;
  tsɛ: boolean;
  y: boolean;
  ən: boolean;
  fɿn: boolean;
};

// Ad hoc transformer for variant FG

// pass this on database form
export function simulateVariantPre(
  pronunciation: string, // from = to = "pinyin"
  mcInfo: MCInfo | null | undefined,
  settings: VariantSettings
): string {
  if (settings.ɥon) {
    pronunciation = pronunciation.replace(/yo([nt])(\d?)$/, "ye$1$2");
  }

  if (settings.jau) {
    pronunciation = pronunciation.replace(/iau(\d?)$/, "ieu$1");
  }

  if (settings.jo) {
    pronunciation = pronunciation.replace(/io(\d?)$/, "yo$1");
  }

  if (settings.kɛ) {
    for (const [standard, variant] of [
      ["g", "ji"],
      ["k", "qi"],
    ]) {
      pronunciation = pronunciation.replace(
        new RegExp(standard + "e(\\d?)$"),
        `${variant}e$1`
      );
    }
  }

  if (settings.tsɛ && mcInfo && "魚虞".split("").includes(mcInfo.韻系)) {
    for (const [standard, variant] of [
      ["z", "ji"],
      ["c", "qi"],
      ["s", "xi"],
    ]) {
      pronunciation = pronunciation.replace(
        new RegExp(standard + "e(\\d?)$"),
        `${variant}e$1`
      );
    }
  }

  if (settings.y && mcInfo && "魚虞".split("").includes(mcInfo.韻系)) {
    pronunciation = pronunciation.replace(/i(\d?)$/, "y$1");
  }

  return pronunciation;
}

// pass this on ipa form
export function simulateVariantPost(
  pronunciation: string, // from = to
  mcInfo: MCInfo | null | undefined,
  settings: VariantSettings
): string {
  // CHECK 變體 ən 的適用範圍
  if (
    settings.ən &&
    !["p", "m", "f"].some((initial) => pronunciation.startsWith(initial)) &&
    mcInfo &&
    !"咸山".split("").includes(mcInfo.攝)
  ) {
    pronunciation = pronunciation.replace("ɛn", "ən");
  }

  if (
    settings.fɿn &&
    ["p", "m", "f"].some((initial) => pronunciation.startsWith(initial))
  ) {
    pronunciation = pronunciation
      .normalize("NFD")
      .replace("ut", "ɨt")
      .normalize("NFC");
    pronunciation = pronunciation.replace("un", "ɨn");
  }

  return pronunciation;
}
