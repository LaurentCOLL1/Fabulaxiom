# M2.2 — No-AI Narrative Entity and Alias CRUD (Windows Qualification)

## Status and provenance

- **Windows operator functional qualification: PASS** on the exact original implementation source `b54fffd8e1f0224372e3b99cee07cb6df3203973`.
- Repository: private `LaurentCOLL1/Fabulaxiom`; implementation PR **#23** on `feat/m2-2-entity-alias-crud-20261008`.
- Starting `main`: `70beb4f998ba3e587533dd7a90689eadeae4f4c3` (post-M2.1 normalized).
- Initial implementation source: `433aeeb2673c2c4b7f2cf2e4828a5956ac447a20`.
- Defensive UI fix: `63ad536ee08d8fd7edbe44561c8864ada212f14a`.
- Final targeted event-value fix and Windows-qualified source: `b54fffd8e1f0224372e3b99cee07cb6df3203973`.
- Source-head `Fabulaxiom CI`: run **37831790345**, `pull_request`, `completed/success`; Windows frontend/Rust job and all steps passed.
- Documentary evidence HEAD: `a96870f823f24cb8962c9b0f43336ccb883ad5c3`; exact-head `Fabulaxiom CI` run **37864503602**, `pull_request`, **completed/success** with the Windows job and every step successful.
- Implementation PR #23 **merged** with `expected_head_sha=`a96870f823f24cb8962c9b0f43336ccb883ad5c3` and re-fetched on `main` at merge SHA `ad7211fa2f292b8bd9812e299dbb6be96214eb89`.
- This separate normalization PR must pass exact-head CI and merge before M2.2 is declared NORMALIZED. M2.3+ remain unauthorized up to that boundary.

## Delivered scope

- Rust narrative entity/alias CRUD services, DTOs, deterministic validation/errors, thin Tauri commands and React entity workspace.
- Six entity kinds: `character`, `place`, `organization`, `object`, `event`, `world_rule`.
- Entity ID, owning Universe and kind immutable; display names can be renamed; distinct entities may share a name.
- Alias IDs and ownership immutable; alias strings can be created, listed, renamed and deleted.
- Per-owner duplicate alias rejection; guard against deleting an entity that retains aliases; transaction/rollback regression tests.
- SQLite v4 registry/alias `STRICT` schema, FKs, four identity triggers, indexes and restored-active-database resolution preserved.
- No dependence on Ollama for entity/alias CRUD; no fact/canon, timeline, FTS5, embeddings, ComfyUI or cloud AI implementation.

## Incident and regression fix

- Initial Windows interactive trial created six kinds, same-name distinct identities and renamed entities, but alias entry blanked the React application.
- The first defensive fix isolated entity rendering with `EntityErrorBoundary`, retained other modules and validated incoming IPC snapshots. Follow-up exposed `Cannot read properties of null (reading 'value')`.
- Root cause: reading `e.currentTarget.value` inside a deferred functional React state updater after the event handler had returned.
- Corrective HEAD captures `const value = e.currentTarget.value` synchronously in `onChange`, then passes the string to `updateAliasDraft(prev, entity.id, value)`.
- Two targeted tests cover a cleared event target and independent drafts for two entities; alias-list rendering and IPC snapshot-shape tests also cover the regression.

## Automated Windows preflight

- Exact HEAD, branch/upstream, fast-forward and clean worktree: PASS.
- Ollama process absent and port 11434 not listening: PASS.
- `npm ci`: PASS; zero vulnerabilities reported.
- `npm run test:ci`: **21/21 PASS** (6 test files).
- `npm run build`: PASS (`tsc` and Vite production build).
- `cargo test --manifest-path src-tauri/Cargo.toml --all-targets --locked`: **51/51 Rust PASS**.
- `cargo check --manifest-path src-tauri/Cargo.toml --locked`: PASS.
- Dependency lockfiles `package-lock.json` / `src-tauri/Cargo.lock` unchanged; final local worktree CLEAN.
- Five nonfatal Rust warnings were observed (unused import / unread error payload fields / unused `atomic` helper). No source cleanup was introduced in this acceptance commit.

## Operator interactive qualification on real Windows

The operator explicitly reported **13/13 PASS** while running Tauri desktop at the exact source SHA, with Ollama `INDISPONIBLE`:

