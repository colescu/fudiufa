import { getFromDB, putToDB } from "./db";
import { DATA_URL } from "../config";
import { lastUpdateCache } from "./last-update";

// Updates cache after checking timestamp
export async function fetchFile(
  filename: string,
  format: "txt" | "csv" | "tsv" | "json" | "yaml",
  baseUrl: string = DATA_URL
) {
  const key = `${filename}.${format}`;
  const url = `${baseUrl}/${key}`;

  const lastUpdate = await lastUpdateCache.getAsync();

  if (process.env.NODE_ENV !== "development") {
    try {
      const cached = await getFromDB(key);
      if (cached && cached.timestamp === lastUpdate?.getTime()) {
        return cached.data;
      }
    } catch (error) {
      console.error("Error fetching from DB:", error);
    }
  }

  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`HTTP error ${response.status} when fetching ${key}`);
  }

  const data =
    format === "json" ? await response.json() : await response.text();

  try {
    if (lastUpdate) {
      await putToDB({ key, data, timestamp: lastUpdate.getTime() });
    } else {
      console.warn("Unknown last update date, skipping DB save.");
    }
  } catch (error) {
    console.error("Error saving to DB:", error);
  }

  console.log(`Successfully fetched ${key}`);

  return data;
}
