import {
  createWebHistory,
  createMemoryHistory,
  createRouter,
  type RouteLocationNormalized,
} from "vue-router";
import { languageRouting } from "@/composables/useParamRouting";

import Home from "@/views/Home.vue";
import Introduction from "@/views/introduction.md";
const Phonology = () => import("@/views/Phonology/PhonologyView.vue");
import Vocabulary from "@/views/Vocabulary/VocabularyView.vue";
import LangWrapper from "@/components/wrapper/LangWrapper.vue";
import Search from "@/views/Search/SearchView.vue";
import Pronounce from "@/views/Pronounce/PronounceView.vue";
import RhymeTable from "@/modules/RhymeTable/RhymeTable.vue";
import DiachronicTable from "@/modules/DiachronicTable/DiachronicTable.vue";
import MCTable from "@/views/MCTable/MCTableView.vue";
import MoreSettings from "@/views/Settings/SettingsView.vue";

const routes = [
  { path: "/", name: "Home", component: Home },
  {
    path: "/gaiseu",
    name: "Introduction",
    component: Introduction,
  },
  {
    path: "/inyn/:tab?/:subtab?",
    name: "Phonology",
    component: Phonology,
  },
  {
    path: "/ifi/:tab?/:subtab?",
    name: "Vocabulary",
    component: Vocabulary,
  },
  {
    path: "/:language?",
    name: "LangWrapper",
    component: LangWrapper,
    props: true,
    beforeEnter: languageRouting,
    children: [
      { path: "caci", name: "Search", component: Search },
      { path: "duin", name: "Pronounce", component: Pronounce },
      // { path: "yntu", component: RhymeTable },
      { path: "gujintu", component: DiachronicTable },
    ],
  },
  {
    path: "/xiauynbiau",
    name: "MCTableView",
    component: MCTable,
    meta: { hideNavbar: true },
  },
  {
    path: "/setdi",
    name: "MoreSettings",
    component: MoreSettings,
  },
];

const routerOptions = {
  history: (typeof window !== "undefined"
    ? createWebHistory
    : createMemoryHistory)(import.meta.env.BASE_URL),
  routes,
  scrollBehavior: async (
    to: RouteLocationNormalized,
    from: RouteLocationNormalized,
    savedPosition: any
  ) => {
    if (savedPosition) return savedPosition;

    if (to.hash) {
      return new Promise(() => {
        setTimeout(() => {
          const id = decodeURIComponent(to.hash.slice(1));
          const el = document.getElementById(id);

          const navbar = document.querySelector(
            "#navbar"
          ) as HTMLElement | null;
          let navbarHeight = 0;
          if (navbar) {
            navbarHeight = navbar.offsetHeight;
          }

          if (el) {
            const style = window.getComputedStyle(el);
            const emInPx = parseFloat(style.fontSize);
            const top =
              (el as HTMLElement).getBoundingClientRect().top +
              window.scrollY -
              navbarHeight -
              emInPx;
            window.scrollTo({ top, behavior: "smooth" });
          }
        }, 500); // wait for rendering
      });
    }

    return { left: 0, top: 0 };
  },
};

export default function createRouterInstance() {
  const router = createRouter(routerOptions);
  return router;
}
