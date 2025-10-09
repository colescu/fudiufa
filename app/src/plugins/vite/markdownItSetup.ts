import type { MarkdownItAsync } from "markdown-it-async";
import markdownItAttrs from "markdown-it-attrs";
import multimdTable from "markdown-it-multimd-table";
import anchor from "markdown-it-anchor";

import markdownPlugins from "./markdownPlugins";

export function markdownItSetup(md: MarkdownItAsync) {
  md.use(markdownItAttrs);

  md.use(multimdTable, {
    rowspan: true,
    multiline: true,
    colspan: true,
  });

  md.use(anchor, {
    slugify: (s: string) => s.match(/[\u4e00-\u9fff]+/g)?.join("") || "",
    // permalink: anchor.permalink.linkInsideHeader({ symbol: "🔗" }),
  });

  markdownPlugins.forEach((plugin) => {
    md.use(plugin);
  });

  // remove HTML comments
  md.core.ruler.after("inline", "remove_comments", (state) => {
    state.tokens = state.tokens.filter((token) => {
      return !(
        token.type === "html_block" && token.content.trim().startsWith("<!--")
      );
    });
  });

  // stylize binary operator symbols
  const operators = "=≠≈≉";
  const defaultTextRender =
    md.renderer.rules.text || ((tokens, index) => tokens[index]!.content);
  md.renderer.rules.text = (tokens, index, options, env, self) =>
    defaultTextRender(tokens, index, options, env, self).replace(
      new RegExp(`([${operators}])`, "g"),
      `<span class="operator">$1</span>`
    );

  // add target="_blank" rel="noopener noreferrer" to links
  const defaultRender =
    md.renderer.rules.link_open ||
    function (tokens, index, options, _env, self) {
      return self.renderToken(tokens, index, options);
    };
  md.renderer.rules.link_open = function (tokens, index, options, env, self) {
    const targetIndex = tokens[index]!.attrIndex("target");
    if (targetIndex < 0) {
      tokens[index]!.attrPush(["target", "_blank"]);
    } else {
      tokens[index]!.attrs![targetIndex]![1] = "_blank";
    }
    const relIndex = tokens[index]!.attrIndex("rel");
    if (relIndex < 0) {
      tokens[index]!.attrPush(["rel", "noopener noreferrer"]);
    } else {
      tokens[index]!.attrs![relIndex]![1] = "noopener noreferrer";
    }
    return defaultRender(tokens, index, options, env, self);
  };
}
