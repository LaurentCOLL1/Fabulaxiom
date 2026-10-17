# M3.2 — Isolated synthetic React chronology inspector

**2026-10-17. Synthetic UI lab only; NOT mounted into Fabulaxiom, no SQLite/operator data, no Tauri IPC, no authoring controls and no real G3 authorization.**

Starting protected `main=f4011f03842af249cf4df5114b0a62b01eafef98`, after PR #56 merged with terminal Windows `pull_request` CI #39030884718 (38/38 SUCCESS, 17/17 new source-identity audit tests). Source donor: draft PR #35 at `41ce7b915e76d22785d53d7fffe288d113dd0bf5`. This independent extraction copies and hardens only its standalone React inspector, not its other 82 files nor its source/service/SQLite proposals. PR #35 remains **OPEN/DRAFT/unmerged**.

## Delivered laboratory functionality

`src/M32ChronologyPreview.tsx` accepts a caller-created fictional in-memory Universe-scoped DTO. No import in `src/App.tsx`, no navigation/menu mounting, no fetch, network, storage, filesystem, `invoke`, SQLite or real source acquisition. React itself is installed already, with no dependency addition.

Three axes remain visibly separate: world-time human assertions (exact, approximate, relative or unknown, historical revoked/superseded states, fictional calendars and explicitly authored before/after), manuscript scene position within a Novel, and reader reveal explicitly *not authored*. Sorting IDs for display is **not** asserting fictional chronological order. Historical text revision IDs are displayed unchanged, distinct homonymous scenes remain distinct.

Before rendering, the module refuses mixed-Universe sources, unknown enum keys including JavaScript inherited properties (`toString` and `__proto__`), duplicate anchors/relations/scenes, dangling or self-referential precedence, invalid approximate calendar/precision, fabricated calendar/label/precision on relative/unknown dates, missing source revision IDs, invalid scene ordering and oversized synthetic arrays. React text escaping is used, not `dangerouslySetInnerHTML`. An invalid projection renders a refusal, not a partial leak.

**This is not a real M3.2 GUI feature:** it is not reachable by users and no real v7 data can be bound. The front-end DTO by itself does not authenticate a SQLite source, prove ACLs, reject all possible active graph cycles or grant edit authority. It cannot substitute for 21 historical custody pins, 3 recent observations, 2 missing external anchors, or actual Windows operator acceptance.

## Exact-head qualification

The existing `npm run test:ci` and TypeScript `npm run build` exercise this new compiled but unmounted component. `src/m32ChronologyPreview.test.tsx` now contains **18** Vitest tests for separation, uncertainty, historical values, independence, reject-on-error, escaping, array preservation, empty data and security boundaries. The Windows CI adds a named targeted suite `npm run test:ci -- src/m32ChronologyPreview.test.tsx`, preserving every previous job and all dependency locks. Exact final HEAD terminal PR CI and 18/18 log results are required before protected merge. Tests are synthetic, not evidence of user-installed GUI usability.

**Unchanged gating:** historical `PENDING_EXTERNAL_ATTESTATION (21/3/2)`, prospective `NOT_STARTED`, G3 real `STOP_UNAVAILABLE` and G3/G4/G5/G6 `NOT_AUTHORIZED`. PR #35 stays OPEN/DRAFT; no production migration 007, original opens, v6 marker switch, writer IPC, M3.3, release or independent human-signoff claim.

Sources: `docs/roadmap/M3_TIME_KNOWLEDGE_RELATIONSHIPS.md`, `docs/qualification/M3_2_MANUAL_CHRONOLOGY_UX_CONTRACT.md` in draft PR #35, and SQLite transaction notes https://sqlite.org/lang_transaction.html.
