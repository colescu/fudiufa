import type MarkdownIt from "markdown-it";
import type Token from "markdown-it/lib/token.mjs";

export type DoubleMode =
  | "pinyin"
  | "ipaStrict"
  | "and"
  | "xor"
  | "left"
  | "right";

function createComponent(
  name: string,
  props: Record<string, string | number | null | undefined>
): string {
  const attrs = Object.entries(props)
    .filter(([_, value]) => value != null)
    .map(([prop, value]) => `:${prop}='${JSON.stringify(value)}'`)
    .join(" ");
  return `<${name} ${attrs} />`;
}

function createInlinePlugin(
  tokenName: string,
  pattern: RegExp,
  metaMapper: string[] | ((match: string[]) => Record<string, any>),
  beforeRule: string = "text",
  renderRule: (meta: any) => string = (meta) => createComponent(tokenName, meta)
) {
  function tokenize(state: any, silent: boolean): boolean {
    const pos = state.pos as number;
    const src = state.src.slice(pos) as string;
    const match = pattern.exec(src);
    if (!match) return false;

    if (!silent) {
      const meta =
        typeof metaMapper === "function"
          ? metaMapper(match.slice(1))
          : Object.fromEntries(
              metaMapper.map((field, index) => [field, match[index + 1]])
            );

      const token = state.push(tokenName, "", 0);
      token.meta = meta;
    }

    state.pos += match[0].length;
    return true;
  }

  function plugin(md: MarkdownIt) {
    md.inline.ruler.before(beforeRule, tokenName, tokenize);
    md.renderer.rules[tokenName] = (tokens: Token[], index: number): string =>
      renderRule(tokens[index]!.meta);
  }

  return plugin;
}

function createDouble(pinyin: string, ipa: string, mode?: DoubleMode): string {
  return `<Double :mode='${JSON.stringify(mode)}'>
    <template #pinyin>${pinyin}</template>
    <template #ipa>${ipa}</template>
  </Double>`;
}

const markdownPlugins = [
  // :p(a) -> <span class="pinyin">a</span>
  createInlinePlugin(
    "Pinyin",
    /^\:p\(([^)\s]+)\)/,
    ["text"],
    undefined,
    ({ text }) => `<span class="pinyin">${text}</span>`
  ),
  // :i(a) -> <span class="ipa">a</span>
  createInlinePlugin(
    "Ipa",
    /^\:i\(([^)\s]+)\)/,
    ["text"],
    undefined,
    ({ text }) => `<span class="ipa">${text}</span>`
  ),
  // :is(a) -> :i(a) with [] if pinyin
  createInlinePlugin(
    "IpaSlash",
    /^\:is\(([^)\s]+)\)/,
    ["text"],
    undefined,
    ({ text }) => createDouble("", `<span class="ipa">${text}</span>`, "right")
  ),
  // :marker(a=b) -> Double Part
  ...(
    [
      ["", undefined],
      ["&", "and"],
      ["x", "xor"],
      ["l", "left"],
      ["r", "right"],
    ] as const
  ).map(([marker, mode]) =>
    createInlinePlugin(
      `Part_${mode}`,
      new RegExp(`^:${marker}\\(([^)\\s]+)=([^)\\s]+)\\)`),
      ["pinyin", "ipa"],
      undefined,
      ({ pinyin, ipa }) =>
        createDouble(
          `<span class="pinyin">${pinyin}</span>`,
          `<span class="ipa">${ipa}</span>`,
          mode
        )
    )
  ),
  // {L:a}(mode) -> DoublePronunciation
  createInlinePlugin(
    "DoublePronunciation",
    /^\{(?:(\w+):)?([^}]+)\}\(([^)]+)\)/,
    ["language", "pronunciation", "mode"]
  ),
  // {L:a}D -> {L:a}()
  createInlinePlugin(
    "DefaultDoublePronunciation",
    /^\{(?:(\w+):)?([^}]+)\}D/,
    ["language", "pronunciation"],
    "DoublePronunciation",
    ({ language, pronunciation }) =>
      createComponent("DoublePronunciation", {
        language,
        pronunciation,
        mode: undefined,
      })
  ),
  // {L:a} -> {L:a}(xor)
  createInlinePlugin(
    "XorPronunciation",
    /^\{(?:(\w+):)?([A-Za-z][^}→]+)\}(?![()}D])/,
    ["language", "pronunciation"],
    "DefaultDoublePronunciation",
    ({ language, pronunciation }) =>
      createComponent("DoublePronunciation", {
        language,
        pronunciation,
        mode: "xor",
      })
  ),
  // {L:a→b} -> ...
  createInlinePlugin(
    "OldNewPronunciation",
    /^\{(?:(\w+):)?([A-Za-z][^}]+)→([A-Za-z][^}]+)\}(?![()}D])/,
    ["language", "oldPronunciation", "newPronunciation"],
    "XorPronunciation",
    ({ language, oldPronunciation, newPronunciation }) =>
      createDouble(
        createComponent("DoublePronunciation", {
          language,
          pronunciation: oldPronunciation,
          mode: "and",
        }) +
          " → [" +
          createComponent("DoublePronunciation", {
            language,
            pronunciation: newPronunciation,
            mode: "ipaStrict",
          }) +
          "]",
        createComponent("DoublePronunciation", {
          language,
          pronunciation: oldPronunciation,
          mode: "ipaStrict",
        }) +
          " → " +
          createComponent("DoublePronunciation", {
            language,
            pronunciation: newPronunciation,
            mode: "ipaStrict",
          }),
        "xor"
      )
  ),
  // [a] -> <Character character="a" />
  createInlinePlugin(
    "Character",
    /^\[([\u4e00-\u9fff\u{20000}-\u{2a6df}□][^\]]*)\]/u,
    ["character"],
    "image"
  ),
  // [a]{L:b} -> <CharacterRuby character="a" pronunciation="b" language="L" />
  createInlinePlugin(
    "CharacterRuby",
    /^\[([^\]]+)\]\{(?:(\w+):)?([^}]+)\}/,
    ["character", "language", "pronunciation"],
    "Character"
  ),
  // @P(L:[a1]{b1}...[an]{bn}) ->
  // <Phrase :phrase='[{character: "a1", pronunciation: "b1"}, ...]' language="L" />
  createInlinePlugin(
    "Phrase",
    /^@P\((?:(\w+):)?([^)]+)\)/,
    (match: string[]) => {
      const [language, content, _] = match;
      return {
        language,
        phrase: [...content!.matchAll(/\[([^\]]+)\]\{([^}]*)\}/g)].map((m) => ({
          character: m[1],
          pronunciation: m[2],
        })),
      };
    },
    "CharacterRuby"
  ),
];

export default markdownPlugins;