1. Created alias for an existing character and observed it rendered.
2. Other Fabulaxiom modules remained visible.
3. Added a second alias to the same character.
4. Renamed an alias.
5. Deleted an alias with confirmation.
6. Attempted a duplicate alias and observed deterministic refusal.
7. Confirmed two characters keep separate alias drafts.
8. Inspected all six narrative entity categories.
9. Confirmed two same-name characters retained distinct IDs.
10. Confirmed deleting an entity with aliases was refused.
11. React → Tauri → Rust bridge and SQLite v4 checks passed.
12. Ollama reported unavailable without impairing CRUD.
13. No operation blanked the interface.

This is an operator observation, not an automated UI-end-to-end test; no unperformed UI test is claimed.

## Post-interactive SQLite integrity — actual active restored database

- App closed; local exact HEAD and CLEAN worktree: PASS.
- Root: `C:\Users\lauco\AppData\Local\com.fabulaxiom.desktop`.
- Active activation marker: `database\activations\activation-00000000000001791428210523732000-0000025660-0000000002.active`.
- Resolved active file (NOT the default database): `database\fabulaxiom-restored-00000000000001791428210487599800-0000025660-0000000001.sqlite3`.
- Historical operator pre-M2.1 v3 backup preserved: `fabulaxiom.operator-pre-m2-1-v3.20261008-170752-0746ccd626fb4030a8c1c3b35801db32.sqlite3`.
- Historical backup SHA-256 still: `f8ec1a1f32f97a0b4f39eeb238c307e5a192854cdd6c4206a05a97b6a385c987`.
- Read-only query verified all four expected migrations, `schema_owner=fabulaxiom`, both registry tables `STRICT`, four immutability triggers and two registry indexes.
- `PRAGMA foreign_key_check = []` and `PRAGMA integrity_check = ok`.
- M1 hierarchy retained: 1 Universe, 1 Series, 1 Novel, 1 Chapter and 1 Scene.
- Before interactive tests: 8 narrative entities, 2 aliases, 3 scene revisions and 1 current pointer.
- After interactive tests: **9 narrative entities, 8 aliases**, 3 scene revisions and 1 current pointer.
- Same-name groups after tests: **1**, with two `character` rows named `QUAL-M22-PERSONNAGE` under one Universe, and **different IDs**.
- Alias ownership and duplicate-alias checks: PASS; duplicate alias rows per `(entity_id, alias)` absent. The same alias string across different entities is permitted.
- Complete inspection of the nine narrative entity records and eight alias records returned normal values; no operator data was auto-deleted.
- Immutable scene history content digest (before and after): `b5af6edaba9fc143d0c319b9408316aa61b934ed7e123241a7a43010536f71e3`.
- Current-head digest (before and after): `8fe7aeb570f121c05083aa3cee06f95bf5fb6c98922c3357f00327ef8c708ce0`.
- Existing backups, active restored database, scene revisions and current pointer preserved; migrations were **not** reapplied as a new migration.
- Final operator summary: `M2.2 WINDOWS QUALIFICATION : PASS`; `INTERACTIVE TESTS : 13/13 PASS (OPERATOR)`; `POST-INTERACTIVE SQLITE : PASS`; `WORKTREE : CLEAN`.

## Post-merge normalization closure

- Original source qualified on real Windows: `b54fffd8e1f0224372e3b99cee07cb6df3203973`; operator interactive 13/13 PASS, and read-only posttest SQLite checks PASS.
- Evidence commit: `a96870f823f24cb8962c9b0f43336ccb883ad5c3`; full `Fabulaxiom CI` run `37864503602` completed/success on that exact pull-request HEAD, including all Windows steps and dependency lock check.
- Implementation PR #23 merged safely with the expected evidence-head SHA.
- Implementation merge commit `ad7211fa2f292b8bd9812e299dbb6be96214eb89` was re-fetched as exact `main`; PR #23 re-fetched as closed/merged with matching merge commit.
- No M2.2 app code changes are part of normalization; only documentation status and roadmap scope change.
- The **separate** normalization PR requires its **own** terminal successful `pull_request` CI, protected expected-HEAD merge, and postmerge authority re-fetch.
- Only then may M2.3 be considered the next authorized subdivision; it has **not** been started or implemented by this M2.2 closure. No ComfyUI implementation is authorized.

## Future visual extension — preserve without implementation

Issue **#19**, accepted proposal-only documentation `docs/roadmap/V1_VISUAL_REFERENCES_COMFYUI_PROPOSAL.md` (documentation PR #21), retains the request for optional local ComfyUI/manual-import visual references for characters, scene revisions and events. This is not implemented or authorized in M2.2.
