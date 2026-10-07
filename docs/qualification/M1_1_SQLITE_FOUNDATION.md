# M1.1 SQLite Foundation Qualification

## Status

**WINDOWS QUALIFIED — EXACT-HEAD CI PENDING**

## Selected SQLite integration

- Rust crate: `rusqlite 0.40.2`
- SQLite linkage: `bundled`
- database path:
  `app_local_data_dir()/database/fabulaxiom.sqlite3`

SQLite foreign-key enforcement is explicitly enabled and verified per connection. SQLite documents foreign-key enforcement as a per-connection setting, so Fabulaxiom does not rely on a default. 

## Qualified implementation source

Exact implementation SHA tested before qualification documentation:

`ccbc9c63220c1a8a641595c0ed2d370660cff1ca`

## Dependency lock qualification

Dependency resolution changed only:

`src-tauri/Cargo.lock`

Observed additions include:

- `rusqlite 0.40.2`
- `libsqlite3-sys 0.38.2`
- transitive SQLite support crates

The lockfile was committed separately in:

`88a5f107e31b56af14535e64c8cf96e632f5c878`

That commit contains exactly `src-tauri/Cargo.lock`.

## Automated Windows results

### Rust

`cargo test --all-targets --locked`

Result:

- 6 tests passed
- 0 failed

Qualified database tests:

- fresh file-backed database creation;
- migration idempotence;
- foreign-key enforcement;
- failed transactional schema work rolls back.

Existing M0 Ollama tests also remained green.

`cargo check --locked`: **PASS**

### Frontend

`npm ci`: **PASS**

`npm run test:ci`:

- 2 test files passed
- 4 tests passed
- 0 failures

`npm run build`: **PASS**

## Interactive Windows qualification

### Rust bridge

Observed:

```text
PASS
Fabulaxiom
M1.1 persistence foundation
React -> Tauri -> Rust operational
```

### SQLite status

Observed:

```text
PASS
SQLite schema v1 · clés étrangères ON ·
C:\Users\lauco\AppData\Local\com.fabulaxiom.desktop\database\fabulaxiom.sqlite3
```

### Database file

Observed:

- file present
- size: 20480 bytes

### Read-only schema inspection

Observed:

```json
{"migrations": [[1, "001_create_app_metadata"]], "schema_owner": "fabulaxiom"}
```

## Ollama independence evidence

Before the interactive Tauri launch, Ollama processes were stopped and:

`http://127.0.0.1:11434/api/version`

was confirmed inaccessible.

Fabulaxiom then launched and the SQLite qualification succeeded.

During the interactive session, the Ollama status control later reported Ollama 0.40.0 available, meaning Ollama had restarted independently. Therefore the UI run is not treated as evidence that Ollama remained absent for the entire session.

Database independence is additionally established structurally and through the Rust test suite:

- the database service does not call the Ollama client;
- file-backed creation/migration tests run without Ollama;
- foreign-key and transaction tests run without Ollama.

## Acceptance remaining

M1.1 may not be marked complete until:

1. the qualification evidence is committed;
2. its PR is open;
3. deterministic exact-head CI passes with committed lockfiles unchanged;
4. the PR is merged;
5. post-merge continuity normalization is complete.
