# M1.3 — No-AI CRUD Service Qualification

## Status

**WINDOWS QUALIFIED — FINAL EXACT-HEAD CI REQUIRED**

## Scope

M1.3 delivers the first usable Fabulaxiom hierarchy CRUD without any dependency on Ollama:

`Universe → optional Series → Novel → Chapter → Scene`

Narrative AI, text revisions/provenance, backup/restore, FTS, embeddings, manuscript generation, canonical-fact extraction and consistency-engine work remain out of scope.

## Qualified implementation source

Implementation PR:

**#11 — feat: implement M1.3 no-AI CRUD service**

Branch:

`feat/m1-3-no-ai-crud-service-20261007`

Base `main` at subdivision start:

`4f90a66a30c72446bfab3dc20429429b6e4217b7`

Exact implementation SHA qualified on Windows:

`6259bd3b4759b683bf4bb7c2c6efdf693ddfebac`

## Delivered architecture

M1.3 keeps the M1 separation of responsibilities:

- `src-tauri/src/database.rs`: SQLite connection, migrations and persistence foundation;
- `src-tauri/src/hierarchy.rs`: application-layer models, DTOs, CRUD service, transaction logic and deterministic service errors;
- `src-tauri/src/hierarchy_commands.rs`: thin Tauri command boundary;
- React/TypeScript hierarchy workspace for the usable CRUD flow;
- Ollama status remains a separate diagnostic path and is not called by hierarchy CRUD.

No new dependency was added.

## Service behavior qualified

Application entities:

- Universe;
- Series;
- Novel;
- Chapter;
- Scene.

Qualified behavior:

- create/read/update/delete at every hierarchy level;
- IDs remain immutable;
- names/titles may change without identity change;
- Novel may remain standalone in a Universe;
- Novel may belong to a Series in the same Universe;
- same-Universe Series assignment/change is supported;
- cross-Universe Series use is rejected/prevented by the qualified flow and schema invariants;
- deterministic sibling ordering is preserved;
- reorder operations avoid transient UNIQUE-order collisions;
- parent deletion with remaining children returns deterministic `has_children` behavior;
- compound mutations use explicit transaction boundaries;
- failed compound mutation rollback is tested;
- service errors serialize to deterministic Tauri-safe payloads.

Deterministic application error codes include:

- `not_found`;
- `validation`;
- `has_children`;
- `cross_universe_series`;
- `order_conflict`;
- `database`.

## GitHub exact-head CI before Windows qualification

Workflow:

`Fabulaxiom CI`

Run:

`37665443163`

Head:

`6259bd3b4759b683bf4bb7c2c6efdf693ddfebac`

Result:

**completed / success**

Successful deterministic steps:

- checkout;
- Node.js setup;
- Rust setup;
- `npm ci`;
- frontend tests;
- frontend production build;
- `cargo test --locked`;
- `cargo check --locked`;
- dependency-lock mutation check.

Frontend result:

- 3 test files PASS;
- 8 tests PASS;
- 0 failures.

Rust result:

- 20 tests PASS;
- 0 failures.

The Rust suite includes the preserved M1.1/M1.2 database tests plus M1.3 tests covering:

- Universe CRUD and child deletion guard;
- Series CRUD, invalid Universe rejection and reorder;
- standalone Novel;
- Novel in Series;
- optional Series;
- same-Universe Series change;
- cross-Universe Series rejection;
- Novel rename/reorder and Chapter deletion guard;
- Chapter CRUD/reorder and Scene deletion guard;
- Scene CRUD/reorder/delete;
- composed mutation rollback;
- deterministic Tauri error serialization.

Dependency locks remained unchanged:

- `package-lock.json`;
- `src-tauri/Cargo.lock`.

## Windows qualification environment

Repository:

`M:\Fabulaxiom`

Production database:

`C:\Users\lauco\AppData\Local\com.fabulaxiom.desktop\database\fabulaxiom.sqlite3`

The existing M1.2 pre-migration backup remains preserved and was not deleted.

### Exact-source anti-race checks

Observed immediately before qualification:

