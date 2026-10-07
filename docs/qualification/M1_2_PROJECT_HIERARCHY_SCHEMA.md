# M1.2 — Project Hierarchy Schema Qualification

## Status

**IMPLEMENTED — EXACT-HEAD CI PENDING**

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

## Automated Rust acceptance

Required tests:

- fresh database reaches schema v2;
- migrations are idempotent;
- schema v1 migrates to v2;
- valid hierarchy accepts both standalone and Series novels;
- cross-Universe Series reference is rejected;
- sibling ordering collisions are rejected;
- orphan references are rejected;
- all hierarchy IDs are immutable;
- `PRAGMA foreign_key_check` reports no violations;
- existing foreign-key and transaction rollback tests remain green.

## Dependency contract

M1.2 adds no dependency.

Expected unchanged files:

- `package-lock.json`
- `src-tauri/Cargo.lock`

## Windows acceptance still required

After exact-head CI passes:

1. migrate the existing target Windows database from v1 to v2;
2. verify migration rows 1 and 2 exactly once;
3. verify all five hierarchy tables;
4. verify foreign keys ON;
5. verify `PRAGMA foreign_key_check` is empty;
6. verify Fabulaxiom displays schema v2;
7. record the exact qualified SHA.
