import { computed, onMounted, onBeforeUnmount, ref } from "vue";

// track if a type of component is mounted
function getTrackUtils(className: string) {
  const trackedElements = ref<Set<HTMLElement>>(new Set<HTMLElement>());
  let observer: MutationObserver | null = null;

  function updateTracked() {
    const nodes = Array.from(
      document.getElementsByClassName(className)
    ) as HTMLElement[];
    trackedElements.value.clear();
    nodes.forEach((el) => {
      trackedElements.value.add(el);
    });
  }

  function track() {
    onMounted(() => {
      if (!observer) {
        observer = new MutationObserver(updateTracked);
        updateTracked();
      }
      observer.observe(document.body, {
        childList: true,
        subtree: true,
        attributes: true,
        attributeFilter: ["style", "class"],
      });
    });

    onBeforeUnmount(() => {
      trackedElements.value.clear();
      if (observer) {
        observer.disconnect();
        observer = null;
      }
    });
  }

  const tracked = computed<boolean>(
    () =>
      Array.from(trackedElements.value).filter((el) => el.offsetParent != null)
        .length > 0
  );

  return { tracked, track };
}

export const { tracked: hasBoth, track: trackHasBoth } =
  getTrackUtils("track-both");
export const { tracked: hasPhrase, track: trackHasPhrase } =
  getTrackUtils("track-phrase");
