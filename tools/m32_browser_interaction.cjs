"use strict";

/* Isolated REAL Chromium interaction suite for invented Fabulaxiom M3.2 data.
 * Windows CI only. The launched Vite page is NOT production App.tsx.
 * Playwright is installed into RUNNER_TEMP, never into this repository.
 * No original database access, IPC, network destination outside loopback.
 */
const assert = require("node:assert/strict");
const path = require("node:path");
const { createHash, randomBytes } = require("node:crypto");
const { createOwnedReadyGate } = require("./m32_ci_owned_child_ready.cjs");
const { spawn, spawnSync } = require("node:child_process");
const { setTimeout: sleep } = require("node:timers/promises");
const { stageFictionOnly } = require("./m32_ci_fixture_stage.cjs");

const root = path.resolve(__dirname, "..");
const playwrightPath = process.env.FABULAXIOM_M32_PLAYWRIGHT_MODULE;
if (!playwrightPath || !path.isAbsolute(playwrightPath)) {
  throw new Error("Expected explicit ephemeral absolute Playwright module directory");
}
const { chromium } = require(playwrightPath);
const stage = stageFictionOnly();
const staticMode = process.env.M32_CI_PRECOMPILED === "1";
const port = "14279";
const url = "http://127.0.0.1:" + port + "/m32-browser-lab.html";
const cases = [];
const errors = [];
const unsafeNetwork = [];
const env = { ...process.env, M32_CI_FIXTURE_STAGE: stage };
const staticNonce = staticMode ? randomBytes(16).toString("hex") : null;
if (staticMode) env.M32_CI_READY_NONCE = staticNonce;
if (staticMode) {
  const build = spawnSync(process.execPath, [
    path.join(root, "node_modules", "vite", "bin", "vite.js"),
    "build", "--config", path.join(root, "vite.m32-ci-isolated.config.mts"),
  ], { cwd: root, env, shell: false, encoding: "utf8",
    windowsHide: true, timeout: 120000, maxBuffer: 10 * 1024 * 1024 });
  assert.equal(build.status, 0, "STOP: fictional-only Vite build failed: " +
    (build.stderr || build.stdout || build.error || "unknown"));
  console.log("M32_CI_PRECOMPILED_FICTION_ONLY_BUILD_PASS");
}
const server = spawn(
  process.execPath,
  staticMode
    ? [path.join(root, "tools", "m32_ci_precompiled_server.cjs")]
    : [path.join(root, "node_modules", "vite", "bin", "vite.js"),
      "--config", path.join(root, "vite.m32-ci-isolated.config.mts"),
      "--port", port, "--strictPort"],
  { cwd: root, stdio: staticMode ? ["ignore", "pipe", "pipe", "ipc"] : "pipe",
    shell: false, windowsHide: true, env },
);
server.on("error", e => errors.push(String(e)));
const ownedReady = staticMode ? createOwnedReadyGate(server.pid, staticNonce) : null;
if (staticMode) server.on("message", msg => ownedReady.observe(msg));
// The fixture-only child logs its RAM pinning marker. Pipe it through the
// Chromium CI driver so acceptance never relies on hidden subprocess output.
let staticPinMarkerSeen = false;
let staticPinOutput = "";
server.stdout.on("data", chunk => {
  if (!staticMode) return;
  staticPinOutput += chunk.toString("utf8");
  if (staticPinOutput.includes("M32_CI_STATIC_BYTES_PINNED_PASS")) {
    staticPinMarkerSeen = true;
  }
  if (staticPinOutput.length > 16000) staticPinOutput = staticPinOutput.slice(-8000);
});

async function awaitLocalServer() {
  for (let n = 0; n < 70; n += 1) {
    if (server.exitCode !== null || server.signalCode !== null || errors.length) {
      throw new Error("STOP: own fixture child exited or failed before browser test");
    }
    if (staticMode) {
      const witness = ownedReady.status();
      if (witness.error) throw new Error("STOP: child IPC witness invalid: " + witness.error);
      if (!witness.ready) { await sleep(350); continue; }
    }
    try {
      const response = await fetch(url, { signal: AbortSignal.timeout(900) });
      if (response.ok) {
        if (staticMode && (!ownedReady.status().ready || server.exitCode !== null)) {
          throw Error("STOP: own server no longer owns a live IPC witness");
        }
        return;
      }
    } catch {
      // A short, bounded loopback-only probe during Vite startup.
    }
    await sleep(350);
  }
  throw new Error("Synthetic Vite server did not start on loopback");
}

