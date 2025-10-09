<script setup lang="ts">
import { toRef } from "vue";
import { useHistoryStore } from "@/stores/history";
import { charactersCache } from "./cache";

import CharacterBlock from "./CharacterBlock.vue";
import { NSpace, NButton } from "naive-ui";

const history = useHistoryStore();
const character = toRef(history.vocabulary.subtabs, "ci");

const CHARACTERS = (charactersCache.get() as { character: string }[]).map(
  (entry) => entry.character
);

const HISTORY_LIMIT = 10;
const lastCharacters: string[] = [];

function getRandom() {
  let nextCharacter: string;
  while (true) {
    nextCharacter = CHARACTERS[Math.floor(Math.random() * CHARACTERS.length)]!;
    if (
      nextCharacter !== character.value &&
      !lastCharacters.includes(nextCharacter)
    ) {
      character.value = nextCharacter;
      lastCharacters.push(nextCharacter);
      if (lastCharacters.length > HISTORY_LIMIT) {
        lastCharacters.shift();
      }
      break;
    }
  }
}
</script>

<template>
  <n-space vertical align="center">
    <CharacterBlock
      v-if="CHARACTERS.includes(character)"
      :character="character"
    />
    <div v-else style="margin-bottom: 1em">未收錄「{{ character }}」</div>

    <n-button @click="getRandom" type="primary">換一個</n-button>
  </n-space>
</template>

<style scoped></style>
