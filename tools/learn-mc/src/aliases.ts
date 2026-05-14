import { simplifier } from "@shared/cjk";
import { FULL_FINALS, MC_CATEGORIES, 入舒_MAP } from "@shared/mc";

export type FieldInput = {
  initial: string;
  she: string;
  final: string;
  tone: string;
};

export type FieldKey = keyof FieldInput;

const unique = <T>(items: T[]) => [...new Set(items)];
export const shortFinal = (value: string) =>
  collapseShortFinal(Array.from(value).slice(1).join(""));

type SearchMode = "includes" | "prefix";
type SearchToken = readonly [value: string, mode: SearchMode];
type SearchMap = Map<string, SearchToken[]>;
type SearchRow = readonly [canonical: string, searchAliases: string];
const divisionDigits: Record<string, string> = {
  一: "1",
  二: "2",
  三: "3",
  四: "4",
};

export const options = {
  initial: [...MC_CATEGORIES.聲母],
  she: [...MC_CATEGORIES.攝],
  final: unique(FULL_FINALS.map(shortFinal)),
  tone: [...MC_CATEGORIES.聲調],
};

export const placeholders: FieldInput = {
  initial: "幫",
  she: "假",
  final: "麻二開",
  tone: "平",
};

const normalizeExact = (value: string) =>
  simplifier(value.normalize("NFKC"))
    .trim()
    .toLowerCase()
    .replace(/ʰ/g, "h")
    .replace(/ɨ/g, "+")
    .replace(/\s+/g, "");

const charPinyin: Record<string, string> = {
  帮: "bang",
  滂: "pang",
  并: "bing",
  明: "ming",
  端: "duan",
  透: "tou",
  定: "ding",
  泥: "ni",
  来: "lai",
  知: "zhi",
  彻: "che",
  澄: "cheng",
  娘: "niang",
  精: "jing",
  清: "qing",
  从: "cong",
  心: "xin",
  邪: "xie",
  庄: "zhuang",
  初: "chu",
  崇: "chong",
  生: "sheng",
  俟: "si",
  章: "zhang",
  昌: "chang",
  常: "chang",
  书: "shu",
  船: "chuan",
  日: "ri",
  见: "jian",
  溪: "xi",
  群: "qun",
  疑: "yi",
  影: "ying",
  晓: "xiao",
  匣: "xia",
  云: "yun",
  以: "yi",
  通: "tong",
  江: "jiang",
  止: "zhi",
  遇: "yu",
  蟹: "xie",
  臻: "zhen",
  山: "shan",
  效: "xiao",
  果: "guo",
  假: "jia",
  宕: "dang",
  梗: "geng",
  曾: "zeng",
  流: "liu",
  深: "shen",
  咸: "xian",
  麻: "ma",
  开: "kai",
  合: "he",
  歌: "ge",
  戈: "ge",
  支: "zhi",
  脂: "zhi",
  之: "zhi",
  微: "wei",
  模: "mo",
  鱼: "yu",
  虞: "yu",
  泰: "tai",
  咍: "hai",
  灰: "hui",
  佳: "jia",
  皆: "jie",
  夬: "guai",
  祭: "ji",
  废: "fei",
  齐: "qi",
  豪: "hao",
  肴: "yao",
  宵: "xiao",
  萧: "xiao",
  侯: "hou",
  尤: "you",
  幽: "you",
  覃: "tan",
  谈: "tan",
  盍: "he",
  洽: "qia",
  衔: "xian",
  狎: "xia",
  盐: "yan",
  叶: "ye",
  严: "yan",
  业: "ye",
  凡: "fan",
  乏: "fa",
  添: "tian",
  怗: "tie",
  侵: "qin",
  缉: "ji",
  寒: "han",
  曷: "he",
  桓: "huan",
  末: "mo",
  删: "shan",
  黠: "xia",
  鎋: "xia",
  仙: "xian",
  薛: "xue",
  先: "xian",
  屑: "xie",
  魂: "hun",
  没: "mo",
  痕: "hen",
  麧: "he",
  真: "zhen",
  质: "zhi",
  谆: "zhun",
  术: "shu",
  文: "wen",
  物: "wu",
  欣: "xin",
  迄: "qi",
  元: "yuan",
  月: "yue",
  觉: "jue",
  唐: "tang",
  铎: "duo",
  阳: "yang",
  药: "yao",
  东: "dong",
  屋: "wu",
  冬: "dong",
  沃: "wo",
  钟: "zhong",
  烛: "zhu",
  庚: "geng",
  陌: "mo",
  耕: "geng",
  麦: "mai",
  昔: "xi",
  青: "qing",
  锡: "xi",
  登: "deng",
  德: "de",
  蒸: "zheng",
  职: "zhi",
  平: "ping",
  上: "shang",
  去: "qu",
  入: "ru",
  一: "yi",
  二: "er",
  三: "san",
  四: "si",
};

