<script setup lang="ts">
import { computed } from "vue";
import { useSettingsStore } from "@/stores/settings";

import Character from "./Character.vue";
import Pronunciation, { type DefaultProps } from "./Pronunciation.vue";

export type RubyData = {
  character: string;
  pronunciation: string;
};

const { character, pronunciation, ...rest } = defineProps<
  RubyData & DefaultProps
>();

const settings = useSettingsStore();
const isTranslate = computed(
  () => settings.format === "ipaStrict" && settings.ipaToneNotation === "number"
);
</script>

<template>
  <ruby :class="{ translate: isTranslate }">
    <rb>
      <Character
        :character="character"
        :hint="pronunciation || undefined"
        :language="rest.language"
      />
    </rb>
    <template v-if="pronunciation">
      <rp>(</rp>
      <rt>
        <Pronunciation :pronunciation="pronunciation" v-bind="rest" />
      </rt>
      <rp>)</rp>
    </template>
  </ruby>
</template>

<style scoped>
ruby rt {
  margin-top: 0.4em;
}

ruby.translate rt span.ipa {
  display: inline-block;
  transform: translateX(0.1em);
}
</style>
