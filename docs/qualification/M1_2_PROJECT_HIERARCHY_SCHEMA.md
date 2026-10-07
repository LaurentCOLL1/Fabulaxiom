# M1.2 — Project Hierarchy Schema Qualification

## Status

**WINDOWS QUALIFIED — FINAL EXACT-HEAD CI REQUIRED**

## Scope

M1.2 is schema-only. It introduces no project CRUD service and no hierarchy-editing UI.

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

The composite Series/Novel key guarantees that a novel with a non-null `series_id` can only reference a Series belonging to the same `universe_id`.

## Exact implementation SHA qualified on Windows

`3d4b2eaf95e13bfa93580a4295ac20e93a076798`

## GitHub exact-head CI

Workflow:

`Fabulaxiom CI`

Run:

`37644123751`

Result:

**completed / success**

Successful deterministic steps:

- checkout;
- Node setup;
- Rust setup;
- `npm ci`;
- frontend tests;
- frontend production build;
- `cargo test --locked`;
- `cargo check --locked`;
- dependency-lock mutation check.

Rust result:

- 13 tests passed;
- 0 failed.

M1.2 coverage includes:

- schema v1 → v2 migration;
- migration idempotence;
- standalone and Series novels;
- cross-Universe Series rejection;
- deterministic sibling ordering;
- orphan rejection;
- immutable hierarchy IDs;
- `PRAGMA foreign_key_check` with no violations;
- existing foreign-key and rollback tests.

## Windows qualification

The target Windows clone was revalidated at the exact implementation SHA.

Observed:

- repository clean before qualification;
- remote `main` exact:
  `d99da744fc04303c0c094a8aa6a2daab9983136f`;
- branch HEAD exact:
  `3d4b2eaf95e13bfa93580a4295ac20e93a076798`;
- frontend tests: 4/4 PASS;
- frontend build: PASS;
- Rust tests: 13/13 PASS;
- `cargo check --locked`: PASS;
- dependency lockfiles unchanged;
- worktree clean.

### Pre-migration state

Production database:

`C:\Users\lauco\AppData\Local\com.fabulaxiom.desktop\database\fabulaxiom.sqlite3`

Before migration:

- schema version 1 only;
- migration `001_create_app_metadata`;
- tables: `app_metadata`, `schema_migrations`.

A SQLite backup was created before migration:

`C:\Users\lauco\AppData\Local\com.fabulaxiom.desktop\database\fabulaxiom.before-m1-2-v1.20261007-174440.sqlite3`

### Interactive application qualification

Rust bridge:

**PASS**

Database status:

**PASS**

Ollama local status:

**PASS**

The database-status action migrated the existing production database transactionally from schema v1 to schema v2.

### Post-migration evidence

Migration history:

1. `001_create_app_metadata`
2. `002_create_project_hierarchy`

Hierarchy tables:

- `universes`: present;
- `series`: present;
- `novels`: present;
- `chapters`: present;
- `scenes`: present.

All five hierarchy tables report SQLite `strict=1`.

Immutable-ID triggers:

- `universes_id_immutable`;
- `series_id_immutable`;
- `novels_id_immutable`;
- `chapters_id_immutable`;
- `scenes_id_immutable`.

Integrity:

- foreign keys: ON;
- `PRAGMA foreign_key_check`: empty;
- `PRAGMA integrity_check`: `ok`.

Final repository state:

- HEAD unchanged at the qualified SHA;
- worktree clean.

## Dependency contract

M1.2 adds no dependency.

Confirmed unchanged:

- `package-lock.json`;
- `src-tauri/Cargo.lock`.

## Acceptance remaining

M1.2 may not be marked COMPLETE until:

1. this Windows qualification evidence is committed;
2. final exact-head CI passes on that new documentation SHA;
3. PR #9 is merged;
4. live `main` is re-fetched;
5. post-merge continuity normalization is merged.

M1.3 remains unauthorized until all five gates are complete.
