# M1.2 — Project Hierarchy Schema Qualification

## Status

**COMPLETE + MERGED + NORMALIZED**

## Scope

M1.2 is schema-only. It introduces no project CRUD service and no hierarchy-editing UI.

## Implementation

Implementation PR:

**#9 — feat: implement M1.2 project hierarchy schema**

Implementation merge:

`91b80e529679d3bc407b5f6ca49e578d86de1d44`

Qualified implementation SHA:

`3d4b2eaf95e13bfa93580a4295ac20e93a076798`

Qualification evidence SHA:

`0da679859c77ef231c6b33e9e91c7264c8d7b5f6`

## Migration

Schema version:

`1 → 2`

Migration:

`002_create_project_hierarchy`

Tables:

- `universes`
- `series`
- `novels`
- `chapters`
- `scenes`

## Integrity design

- SQLite `STRICT` tables;
- non-empty TEXT primary IDs;
- immutable-ID triggers;
- non-negative sibling `sort_order`;
- unique ordering within parent scope;
- Universe → Series foreign key;
- Universe → Novel foreign key;
- optional Series → Novel composite foreign key;
- Novel → Chapter foreign key;
- Chapter → Scene foreign key;
- `ON UPDATE RESTRICT`;
- `ON DELETE RESTRICT`;
- child-key indexes where UNIQUE constraints do not already provide an efficient prefix.

## GitHub qualification

Implementation CI:

- run `37644123751`;
- completed/success;
- 13 Rust tests passed;
- frontend tests/build passed;
- Cargo locked checks passed;
- lockfiles unchanged.

Terminal evidence-commit CI:

- head `0da679859c77ef231c6b33e9e91c7264c8d7b5f6`;
- run `37646868694`;
- completed/success;
- `cargo test --locked`: PASS;
- `cargo check --locked`: PASS;
- dependency-lock mutation check: PASS.

## Windows production migration qualification

Production database before migration:

`C:\Users\lauco\AppData\Local\com.fabulaxiom.desktop\database\fabulaxiom.sqlite3`

Observed pre-migration:

- schema version 1;
- only migration `001_create_app_metadata`;
- hierarchy tables absent.

Pre-migration backup:

`C:\Users\lauco\AppData\Local\com.fabulaxiom.desktop\database\fabulaxiom.before-m1-2-v1.20261007-174440.sqlite3`

Observed post-migration:

- migration 1 present exactly once;
- migration 2 present exactly once;
- hierarchy tables 5/5 present;
- STRICT 5/5;
- immutable-ID triggers 5/5;
- foreign keys ON;
- `PRAGMA foreign_key_check`: empty;
- `PRAGMA integrity_check`: `ok`;
- Rust bridge: PASS;
- database status: PASS;
- Ollama local status: PASS;
- final HEAD unchanged during qualification;
- worktree clean.

## Dependency contract

M1.2 introduced no dependency.

Confirmed unchanged:

- `package-lock.json`;
- `src-tauri/Cargo.lock`.

## Conclusion

M1.2 satisfied implementation, deterministic CI, real Windows v1→v2 migration, integrity, merge, and normalization requirements.

M1.3 may begin only from live normalized `main`.
