import type { DefineComponent } from 'vue';

declare module '*.vue' {
  const component: DefineComponent<{}, {}, any>;
  export default component;
}

declare module 'vue' {
  export interface GlobalComponents {
    Character: typeof import('../components/content/Character.vue')['default'];
    CharacterRuby: typeof import('../components/content/CharacterRuby.vue')['default'];
    Double: typeof import('../components/content/Double.vue')['default'];
    DoublePronunciation: typeof import('../components/content/DoublePronunciation.vue')['default'];
    MCInfo: typeof import('../components/content/MCInfo.vue')['default'];
    Phrase: typeof import('../components/content/Phrase.vue')['default'];
    Pronunciation: typeof import('../components/content/Pronunciation.vue')['default'];
    Reference: typeof import('../components/content/Reference.vue')['default'];
    Tooltip: typeof import('../components/content/Tooltip.vue')['default'];
  }
}

export {};
