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

#### M1.3 — No-AI CRUD service

**COMPLETE + MERGED + NORMALIZED**

Implementation PR:

**#11 — feat: implement M1.3 no-AI CRUD service**

Implementation merge:

`49424f1ecafa1be3c4f47b806231b6644e9c73a4`

Qualified implementation SHA:

`6259bd3b4759b683bf4bb7c2c6efdf693ddfebac`

Qualification evidence commit:

`d9df8151b0c3336e0a12c65a7ba7841cab4e091b`

Terminal exact-head CI:

- workflow: `Fabulaxiom CI`;
- run: `37684422252`;
- result: `completed/success`;
- frontend tests: 8/8 PASS;
- frontend build: PASS;
- Rust tests: 20/20 PASS;
- `cargo check --locked`: PASS;
- dependency lockfiles unchanged.

Windows no-AI CRUD qualification:

- exact implementation source and clean worktree: PASS;
- Ollama process absent and loopback API inaccessible;
- local frontend tests/build: PASS;
- local Rust tests/check: PASS;
- Rust bridge: PASS;
- SQLite schema v2 / foreign keys ON: PASS;
- Ollama status expected unavailable;
- full Universe / Series / Novel / Chapter / Scene CRUD: PASS;
- optional-Series workflow: PASS;
- deterministic reorder: PASS;
- rename at every hierarchy level: PASS;
- cross-Universe Series protection: PASS;
- parent deletion guards with `has_children`: PASS;
- CRUD remained operational with Ollama stopped;
- qualification data cleanup: PASS;
- `PRAGMA foreign_key_check`: empty;
- `PRAGMA integrity_check`: `ok`;
- final worktree clean;
- Ollama remained stopped.

Detailed evidence:

`docs/qualification/M1_3_NO_AI_CRUD_SERVICE.md`

Delivered M1.3 foundation:

- Rust application models/DTOs separate from SQLite rows;
- CRUD service for all five hierarchy levels;
- explicit transaction boundaries for compound mutations;
- deterministic application/Tauri error payloads;
- thin Tauri commands;
- React hierarchy CRUD workspace;
- no Ollama dependency for CRUD;
- preserved M1.1/M1.2 persistence guarantees.

#### M1.4 — Text revisions and provenance foundation

**AUTHORIZED**

M1.4 is now the only implementation subdivision authorized.

Scope:

- scene text revisions;
- immutable revision IDs;
- timestamps;
- current revision pointer;
- source/provenance primitives for later canonical facts;
- preserve the existing no-AI hierarchy CRUD and persistence guarantees.

M1.5+ remain unauthorized until M1.4 is complete, qualified, merged, and normalized.

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
