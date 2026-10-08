# Fabulaxiom — Next Authorized Work

## Current milestone

**M1 — Persistence and project foundation**

## Completed subdivision

**M1.4 — Text revisions and provenance foundation**

Status: **COMPLETE + MERGED + NORMALIZED**

Implementation PR: **#13 — feat: implement M1.4 text revisions and provenance foundation**

Implementation merge:

`75ab73b176b481f64b0e7f8c510b4ede0c617e31`

Qualified implementation SHA:

`d62fe92e4c01e5a58a6fbf85bdcf465267b41ea6`

Qualification evidence SHA:

`e6b3bf13399604a3b4922f9510a1c6761d9e5775`

Terminal exact-head CI:

- run `37709917550`;
- completed/success;
- frontend tests 10/10 PASS;
- Rust tests 29/29 PASS;
- frontend build, `cargo check --locked`, lockfiles PASS.

Windows acceptance:

- pre-migration SQLite v2 backup and SHA256 recorded;
- production migration v2 → v3 PASS;
- two STRICT revision tables and three migrations;
- UI revision creation/restoration history scenario PASS;
- preserved three revisions / one current head;
- foreign-key check empty; integrity check ok;
- Ollama stopped, HEAD exact, worktree clean.

## Authorized subdivision

**M1.5 — Backup and restore baseline**

Status: **WINDOWS QUALIFIED — FINAL EXACT-HEAD CI REQUIRED**

Implementation PR: **#15 — feat: implement M1.5 safe SQLite backup and restore baseline**

Branch: `feat/m1-5-backup-restore-baseline-20261008`

Base `main`: `2c942c5b58f316a5f02f69abfcf3883fb9d5929e`

Windows-qualified source HEAD: `7f968075f632843144c9833f61cc51910b538530`.

Pre-evidence CI: `Fabulaxiom CI` run `37718677686` completed/success; frontend 13/13, Rust 37/37, build/check, locks PASS.

Windows qualification: SQLite v3, Rust bridge, Ollama-off, application backup and restore, three preserved text revisions, hierarchy and current pointer: PASS.

Detailed report: `docs/qualification/M1_5_BACKUP_RESTORE_BASELINE.md`.

## Immediate sequence

1. commit this Windows qualification evidence to PR #15;
2. require new `Fabulaxiom CI` terminal success on the exact evidence SHA;
3. merge PR #15 only with the expected-head lease;
4. re-fetch live `main`;
5. create a separate post-merge M1.5 normalization PR and qualify its own exact-head CI;
6. merge normalization, re-fetch `main` and only then determine if M1 is COMPLETE or M2 can be authorized.

M1 is not COMPLETE and M2 remains unauthorized until these gates finish.

## Required deliverables

1. provide an application-level backup command for Fabulaxiom's local database;
2. produce a consistent SQLite snapshot using the supported backup API or equivalent SQLite-consistent method;
3. store backups at an explicit controlled destination without overwriting existing backups;
4. validate source and backup integrity, migration/schema compatibility and foreign keys;
5. provide an application-level restore path with a safe, controlled destination and integrity verification;
6. never overwrite a live database, existing source file or the operator's pre-M1.2/pre-M1.4 backups without explicit safe controls;
7. design rollback or failure behavior so an interrupted restore cannot partially corrupt an existing database;
8. preserve historical scene revisions, provenance and current-revision pointers exactly;
9. isolate filesystem access in Rust services behind minimal Tauri commands and deterministic errors;
10. include usable, explicit React backup/restore controls with safety-focused confirmation where necessary;
11. test backup consistency, restore integrity, source/target failures, rollback, and no unintended mutation;
12. preserve existing M1.1–M1.4 tests and lockfiles; avoid new dependencies unless justified;
13. require terminal exact-head Windows CI and target-machine backup/restore qualification;
14. merge the M1.5 implementation PR only after qualified evidence receives new exact-head CI;
15. post-merge normalize M1.5 before considering M1 complete.

## Boundary

M1.5 is the backup/restore **baseline** only.

Do not implement:

- FTS/semantic search or embeddings;
- canonical-fact extraction and narrative entities;
- consistency analysis;
- AI generation or manuscript generation;
- other unapproved M2+ features.

Do not silently delete or supersede preexisting operator backups.
