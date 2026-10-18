"use strict";

/** CI-only, new-and-never-reused M3.2 staging of literal fictional modules.
 * No database or user files, no symlinks, no recursive source directory copy.
 * The staging directory lives under the ephemeral Actions checkout so React
 * resolves from the locked parent node_modules. This is not an operator setup.
 */
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const ROOT = path.resolve(__dirname, "..");
const MANIFEST = Object.freeze([
  "m32-browser-lab.html",
  "src/m32BrowserLab.tsx",
  "src/m32BrowserLab.css",
  "src/M32ChronologyConsultation.tsx",
  "src/M32ChronologyPreview.tsx",
  "src/M32WorldOrderComparison.tsx",
  "src/M32SyntheticEventExplorer.tsx",
]);

function stageFictionOnly() {
  assert.equal(process.env.CI?.toLowerCase(), "true", "STOP: ephemeral CI only");
  assert.equal(process.env.RUNNER_OS, "Windows", "STOP: Windows CI required");
  assert.equal(process.env.TAURI_DEV_HOST, undefined, "STOP: TAURI_DEV_HOST inherited");
  assert.equal(process.env.__VITE_ADDITIONAL_SERVER_ALLOWED_HOSTS, undefined,
    "STOP: additional host allowance inherited");
  assert.equal(new Set(MANIFEST).size, MANIFEST.length);
  assert.ok(fs.statSync(path.join(ROOT, "node_modules", "vite")).isDirectory(),
    "STOP: locked Vite dependencies unavailable");

  // Refuse new imports outside the exact fiction-only transitive module graph.
  // Importing a normal app module must fail BEFORE staging or starting Vite.
  const allow = new Set(MANIFEST);
  for (const relative of MANIFEST.filter(f => f.endsWith(".tsx"))) {
    const content = fs.readFileSync(path.join(ROOT, relative), "utf8");
    const imports = [...content.matchAll(/\b(?:from\s*|import\s*|import\s*\(\s*)["']([^"']+)["']/g)];
    for (const match of imports) {
      const specifier = match[1];
      if (!specifier.startsWith(".")) {
        assert.ok(["react", "react-dom/client"].includes(specifier),
          "STOP: non-fictional package import " + specifier);
        continue;
      }
      const normalized = path.posix.normalize(path.posix.join(path.posix.dirname(relative), specifier));
      const candidates = [normalized, normalized + ".ts", normalized + ".tsx", normalized + ".css"];
      assert.ok(candidates.some(candidate => allow.has(candidate)),
        "STOP: import escaped fictional file manifest: " + relative + " -> " + specifier);
    }
  }

  // Deliberately create a brand-new uniquely named directory. No cleanup of
  // any previously existing directory; runner itself is ephemeral.
  const stage = fs.mkdtempSync(path.join(ROOT, ".m32-fixture-only-"));
  const made = [];
  for (const relative of MANIFEST) {
    const source = path.resolve(ROOT, relative);
    const stat = fs.lstatSync(source);
    assert.ok(stat.isFile() && !stat.isSymbolicLink(), "STOP: source is not a regular file");
    const target = path.resolve(stage, relative);
    assert.ok(target.startsWith(stage + path.sep));
    fs.mkdirSync(path.dirname(target), { recursive: true });
    fs.copyFileSync(source, target, fs.constants.COPYFILE_EXCL);
    made.push(relative);
  }
  const actual = [];
  function visit(dir) {
    for (const item of fs.readdirSync(dir, { withFileTypes: true })) {
      assert.ok(!item.isSymbolicLink(), "STOP: staged symlink not permitted");
      const child = path.join(dir, item.name);
      if (item.isDirectory()) visit(child);
      else if (item.isFile()) actual.push(path.relative(stage, child).replaceAll("\\", "/"));
      else throw Error("STOP: unexpected file type in stage");
    }
  }
  visit(stage);
  assert.deepEqual(actual.sort(), [...MANIFEST].sort(), "STOP: stage contains unexpected files");
  assert.ok(!actual.includes("index.html") && !actual.includes("src/App.tsx")
    && !actual.includes("src/main.tsx"), "STOP: normal application staged");
  console.log("M32_CI_FIXTURE_STAGE_EXACT_PASS: " + made.length + " fictional files; no normal App");
  return stage;
}

module.exports = { stageFictionOnly, MANIFEST };
