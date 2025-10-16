<script setup lang="ts">
import { onMounted, onUnmounted, ref } from "vue";
import { useRoute } from "vue-router";
import { useSettingsStore } from "@/stores/settings";
import { hasBoth, hasPhrase } from "@/composables/useTrack";

import FloatPopover from "@/components/common/FloatPopover.vue";
import {
  NSpace,
  NFloatButton,
  NIcon,
  NTag,
  NSwitch,
  NRadioGroup,
  NRadioButton,
  NButton,
  NSlider,
} from "naive-ui";
import {
  SettingsOutline,
  HelpOutline,
  ChevronForwardOutline,
} from "@vicons/ionicons5";
import { ArrowBarToUp } from "@vicons/tabler";

const route = useRoute();
const settings = useSettingsStore();

const helpDefault = `
  點擊注音可聽單字發音。<br />
  點擊<span class="char">例字</span>可查看中古音韻。<br />
  點擊中古音韻可查看各方言推導音。
`;
const helpHtml = ref<string>("");
function getHelpHtml() {
  const helpContainer = document.getElementById("help");
  const teleported = helpContainer?.innerHTML.trim();
  helpHtml.value = teleported
    ? teleported.endsWith("default")
      ? teleported.slice(0, -7) + helpDefault
      : teleported
    : helpDefault;
}

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: "smooth" });
}

const showBackTop = ref<boolean>(false);
function handleScroll() {
  showBackTop.value = window.scrollY > 100;
}
onMounted(() => window.addEventListener("scroll", handleScroll));
onUnmounted(() => window.removeEventListener("scroll", handleScroll));
</script>

<template>
  <div id="float">
    <n-float-button
      v-if="showBackTop"
      :right="66"
      :bottom="66"
      @click="scrollToTop"
    >
      <n-icon :component="ArrowBarToUp" />
    </n-float-button>

    <n-float-button
      :right="66"
      :bottom="16"
      @click="settings.isSimplified = !settings.isSimplified"
    >
      {{ settings.isSimplified ? "简" : "繁" }}
    </n-float-button>

    <FloatPopover
      v-if="route.path !== '/'"
      :icon="HelpOutline"
      :icon-size="40"
      :right="16"
      :bottom="66"
      :on-update-show="getHelpHtml"
    >
      <div v-html="helpHtml" />
    </FloatPopover>

    <FloatPopover
      :icon="SettingsOutline"
      :icon-size="40"
      :right="16"
      :bottom="16"
      style="min-width: 19.1em"
    >
      <n-space vertical style="margin: 0.5em 0">
        <n-space align="center">
          <n-tag>注音</n-tag>
          <n-radio-group
            v-model:value="settings.format"
            name="format"
            size="small"
          >
            <n-radio-button value="pinyin">
              拼音
              <Pronunciation pronunciation="qiah7" format="pinyin" no-audio />
            </n-radio-button>
            <n-radio-button value="ipaStrict">
              音標&thinsp;
              <Pronunciation
                pronunciation="qiah7"
                format="ipaStrict"
                no-audio
              />
            </n-radio-button>
          </n-radio-group>
        </n-space>

        <n-space v-if="hasBoth" align="center">
          <n-tag style="visibility: hidden">注音</n-tag>
          同時顯示（部分支持）
          <n-switch
            v-model:value="settings.displayBoth"
            style="margin-left: -0.5em"
          />
        </n-space>

        <n-space align="center">
          <n-tag>拼音聲調</n-tag>
          <n-radio-group
            v-model:value="settings.pinyinToneNotation"
            name="pinyinToneNotation"
            size="small"
          >
            <n-radio-button value="ordinal">
              調號 <span class="pinyin">a3</span>
            </n-radio-button>
            <n-radio-button value="diacritic">
              变音符 <span class="pinyin">â</span>
            </n-radio-button>
          </n-radio-group>
        </n-space>

        <n-space align="center">
          <n-tag>音標聲調</n-tag>
          <n-radio-group
            v-model:value="settings.ipaToneNotation"
            name="ipaToneNotation"
            size="small"
          >
            <n-radio-button value="letter">
              折綫 <span class="ipa">a˦˥</span>
            </n-radio-button>
            <n-radio-button value="number">
              數字 <span class="ipa">a⁴⁵</span>
            </n-radio-button>
          </n-radio-group>
        </n-space>

        <n-space v-if="hasPhrase" align="center">
          <n-tag>播放速度</n-tag>
          <n-slider
            v-model:value="settings.playSpeed"
            :step="100"
            :max="1000"
            :min="300"
            :format-tooltip="(val) => val / 1000 + ' 秒/字'"
            style="width: 12em"
          />
        </n-space>
      </n-space>

      <n-space align="center" justify="end" style="margin-bottom: 0.1em">
        <RouterLink to="/setdi">
          <n-button icon-placement="right" text>
            <template #icon>
              <n-icon
                :component="ChevronForwardOutline"
                size="large"
                style="margin-left: 0.2em"
              />
            </template>
            更多設置
          </n-button>
        </RouterLink>
      </n-space>
    </FloatPopover>
  </div>
</template>

<style scoped>
#float :deep(.n-float-button) {
  z-index: 10000;
}
</style>
