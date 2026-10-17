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
      assert.equal(await page.getByText("Le messager arrive", { exact: false }).count(), 1);
      assert.equal(await page.getByText("La porte s'ouvre", { exact: false }).count(), 0);
    });
    await caseRun("03-transitive-human-witness", async () => {
      await first().selectOption("A");
      await second().selectOption("C");
      assert.equal(await page.getByRole("region", { name: "Justification des précédences" }).count(), 1);
      assert.equal(await page.getByText("Le messager arrive", { exact: false }).count(), 1);
      assert.equal(await page.getByText("La porte s'ouvre", { exact: false }).count(), 1);
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
      assert.equal(await page.getByText("La porte s'ouvre", { exact: false }).count(), 1);
      await second().selectOption("B");
      assert.equal(await page.getByText("La porte s'ouvre", { exact: false }).count(), 0);
      assert.equal(await page.getByText("Le messager arrive", { exact: false }).count(), 1);
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
      await first().press("ArrowDown");
      await first().press("Enter");
      assert.equal(await first().inputValue(), "A");
      await first().press("Tab");
      assert.equal(await second().evaluate(el => el === document.activeElement), true);
      await second().press("ArrowDown");
      await second().press("Enter");
      assert.equal(await second().inputValue(), "A");
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
      assert.equal(await page.getByText("<script>not executable()</script>").count(), 1);
    });
    assert.equal(cases.length, 14);
    console.log("M32_BROWSER_REAL_CHROMIUM_PASS 14/14");
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
