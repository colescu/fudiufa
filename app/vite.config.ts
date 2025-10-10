import { defineConfig, loadEnv, type ConfigEnv } from "vite";
import { resolve } from "path";
import vue from "@vitejs/plugin-vue";
import svgLoader from "vite-svg-loader";
import Markdown from "unplugin-vue-markdown/vite";
import { markdownItSetup } from "./src/plugins/vite/markdownItSetup";
import vueDevTools from "vite-plugin-vue-devtools";
import { visualizer } from "rollup-plugin-visualizer";

export default (configEnv: ConfigEnv) => {
  const env = loadEnv(configEnv.mode, process.cwd(), "");
  return defineConfig({
    esbuild: {
      target: "esnext",
    },
    base: env.VITE_BASE || "/",
    build: {
      outDir: env.VITE_OUT_DIR || "dist",
      cssCodeSplit: false,
      rollupOptions: {
        output: {
          manualChunks(id) {
            if (id.includes("node_modules")) {
              for (const name of ["naive-ui"]) {
                if (id.includes(name)) {
                  return name;
                }
              }
              return "vendor";
            }
            if (id.endsWith(".vue")) {
              return "components";
            }
            if (id.includes("updates/")) {
              return "updates";
            }
          },
        },
      },
    },
    resolve: {
      alias: {
        "@": resolve(__dirname, "src"),
        "@shared": resolve(__dirname, "../shared/typescript"),
      },
      extensions: [".vue", ".ts", ".json", ".md"],
    },
    server: {
      fs: {
        allow: [resolve(__dirname, "..")],
      },
    },
    plugins: [
      vue({
        include: [/\.vue$/, /\.md$/],
        template: {
          compilerOptions: {
            isCustomElement: (tag) => tag === "rb",
          },
        },
      }),
      svgLoader(),
      Markdown({
        wrapperComponent: "MarkdownWrapper",
        markdownItOptions: {
          html: true,
          linkify: true,
          typographer: true,
        },
        markdownItSetup,
      }),
      // vueDevTools(),
      // visualizer({ open: true }),
    ],
    define: {
      __LAST_UPDATE__: JSON.stringify(new Date().toISOString()),
      __IS_DEV__: process.env.NODE_ENV === "development",
    },
  });
};