const finalPinyin: Record<string, readonly string[]> = {
  "東一": ["oung", "uwng"],
  "冬一": ["ong", "owng"],
  "東三": ["ung", "juwng"],
  "鍾三": ["uong", "jowng"],
  "江二": ["oeung", "aewng"],
  "支三開": ["ie", "je"],
  "脂三開": ["i", "jij"],
  "之三開": ["y", "i"],
  "微三開": ["yj", "j+j"],
  "支三合": ["wie", "jwe"],
  "脂三合": ["wi", "jwij"],
  "微三合": ["uj", "jw+j"],
  "模一": ["o", "u"],
  "魚三": ["yo", "jo"],
  "虞三": ["uo", "ju"],
  "咍一開": ["eoj", "oj"],
  "泰一開": ["aj"],
  "灰一合": ["oj", "woj"],
  "泰一合": ["waj"],
  "佳二開": ["ee", "ea"],
  "皆二開": ["eej", "eaj"],
  "夬二開": ["aej"],
  "佳二合": ["wee", "wea"],
  "皆二合": ["weej", "weaj"],
  "夬二合": ["waej"],
  "祭三開": ["iej", "jej"],
  "廢三開": ["yoj", "joj"],
  "祭三合": ["wiej", "jwej"],
  "廢三合": ["uoj", "jwoj"],
  "齊四開": ["ej"],
  "齊四合": ["wej"],
  "痕一開": ["eon", "on"],
  "魂一合": ["on", "won"],
  "眞三開": ["in", "jin"],
  "臻三開": ["yin", "in"],
  "欣三開": ["yn", "j+n"],
  "元三開": ["yon", "jon"],
  "眞三合": ["win", "jwin"],
  "諄三合": ["uin", "jwin"],
  "文三合": ["un", "jun"],
  "元三合": ["uon", "jwon"],
  "寒一開": ["an"],
  "桓一合": ["wan"],
  "刪二開": ["aen"],
  "山二開": ["een", "ean"],
  "刪二合": ["waen"],
  "山二合": ["ween", "wean"],
  "仙三開": ["ien", "jen"],
  "仙三合": ["wien", "jwen"],
  "先四開": ["en"],
  "先四合": ["wen"],
  "豪一": ["aw"],
  "肴二": ["aew"],
  "宵三": ["iew", "jew"],
  "蕭四": ["ew"],
  "歌一開": ["a"],
  "戈一合": ["wa"],
  "戈三開": ["ya", "ja"],
  "戈三合": ["ua", "jwa"],
  "麻二開": ["ae"],
  "麻二合": ["wae"],
  "麻三開": ["iae", "jae"],
  "唐一開": ["ang"],
  "唐一合": ["wang"],
  "陽三開": ["yang", "jang"],
  "陽三合": ["uang", "jwang"],
  "庚二開": ["aeng", "jaeng"],
  "耕二開": ["eeng", "eang"],
  "庚二合": ["waeng"],
  "耕二合": ["weeng", "weang"],
  "庚三開": ["yaeng", "jaeng"],
  "清三開": ["iaeng", "jeng"],
  "庚三合": ["uaeng", "jwaeng"],
  "清三合": ["wiaeng", "jweng"],
  "青四開": ["eng"],
  "青四合": ["weng"],
  "登一開": ["eong", "ong"],
  "登一合": ["weong", "wong"],
  "蒸三開": ["yng", "ing"],
  "蒸三合": ["uing", "wing"],
  "侯一": ["ou", "uw"],
  "尤三": ["u", "juw"],
  "幽三": ["iw", "jiw"],
  "侵三開": ["im"],
  "覃一開": ["om"],
  "談一開": ["am"],
  "咸二開": ["eem", "eam"],
  "銜二開": ["aem"],
  "鹽三開": ["iem", "jem"],
  "嚴三開": ["yom", "jaem"],
  "凡三合": ["uom", "jom"],
  "添四開": ["em"],
};

