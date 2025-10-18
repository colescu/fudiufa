import { Language } from "./types";

export const LANGUAGE_MAP: Record<Language, string> = {
  FG: "撫州話",
  PM: "普通話",
  GC: "廣州話",
  SW: "上海話",
  MH: "梅縣話",
  JP: "日本音",
  KR: "朝鮮音",
  VN: "越南音",
} as const;

export const LANGUAGES = Object.keys(LANGUAGE_MAP) as readonly Language[];
export const PARTIAL_LANGUAGES =
  localStorage.getItem("user") === "colescu"
    ? LANGUAGES
    : (["FG", "PM", "GC", "SW"] as readonly Language[]);
