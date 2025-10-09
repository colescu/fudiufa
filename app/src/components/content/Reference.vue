<script setup lang="ts">
import { computed } from "vue";
import { ROUTES_MAP } from "@/router/routes";

const { to } = defineProps<{
  to: string;
}>();

const parsedPath = computed(() => ({
  path: ROUTES_MAP[to.split("#")[0] as keyof typeof ROUTES_MAP],
  hash: "#" + to.split("#")[1],
}));
</script>

<template>
  <RouterLink v-if="$slots.default" :to="parsedPath">
    <slot />
  </RouterLink>

  <sup v-else class="footnote">
    <RouterLink :to="parsedPath">⋆</RouterLink>
  </sup>
</template>

<style scoped>
.footnote {
  margin-left: -0.1em;
  transform: translateY(-0.8em);
}
</style>
