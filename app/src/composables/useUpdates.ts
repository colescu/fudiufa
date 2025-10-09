import { getComparer, precomposeComparer } from "@shared/common/sort";
import { markRaw, ref, type DefineComponent } from "vue";
import pkg from "@/../package.json";

function parseVersion(text: string) {
  return text.split(".").map(Number);
}

const versionComparer = getComparer(parseVersion);

type Update = {
  version: string;
  component: DefineComponent;
  date: string;
};

export function useUpdates() {
  const currentVersion = pkg.version;
  const lastVersion = localStorage.getItem("lastVersion");

  const modules = Object.entries(import.meta.glob("@/updates/*.md"))
    .map(([path, loader]) => ({
      version: path.split("/").pop()!.replace(/\.md$/, ""),
      loader: loader as () => Promise<{ default: DefineComponent }>,
    }))
    .sort(precomposeComparer(versionComparer, (module) => module.version))
    .filter(
      (update) =>
        (lastVersion == undefined ||
          versionComparer(lastVersion, update.version) < 0) &&
        versionComparer(update.version, currentVersion) <= 0
    );

  async function getUpdate(module: (typeof modules)[number]) {
    const { version, loader } = module;
    if (version) {
      localStorage.setItem("lastVersion", version);
    }
    const mod = await loader();
    return {
      version,
      component: markRaw(mod.default),
      date: (mod as any)["date"].split("T")[0] as string,
    };
  }

  let index = 0;
  const currentUpdate = ref<Update | null>(null);

  async function next() {
    currentUpdate.value =
      index < modules.length ? await getUpdate(modules[index]!) : null;
    index++;
  }

  return { currentUpdate, next };
}