const initialSearchRows: readonly SearchRow[] = [
  ["幫", "p f"],
  ["滂", "ph p' f"],
  ["並", "b f v"],
  ["明", "m v"],
  ["端", "t"],
  ["透", "th t'"],
  ["定", "d"],
  ["泥", "n"],
  ["來", "l"],
  ["知", "tr ʈ"],
  ["徹", "trh tr' ʈh ʈ'"],
  ["澄", "dr ɖ"],
  ["娘", "nr ɳ"],
  ["精", "ts"],
  ["清", "tsh ts'"],
  ["從", "dz"],
  ["心", "s"],
  ["邪", "z"],
  ["莊", "tsr tʂ ʈʂ"],
  ["初", "tsrh tsr' tʂh tʂ' ʈʂh ʈʂ'"],
  ["崇", "dzr dʐ ɖʐ"],
  ["生", "sr ʂ"],
  ["章", "tj tsy tɕ"],
  ["昌", "tjh tj' tsyh tsy' tɕh tɕ'"],
  ["常", "dj dzy dʑ"],
  ["書", "sj sy ɕ"],
  ["船", "zj zy ʑ"],
  ["日", "nj ny ȵ"],
  ["見", "k"],
  ["溪", "kh k'"],
  ["羣", "g"],
  ["疑", "ng ŋ"],
  ["影", "q ' ʔ"],
  ["曉", "x h"],
  ["匣", "gh h ɣ"],
  ["云", "hj ɦ"],
  ["以", "j y"],
];
const finalAnswerMap = makeFinalAnswerMap();

export const normalizeText = normalizeExact;
export const normalizePinyin = normalizeExact;
export const normalizeInitial = normalizeExact;
export const normalizeShe = normalizeExact;
export const normalizeTone = normalizeExact;

const initialSearch = makeSearchMap(options.initial, initialSearchRows);

const toneSearch = makeSearchMap(options.tone, [
  ["平", "1"],
  ["上", "2 q x"],
  ["去", "3 h"],
  ["入", "4"],
]);
const finalSearch = makeFinalSearchMap();

export const optionFilters: Record<
  FieldKey,
  (option: string, query: string) => boolean
> = {
  initial: (option, query) => matchesSearch(initialSearch, option, query),
  she: defaultOptionFilter,
  final: (option, query) => matchesSearch(finalSearch, option, query),
  tone: (option, query) => matchesSearch(toneSearch, option, query),
};

export function normalizeFinal(value: string, she = "") {
  const final = normalizeExact(value);
  const normalizedShe = normalizeShe(she);
  const withShe =
    normalizedShe &&
    !options.she.some((item) => final.startsWith(normalizeExact(item)))
      ? normalizedShe + final
      : final;
  return finalAnswerMap.get(withShe) ?? withShe;
}

