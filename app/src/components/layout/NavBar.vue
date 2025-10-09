<script setup lang="ts">
import { NSpace, NButton, NIcon } from "naive-ui";
import { LogoGithub } from "@vicons/ionicons5";
import FuIcon from "@/assets/撫.svg";
</script>

<template>
  <div id="navbar">
    <div class="icon">
      <RouterLink to="/">
        <n-button :focusable="false" text icon>
          <FuIcon style="width: 2.5em" />
        </n-button>
      </RouterLink>
    </div>

    <n-space align="center" :wrap="false">
      <RouterLink to="/gaiseu">
        <n-button :focusable="false" text>介紹</n-button>
      </RouterLink>
      <RouterLink to="/inyn">
        <n-button :focusable="false" text>音韻</n-button>
      </RouterLink>
      <RouterLink to="/ifi">
        <n-button :focusable="false" text>語彙</n-button>
      </RouterLink>
      <RouterLink to="/caci">
        <n-button :focusable="false" text>查字</n-button>
      </RouterLink>
      <RouterLink to="/duin">
        <n-button :focusable="false" text>注音</n-button>
      </RouterLink>
    </n-space>

    <div class="icon">
      <n-button
        tag="a"
        href="https://github.com/colescu/fudiufa"
        target="_blank"
        rel="noopener noreferrer"
        :focusable="false"
        text
        icon
      >
        <n-icon :component="LogoGithub" size="2.1em" />
      </n-button>
    </div>
  </div>
</template>

<style scoped>
#navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  height: 4em;
  background-color: var(--colescu);
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}

.icon,
.icon a {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 4em;
}

.n-button {
  font-size: 1.2em;
  color: #fff;
  padding: 0 0.12em;
}
</style>
