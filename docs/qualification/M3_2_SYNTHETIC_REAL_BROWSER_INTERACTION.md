# M3.2 — Real Chromium synthetic-only interaction qualification

**2026-10-17. Browser interaction laboratory only, no operator originals, no Tauri IPC, no production App.tsx mount, no real source authority.**

Protected baseline `main=008761b0778b8ad3dd5e5dd711ef406394bf41d2` after PR #59 (exact-head Windows CI #39044031084 41/41 SUCCESS, 24/24 added React tests). The isolated `M32ChronologyConsultation` now has static SSR/Vitest and pure transition checks, but these are not actual user interaction evidence. This PR adds a **different evidence dimension**: a Chromium headless browser on Windows interacting with native selects via Playwright. It is not a Windows desktop Tauri acceptance session.

## Isolation

`m32-browser-lab.html` (standalone Vite development/test entry, not referenced from production `index.html` or `src/App.tsx`) loads `src/m32BrowserLab.tsx` with **only hard-coded, invented** universes `fiction-world-one` / `fiction-world-two`. It includes explicitly fictive and revoked chronology assertions, a short human precedence chain and a deliberately cyclic scenario; scenario-switch buttons are *only* in the test harness. This page is not a feature of the normal `vite build` input and is never wired to the user's databases.

The browser test `tools/m32_browser_interaction.cjs` uses only Node built-ins plus a **separate pinned** ephemeral `playwright@1.64.1`, installed in the Windows runner's `RUNNER_TEMP` directory with `npm install --prefix ... --no-save --package-lock=false`. The Chromium browser is installed by that pinned CLI. Project `package.json`, `package-lock.json`, Rust Cargo dependencies and the user's Windows environment are untouched. Only a temporary Vite dev server on explicit `127.0.0.1:14279` is started, with fail-on-foreign-request observation and bounded startup. Its fixture only imports React and the two earlier M3.2 UI modules, not `App.tsx` or Tauri. CI discards all ephemeral bytes with the runner.

## Actual-browser checks

The 14 cases use Playwright's real Chromium native select, focus, ArrowDown, Enter, Tab, option-change and scenario-button actions to validate no default pair, direct/transitive/reversed human evidence, same/incomparable outcomes, witness reactivity, clearing, historical source exclusion, keyboard focus, complete reset after a fictional Universe change, fail-closed cycle and script-like text escaping. Every case reloads the fictional page, so the test never requires an original SQLite file. Browser console/runtime errors or external HTTP fetches cause failure. The test counts `M32_BROWSER_CASE_PASS` and terminates with `M32_BROWSER_REAL_CHROMIUM_PASS 14/14` only after all tests succeed.

**Limitations:** A Windows GitHub runner's headless Chromium is not a live Fabulaxiom desktop user trial. Native keyboard popup differences, actual user's UI scaling, Windows screen-reader behavior, persistent Tauri state and real v7 custody are not established. The Vite dev server is test-only. Any browser installation/download occurs on GitHub's ephemeral runner; no Playwright dependency is shipped.

## New exact-head CI gate

The existing mandatory Windows `pull_request` job adds one step after `npm ci` and the static frontend suites. It installs pinned Playwright to `RUNNER_TEMP`, invokes its Chromium installer and the scripted **14** test cases. Existing locked npm/vitest/build, Rust, Python G3 suites and file-diff checks remain required. The final PR head must receive `completed/success`, logs for all 14 real-browser cases and the strict protected GitHub check before a protected merge.

**Governance unchanged:** historical `PENDING_EXTERNAL_ATTESTATION (21/3/2)`, prospective `NOT_STARTED`, real G3 `STOP_UNAVAILABLE`, G3/G4/G5/G6 `NOT_AUTHORIZED`, PR #35 `OPEN/DRAFT`. No operator source open, backup/restore, schema 007, activation marker change, writer IPC, M3.3 or release. No independent human reviewer claimed.

Official references: https://playwright.dev/docs/ci ; https://playwright.dev/docs/input ; https://playwright.dev/docs/api/class-keyboard ; https://vite.dev/guide/ .
