import { createCache } from "./cache";
import { parseChineseDate } from "../common/date";
import { DATA_URL } from "../config";

async function fetchLastUpdate() {
  try {
    const response = await fetch(`${DATA_URL}/last-update.txt`);
    const text = await response.text();
    return parseChineseDate(text);
  } catch (error) {
    console.error("Error fetching the last update date:", error);
    return undefined;
  }
}

export const lastUpdateCache = createCache(fetchLastUpdate);
