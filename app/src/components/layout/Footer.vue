<script setup lang="ts">
import { NPopover } from "naive-ui";
import Weixin from "@/assets/weixin.jpg";
</script>

<template>
  <div id="footer">
    <div>贛 ICP 備 2025071588 號</div>
    <div>
      © 2025 苦芋頭 —
      <n-popover trigger="hover">
        <template #trigger>
          <span>聯繫作者</span>
        </template>
        <div class="center">
          <img :src="Weixin" alt="微信二維碼" width="150" />
        </div>
      </n-popover>
    </div>
  </div>
</template>

<style scoped>
#footer {
  background-color: var(--gray-background);
  color: var(--gray-text);
  border-top: 1px solid var(--border-color);
  font-size: 0.9em;
  padding: 1.2em 0;
  padding-left: 1.5em;
}
</style>
