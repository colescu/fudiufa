import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const componentsDir = path.resolve(__dirname, "../src/components/content");
const outputFile = path.resolve(
  __dirname,
  "../src/types/content-components.d.ts"
);

const files = fs.readdirSync(componentsDir).filter((f) => f.endsWith(".vue"));

let content = `import type { DefineComponent } from 'vue';

declare module '*.vue' {
  const component: DefineComponent<{}, {}, any>;
  export default component;
}

declare module 'vue' {
  export interface GlobalComponents {
`;

files.forEach((file) => {
  const name = path.basename(file, ".vue");
  content += `    ${name}: typeof import('../components/content/${file}')['default'];\n`;
});

content += `  }
}

export {};
`;

fs.writeFileSync(outputFile, content);
console.log(`Generated ${outputFile} with ${files.length} components.`);
