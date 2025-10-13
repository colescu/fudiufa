import { mcCache, strataCache } from "./cache";

export async function initMCModule() {
  await Promise.all([mcCache.load(), strataCache.load()]);
}
