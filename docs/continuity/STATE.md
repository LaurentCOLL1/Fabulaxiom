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

## M1.1 Windows qualification

Qualified source before qualification-doc update:

`ccbc9c63220c1a8a641595c0ed2d370660cff1ca`

Observed on the target Windows machine:

- Git branch/upstream repair: PASS
- exact source HEAD: PASS
- `rusqlite 0.40.2` with `bundled`: PASS
- only `src-tauri/Cargo.lock` changed during dependency resolution
- Rust tests: 6/6 PASS
- `cargo check --locked`: PASS
- `npm ci`: PASS
- frontend tests: 4/4 PASS
- production frontend build: PASS
- Tauri desktop launch: PASS
- React → Tauri → Rust bridge: PASS
- database status control: PASS
- database path:
  `C:\Users\lauco\AppData\Local\com.fabulaxiom.desktop\database\fabulaxiom.sqlite3`
- SQLite file present: 20480 bytes
- schema migration evidence:
  `[[1, "001_create_app_metadata"]]`
- `schema_owner`: `fabulaxiom`
- schema version shown in application: `1`
- foreign keys shown in application: ON

Ollama was explicitly stopped and its HTTP API was confirmed inaccessible before Fabulaxiom was launched. Ollama later became available again during the interactive session, so the UI observation alone does not prove continuous Ollama absence. Independence is instead supported by the Rust database test suite and the separate database command path, neither of which invokes the Ollama client.

## Reproducibility status

The SQLite dependency lock update has now been versioned.

Lock commit:

`88a5f107e31b56af14535e64c8cf96e632f5c878`

The commit contains exactly:

`src-tauri/Cargo.lock`

The lock contains:

- `rusqlite 0.40.2`
- `libsqlite3-sys 0.38.2`

M1.1 now requires terminal exact-head CI with `--locked` and unchanged lockfiles before merge.

## Windows Git configuration

The local clone's origin refspec was repaired from the original single-branch M0 mapping to the standard all-branches mapping:

`+refs/heads/*:refs/remotes/origin/*`

This is local Git configuration only and does not alter repository source.

## Known non-blocking environment warnings

- Ollama AMD-driver warning while Vulkan inference works
- potentially incompatible external `ggml-base.dll` in PATH
- two corrupt Ollama manifests

These remain unrelated to M1.1 database acceptance.
