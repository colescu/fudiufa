<script setup lang="ts">
import { computed, ref } from "vue";
import { useSettingsStore } from "@/stores/settings";
import { getLangQueryUtils, LangEntry } from "@shared/lang";
import { isChineseCharacter } from "@shared/cjk";
import { PronounceProps } from "./types";

import ConstrainedPopover from "@/components/common/ConstrainedPopover.vue";
import EntryInline from "./EntryInline.vue";
import { NRadioGroup, NRadioButton } from "naive-ui";

const settings = useSettingsStore();

const { char, indices, displayStyle, ...rest } = defineProps<
  {
    char: string;
    indices: number[]; // pass entries as indices
    displayStyle: "interlinear" | "ruby";
  } & PronounceProps
>();
const isRuby = computed<boolean>(() => displayStyle === "ruby");

const entryAt = computed(
  () => getLangQueryUtils(rest.language ?? "FG").entryAt
);

const entries = computed<LangEntry[]>(() =>
  indices.map(entryAt.value).filter((entry) => entry != undefined)
);

const choice = defineModel<number | undefined>({ required: true });
const chosenEntry = computed<LangEntry | undefined>(() =>
  choice.value ? entryAt.value(choice.value) : undefined
);
const chosenPronunciation = computed<string | undefined>(
  () => chosenEntry.value?.讀音
);

const showPopover = ref<boolean>(false);

// FEATURE manually set to light tone
</script>

<template>
  <template v-if="!isChineseCharacter(char)">
    <span class="char" style="white-space: pre">{{ char }}</span>
  </template>

  <template v-else>
    <component
      :is="isRuby ? 'ruby' : 'div'"
      class="interlinear"
      :class="{ 'track-both': !isRuby && !rest.proto }"
    >
      <span>
        <ConstrainedPopover v-model:show="showPopover" style="padding: 0.4em 0">
          <template #trigger>
            <component :is="isRuby ? 'rb' : 'span'">
              <span
                class="char no-simplify"
                :class="{
                  clickable: indices.length > 0,
                  highlight:
                    new Set(
                      entries
                        .filter((entry) => entry.層 !== '官')
                        .map((entry) => entry.讀音)
                    ).size > 1,
                }"
                style="display: inline-block; line-height: 1em"
              >
                {{ char }}
              </span>
            </component>
          </template>

          <n-radio-group
            name="radio"
            v-model:value="choice"
            @update:value="showPopover = false"
            @click.stop
          >
            <div class="vertical-radio-buttons">
              <n-radio-button
                v-for="index of indices"
                :key="index"
                :value="index"
              >
                <EntryInline :entry="entryAt(index)!" v-bind="rest" />
              </n-radio-button>
            </div>
          </n-radio-group>
        </ConstrainedPopover>
      </span>

      <template v-if="!isRuby">
        <template v-if="chosenPronunciation != null">
          <span
            v-if="
              (settings.format === 'pinyin' || settings.displayBoth) &&
              (!rest.proto || language !== 'FG')
            "
          >
            <Pronunciation
              :pronunciation="chosenPronunciation"
              format="pinyin"
              v-bind="rest"
              :mc-info="chosenEntry?.MC"
            />
          </span>
          <span v-if="settings.format === 'ipaStrict' || settings.displayBoth">
            <Pronunciation
              :pronunciation="chosenPronunciation"
              format="ipaStrict"
              v-bind="rest"
              :mc-info="chosenEntry?.MC"
            />
          </span>
        </template>
        <template v-else>
          <span class="gray">無</span>
        </template>
      </template>

      <template v-else>
        <template v-if="chosenPronunciation != null">
          <rp>(</rp>
          <rt>
            <Pronunciation
              :pronunciation="chosenPronunciation"
              v-bind="rest"
              :mc-info="chosenEntry?.MC"
            />
          </rt>
          <rp>)</rp>
        </template>
      </template>
    </component>
  </template>
</template>

<style scoped lang="scss">
.interlinear {
  margin: 0 0.2em;
}

div.interlinear {
  display: inline-block;
  position: relative;
  vertical-align: top;
  margin-bottom: 0.8em;

  > span {
    display: block;
    margin-bottom: 0.1em;

    &:nth-child(3) {
      margin-top: -0.1em;
    }
  }
}

ruby rt {
  margin-top: 1em;
  margin-bottom: 0;
  font-size: 1em;
}

.vertical-radio-buttons {
  display: flex;
  flex-direction: column;

  .n-radio-button {
    border: none;
    padding: 0 0.6em;
  }
}
</style>
