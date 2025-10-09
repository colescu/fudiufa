import { onBeforeUnmount, onMounted, watch, type Ref } from "vue";
import Sortable from "sortablejs";

type DraggableGroup<T> = {
  ordering: Ref<T[]>;
  keyName: string;
  keyGetter?: (value: T) => string;
  draggable?: string;
};

// ChatGPT
export function useDraggable<T extends readonly DraggableGroup<any>[]>(
  container: Ref<HTMLElement | null>,
  groups: T,
  watched?: any
) {
  let sortableInstance: Sortable | null = null;

  function findGroup(groupName: string | null) {
    if (!groupName) return null;
    return groups.find((group) => group.keyName === groupName);
  }

  function findIndex(group: DraggableGroup<any>, key: string) {
    const keyGetter = group.keyGetter ?? ((v) => v as string);
    return group.ordering.value.map(keyGetter).indexOf(key);
  }

  function createSortable() {
    if (!container.value) return;
    if (sortableInstance) return;
    sortableInstance = Sortable.create(container.value, {
      animation: 0,
      draggable:
        groups
          .map((g) => g.draggable)
          .filter(Boolean)
          .join(",") || "*",
      onMove: (evt) => {
        const draggedGroupName = evt.dragged.getAttribute("group");
        const relatedGroupName = evt.related.getAttribute("group");
        if (draggedGroupName !== relatedGroupName) return false;

        const group = findGroup(draggedGroupName);
        if (!group) return false;

        const from = findIndex(
          group,
          evt.dragged.getAttribute(group.keyName) || ""
        );
        const to = findIndex(
          group,
          evt.related.getAttribute(group.keyName) || ""
        );
        if (from < 0 || to < 0 || from === to) return false;

        const arr = group.ordering.value;
        [arr[from], arr[to]] = [arr[to], arr[from]];
        return true;
      },
    });
  }

  onMounted(() => createSortable());

  if (watched) {
    watch(
      watched,
      () => {
        if (!sortableInstance) createSortable();
      },
      { deep: true }
    );
  }

  onBeforeUnmount(() => {
    if (sortableInstance) sortableInstance.destroy();
  });
}
