import { loadCJKData } from "./cjk/cache";
import { initSyllableModule } from "./syllable/init";
import { mcCache } from "./mc";

export async function init() {
  await Promise.all([loadCJKData(), initSyllableModule(), mcCache.load()]);
}