- worktree clean: PASS;
- `remote.origin.fetch = +refs/heads/*:refs/remotes/origin/*`: PASS;
- live `origin/main = 4f90a66a30c72446bfab3dc20429429b6e4217b7`: PASS;
- live feature branch `= 6259bd3b4759b683bf4bb7c2c6efdf693ddfebac`: PASS;
- local HEAD `= 6259bd3b4759b683bf4bb7c2c6efdf693ddfebac`: PASS;
- upstream exact: PASS.

### Ollama-off precondition

Before launching the application:

- no Ollama process was running;
- `http://127.0.0.1:11434/api/version` was inaccessible.

Result:

**PASS**

### Deterministic local checks with Ollama stopped

Frontend:

- `npm ci`: PASS;
- `npm run test:ci`: 8/8 PASS;
- `npm run build`: PASS.

Rust:

- `cargo test --manifest-path src-tauri/Cargo.toml --all-targets --locked`: 20/20 PASS;
- `cargo check --manifest-path src-tauri/Cargo.toml --locked`: PASS.

Reproducibility:

- lockfiles unchanged: PASS;
- final pre-UI HEAD exact: PASS;
- worktree clean: PASS.

## Interactive Windows qualification with Ollama stopped

Fabulaxiom launched from the exact qualified source with Ollama still stopped.

### Rust bridge

Action:

`Tester le pont Rust`

Observed:

**PASS**

- Fabulaxiom;
- `M1.3 no-AI CRUD service`;
- React → Tauri → Rust operational.

### SQLite

Action:

`Vérifier la base locale`

Observed:

**PASS**

- SQLite schema v2;
- foreign keys ON;
- production database path resolved correctly.

### Ollama

Action:

`Vérifier Ollama local`

Observed:

**INDISPONIBLE — EXPECTED**

The local Ollama API remained inaccessible.

This is an acceptance success for M1.3 because CRUD must remain usable with Ollama stopped.

### CRUD qualification data

The operator exercised temporary `QUAL-M13-*` data covering:

- two Universes;
- same-Universe and cross-Universe Series fixtures;
- standalone Novel;
- Novel assigned to Series;
- Series changes for Novel;
- deterministic Series/Novel/Chapter/Scene reorder flows;
- Chapter and Scene hierarchy creation;
- rename at every hierarchy level;
- delete guards while children remained;
- leaf-to-parent cleanup.

All requested `QUAL-M13-*` interactive tests passed.

Observed acceptance behavior included:

- optional Series: PASS;
- same-Universe Series assignment/change: PASS;
- cross-Universe Series not offered to the qualified Novel flow: PASS;
- rename Universe/Series/Novel/Chapter/Scene: PASS;
- Series/Novel/Chapter/Scene reorder: PASS;
- Chapter deletion with Scenes present rejected with `has_children`: PASS;
- Novel deletion with Chapters present rejected with `has_children`: PASS;
- Universe deletion while descendants remain rejected: PASS;
- CRUD remained responsive and functional while Ollama stayed stopped: PASS.

## Post-qualification integrity

After closing Fabulaxiom:

- HEAD still exact: PASS;
- final worktree clean: PASS;
- `PRAGMA foreign_key_check`: empty;
- `PRAGMA integrity_check`: `ok`;
- remaining `QUAL-M13-*` rows:
  - Universes: 0;
  - Series: 0;
  - Novels: 0;
  - Chapters: 0;
  - Scenes: 0;
- Ollama remained stopped: PASS.

## Conclusion

M1.3 implementation and Windows no-AI CRUD qualification are accepted for the implementation SHA:

`6259bd3b4759b683bf4bb7c2c6efdf693ddfebac`

This evidence commit creates a new PR head. The prior CI run `37665443163` remains historical evidence for the qualified implementation SHA but cannot authorize merge of the new evidence SHA.

## Acceptance remaining

M1.3 may not be marked COMPLETE until:

1. this Windows qualification evidence is committed;
2. `Fabulaxiom CI` passes completely on that new exact head;
3. PR #11 is merged with expected-head protection;
4. live `main` is re-fetched;
5. post-merge M1.3 continuity normalization is created, exact-head qualified and merged.

M1.4 remains unauthorized until all five gates are complete.
