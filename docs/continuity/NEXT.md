# Fabulaxiom — Next Authorized Work

## Current milestone

**M1 — Persistence and project foundation**

## Authorized subdivision

**M1.1 — SQLite foundation and migration runner**

M1.1 is the only implementation subdivision currently authorized.

## Required deliverables

1. select and add the SQLite Rust dependency;
2. establish a deterministic application data-directory strategy;
3. create a database connection service in Rust;
4. enable `PRAGMA foreign_keys = ON` on every connection;
5. add an explicit schema-version / migration table;
6. implement an ordered migration runner;
7. create only the minimal initial metadata schema needed to prove migrations;
8. provide a transaction baseline;
9. test fresh database creation;
10. test repeat/idempotent migration;
11. prove foreign-key enforcement;
12. prove failed transactional work does not leave partial state;
13. prove database creation/migration on the target Windows machine;
14. keep the application usable without Ollama;
15. run deterministic exact-head CI with committed lockfiles.

## Acceptance boundary

M1.1 is complete only when:

- source and dependency locks are committed;
- automated Rust tests pass;
- frontend build remains green;
- exact-head CI is fully successful;
- Windows operator qualification proves the database path and migrations;
- its PR is merged;
- post-merge continuity normalization is complete.

## Not authorized in M1.1

Do not yet implement:

- full Universe/Series/Novel/Chapter/Scene CRUD;
- text revision history UI;
- backup/restore UI;
- FTS search;
- embeddings/vector search;
- manuscript generation;
- automatic canonical-fact extraction.

Those belong to later subdivisions.
