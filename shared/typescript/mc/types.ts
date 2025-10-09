import { Language } from "../lang";

export type MCInfoStyle = {
  ordering: Exclude<keyof MCInfo, "音韻地位">[];
  show: { 攝: boolean; 聲調: boolean };
  final: "韻系" | "韻系舒入" | "韻目";
};

export interface MCInfo {
  字: string; // 代表字
  反切: string | null; // 例：德紅切
  音韻地位: (style?: MCInfoStyle) => string; // 例：端通東一平
  聲母: string; // 例：端
  清濁: string; // 例：全清
  音: string; // 例：舌
  組: string; // 例：端
  攝: string; // 例：通
  韻系: string; // 例：東
  等: string; // 例：一
  呼: "開" | "合" | "";
  重紐: "A" | "B" | null;
  聲調: string; // 例：平
}

export interface MCEntry {
  字數: number;
  MC: MCInfo;
  reflex: Record<Language, string | null>; // expected reflex in pinyin
}
