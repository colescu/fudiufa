export const DATA_URL =
  (typeof import.meta !== "undefined" &&
    (import.meta as any).env?.VITE_DATA_URL) ||
  "/data";

export const EXTERNAL_URL =
  typeof import.meta !== "undefined" &&
  (import.meta as any).env?.VITE_EXTERNAL_URL;
