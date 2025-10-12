import {
  ComputedRef,
  inject,
  onBeforeUnmount,
  provide,
  reactive,
  Ref,
  watch,
} from "vue";
import { DiachronicTableState } from "./types";

type Reactive<T> = Ref<T> | ComputedRef<T>;

export function useProvideDiachronicTableState() {
  const diachronicTableState = reactive<DiachronicTableState>({
    isFullscreen: false,
    mcIndices: [],
    langIndices: [],
  });
  provide("diachronicTableState", diachronicTableState);

  return { diachronicTableState };
}

export function useInjectDiachronicTableState(
  mcIndices: Reactive<number[]>,
  langIndices: Reactive<number[]>
) {
  const diachronicTableState = inject(
    "diachronicTableState"
  ) as DiachronicTableState;

  let mcWatcher: any = null;
  let langWatcher: any = null;

  function resetDiachronicTable() {
    mcWatcher?.();
    langWatcher?.();
    mcWatcher = null;
    langWatcher = null;
    diachronicTableState.isFullscreen = false;
    diachronicTableState.mcIndices = [];
    diachronicTableState.langIndices = [];
  }

  function updateDiachronicTable() {
    diachronicTableState.isFullscreen = true;
    mcWatcher = watch(
      mcIndices,
      (value) => {
        diachronicTableState.mcIndices = value;
      },
      { immediate: true }
    );
    langWatcher = watch(
      langIndices,
      (value) => {
        diachronicTableState.langIndices = value;
      },
      { immediate: true }
    );
  }

  onBeforeUnmount(resetDiachronicTable);

  return { diachronicTableState, updateDiachronicTable };
}
