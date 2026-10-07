# Fabulaxiom — Current State

## Repository

- Repository: `LaurentCOLL1/Fabulaxiom`
- Visibility: private
- Default branch: `main`
- M1.1 working branch: `feat/m1-1-sqlite-foundation-20261007`

## Milestone state

### M0 — Environment and architecture qualification

**COMPLETE + MERGED + NORMALIZED**

M0 is closed.

### M1 — Persistence and project foundation

**IN PROGRESS — M1.1 ONLY**

Current subdivision:

**M1.1 — SQLite foundation and migration runner**

Implementation decisions:

- SQLite wrapper: `rusqlite 0.40.2`
- SQLite linkage: `bundled`
- production database location:
  `app_local_data_dir()/database/fabulaxiom.sqlite3`
- explicit `schema_migrations` table
- foreign keys enabled and verified on every connection
- migration application is transactional
- initial schema version: `1`
- initial schema contains metadata only; project hierarchy CRUD remains out of scope

## Reproducibility status

The M0 dependency locks remain authoritative until the new rusqlite dependency is resolved.

M1.1 must not be accepted or merged until:

- `src-tauri/Cargo.lock` includes the selected SQLite dependency;
- locked Rust tests/checks pass;
- the lockfile remains unchanged in terminal CI.

## Windows qualification

Pending for M1.1.

Required observed evidence:

- database status PASS;
- path under the Tauri local app-data directory;
- schema version 1;
- foreign keys ON;
- no Ollama dependency for database operation.

## Known non-blocking environment warnings

- Ollama AMD-driver warning while Vulkan inference works
- potentially incompatible external `ggml-base.dll` in PATH
- two corrupt Ollama manifests

These remain unrelated to M1.1 database acceptance.
