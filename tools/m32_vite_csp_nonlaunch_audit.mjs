/**
 * M3.2 fail-closed preflight evidence: Vite 8 config RESOLUTION only.
 * CI child processes evaluate trusted vite.config.ts; no createServer,
 * no listen(), no Vite/ Tauri executable, no WebView2 or SQLite.
 * This is NOT a Windows runtime exposure scan or launch authorization.
 */
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { spawnSync } from "node:child_process";
import process from "node:process";

const root = resolve(import.meta.dirname, "..");
const mode = process.argv[2];

function file(path) { return readFileSync(resolve(root, path), "utf8"); }
function json(path) { return JSON.parse(file(path)); }

function assessHost(host, port, strictPort, hmr) {
  const violations = [];
  if (host !== "127.0.0.1") violations.push("M32_EXACT_IPV4_BIND_NOT_PROVEN");
  if (port !== 1420 || strictPort !== true) violations.push("M32_PORT_DRIFT");
  if (hmr && (hmr.host !== "127.0.0.1" || hmr.port !== 1421 || hmr.protocol !== "ws")) {
    violations.push("M32_HMR_HOST_OR_PORT_DRIFT");
  }
  return violations;
}

function assessDocumentIsolation(tauri, overlay, normalHTML, labHTML) {
  const issues = [];
  const security = { ...tauri.app.security, ...overlay.app.security };
  if (security.csp == null && security.devCsp == null) {
    issues.push("M32_CSP_UNCONFIGURED");
  }
  // The normal root page can be served by the SAME Vite source root.
  if (normalHTML.includes('/src/main.tsx') && labHTML.includes('/src/m32BrowserLab.tsx')) {
    issues.push("M32_NORMAL_APP_COHOSTED_IN_VITE_ROOT");
  }
  if (overlay.build.devUrl !== "http://127.0.0.1:1420/m32-browser-lab.html") {
    issues.push("M32_TAURI_URL_DRIFT");
  }
  if (JSON.stringify(overlay.app.security.capabilities) !== JSON.stringify(["default"])) {
    issues.push("M32_CAPABILITY_DRIFT");
  }
  return issues;
}

async function probe() {
  // Vite resolveConfig runs config evaluation, NOT createServer/listen.
  const { resolveConfig } = await import("vite");
  const config = await resolveConfig({
    configFile: resolve(root, "vite.config.ts"),
    envFile: false,
    logLevel: "silent",
  }, "serve", "development");
  const data = {
    host: config.server.host,
    port: config.server.port,
    strictPort: config.server.strictPort,
    hmr: config.server.hmr ? {
      host: config.server.hmr.host,
      port: config.server.hmr.port,
      protocol: config.server.hmr.protocol,
    } : null,
    open: config.server.open,
  };
  process.stdout.write("M32_VITE_CONFIG_RESOLVED_JSON=" + JSON.stringify(data) + "\n");
}

function runProbe(host) {
  const env = { ...process.env };
  if (host === null) delete env.TAURI_DEV_HOST;
  else env.TAURI_DEV_HOST = host;
  const child = spawnSync(process.execPath, [resolve(root, "tools/m32_vite_csp_nonlaunch_audit.mjs"), "--probe"], {
    cwd: root, env, encoding: "utf8", shell: false, windowsHide: true, timeout: 45000,
  });
  assert.equal(child.status, 0, "nonlaunch Vite config resolve failed");
  const line = child.stdout.split(/\r?\n/).find(x => x.startsWith("M32_VITE_CONFIG_RESOLVED_JSON="));
  assert.ok(line, "missing Vite resolved config output");
  return JSON.parse(line.slice("M32_VITE_CONFIG_RESOLVED_JSON=".length));
}

function parent() {
  assert.equal(process.env.CI?.toLowerCase(), "true", "STOP: only disposable CI runner permitted");
  assert.equal(process.env.RUNNER_OS, "Windows", "STOP: Windows runner required");
  // Pure negative-control cases test the policy itself, independent of Vite.
  assert.deepEqual(assessHost("127.0.0.1", 1420, true, null), []);
  for (const host of [false, "localhost", "0.0.0.0", "::", "192.0.2.10", true]) {
    assert.ok(assessHost(host, 1420, true, null).includes("M32_EXACT_IPV4_BIND_NOT_PROVEN"));
  }
  assert.ok(assessHost("127.0.0.1", 1421, true, null).includes("M32_PORT_DRIFT"));
  assert.ok(assessHost("127.0.0.1", 1420, false, null).includes("M32_PORT_DRIFT"));
  assert.ok(assessHost("127.0.0.1", 1420, true, {
    host: "0.0.0.0", port: 1421, protocol: "ws",
  }).includes("M32_HMR_HOST_OR_PORT_DRIFT"));

  // Each probe starts a new Node process so TAURI_DEV_HOST cannot be cached
  // when vite.config.ts is evaluated. None starts a dev server or socket.
  const noEnv = runProbe(null);
  const loopback = runProbe("127.0.0.1");
  const wildcard = runProbe("0.0.0.0");
  assert.equal(noEnv.host, false, "default Vite host changed: re-review");
  assert.equal(loopback.host, "127.0.0.1");
  assert.equal(wildcard.host, "0.0.0.0");
  for (const config of [noEnv, loopback, wildcard]) {
    assert.equal(config.port, 1420);
    assert.equal(config.strictPort, true);
  }
  assert.deepEqual(assessHost(loopback.host, loopback.port, loopback.strictPort, loopback.hmr), []);
  assert.ok(assessHost(noEnv.host, noEnv.port, noEnv.strictPort, noEnv.hmr)
    .includes("M32_EXACT_IPV4_BIND_NOT_PROVEN"));
  assert.ok(assessHost(wildcard.host, wildcard.port, wildcard.strictPort, wildcard.hmr)
    .includes("M32_EXACT_IPV4_BIND_NOT_PROVEN"));

  const base = json("src-tauri/tauri.conf.json");
  const overlay = json("src-tauri/tauri.m32-synthetic-preview.conf.json");
  const findings = assessDocumentIsolation(base, overlay, file("index.html"), file("m32-browser-lab.html"));
  assert.ok(findings.includes("M32_CSP_UNCONFIGURED"), "unexpected CSP policy changed; requalify");
  assert.ok(findings.includes("M32_NORMAL_APP_COHOSTED_IN_VITE_ROOT"),
    "normal page cohosting model changed: requalify");
  assert.ok(!findings.includes("M32_TAURI_URL_DRIFT"));
  assert.ok(!findings.includes("M32_CAPABILITY_DRIFT"));

  // A passing AUDIT intentionally leaves the launch gate STOP.
  process.stdout.write("M32_VITE_CONFIG_RESOLUTION_SOURCE_ONLY_PASS: 3 independent Vite config evaluations\n");
  process.stdout.write("M32_SECURITY_PREFLIGHT_STOP: M32_CSP_UNCONFIGURED; M32_NORMAL_APP_COHOSTED_IN_VITE_ROOT; wildcard TAURI_DEV_HOST may expose Vite\n");
  process.stdout.write("TAURI_RUNTIME_NOT_TESTED; OPERATOR_ACCEPTANCE_NOT_PERFORMED; REAL_G3_STOP_UNAVAILABLE\n");
}

if (mode === "--probe") {
  await probe();
} else if (mode === "--audit") {
  parent();
} else {
  throw Error("STOP: explicit --audit / internal --probe required");
}
