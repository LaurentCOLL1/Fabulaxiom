"use strict";

/* Isolated REAL Chromium interaction suite for invented Fabulaxiom M3.2 data.
 * Windows CI only. The launched Vite page is NOT production App.tsx.
 * Playwright is installed into RUNNER_TEMP, never into this repository.
 * No original database access, IPC, network destination outside loopback.
 */
const assert = require("node:assert/strict");
const path = require("node:path");
const { createHash } = require("node:crypto");
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
  { cwd: root, stdio: "pipe", shell: false, windowsHide: true, env },
);
server.on("error", e => errors.push(String(e)));
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
    if (server.exitCode !== null) throw new Error("Vite exited before browser test");
    try {
      const response = await fetch(url, { signal: AbortSignal.timeout(900) });
      if (response.ok) return;
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
    assert.equal(cases.length, 29);
    console.log("M32_BROWSER_REAL_CHROMIUM_PASS 29/29");
    // Actual Chromium enforced-CSP veto, separate from the 29 pre-existing
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
      console.log("M32_CI_PRECOMPILED_STRICT_CSP_BROWSER_PASS: 29/29");
    }
    console.log("M32_CI_FIXTURE_ONLY_BROWSER_PASS: 29/29; no normal source pages");
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
