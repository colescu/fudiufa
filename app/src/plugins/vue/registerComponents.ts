import type { App, DefineComponent } from "vue";

function getComponentNameFromPath(path: string): string {
  const fileName = path.split("/").pop() || "";
  return fileName.replace(/\.\w+$/, "");
}

// Registers /components/content/* globally for use in markdown files
export function registerComponents(app: App) {
  const moduleMap = {
    ...import.meta.glob("@/components/wrapper/MarkdownWrapper.vue", {
      eager: true,
    }),
    ...import.meta.glob("@/components/content/*.vue", { eager: true }),
  };

  for (const [path, module] of Object.entries(moduleMap)) {
    const comp = (module as { default: DefineComponent }).default;
    const name = comp.name ?? getComponentNameFromPath(path);
    app.component(name, comp);
  }
}
