<script setup lang="ts">
import { computed, onBeforeMount, ref } from "vue";
import { getLangQueryUtils } from "@shared/lang";
import { lastUpdateCache } from "@shared/cache";
import { toChineseDate } from "@shared/common/date";

import Fuzhouhua from "@/assets/撫州話.svg";

const counts = computed(() => {
  const { select } = getLangQueryUtils("FG");
  return {
    character:
      new Set(
        select((entry) => entry.字頭 != null && entry.記錄讀音 != null).map(
          (entry) => entry.字頭
        )
      ).size + select((entry) => entry.字頭 == null).length,
    entry: select((entry) => entry.記錄讀音 != null).length,
  };
});

const lastUpdate = ref(__LAST_UPDATE__);
onBeforeMount(() => {
  const lastUpdateBackend = lastUpdateCache.get();
  if (lastUpdateBackend && lastUpdateBackend > new Date(lastUpdate.value)) {
    lastUpdate.value = lastUpdateBackend.toISOString();
  }
});
</script>

<template>
  <div id="home" class="center center-text">
    <Fuzhouhua width="300" />
    <div class="caption">
      歡迎來到苦芋頭嗰
      <Phrase
        :phrase="[
          { character: '撫', pronunciation: 'fu3' },
          { character: '州', pronunciation: 'diu1' },
          { character: '話', pronunciation: 'fa6' },
        ]"
      />
      網站
    </div>
    <br />

    <div>
      收錄撫州話 {{ counts.character }} 字、{{ counts.entry }} 隻讀音<br />
      最後更新：{{ toChineseDate(lastUpdate).replace("日", "號") }}
    </div>
  </div>
</template>

<style scoped lang="scss">
#home {
  flex-direction: column;
  position: absolute;
  top: 47%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.caption {
  font-size: 1.5em;
  margin-top: -0.4em;
  white-space: nowrap;

  :deep(.phrase) {
    margin: auto -0.1em;
    border-bottom: 1px solid currentColor;

    ruby rt {
      font-size: 0.8em;
    }

    button {
      font-size: 0.7em;
      margin-left: -1.1em;
      margin-top: 0.9em;
    }
  }
}
</style>
