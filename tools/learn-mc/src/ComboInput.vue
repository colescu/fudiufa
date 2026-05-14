<script setup lang="ts">
import { ChevronDown, ChevronUp } from "@vicons/ionicons5";
import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { normalizeText } from "./aliases";

const props = defineProps<{
  modelValue: string;
  options: readonly string[];
  disabled?: boolean;
  state?: "" | "ok" | "bad";
  placeholder?: string;
  filter?: (option: string, query: string) => boolean;
}>();

const emit = defineEmits<{ "update:modelValue": [value: string] }>();
const root = ref<HTMLElement | null>(null);
const open = ref(false);
const activeIndex = ref(0);

const matches = computed(() => {
  const value = props.modelValue.trim();
  return value && !props.options.includes(value)
    ? props.options.filter((item) => matchesOption(item, value))
    : props.options;
});

watch(matches, () => {
  activeIndex.value = 0;
});

watch(open, (value) => {
  if (value) activeIndex.value = 0;
});

onMounted(() => document.addEventListener("pointerdown", closeOutside));
onBeforeUnmount(() => document.removeEventListener("pointerdown", closeOutside));

function choose(value: string) {
  emit("update:modelValue", value);
  open.value = false;
}

function commit() {
  const value = props.modelValue.trim();
  const exact = props.options.find((option) => normalizeText(option) === normalizeText(value));
  const choice = open.value ? matches.value[activeIndex.value] : exact ?? matches.value[0];
  if (choice) choose(choice);
  else open.value = false;
}

function moveActive(step: 1 | -1) {
  if (!open.value) {
    open.value = true;
    return;
  }
  if (!matches.value.length) return;
  activeIndex.value = (activeIndex.value + step + matches.value.length) % matches.value.length;
}

function matchesOption(option: string, query: string) {
  return props.filter
    ? props.filter(option, query)
    : normalizeText(option).includes(normalizeText(query));
}

function closeOutside(event: PointerEvent) {
  if (!root.value?.contains(event.target as Node)) open.value = false;
}

function closeForTab() {
  open.value = false;
}
</script>

<template>
  <div ref="root" class="combo" :class="state">
    <input
      :value="modelValue"
      :disabled="disabled"
      :placeholder="placeholder"
      autocomplete="off"
      @input="emit('update:modelValue', ($event.target as HTMLInputElement).value); open = true"
      @keydown.down.prevent="moveActive(1)"
      @keydown.up.prevent="moveActive(-1)"
      @keydown.enter.prevent="commit"
      @keydown.tab="closeForTab"
    />
    <button
      type="button"
      :disabled="disabled"
      aria-label="Show options"
      :aria-expanded="open"
      tabindex="-1"
      @click="open = !open"
    >
      <component :is="open ? ChevronUp : ChevronDown" class="combo-icon" aria-hidden="true" />
    </button>
    <div v-if="open && matches.length" class="menu">
      <button
        v-for="(item, index) in matches"
        :key="item"
        type="button"
        :class="{ active: index === activeIndex }"
        @mouseenter="activeIndex = index"
        @click="choose(item)"
      >
        {{ item }}
      </button>
    </div>
  </div>
</template>
