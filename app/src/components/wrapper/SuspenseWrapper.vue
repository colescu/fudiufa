<script setup lang="ts"></script>

<template>
  <Suspense>
    <template #default>
      <slot />
    </template>
    <template #fallback>
      <div class="center" style="margin: 2em auto">加載中…</div>
    </template>

    <!-- FIXME UI suspense blocks animation -->
  </Suspense>
</template>

<style scoped></style>
