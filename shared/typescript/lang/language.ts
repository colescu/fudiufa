import { Language } from "./types";

export const LANGUAGE_MAP: Record<Language, string> = {
  FG: "撫州話",
  PM: "普通話",
  GC: "廣州話",
  SW: "上海話",
} as const;

export const LANGUAGES = Object.keys(LANGUAGE_MAP) as readonly Language[];
