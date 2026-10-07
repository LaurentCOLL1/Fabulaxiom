# M1.3 — No-AI CRUD Service Qualification

## Status

**COMPLETE + MERGED + NORMALIZED**

## Scope

M1.3 delivers the first usable Fabulaxiom hierarchy CRUD without any dependency on Ollama:

`Universe → optional Series → Novel → Chapter → Scene`

Narrative AI, text revisions/provenance, backup/restore, FTS, embeddings, manuscript generation, canonical-fact extraction and consistency-engine work remain out of scope.

## Implementation

Implementation PR:

**#11 — feat: implement M1.3 no-AI CRUD service**

Implementation merge:

`49424f1ecafa1be3c4f47b806231b6644e9c73a4`

Base `main` at subdivision start:

`4f90a66a30c72446bfab3dc20429429b6e4217b7`

Exact implementation SHA qualified on Windows:

`6259bd3b4759b683bf4bb7c2c6efdf693ddfebac`

Qualification evidence SHA:

`d9df8151b0c3336e0a12c65a7ba7841cab4e091b`

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
- cross-Universe Series use is rejected/prevented by service/UI/schema invariants;
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

## Implementation CI

Workflow:

`Fabulaxiom CI`

Run:

`37665443163`

Head:

`6259bd3b4759b683bf4bb7c2c6efdf693ddfebac`

Result:

**completed / success**

Frontend:

- 3 test files PASS;
- 8 tests PASS;
- 0 failures;
- production build PASS.

Rust:

- 20 tests PASS;
- 0 failures;
- `cargo check --locked`: PASS.

Dependency locks unchanged:

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
- local HEAD exact: PASS;
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

### Rust bridge

`Tester le pont Rust`: **PASS**

Observed milestone:

`M1.3 no-AI CRUD service`

### SQLite

`Vérifier la base locale`: **PASS**

- SQLite schema v2;
- foreign keys ON;
- production database path resolved correctly.

### Ollama

`Vérifier Ollama local`: **INDISPONIBLE — EXPECTED**

The local Ollama API remained inaccessible. This is an acceptance success because M1.3 CRUD must work without Ollama.

### CRUD qualification

Temporary `QUAL-M13-*` data exercised:

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

All requested interactive tests passed, including:

- optional Series: PASS;
- same-Universe Series assignment/change: PASS;
- cross-Universe Series protection: PASS;
- rename Universe/Series/Novel/Chapter/Scene: PASS;
- Series/Novel/Chapter/Scene reorder: PASS;
- Chapter deletion with Scenes rejected with `has_children`: PASS;
- Novel deletion with Chapters rejected with `has_children`: PASS;
- Universe deletion while descendants remain rejected: PASS;
- CRUD remained responsive and functional while Ollama stayed stopped: PASS.

## Post-qualification integrity

After closing Fabulaxiom:

- HEAD still exact: PASS;
- final worktree clean: PASS;
- `PRAGMA foreign_key_check`: empty;
- `PRAGMA integrity_check`: `ok`;
- remaining `QUAL-M13-*` rows: 0 for Universes, Series, Novels, Chapters and Scenes;
- Ollama remained stopped: PASS.

## Terminal evidence-commit CI

The Windows qualification was recorded in evidence commit:

`d9df8151b0c3336e0a12c65a7ba7841cab4e091b`

Workflow:

`Fabulaxiom CI`

Run:

`37684422252`

Result:

**completed / success**

All deterministic steps passed on that exact evidence head:

- `npm ci`;
- frontend tests;
- frontend production build;
- `cargo test --locked`;
- `cargo check --locked`;
- dependency-lock mutation check.

## Conclusion

M1.3 satisfied implementation, deterministic CI, real Windows no-AI CRUD qualification, integrity, exact-head evidence requalification, merge and post-merge normalization requirements.

M1.4 may begin only from live normalized `main`.
