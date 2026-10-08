# M2.1 — Entity Registry Schema and Migration (Windows Qualification)

## Status

**WINDOWS QUALIFIED — TERMINAL EXACT-HEAD EVIDENCE CI REQUIRED**

Implementation PR: **#20 — feat: implement M2.1 narrative entity registry schema v4**.

Repository: private `LaurentCOLL1/Fabulaxiom`.

Implementation branch: `feat/m2-1-entity-registry-schema-20261008`.

Qualified exact source SHA: `c7a663d88ba2538714d42fdd366719cd54fe6f70`.

Original base `main`: `5fc54f234227ad43a91ffe28fe2662453221e31e`.

Current synchronized base at Windows qualification: `bf56b5817e55faa01ab9c43eacfbf88dc95e4a3b`.

Local repository: `M:\Fabulaxiom`.

## Delivered schema/compatibility scope

- SQLite schema version 4, additive migration `004_create_narrative_entity_registry`;
- `STRICT` Universe-scoped `narrative_entities` and `entity_aliases`;
- allowed narrative entity kinds `character`, `place`, `organization`, `object`, `event`, `world_rule`;
- immutable entity/alias IDs, immutable entity owner and kind, immutable alias ownership;
- restrictive foreign keys, nonblank identifiers/text, unique aliases per owner and relevant indexes;
- M1 hierarchy/revisions and active-restored-database selection preserved;
- M1.5 application backup/restore updated for v4 registry counts and legacy application-owned v3 backup restoration into an independent migrated v4 copy;
- no entity CRUD UI, canonical facts, ComfyUI/Ollama code or new dependency.

## Deterministic CI on implementation SHA

Workflow: `Fabulaxiom CI`.

Run: `37795098224`.

Conclusion: **completed/success**, all workflow steps successful on `c7a663d88ba2538714d42fdd366719cd54fe6f70`.

Local Windows pre-migration qualification:

- worktree clean and live/local exact main/branch SHA checks PASS;
- `npm ci` PASS, 0 vulnerabilities reported;
- frontend tests **13/13 PASS**, 5 files;
- frontend production build PASS;
- Rust tests **44/44 PASS**;
- `cargo check --locked` PASS;
- dependency lockfiles unchanged;
- three nonfatal Rust unused-import/dead-field warnings in `backup.rs`, not functional failures.

## Exact production active database and pre-migration backup

The app's M1.5 active database is **not** the default `fabulaxiom.sqlite3`.

Activation marker:

`C:\Users\lauco\AppData\Local\com.fabulaxiom.desktop\database\activations\activation-00000000000001791428210523732000-0000025660-0000000002.active`

Active SQLite file:

`C:\Users\lauco\AppData\Local\com.fabulaxiom.desktop\database\fabulaxiom-restored-00000000000001791428210487599800-0000025660-0000000001.sqlite3`

Operator-created SQLite-consistent pre-M2.1 backup, using Python SQLite backup API:

`C:\Users\lauco\AppData\Local\com.fabulaxiom.desktop\backups\fabulaxiom.operator-pre-m2-1-v3.20261008-170752-0746ccd626fb4030a8c1c3b35801db32.sqlite3`

Recorded backup SHA-256:

`f8ec1a1f32f97a0b4f39eeb238c307e5a192854cdd6c4206a05a97b6a385c987`

Before launching v4, the operator rechecked:

- marker, active DB name and immutable backup SHA-256: PASS;
- SQLite schema version 3 and exact migrations 1/2/3: PASS;
- SQLite owner: `fabulaxiom`;
- snapshot comparison of all M1 tables with saved backup: PASS;
- integrity/FK checks: PASS.

Pre-migration row counts:
- Universes 1, Series 1, Novels 1, Chapters 1, Scenes 1;
- Scene text revisions 3;
- Scene revision heads 1.

**The historical M1.2/M1.4/M1.5 backups and this operator-created pre-M2.1 backup must not be removed or overwritten.**

## Tauri Windows production migration and visual verification

App launched via `npm run tauri dev` from exact M2.1 implementation HEAD. Rust build and Tauri process startup/normal termination: PASS.

Observed `Vérifier la base locale`:
- PASS;
- `SQLite schema v4 · clés étrangères ON`;
- correct restored active database path, not a new/default path.

Observed `Tester le pont Rust`: PASS, React → Tauri → Rust operational.

The bootstrap status continues to display `M1.5 backup and restore baseline`. This historical UI marker is expected because M2.1 changes the database schema, not the bootstrap label.

Observed `Vérifier Ollama local`: `INDISPONIBLE` (EXPECTED). Hierarchy and text revision functionality remained usable without Ollama.

The operator confirmed the three saved text revisions and current revision remained accessible.

## Independent read-only post-migration verification

After the app was closed, an external Python SQLite read-only check reported:

- active database and activation marker: unchanged, PASS;
- SHA-256 of pre-migration v3 backup: unchanged, PASS;
- schema version: 4;
- migration records 1–4 exactly once: PASS;
- `narrative_entities` and `entity_aliases`: both STRICT (2/2);
- immutable-identity triggers: 4/4 PASS;
- registry indexes: 2/2 PASS;
- existing M1 rows across `app_metadata`, `universes`, `series`, `novels`, `chapters`, `scenes`, `scene_text_revisions`, `scene_revision_heads`: content equal to the saved v3 snapshot for each table (same row data);
- counts: app_metadata=1; universes=1; series=1; novels=1; chapters=1; scenes=1; scene_text_revisions=3; scene_revision_heads=1;
- narrative_entities=0; entity_aliases=0 (expected in schema-only M2.1);
- `PRAGMA foreign_key_check = []`;
- `PRAGMA integrity_check = ok`;
- final local HEAD exact: PASS;
- final worktree CLEAN: PASS;
- Ollama remained OFF: PASS.

This verification compares the **logical row values** to the v3 backup; it does not assert identical raw SQLite file bytes after the schema migration.

## Conclusion and remaining governance gates

Windows implementation acceptance: **PASS**, bound to exact SHA `c7a663d88ba2538714d42fdd366719cd54fe6f70`.

The evidence commit will change the PR HEAD; run `37795098224` becomes historical and **cannot authorize merging that new HEAD**.

Remaining:
1. qualification evidence commit;
2. terminal exact-head PR CI on new SHA;
3. protected merge of PR #20, only after re-fetch and success;
4. re-fetch `main`;
5. post-merge M2.1 normalization PR, terminal exact-head CI, and merge;
6. only then determine M2.2 authorization from live authorities.

**M2.2 and all later subdivisions remain unauthorized now.**
