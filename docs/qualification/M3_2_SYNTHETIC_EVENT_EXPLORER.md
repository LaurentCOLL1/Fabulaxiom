# M3.2 — Synthetic event explorer: local filtering, paging and readable human proof

**2026-10-17 — unmounted React/Chromium laboratory only; no operator data or G3 authorization.**

Protected starting `main=53c3de511dec6a16da1c5a36e9f5eafee11be900` after PR #60 qualified (Windows pull_request CI #39046517029 42/42, real Chromium 14/14, frontend 101/101, default Rust 100/100). PR #35 remains OPEN/DRAFT/unmerged, historic external attestation 21/3/2 remains pending, and real G3 remains STOP_UNAVAILABLE.

## Narrow fictional-only functionality

`src/M32SyntheticEventExplorer.tsx` is an independent, **not mounted in App.tsx**, React component built around the previously qualified `M32ChronologyConsultation` and its pure graph validation. It shows **only invented caller-provided assertions** in a searchable, bounded page of eight, with stable immutable identity keys. Filtering works on ID and literal fictional label, not text extraction, event chronology, real calendar time or authoritative metadata. The filter can select all/current/historical. Historical items are visible as history and are **never** offered as a current-event selection. A duplicated fictional title does not merge IDs.

Clicking an explicit first/second button locally chooses a current ID; the old native select pair remains available. A selected pair is not silently replaced or cleared by filtering or page changes. The whole graph is validated **before any filter and on every render**: foreign Universe, invalid source, historical endpoint, duplicate active pair and cycle vetoes from the prior comparator all remain enforced, including cases where the filter hides the relevant node. No candidate data leaks from a partially refused world.

Paging (8 rows per page; max 512 anchors in previously bounded projection) clamps the *display page*, without touching selection or source graph. Search and status changes deliberately reset browse page to first. The proof summary shows explicit before/after/same/incomparable plus an enumerated chain of stable human edge IDs and reasons. It is not an audit signature, canon inference, global chronology or provenance verification.

The optional browser fixture remains a **separate Vite test page**, with hard-coded fictional data and now 19 additional imaginary current anchors to exercise pagination. A lab-only toggle switches between old consultation and the new explorer. It is neither an App.tsx menu, production build entry nor Tauri route. No network except the local test Vite server, no SQLite/Windows original, no IPC, persistence, original file/ACL, writer, G3 capture or restore.

## Qualification

- New `src/m32SyntheticEventExplorer.test.tsx`: **22** pure/SSR Vitest cases for ID vs label filtering, historical/current views, no implicit choice, stable 8-row paging, clamp without selection loss, invalid filters/foreign Universes, global cycle refusal even under hidden filters, explicit only memory provenance, text escape, immutable DTO and page state.
- Add one exact named Windows `npm run test:ci -- src/m32SyntheticEventExplorer.test.tsx` step; the full `npm run test:ci` remains required.
- Existing pinned **ephemeral** Playwright Chromium Windows runner script expands from 14 to **23** real-browser cases: default 8 rows, local search and explicit second selection, paging and reset, historical rows denied selection, title vs ID, transitive proof across filters, cleared choice and retained filter, Universe reset and global cycle refusal. No new npm/Cargo dependency.
- Require locked TypeScript/Vite production build, Rust tests, all previous Python/Rust source G3 audits, exact final PR HEAD terminal GitHub Actions `pull_request` success and protected merge guard. A source change invalidates previous CI.

**No production completion claimed:** real Tauri operator acceptance remains unperformed. Pure fictional browser tests cannot establish source identity, live v7 safety, stable handle custody, restore capability, actual Windows screen-reader compatibility or M3.2 CRUD.

**Unchanged authorities:** historic `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, real G3 `STOP_UNAVAILABLE`, G3/G4/G5/G6 `NOT_AUTHORIZED`, PR #35 `OPEN/DRAFT`. No original v6/v7 open, migration 007, activation marker, writer IPC, M3.3 or release.

References: https://react.dev/learn/rendering-lists ; https://playwright.dev/docs/locators ; https://playwright.dev/docs/input .
