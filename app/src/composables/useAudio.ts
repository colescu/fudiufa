import {
  computed,
  onUnmounted,
  ref,
  shallowRef,
  watch,
  watchEffect,
  type Ref,
} from "vue";
import { useRoute } from "vue-router";
import { useSettingsStore } from "../stores/settings";
import type { RubyData } from "@/components/content/CharacterRuby.vue";

// CLEANUP integrate into normalizeTone in @shared
// ipaRaw format with ordinal tone notation
function normalizePronunciation(pronunciation: string): string {
  if (isNaN(Number(pronunciation.at(-1)))) {
    pronunciation += "0";
  }
  let tone = pronunciation.at(-1);
  if (tone === "6") {
    tone = "1";
  }
  if (tone === "0") {
    tone = "ptkʔ".includes(pronunciation.slice(-2, -1)) ? "7" : "1";
  }
  return pronunciation.slice(0, -1) + tone;
}

function getAudioUrl(syllable: string): string {
  return `${
    import.meta.env.DEV ? "/" : import.meta.env.BASE_URL
  }audio/${syllable}.wav`;
}

const audioMapCache = new Map<string, HTMLAudioElement>();

function getAudio(pronunciation: string): HTMLAudioElement {
  pronunciation = normalizePronunciation(pronunciation);
  let audio = audioMapCache.get(pronunciation);
  if (!audio) {
    audio = new Audio(getAudioUrl(pronunciation));
    audio.preload = "auto";
    audioMapCache.set(pronunciation, audio);
  }
  return audio;
}

export function useAudio(pronunciation: string) {
  const isPlaying = ref(false);

  async function play() {
    let audio = getAudio(pronunciation);

    if (audio.currentTime > 0) {
      const tempAudio = new Audio(audio.src);
      audio = tempAudio;
    }

    isPlaying.value = true;
    try {
      await audio.play();
      audio.addEventListener(
        "ended",
        () => {
          isPlaying.value = false;
          audio.currentTime = 0;
        },
        { once: true }
      );
    } catch (error) {
      console.error(
        `Failed to play audio for ${normalizePronunciation(pronunciation)}:`,
        error
      );
      isPlaying.value = false;
    }
  }

  return { play, isPlaying };
}

// Ad hoc TTS

function useSequentialAudio(
  pronunciations: string[],
  delay: number,
  isPlaying: Ref<boolean>
) {
  let stopped = false;
  const current = ref(-1);
  let currentAudio: HTMLAudioElement | null = null;
  let timer: ReturnType<typeof setTimeout> | null = null;

  async function playNext() {
    if (stopped || current.value >= pronunciations.length) {
      isPlaying.value = false;
      current.value = -1;
      return;
    }

    const pronunciation = pronunciations[current.value];
    if (!pronunciation) {
      current.value++;
      timer = setTimeout(playNext, delay);
      return;
    }

    let audio = getAudio(pronunciation);

    if (audio.currentTime > 0) {
      const tempAudio = new Audio(audio.src);
      audio = tempAudio;
    }

    currentAudio = audio;

    if (audio.readyState < 4) {
      try {
        await new Promise<void>((resolve, reject) => {
          audio.addEventListener("canplaythrough", () => resolve(), {
            once: true,
          });
          audio.addEventListener("error", (e) => reject(e), { once: true });
          audio.load();
        });
      } catch (err) {
        console.error(`Failed to load audio for "${pronunciation}":`, err);
        current.value++;
        timer = setTimeout(playNext, delay); // skip failed audio
        return;
      }
    }

    if (stopped) return;

    if (current.value === 0) {
      isPlaying.value = true;
    }

    try {
      audio.currentTime = 0;
      await audio.play();
    } catch (err) {
      console.error(`Failed to play audio for "${pronunciation}":`, err);
    }

    if (!stopped) {
      timer = setTimeout(() => {
        current.value++;
        playNext();
      }, delay);
    }
  }

  async function start() {
    stopped = false;
    if (pronunciations.length === 0) return;

    current.value = 0;
    try {
      await playNext();
    } catch {
      console.error(`Failed to play audio`);
    }
  }

  function stop() {
    stopped = true;
    isPlaying.value = false;
    current.value = -1;

    if (timer) {
      clearTimeout(timer);
      timer = null;
    }

    if (currentAudio) {
      currentAudio.pause();
      currentAudio.currentTime = 0;
      currentAudio = null;
    }
  }

  function toggleAudio() {
    if (isPlaying.value) stop();
    else start();
  }

  return { start, stop, toggleAudio, current };
}

export function useManagedSequentialAudio(phrase: Ref<RubyData[]>) {
  const route = useRoute();
  const settings = useSettingsStore();

  const pronunciations = computed<string[]>(() =>
    phrase.value.map((ruby) => ruby.pronunciation)
  );

  const sequentialAudio = shallowRef<ReturnType<
    typeof useSequentialAudio
  > | null>();
  const isPlaying = ref<boolean>(false);

  watchEffect((onCleanup) => {
    if (sequentialAudio.value) sequentialAudio.value.stop();

    sequentialAudio.value = useSequentialAudio(
      pronunciations.value,
      settings.playSpeed,
      isPlaying
    );

    onCleanup(() => {
      if (sequentialAudio.value) sequentialAudio.value.stop();
    });
  });

  watch(
    () => [route.fullPath, settings.playSpeed],
    () => {
      if (sequentialAudio.value) sequentialAudio.value.stop();
    },
    { deep: true }
  );

  onUnmounted(() => {
    if (sequentialAudio.value) sequentialAudio.value.stop();
  });

  return {
    toggleAudio: () => sequentialAudio.value?.toggleAudio(),
    isPlaying,
    current: computed(() => sequentialAudio.value?.current.value),
  };
}
