<script setup lang="ts">
import {
  nextTick,
  ref,
  toRef,
  toRefs,
  watch,
  computed,
  type Component,
} from "vue";
import { useRoute, useRouter } from "vue-router";
import { useHistoryStore } from "../../stores/history";
import { PredictFormUtils } from "@/views/Phonology/Predict/form";
import { LANGUAGE_MAP, LANGUAGES } from "@shared/lang";
import { fromEntriesConst } from "@shared/common/object";

import Initial from "./content/phonetics/initial.md";
import Final from "./content/phonetics/final.md";
import Tone from "./content/phonetics/tone.md";
import Variations from "./content/phonetics/variations.md";
import RhymeTable from "@/views/Phonology/RhymeTable/RhymeTableTab.vue";
import DiachronicTable from "@/views/Phonology/DiachronicTable/DiachronicTableTab.vue";
import Characteristics from "./content/phonology/characteristics.md";
import Strata from "./content/phonology/strata.md";
import Predict from "@/views/Phonology/Predict/PredictTab.vue";
import { NTabs, NTabPane, NPopselect, NIcon } from "naive-ui";
import {
  ChevronDown as Expand,
  ChevronUp as Collapse,
} from "@vicons/ionicons5";
import { useSettingsStore } from "@/stores/settings";

const settings = useSettingsStore();

const comparedLanguages = computed(() =>
  settings.languages.filter((language) => language !== "FG")
);
const languageOptions = computed(() =>
  comparedLanguages.value.map((language) => ({
    value: language,
    label: LANGUAGE_MAP[language],
  }))
);
const modules = import.meta.glob(`./content/compare/*.md`, {
  eager: true,
}) as Record<string, { default: Component }>;
const languageComponents = fromEntriesConst(
  [...LANGUAGES]
    .filter((language) => language !== "FG")
    .map((language) => [
      language,
      modules[`./content/compare/${language}.md`]!.default,
    ])
);

const route = useRoute();
const router = useRouter();
const history = useHistoryStore();

const showPopover = ref<boolean>(false);
document.addEventListener(
  "click",
  (e) => {
    const target = e.target as HTMLElement;
    if (!!!target.closest("#bigau-select")) {
      showPopover.value = false;
    } else if (route.params.subtab === "bigau") {
      showPopover.value = !showPopover.value;
    }
  },
  { capture: true }
);

// bind tab and query with url

const { tab, subtabs } = toRefs(history.phonology);
const form = toRef(history.phonology.predict, "form");

function updateUrl(isReplace: boolean) {
  const targetRoute = {
    name: "Phonology",
    params: {
      tab: tab.value,
      subtab: (subtabs.value as any)[tab.value] as string | undefined,
    },
    query: {
      ninien:
        tab.value === "nienjiu" && subtabs.value[tab.value] === "bigau"
          ? LANGUAGE_MAP[subtabs.value.bigau]
          : undefined,
      biaudan:
        tab.value === "tuitauqi" && form.value != null
          ? JSON.stringify(form.value)
          : undefined,
    },
  };

  if (isReplace) {
    router.replace({ ...targetRoute, hash: route.hash });
  } else {
    router.push(targetRoute);
  }
}

const SUBTABS_MAP = {
  sangyntiau: ["sangmu", "ynmu", "sangtiau", "bienti", "yntu"],
  nienjiu: ["gujintu", "tehdin", "cenci", "bigau"],
} as const;

const syncingFromRoute = ref(false);
watch(
  () => [route.params, route.query],
  ([params, query]) => {
    if (!params || !query) return;

    syncingFromRoute.value = true;

    const newTab = params.tab as string | undefined;
    if (newTab && ["sangyntiau", "nienjiu", "tuitauqi"].includes(newTab)) {
      tab.value = newTab;
    }

    const newSubtab = params.subtab as string | undefined;
    if (newSubtab && tab.value in SUBTABS_MAP) {
      const currentTab = tab.value as keyof typeof SUBTABS_MAP;
      if ((SUBTABS_MAP[currentTab] as readonly string[]).includes(newSubtab)) {
        subtabs.value[currentTab] = newSubtab;
      }
    }

    if (typeof query.ninien === "string") {
      for (const { value, label } of languageOptions.value) {
        if (label === query.ninien) {
          subtabs.value.bigau = value;
          break;
        }
      }
    }

    if (typeof query.biaudan === "string") {
      try {
        const queryForm = JSON.parse(query.biaudan);
        if (PredictFormUtils.checkForm(queryForm)) {
          form.value = queryForm;
        }
        throw Error();
      } catch {}
    }

    updateUrl(true);
    nextTick(() => (syncingFromRoute.value = false));
  },
  { immediate: true, deep: true }
);
watch(
  [tab, subtabs, form],
  () => {
    if (syncingFromRoute.value) return;
    updateUrl(false);
  },
  { deep: true }
);
</script>

<template>
  <n-tabs
    v-model:value="tab"
    type="line"
    justify-content="center"
    size="large"
    animated
  >
    <n-tab-pane
      id="phonetics"
      name="sangyntiau"
      tab="聲韻調"
      display-directive="show:lazy"
    >
      <n-tabs
        v-model:value="subtabs.sangyntiau"
        type="segment"
        justify-content="center"
        size="small"
        animated
      >
        <n-tab-pane name="sangmu" tab="聲母">
          <Initial />
        </n-tab-pane>
        <n-tab-pane name="ynmu" tab="韻母">
          <Final />
        </n-tab-pane>
        <n-tab-pane name="sangtiau" tab="聲調">
          <Tone />
        </n-tab-pane>
        <n-tab-pane name="yntu" tab="韻圖">
          <RhymeTable />
        </n-tab-pane>
        <n-tab-pane name="bienti" tab="變體" display-directive="show:lazy">
          <Variations />
        </n-tab-pane>
      </n-tabs>
    </n-tab-pane>

    <n-tab-pane
      id="phonology"
      name="nienjiu"
      tab="音韻研究"
      display-directive="show:lazy"
    >
      <n-tabs
        v-model:value="subtabs.nienjiu"
        type="segment"
        size="small"
        animated
      >
        <n-tab-pane name="gujintu" tab="古今對照">
          <DiachronicTable />
        </n-tab-pane>
        <n-tab-pane name="tehdin" tab="音韻特徵" display-directive="show:lazy">
          <Characteristics />
        </n-tab-pane>
        <n-tab-pane name="cenci" tab="文白新老" display-directive="show:lazy">
          <Strata />
        </n-tab-pane>
        <n-tab-pane name="bigau" display-directive="show:lazy">
          <template #tab>
            <span id="bigau-select" style="padding: 0 0.8em">
              比較<n-popselect
                trigger="manual"
                v-model:show="showPopover"
                v-model:value="subtabs.bigau"
                :options="languageOptions"
              >
                <span>
                  {{ LANGUAGE_MAP[subtabs.bigau] }}
                  <n-icon
                    :component="showPopover ? Collapse : Expand"
                    style="vertical-align: -2px"
                  />
                </span>
              </n-popselect>
            </span>
          </template>
          <component :is="languageComponents[subtabs.bigau]" />
        </n-tab-pane>
      </n-tabs>
    </n-tab-pane>

    <n-tab-pane name="tuitauqi" tab="推導器">
      <Predict />
    </n-tab-pane>
  </n-tabs>
</template>

<style scoped>
:deep(.n-tabs-rail) {
  margin: 0 auto;
  max-width: 25em;
}
</style>
