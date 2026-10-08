# M1.4 — Text Revisions and Provenance Foundation: Windows Qualification

## Gate

**WINDOWS QUALIFIED — FINAL EXACT-HEAD CI PENDING**

M1.4 is **not** COMPLETE yet. Merge and post-merge normalization are required before M1.5.

## Live source and operator environment

- Repository: `LaurentCOLL1/Fabulaxiom` (private).
- Implementation PR: #13 — `feat: implement M1.4 text revisions and provenance foundation`.
- Implementation branch: `feat/m1-4-text-revisions-provenance-20261007`.
- `main` at implementation start: `d75971ca0540c6811d8728ec4f6431d39125bbb2`.
- Exact implementation SHA qualified on Windows: `d62fe92e4c01e5a58a6fbf85bdcf465267b41ea6`.
- Local worktree: `M:\Fabulaxiom`.
- SQLite database: `C:\Users\lauco\AppData\Local\com.fabulaxiom.desktop\database\fabulaxiom.sqlite3`.
- Remote refspec: `+refs/heads/*:refs/remotes/origin/*`.
- Source `main` and PR branch fetched and verified exact; HEAD and worktree clean.

## Pre-migration backup: VERIFIED

Prior production schema version: **2**.

Pre-migration database passed `PRAGMA integrity_check` and `PRAGMA foreign_key_check` before backup.

Backup created with Python `sqlite3.Connection.backup` API (not raw file copying):

`C:\Users\lauco\AppData\Local\com.fabulaxiom.desktop\database\fabulaxiom.before-m1-4-v2.20261008-023513-9d760433.sqlite3`

SHA256:

`0ca0ce4324dba0d3ae6861439576f92c819c741a09da9461c352cba264645d7d`

Backup operation and backup integrity check: **PASS**.

**Do not delete this backup or the earlier M1.2 pre-migration backup.**

## Local deterministic qualification with Ollama OFF

Initial checks:

- Fabulaxiom closed;
- Ollama processes absent;
- loopback API `127.0.0.1:11434/api/version` inaccessible;
- branch HEAD exact, upstream correct, worktree clean.

Frontend:

- `npm ci`: PASS, 0 vulnerabilities reported;
- `npm run test:ci`: 4 test files / **10/10 PASS**;
- `npm run build`: PASS.

Rust:

- `cargo test --manifest-path src-tauri/Cargo.toml --all-targets --locked`: **29/29 PASS**;
- `cargo check --manifest-path src-tauri/Cargo.toml --locked`: PASS.

Dependency lockfiles unchanged; final HEAD exact; worktree clean.

GitHub CI qualifying implementation SHA `d62fe92e4c01e5a58a6fbf85bdcf465267b41ea6`:

- workflow: `Fabulaxiom CI`;
- run: `37688250040`;
- `completed/success`;
- 10 frontend tests, 29 Rust tests, build/check, lockfiles: PASS.

## Interactive Windows verification

Fabulaxiom launched with Ollama stopped.

`Vérifier la base locale`:
- **PASS**;
- SQLite schema **v3**;
- foreign keys **ON**.

`Tester le pont Rust`:
- **PASS**;
- reported `M1.4 text revisions and provenance foundation`;
- React → Tauri → Rust operational.

`Vérifier Ollama local`:
- **INDISPONIBLE (EXPECTED)**;
- loopback Ollama API inaccessible.

Scene text revision scenario:
- operator reported the requested creation and revision-flow scenario **PASS**;
- plan exercised saving v1 and v2, restoring earlier revision as current, and saving v3 while retaining history;
- scene revision history is append-only and `parent_revision_id` is the provenance primitive;
- this is human UI qualification evidence; the final SQLite read-only report independently confirmed counts/integrity but did **not** output per-revision parent IDs.

`npm run tauri dev`:
- frontend dev server launched;
- Rust app compiled and launched;
- application closed normally;
- terminal reported **TAURI DEV TERMINE: PASS**.

## Post-qualification read-only verification

Reported by operator after closing the application:

- `SCHEMA VERSION = 3`;
- `MIGRATIONS = [(1, '001_create_app_metadata'), (2, '002_create_project_hierarchy'), (3, '003_create_scene_text_revisions')]`;
- `STRICT REVISION TABLES = 2`;
- `FOREIGN KEY CHECK = []`;
- `INTEGRITY CHECK = ok`;
- `SAVED REVISIONS = 3`;
- `CURRENT HEADS = 1`;
- exact local HEAD: PASS;
- final worktree clean: PASS;
- Ollama still OFF: PASS.

Revision history was **intentionally retained**. The M1.4 append-only revision schema and scene deletion guard prevent deleting a scene with saved revisions through normal CRUD. No test data was destroyed.

## Governance conclusion

M1.4 implementation on `d62fe92e4c01e5a58a6fbf85bdcf465267b41ea6` is accepted by deterministic tests and real Windows operator qualification.

The **new qualification-documentation commit** must receive its *own* terminal exact-head `Fabulaxiom CI`; run `37688250040` becomes historical for merge authorization.

Required next gates:

1. commit this qualification evidence in PR #13;
2. verify all PR-triggered CI jobs success on the new exact HEAD;
3. merge #13 with expected HEAD lease;
4. re-fetch `main`;
5. prepare and merge a separately qualified post-merge M1.4 normalization PR;
6. only then authorize any M1.5 implementation.
