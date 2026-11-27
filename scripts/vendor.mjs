// Copies the browser-ready files of frontend npm dependencies into
// app/static/vendor/ so Flask can serve them. The output is gitignored and is
// rebuilt with `npm run vendor` after every `npm ci` (locally, in CI, in the
// Docker image and on deploy).
//
// Only the files the templates actually load are copied. To use another
// Three.js addon, add it to THREE_ADDONS below.

import { cpSync, existsSync, mkdirSync, rmSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const modules = join(root, "node_modules");
const out = join(root, "app", "static", "vendor");

const THREE_ADDONS = [
  "controls/OrbitControls.js",
  "geometries/RoundedBoxGeometry.js",
  "libs/tween.module.js",
  "renderers/CSS3DRenderer.js",
];

// [source relative to node_modules, destination relative to app/static/vendor]
const files = [
  ["three/build/three.module.js", "three/three.module.js"],
  ["three/build/three.core.js", "three/three.core.js"],
  ...THREE_ADDONS.map((addon) => [
    `three/examples/jsm/${addon}`,
    `three/addons/${addon}`,
  ]),

  ["@fortawesome/fontawesome-free/css/all.min.css", "fontawesome/css/all.min.css"],
  ["@fortawesome/fontawesome-free/webfonts", "fontawesome/webfonts"],

  ["lucide/dist/umd/lucide.min.js", "lucide/lucide.min.js"],
  ["chart.js/dist/chart.umd.min.js", "chart.js/chart.umd.min.js"],
  ["htmx.org/dist/htmx.min.js", "htmx/htmx.min.js"],
  ["fabric/dist/fabric.min.js", "fabric/fabric.min.js"],
  ["moment/min/moment.min.js", "moment/moment.min.js"],

  ["remixicon/fonts/remixicon.css", "remixicon/remixicon.css"],
  ...["eot", "svg", "ttf", "woff", "woff2"].map((ext) => [
    `remixicon/fonts/remixicon.${ext}`,
    `remixicon/remixicon.${ext}`,
  ]),
];

const missing = files.filter(([src]) => !existsSync(join(modules, src)));
if (missing.length > 0) {
  console.error("Missing files in node_modules (did you run `npm ci`?):");
  for (const [src] of missing) console.error(`  ${src}`);
  process.exit(1);
}

rmSync(out, { recursive: true, force: true });

for (const [src, dest] of files) {
  const target = join(out, dest);
  mkdirSync(dirname(target), { recursive: true });
  cpSync(join(modules, src), target, { recursive: true });
}

console.log(`Vendored ${files.length} entries into app/static/vendor/`);
