# Fabulaxiom — Current State

## Repository

- Repository: `LaurentCOLL1/Fabulaxiom`
- Visibility: private
- Default branch: `main`

## Milestone state

### M0 — Environment and architecture qualification

**COMPLETE + MERGED + NORMALIZED**

### M1 — Persistence and project foundation

**IN PROGRESS**

#### M1.1 — SQLite foundation and migration runner

**COMPLETE + MERGED + NORMALIZED**

Final normalization merge:

`d99da744fc04303c0c094a8aa6a2daab9983136f`

#### M1.2 — Project hierarchy schema

**COMPLETE + MERGED + NORMALIZED**

Implementation PR:

**#9 — feat: implement M1.2 project hierarchy schema**

Implementation merge:

`91b80e529679d3bc407b5f6ca49e578d86de1d44`

Qualified implementation SHA:

`3d4b2eaf95e13bfa93580a4295ac20e93a076798`

Qualification evidence commit:

`0da679859c77ef231c6b33e9e91c7264c8d7b5f6`

Deterministic exact-head CI:

- workflow: `Fabulaxiom CI`;
- terminal run: `37646868694`;
- result: `completed/success`;
- frontend tests/build: PASS;
- Rust tests: 13/13 PASS;
- `cargo check --locked`: PASS;
- dependency lockfiles unchanged.

Windows production migration qualification:

- schema-v1 production database detected;
- pre-migration SQLite backup created;
- migration v1 → v2: PASS;
- migrations 1 and 2 present exactly once;
- hierarchy tables 5/5 present;
- SQLite STRICT 5/5;
- immutable-ID triggers 5/5;
- foreign keys ON;
- `PRAGMA foreign_key_check`: empty;
- `PRAGMA integrity_check`: `ok`;
- Rust bridge: PASS;
- database status: PASS;
- Ollama local status: PASS;
- worktree clean.

Detailed evidence:

`docs/qualification/M1_2_PROJECT_HIERARCHY_SCHEMA.md`

Delivered schema:

- Universe;
- optional Series;
- Novel;
- Chapter;
- Scene;
- immutable non-name IDs;
- deterministic sibling ordering;
- cross-universe Series/Novel integrity;
- conservative `RESTRICT` update/delete behavior;
- child-key indexes;
- migration v2 from the M1.1 schema.

#### M1.3 — No-AI CRUD service

**WINDOWS QUALIFIED — FINAL EXACT-HEAD CI + MERGE PENDING**

Implementation PR:

**#11 — feat: implement M1.3 no-AI CRUD service**

Branch:

`feat/m1-3-no-ai-crud-service-20261007`

Base `main` at subdivision start:

`4f90a66a30c72446bfab3dc20429429b6e4217b7`

Qualified implementation SHA:

`6259bd3b4759b683bf4bb7c2c6efdf693ddfebac`

Deterministic exact-head CI before Windows qualification:

- workflow: `Fabulaxiom CI`;
- run: `37665443163`;
- result: `completed/success`;
- frontend tests: 8/8 PASS;
- frontend build: PASS;
- Rust tests: 20/20 PASS;
- `cargo check --locked`: PASS;
- dependency lockfiles unchanged.

Windows no-AI CRUD qualification:

- exact source HEAD: PASS;
- live `origin/main` exact: PASS;
- live feature branch exact: PASS;
- worktree clean before and after qualification;
- Ollama process absent;
- Ollama API inaccessible at `127.0.0.1:11434`;
- local frontend tests/build: PASS;
- local Rust tests/check: PASS;
- Rust bridge: PASS;
- SQLite schema v2 / foreign keys ON: PASS;
- Ollama status: expected `INDISPONIBLE`;
- Universe / Series / Novel / Chapter / Scene create-read-update-delete: PASS;
- optional Series workflow: PASS;
- deterministic sibling reorder: PASS;
- same-Universe Novel Series changes: PASS;
- cross-Universe Series not offered/rejected by the qualified flow: PASS;
- parent deletion with children rejected with `has_children`: PASS;
- CRUD remained operational while Ollama stayed stopped;
- all `QUAL-M13-*` qualification data removed;
- `PRAGMA foreign_key_check`: empty;
- `PRAGMA integrity_check`: `ok`;
- Ollama remained stopped through final verification.

Detailed evidence:

`docs/qualification/M1_3_NO_AI_CRUD_SERVICE.md`

M1.4+ remain unauthorized until this qualification evidence receives terminal exact-head CI, PR #11 merges, and post-merge normalization completes.

## Reproducibility contract

- `package-lock.json` committed;
- `src-tauri/Cargo.lock` committed;
- CI uses `npm ci`;
- Rust CI uses Cargo `--locked`;
- dependency-lock mutation is rejected in CI.

## Governance rule

Every subdivision must:

- begin from freshly fetched live `main`;
- use a dedicated branch and pull request;
- preserve deterministic dependency locks;
- pass exact-head CI;
- receive Windows operator qualification when local behavior is part of acceptance;
- be merged and normalized before a dependent subdivision begins.
