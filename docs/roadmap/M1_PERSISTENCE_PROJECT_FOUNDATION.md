# M1 — Persistence and Project Foundation

## Goal

Establish Fabulaxiom's authoritative local persistence layer before adding narrative-memory intelligence.

## M1.1 — SQLite foundation and migration runner

Status: **COMPLETE + MERGED**

Merge commit:

`d212de93cc869bfbe0e047a12594d23e1732d5cb`

Delivered:

- bundled SQLite through `rusqlite 0.40.2`;
- deterministic application-local database path;
- schema migration table;
- ordered transactional migration runner;
- `PRAGMA foreign_keys = ON` enforced and verified per connection;
- transaction helper/baseline;
- initial metadata schema;
- fresh database, idempotence, foreign-key and rollback tests;
- deterministic dependency locks;
- Windows operator qualification;
- exact-head CI.

## M1.2 — Project hierarchy schema

Status: **AUTHORIZED AFTER M1.1 NORMALIZATION**

Deliverables:

- Universe;
- optional Series;
- Novel;
- Chapter;
- Scene;
- stable immutable IDs;
- ordering fields and referential rules;
- schema-level integrity tests;
- migration from M1.1 schema version 1;
- Windows migration qualification.

Boundary:

M1.2 is schema-only. No general CRUD application service or project-editing UI is authorized yet.

## M1.3 — No-AI CRUD service

Deliverables:

- Rust application services for create/read/update/delete;
- explicit transactions;
- basic React screens/forms;
- no AI requirement;
- integrity/error handling.

## M1.4 — Text revisions and provenance foundation

Deliverables:

- scene text revisions;
- immutable revision IDs;
- timestamps;
- current revision pointer;
- source/provenance primitives for later canonical facts.

## M1.5 — Backup and restore baseline

Deliverables:

- application-level backup;
- restore into a controlled location;
- integrity verification;
- tested recovery path.

## M1 completion

M1 becomes COMPLETE only after all subdivisions are merged and normalized.
