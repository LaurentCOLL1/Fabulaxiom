# Fabulaxiom — Current State

## Repository

- Repository: `LaurentCOLL1/Fabulaxiom`
- Visibility: private
- Default branch: `main`

## Milestone state

### M0 — Environment and architecture qualification

**COMPLETE + MERGED + NORMALIZED**

M0 is closed.

### M1 — Persistence and project foundation

**IN PROGRESS**

#### M1.1 — SQLite foundation and migration runner

**COMPLETE + MERGED — POST-MERGE NORMALIZATION IN PROGRESS**

Authoritative evidence:

- PR #5: merged
- merge commit:
  `d212de93cc869bfbe0e047a12594d23e1732d5cb`
- final PR head:
  `11fc259816ac4f4e98672aa42c9176d140f783fd`
- terminal exact-head CI:
  - workflow: `Fabulaxiom CI`
  - run: `37637727620`
  - result: `completed/success`
- Windows qualification: PASS
- `rusqlite 0.40.2` with bundled SQLite
- database path under Tauri local app-data
- schema version 1
- foreign keys ON per connection
- transactional migration runner
- initial migration `001_create_app_metadata`
- Rust tests: 6/6 PASS
- frontend tests: 4/4 PASS
- deterministic lockfile checks: PASS

Detailed evidence:

`docs/qualification/M1_1_SQLITE_FOUNDATION.md`

#### M1.2 — Project hierarchy schema

**AUTHORIZED AFTER THIS NORMALIZATION MERGES**

Scope:

- Universe;
- optional Series;
- Novel;
- Chapter;
- Scene;
- stable immutable IDs;
- ordering fields;
- referential/integrity rules;
- schema-level tests.

No CRUD UI/service is authorized yet; that belongs to M1.3.

## Reproducibility contract

- `package-lock.json` committed
- `src-tauri/Cargo.lock` committed
- CI uses `npm ci`
- Rust CI uses Cargo `--locked`
- lockfile mutation is rejected in CI

## Known non-blocking environment warnings

- Ollama AMD-driver warning while Vulkan inference works
- potentially incompatible external `ggml-base.dll` in PATH
- two corrupt Ollama manifests

These remain documented and do not block M1.2.

## Governance rule

Every subdivision must:

- begin from freshly fetched live `main`;
- use a dedicated branch and pull request;
- preserve deterministic dependency locks;
- pass exact-head CI;
- receive Windows operator qualification when local behavior is part of acceptance;
- be merged and normalized before a dependent subdivision begins.
