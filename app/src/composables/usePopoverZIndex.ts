import { Ref, watch } from "vue";
import { nextTick, ref } from "vue";

function raiseZIndex(el: HTMLElement, offset: number) {
  if (!el) return;
  const style = window.getComputedStyle(el);
  const currentZ = parseInt(style.zIndex || "0", 10);
  el.style.zIndex = (currentZ + offset).toString();
}

let popoverCounter = 0;

function getPopoverId(): number {
  return popoverCounter++;
}

export function usePopoverZIndex(
  showPopover: Ref<boolean>,
  baseZIndex: number | undefined
) {
  const popoverId = ref(getPopoverId());

  if (baseZIndex) {
    watch(showPopover, async (value) => {
      if (value) {
        popoverId.value = getPopoverId();
        await nextTick();
        const container = document.querySelector(
          `[popover-id="${popoverId.value}"]`
        ) as HTMLElement;
        if (container) {
          raiseZIndex(
            container.parentElement!.parentElement!,
            baseZIndex - 2000
          );
        }
      }
    });
  }

  return { popoverId };
}
