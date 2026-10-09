# M2.4 — Human-governed fact status and append-only review qualification

**IMPLEMENTATION IN PROGRESS — NOT WINDOWS QUALIFIED — NOT MERGED**

Authority: live normalized `main=ebaaf62933dadf6f0662ca749227a0b340b8a7e3`, M2.3 COMPLETE + MERGED + NORMALIZED.
Branch: `feat/m2-4-canon-status-review-20261009`.

## Strictly limited implementation
- Additive migration **SQLite v6**: `fact_review_events` in a STRICT, FK-scoped append-only table. Each fact's current status is **derived** from its latest review event, with a `draft` default for facts without reviews. Original v5 facts, citations, scene revisions and source bytes stay immutable.
- Status vocabulary: `draft`, `suggestion`, `canon`, `variant`, `unknown`, `ambiguous`, `contradictory`.
- Deterministic Rust/Tauri read history, list Universe-scoped review states, and write a human-declared review with expected revision, reviewer label, rationale, explicit action type, immutable event ID and timestamp.
- No inferred human identity: `reviewer_label` is a declared, non-authenticated label. A `canon` transition requires `approve_canon` plus explicit confirmation phrase `APPROVE_CANON`; removing canon requires `revoke_canon` and `REVOKE_CANON`. Both event history and DB triggers refuse silent/automatic promotion.
- Optimistic revision checks and status change rules reject invalid status, identical state, stale reads, duplicate review IDs, cross-Universe access and direct SQL attempts to rewrite review history. All changes atomic with no update of original fact records.
- No Ollama dependency, AI extraction, canon suggestions inferred from LLM output, calendar engine, FTS, chronology or ComfyUI. No M2.5 React fact review/edit UI. The commands are manual-facing APIs, not authenticated proof of a person.

## Required CI
- `npm ci`, frontend tests/build, `cargo test --all-targets --locked`, `cargo check --locked`, unchanged `package-lock.json` and `Cargo.lock`.
- V1–V6 migration test, **v5→v6** on existing fact/source and exact scene revision/head data; idempotence; STRICT, FK and integrity checks.
- Rust tests: default draft; manual suggestion and approval/revocation; invalid transitions; stale concurrent revision; signed human confirmation; many unresolved statuses; immutable audit history; cross-Universe FK; entity renames; no altered source or fact.
- Backup service must restore historical v3/v4/v5 files into **new v6 copies**, never overwrite source, retain all old backup hashes and M1.5 active marker. Review events must be included in counts and checked for a valid chain.
- All assertions must pass **on the exact pull_request head SHA** after every source change.

## Mandatory Windows boundary — NOT YET AUTHORIZED
1. Obtain fresh exact-head green CI and re-fetch all governance + PR files first. Do **not** launch the M2.4 executable on `M:\Fabulaxiom` yet.
2. Stop Fabulaxiom, `tauri dev`, Ollama. Resolve the real restored-active SQLite using the newest M1.5 activation marker; **do not assume** the default database path.
3. Take a **new SQLite-consistent pre-v6 backup of the active v5 database** to its own non-overwriting custody path and verify SHA256, manifest, migration history, FK/integrity, all original row digests and scene-head/revision lineage. Keep both pre-M2.1 and pre-M2.3 backups intact.
4. Only then perform a controlled application-driven migration **v5→v6**, explicitly keeping database backups and marker unchanged.
5. With Ollama off, operator verifies v6 diagnostic and original hierarchy/9 entities/8 aliases/3 scene revisions/1 current head, no blank screen, and no M2.5 fact review UI claimed.
6. After app exit, read-only audit v6: exact six migration rows, STRICT review table, trigger/index/FK invariants, zero review events before any operator review, old table counts/content digests exactly matching pre-v6 manifest, backups unchanged, `foreign_key_check=[]`, `integrity_check=ok`.
7. Any manual review API exercise needs explicit safe test facts, separate from production data or operator-authorized test setup; do not write unrequested fact/review rows into the user's main database. UI 8/8 migration tests are not proof of fact review API usage.
8. Only after Windows PASS: evidence commit, new SHA exact-head green CI, protected implementation merge and independent normalization PR/CI; **M2.5 is blocked until M2.4 NORMALIZED**.

## Deferred
Existing issue #19 + `docs/roadmap/V1_VISUAL_REFERENCES_COMFYUI_PROPOSAL.md` retain the request for local ComfyUI/manual imported visual references, but implementation remains unauthorized.
