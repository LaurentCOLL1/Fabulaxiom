# Fabulaxiom — Next Authorized Work

## Current milestone

**M1 — Persistence and project foundation**

## Completed subdivision

**M1.1 — SQLite foundation and migration runner**

Status:

**COMPLETE + MERGED + NORMALIZED**

Implementation merge:

`d212de93cc869bfbe0e047a12594d23e1732d5cb`

Normalization merge:

`807949c3e23812416aa1282541c7c3ecbf6e693f`

## Authorized subdivision

**M1.2 — Project hierarchy schema**

M1.2 is the only implementation subdivision currently authorized.

## Required deliverables

1. add ordered migration version 2 for the hierarchy schema;
2. add Universe;
3. add optional Series;
4. add Novel;
5. add Chapter;
6. add Scene;
7. use stable immutable identifiers independent of names;
8. define deterministic ordering fields for Series/Novel/Chapter/Scene where applicable;
9. define explicit foreign-key relationships and conservative deletion/update rules;
10. add CHECK/UNIQUE constraints needed for structural integrity;
11. add indexes for foreign-key child columns used by integrity checks and future access patterns;
12. test valid hierarchy creation;
13. test novels with and without a Series;
14. test that a Novel cannot reference a Series from another Universe;
15. test deterministic ordering uniqueness;
16. test rejected orphaned references;
17. test migration from M1.1 schema v1 to schema v2;
18. test migration idempotence;
19. keep M1.2 schema-only: no CRUD UI/service yet;
20. require deterministic exact-head CI and Windows database migration qualification.

## Acceptance boundary

M1.2 is complete only when:

- schema migration is versioned;
- automated integrity tests pass;
- all M1.1 tests remain green;
- frontend build remains green;
- dependency locks stay unchanged unless an explicitly justified dependency is added;
- exact-head CI is fully successful;
- the target Windows database migrates cleanly from schema v1 to schema v2;
- its PR is merged;
- post-merge continuity normalization is complete.

## Not authorized in M1.2

Do not yet implement:

- full create/read/update/delete services;
- project hierarchy forms/screens;
- text revision history;
- backup/restore;
- FTS search;
- embeddings/vector search;
- manuscript generation;
- canonical-fact extraction.

Those belong to later M1/M2 subdivisions.
