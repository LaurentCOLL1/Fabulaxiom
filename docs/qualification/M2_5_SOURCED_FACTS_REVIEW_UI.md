# M2.5 — Sourced facts and human review UI — implementation gate

**IN PROGRESS — GITHUB SOURCE CI AND OPERATOR WINDOWS ACCEPTANCE PENDING. NOT MERGED.**

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

## Operator Windows qualification — NOT YET PERFORMED

1. Re-fetch actual GitHub main, PR, HEAD, exact CI; qualify only a source with all terminal jobs green. Re-fetch the exact local branch using non-destructive fast-forward; require CLEAN source and lockfiles.
2. **Before running the M2.5 Tauri frontend**, close Fabulaxiom/Tauri/Ollama, resolve the real restored active SQLite v6 via current M1.5 activation marker and verify historical operator backups and original data; create a **new separately retained SQLite-consistent pre-M2.5 v6 backup + manifest** if exercising writes on the operator live DB. Prefer a disposable isolated local database for end-to-end create/review tests. Never silently switch active database or overwrite originals.
3. Windows UI operator acceptance across **two universes and multiple novels/scenes**: no-Ollama manual fact create both sourced/unsourced; verify saved exact source and historical revision after current head changes; Unicode accents/emoji boundaries; reject incorrect cross-universe and invalid citation; review unknown/ambiguous/contradictory/variant and suggestion states without automatic canon; explicit human approve/revoke; durable audit and stale review rejection; ensure no blank screen.
4. After application exit, inspect **actual activated DB** and any isolated fixture database in read-only mode, verify schema v6 unchanged, FK/integrity and all pre-existing row-digests, back-up hashes, the three immutable scene revisions and head, nine preexisting entities/eight aliases. Preserve user's original records and test records as declared; no cleanup without authorization.
5. Only after Windows **functional** PASS: evidence docs commit, requalify new exact-head CI, protected implementation merge using expected SHA, re-fetch main, then **separate** post-merge normalization PR with its own green exact-head CI and protected merge. No M3 or ComfyUI until formally authorized after M2 completion.

This document records scope and gates, **not** proof of a completed implementation or Windows acceptance.

## Windows isolated operator checkpoint — 2026-10-10 — NOT ACCEPTED

- Operator qualified exact implementation HEAD `35fb842c1f9b7933a4b7e9ae6b6250dd754117c4` (first-source CI #37996421228 green) in detached isolated worktree under `M:\Fabulaxiom-M25-qual-35fb842c`. This is a **local-only** Tauri identity override; the tracked branch remains unchanged.
- Independent **before-write** baseline v6 on `com.fabulaxiom.desktop` logical schema/data SHA256 `67dfd9194ff884762bbffaa39d774df10fadcd74cbc9e6774e36d323e4506fc6`; isolated `com.fabulaxiom.m25qual35fb842c` initially empty logical SHA256 `af4b30f5b3ca32fd06618793a7f78954042e94822b43f5c579d817e7ff1961f3`. Backup custody and FK/integrity checked, all PASS.
- Isolated operator subsequently created **two test Universes, three Novel→Chapter→Scene hierarchies, two revisions in Unicode scene, one revision in alternate-Universe scene, two homonymous characters in separate Universes and one object**, with 8/8 hierarchy, entity, revision, no-Ollama and app-stability checks PASS. These test records **now exist in the isolated v6 database** and must not be silently deleted or treated as empty baseline.
- **BLOCKER discovered:** existing M2.5 `FactWorkspace` displayed `Aucun univers` after those successful creations; its **Actualiser** button was disabled with no selected Universe and previously reloaded only entity/fact/review snapshots, not `hierarchy_snapshot`. Cannot declare M2.5 accepted or proceed to canonical fact writes until a new HEAD fixes the bug and an operator confirms it.
- Targeted fix: invalidate/re-fetch hierarchy after successful hierarchy mutations, preserve valid selected Universe or choose first available, allow refresh with no selection, observe entity and scene revision changes, and add regression coverage. No SQLite migration, dependencies, or canonical policy changes. New candidate SHA and fresh exact-head CI must replace historical results.
- **Next operator boundary:** keep original detached worktree and all isolated records, and revalidate production snapshot and backups. Re-qualify updated source with non-destructive worktree/revision switch only after CI green; verify automatic and manual hierarchy refresh, entity and revision updates, and then continue separate facts/review UI tests. Re-audit both actual databases post-test, without creating test facts in production. No merge or M3/ComfyUI.
