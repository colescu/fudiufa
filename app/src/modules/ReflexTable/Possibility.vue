<script setup lang="ts">
import { computed, inject } from "vue";
import { useHistoryStore } from "@/stores/history";
import { PossibilityData } from "./types";

const history = useHistoryStore();
const hasComment = inject("hasComment");

const { possibility, mcIndices, tableUrl } = defineProps<{
  possibility: PossibilityData;
  mcIndices: number[];
  tableUrl: string;
}>();

// Ad hoc parsing
function parseComment(text: string) {
  return { comment: text.split("|")[0], to: text.split("|")[1] };
}

const renderedComments = computed(() =>
  possibility.comment.split("、").map(parseComment)
);

function openTable() {
  window.open(tableUrl, "_blank");
}

// FEATURE 改爲顯示古今圖
</script>

<template>
  <span v-if="possibility.comment !== '罕'" class="block">
    <span
      class="text clickable"
      @click="openTable"
      v-html="possibility.value"
    />
    <table class="subsup">
      <tbody>
        <tr>
          <td>
            <span
              v-if="
                possibility.comment &&
                hasComment &&
                history.phonology.predict.show.comment
              "
            >
              <template v-for="item of renderedComments">
                {{ item.comment }}
                <Reference v-if="item.to" :to="item.to" />
              </template>
            </span>
            <span v-else class="placeholder"></span>
          </td>
        </tr>
        <tr>
          <td>
            <span
              v-if="
                possibility.frequency != 1 &&
                history.phonology.predict.show.frequency
              "
              style="color: var(--gray-text)"
            >
              {{ Math.round(possibility.frequency * 100) }}%
            </span>
            <span v-else class="placeholder"></span>
          </td>
        </tr>
      </tbody>
    </table>
  </span>
</template>

<style scoped>
.text {
  white-space: pre;
}

.block {
  display: inline-block;
  min-width: max-content;
  white-space: nowrap;
  margin: 0 0.2em;
}

.subsup {
  display: inline-table;
  vertical-align: middle;
  border-collapse: collapse;
  padding: 0;
  margin: 0;
  margin-left: 0.1em;
}

.subsup td {
  text-align: left;
  border: none;
  line-height: 1.2em;
  font-size: 0.7em;
  padding: 0;
  margin: 0;
}

.placeholder {
  display: inline-block;
  height: 1em;
  width: 0;
}
</style>
