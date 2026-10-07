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

Status:

**QUALIFIED — MERGE + POST-MERGE NORMALIZATION PENDING**

## M1.1 implementation

- SQLite wrapper: `rusqlite 0.40.2`
- SQLite linkage: `bundled`
- production database:
  `app_local_data_dir()/database/fabulaxiom.sqlite3`
- explicit `schema_migrations` table
- foreign keys enabled and verified on every connection
- migration application is transactional
- initial schema version: `1`
- initial metadata table only; project hierarchy CRUD remains out of scope

## Windows qualification

Qualified implementation source:

`ccbc9c63220c1a8a641595c0ed2d370660cff1ca`

Observed:

- Rust tests: 6/6 PASS
- `cargo check --locked`: PASS
- `npm ci`: PASS
- frontend tests: 4/4 PASS
- frontend production build: PASS
- Tauri launch: PASS
- Rust bridge: PASS
- database status UI: PASS
- database path:
  `C:\Users\lauco\AppData\Local\com.fabulaxiom.desktop\database\fabulaxiom.sqlite3`
- schema version: `1`
- foreign keys: ON
- migration: `001_create_app_metadata`
- `schema_owner`: `fabulaxiom`

## Reproducibility

SQLite dependency-lock commit:

`88a5f107e31b56af14535e64c8cf96e632f5c878`

That commit contains exactly:

`src-tauri/Cargo.lock`

## Exact-head CI

Qualification head:

`59923690d08687efd42b452e3e29976131a4be8b`

Workflow:

`Fabulaxiom CI`

Run:

`37636677552`

Result:

**completed / success**

Successful checks:

- checkout
- Node setup
- Rust setup
- `npm ci`
- frontend tests
- frontend production build
- `cargo test --locked`
- `cargo check --locked`
- dependency-lock mutation check

## Remaining M1.1 acceptance gates

M1.1 is not yet marked COMPLETE because governance still requires:

1. qualification evidence commit;
2. final exact-head CI on that evidence commit;
3. merge of PR #5 with expected-head protection;
4. re-fetch live `main`;
5. post-merge continuity normalization.

Only after those gates may M1.2 be authorized.

## Windows Git configuration

The local clone's `origin` refspec was repaired to:

`+refs/heads/*:refs/remotes/origin/*`

This is local Git configuration only and does not alter repository source.

## Known non-blocking environment warnings

- Ollama AMD-driver warning while Vulkan inference works
- potentially incompatible external `ggml-base.dll` in PATH
- two corrupt Ollama manifests