function makeFinalAnswerMap() {
  const map = new Map<string, string>();
  const shortTargets = new Map<string, Set<string>>();

  for (const value of FULL_FINALS) {
    const canonical = collapseFullFinal(value);
    const short = shortFinal(value);
    map.set(normalizeExact(value), canonical);
    shortTargets.set(
      short,
      (shortTargets.get(short) ?? new Set()).add(canonical),
    );
  }

  for (const [short, targets] of shortTargets) {
    if (targets.size === 1) map.set(normalizeExact(short), [...targets][0]!);
  }

  return map;
}

function collapseFullFinal(value: string) {
  const chars = Array.from(value);
  return chars[0]! + collapseShortFinal(chars.slice(1).join(""));
}

function collapseShortFinal(value: string) {
  const chars = Array.from(value);
  const first = chars[0] as keyof typeof 入舒_MAP | undefined;
  const base = first ? 入舒_MAP[first] : undefined;
  return base ? base + chars.slice(1).join("") : value;
}

function makeSearchMap(
  values: readonly string[],
  rows: readonly (readonly [string, string])[],
): SearchMap {
  const map = new Map(values.map((value) => [value, searchTokens(value)]));
  for (const [canonical, aliases] of rows) {
    map.set(canonical, [
      ...(map.get(canonical) ?? []),
      ...searchAliasTokens(aliases),
    ]);
  }
  return map;
}

function makeFinalSearchMap(): SearchMap {
  const map = makeSearchMap(options.final, []);
  for (const option of options.final) {
    map.set(option, [
      ...(map.get(option) ?? []),
      ...finalPinyinAliases(option).map(aliasToken),
    ]);
  }
  return map;
}

function finalPinyinAliases(final: string) {
  const direct = finalPinyin[final];
  if (direct) return unique([...direct, ...direct.map(enteringFinalPinyin)]);
  const chars = Array.from(final);
  const first = chars[0] as keyof typeof 入舒_MAP | undefined;
  const base = first ? 入舒_MAP[first] : undefined;
  const smooth = base ? finalPinyin[base + chars.slice(1).join("")] ?? [] : [];
  return smooth.map(enteringFinalPinyin);
}

function enteringFinalPinyin(value: string) {
  if (value.endsWith("ng")) return value.slice(0, -2) + "k";
  if (value.endsWith("m")) return value.slice(0, -1) + "p";
  if (value.endsWith("n")) return value.slice(0, -1) + "t";
  return value;
}

function defaultOptionFilter(option: string, query: string) {
  return matchesTokens(searchTokens(option), query);
}

function matchesSearch(search: SearchMap, option: string, query: string) {
  return matchesTokens(search.get(option) ?? searchTokens(option), query);
}

function matchesTokens(tokens: readonly SearchToken[], query: string) {
  const q = normalizeExact(query);
  return (
    !q ||
    tokens.some(([token, mode]) =>
      mode === "prefix" ? token.startsWith(q) : token.includes(q),
    )
  );
}

function searchTokens(value: string): SearchToken[] {
  const pinyin = toPinyin(value);
  return [
    [normalizeExact(value), "includes"],
    ...divisionTokens(value),
    ...(pinyin ? [[pinyin, "prefix"] as const] : []),
  ];
}

function searchAliasTokens(value: string) {
  return value.split(/\s+/).filter(Boolean).map(aliasToken);
}

function aliasToken(value: string): SearchToken {
  const token = normalizeExact(value);
  return [token, /[a-z]/.test(token) ? "prefix" : "includes"];
}

function divisionTokens(value: string): SearchToken[] {
  return unique(
    Array.from(value).flatMap((char) => divisionDigits[char] ?? []),
  ).map((digit) => [digit, "includes"]);
}

function toPinyin(value: string) {
  const chars = Array.from(
    simplifier(value.normalize("NFKC")).trim() as string,
  );
  const syllables = chars.map((char) => charPinyin[char]);
  return syllables.every(Boolean) ? syllables.join("") : "";
}
