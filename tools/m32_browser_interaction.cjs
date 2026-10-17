"use strict";

/* Isolated REAL Chromium interaction suite for invented Fabulaxiom M3.2 data.
 * Windows CI only. The launched Vite page is NOT production App.tsx.
 * Playwright is installed into RUNNER_TEMP, never into this repository.
 * No original database access, IPC, network destination outside loopback.
 */
const assert = require("node:assert/strict");
const path = require("node:path");
const { spawn } = require("node:child_process");
const { setTimeout: sleep } = require("node:timers/promises");

const root = path.resolve(__dirname, "..");
const playwrightPath = process.env.FABULAXIOM_M32_PLAYWRIGHT_MODULE;
if (!playwrightPath || !path.isAbsolute(playwrightPath)) {
  throw new Error("Expected explicit ephemeral absolute Playwright module directory");
}
const { chromium } = require(playwrightPath);
const port = "14279";
const url = "http://127.0.0.1:" + port + "/m32-browser-lab.html";
const cases = [];
const errors = [];
const unsafeNetwork = [];
const server = spawn(
  process.execPath,
  [path.join(root, "node_modules", "vite", "bin", "vite.js"),
    "--host", "127.0.0.1", "--port", port, "--strictPort"],
  { cwd: root, stdio: "pipe", shell: false, windowsHide: true },
);
server.on("error", e => errors.push(String(e)));

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

async function run() {
  let browser;
  try {
    await awaitLocalServer();
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
