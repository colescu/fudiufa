<script setup lang="ts">
import { computed } from "vue";
import MarkdownIt from "markdown-it";
import { charactersCache } from "./cache";
import { CharacterData } from "./types";

import { NCard, NSpace, NTag } from "naive-ui";

const { character } = defineProps<{ character: string }>();

const data = computed<CharacterData | undefined>(() => {
  const CHARACTERS_DATA = charactersCache.get();
  for (const characterData of CHARACTERS_DATA) {
    if (characterData.character === character) {
      return characterData;
    }
  }
});

// Ad hoc parsing
const md = new MarkdownIt();
function parseMarkdown(text: string) {
  const html = md
    .renderInline(text)
    .replace(/<a /g, '<a target="_blank" rel="noopener noreferrer" ');

  const regex = /\[([^\|]+)\|([^\]#]+#([^\]]+))?\]/g;
  const nodes: Array<any> = [];
  let lastIndex = 0;
  let match;

  while ((match = regex.exec(html)) !== null) {
    if (match.index > lastIndex) {
      nodes.push({
        type: "span",
        html: html.slice(lastIndex, match.index),
      });
    }

    // [text|link#anchor] -> <Reference to="link#anchor">text</Reference>
    if (match[1] && match[2]) {
      nodes.push({
        type: "Reference",
        props: { to: match[2] },
        text: match[1],
      });
    }

    lastIndex = regex.lastIndex;
  }

  if (lastIndex < html.length) {
    nodes.push({
      type: "span",
      html: html.slice(lastIndex),
    });
  }

  return nodes;
}

const renderedComment = computed(() =>
  parseMarkdown(data.value?.comment ?? "")
);

const renderedExamples = computed(
  () =>
    data.value?.example.split("、").map((text) =>
      text.split("|").map((item) => ({
        character: [...item][0],
        pronunciation: [...item].slice(1).join(""),
      }))
    ) ?? []
);

function openZiTools() {
  window.open(`https://zi.tools/zi/${character}`, "_blank");
}
</script>

<template>
  <n-card v-if="data">
    <div class="block">
      <div @click="openZiTools" class="char clickable no-simplify">
        {{ data.character }}
      </div>

      <n-space style="font-size: 1.5em; margin-top: 0.9em" vertical>
        <n-space align="center">
          <DoublePronunciation :pronunciation="data.pronunciation" />
        </n-space>
        <n-space align="center" style="white-space: nowrap">
          {{ data.meaning }}
        </n-space>
      </n-space>
    </div>

    <n-space vertical>
      <div>
        <n-tag size="small" style="margin-right: 1em">普通話讀音</n-tag>
        <template v-for="(pronunciation, index) of data.mandarin.split(',')">
          <Pronunciation :pronunciation="pronunciation" language="PM" />
          <template v-if="index !== data.mandarin.split(',').length - 1"
            >&nbsp;、</template
          >
        </template>
      </div>

      <div v-if="data.example" class="float-tagged" style="margin-top: -0.7em">
        <n-tag
          size="small"
          style="
            float: inline-start;
            margin-right: 1em;
            transform: translateX(-0.3em) translateY(1.8em);
          "
        >
          示例
        </n-tag>
        <template v-for="(phrase, index) of renderedExamples">
          <Phrase :phrase="phrase" />
          <template v-if="index !== renderedExamples.length - 1">、 </template>
        </template>
      </div>

      <MarkdownWrapper v-if="data.comment" class="float-tagged">
        <n-tag
          size="small"
          style="
            float: inline-start;
            margin-right: 0.5em;
            transform: translateX(-0.3em) translateY(0.3em);
          "
        >
          注釋
        </n-tag>
        <template v-for="(node, i) in renderedComment" :key="i">
          <component
            v-if="node.type !== 'span'"
            :is="node.type"
            v-bind="node.props"
          >
            {{ node.text }}
          </component>
          <span v-else v-html="node.html"></span>
        </template>
      </MarkdownWrapper>
    </n-space>
  </n-card>
</template>

<style scoped>
.n-card {
  display: flex;
  justify-content: center;
  margin: 1.5em auto;
  width: 20em;
}

.block {
  display: flex;
  justify-content: left;
  align-items: start;
  gap: 1.5em;
  margin-top: -1em;
}

.char {
  font-size: 5em;
  min-width: 1em;
}

.markdown-wrapper {
  line-height: 2;
}

.float-tagged {
  margin-left: 0.3em;
}
</style>
