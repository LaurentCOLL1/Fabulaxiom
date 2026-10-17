# M3.2 — Unmounted React human-precedence comparison (synthetic)

**2026-10-17, isolated frontend laboratory; no operator-source data, no real G3, no Tauri command, no SQLite access, no production UI mount.**

Starting protected `main=20e3176896da325cbbd8683bb7692161cd7ad6f0` after exact-qualified PR #57 (Windows CI #39033928000, 39/39 steps and 18/18 targeted React tests PASS). The large PR #35 remains OPEN/DRAFT and unmerged. This independent six-file PR does not incorporate its unpublished business logic or DB services.

## New functionality

`src/M32WorldOrderComparison.tsx` is a standalone **unmounted**, read-only React component plus exported pure graph function consuming **only a caller-provided fictional projection**, revalidated through `decodeM32ChronologyProjection`. The explicit two selected IDs must both be current in the same fictional Universe. Relation is `same`, `before`, `after`, or `incomparable`; display translates the last as **« Ordre indéterminé »**, not an impossibility or a total ranking.

Only active, human-written `before_anchor_id -> after_anchor_id` edges are traversed. Historical revoked/superseded edges never provide current precedence. Active edges to historical anchors and duplicated active endpoint pairs are refused. An active cycle **anywhere** vetoes the entire preview by an iterative Kahn graph check (up to 512 anchors / 2048 edges inherited from the bounded DTO), rather than hiding a contradiction. No reading or sorting fictional calendar strings, novel scene order, text revisions or reader reveal to construct new world precedence.

When a path exists, breadth-first traversal returns a **shortest authored edge chain**, chosen deterministically by edge ID for ties and containing unchanged human reasons plus immutable edge/source IDs. When no path exists, the witness list is empty. For reversed selection `after`, witnesses still show human-authored world direction `before -> after`. For identical selected IDs, `same` is an identity check only. Neither the witness nor a client-provided projection is a historical source attestation, permission, signature, integrity proof or valid production custody.

Rendered text is React-escaped; all output is display-only with no button/input/form, Tauri invocation or network. The component is **not imported in `App.tsx`** and thus not visible to an operator, even if the frontend TypeScript/Vite build compiles it. This does not claim M3.2 complete or Windows functional operator acceptance.

## Synthetic qualification

`src/m32WorldOrderComparison.test.tsx` contains **24 tests**: direct/transitive/reversed witness, same/unrelated, retired edges, historical endpoints, dangling/foreign/self/duplicate edges, local and unrelated cycles, invented calendar non-inference, stable shortest chain, escaping, immutable payload, bounded graph and a never-authorized display. The existing `npm run test:ci` plus an additional explicit targeted Windows CI step cover the new tests; `npm run build` must compile strict TypeScript and all old Windows Rust/Python checks must pass at **the final exact PR SHA**.

## Limitations and STOP boundary

The Python-only candidate reference modules in draft PR #35 are not imported. Graph computations only verify internal consistency of invented inputs; they cannot authenticate the real v7 source, source revisions, WAL/journals, exclusive owner, external custody or permission. Source-G3 is still `STOP_UNAVAILABLE`, historical `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, actual G3/G4/G5/G6 `NOT_AUTHORIZED`. No protected original is opened, no automatic migration 007, writer IPC, activation marker, M3.3, release or PR #35 merge.

References: https://www.sqlite.org/lang_with.html ; https://react.dev/learn/conditional-rendering ; `docs/roadmap/M3_TIME_KNOWLEDGE_RELATIONSHIPS.md`.
