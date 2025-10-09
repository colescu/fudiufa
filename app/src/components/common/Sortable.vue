<script setup lang="ts">
import { onMounted, ref } from "vue";
import Sortable from "sortablejs";

const items = defineModel<string[]>();

const sortable = ref<HTMLElement | null>(null);

onMounted(() => {
  if (sortable.value) {
    Sortable.create(sortable.value, {
      animation: 0,
      ghostClass: "drag-ghost",
      onEnd: (event) => {
        const moved = items.value!.splice(event.oldIndex!, 1)[0]!;
        items.value!.splice(event.newIndex!, 0, moved);
      },
    });
  }
});
</script>

<template>
  <div ref="sortable">
    <template v-for="(item, index) of items" :key="item">
      <slot :item="item" :index="index" />
    </template>
  </div>
</template>

<style scoped></style>
