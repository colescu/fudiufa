<script setup lang="ts">
import { nextTick, ref, toRefs, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useHistoryStore } from "../../stores/history";

import RandomCharacter from "./Character/RandomCharacter.vue";
import Sentences from "./content/sentences.md";
import Poems from "./content/poems.md";
import Articles from "./content/articles.md";
import { NTabs, NTabPane } from "naive-ui";

const route = useRoute();
const router = useRouter();
const history = useHistoryStore();

// bind tab and query with url

const { tab, subtabs } = toRefs(history.vocabulary);

function updateUrl(isReplace: boolean) {
  const targetRoute = {
    name: "Vocabulary",
    params: {
      tab: tab.value,
      subtab: (subtabs.value as any)[tab.value] as string | undefined,
    },
    query: tab.value === "fongnienci" ? { ci: subtabs.value.ci } : undefined,
  };

  if (isReplace) {
    router.replace({ ...targetRoute, hash: route.hash });
  } else {
    router.push(targetRoute);
  }
}

const SUBTABS_MAP = {
  diun: ["diji", "xici", "qiun"],
} as const;

const syncingFromRoute = ref(false);
watch(
  () => [route.params, route.query],
  ([params, query]) => {
    if (!params || !query) return;

    const newTab = params.tab as string | undefined;
    if (newTab && ["fongnienci", "tehsehcifi", "diun"].includes(newTab)) {
      tab.value = newTab;
    }

    const newSubtab = params.subtab as string | undefined;
    if (newSubtab && tab.value in SUBTABS_MAP) {
      const currentTab = tab.value as keyof typeof SUBTABS_MAP;
      if ((SUBTABS_MAP[currentTab] as readonly string[]).includes(newSubtab)) {
        subtabs.value[currentTab] = newSubtab;
      }
    }

    if (typeof query.ci === "string") {
      history.vocabulary.subtabs.ci = query.ci;
    }

    updateUrl(true);
    nextTick(() => (syncingFromRoute.value = false));
  },
  { immediate: true, deep: true }
);
watch(
  [tab, subtabs],
  () => {
    if (syncingFromRoute.value) return;
    updateUrl(false);
  },
  { deep: true }
);
</script>

<template>
  <div>
    <n-tabs
      v-model:value="tab"
      type="line"
      justify-content="center"
      size="large"
      animated
    >
      <n-tab-pane name="fongnienci" tab="方言字">
        <RandomCharacter />
      </n-tab-pane>

      <n-tab-pane name="tehsehcifi" tab="特色詞彙">
        <span class="center">尚未開發，敬請期待！</span>
      </n-tab-pane>

      <n-tab-pane
        name="diun"
        tab="例文"
        class="corpus"
        display-directive="show:lazy"
      >
        <n-tabs
          v-model:value="subtabs.diun"
          type="segment"
          size="small"
          animated
        >
          <n-tab-pane name="diji" tab="例句" display-directive="show:lazy">
            <Sentences />
          </n-tab-pane>
          <n-tab-pane name="xici" tab="詩詞" display-directive="show:lazy">
            <Poems />
          </n-tab-pane>
          <n-tab-pane
            name="qiun"
            tab="奇文"
            display-directive="show:lazy"
            class="articles"
          >
            <Articles />
          </n-tab-pane>
        </n-tabs>

        <Teleport to="#help"> 該板塊僅爲示例，歡迎提供想法或意見！ </Teleport>
      </n-tab-pane>
    </n-tabs>
  </div>
</template>

<style scoped lang="scss">
.corpus {
  :deep(ruby) {
    .pinyin,
    .ipa {
      font-size: 0.85rem !important;
    }
  }
}

:deep(.n-tabs-rail) {
  margin: 0 auto;
  max-width: 15em;
}
</style>
