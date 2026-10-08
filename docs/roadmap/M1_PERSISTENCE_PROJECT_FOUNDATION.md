# M1 — Persistence and Project Foundation

## Goal

Establish Fabulaxiom's authoritative local persistence layer and usable no-AI project foundation before narrative-memory intelligence.

## M1.1 — SQLite foundation and migration runner

Status: **COMPLETE + MERGED + NORMALIZED**

Final normalization merge:

`d99da744fc04303c0c094a8aa6a2daab9983136f`

Delivered:

- bundled SQLite through `rusqlite 0.40.2`;
- deterministic application-local database path;
- schema migration table;
- ordered transactional migration runner;
- `PRAGMA foreign_keys = ON` enforced and verified per connection;
- transaction helper/baseline;
- initial metadata schema;
- deterministic dependency locks;
- Windows operator qualification;
- exact-head CI;
- post-merge normalization.

## M1.2 — Project hierarchy schema

Status: **COMPLETE + MERGED + NORMALIZED**

Implementation merge:

`91b80e529679d3bc407b5f6ca49e578d86de1d44`

Delivered:

- schema migration v2;
- Universe;
- optional Series;
- Novel;
- Chapter;
- Scene;
- immutable stable IDs;
- deterministic sibling ordering;
- cross-Universe consistency;
- conservative referential rules;
- indexes for foreign-key child lookups;
- schema-level integrity tests;
- production migration from schema v1 to schema v2;
- Windows migration qualification;
- exact-head CI.

## M1.3 — No-AI CRUD service

Status: **COMPLETE + MERGED + NORMALIZED**

Implementation merge:

`49424f1ecafa1be3c4f47b806231b6644e9c73a4`

Delivered:

- Rust application models/DTOs for Universe, Series, Novel, Chapter and Scene;
- hierarchy create/read/update/delete service;
- explicit transactions for compound mutations and reordering;
- deterministic service/Tauri errors;
- thin Tauri command boundary;
- basic React hierarchy screens/forms;
- optional-Series workflow and cross-Universe protection;
- no Ollama dependency for CRUD;
- CRUD, reorder, rollback and integrity tests;
- Windows interactive qualification with Ollama stopped;
- exact-head terminal CI;
- post-merge normalization.

## M1.4 — Text revisions and provenance foundation

Status: **COMPLETE + MERGED + NORMALIZED**

Implementation merge:

`75ab73b176b481f64b0e7f8c510b4ede0c617e31`

Delivered:

- SQLite schema v3 and migration v2 → v3;
- immutable append-only scene text revisions;
- database timestamps and immutable revision IDs;
- current revision pointer with non-destructive restore;
- parent-revision provenance;
- safe transaction behavior and scene-deletion guard;
- Rust/Tauri commands and React revision editor/history;
- frontend and Rust tests, exact-head CI and real Windows qualification with Ollama stopped.

## M1.5 — Backup and restore baseline

Status: **COMPLETE + MERGED + NORMALIZED**

Implementation merge:

`282b325fb6c588a70df08a5128415c8fa0a0f72e`

Delivered:

- application-owned consistent SQLite snapshots using `VACUUM INTO`;
- unique non-overwriting backup names;
- validation of schema owner, migration lineage, foreign keys and integrity;
- restore to a separately verified new SQLite file without overwriting the old database;
- durable active-database marker and preservation of old backups;
- minimal Tauri command boundary and React confirmation flow;
- deterministic frontend/Rust tests and Windows Ollama-off qualification;
- terminal CI on exact evidence SHA `152b40e616f40799abc61f9ce8db142e3b19340b`, run `37720676744` (success).

Detailed evidence:

`docs/qualification/M1_5_BACKUP_RESTORE_BASELINE.md`

## M1 completion

**M1 is COMPLETE + MERGED + NORMALIZED.** M1.1–M1.5 have all been accepted. M2 requires its own detailed, approved plan before implementing new feature code.
