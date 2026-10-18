"use strict";

/** Static, precompiled, fictional-only HTTP server for ephemeral Windows CI.
 * Serves EXACTLY one invented HTML entry and compiled hashed JS/CSS assets.
 * No Tauri, WebView2, normal App, DB, IPC or user Windows processes.
 */
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const http = require("node:http");
const { allowed, pinStaticBytes } = require("./m32_ci_static_byte_snapshot.cjs");

assert.equal(process.env.CI?.toLowerCase(), "true", "STOP: static fixture server CI only");
assert.equal(process.env.RUNNER_OS, "Windows", "STOP: Windows runner only");
assert.ok(typeof process.send === "function",
  "STOP: static fixture requires private parent/child IPC");
assert.ok(/^[a-f0-9]{32}$/.test(process.env.M32_CI_READY_NONCE || ""),
  "STOP: static fixture requires parent-provided ephemeral nonce");
assert.equal(process.env.TAURI_DEV_HOST, undefined, "STOP: unexpected inherited host");
assert.equal(process.env.__VITE_ADDITIONAL_SERVER_ALLOWED_HOSTS, undefined,
  "STOP: unexpected additional Vite host allowance");

const root = path.resolve(__dirname, "..");
const stage = process.env.M32_CI_FIXTURE_STAGE;
if (!stage || !path.isAbsolute(stage)) throw Error("STOP: no staged fictional root");
const canonicalStage = fs.realpathSync(stage);
if (path.dirname(canonicalStage) !== root ||
    !path.basename(canonicalStage).startsWith(".m32-fixture-only-") ||
    fs.lstatSync(stage).isSymbolicLink()) {
  throw Error("STOP: source stage outside ephemeral checkout");
}
const out = path.join(canonicalStage, "dist-static");
if (!fs.existsSync(out) || !fs.statSync(out).isDirectory() || fs.lstatSync(out).isSymbolicLink()) {
  throw Error("STOP: no genuine precompiled static output");
}
const csp = [
  "default-src 'none'",
  "script-src 'self'",
  "style-src 'self'",
  "connect-src 'none'",
  "img-src 'self' data:",
  "font-src 'self'",
  "object-src 'none'",
  "frame-src 'none'",
  "frame-ancestors 'none'",
  "base-uri 'none'",
  "form-action 'none'",
  "worker-src 'none'",
  "manifest-src 'none'",
].join("; ");

function walk(directory) {
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const localPath = path.join(directory, entry.name);
    if (entry.isSymbolicLink()) throw Error("STOP: static bundle symlink");
    if (entry.isDirectory()) walk(localPath);
    else if (entry.isFile()) {
      const relative = path.relative(out, localPath).replaceAll("\\", "/");
      assert.ok(allowed(relative), "STOP: unexpected output file: " + relative);
      assert.ok(fs.statSync(localPath).size > 0, "STOP: empty output " + relative);
    } else throw Error("STOP: unusual bundle entry");
  }
}
walk(out);
const pinned = pinStaticBytes(out);
const html = pinned.get("m32-browser-lab.html").body.toString("utf8");
console.log("M32_CI_STATIC_BYTES_PINNED_PASS: " + pinned.inventory.length +
  " resources SHA256-pinned in RAM; no HTTP disk reopens");
assert.ok(/<script\s+[^>]*src=["']\/assets\/[^"']+\.js["']/i.test(html),
  "STOP: fictional bundle JS not externalized");
assert.ok(!/<script(?:\s[^>]*)?>[\s\S]*?<\/script>/i.test(
  html.replace(/<script\s+[^>]*src=["'][^"']+["'][^>]*><\/script>/gi, "")),
  "STOP: inline script in static HTML");
assert.ok(!/<style\b/i.test(html) && !/\son[a-z]+\s*=/i.test(html),
  "STOP: inline CSS or event handler in static HTML");
assert.ok(!html.includes("/src/main.tsx") && !html.includes("/src/App.tsx"),
  "STOP: normal App reference in built HTML");
assert.ok(!csp.includes("unsafe-inline") && !csp.includes("unsafe-eval"),
  "STOP: lax static CSP");

const { requestAuthorityAllowed } = require("./m32_ci_http_authority.cjs");
const server = http.createServer((req, res) => {
  if (!requestAuthorityAllowed(req.headers, req.url, req.rawHeaders)) {
    res.writeHead(403, { "Content-Type": "text/plain", "Cache-Control": "no-store" });
    res.end("Forbidden"); return;
  }
  const pathname = (req.url || "").split("?")[0];
  // No URL decoding, aliases, directory indexes, SPA fallback, redirects,
  // proxy, filesystem exploration or API endpoints.
  const relative = pathname.startsWith("/") ? pathname.slice(1) : "";
  if (req.method !== "GET" && req.method !== "HEAD") {
    res.writeHead(405, { "Content-Type": "text/plain" }); res.end("Method Not Allowed"); return;
  }
  if (!allowed(relative)) {
    res.writeHead(404, { "Content-Type": "text/plain" }); res.end("Not Found"); return;
  }
  const resource = pinned.get(relative);
  if (!resource) {
    res.writeHead(404, { "Content-Type": "text/plain" }); res.end("Not Found"); return;
  }
  const type = relative.endsWith(".html") ? "text/html; charset=utf-8" :
    relative.endsWith(".css") ? "text/css; charset=utf-8" : "text/javascript; charset=utf-8";
  res.writeHead(200, {
    "Content-Type": type,
    "Content-Security-Policy": csp,
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "no-referrer",
    "Cache-Control": "no-store",
    // CI-local consistency metadata only; not a provenance attestation.
    "X-M32-Local-SHA256": resource.sha256,
  });
  res.end(req.method === "HEAD" ? undefined : resource.body);
});
server.on("error", error => { console.error("M32_STATIC_SERVER_FAIL", error.code); process.exitCode = 1; });
server.listen(14279, "127.0.0.1", () => {
  process.send({
    type: "M32_CI_STATIC_LISTENING", host: "127.0.0.1",
    port: 14279, pid: process.pid, nonce: process.env.M32_CI_READY_NONCE,
  });
  console.log("M32_STATIC_FICTIONAL_LOOPBACK_READY: 127.0.0.1:14279; strict CSP; no inline");
});
