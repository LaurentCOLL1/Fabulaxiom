# M1.1 SQLite Foundation Qualification

## Status

**QUALIFIED — MERGE + POST-MERGE NORMALIZATION PENDING**

## Selected SQLite integration

- Rust crate: `rusqlite 0.40.2`
- SQLite linkage: `bundled`
- database path:
  `app_local_data_dir()/database/fabulaxiom.sqlite3`

SQLite foreign-key enforcement is explicitly enabled and verified per connection.

## Qualified implementation source

Exact implementation SHA tested locally:

`ccbc9c63220c1a8a641595c0ed2d370660cff1ca`

## Dependency lock qualification

Dependency resolution changed only:

`src-tauri/Cargo.lock`

Lock commit:

`88a5f107e31b56af14535e64c8cf96e632f5c878`

That commit contains exactly `src-tauri/Cargo.lock`.

Observed locked dependencies include:

- `rusqlite 0.40.2`
- `libsqlite3-sys 0.38.2`

## Automated Windows results

### Rust

`cargo test --all-targets --locked`

- 6 tests passed
- 0 failed

Qualified database tests:

- fresh file-backed database creation;
- migration idempotence;
- foreign-key enforcement;
- rollback of failed transactional schema work.

`cargo check --locked`: **PASS**

### Frontend

`npm ci`: **PASS**

`npm run test:ci`:

- 2 test files passed
- 4 tests passed
- 0 failed

`npm run build`: **PASS**

## Interactive Windows qualification

### Rust bridge

```text
PASS
Fabulaxiom
M1.1 persistence foundation
React -> Tauri -> Rust operational
```

### SQLite status

```text
PASS
SQLite schema v1 · clés étrangères ON ·
C:\Users\lauco\AppData\Local\com.fabulaxiom.desktop\database\fabulaxiom.sqlite3
```

### Database file

- present
- size: 20480 bytes

### Read-only schema inspection

```json
{"migrations": [[1, "001_create_app_metadata"]], "schema_owner": "fabulaxiom"}
```

## Ollama independence note

Ollama was stopped and its HTTP API confirmed inaccessible before the Tauri launch. During the later interactive session, Ollama became available again, so continuous absence is not claimed.

Database independence is supported by the separate Rust database module and its tests, none of which call the Ollama client.

## Exact-head GitHub CI

Head:

`59923690d08687efd42b452e3e29976131a4be8b`

Workflow:

`Fabulaxiom CI`

Run:

`37636677552`

Result:

**completed / success**

Every deterministic step passed, including:

- `npm ci`;
- frontend tests;
- frontend production build;
- `cargo test --locked`;
- `cargo check --locked`;
- dependency-lock mutation check.

## Acceptance remaining

M1.1 may be marked COMPLETE only after:

1. this qualification evidence is committed;
2. final exact-head CI passes on that commit;
3. PR #5 is merged;
4. post-merge continuity normalization is merged.
