# Fabulaxiom — Next Authorized Work

## Current subdivision

**M1.1 — SQLite foundation and migration runner**

Status: **WINDOWS QUALIFIED — PR + EXACT-HEAD CI REQUIRED**

## Qualified

- exact M1.1 implementation fetched and tested on Windows
- `rusqlite 0.40.2` bundled SQLite linkage
- `Cargo.lock` updated and committed
- Rust tests: 6/6 PASS
- Cargo check `--locked`: PASS
- frontend tests: 4/4 PASS
- frontend build: PASS
- Tauri launch: PASS
- database status UI: PASS
- database path under Tauri local app-data directory
- schema version: 1
- foreign keys: ON
- migration record: `001_create_app_metadata`
- schema owner: `fabulaxiom`

## Immediate sequence

1. record the Windows qualification on the M1.1 branch;
2. open the M1.1 pull request;
3. run deterministic exact-head CI;
4. require:
   - `npm ci`;
   - frontend tests/build;
   - `cargo test --locked`;
   - `cargo check --locked`;
   - no dependency-lock mutation;
5. correct any exact-head failure without bypass;
6. when CI is fully green, mark M1.1 complete;
7. merge with expected-head protection;
8. re-fetch live `main`;
9. perform post-merge continuity normalization;
10. only then authorize M1.2.

## Not authorized

Do not yet implement:

- full Universe/Series/Novel/Chapter/Scene CRUD;
- text revision history UI;
- backup/restore UI;
- FTS search;
- embeddings/vector search;
- manuscript generation;
- automatic canonical-fact extraction.
