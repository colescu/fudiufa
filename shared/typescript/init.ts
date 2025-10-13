import { loadCJKData } from "./cjk/cache";
import { initSyllableModule } from "./syllable/init";
import { initMCModule } from "./mc/init";

export async function init() {
  await Promise.all([loadCJKData(), initSyllableModule(), initMCModule()]);
}
