# Fabulaxiom — Next Authorized Work

## Current milestone

**M1 — Persistence and project foundation**

## Completed subdivision

**M1.2 — Project hierarchy schema**

Status:

**COMPLETE + MERGED + NORMALIZED**

Implementation merge:

`91b80e529679d3bc407b5f6ca49e578d86de1d44`

Terminal exact-head CI:

- run `37646868694`;
- completed/success;
- 13 Rust tests PASS;
- frontend tests/build PASS;
- lockfiles unchanged.

Windows migration qualification:

- production schema v1 → v2 PASS;
- hierarchy tables 5/5 PASS;
- STRICT 5/5 PASS;
- immutable-ID triggers 5/5 PASS;
- foreign keys/integrity PASS.

## Current subdivision

**M1.3 — No-AI CRUD service**

Status: **IN PROGRESS**

Branch:

`feat/m1-3-no-ai-crud-service-20261007`

Base `main` at subdivision start:

`4f90a66a30c72446bfab3dc20429429b6e4217b7`

M1.3 remains the only implementation subdivision currently authorized.

## Required deliverables

1. define Rust application-layer models/DTOs for Universe, Series, Novel, Chapter and Scene;
2. implement create/read/update/delete services over the schema-v2 tables;
3. keep immutable IDs immutable;
4. preserve deterministic sibling ordering;
5. enforce Universe/Series/Novel ownership invariants through the existing schema and service validation;
6. wrap multi-step mutations in explicit transactions;
7. return deterministic typed/service errors suitable for the Tauri boundary;
8. expose the minimum Tauri commands required by the CRUD screens;
9. add basic React hierarchy screens/forms usable without Ollama;
10. allow Series to remain optional for a Novel;
11. test create/read/update/delete for every hierarchy level;
12. test invalid/orphan/cross-Universe mutations;
13. test transaction rollback for compound mutations;
14. test application behavior with Ollama unavailable;
15. preserve all M1.1/M1.2 database tests;
16. preserve committed dependency locks unless a new dependency is explicitly justified;
17. require deterministic exact-head CI;
18. require Windows interactive CRUD qualification;
19. merge the M1.3 PR;
20. complete post-merge continuity normalization before M1.4.

## Boundary

M1.3 is a no-AI CRUD milestone.

Do not implement yet:

- text revision history/provenance;
- backup/restore;
- FTS;
- embeddings/vector search;
- manuscript generation;
- canonical-fact extraction;
- consistency engine.

Those belong to later subdivisions/milestones.
