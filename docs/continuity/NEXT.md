# Fabulaxiom — Next Authorized Work

## Current milestone

**M1 — Persistence and project foundation**

## Completed subdivision

**M1.1 — SQLite foundation and migration runner**

Status:

**COMPLETE + MERGED + NORMALIZED**

## Authorized subdivision

**M1.2 — Project hierarchy schema**

M1.2 is the only implementation subdivision currently authorized.

## Required deliverables

1. add an ordered SQLite migration from schema v1 to the hierarchy schema;
2. add Universe;
3. add optional Series;
4. add Novel;
5. add Chapter;
6. add Scene;
7. use stable immutable identifiers independent of names;
8. define deterministic ordering fields where applicable;
9. define foreign-key relationships and deletion/update rules;
10. add CHECK/UNIQUE constraints required for structural integrity;
11. test valid hierarchy creation;
12. test optional Series behavior;
13. test ordering constraints;
14. test rejection of orphaned references;
15. test identifier immutability;
16. test migration idempotence from M1.1 schema v1;
17. keep M1.2 schema-only: no CRUD application service/UI;
18. require deterministic exact-head CI;
19. qualify migration of the target Windows database from schema v1.

## Acceptance boundary

M1.2 is complete only when:

- migration v2 is committed;
- schema-level integrity tests pass;
- existing M1.1 tests remain green;
- frontend build remains green;
- dependency lockfiles remain unchanged;
- exact-head CI is fully successful;
- the target Windows database migrates cleanly from schema v1 to v2;
- its PR is merged;
- post-merge continuity normalization is complete.

## Not authorized in M1.2

Do not yet implement:

- general create/read/update/delete services;
- project hierarchy forms/screens;
- text revision history;
- backup/restore;
- FTS search;
- embeddings/vector search;
- manuscript generation;
- canonical-fact extraction.

Those belong to later subdivisions.
