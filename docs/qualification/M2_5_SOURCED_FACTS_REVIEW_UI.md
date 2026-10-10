# M2.5 — Sourced facts and human review UI — implementation gate

**IMPLEMENTATION WINDOWS ACCEPTANCE: PASS ON SOURCE HEAD `7eaaf45ae164c9336df7e01c9da6787e4971d59e`. EVIDENCE-HEAD CI, PROTECTED MERGE AND NORMALIZATION PENDING. NOT MERGED.**

Authority: normalized main 11e9614ccecb42c64d50614e3b87b6062254cec6, after protected M2.4 PR #27 implementation and PR #28 normalization. Implementation branch: `feat/m2-5-sourced-facts-human-review-ui-20261009`.

## Implementation scope

- A new dedicated React facts workspace separated from the M2.2 entity CRUD module by its own error boundary. Select a Universe, entity, optional temporal descriptor and provenance.
- For **sourced** facts, navigate same-Universe Novel/Chapter/Scene hierarchy and choose an immutable scene text revision, then select an exact passage in a read-only field. Convert browser UTF-16 selection indices to **UTF-8 byte** offsets and reject selections splitting Unicode codepoints. Submit the original revision ID, bytes, quote and new durable IDs to M2.3 Rust/Tauri `create_narrative_fact`; Rust remains authoritative for cross-Universe and exact passage validation. **Unsourced** facts visibly lack provenance and never receive a fabricated source.
- Browse saved facts and optional fictional temporal validity, as well as separate `draft`, `suggestion`, `canon`, `variant`, `unknown`, `ambiguous`, `contradictory` statuses. Every new fact begins draft, even if sourced.
- Read-only `fact_source_revision` Tauri command loads original immutable historical revision by citation and independently compares Unicode bytes, avoiding interpretation of the mutable current scene-head pointer.
- Read-only human review history with explicit proposed state, **self-declared reviewer label** and reason. Promote using M2.4 `approve_canon` plus exact phrase `APPROVE_CANON`; revoke using `revoke_canon` plus `REVOKE_CANON`. The UI requires a distinct checkbox and user confirmation dialogue for both. It never silently auto-promotes. Optimistic review revision is passed through and enforced again by Rust/SQLite.
- Existing IPC errors surface as stable, visible messages; malformed facts/review/source results are rejected rather than crashing the window. Keep independent diagnostics, hierarchy, backup and entity modules accessible.
- No new dependency, no new SQLite migration, no Ollama/AI calls, no M3 chronology or semantic search, and **no ComfyUI**. The separate visual references/ComfyUI request stays a future, unimplemented proposal (issue #19).

## Automated qualification required

- Frontend pure DTO/IPC invalid-shape tests, exact UTF-16 → UTF-8 byte quote tests (accent, emoji, split surrogate), status-review approval/revocation and optimistic history checks, SSR baseline render.
- Rust exact historical cited revision read test including head changes, cross-Universe refusal and unsourced-fact refusal. Existing immutable source and review unit tests must remain green.
- CI `Fabulaxiom CI` on every **exact HEAD** with frontend tests, build, all Rust tests, cargo check locked and unchanged package/Cargo lockfiles. A new commit invalidates previous job results.

## Operator Windows qualification — original acceptance requirements (subsequently performed)

1. Re-fetch actual GitHub main, PR, HEAD, exact CI; qualify only a source with all terminal jobs green. Re-fetch the exact local branch using non-destructive fast-forward; require CLEAN source and lockfiles.
2. **Before running the M2.5 Tauri frontend**, close Fabulaxiom/Tauri/Ollama, resolve the real restored active SQLite v6 via current M1.5 activation marker and verify historical operator backups and original data; create a **new separately retained SQLite-consistent pre-M2.5 v6 backup + manifest** if exercising writes on the operator live DB. Prefer a disposable isolated local database for end-to-end create/review tests. Never silently switch active database or overwrite originals.
3. Windows UI operator acceptance across **two universes and multiple novels/scenes**: no-Ollama manual fact create both sourced/unsourced; verify saved exact source and historical revision after current head changes; Unicode accents/emoji boundaries; reject incorrect cross-universe and invalid citation; review unknown/ambiguous/contradictory/variant and suggestion states without automatic canon; explicit human approve/revoke; durable audit and stale review rejection; ensure no blank screen.
4. After application exit, inspect **actual activated DB** and any isolated fixture database in read-only mode, verify schema v6 unchanged, FK/integrity and all pre-existing row-digests, back-up hashes, the three immutable scene revisions and head, nine preexisting entities/eight aliases. Preserve user's original records and test records as declared; no cleanup without authorization.
5. Only after Windows **functional** PASS: evidence docs commit, requalify new exact-head CI, protected implementation merge using expected SHA, re-fetch main, then **separate** post-merge normalization PR with its own green exact-head CI and protected merge. No M3 or ComfyUI until formally authorized after M2 completion.

The requirements above are historical acceptance gates. Actual Windows evidence and current merge status are recorded below; M2.5 is not declared merged or normalized.

## Windows isolated operator checkpoint — 2026-10-10 — NOT ACCEPTED

- Operator qualified exact implementation HEAD `35fb842c1f9b7933a4b7e9ae6b6250dd754117c4` (first-source CI #37996421228 green) in detached isolated worktree under `M:\Fabulaxiom-M25-qual-35fb842c`. This is a **local-only** Tauri identity override; the tracked branch remains unchanged.
- Independent **before-write** baseline v6 on `com.fabulaxiom.desktop` logical schema/data SHA256 `67dfd9194ff884762bbffaa39d774df10fadcd74cbc9e6774e36d323e4506fc6`; isolated `com.fabulaxiom.m25qual35fb842c` initially empty logical SHA256 `af4b30f5b3ca32fd06618793a7f78954042e94822b43f5c579d817e7ff1961f3`. Backup custody and FK/integrity checked, all PASS.
- Isolated operator subsequently created **two test Universes, two Novel→Chapter→Scene hierarchies, two revisions in Unicode scene, one revision in alternate-Universe scene, two homonymous characters in separate Universes and one object**, with 8/8 hierarchy, entity, revision, no-Ollama and app-stability checks PASS. These test records **now exist in the isolated v6 database** and must not be silently deleted or treated as empty baseline.
- **BLOCKER discovered:** existing M2.5 `FactWorkspace` displayed `Aucun univers` after those successful creations; its **Actualiser** button was disabled with no selected Universe and previously reloaded only entity/fact/review snapshots, not `hierarchy_snapshot`. Cannot declare M2.5 accepted or proceed to canonical fact writes until a new HEAD fixes the bug and an operator confirms it.
- Targeted fix: invalidate/re-fetch hierarchy after successful hierarchy mutations, preserve valid selected Universe or choose first available, allow refresh with no selection, observe entity and scene revision changes, and add regression coverage. No SQLite migration, dependencies, or canonical policy changes. New candidate SHA and fresh exact-head CI must replace historical results.
- **Next operator boundary:** keep original detached worktree and all isolated records, and revalidate production snapshot and backups. Re-qualify updated source with non-destructive worktree/revision switch only after CI green; verify automatic and manual hierarchy refresh, entity and revision updates, and then continue separate facts/review UI tests. Re-audit both actual databases post-test, without creating test facts in production. No merge or M3/ComfyUI.

## Actual Windows implementation acceptance — PASS, 2026-10-10

### Exact source and CI

- PR **#29** remains OPEN at this documentary-evidence checkpoint. Qualified implementation source is `7eaaf45ae164c9336df7e01c9da6787e4971d59e` derived from normalized `main=11e9614ccecb42c64d50614e3b87b6062254cec6`.
- `Fabulaxiom CI` **pull_request** [run 38017441504](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/38017441504): `completed/success`, Windows job **13/13** steps PASS on the exact source HEAD; frontend **32/32** tests, TypeScript/Vite build, Rust **72/72** tests, `cargo check --locked`, and unchanged dependency locks all PASS.
- Previous failing workflow runs relate only to older source SHAs. **This qualification document commit creates a new HEAD and invalidates that run as merge authorization; evidence-head CI must be terminal-green before merge.**

### Isolation and custody

- Isolated Windows test application: detached worktree `M:\\Fabulaxiom-M25-sync-7eaaf45`, local-only identifier `com.fabulaxiom.m25qual35fb842c`, distinct from production `com.fabulaxiom.desktop`. The detached prior test worktree `M:\\Fabulaxiom-M25-qual-35fb842c` is preserved.
- Active production database is the **M1.5 restored-active** SQLite under `%LOCALAPPDATA%\\com.fabulaxiom.desktop\\database\\fabulaxiom-restored-00000000000001791428210487599800-0000025660-0000000001.sqlite3`, not the default `fabulaxiom.sqlite3`. Production pointer unchanged. Six migrations, foreign-key and integrity PASS. Complete production logical schema/data SHA-256 **`67dfd9194ff884762bbffaa39d774df10fadcd74cbc9e6774e36d323e4506fc6`**, unchanged throughout.
- Separate isolated SQLite v6: `%LOCALAPPDATA%\\com.fabulaxiom.m25qual35fb842c\\database\\fabulaxiom.sqlite3`. *Historical empty* baseline SHA-256 `af4b30f5b3ca32fd06618793a7f78954042e94822b43f5c579d817e7ff1961f3`; after narrative fixtures, before fact creation `02a122fbed60cd2ea6e1ec98967b397d67fc6499c625d5d580a8638a098e7e45`. Separate **SQLite-consistent** isolated pre-fact backup (237,568 bytes): `operator-qualification/m2_5/fabulaxiom.operator-pre-m2-5-v6.20261010T063838Z-5a1f631aa5c148e49377d0465b931706.sqlite3`, SHA-256 `9e738d58519e1a0e3c1750d71726b661132fcbc0211fddea3178f6314bbfc7cf` and associated verified `.manifest.json`; no overwrites.
- Original production historical backups preserved and independently hash-verified: pre-M2.1 v3 `f8ec1a1f32f97a0b4f39eeb238c307e5a192854cdd6c4206a05a97b6a385c987`; pre-M2.3 v4 `c624241080d6e820398cc502b4db206fcaba457405083ce806c302a6ce464976`; pre-M2.4 v5 `db02961d7a30c6a6522bd52faeab8ceb09e26c1a4a6a58be467d142806e22fee`. One *earlier script* flagged the v4 hash in error; independent direct hashing + v4 schema/content/manifest subsequently PASS. Do not rewrite old backup, digest or manifest.

### Operator UI and IPC acceptance

- 8/8 hierarchy, entity and scene-revision fixture actions PASS: actually **2** Universes, **2** Novels, **2** Chapters, **2** Scenes, 3 immutable revisions (two A Unicode, one B), 2 current revision heads, 3 entities (two same-name characters in distinct Universes plus one object). Zero Series, not 3 Novels; acceptance uses **actual** fixtures, not a script-invented extra Novel. No Ollama dependency.
- First UI run exposed `FactWorkspace` stuck on `Aucun univers`, with a disabled refresh. The repaired current source HEAD passed **8/8 operator cross-workspace sync checks**: both Universes visible without full page reload, manual `Actualiser` reloads the hierarchy, scoped entities and historical Unicode revisions visible, no blank React page, Ollama OFF. Data digest unaffected by read-only sync checks.
- **9/9 operator sourced/unsourced fact GUI tests PASS**: facts are all initially `draft`; two historical exact UTF-8 citations remain tied to their original immutable revision IDs even with a later current scene head; first cited passage `Été 🐈` is exactly [0,10) bytes in v1; second `ouvre le carnet` uses [51,66) bytes in v2. B Universe `hypothèse` is **unsourced** (no fabricated `fact_sources` row). Cross-Universe fact display scoped; no React/IPC crash. After this stage 3 facts, 2 sources, 0 reviews.
- **10/10 operator human-review GUI action checklist PASS**: cancel of explicit canon confirmation left history unchanged; checkbox/dialog guarded canon promotion and revocation, distinct suggestion/unknown/ambiguous/contradictory/variant statuses, review history and refresh persistence, no Ollama. A manually **self-declared** reviewer name is **not an authenticated identity**. The *operator checklist count* and *actual database event count* are not interchangeable.
- Rust/Tauri automated tests cover source-boundary rejection, wrong Unicode boundaries, cross-Universe, stale review revisions and illegal transitions; these are **not claimed to be separate operator GUI negative-path executions**.

### Independent read-only post-review SQLite acceptance — PASS

Source/test environment stopped before the audit. `PRAGMA foreign_key_check=[]` and `PRAGMA integrity_check=ok`. Production untouched, backup/manifest SHA custody PASS. Isolated final full logical schema/data SHA-256 **`cff8a04f29ec60757c02ef9ed186be40c806cfcc6a2cfd11fa8072be44f273cb`**. Reconstructed pre-fact original-table contents **all unchanged** (2 Universes, 2 Novels, 2 Chapters, 2 Scenes, 3 scene revisions, 2 scene heads, 3 original narrative entities). The new rows are **3 facts, 2 UTF-8 exact same-Universe source anchors, 11 review events**.

| Fact key | Stable fact ID | Citation byte range | Event chain | Current state |
| --- | --- | --- | --- | --- |
| `signe_du_chat` | `fact-d499ddca-be0e-4c1e-b78a-8de791697a21` | `[0,10)` | 8: draft→suggestion→unknown→draft→ambiguous→contradictory→variant→canon→draft | `draft` |
| `utilisation` | `fact-d27b49c3-e4e0-41b2-98af-cd4117d7d66e` | `[51,66)` | 2: draft→canon→suggestion | `suggestion` |
| `hypothèse` | `fact-4f91d70f-38a2-4ba4-82dc-80b740fc5722` | none, `unsourced` | 1: draft→unknown | `unknown` |

The initial human-review audit script asserted **10** events (7+2+1) but omitted a genuine eighth transition on `signe_du_chat`. An independent diagnostic identified 8+2+1 = **11 actual immutable events**, with contiguous per-fact revision chains, correct explicit canon approval/revocation and no orphaned review, same-Universe source or revised scene history. The subsequent operator `M2.5 READ-ONLY ACCEPTANCE : PASS` confirms **11/11**, production unchanged, all backups verified; **the audit performed zero writes**. Do not delete or massage genuine audit history to satisfy an incorrect historical script.

### Remaining governance gate

**WINDOWS FUNCTIONAL ACCEPTANCE: PASS for this source SHA; PR #29 is still NOT MERGED.** Next: evidence-document HEAD exact `pull_request` CI terminal success on *every job*, protected merge using exact HEAD compare-and-swap, re-fetch merged main, **separate post-merge normalization** PR and its own exact-head CI/protected merge. Only after normalized authority can M2 be declared COMPLETE and M3 be evaluated for authorization. M3/AI extraction and ComfyUI visual proposal issue #19 remain excluded from this PR.
