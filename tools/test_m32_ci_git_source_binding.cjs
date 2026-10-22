"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { spawnSync } = require("node:child_process");
const { createHash } = require("node:crypto");
const { bindSourcesToCheckout } = require("./m32_ci_git_source_binding.cjs");
const { MANIFEST } = require("./m32_ci_fixture_stage.cjs");

assert.equal(process.env.CI?.toLowerCase(), "true", "STOP: fixture Git tests require CI");
assert.equal(process.env.RUNNER_OS, "Windows", "STOP: disposable Windows runner only");
assert.ok(process.env.RUNNER_TEMP, "STOP: no disposable runner TEMP");

function git(root, ...args) {
  const run = spawnSync("git", ["-C", root, ...args], {
    encoding: "utf8", windowsHide: true, shell: false, timeout: 30000,
  });
  assert.equal(run.status, 0, "isolated fixture Git failure: " + run.stderr);
  return run.stdout.trim();
}

function fixture() {
  const root = fs.mkdtempSync(path.join(process.env.RUNNER_TEMP, "fabulaxiom-m32-git-"));
  git(root, "init", "-q");
  for (const rel of MANIFEST) {
    const file = path.join(root, rel);
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, "invented-only-file:" + rel + "\n", { flag: "wx" });
  }
  git(root, "add", "--", ...MANIFEST);
  git(root, "-c", "user.name=CI fictional fixture", "-c",
    "user.email=fictional-fixture@example.invalid", "commit", "-qm", "exact fabricated source");
  return { root, head: git(root, "rev-parse", "HEAD") };
}

test("01 exact SHA and eleven Git blobs match fictional-only sources", () => {
  const f = fixture();
  const evidence = bindSourcesToCheckout(f.root, f.head, MANIFEST);
  assert.equal(evidence.gitHead, f.head);
  assert.equal(evidence.inventory.length, 11);
  assert.match(evidence.inventorySha, /^[a-f0-9]{64}$/);
  for (const item of evidence.inventory) {
    assert.equal(item.sha256,
      createHash("sha256").update(fs.readFileSync(path.join(f.root,item.path))).digest("hex"));
    assert.ok(evidence.source(item.path).equals(fs.readFileSync(path.join(f.root,item.path))));
  }
});

test("02 reject falsified or empty checkout SHA", () => {
  const f = fixture();
  for (const hash of ["", "00", "0".repeat(40), "not-a-sha"]) {
    assert.throws(() => bindSourcesToCheckout(f.root, hash, MANIFEST), /STOP|AssertionError/);
  }
});

test("03 refuse edited worktree data even though committed blob is intact", () => {
  const f = fixture();
  fs.writeFileSync(path.join(f.root, MANIFEST[1]), "tampered-non-fictional-code\n");
  assert.throws(() => bindSourcesToCheckout(f.root, f.head, MANIFEST),
    /differs from Git blob beyond permitted Windows CRLF checkout/);
});

test("04 refuse missing tracked source instead of inventing or re-fetching", () => {
  const f = fixture();
  fs.unlinkSync(path.join(f.root, MANIFEST[2]));
  assert.throws(() => bindSourcesToCheckout(f.root, f.head, MANIFEST));
});

test("05 refuse added normal App source in manifest", () => {
  const f = fixture();
  assert.throws(() => bindSourcesToCheckout(f.root, f.head, [...MANIFEST, "src/App.tsx"]),
    /exact fictional-only manifest/);
});

test("06 refuse missing, repeated, or reordered wrong manifest entries", () => {
  const f = fixture();
  assert.throws(() => bindSourcesToCheckout(f.root, f.head, MANIFEST.slice(0, -1)),
    /exact fictional-only manifest/);
  assert.throws(() => bindSourcesToCheckout(f.root, f.head, [...MANIFEST, MANIFEST[0]]),
    /duplicate source path/);
});

test("07 refuse checkout movement after a second synthetic commit", () => {
  const f = fixture();
  fs.writeFileSync(path.join(f.root, MANIFEST[0]), "second synthetic commit\n");
  git(f.root, "add", "--", MANIFEST[0]);
  git(f.root, "-c", "user.name=CI fictional fixture", "-c",
    "user.email=fictional-fixture@example.invalid", "commit", "-qm", "second");
  assert.throws(() => bindSourcesToCheckout(f.root, f.head, MANIFEST),
    /Git HEAD differs/);
});

test("08 returned buffer modifications cannot alter remembered Git bytes", () => {
  const f = fixture();
  const bound = bindSourcesToCheckout(f.root, f.head, MANIFEST);
  const first = bound.source(MANIFEST[0]);
  first.fill(0);
  const again = bound.source(MANIFEST[0]);
  assert.notDeepEqual(first, again);
  assert.equal(createHash("sha256").update(again).digest("hex"),
    bound.inventory.find(x=>x.path===MANIFEST[0]).sha256);
});

test("09 permitted CRLF Windows checkout still stages the immutable LF Git blob", () => {
  const f = fixture();
  const rel = MANIFEST[0];
  const original = fs.readFileSync(path.join(f.root, rel), "utf8");
  assert.ok(original.includes("\n") && !original.includes("\r"));
  fs.writeFileSync(path.join(f.root, rel), original.replace(/\n/g, "\r\n"));
  const bound = bindSourcesToCheckout(f.root, f.head, MANIFEST);
  assert.equal(bound.source(rel).toString("utf8"), original);
});

test("10 refuse arbitrary carriage returns or whitespace changes", () => {
  const f = fixture();
  fs.writeFileSync(path.join(f.root, MANIFEST[0]),
    "invented-only-file:" + MANIFEST[0] + "\rMALICIOUS\n");
  assert.throws(() => bindSourcesToCheckout(f.root, f.head, MANIFEST),
    /differs from Git blob beyond permitted Windows CRLF checkout/);
  const second = fixture();
  fs.writeFileSync(path.join(second.root, MANIFEST[0]),
    "invented-only-file:" + MANIFEST[0] + " \r\n");
  assert.throws(() => bindSourcesToCheckout(second.root, second.head, MANIFEST),
    /differs from Git blob beyond permitted Windows CRLF checkout/);
});

console.log("M32_CI_GIT_BLOB_TESTS_DEFINED: fabricated disposable Git repositories; NO operator source");
