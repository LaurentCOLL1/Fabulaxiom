"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { createHash } = require("node:crypto");
const { allowed, pinStaticBytes } = require("./m32_ci_static_byte_snapshot.cjs");

assert.equal(process.env.CI?.toLowerCase(), "true", "STOP: fixture audit only in CI");
assert.equal(process.env.RUNNER_OS, "Windows", "STOP: fixture audit only on Windows runner");
assert.ok(process.env.RUNNER_TEMP, "STOP: runner temporary folder not configured");

function fixture(html = '<!doctype html><html><body><script type="module" src="/assets/main.abcdef.js"></script></body></html>') {
  const root = fs.mkdtempSync(path.join(process.env.RUNNER_TEMP, "fabulaxiom-m32-bytes-"));
  fs.mkdirSync(path.join(root, "assets"));
  fs.writeFileSync(path.join(root, "m32-browser-lab.html"), html);
  fs.writeFileSync(path.join(root, "assets", "main.abcdef.js"), "globalThis.fictional = true;\n");
  fs.writeFileSync(path.join(root, "assets", "main.abcdef.css"), "body{margin:0}\n");
  return root; // CI scratch; never traverse/delete unrelated paths
}

test("01 filename allowlist cannot serve main application or alternate routes", () => {
  for (const bad of ["", "index.html", "src/App.tsx", "src/main.tsx", "/assets/a.js",
    "assets/../../index.html", "assets/.env", "assets/file.js?foo", "assets/a.svg"]) {
    assert.equal(allowed(bad), false, bad);
  }
  assert.equal(allowed("m32-browser-lab.html"), true);
  assert.equal(allowed("assets/main.a1b2.js"), true);
});

test("02 SHA256 inventory exact and deterministic for a fictional bundle", () => {
  const seal = pinStaticBytes(fixture());
  assert.deepEqual(seal.inventory.map(e => e.name), [
    "assets/main.abcdef.css", "assets/main.abcdef.js", "m32-browser-lab.html"
  ]);
  for (const item of seal.inventory) {
    const result = seal.get(item.name);
    assert.equal(item.sha256, createHash("sha256").update(result.body).digest("hex"));
    assert.equal(item.bytes, result.body.length);
  }
  assert.equal(seal.get("index.html"), null);
});

test("03 previously pinned body unaffected by source overwrite and deletion", () => {
  const root = fixture();
  const seal = pinStaticBytes(root);
  const first = seal.get("assets/main.abcdef.js");
  fs.writeFileSync(path.join(root, "assets", "main.abcdef.js"), "throw Error('tamper');");
  fs.unlinkSync(path.join(root, "m32-browser-lab.html"));
  const second = seal.get("assets/main.abcdef.js");
  assert.deepEqual(first.body, second.body);
  assert.equal(first.sha256, second.sha256);
  assert.ok(seal.get("m32-browser-lab.html").body.toString("utf8").includes("m32-browser-lab") === false);
});

test("04 returned Buffer is a copy and cannot change sealed RAM", () => {
  const seal = pinStaticBytes(fixture());
  const first = seal.get("assets/main.abcdef.js");
  first.body.fill(0);
  const second = seal.get("assets/main.abcdef.js");
  assert.notDeepEqual(first.body, second.body);
  assert.equal(createHash("sha256").update(second.body).digest("hex"), second.sha256);
});

test("05 unexpected normal product file vetoes entire snapshot", () => {
  const root = fixture();
  fs.writeFileSync(path.join(root, "index.html"), "NORMAL_APP");
  assert.throws(() => pinStaticBytes(root), /unlisted static file/);
});

test("06 entry script must exist in exact compiled output", () => {
  const root = fixture();
  fs.unlinkSync(path.join(root, "assets", "main.abcdef.js"));
  assert.throws(() => pinStaticBytes(root), /no compiled JS|referenced script not in bundle/);
});

test("07 inline script and handler mutation are forbidden", () => {
  assert.throws(() => pinStaticBytes(fixture(
    '<script src="/assets/main.abcdef.js"></script><script>alert("bad")</script>'
  )), /inline JS/);
  assert.throws(() => pinStaticBytes(fixture(
    '<script src="/assets/main.abcdef.js"></script><div onclick="bad()">a</div>'
  )), /inline styles\/events/);
});

test("08 empty or unexpected asset type is refused before listening", () => {
  const root = fixture();
  fs.writeFileSync(path.join(root, "assets", "main.abcdef.js"), "");
  assert.throws(() => pinStaticBytes(root), /empty static resource/);
  const second = fixture();
  fs.writeFileSync(path.join(second, "assets", "unknown.svg"), "no");
  assert.throws(() => pinStaticBytes(second), /unlisted static file/);
});

console.log("M32_CI_STATIC_RAM_SNAPSHOT_TESTS_DEFINED: source-only Windows CI; no Tauri launch");
