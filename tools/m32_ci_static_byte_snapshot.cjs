"use strict";

/** Ephemeral Windows-CI-only fixture byte pinning.
 * This snapshots build output into RAM ONCE before the HTTP server listens;
 * later file edits/renames do not modify the served bytes. SHA256 is a local
 * consistency digest, NOT a signature or independent source attestation.
 */
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { createHash } = require("node:crypto");

function allowed(relative) {
  return relative === "m32-browser-lab.html" ||
    /^assets\/[A-Za-z0-9_.-]+\.(?:js|css)$/.test(relative);
}

function pinStaticBytes(directory) {
  const entries = new Map();
  const root = fs.realpathSync(directory);
  assert.ok(fs.statSync(root).isDirectory(), "STOP: no static asset directory");
  assert.ok(!fs.lstatSync(directory).isSymbolicLink(), "STOP: static directory symlink");
  function traverse(folder) {
    for (const child of fs.readdirSync(folder, { withFileTypes: true })) {
      const file = path.join(folder, child.name);
      const stat = fs.lstatSync(file);
      assert.ok(!stat.isSymbolicLink(), "STOP: static bundle symlink");
      if (stat.isDirectory()) {
        traverse(file);
        continue;
      }
      assert.ok(stat.isFile(), "STOP: unexpected static file type");
      const relative = path.relative(root, file).replaceAll("\\", "/");
      assert.ok(allowed(relative), "STOP: unlisted static file " + relative);
      assert.ok(!entries.has(relative), "STOP: duplicate static resource");
      const bytes = fs.readFileSync(file);
      assert.ok(bytes.length > 0, "STOP: empty static resource");
      // Verify content still corresponds to the file just inspected, before
      // pinning. No filesystem paths will be reopened by the HTTP handler.
      const after = fs.lstatSync(file);
      assert.ok(after.isFile() && !after.isSymbolicLink() &&
        after.size === bytes.length && after.ino === stat.ino && after.dev === stat.dev,
        "STOP: changed static source during snapshot");
      entries.set(relative, {
        bytes,
        sha256: createHash("sha256").update(bytes).digest("hex"),
      });
    }
  }
  traverse(root);
  assert.ok(entries.has("m32-browser-lab.html"), "STOP: missing fictional HTML");
  assert.ok([...entries.keys()].some(x => x.endsWith(".js")), "STOP: no compiled JS");
  const html = entries.get("m32-browser-lab.html").bytes.toString("utf8");
  const scripts = [...html.matchAll(/<script\b[^>]*\bsrc=["'](\/assets\/[A-Za-z0-9_.-]+\.js)["']/gi)];
  assert.ok(scripts.length > 0, "STOP: fictional entry script missing");
  for (const match of scripts) {
    assert.ok(entries.has(match[1].slice(1)), "STOP: referenced script not in bundle");
  }
  assert.ok(!/<script(?:\s[^>]*)?>[\s\S]*?<\/script>/i.test(
    html.replace(/<script\s+[^>]*src=["'][^"']+["'][^>]*><\/script>/gi, "")),
    "STOP: inline JS in compiled entry");
  assert.ok(!/<style\b/i.test(html) && !/\son[a-z]+\s*=/i.test(html),
    "STOP: inline styles/events in compiled entry");
  assert.ok(!html.includes("/src/App.tsx") && !html.includes("/src/main.tsx"),
    "STOP: ordinary Fabulaxiom source in fictional bundle");
  const inventory = Object.freeze([...entries].map(([name, data]) =>
    Object.freeze({ name, bytes: data.bytes.length, sha256: data.sha256 })
  ).sort((a,b) => a.name.localeCompare(b.name)));
  return Object.freeze({
    inventory,
    get(relative) {
      const data = entries.get(relative);
      // Always return a COPY; nobody outside this closure mutates pinned RAM.
      return data ? Object.freeze({
        body: Buffer.from(data.bytes), sha256: data.sha256
      }) : null;
    },
  });
}

module.exports = { allowed, pinStaticBytes };