async function assertNormalAppNotServed() {
  const normal = [
    "/", "/index.html", "/src/main.tsx", "/src/App.tsx",
    "/@fs/" + path.join(root, "index.html").replaceAll("\\", "/"),
    "/@fs/" + path.join(root, "src", "App.tsx").replaceAll("\\", "/"),
  ];
  for (const suffix of normal) {
    const response = await fetch("http://127.0.0.1:" + port + suffix, {
      redirect: "manual", signal: AbortSignal.timeout(5000),
    });
    assert.notEqual(response.status, 200,
      "STOP: normal App content reachable through isolated Vite root at " + suffix);
  }
  if (staticMode) {
    for (const headers of [
      { Host: "evil.invalid:14279" },
      { Origin: "https://evil.invalid" },
      { "X-Forwarded-Host": "evil.invalid" },
      { "Sec-Fetch-Site": "cross-site" },
    ]) {
      // Use raw Node HTTP to send exact adversarial Host/Origin bytes.
      // fetch() may normalize or silently replace restricted Host headers.
      const forbidden = await new Promise((resolve, reject) => {
        const http = require("node:http");
        const request = http.request(url, { method: "GET", headers, timeout: 5000 }, response => {
          response.resume();
          response.on("end", () => resolve(response.statusCode));
        });
        request.on("error", reject);
        request.on("timeout", () => request.destroy(new Error("HTTP veto timeout")));
        request.end();
      });
      assert.equal(forbidden, 403,
        "STOP: static server accepted hostile HTTP authority: " + JSON.stringify(headers));
    }
    console.log("M32_CI_HTTP_AUTHORITY_DENIAL_PASS: 4 real loopback HTTP vetoes");
    // Raw TCP is essential: node:http clients may normalize security headers.
    // Node's parser may reject a malformed duplicate first (400); the fixture
    // policy must reject any duplicate that reaches request handling (403).
    const net = require("node:net");
    async function rawStatus(lines) {
      return await new Promise((resolve, reject) => {
        let settled = false;
        const socket = net.createConnection({ host: "127.0.0.1", port: 14279 });
        const done = (error, status) => {
          if (settled) return;
          settled = true;
          socket.destroy();
          if (error) reject(error); else resolve(status);
        };
        let buffer = "";
        socket.setTimeout(5000, () => done(new Error("raw HTTP veto timeout")));
        socket.on("connect", () => socket.write(
          "GET /m32-browser-lab.html HTTP/1.1\r\n" +
          lines.join("\r\n") + "\r\nConnection: close\r\n\r\n"));
        socket.on("data", bytes => {
          buffer += bytes.toString("latin1");
          if (buffer.includes("\r\n")) {
            const match = /^HTTP\/1\.[01] ([0-9]{3})/.exec(buffer);
            done(match ? null : new Error("missing HTTP status"), match && Number(match[1]));
          }
        });
        socket.on("error", error => done(error));
        socket.on("close", () => {
          if (!settled) done(new Error("server closed without status"));
        });
      });
    }
    const casesRaw = [
      ["Host: 127.0.0.1:14279", "hOsT: evil.invalid:14279"],
      ["Host: 127.0.0.1:14279", "Origin: http://127.0.0.1:14279",
        "origin: https://evil.invalid"],
      ["Host: 127.0.0.1:14279", "Sec-Fetch-Site: same-origin",
        "sec-fetch-site: cross-site"],
    ];
    for (const headers of casesRaw) {
      const status = await rawStatus(headers);
      assert.ok(status === 400 || status === 403,
        "STOP: ambiguous raw HTTP request accepted: " + status);
    }
    console.log("M32_CI_HTTP_RAW_DUPLICATE_DENIAL_PASS: 3 real loopback raw header vetoes");

  }
  const allowed = await fetch(url, { signal: AbortSignal.timeout(5000) });
  assert.equal(allowed.status, 200, "STOP: fictional lab unavailable");
  const csp = allowed.headers.get("content-security-policy");
  assert.ok(csp, "STOP: fictional HTML served WITHOUT CSP");
  for (const directive of [
    "default-src 'none'",
    staticMode ? "script-src 'self'" : "script-src 'self' 'unsafe-inline'",
    staticMode ? "style-src 'self'" : "style-src 'self' 'unsafe-inline'",
    staticMode ? "connect-src 'none'" : "connect-src 'self' ws://127.0.0.1:14279",
    "object-src 'none'", "frame-ancestors 'none'",
    "base-uri 'none'", "form-action 'none'",
  ]) {
    assert.ok(csp.includes(directive), "STOP: CSP missing directive " + directive);
  }
  assert.ok(!csp.includes("https:") && !csp.includes("http:") &&
    !csp.includes("wss:") && !csp.includes("0.0.0.0"),
    "STOP: non-loopback or broad origin in lab CSP");
  assert.equal(allowed.headers.get("x-content-type-options"), "nosniff");
  assert.equal(allowed.headers.get("referrer-policy"), "no-referrer");
  if (staticMode) {
    assert.ok(!csp.includes("unsafe-inline") && !csp.includes("unsafe-eval"),
      "STOP: static bundle CSP must forbid inline code and eval");
    console.log("M32_CI_PRECOMPILED_NO_INLINE_CSP_HEADER_PASS");
  } else {
    console.log("M32_CI_CSP_HEADER_SOURCE_PASS: local-only script/connect; dev inline concession");
  }
  const htmlBytes = Buffer.from(await allowed.arrayBuffer());
  const html = htmlBytes.toString("utf8");
  if (staticMode) {
    const actual = createHash("sha256").update(htmlBytes).digest("hex");
    assert.equal(allowed.headers.get("x-m32-local-sha256"), actual,
      "STOP: static HTML bytes do not match the pinned local digest");
    const jsRef = html.match(/\/assets\/[A-Za-z0-9_.-]+\.js/);
    assert.ok(jsRef, "STOP: no compiled JS source in fictional HTML");
    const jsResponse = await fetch("http://127.0.0.1:" + port + jsRef[0], {
      signal: AbortSignal.timeout(5000),
    });
    assert.equal(jsResponse.status, 200, "STOP: compiled script absent");
    const scriptBody = Buffer.from(await jsResponse.arrayBuffer());
    assert.equal(jsResponse.headers.get("x-m32-local-sha256"),
      createHash("sha256").update(scriptBody).digest("hex"),
      "STOP: served JS bytes and local digest mismatch");
    console.log("M32_CI_STATIC_HTTP_DIGEST_PASS: pinned fictional HTML and JS consistent");
  }
  assert.ok(staticMode ? /\/assets\/[^"']+\.js/.test(html)
    : html.includes("m32BrowserLab.tsx"), "STOP: unexpected HTML entry");
  assert.ok(!html.includes('src/main.tsx'), "STOP: production entry leaked");
  console.log("M32_CI_VITE_NORMAL_ROUTES_DENIED_PASS: " + normal.length + " routes");
}

async function run() {
  let browser;
  try {
    await awaitLocalServer();
    if (staticMode) {
      assert.deepEqual(ownedReady.status(), { ready: true, error: null },
        "STOP: no confirmed direct child process listening");
      console.log("M32_CI_OWNED_STATIC_CHILD_READY_PASS: direct child IPC after listen; CI-local only");
      for (let i = 0; i < 25 && !staticPinMarkerSeen; i += 1) {
        await sleep(50);
      }
      assert.ok(staticPinMarkerSeen,
        "STOP: static server did not emit RAM pinning evidence");
      console.log("M32_CI_STATIC_BYTES_PINNED_PASS: child startup evidence observed by Chromium driver");
    }
    await assertNormalAppNotServed();
    browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();
    page.on("pageerror", err => errors.push(err.message));
    page.on("request", req => {
      if (!req.url().startsWith("http://127.0.0.1:" + port + "/")) {
        unsafeNetwork.push(req.url());
      }
    });
    const first = () => page.getByRole("combobox", { name: "Premier événement" });
    const second = () => page.getByRole("combobox", { name: "Deuxième événement" });
    async function fresh() {
      await page.goto(url, { waitUntil: "networkidle" });
      assert.equal(await page.locator("#m32-browser-lab-root").count(), 1);
      assert.equal(await first().inputValue(), "");
      assert.equal(await second().inputValue(), "");
    }
    async function caseRun(name, action) {
      await fresh();
      await action();
      if (errors.length || unsafeNetwork.length) {
        throw new Error("JS/runtime/network failure: " +
          JSON.stringify({ errors, unsafeNetwork }));
      }
      cases.push(name);
      console.log("M32_BROWSER_CASE_PASS " + name);
    }
    await caseRun("01-no-default-pair", async () => {
      assert.equal(await page.getByText("Choisissez les deux événements", { exact: false }).count(), 1);
      assert.equal(await page.getByRole("region", { name: "Justification des précédences" }).count(), 0);
      assert.equal(await first().count(), 1);
      assert.equal(await second().count(), 1);
    });
    await caseRun("02-direct-human-witness", async () => {
      await first().selectOption("A");
      await second().selectOption("B");
      assert.equal(await page.getByText("Avant : précédence humaine explicite ou transitive").isVisible(), true);
      assert.equal(await page.getByRole("region", { name: "Justification des précédences" }).getByText("Le messager arrive", { exact: false }).count(), 1);
      assert.equal(await page.getByRole("region", { name: "Justification des précédences" }).getByText("La porte s'ouvre", { exact: false }).count(), 0);
    });
    await caseRun("03-transitive-human-witness", async () => {
      await first().selectOption("A");
      await second().selectOption("C");
      assert.equal(await page.getByRole("region", { name: "Justification des précédences" }).count(), 1);
      assert.equal(await page.getByRole("region", { name: "Justification des précédences" }).getByText("Le messager arrive", { exact: false }).count(), 1);
      assert.equal(await page.getByRole("region", { name: "Justification des précédences" }).getByText("La porte s'ouvre", { exact: false }).count(), 1);
      assert.equal(await page.getByText("Avant : précédence humaine explicite ou transitive").isVisible(), true);
    });
    await caseRun("04-reverse-after", async () => {
      await first().selectOption("C");
      await second().selectOption("A");
      assert.equal(await page.getByText("Après : précédence humaine explicite ou transitive").isVisible(), true);
    });
    await caseRun("05-identical-source", async () => {
      await first().selectOption("B");
      await second().selectOption("B");
      assert.equal(await page.getByText("Même assertion : identité exacte", { exact: false }).count(), 1);
      assert.equal(await page.getByRole("region", { name: "Justification des précédences" }).count(), 0);
    });
    await caseRun("06-incomparable-revoked-edge", async () => {
      await first().selectOption("A");
      await second().selectOption("D");
      assert.equal(await page.getByText("Ordre indéterminé", { exact: false }).count(), 1);
      assert.equal(await page.getByRole("region", { name: "Justification des précédences" }).count(), 0);
    });
    await caseRun("07-change-selection-refreshes-proof", async () => {
      await first().selectOption("A");
      await second().selectOption("C");
      assert.equal(await page.getByRole("region", { name: "Justification des précédences" }).getByText("La porte s'ouvre", { exact: false }).count(), 1);
      await second().selectOption("B");
      assert.equal(await page.getByRole("region", { name: "Justification des précédences" }).getByText("La porte s'ouvre", { exact: false }).count(), 0);
      assert.equal(await page.getByRole("region", { name: "Justification des précédences" }).getByText("Le messager arrive", { exact: false }).count(), 1);
    });
    await caseRun("08-clearing-explicit-choice", async () => {
      await first().selectOption("A");
      await second().selectOption("C");
      await second().selectOption("");
      assert.equal(await second().inputValue(), "");
      assert.equal(await page.getByText("Choisissez les deux événements", { exact: false }).count(), 1);
      assert.equal(await page.getByRole("region", { name: "Justification des précédences" }).count(), 0);
    });
    await caseRun("09-retired-identities-unselectable", async () => {
      assert.equal(await first().locator('option[value="retired"]').count(), 0);
      assert.equal(await second().locator('option[value="escape-demo"]').count(), 0);
      assert.equal(await page.getByText("Révoquée (historique)", { exact: false }).count() > 0, true);
    });
    await caseRun("10-keyboard-focus-and-native-arrow", async () => {
      await first().focus();
      assert.equal(await first().evaluate(el => el === document.activeElement), true);
      // Test Tab navigation while the native select popup is CLOSED.
      // Opening/committing a Windows native-select dropdown before pressing
      // Tab may consume Tab to dismiss the popup rather than advance focus.
      await page.keyboard.press("Tab");
      assert.equal(await second().evaluate(el => el === document.activeElement), true);
      await second().press("ArrowDown");
      await second().press("Enter");
      assert.equal(await second().inputValue(), "A");
      await first().press("ArrowDown");
      await first().press("Enter");
      assert.equal(await first().inputValue(), "A");
      assert.equal(await page.getByText("Même assertion : identité exacte", { exact: false }).count(), 1);
    });
    await caseRun("11-fictional-scenario-switch-resets-state", async () => {
      await first().selectOption("A");
      await second().selectOption("C");
      await page.getByRole("button", { name: "Charger un autre univers fictif" }).click();
      assert.equal(await first().inputValue(), "");
      assert.equal(await second().inputValue(), "");
      assert.equal(await first().locator('option[value="K"]').count(), 1);
      assert.equal(await first().locator('option[value="A"]').count(), 0);
      assert.equal(await page.getByRole("region", { name: "Justification des précédences" }).count(), 0);
    });
    await caseRun("12-return-to-original-stays-unselected", async () => {
      await page.getByRole("button", { name: "Charger un autre univers fictif" }).click();
      await first().selectOption("K");
      await second().selectOption("L");
      await page.getByRole("button", { name: "Revenir au premier univers fictif" }).click();
      assert.equal(await first().inputValue(), "");
      assert.equal(await second().inputValue(), "");
      assert.equal(await first().locator('option[value="A"]').count(), 1);
    });
    await caseRun("13-active-cycle-refuses-all-content", async () => {
      await page.getByRole("button", { name: "Charger un cycle fictif invalide" }).click();
      assert.equal(await page.getByRole("alert", { name: "Consultation M3.2 refusée" }).count(), 1);
      assert.equal(await page.getByText("Troisième cloche").count(), 0);
      assert.equal(await page.getByRole("combobox").count(), 0);
      assert.equal(await page.getByText("Le messager arrive", { exact: false }).count(), 0);
    });
    await caseRun("14-script-like-fixture-text-escaped", async () => {
      assert.equal(await page.locator("script:has-text('not executable()')").count(), 0);
      assert.equal(await page.getByText("<script>not executable()</script>", { exact: false }).count(), 1);
    });

    async function explore() {
      await page.getByRole("button", { name: "Afficher l'explorateur fictif" }).click();
      assert.equal(await page.getByRole("region", { name: "Explorateur M3.2 fictif filtrable" }).count(), 1);
    }
    const searchField = () => page.getByRole("searchbox", { name: "Filtrer les événements" });
    const statuses = () => page.getByRole("combobox", { name: "Filtre de statut" });
    const filteredList = () => page.getByRole("list", { name: "Événements filtrés" });
    await caseRun("15-explorer-first-page-eight-visible-ids", async () => {
      await explore();
      assert.equal(await filteredList().getByRole("listitem").count(), 8);
      assert.equal(await page.getByText("25 assertions correspondantes", { exact: false }).count(), 1);
      assert.equal(await page.getByText("Page 1 sur 4", { exact: false }).count(), 1);
      assert.equal(await first().inputValue(), "");
    });
    await caseRun("16-search-id-select-second-only", async () => {
      await explore();
      await searchField().fill(" n17 ");
      assert.equal(await filteredList().getByRole("listitem").count(), 1);
      await page.getByRole("button", { name: "Choisir N17 comme deuxième événement" }).click();
      assert.equal(await second().inputValue(), "N17");
      assert.equal(await first().inputValue(), "");
      assert.equal(await page.getByRole("region", { name: "Résumé de justification de comparaison" }).count(), 0);
    });
    await caseRun("17-page-navigation-and-query-reset", async () => {
      await explore();
      await page.getByRole("button", { name: "Page suivante" }).click();
      assert.equal(await page.getByText("Page 2 sur 4", { exact: false }).count(), 1);
      await searchField().fill("N19");
      assert.equal(await page.getByText("Page 1 sur 1", { exact: false }).count(), 1);
      assert.equal(await filteredList().getByRole("listitem").count(), 1);
      assert.equal(await page.getByRole("button", { name: "Page précédente" }).isDisabled(), true);
    });
    await caseRun("18-historical-filter-retains-display-denies-selection", async () => {
      await explore();
      await statuses().selectOption("historical");
      assert.equal(await filteredList().getByRole("listitem").count(), 2);
      assert.equal(await filteredList().getByRole("button").count(), 0);
      assert.equal(await filteredList().getByText("retired", { exact: false }).count() > 0, true);
    });
    await caseRun("19-fictional-title-query-does-not-confuse-id", async () => {
      await explore();
      await searchField().fill("Troisième");
      assert.equal(await filteredList().getByRole("listitem").count(), 1);
      assert.equal(await page.getByRole("button", { name: "Choisir A comme premier événement" }).count(), 1);
      assert.equal(await page.getByRole("button", { name: "Choisir B comme premier événement" }).count(), 0);
    });
    await caseRun("20-select-across-filters-and-retain-edge-witness", async () => {
      await explore();
      await searchField().fill("Troisième");
      await page.getByRole("button", { name: "Choisir A comme premier événement" }).click();
      await searchField().fill("C");
      await page.getByRole("button", { name: "Choisir C comme deuxième événement" }).click();
      const proof = page.getByRole("region", { name: "Résumé de justification de comparaison" });
      assert.equal(await proof.getByRole("list", { name: "Chaîne de précédence sélectionnée" }).getByRole("listitem").count(), 2);
      assert.equal(await proof.getByText("Le messager arrive", { exact: false }).count(), 1);
      assert.equal(await proof.getByText("La porte s'ouvre", { exact: false }).count(), 1);
      await searchField().fill("N19");
      assert.equal(await first().inputValue(), "A");
      assert.equal(await second().inputValue(), "C");
      assert.equal(await proof.getByText("La porte s'ouvre", { exact: false }).count(), 1);
    });
    await caseRun("21-clear-selection-removes-proof-but-not-filter", async () => {
      await explore();
      await page.getByRole("button", { name: "Choisir A comme premier événement" }).click();
      await page.getByRole("button", { name: "Choisir C comme deuxième événement" }).click();
      await second().selectOption("");
      assert.equal(await page.getByRole("region", { name: "Résumé de justification de comparaison" }).count(), 0);
      assert.equal(await first().inputValue(), "A");
    });
    await caseRun("22-fictional-universe-switch-resets-all-filters-and-pair", async () => {
      await explore();
      await searchField().fill("Troisième");
      await page.getByRole("button", { name: "Choisir A comme premier événement" }).click();
      await page.getByRole("button", { name: "Charger un autre univers fictif" }).click();
      assert.equal(await searchField().inputValue(), "");
      assert.equal(await first().inputValue(), "");
      assert.equal(await second().inputValue(), "");
      assert.equal(await filteredList().getByRole("listitem").count(), 2);
    });
    await caseRun("23-cycle-veto-before-list-or-selections", async () => {
      await explore();
      await page.getByRole("button", { name: "Charger un cycle fictif invalide" }).click();
      assert.equal(await page.getByRole("alert", { name: "Explorateur M3.2 refusé" }).count(), 1);
      assert.equal(await filteredList().count(), 0);
      assert.equal(await page.getByRole("combobox", { name: "Premier événement" }).count(), 0);
    });

    await caseRun("24-accessible-search-landmark-and-live-status", async () => {
      await explore();
      assert.equal(await page.getByRole("search", {
        name: "Recherche dans la chronologie fictive",
      }).count(), 1);
      assert.equal(await page.getByRole("status", { name: "Résultat du filtrage" }).count(), 1);
      assert.equal(await page.getByRole("status", { name: "Événements choisis" }).count(), 1);
      assert.equal(await page.getByRole("status", { name: "Événements choisis" })
        .getAttribute("aria-atomic"), "true");
    });
    await caseRun("25-pressed-state-reflects-two-explicit-choices", async () => {
      await explore();
      const a = page.getByRole("button", { name: "Choisir A comme premier événement" });
      const b = page.getByRole("button", { name: "Choisir B comme deuxième événement" });
      assert.equal(await a.getAttribute("aria-pressed"), "false");
      assert.equal(await b.getAttribute("aria-pressed"), "false");
      await a.click();
      await b.click();
      assert.equal(await a.getAttribute("aria-pressed"), "true");
      assert.equal(await b.getAttribute("aria-pressed"), "true");
      assert.equal(await page.getByRole("status", { name: "Événements choisis" })
        .innerText().then(s => s.includes("Premier : A") && s.includes("deuxième : B")), true);
    });
    await caseRun("26-announces-changing-query-count-without-taking-focus", async () => {
      await explore();
      await searchField().focus();
      await searchField().fill("N19");
      const result = page.getByRole("status", { name: "Résultat du filtrage" });
      assert.equal(await result.innerText().then(s => s.includes("1 assertions correspondantes")), true);
      assert.equal(await searchField().evaluate(el => el === document.activeElement), true);
      await searchField().fill("not-an-event");
      assert.equal(await result.innerText().then(s => s.includes("0 assertions correspondantes")), true);
      assert.equal(await searchField().evaluate(el => el === document.activeElement), true);
    });
    await caseRun("27-visible-keyboard-focus-and-44px-targets", async () => {
      await explore();
      await searchField().focus();
      const focus = await searchField().evaluate(el => {
        const styles = getComputedStyle(el);
        return { kind: styles.outlineStyle, width: parseFloat(styles.outlineWidth) };
      });
      assert.equal(focus.kind, "solid");
      assert.equal(focus.width >= 3, true);
      const controls = [
        searchField(),
        statuses(),
        page.getByRole("button", { name: "Choisir A comme premier événement" }),
        page.getByRole("button", { name: "Page suivante" }),
      ];
      for (const control of controls) {
        const height = await control.evaluate(el => el.getBoundingClientRect().height);
        assert.equal(height >= 44, true);
      }
    });
    await caseRun("28-mobile-375px-explorer-does-not-overflow-its-panel", async () => {
      await page.setViewportSize({ width: 375, height: 800 });
      await explore();
      const panel = page.getByRole("region", { name: "Explorateur M3.2 fictif filtrable" });
      const width = await panel.evaluate(el => ({
        scroll: el.scrollWidth, client: el.clientWidth,
      }));
      assert.equal(width.scroll <= width.client + 2, true,
        "Explorer panel overflow on narrow mobile viewport: " + JSON.stringify(width));
      assert.equal(await searchField().isVisible(), true);
      await page.setViewportSize({ width: 1280, height: 720 });
    });
    await caseRun("29-history-filter-preserves-current-pair-announcements", async () => {
      await explore();
      await page.getByRole("button", { name: "Choisir A comme premier événement" }).click();
      await page.getByRole("button", { name: "Choisir C comme deuxième événement" }).click();
      const status = page.getByRole("status", { name: "Événements choisis" });
      await statuses().selectOption("historical");
      assert.equal(await status.innerText().then(s => s.includes("Premier : A") && s.includes("deuxième : C")), true);
      assert.equal(await filteredList().getByRole("button").count(), 0);
      const witness = page.getByRole("region", { name: "Résumé de justification de comparaison" });
      assert.equal(await witness.getByRole("list", { name: "Chaîne de précédence sélectionnée" })
        .getByRole("listitem").count(), 2);
    });
    await caseRun("30-manual-fictional-anchor-added-without-persistence", async () => {
      await page.getByRole("button", { name: "Ouvrir l'atelier manuel fictif" }).click();
      const lab = page.getByRole("region", { name: "Atelier manuel M3.2 exclusivement fictif" });
      assert.equal(await lab.count(), 1);
      await lab.getByRole("button", { name: "Ajouter l'ancre" }).click();
      assert.ok(await lab.getByText("fiction-draft-0001", { exact: false }).count() >= 1);
      assert.equal(await lab.getByRole("status").filter({ hasText: "Ancre fictive créée" }).count(), 1);
    });
    await caseRun("31-manual-fictitious-cycle-rejected-before-commit", async () => {
      await page.getByRole("button", { name: "Ouvrir l'atelier manuel fictif" }).click();
      const lab = page.getByRole("region", { name: "Atelier manuel M3.2 exclusivement fictif" });
      await lab.getByRole("combobox", { name: "Événement antérieur" }).selectOption("C");
      await lab.getByRole("combobox", { name: "Événement postérieur" }).selectOption("A");
      await lab.getByRole("textbox", { name: "Justification humaine fictive" }).fill("Cycle fictif refusé");
      await lab.getByRole("button", { name: "Ajouter avant/après" }).click();
      assert.ok((await lab.getByRole("alert").innerText()).includes("cycle temporel"));
      assert.equal(await lab.getByText("Cycle fictif refusé", { exact: true }).count(), 0);
    });
    await caseRun("32-invalid-cycle-fixture-refuses-manual-form", async () => {
      await page.getByRole("button", { name: "Charger un cycle fictif invalide" }).click();
      await page.getByRole("button", { name: "Ouvrir l'atelier manuel fictif" }).click();
      assert.equal(await page.getByRole("heading", { name: "Atelier fictif refusé" }).count(), 1);
      assert.equal(await page.getByRole("button", { name: "Ajouter l'ancre" }).count(), 0);
    });
    await caseRun("33-explicit-historical-scene-revision-select-and-create", async () => {
      await page.getByRole("button", { name: "Ouvrir l'atelier manuel fictif" }).click();
      const lab = page.getByRole("region", { name: "Atelier manuel M3.2 exclusivement fictif" });
      await lab.getByRole("combobox", { name: "Scène inventée à citer (facultatif)" }).selectOption("s1");
      await lab.getByRole("combobox", { name: "Révision exacte et immuable de cette scène" })
        .selectOption("invented-rev-B");
      await lab.getByRole("button", { name: "Ajouter l'ancre" }).click();
      assert.equal(await lab.getByText("Ancre fictive créée").count(), 1);
      assert.equal(await lab.getByText("révision : invented-rev-B", { exact: false }).count(), 1);
      assert.equal(await lab.getByText("révision : invented-rev-A", { exact: false }).count(), 1);
    });
    await caseRun("34-second-fiction-universe-has-no-foreign-revision-choices", async () => {
      await page.getByRole("button", { name: "Charger un autre univers fictif" }).click();
      await page.getByRole("button", { name: "Ouvrir l'atelier manuel fictif" }).click();
      const lab = page.getByRole("region", { name: "Atelier manuel M3.2 exclusivement fictif" });
      assert.equal(await lab.getByRole("combobox", { name: "Scène inventée à citer (facultatif)" })
        .locator("option").count(), 1);
      assert.equal(await lab.getByRole("combobox", { name: "Révision exacte et immuable de cette scène" }).count(), 0);
      assert.equal(await lab.getByText("invented-rev-A", { exact: false }).count(), 0);
    });
    await caseRun("35-conflict-preview-shows-existing-human-edges-before-click", async () => {
      await page.getByRole("button", { name: "Ouvrir l'atelier manuel fictif" }).click();
      const lab = page.getByRole("region", { name: "Atelier manuel M3.2 exclusivement fictif" });
      await lab.getByRole("combobox", { name: "Événement antérieur" }).selectOption("C");
      await lab.getByRole("combobox", { name: "Événement postérieur" }).selectOption("A");
      const preview = lab.getByRole("status", { name: "Vérification avant/après fictive" });
      assert.ok((await preview.innerText()).includes("cycle temporel"));
      assert.ok((await preview.innerText()).includes("human-ab"));
      assert.ok((await preview.innerText()).includes("human-bc"));
      assert.equal(await lab.getByRole("alert").count(), 0);
    });
    await caseRun("36-explicit-revocation-updates-correction-preflight", async () => {
      await page.getByRole("button", { name: "Ouvrir l'atelier manuel fictif" }).click();
      const lab = page.getByRole("region", { name: "Atelier manuel M3.2 exclusivement fictif" });
      await lab.getByRole("combobox", { name: "Correction : remplacer une ancre active" }).selectOption("A");
      const preview = lab.getByRole("status", { name: "Vérification de correction fictive" });
      assert.ok((await preview.innerText()).includes("human-ab"));
      assert.ok((await preview.innerText()).includes("invented-rev-A"));
      await lab.getByRole("combobox", { name: "Relation à révoquer (historique conservé)" })
        .selectOption("human-ab");
      await lab.getByRole("textbox", { name: "Justification humaine fictive" }).fill("Révocation humaine fictive");
      await lab.getByRole("button", { name: "Révoquer explicitement" }).click();
      assert.ok((await preview.innerText()).includes("Correction possible"));
      assert.ok(!(await preview.innerText()).includes("Révoquer explicitement les liens actifs"));
    });
    await caseRun("37-second-novel-historical-revision-selected-without-world-order", async () => {
      await page.getByRole("button", { name: "Revenir au premier univers fictif" }).click();
      await page.getByRole("button", { name: "Ouvrir l'atelier manuel fictif" }).click();
      const lab = page.getByRole("region", { name: "Atelier manuel M3.2 exclusivement fictif" });
      assert.ok((await lab.innerText()).includes("romans différents du même Univers"));
      await lab.getByRole("combobox", { name: "Scène inventée à citer (facultatif)" }).selectOption("s2");
      await lab.getByRole("combobox", { name: "Révision exacte et immuable de cette scène" })
        .selectOption("invented-rev-C");
      await lab.getByRole("button", { name: "Ajouter l'ancre" }).click();
      assert.equal(await lab.getByText("révision : invented-rev-C", { exact: false }).count(), 1);
      assert.ok((await lab.innerText()).includes("Ordre de révélation au lecteur"));
    });
    await caseRun("38-two-novels-filter-revisions-by-immutable-scene-identity", async () => {
      await page.getByRole("button", { name: "Revenir au premier univers fictif" }).click();
      await page.getByRole("button", { name: "Ouvrir l'atelier manuel fictif" }).click();
      const lab = page.getByRole("region", { name: "Atelier manuel M3.2 exclusivement fictif" });
      const scene = lab.getByRole("combobox", { name: "Scène inventée à citer (facultatif)" });
      await scene.selectOption("s2");
      const revisions = lab.getByRole("combobox", { name: "Révision exacte et immuable de cette scène" });
      assert.equal(await revisions.locator("option").count(), 2);
      assert.equal(await revisions.locator('option[value="invented-rev-A"]').count(), 0);
      await scene.selectOption("s1");
      assert.equal(await revisions.locator('option[value="invented-rev-C"]').count(), 0);
      assert.equal(await revisions.locator('option[value="invented-rev-B"]').count(), 1);
      assert.equal(await revisions.inputValue(), "");
    });
    await caseRun("39-three-orders-intra-novel-narration-only", async () => {
      await page.getByRole("button", { name: "Revenir au premier univers fictif" }).click();
      await page.getByRole("button", { name: "Ouvrir l'atelier manuel fictif" }).click();
      const lab = page.getByRole("region", { name: "Atelier manuel M3.2 exclusivement fictif" });
      await lab.getByRole("combobox", { name: "Première scène à comparer" }).selectOption("s1");
      await lab.getByRole("combobox", { name: "Deuxième scène à comparer" }).selectOption("s3");
      const explanation = lab.getByRole("status", { name: "Comparaison des trois ordres fictifs" });
      assert.ok((await explanation.innerText()).includes("première scène précède la seconde"));
      assert.ok((await explanation.innerText()).includes("Chronologie du monde : indéterminée"));
      assert.ok((await explanation.innerText()).includes("Révélation au lecteur : non renseignée"));
    });
    await caseRun("40-three-orders-distinct-novels-have-no-shared-manuscript-order", async () => {
      await page.getByRole("button", { name: "Ouvrir l'atelier manuel fictif" }).click();
      const lab = page.getByRole("region", { name: "Atelier manuel M3.2 exclusivement fictif" });
      await lab.getByRole("combobox", { name: "Première scène à comparer" }).selectOption("s1");
      await lab.getByRole("combobox", { name: "Deuxième scène à comparer" }).selectOption("s2");
      const explanation = lab.getByRole("status", { name: "Comparaison des trois ordres fictifs" });
      assert.ok((await explanation.innerText()).includes("indéterminé entre romans distincts"));
      assert.ok((await explanation.innerText()).includes("Révélation au lecteur : non renseignée"));
    });
    await caseRun("41-three-orders-empty-fictional-universe-has-no-foreign-scenes", async () => {
      await page.getByRole("button", { name: "Charger un autre univers fictif" }).click();
      await page.getByRole("button", { name: "Ouvrir l'atelier manuel fictif" }).click();
      const lab = page.getByRole("region", { name: "Atelier manuel M3.2 exclusivement fictif" });
      assert.equal(await lab.getByRole("combobox", { name: "Première scène à comparer" })
        .locator("option").count(), 1);
      assert.equal(await lab.getByRole("combobox", { name: "Deuxième scène à comparer" })
        .locator("option").count(), 1);
      assert.ok((await lab.getByRole("status", { name: "Comparaison des trois ordres fictifs" })
        .innerText()).includes("Choisir deux scènes fictives"));
    });
    await caseRun("42-existing-human-witness-transitive-two-edges", async () => {
      await page.getByRole("button", { name: "Ouvrir l'atelier manuel fictif" }).click();
      const lab = page.getByRole("region", { name: "Atelier manuel M3.2 exclusivement fictif" });
      await lab.getByRole("combobox", { name: "Première ancre à consulter" }).selectOption("A");
      await lab.getByRole("combobox", { name: "Deuxième ancre à consulter" }).selectOption("C");
      const proof = lab.getByRole("region", { name: "Comparaison M3.2 isolée" });
      assert.ok((await proof.innerText()).includes("Avant : précédence humaine explicite ou transitive"));
      assert.ok((await proof.innerText()).includes("human-ab"));
      assert.ok((await proof.innerText()).includes("human-bc"));
      assert.ok((await proof.innerText()).includes("Le messager arrive"));
    });
    await caseRun("43-revoked-edge-is-not-world-precedence-proof", async () => {
      await page.getByRole("button", { name: "Ouvrir l'atelier manuel fictif" }).click();
      const lab = page.getByRole("region", { name: "Atelier manuel M3.2 exclusivement fictif" });
      await lab.getByRole("combobox", { name: "Première ancre à consulter" }).selectOption("A");
      await lab.getByRole("combobox", { name: "Deuxième ancre à consulter" }).selectOption("D");
      const proof = lab.getByRole("region", { name: "Comparaison M3.2 isolée" });
      assert.ok((await proof.innerText()).includes("Ordre indéterminé"));
      assert.ok(!(await proof.innerText()).includes("retired-ad"));
      await lab.getByRole("combobox", { name: "Première ancre à consulter" }).selectOption("C");
      await lab.getByRole("combobox", { name: "Deuxième ancre à consulter" }).selectOption("A");
      assert.ok((await proof.innerText()).includes("Après : précédence humaine explicite ou transitive"));
      assert.ok((await proof.innerText()).includes("human-ab"));
    });
    await caseRun("44-proof-refreshes-on-explicit-revocation-without-inventing-time", async () => {
      await page.getByRole("button", { name: "Ouvrir l'atelier manuel fictif" }).click();
      const lab = page.getByRole("region", { name: "Atelier manuel M3.2 exclusivement fictif" });
      await lab.getByRole("combobox", { name: "Première ancre à consulter" }).selectOption("A");
      await lab.getByRole("combobox", { name: "Deuxième ancre à consulter" }).selectOption("B");
      const proof = lab.getByRole("region", { name: "Comparaison M3.2 isolée" });
      assert.ok((await proof.innerText()).includes("human-ab"));
      await lab.getByRole("combobox", { name: "Relation à révoquer (historique conservé)" })
        .selectOption("human-ab");
      await lab.getByRole("textbox", { name: "Justification humaine fictive" })
        .fill("Révocation volontaire du lien humain");
      await lab.getByRole("button", { name: "Révoquer explicitement" }).click();
      assert.ok((await proof.innerText()).includes("Ordre indéterminé"));
      assert.ok(!(await proof.innerText()).includes("human-ab"));
      assert.ok((await lab.innerText()).includes("ordre de révélation non renseigné"));
    });
    await caseRun("45-corrected-anchor-never-remains-active-world-proof", async () => {
      await page.getByRole("button", { name: "Ouvrir l'atelier manuel fictif" }).click();
      const lab = page.getByRole("region", { name: "Atelier manuel M3.2 exclusivement fictif" });
      await lab.getByRole("combobox", { name: "Première ancre à consulter" }).selectOption("C");
      await lab.getByRole("combobox", { name: "Deuxième ancre à consulter" }).selectOption("D");
      assert.ok((await lab.getByRole("region", { name: "Comparaison M3.2 isolée" })
        .innerText()).includes("Ordre indéterminé"));
      await lab.getByRole("combobox", { name: "Correction : remplacer une ancre active" })
        .selectOption("D");
      await lab.getByRole("button", { name: "Remplacer sans effacer l'historique" }).click();
      assert.ok((await lab.innerText()).includes("Sélection historique"));
      assert.equal(await lab.getByRole("region", { name: "Comparaison M3.2 isolée" }).count(), 0);
      await lab.getByRole("combobox", { name: "Deuxième ancre à consulter" })
        .selectOption("fiction-draft-0001");
      assert.ok((await lab.getByRole("region", { name: "Comparaison M3.2 isolée" })
        .innerText()).includes("Ordre indéterminé"));
    });
    await caseRun("46-switching-fictional-universe-clears-world-proof-selection", async () => {
      await page.getByRole("button", { name: "Ouvrir l'atelier manuel fictif" }).click();
      let lab = page.getByRole("region", { name: "Atelier manuel M3.2 exclusivement fictif" });
      await lab.getByRole("combobox", { name: "Première ancre à consulter" }).selectOption("A");
      await lab.getByRole("combobox", { name: "Deuxième ancre à consulter" }).selectOption("B");
      assert.ok((await lab.getByRole("region", { name: "Comparaison M3.2 isolée" })
        .innerText()).includes("human-ab"));
      await page.getByRole("button", { name: "Charger un autre univers fictif" }).click();
      lab = page.getByRole("region", { name: "Atelier manuel M3.2 exclusivement fictif" });
      assert.ok((await lab.innerText()).includes("fiction-world-two"));
      assert.equal(await lab.getByRole("combobox", { name: "Première ancre à consulter" })
        .locator('option[value="A"]').count(), 0);
      assert.equal(await lab.getByRole("region", { name: "Comparaison M3.2 isolée" }).count(), 0);
      await lab.getByRole("combobox", { name: "Première ancre à consulter" }).selectOption("K");
      await lab.getByRole("combobox", { name: "Deuxième ancre à consulter" }).selectOption("L");
      assert.ok((await lab.getByRole("region", { name: "Comparaison M3.2 isolée" })
        .innerText()).includes("Ordre indéterminé"));
      await page.getByRole("button", { name: "Revenir au premier univers fictif" }).click();
      lab = page.getByRole("region", { name: "Atelier manuel M3.2 exclusivement fictif" });
      assert.equal(await lab.getByRole("region", { name: "Comparaison M3.2 isolée" }).count(), 0);
      assert.equal(await lab.getByRole("combobox", { name: "Première ancre à consulter" })
        .locator('option[value="K"]').count(), 0);
    });
    await caseRun("47-revocation-impact-preview-does-not-revoke-human-link", async () => {
      await page.getByRole("button", { name: "Ouvrir l'atelier manuel fictif" }).click();
      const lab = page.getByRole("region", { name: "Atelier manuel M3.2 exclusivement fictif" });
      const impact = lab.getByRole("status", { name: "Prévisualisation de révocation fictive" });
      await lab.getByRole("combobox", { name: "Relation à révoquer (historique conservé)" })
        .selectOption("human-ab");
      assert.ok((await impact.innerText()).includes("ordre indéterminé"));
      assert.ok((await impact.innerText()).includes("ne révoque rien"));
      await lab.getByRole("combobox", { name: "Première ancre à consulter" })
        .selectOption("A");
      await lab.getByRole("combobox", { name: "Deuxième ancre à consulter" })
        .selectOption("B");
      assert.ok((await lab.getByRole("region", { name: "Comparaison M3.2 isolée" })
        .innerText()).includes("human-ab"));
    });
    await caseRun("48-alternate-authored-route-survives-hypothetical-direct-revocation", async () => {
      await page.getByRole("button", { name: "Ouvrir l'atelier manuel fictif" }).click();
      const lab = page.getByRole("region", { name: "Atelier manuel M3.2 exclusivement fictif" });
      await lab.getByRole("combobox", { name: "Événement antérieur" }).selectOption("A");
      await lab.getByRole("combobox", { name: "Événement postérieur" }).selectOption("C");
      await lab.getByRole("textbox", { name: "Justification humaine fictive" })
        .fill("raccourci humain AC");
      await lab.getByRole("button", { name: "Ajouter avant/après" }).click();
      await lab.getByRole("combobox", { name: "Relation à révoquer (historique conservé)" })
        .selectOption("fiction-draft-0001");
      const impact = lab.getByRole("status", { name: "Prévisualisation de révocation fictive" });
      assert.ok((await impact.innerText()).includes("autre chemin humain actif"));
      assert.ok((await impact.innerText()).includes("human-ab"));
      assert.ok((await impact.innerText()).includes("human-bc"));
      assert.ok((await lab.innerText()).includes("ordre de révélation non renseigné"));
    });

    await caseRun("49-exact-revision-proof-needs-unique-current-anchor", async () => {
      await page.getByRole("button", { name: "Ouvrir l'atelier manuel fictif" }).click();
      const lab = page.getByRole("region", { name: "Atelier manuel M3.2 exclusivement fictif" });
      await lab.getByRole("combobox", { name: "Première scène à comparer" }).selectOption("s1");
      await lab.getByRole("combobox", { name: "Deuxième scène à comparer" }).selectOption("s2");
      await lab.getByRole("combobox", { name: "Révision exacte de la première scène pour le temps du monde" }).selectOption("invented-rev-A");
      await lab.getByRole("combobox", { name: "Révision exacte de la deuxième scène pour le temps du monde" }).selectOption("invented-rev-C");
      const proof = lab.getByRole("status", { name: "Résultat du temps du monde lié aux révisions" });
      assert.ok((await proof.innerText()).includes("ancre courante unique"));
    });
    await caseRun("50-two-revisions-cross-novel-world-human-proof-only", async () => {
      await page.getByRole("button", { name: "Ouvrir l'atelier manuel fictif" }).click();
      const lab = page.getByRole("region", { name: "Atelier manuel M3.2 exclusivement fictif" });
      await lab.getByRole("combobox", { name: "Scène inventée à citer (facultatif)" }).selectOption("s2");
      await lab.getByRole("combobox", { name: "Révision exacte et immuable de cette scène" }).selectOption("invented-rev-C");
      await lab.getByRole("button", { name: "Ajouter l'ancre" }).click();
      await lab.getByRole("combobox", { name: "Événement antérieur" }).selectOption("A");
      await lab.getByRole("combobox", { name: "Événement postérieur" }).selectOption("fiction-draft-0001");
      await lab.getByRole("textbox", { name: "Justification humaine fictive" }).fill("ordre humain");
      await lab.getByRole("button", { name: "Ajouter avant/après" }).click();
      await lab.getByRole("combobox", { name: "Première scène à comparer" }).selectOption("s1");
      await lab.getByRole("combobox", { name: "Deuxième scène à comparer" }).selectOption("s2");
      await lab.getByRole("combobox", { name: "Révision exacte de la première scène pour le temps du monde" }).selectOption("invented-rev-A");
      await lab.getByRole("combobox", { name: "Révision exacte de la deuxième scène pour le temps du monde" }).selectOption("invented-rev-C");
      const proof = lab.getByRole("status", { name: "Résultat du temps du monde lié aux révisions" });
      assert.ok((await proof.innerText()).includes("Temps du monde établi"));
      assert.ok((await proof.innerText()).includes("fiction-draft-0002"));
      assert.ok((await lab.getByRole("status", { name: "Comparaison des trois ordres fictifs" })
        .innerText()).includes("indéterminé entre romans distincts"));
      assert.ok((await proof.innerText()).includes("Révélation au lecteur non renseignée"));
    });
    await caseRun("51-fictional-correction-history-readonly-three-generations", async () => {
      await page.getByRole("button", { name: "Afficher l'historique fictif des corrections" }).click();
      const history = page.getByRole("region", {
        name: "Historique fictif des corrections chronologiques",
      });
      assert.equal(await history.getByRole("listitem").count(), 3);
      assert.ok((await history.innerText()).includes("fiction-chain-2"));
      assert.ok((await history.innerText()).includes("correction retirée"));
      assert.ok((await history.innerText()).includes("Correction active : fiction-chain-2"));
      assert.ok((await history.innerText()).includes("Corrige explicitement fiction-successor"));
      assert.ok((await history.innerText()).includes("Corrige explicitement fiction-chain-1"));
      assert.ok((await history.innerText()).includes("ancienne assertion A avant B"));
      assert.ok((await history.innerText()).includes("Aucun ordre global déduit"));
      assert.equal(await history.getByRole("button").count(), 0);
    });
    await caseRun("52-fictional-correction-history-other-world-no-leak", async () => {
      await page.getByRole("button", { name: "Charger un autre univers fictif" }).click();
      await page.getByRole("button", { name: "Afficher l'historique fictif des corrections" }).click();
      const history = page.getByRole("region", {
        name: "Historique fictif des corrections chronologiques",
      });
      assert.ok((await history.innerText()).includes("Aucune correction fictive"));
      assert.ok(!(await history.innerText()).includes("fiction-chain-2"));
    });
    await caseRun("53-fictional-correction-history-cycle-fails-closed", async () => {
      await page.getByRole("button", { name: "Charger un cycle fictif invalide" }).click();
      await page.getByRole("button", { name: "Afficher l'historique fictif des corrections" }).click();
      const alert = page.getByRole("alert", { name: "Historique fictif rejeté" });
      assert.equal(await alert.count(), 1);
      assert.ok((await alert.innerText()).includes("Historique de corrections refusé"));
      assert.equal(await page.getByText("fiction-chain-2", { exact: true }).count(), 0);
    });
    const eventForm = () => page.getByRole("form", { name: "Formulaire d'événement fictif" });
    const eventRegion = () => page.getByRole("region", {
      name: "Atelier manuel fictif d'événements M3.2",
    });
    async function openEventForm() {
      await page.getByRole("button", { name: "Ouvrir le carnet d'événements fictifs" }).click();
      assert.equal(await eventRegion().count(), 1);
    }
    async function createInventedEvent(title = "Rencontre fictive") {
      await eventForm().getByRole("textbox", { name: "Titre de l'événement (obligatoire)" })
        .fill(title);
      await eventForm().getByRole("button", { name: "Créer en mémoire" }).click();
    }
    await caseRun("54-fictional-event-form-empty-safe", async () => {
      await openEventForm();
      assert.ok((await eventRegion().innerText()).includes("Aucun enregistrement"));
      assert.ok((await eventRegion().innerText()).includes("Événements courants (0)"));
      assert.equal(await eventRegion().getByRole("listitem").count(), 0);
    });
    await caseRun("55-fictional-event-human-create-no-inferred-time", async () => {
      await openEventForm();
      await createInventedEvent();
      assert.equal(await eventRegion().getByRole("listitem").count(), 1);
      assert.ok((await eventRegion().innerText()).includes("Rencontre fictive"));
      assert.ok((await eventRegion().innerText()).includes("1 versions"));
      assert.ok((await eventRegion().getByRole("status").innerText()).includes("Aucune sauvegarde"));
    });
    await caseRun("56-fictional-event-human-amend-retains-version", async () => {
      await openEventForm();
      await createInventedEvent();
      await eventRegion().getByRole("button", { name: /Corriger ou retirer/ }).click();
      await eventForm().getByRole("textbox", { name: "Titre de l'événement (obligatoire)" })
        .fill("Rencontre amendée");
      await eventForm().getByRole("textbox", {
        name: "Justification de correction ou de retrait",
      }).fill("Rédaction historique");
      await eventForm().getByRole("button", { name: "Enregistrer une nouvelle version" }).click();
      assert.ok((await eventRegion().innerText()).includes("Rencontre amendée"));
      assert.ok((await eventRegion().innerText()).includes("version 2"));
      assert.ok((await eventRegion().innerText()).includes("2 versions"));
    });
    await caseRun("57-fictional-event-human-withdraw-tombstone", async () => {
      await openEventForm();
      await createInventedEvent();
      await eventRegion().getByRole("button", { name: /Corriger ou retirer/ }).click();
      await eventForm().getByRole("textbox", {
        name: "Justification de correction ou de retrait",
      }).fill("Retrait humain explicite");
      await eventForm().getByRole("button", {
        name: "Retirer en conservant l'historique",
      }).click();
      assert.ok((await eventRegion().innerText()).includes("Événements courants (0)"));
      assert.ok((await eventRegion().innerText()).includes("2 versions"));
      assert.equal(await eventRegion().getByRole("listitem").count(), 0);
    });
    await caseRun("58-fictional-event-explicit-historical-revision", async () => {
      await openEventForm();
      await eventForm().getByRole("textbox", { name: "Titre de l'événement (obligatoire)" })
        .fill("Révision liée");
      await eventForm().getByRole("combobox", {
        name: "Ancre temporelle explicitement choisie",
      }).selectOption("A");
      await eventForm().getByRole("combobox", {
        name: "Révision historique explicitement choisie",
      }).selectOption("invented-rev-A");
      await eventForm().getByRole("button", { name: "Créer en mémoire" }).click();
      assert.ok((await eventRegion().innerText()).includes("Événements courants (1)"));
      assert.ok((await eventRegion().innerText()).includes("Révision liée"));
    });
    await caseRun("59-fictional-event-refuses-ambiguous-source", async () => {
      await openEventForm();
      await eventForm().getByRole("textbox", { name: "Titre de l'événement (obligatoire)" })
        .fill("Révision non prouvée");
      await eventForm().getByRole("combobox", {
        name: "Ancre temporelle explicitement choisie",
      }).selectOption("A");
      await eventForm().getByRole("button", { name: "Créer en mémoire" }).click();
      assert.equal(await eventRegion().getByRole("alert").count(), 1);
      assert.ok((await eventRegion().innerText()).includes("Événements courants (0)"));
    });
    await caseRun("60-fictional-event-world-switch-clears-previous", async () => {
      await openEventForm();
      await createInventedEvent("Secret du premier univers");
      await page.getByRole("button", { name: "Charger un autre univers fictif" }).click();
      assert.ok((await eventRegion().innerText()).includes("fiction-world-two"));
      assert.ok((await eventRegion().innerText()).includes("Événements courants (0)"));
      assert.ok(!(await eventRegion().innerText()).includes("Secret du premier univers"));
    });
    await caseRun("61-fictional-event-inert-hostile-label", async () => {
      await openEventForm();
      await createInventedEvent("<script>window.__fictionInjected=1</script>");
      assert.equal(await eventRegion().locator("script").count(), 0);
      assert.equal(await page.evaluate(() => Boolean(window.__fictionInjected)), false);
      assert.ok((await eventRegion().innerText()).includes("<script>"));
    });
    await caseRun("62-fictional-event-cycle-is-rejected", async () => {
      await page.getByRole("button", { name: "Charger un cycle fictif invalide" }).click();
      await page.getByRole("button", { name: "Ouvrir le carnet d'événements fictifs" }).click();
      assert.equal(await page.getByRole("alert", { name: "" }).count(), 1);
      assert.ok((await page.getByRole("alert").innerText()).includes("Cycle fictif refusé"));
      assert.equal(await eventRegion().count(), 0);
    });
    const picker = () => page.getByRole("region", {
      name: "Laboratoire de sélection de versions fictives",
    });
    const eventSelect = () => picker().getByRole("combobox", { name: "Événement fictif à comparer" });
    const fromSelect = () => picker().getByRole("combobox", { name: "Version fictive de départ" });
    const toSelect = () => picker().getByRole("combobox", { name: "Version fictive d'arrivée" });
    async function openPicker() {
      await page.getByRole("button", { name: "Comparer deux versions fictives (laboratoire)" }).click();
      assert.equal(await picker().count(), 1);
    }
    await caseRun("63-pair-picker-starts-empty", async () => {
      await openPicker();
      assert.equal(await eventSelect().inputValue(), "");
      assert.equal(await fromSelect().isDisabled(), true);
      assert.equal(await toSelect().isDisabled(), true);
      assert.equal(await picker().getByRole("region", { name: "Comparaison fictive demandée explicitement" }).count(), 0);
    });
    await caseRun("64-pair-picker-middle-to-final-exact", async () => {
      await openPicker();
      await eventSelect().selectOption("fiction-world-one-event-0001");
      await fromSelect().selectOption("2");
      await toSelect().selectOption("3");
      const result = picker().getByRole("region", { name: "Comparaison fictive demandée explicitement" });
      assert.ok((await result.innerText()).includes("version 2 vers version 3"));
      assert.ok((await result.innerText()).includes("avant = Deuxième version inventée"));
      assert.ok((await result.innerText()).includes("après = <script>fiction-inerte</script>"));
    });
    await caseRun("65-pair-picker-refuses-inverted-and-resets-stale-target", async () => {
      await openPicker();
      await eventSelect().selectOption("fiction-world-one-event-0001");
      await fromSelect().selectOption("1");
      await toSelect().selectOption("2");
      assert.equal(await picker().getByRole("region", { name: "Comparaison fictive demandée explicitement" }).count(), 1);
      await fromSelect().selectOption("2");
      assert.equal(await toSelect().inputValue(), "");
      assert.equal(await toSelect().locator('option[value="1"]').count(), 0);
      assert.equal(await toSelect().locator('option[value="2"]').count(), 0);
      assert.equal(await picker().getByRole("region", { name: "Comparaison fictive demandée explicitement" }).count(), 0);
    });
    await caseRun("66-pair-picker-withdrawal-preserves-history", async () => {
      await openPicker();
      await eventSelect().selectOption("fiction-world-one-event-0002");
      await fromSelect().selectOption("1");
      await toSelect().selectOption("2");
      const result = picker().getByRole("region", { name: "Comparaison fictive demandée explicitement" });
      assert.ok((await result.innerText()).includes("Aucun écart de contenu"));
      assert.ok((await result.innerText()).includes("withdrawn"));
    });
    await caseRun("67-pair-picker-changing-event-clears-both-versions", async () => {
      await openPicker();
      await eventSelect().selectOption("fiction-world-one-event-0001");
      await fromSelect().selectOption("1");
      await toSelect().selectOption("3");
      await eventSelect().selectOption("fiction-world-one-event-0002");
      assert.equal(await fromSelect().inputValue(), "");
      assert.equal(await toSelect().inputValue(), "");
      assert.equal(await picker().getByRole("region", { name: "Comparaison fictive demandée explicitement" }).count(), 0);
    });
    await caseRun("68-pair-picker-switch-world-restarts-isolated-selection", async () => {
      await openPicker();
      await eventSelect().selectOption("fiction-world-one-event-0001");
      await fromSelect().selectOption("1");
      await toSelect().selectOption("3");
      await page.getByRole("button", { name: "Charger un autre univers fictif" }).click();
      assert.equal(await eventSelect().inputValue(), "");
      assert.ok((await picker().innerText()).includes("fiction-world-two"));
      assert.ok(!(await picker().innerText()).includes("fiction-world-one-event"));
    });
    await caseRun("69-pair-picker-cycle-fails-closed", async () => {
      await page.getByRole("button", { name: "Charger un cycle fictif invalide" }).click();
      await page.getByRole("button", { name: "Comparer deux versions fictives (laboratoire)" }).click();
      assert.equal(await picker().count(), 0);
      assert.ok((await page.getByRole("alert").innerText()).includes("Cycle fictif refusé"));
    });
    await caseRun("70-pair-picker-script-looking-label-inert", async () => {
      await openPicker();
      await eventSelect().selectOption("fiction-world-one-event-0001");
      await fromSelect().selectOption("2");
      await toSelect().selectOption("3");
      assert.equal(await picker().locator("script").count(), 0);
      assert.equal(await page.evaluate(() => Boolean(window.__fictionInjected)), false);
      assert.ok((await picker().innerText()).includes("<script>fiction-inerte</script>"));
    });
    const liveComparisonButton = () => eventRegion().getByRole("button", {
      name: "Comparer les versions créées dans cet atelier fictif",
    });
    const livePicker = () => eventRegion().getByRole("region", {
      name: "Laboratoire de sélection de versions fictives",
    });
    const liveEvent = () => livePicker().getByRole("combobox", {
      name: "Événement fictif à comparer",
    });
    const liveFrom = () => livePicker().getByRole("combobox", {
      name: "Version fictive de départ",
    });
    const liveTo = () => livePicker().getByRole("combobox", {
      name: "Version fictive d'arrivée",
    });
    async function amendLive(title) {
      await eventRegion().getByRole("button", { name: /Corriger ou retirer/ }).click();
      await eventForm().getByRole("textbox", { name: "Titre de l'événement (obligatoire)" })
        .fill(title);
      await eventForm().getByRole("textbox", {
        name: "Justification de correction ou de retrait",
      }).fill("Correction humaine inventée");
      await eventForm().getByRole("button", { name: "Enregistrer une nouvelle version" }).click();
    }
    await caseRun("71-live-workshop-comparison-hidden-until-author-requests", async () => {
      await openEventForm();
      assert.equal(await liveComparisonButton().getAttribute("aria-expanded"), "false");
      assert.equal(await livePicker().count(), 0);
      await liveComparisonButton().click();
      assert.equal(await livePicker().count(), 1);
      assert.equal(await liveEvent().inputValue(), "");
      assert.equal(await liveFrom().isDisabled(), true);
      assert.equal(await liveTo().isDisabled(), true);
    });
    await caseRun("72-live-workshop-create-amend-compare-exact-own-versions", async () => {
      await openEventForm();
      await createInventedEvent("Version A inventée");
      await amendLive("Version B inventée");
      await liveComparisonButton().click();
      await liveEvent().selectOption("fiction-world-one-event-0001");
      await liveFrom().selectOption("1");
      await liveTo().selectOption("2");
      const diff = livePicker().getByRole("region", { name: "Comparaison fictive demandée explicitement" });
      assert.ok((await diff.innerText()).includes("avant = Version A inventée"));
      assert.ok((await diff.innerText()).includes("après = Version B inventée"));
    });
    await caseRun("73-live-workshop-new-amendment-updates-available-version-pair", async () => {
      await openEventForm();
      await createInventedEvent("Version A inventée");
      await amendLive("Version B inventée");
      await liveComparisonButton().click();
      await liveEvent().selectOption("fiction-world-one-event-0001");
      await liveFrom().selectOption("1");
      await liveTo().selectOption("2");
      await amendLive("Version C inventée");
      assert.equal(await liveFrom().inputValue(), "1");
      assert.equal(await liveTo().inputValue(), "2");
      await liveFrom().selectOption("2");
      assert.equal(await liveTo().inputValue(), "");
      await liveTo().selectOption("3");
      const diff = livePicker().getByRole("region", { name: "Comparaison fictive demandée explicitement" });
      assert.ok((await diff.innerText()).includes("avant = Version B inventée"));
      assert.ok((await diff.innerText()).includes("après = Version C inventée"));
    });
    await caseRun("74-live-workshop-withdrawal-keeps-historical-comparison", async () => {
      await openEventForm();
      await createInventedEvent("Retrait fictif");
      await eventRegion().getByRole("button", { name: /Corriger ou retirer/ }).click();
      await eventForm().getByRole("textbox", {
        name: "Justification de correction ou de retrait",
      }).fill("Motif de retrait inventé");
      await eventForm().getByRole("button", {
        name: "Retirer en conservant l'historique",
      }).click();
      await liveComparisonButton().click();
      await liveEvent().selectOption("fiction-world-one-event-0001");
      await liveFrom().selectOption("1");
      await liveTo().selectOption("2");
      assert.ok((await livePicker().innerText()).includes("Aucun écart de contenu"));
      assert.ok((await livePicker().innerText()).includes("withdrawn"));
      assert.ok((await eventRegion().innerText()).includes("Événements courants (0)"));
    });
    await caseRun("75-live-workshop-world-switch-remounts-without-stale-data", async () => {
      await openEventForm();
      await createInventedEvent("Secret du premier univers");
      await liveComparisonButton().click();
      await liveEvent().selectOption("fiction-world-one-event-0001");
      await page.getByRole("button", { name: "Charger un autre univers fictif" }).click();
      assert.ok((await eventRegion().innerText()).includes("fiction-world-two"));
      assert.equal(await livePicker().count(), 0);
      assert.ok(!(await eventRegion().innerText()).includes("Secret du premier univers"));
      await liveComparisonButton().click();
      assert.equal(await liveEvent().inputValue(), "");
      assert.equal(await liveEvent().locator("option[value^='fiction-world-one']").count(), 0);
    });
    await caseRun("76-live-workshop-comparison-escapes-user-looking-script", async () => {
      await openEventForm();
      await createInventedEvent("Départ inventé");
      await amendLive("<script>window.__fictionInjected=1</script>");
      await liveComparisonButton().click();
      await liveEvent().selectOption("fiction-world-one-event-0001");
      await liveFrom().selectOption("1");
      await liveTo().selectOption("2");
      assert.equal(await livePicker().locator("script").count(), 0);
      assert.equal(await page.evaluate(() => Boolean(window.__fictionInjected)), false);
      assert.ok((await livePicker().getByRole("region", {
        name: "Comparaison fictive demandée explicitement",
      }).innerText()).includes("<script>window.__fictionInjected=1</script>"));
    });
    assert.equal(cases.length, 76);
    // Historical PR #146 source marker: M32_BROWSER_REAL_CHROMIUM_PASS 62/62
    // Previous PR #156 marker retained: M32_BROWSER_REAL_CHROMIUM_PASS 70/70
    console.log("M32_BROWSER_REAL_CHROMIUM_PASS 76/76");

    // Actual Chromium enforced-CSP veto, separate from the 36
    // fictional interaction cases. Never make an off-loopback network call.
    const cspVeto = await page.evaluate(async () => {
      const notices = [];
      const handler = event => notices.push({
        directive: event.effectiveDirective, blocked: event.blockedURI,
      });
      document.addEventListener("securitypolicyviolation", handler);
      let rejected = false;
      try { await fetch("https://example.invalid/m32-csp-must-block", { mode: "cors" }); }
      catch { rejected = true; }
      await new Promise(resolve => setTimeout(resolve, 200));
      document.removeEventListener("securitypolicyviolation", handler);
      return { rejected, notices };
    });
    assert.equal(cspVeto.rejected, true, "STOP: Chromium permitted a remote fetch");
    assert.ok(cspVeto.notices.some(x =>
      x.directive === "connect-src" && x.blocked.includes("example.invalid")),
      "STOP: missing actual browser CSP connect-src enforcement");
    assert.deepEqual(unsafeNetwork, [], "STOP: remote request escaped local CSP");
    console.log("M32_CI_CHROMIUM_CSP_CONNECT_BLOCK_PASS: external fetch denied by CSP");
    if (staticMode) {
      const scriptVeto = await page.evaluate(() => {
        const trap = document.createElement("script");
        trap.textContent = "window.__M32_INLINE_EXECUTED = true";
        document.body.appendChild(trap);
        return window.__M32_INLINE_EXECUTED === true;
      });
      assert.equal(scriptVeto, false, "STOP: inline JS executed under strict CSP");
      console.log("M32_CI_PRECOMPILED_INLINE_SCRIPT_DENIED_PASS");
      console.log("M32_CI_PRECOMPILED_STRICT_CSP_BROWSER_PASS: 76/76");
    }
    console.log("M32_CI_FIXTURE_ONLY_BROWSER_PASS: 76/76; no normal source pages");
  } finally {
    if (browser) await browser.close();
    server.kill();
  }
}
run().catch(error => {
  console.error("M32_BROWSER_REAL_CHROMIUM_FAIL " + error.stack);
  process.exitCode = 1;
  server.kill();
});
