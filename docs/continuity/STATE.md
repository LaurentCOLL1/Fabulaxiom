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

**IMPLEMENTATION IN PROGRESS**

Branch:

`feat/m1-2-project-hierarchy-schema-20261007`

Authorized implementation:

- schema migration v2;
- Universe;
- optional Series;
- Novel;
- Chapter;
- Scene;
- immutable non-name IDs;
- deterministic sibling ordering;
- cross-universe Series/Novel integrity;
- conservative `RESTRICT` update/delete behavior;
- schema-level tests;
- Windows migration qualification.

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
- schema version advances from 1 to 2.

## Reproducibility contract

- no new dependency is introduced by M1.2;
- `package-lock.json` and `src-tauri/Cargo.lock` must remain unchanged;
- CI uses `npm ci`;
- Rust CI uses Cargo `--locked`;
- lockfile mutation is rejected in CI.

## Governance rule

M1.2 is not complete until exact-head CI, Windows migration qualification, merge, and post-merge normalization all pass.
