import { createReadStream, existsSync, statSync } from "node:fs";
import { extname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import vue from "@vitejs/plugin-vue";
import { defineConfig, loadEnv, type Plugin } from "vite";

const here = fileURLToPath(new URL(".", import.meta.url));
const repoRoot = resolve(here, "../..");
const appPublic = resolve(repoRoot, "app/public");

function serveSharedPublic(): Plugin {
  const mime: Record<string, string> = {
    ".json": "application/json; charset=utf-8",
    ".txt": "text/plain; charset=utf-8",
    ".yaml": "text/yaml; charset=utf-8",
  };

  return {
    name: "serve-shared-public",
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        const url = decodeURIComponent(req.url?.split("?")[0] ?? "");
        if (!url.startsWith("/data/") && !url.startsWith("/external/")) {
          next();
          return;
        }

        const file = resolve(appPublic, `.${url}`);
        if (!file.startsWith(appPublic) || !existsSync(file) || statSync(file).isDirectory()) {
          next();
          return;
        }

        res.setHeader("Content-Type", mime[extname(file)] ?? "application/octet-stream");
        createReadStream(file).pipe(res);
      });
    },
  };
}

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, here, "");

  return {
    base: env.VITE_BASE || (mode === "production" ? "/fudiufa/learn-mc/" : "/"),
    resolve: {
      alias: {
        "@": resolve(here, "src"),
        "@shared": resolve(repoRoot, "shared/typescript"),
      },
    },
    server: {
      fs: { allow: [repoRoot] },
    },
    plugins: [vue(), serveSharedPublic()],
  };
});
