# Fabulaxiom — Next Authorized Work

## Current milestone

**M1 — Persistence and project foundation**

## M1.1

**COMPLETE + MERGED**

Merge commit:

`d212de93cc869bfbe0e047a12594d23e1732d5cb`

This normalization PR must pass exact-head CI and merge before implementation of M1.2 starts.

## Next subdivision

**M1.2 — Project hierarchy schema**

M1.2 becomes the only authorized implementation subdivision after this normalization is merged.

## Required deliverables

1. add an ordered SQLite migration for the project hierarchy;
2. add Universe;
3. add optional Series;
4. add Novel;
5. add Chapter;
6. add Scene;
7. use stable immutable identifiers independent of names;
8. define deterministic ordering fields for Series/Novel/Chapter/Scene where applicable;
9. define foreign-key relationships and deletion/update rules;
10. add CHECK/UNIQUE constraints needed for structural integrity;
11. test valid hierarchy creation;
12. test optional Series behavior;
13. test ordering constraints;
14. test rejected orphaned references;
15. test migration idempotence from M1.1 schema v1 to the new version;
16. keep M1.2 schema-only: no CRUD UI/service yet;
17. require deterministic exact-head CI and Windows database migration qualification.

## Acceptance boundary

M1.2 is complete only when:

- schema migration is versioned;
- automated integrity tests pass;
- existing M1.1 tests remain green;
- frontend build remains green;
- dependency locks stay unchanged unless an explicitly justified dependency is added;
- exact-head CI is fully successful;
- the target Windows database migrates cleanly from schema v1;
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
