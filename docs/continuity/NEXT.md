# Fabulaxiom — Next Authorized Work

## Current milestone

**M1 — Persistence and project foundation**

## Completed subdivision

**M1.3 — No-AI CRUD service**

Status:

**COMPLETE + MERGED + NORMALIZED**

Implementation PR:

**#11 — feat: implement M1.3 no-AI CRUD service**

Implementation merge:

`49424f1ecafa1be3c4f47b806231b6644e9c73a4`

Qualified implementation SHA:

`6259bd3b4759b683bf4bb7c2c6efdf693ddfebac`

Qualification evidence SHA:

`d9df8151b0c3336e0a12c65a7ba7841cab4e091b`

Terminal exact-head CI:

- run `37684422252`;
- completed/success;
- frontend tests 8/8 PASS;
- frontend build PASS;
- Rust tests 20/20 PASS;
- `cargo check --locked` PASS;
- lockfiles unchanged.

Windows qualification:

- Ollama stopped and API inaccessible;
- full hierarchy CRUD PASS;
- optional-Series workflow PASS;
- reorder/rename/delete-guard flows PASS;
- CRUD independence from Ollama PASS;
- final foreign-key/integrity checks PASS;
- qualification data cleanup PASS;
- final worktree clean.

## Authorized subdivision

**M1.4 — Text revisions and provenance foundation**

M1.4 is the only implementation subdivision currently authorized.

## Required deliverables

1. add scene text revision persistence;
2. use immutable revision identifiers independent of mutable text;
3. record deterministic revision timestamps;
4. provide an explicit current-revision pointer/state for each Scene;
5. add source/provenance primitives suitable for later canonical-fact attribution;
6. preserve the existing Universe → optional Series → Novel → Chapter → Scene CRUD;
7. preserve M1.1/M1.2/M1.3 transaction and referential-integrity guarantees;
8. keep revision/provenance mutations transactional where multiple rows/state changes are involved;
9. expose deterministic application/Tauri errors rather than opaque SQLite failures where an application error is possible;
10. keep M1.4 useful without Ollama and do not make AI a persistence dependency;
11. preserve committed dependency locks unless a new dependency is explicitly justified;
12. add automated tests for revision immutability, current-revision behavior, provenance primitives and rollback;
13. require deterministic exact-head CI;
14. require Windows qualification for the real local database and user-visible revision flow introduced by M1.4;
15. merge the M1.4 PR;
16. complete post-merge continuity normalization before M1.5.

## Boundary

M1.4 is the text-revision and provenance **foundation**.

Do not implement yet:

- application-level backup/restore (M1.5);
- FTS/search milestone work;
- embeddings/vector search;
- narrative entities/canonical-fact engine;
- consistency engine;
- manuscript generation;
- AI-assisted narrative mutation.

Those belong to later subdivisions/milestones.
