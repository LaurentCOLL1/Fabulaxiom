# M2.4 — Human-governed fact status and append-only review qualification

**EXACT SOURCE WINDOWS QUALIFIED — IMPLEMENTATION PR #27 MERGE AND NORMALIZATION PENDING**

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

## Mandatory Windows boundary — COMPLETED ON EXACT SOURCE
1. Obtained terminal exact-head green CI and re-fetched governance + PR files before Windows migration.
2. Stop Fabulaxiom, `tauri dev`, Ollama. Resolve the real restored-active SQLite using the newest M1.5 activation marker; **do not assume** the default database path.
3. Take a **new SQLite-consistent pre-v6 backup of the active v5 database** to its own non-overwriting custody path and verify SHA256, manifest, migration history, FK/integrity, all original row digests and scene-head/revision lineage. Keep both pre-M2.1 and pre-M2.3 backups intact.
4. Only then perform a controlled application-driven migration **v5→v6**, explicitly keeping database backups and marker unchanged.
5. With Ollama off, operator verifies v6 diagnostic and original hierarchy/9 entities/8 aliases/3 scene revisions/1 current head, no blank screen, and no M2.5 fact review UI claimed.
6. After app exit, read-only audit v6: exact six migration rows, STRICT review table, trigger/index/FK invariants, zero review events before any operator review, old table counts/content digests exactly matching pre-v6 manifest, backups unchanged, `foreign_key_check=[]`, `integrity_check=ok`.
7. Any manual review API exercise needs explicit safe test facts, separate from production data or operator-authorized test setup; do not write unrequested fact/review rows into the user's main database. UI 8/8 migration tests are not proof of fact review API usage.
8. Windows migration and isolated review tests passed. **Still outstanding:** evidence commit, new SHA exact-head green CI, protected implementation merge and independent normalization PR/CI; **M2.5 is blocked until M2.4 NORMALIZED**.


## Operator evidence — 9 October 2026

**Qualified source exact HEAD:** `aad56bd59fdb87be5ac1eda99b1969452bf61a26` (after E0308 single-file Rust fix from failed original source). `Fabulaxiom CI`, event `pull_request`, run [37974831473](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/37974831473): `completed/success`, all 13 Windows steps PASS. Automated 21/21 frontend tests, frontend build, 71/71 Rust tests, `cargo check --locked`, both lockfiles unchanged; operator also repeated local 21/21 frontend and 71/71 Rust tests, source-head/worktree PASS. Existing Rust unused/dead-code warnings are non-blocking.

**Protected backup and marker:** before v6 start, operator closed Fabulaxiom/Tauri/Ollama, resolved actual M1.5 restored-active database using marker `activation-00000000000001791428210523732000-0000025660-0000000002.active`; active file `fabulaxiom-restored-00000000000001791428210487599800-0000025660-0000000001.sqlite3` under the application database folder, **not** assumed default. A new *consistent and non-overwriting* v5 backup `operator-qualification/m2_4/fabulaxiom.operator-pre-m2-4-v5.20261009T200405Z-ed169c2ac6724ab6aca018024b26e8af.sqlite3`, **217088 bytes**, SHA-256 `db02961d7a30c6a6522bd52faeab8ceb09e26c1a4a6a58be467d142806e22fee`, manifest verified against v5 source row counts and content. Old pre-M2.3 backup SHA-256 `c624241080d6e820398cc502b4db206fcaba457405083ce806c302a6ce464976`; pre-M2.1 SHA-256 `f8ec1a1f32f97a0b4f39eeb238c307e5a192854cdd6c4206a05a97b6a385c987`. All preserved; no restore or overwriting.

**Controlled migration and interactive checks:** prelaunch v5/backup/manifest/pointer/HEAD PASS; operator launched v6 Tauri, ran the **Vérifier la base locale** action, observed schema v6 without error, and reported **8/8 PASS** (Universe, Series, Novel, Chapter, Scene, six entity categories, nine narrative entities/eight aliases, separate IDs for same-name characters, three scene revisions/current head, Ollama unavailable, no React blank screen). No new fact-review editing screen exists.

**Independent read-only v6 audit after app exit:** exact migration rows v1–v6, `fact_review_events` STRICT, required triggers and index, composite fact/universe FK, `foreign_key_check=[]` and `integrity_check=ok`: all PASS. Every original v5 table's count and logical content SHA-256 exactly matched the verified pre-v6 manifest; nine entities/eight aliases and three scene revisions/one current head preserved. There were 0 facts, 0 sources and **0 review events** (correct before any user actions). Scene revision digest `b5af6edaba9fc143d0c319b9408316aa61b934ed7e123241a7a43010536f71e3`, current head digest `8fe7aeb570f121c05083aa3cee06f95bf5fb6c98922c3357f00327ef8c708ce0`; exact matches. Active marker, all backups and worktree unchanged. Operator banner `M2.4 WINDOWS SQLITE V6 QUALIFICATION : PASS`.

**Isolated real Windows Rust review tests:** 8/8 of `review::tests` PASS with single test thread and locked Cargo resolution. Tests explicitly cover draft default, suggestion not auto-canon, explicit approval/revocation, seven state variants, duplicate/stale/cross-Universe rejection, immutable direct-SQL audit, entity rename preservation and reviewer-label/confirmation constraints. Production SQLite read-only schema/data snapshot SHA-256 was `67dfd9194ff884762bbffaa39d774df10fadcd74cbc9e6774e36d323e4506fc6` **before and after** the isolated tests; original base/backup/pointer untouched; clean worktree.

**Qualification boundary:** these Windows results qualify SQLite migration, existing GUI non-regression and *in-memory Rust review service* behavior. They are **not** an E2E Tauri IPC interaction or a manual Windows React review UI test, and the self-declared reviewer label is not authenticated. No production fact/review test rows were inserted. No AI/Ollama automatic canon promotion was introduced.

**Outstanding GitHub gates:** create an evidence-only documentary commit on PR #27; requalify **all** `pull_request` jobs on its **new** exact HEAD, protected merge PR #27 with expected SHA, then **separate** post-merge normalization PR/CI and re-fetch normalized authorities. M2.5 and ComfyUI implementation remain unauthorized before M2.4 normalization.

## Deferred
Existing issue #19 + `docs/roadmap/V1_VISUAL_REFERENCES_COMFYUI_PROPOSAL.md` retain the request for local ComfyUI/manual imported visual references, but implementation remains unauthorized.
