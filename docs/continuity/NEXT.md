# Fabulaxiom — Next Authorized Work

## Current milestone

**M1 — Persistence and project foundation**

## Current subdivision

**M1.2 — Project hierarchy schema**

Status:

**IMPLEMENTATION + QUALIFICATION**

## Implementation contract

The M1.2 branch must deliver:

1. schema migration version 2;
2. Universe table;
3. optional Series hierarchy;
4. Novel table;
5. Chapter table;
6. Scene table;
7. stable immutable IDs independent of names;
8. deterministic non-negative sibling ordering;
9. explicit conservative foreign-key update/delete rules;
10. cross-universe Series/Novel protection;
11. indexes required for foreign-key child lookup;
12. valid hierarchy tests;
13. optional-Series tests;
14. cross-universe rejection tests;
15. ordering uniqueness tests;
16. orphan rejection tests;
17. immutable-ID tests;
18. schema v1 → v2 migration test;
19. migration idempotence;
20. exact-head CI;
21. target Windows migration qualification from the existing schema-v1 database.

## Acceptance boundary

M1.2 remains schema-only.

Do not implement:

- hierarchy CRUD services;
- hierarchy editing UI;
- text revisions;
- backup/restore;
- FTS;
- embeddings;
- manuscript generation;
- canonical-fact extraction.

Those remain unauthorized until later subdivisions.

## Next action after deterministic CI

If exact-head CI is fully green, perform the Windows qualification against:

`%LOCALAPPDATA%\com.fabulaxiom.desktop\database\fabulaxiom.sqlite3`

Expected result:

- existing schema v1 migrates transactionally to schema v2;
- migration history contains versions 1 and 2 exactly once;
- foreign keys remain ON;
- `PRAGMA foreign_key_check` returns no rows;
- the five hierarchy tables are present;
- Fabulaxiom reports `SQLite schema v2`.
