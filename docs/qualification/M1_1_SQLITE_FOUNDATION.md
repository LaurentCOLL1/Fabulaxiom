# M1.1 SQLite Foundation Qualification

## Status

**IMPLEMENTATION PREPARED — WINDOWS QUALIFICATION PENDING**

## Selected SQLite integration

- Rust crate: `rusqlite 0.40.2`
- SQLite linkage: `bundled`
- rationale: Fabulaxiom controls its own application database and must package reliably on Windows without depending on a system SQLite installation.

## Database location strategy

The production database resolves through Tauri:

`app_local_data_dir()/database/fabulaxiom.sqlite3`

The application installation directory and Git repository are never used for production database storage.

## Connection contract

Every connection must:

- enable `PRAGMA foreign_keys = ON`;
- verify that foreign-key enforcement is actually enabled;
- configure a finite busy timeout.

## Migration contract

Fabulaxiom maintains an explicit:

`schema_migrations(version, name, applied_at_utc)`

table.

Migrations:

- are ordered and versioned;
- run inside transactions;
- record their version only after migration SQL succeeds;
- are safe to run repeatedly;
- reject schema versions unknown to the current application.

Initial schema version:

`1`

Initial metadata table:

`app_metadata`

No Universe/Series/Novel/Chapter/Scene schema is authorized in M1.1.

## Automated acceptance tests prepared

- fresh file-backed database creation;
- initial migration and metadata record;
- migration idempotence;
- foreign-key enforcement;
- rollback of failed transactional schema work.

## Windows operator acceptance pending

The target Windows machine must still prove:

- dependency-lock update is exact;
- Rust tests pass;
- frontend tests/build stay green;
- Fabulaxiom launches;
- the database status control reports PASS;
- the reported path is under the Tauri local app-data directory;
- schema version is `1`;
- foreign keys are ON;
- Fabulaxiom still launches and the database works when Ollama is not required.
