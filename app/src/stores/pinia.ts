import { createPinia } from "pinia";
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";

export default function createPiniaInstance() {
  const pinia = createPinia();
  pinia.use(piniaPluginPersistedstate);

  const stores = import.meta.glob(["./*.ts", "!./pinia/*.ts"], { eager: true });

  // sync across tabs, except for history
  if (typeof window !== "undefined") {
    Object.entries(stores).forEach(([file, module]) => {
      if (file !== "./history.ts") {
        const name = file.slice(2, -3);
        window.addEventListener("storage", (event) => {
          if (event.key === name) {
            const newState = event.newValue ? JSON.parse(event.newValue) : null;
            if (newState) {
              const store = (
                (module as Record<string, unknown>)[
                  `use${name[0]!.toUpperCase() + name.slice(1)}Store`
                ] as Function
              )();
              store.$patch(newState);
            }
          }
        });
      }
    });
  }

  return pinia;
}
