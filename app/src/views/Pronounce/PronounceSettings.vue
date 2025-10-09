<script setup lang="ts">
import { ref, watch, computed, toRefs } from "vue";
import { useSettingsStore } from "@/stores/settings";
import { useHistoryStore } from "@/stores/history";

import {
  NSpace,
  NRadioGroup,
  NRadioButton,
  NCheckbox,
  NSwitch,
  NButton,
  NIcon,
} from "naive-ui";
import { Sync } from "@vicons/ionicons5";

const settings = useSettingsStore();
const history = useHistoryStore();
const { variant, proto } = toRefs(history.pronounce);

const disable新 = computed(
  () => settings.dictionary.disable.新 || history.pronounce.proto.enable
);
watch(
  disable新,
  (disabled) => {
    if (disabled) {
      history.pronounce.prefer.新 = false;
    }
  },
  { immediate: true }
);

const rotation = ref(0);
const emit = defineEmits(["reset-choices"]);
function resetChoices() {
  emit("reset-choices");
  rotation.value += 360;
}
</script>

<template>
  <n-space align="center" justify="end" style="margin: 0.5em 0">
    <n-space align="end" style="gap: 0.8em" vertical>
      <div>
        <span>顯示方式： </span>
        <n-radio-group
          v-model:value="history.pronounce.style"
          name="ruby"
          size="small"
        >
          <n-radio-button value="interlinear">對照式</n-radio-button>
          <n-radio-button value="ruby">注音式</n-radio-button>
        </n-radio-group>
      </div>

      <div class="row">
        <n-checkbox
          v-model:checked="history.pronounce.prefer.新"
          :disabled="disable新"
        >
          優先新派音
        </n-checkbox>
        <n-checkbox v-model:checked="history.pronounce.prefer.文">
          優先文讀音
        </n-checkbox>
        <n-button @click="resetChoices" text>
          <n-icon
            :component="Sync"
            :style="{
              transform: `rotate(${rotation}deg)`,
              transition: 'transform 0.5s',
            }"
            size="large"
          />
        </n-button>
      </div>

      <n-space align="center">
        <span>未收錄的字使用理論推導音</span>
        <n-switch v-model:value="history.pronounce.includePredicted" />
      </n-space>

      <hr style="width: 12em" />

      <!-- <n-space align="center">
        <span style="margin-right: -0.2em">
          使用變讀
        </span>
        <n-switch v-model:value="variant.enable" />
      </n-space>

      <template v-if="variant.enable">
        <div class="row" style="margin-bottom: -0.5em">
          <n-checkbox
            v-model:checked="variant.settings.ɥon"
          >
            「遠」讀作 <Pronunciation pronunciation="yen3" />
            <Reference to="variations#韻母-yon-yot" @click.stop />
          </n-checkbox>
          <n-checkbox v-model:checked="variant.settings.jau">
            「笑」讀作 <Pronunciation pronunciation="xieu5" />
            <Reference to="variations#韻母-jau" @click.stop />
          </n-checkbox>
          <n-checkbox v-model:checked="variant.settings.jo">
            「茄」讀作 <Pronunciation pronunciation="qyo2" />
            <Reference to="variations#韻母-jo" @click.stop />
          </n-checkbox>
          <n-checkbox v-model:checked="variant.settings.去">
            「去」讀作 <Pronunciation pronunciation="qie5" />
            <Reference to="variations#去類字" @click.stop />
          </n-checkbox>
          <n-checkbox v-model:checked="variant.settings.灰">
            「灰」讀作 <Pronunciation pronunciation="fui1" />
            <Reference to="variations#貝妹灰類字" @click.stop />
          </n-checkbox>
        </div>
      </template> -->
      <!-- TODO 變讀
       選項 蛆 qie 歲 soi 雨 y 身 sən 佛 fiit 分 fiin -->

      <n-space align="center">
        <span style="margin-right: -0.2em">
          模擬墳派音
          <Tooltip marker="?" trigger-style="margin: -0.1em">
            即復原一些晚近的合流。根據中古音反推而得，不完全可靠，目前爲測試階段。僅支持音標。
          </Tooltip>
        </span>
        <n-switch v-model:value="proto.enable" />
      </n-space>

      <template v-if="proto.enable">
        <div class="row" style="margin-bottom: -0.5em">
          <n-checkbox v-model:checked="proto.settings.閉口韻尾">
            閉口韻尾
            <Reference to="variations#閉口韻尾" @click.stop />
          </n-checkbox>
          <n-checkbox v-model:checked="proto.settings.尖團">
            尖團音
            <Reference to="variations#尖團音" @click.stop />
          </n-checkbox>
        </div>

        <div class="row">
          <n-checkbox v-model:checked="proto.settings.陽去">
            陽去
            <Reference to="variations#陽去調" @click.stop />
          </n-checkbox>
          <n-checkbox v-model:checked="proto.settings.分泥來">
            分泥來
            <Reference to="characteristics#泥來不分" @click.stop />
          </n-checkbox>
          <n-checkbox v-model:checked="proto.settings.分疑影">
            分疑影
            <Reference to="characteristics#疑影不分" @click.stop />
          </n-checkbox>
        </div>
      </template>
    </n-space>
  </n-space>
</template>

<style scoped>
.row {
  display: flex;
  align-items: center;
  gap: 0.2em;
}
</style>
