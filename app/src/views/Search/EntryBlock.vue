<script setup lang="ts">
import { DefaultProps } from "@/components/content/Pronunciation.vue";
import { LangEntry, LANGUAGE_MAP } from "@shared/lang";

import { NSpace, NTag } from "naive-ui";

const { entry, ...rest } = defineProps<
  {
    entry: LangEntry;
  } & DefaultProps
>();
</script>

<template>
  <div class="block">
    <span class="char no-simplify center-text">
      {{ entry.字頭 || "□" }}
    </span>

    <n-space vertical>
      <n-space>
        <n-space align="center">
          <n-tag size="small"> 記錄音 </n-tag>
          <span v-if="entry.記錄讀音">
            <Pronunciation :pronunciation="entry.記錄讀音" v-bind="rest" />
            <sub v-if="entry.層">&nbsp;{{ entry.層 }} </sub>
            <span v-if="entry.訓作"
              >&nbsp;<template v-if="entry.訓作 === '？'">本字存疑</template
              ><template v-else
                >訓作「<span class="char no-simplify">{{ entry.訓作 }}</span
                >」</template
              ></span
            >
          </span>
          <span v-else>無</span>
        </n-space>
        <n-space v-if="entry.推導讀音" align="center">
          <n-tag size="small"> 推導音 </n-tag>
          <span v-if="entry.推導讀音 && entry.推導讀音 !== entry.記錄讀音">
            *<Pronunciation :pronunciation="entry.推導讀音" v-bind="rest" />
          </span>
          <span v-else>同</span>
        </n-space>
      </n-space>

      <n-space v-if="entry.釋義" align="center">
        <n-tag size="small">
          {{ LANGUAGE_MAP[rest.language ?? "FG"]
          }}{{ entry.釋義.includes("～") ? "詞例" : "注釋" }}
        </n-tag>
        <span>{{ entry.釋義 }}</span>
      </n-space>

      <n-space v-if="entry.MC" align="center">
        <n-space align="center">
          <n-tag size="small"> 中古音韻 </n-tag>
          <MCInfo :mc-entry="entry.小韻號!" 反切 />
        </n-space>
      </n-space>

      <!-- FEATURE link to website for comprehensive character info? -->
    </n-space>
  </div>
</template>

<style scoped>
.block {
  display: flex;
  flex-wrap: nowrap;
  align-items: center;
  gap: 1.2em;
  padding: 1em;
  width: 23em;
}

.block > .char {
  font-size: 3em;
  min-width: 1em;
  margin-left: 0.13em;
}

.n-tag {
  margin-right: -0.4em;
}

@media (min-width: 600px) {
  .block {
    margin: 0 1em;
  }
}
</style>
