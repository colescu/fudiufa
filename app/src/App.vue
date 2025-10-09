<script setup lang="ts">
import { computed, onBeforeMount, ref } from "vue";
import { useRoute } from "vue-router";
import { useUpdates } from "./composables/useUpdates";
import { trackHasBoth, trackHasPhrase } from "./composables/useTrack";

import SimplifiedConverter from "./components/wrapper/SimplifiedConverter.vue";
import NavBar from "./components/layout/NavBar.vue";
import Footer from "./components/layout/Footer.vue";
import Float from "./views/Settings/FloatPanel.vue";
import {
  NLayout,
  NLayoutHeader,
  NLayoutContent,
  NLayoutFooter,
  NModal,
} from "naive-ui";

const show = ref(true);
const { currentUpdate, next: nextUpdate } = useUpdates();
onBeforeMount(async () => await nextUpdate());

const route = useRoute();
const hideNavbar = computed(() => !!route.meta.hideNavbar);

trackHasBoth();
trackHasPhrase();
</script>

<template>
  <SimplifiedConverter>
    <n-layout>
      <n-layout-header v-if="!hideNavbar">
        <NavBar />
      </n-layout-header>

      <n-layout-content>
        <RouterView v-slot="{ Component }">
          <Transition name="fade" mode="out-in">
            <component :is="Component" />
          </Transition>
        </RouterView>
      </n-layout-content>

      <n-layout-footer v-if="!hideNavbar" position="absolute">
        <Footer />
      </n-layout-footer>
    </n-layout>

    <Float />

    <n-modal
      v-if="currentUpdate"
      v-model:show="show"
      @update:show="nextUpdate"
      preset="card"
      title="更新日誌"
      style="width: 22em"
    >
      <div>版本 {{ currentUpdate.version }} ({{ currentUpdate.date }})</div>
      <component :is="currentUpdate.component" />
    </n-modal>
  </SimplifiedConverter>
</template>

<style scoped lang="scss">
.n-layout {
  min-width: 360px;
  min-height: 100vh;
}

.n-layout-content {
  padding-top: 5em;
  padding-bottom: 9em;
  width: 65%;
  min-width: 540px;
  margin: 0 auto;
  overflow: visible;

  @media (max-width: 600px) {
    width: 90%;
    min-width: 0;
  }
}

.fade {
  &-enter-active,
  &-leave-active {
    transition: opacity 0.1s ease;
  }

  &-enter-from,
  &-leave-to {
    opacity: 0;
  }

  &-enter-to,
  &-leave-from {
    opacity: 1;
  }
}
</style>
