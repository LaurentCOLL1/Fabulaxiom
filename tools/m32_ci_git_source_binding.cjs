"use strict";

/** M3.2 fictional-only CI source binding.
 * Compares exact seven tracked files with immutable blobs from the CHECKED
 * OUT Git commit. This is a local CI consistency check, NOT an authenticated
 * external provenance, signature, independent GitHub attestation, or G3 proof.
 */
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { spawnSync } = require("node:child_process");
const { createHash } = require("node:crypto");

const MAX_FILE_BYTES = 2 * 1024 * 1024;
function git(root, args, options = {}) {
  const result = spawnSync("git", ["-C", root, ...args], {
    windowsHide: true, shell: false, encoding: null,
    timeout: 15000, maxBuffer: MAX_FILE_BYTES + 1024,
    ...options,
  });
  if (result.error || result.status !== 0) {
    throw Error("STOP: Git source-object check failed (no fallback to working tree)");
  }
  return result.stdout;
}

function bindSourcesToCheckout(root, expectedCommit, allowlist) {
  assert.match(expectedCommit, /^[a-f0-9]{40}$/, "STOP: exact checkout SHA required");
  assert.ok(Array.isArray(allowlist) && allowlist.length > 0, "STOP: source allowlist required");
  assert.equal(new Set(allowlist).size, allowlist.length, "STOP: duplicate source path");
  const actualCommit = git(root, ["rev-parse", "--verify", "HEAD"]).toString("utf8").trim();
  assert.equal(actualCommit, expectedCommit, "STOP: checked-out Git HEAD differs from CI event SHA");
  const blobs = new Map();
  const inventory = [];
  for (const relative of allowlist) {
    assert.match(relative, /^(?:m32-browser-lab\.html|src\/[A-Za-z0-9_]+\.tsx|src\/m32BrowserLab\.css)$/,
      "STOP: a source path outside the known fictional module family");
    const source = path.resolve(root, relative);
    assert.ok(source.startsWith(path.resolve(root) + path.sep), "STOP: source path escaped checkout");
    const stat = fs.lstatSync(source);
    assert.ok(stat.isFile() && !stat.isSymbolicLink(), "STOP: source is not a regular file");
    assert.ok(stat.size > 0 && stat.size <= MAX_FILE_BYTES, "STOP: source size unexpected");
    const committedBytes = git(root, ["cat-file", "blob", expectedCommit + ":" + relative]);
    const currentBytes = fs.readFileSync(source);
    assert.ok(currentBytes.equals(committedBytes),
      "STOP: staged fictional source differs from exact Git commit blob: " + relative);
    const after = fs.lstatSync(source);
    assert.ok(after.isFile() && !after.isSymbolicLink() &&
      after.size === stat.size && after.ino === stat.ino && after.dev === stat.dev,
      "STOP: file identity changed during local source comparison");
    const sha256 = createHash("sha256").update(committedBytes).digest("hex");
    inventory.push(Object.freeze({ path: relative, bytes: committedBytes.length, sha256 }));
    blobs.set(relative, committedBytes);
  }
  const sortedInventory = Object.freeze(inventory.sort((a, b) => a.path.localeCompare(b.path)));
  const inventorySha = createHash("sha256").update(
    JSON.stringify({ gitHead: expectedCommit, sources: sortedInventory }), "utf8"
  ).digest("hex");
  return Object.freeze({
    gitHead: actualCommit,
    inventory: sortedInventory,
    inventorySha,
    source(relative) {
      const blob = blobs.get(relative);
      return blob ? Buffer.from(blob) : null;
    },
  });
}

module.exports = { bindSourcesToCheckout };
