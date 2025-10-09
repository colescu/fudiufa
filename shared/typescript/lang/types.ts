import { MCInfo } from "../mc";

export type Language = "FG" | "PM" | "GC" | "SW";

// pronunciations all in pinyin
export interface LangEntry {
  language: Language;
  字頭: string | null;
  讀音: string; // 記錄讀音 || 推導讀音
  記錄讀音: string | null;
  推導讀音: string | null;
  層: string | null;
  訓作: string | null;
  釋義: string | null;
  小韻號: number | null;
  MC: MCInfo | null; // property from 小韻號
}
