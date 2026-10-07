# Fabulaxiom — Next Authorized Work

## Current milestone

**M1 — Persistence and project foundation**

Status: **AUTHORIZED**

## First authorized subdivision

**M1.1 — SQLite foundation and migration runner**

Required deliverables:

1. add the SQLite Rust dependency selected for the project;
2. establish the application data-directory strategy;
3. create a migration runner with an explicit schema version table;
4. enable foreign keys on every database connection;
5. create a minimal initial schema foundation without yet implementing full project CRUD;
6. add transaction/integrity tests;
7. prove database creation/migration on Windows;
8. keep the UI functional without Ollama;
9. run deterministic exact-head CI.

## Not authorized in M1.1

Do not yet implement:

- full Universe/Series/Novel/Chapter/Scene CRUD;
- text revision history UI;
- backup/restore UI;
- FTS search;
- embeddings/vector search;
- manuscript generation.

Those belong to later M1 subdivisions.
