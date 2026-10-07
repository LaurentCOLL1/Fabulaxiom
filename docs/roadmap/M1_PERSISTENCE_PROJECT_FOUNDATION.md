# M1 — Persistence and Project Foundation

## Goal

Establish Fabulaxiom's authoritative local persistence layer before adding narrative-memory intelligence.

## M1.1 — SQLite foundation and migration runner

Status: **AUTHORIZED**

Deliverables:

- SQLite dependency and connection service in Rust;
- deterministic database location under the application data directory;
- schema-version/migration table;
- ordered migration runner;
- `PRAGMA foreign_keys = ON` enforced per connection;
- transaction helper/baseline;
- initial database metadata schema;
- tests for fresh database creation, repeat migration, rollback/integrity behavior;
- CI using committed dependency locks;
- Windows operator qualification.

Acceptance:

- a fresh local database can be created;
- migrations are idempotent;
- foreign-key enforcement is proven;
- failed transactional work does not leave partial state;
- no Ollama dependency is required.

## M1.2 — Project hierarchy schema

Deliverables:

- Universe;
- optional Series;
- Novel;
- Chapter;
- Scene;
- stable immutable IDs;
- ordering fields and referential rules;
- schema-level integrity tests.

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
