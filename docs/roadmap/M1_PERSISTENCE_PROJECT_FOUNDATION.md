# M1 — Persistence and Project Foundation

## Goal

Establish Fabulaxiom's authoritative local persistence layer before adding narrative-memory intelligence.

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

Status: **IN PROGRESS**

Deliverables:

- migration v2;
- Universe;
- optional Series;
- Novel;
- Chapter;
- Scene;
- immutable stable IDs;
- deterministic sibling ordering;
- cross-universe consistency;
- explicit conservative referential rules;
- indexes for child foreign-key lookups;
- schema-level integrity tests;
- migration from schema v1 to schema v2;
- Windows migration qualification.

Boundary:

M1.2 is schema-only. General CRUD services and project-editing UI remain M1.3 work.

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
