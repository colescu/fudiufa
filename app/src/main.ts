import { setupGoogleAnalytics } from "./analytics";

import { createApp, type App as VueApp } from "vue";
import App from "./components/wrapper/NaiveUIWrapper.vue";
import "./styles/main.scss";
import Vue3TouchEvents from "vue3-touch-events";
import createRouterInstance from "./router/router";
import createPiniaInstance from "./stores/pinia";
import { registerComponents } from "./plugins/vue/registerComponents";
import { ROUTES_MAP } from "./router/routes";

import { init as initShared } from "@shared/init";
import { dictionaryCache } from "@shared/lang";
import { rhymeTableCache } from "./modules/RhymeTable/cache";
import { commentsCache } from "./modules/ReflexTable/cache";
import { charactersCache } from "./views/Vocabulary/Character/cache";

setupGoogleAnalytics();

await Promise.all([
  initShared(),
  dictionaryCache.load("FG"),
  rhymeTableCache.load(),
  commentsCache.load(),
  charactersCache.load(),
]);

let appInstance: VueApp<Element> | null = null;
let router = createRouterInstance();
let pinia = createPiniaInstance();

function createAppInstance(): VueApp<Element> {
  const app = createApp(App);
  app.use(router);
  app.use(pinia);
  app.use(Vue3TouchEvents, {
    swipeConeSize: 0.5,
  });
  app.config.globalProperties.$ROUTES = ROUTES_MAP;
  registerComponents(app);
  return app;
}

export async function mountApp() {
  if (appInstance) {
    appInstance.unmount();
  }
  const app = createAppInstance();
  app.mount("#app");
  appInstance = app;
}
// FIXME TypeError: Cannot read properties of undefined (reading 'app')

await mountApp();
