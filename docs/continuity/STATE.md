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

**WINDOWS QUALIFIED — FINAL EXACT-HEAD CI + MERGE PENDING**

Branch:

`feat/m1-2-project-hierarchy-schema-20261007`

Qualified implementation SHA:

`3d4b2eaf95e13bfa93580a4295ac20e93a076798`

GitHub CI on that implementation SHA:

- workflow: `Fabulaxiom CI`;
- run: `37644123751`;
- result: `completed/success`;
- Rust tests: 13/13 PASS;
- frontend tests: 4/4 PASS;
- lockfiles unchanged.

Windows production migration qualification:

- exact source HEAD: PASS;
- existing schema v1 detected before launch;
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

M1.2 remains schema-only. CRUD services and project hierarchy UI remain deferred to M1.3.

## M1.2 schema decisions

- all hierarchy tables use SQLite `STRICT`;
- IDs are non-empty `TEXT PRIMARY KEY` values and are protected by immutable-ID triggers;
- Series belongs to exactly one Universe;
- Novel belongs to exactly one Universe and may optionally belong to a Series;
- a composite foreign key prevents a Novel from referencing a Series in a different Universe;
- Chapter belongs to exactly one Novel;
- Scene belongs to exactly one Chapter;
- sibling `sort_order` values are non-negative and unique within their parent scope;
- foreign-key child lookups are indexed where not already covered by a UNIQUE index;
- schema version is 2.

## Reproducibility contract

- no new dependency is introduced by M1.2;
- `package-lock.json` and `src-tauri/Cargo.lock` remain unchanged;
- CI uses `npm ci`;
- Rust CI uses Cargo `--locked`;
- lockfile mutation is rejected in CI.

## Governance rule

M1.2 is not complete until the qualification evidence commit receives final exact-head CI, PR #9 merges, and post-merge normalization completes.

M1.3 is not yet authorized.
