# Fabulaxiom — Current State

## Repository

- Repository: `LaurentCOLL1/Fabulaxiom`
- Visibility: private
- Default branch: `main`

## Milestone state

### M0 — Environment and architecture qualification

**COMPLETE + MERGED + NORMALIZED**

### M1 — Persistence and project foundation

**COMPLETE + MERGED + NORMALIZED**

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

**COMPLETE + MERGED + NORMALIZED**

Implementation PR:

**#13 — feat: implement M1.4 text revisions and provenance foundation**

Implementation merge:

`75ab73b176b481f64b0e7f8c510b4ede0c617e31`

Qualified implementation SHA:

`d62fe92e4c01e5a58a6fbf85bdcf465267b41ea6`

Windows qualification evidence commit:

`e6b3bf13399604a3b4922f9510a1c6761d9e5775`

Terminal exact-head CI:

- workflow: `Fabulaxiom CI`;
- run: `37709917550`;
- result: `completed/success`;
- frontend tests: 10/10 PASS;
- Rust tests: 29/29 PASS;
- frontend build and `cargo check --locked`: PASS;
- lockfiles unchanged.

Windows qualification:

- source exact, worktree clean, Ollama stopped;
- production SQLite schema v2 backed up via SQLite Backup API; SHA256 preserved;
- production migration v2 → v3 PASS;
- two `STRICT` revision tables and three migrations present;
- immutable append-only scene text revisions, lineage and current pointer;
- operator-reported create v1/v2, restore v1 and save v3 scenario PASS;
- persisted three revisions, one current head;
- `PRAGMA foreign_key_check`: empty;
- `PRAGMA integrity_check`: `ok`;
- Ollama remained stopped through qualification.

Detailed evidence:

`docs/qualification/M1_4_TEXT_REVISIONS_PROVENANCE.md`

Delivered M1.4 foundation:

- schema v3 for scene text revisions and explicit current heads;
- immutable revision IDs, database timestamps and per-scene revision ordering;
- parent revision provenance;
- transactional creation and pointer changes;
- guarded scene deletion with existing revision history;
- Rust/Tauri revision commands and React editor/history;
- no dependency on Ollama.

#### M1.5 — Backup and restore baseline

**COMPLETE + MERGED + NORMALIZED**

Implementation PR: **#15 — feat: implement M1.5 safe SQLite backup and restore baseline**

Implementation merge:

`282b325fb6c588a70df08a5128415c8fa0a0f72e`

Windows-qualified implementation SHA:

`7f968075f632843144c9833f61cc51910b538530`

Windows qualification evidence commit:

`152b40e616f40799abc61f9ce8db142e3b19340b`

Terminal exact-head CI:

- workflow: `Fabulaxiom CI`;
- run: `37720676744`;
- result: `completed/success`;
- frontend tests: 13/13 PASS;
- Rust tests: 37/37 PASS;
- frontend production build: PASS;
- `cargo check --locked`: PASS;
- dependency lockfiles unchanged.

Windows qualification:

- exact main/PR HEAD and local worktree clean: PASS;
- SQLite schema v3 and Tauri/Rust bridge PASS;
- Ollama unavailable as intended;
- application-created verified backup: PASS;
- UI-confirmed restore and reload: PASS;
- 1 Universe, 1 Novel, 1 Scene, 3 revisions, 1 current revision head preserved;
- previous active database is not overwritten by the restore design;
- operator historic backups are preserved;
- actual restored database path and independent post-restore integrity PRAGMAs were not supplied as evidence;
- three nonfatal Rust unused-code warnings remain tracked.

Detailed evidence:

`docs/qualification/M1_5_BACKUP_RESTORE_BASELINE.md`

Delivered:

- SQLite-consistent `VACUUM INTO` snapshot to app-owned unique backup files;
- schema owner, migration and integrity validation;
- new non-overwriting database file for restore;
- durable activation marker and old database preservation;
- deterministic Rust/Tauri errors and explicit restore confirmation;
- React backup/list/restore controls without Ollama;
- source preservation, failure and backup/restore automated tests.

### M1 closure

M1.1–M1.5 are all **COMPLETE + MERGED + NORMALIZED**. M1's database, hierarchy, revision history and backup/restore baseline are delivered and qualified. This is **not** a declaration that V1 as a whole is complete.

### M2 — Narrative entities and canonical facts

**IN PROGRESS**

Detailed planning PR #17 merged at `4a9115ec362a0efae696ebc94b5101fa46d7a03a`.

Accepted roadmap: `docs/roadmap/M2_NARRATIVE_ENTITIES_CANONICAL_FACTS.md`.

#### M2.1 — Entity registry schema and migration

**COMPLETE + MERGED + NORMALIZED**

Implementation PR: **#20 — feat: implement M2.1 narrative entity registry schema v4**.

Implementation merge:

`6c58b3bd4f0588436da8ba45adb875f897f426b2`

Qualified implementation SHA:

`c7a663d88ba2538714d42fdd366719cd54fe6f70`

Windows qualification evidence SHA:

`88fa3b22904b92d4ecdcb32ed7fd01dc23e24a4c`

Terminal exact-head CI:

- workflow: `Fabulaxiom CI`;
- run: `37814949619`;
- `completed/success`;
- frontend 13/13, Rust 44/44 tests PASS;
- frontend build, `cargo check --locked` and lockfile check PASS.

Windows production schema-v3 → schema-v4 qualification:

- actual restored active database resolved from M1.5 activation marker, not assumed default;
- source and backup verified before migration, backup SHA256 preserved;
- migration v4 applied by Tauri, four migrations recorded exactly once;
- both new narrative registry/alias tables STRICT;
- four immutable-identity triggers, two indexes;
- six narrative kinds constrained at schema level;
- existing hierarchy, metadata, revision and current-head rows unchanged in logical value;
- three scene text revisions and one current revision head preserved;
- `PRAGMA foreign_key_check` empty and `PRAGMA integrity_check` `ok`;
- no Ollama dependency; final worktree CLEAN;
- original backup and active activation marker unchanged.

Detailed evidence:

`docs/qualification/M2_1_ENTITY_REGISTRY_SCHEMA.md`

Delivered M2.1 scope:
- SQLite schema v4 for Universe-scoped narrative entity registry and aliases;
- immutable IDs, entity kind and Universe ownership; FK restrictions/indexes;
- M1.5 v3/v4 backup and safe legacy-v3 restore compatibility;
- deterministic regression tests;
- **no** entity CRUD UI, fact/canon engine, image/ComfyUI code.

#### M2.2 — No-AI entity and alias CRUD

**WINDOWS QUALIFIED — IMPLEMENTATION MERGE / NORMALIZATION PENDING**

Windows-qualified source: `b54fffd8e1f0224372e3b99cee07cb6df3203973`; operator interactive alias / entity scenarios **13/13 PASS** on real Windows with Ollama OFF. Local preflight **21/21 frontend, 51/51 Rust PASS**; SQLite v4 postinteractive checks, eight alias rows, nine entity rows, one same-name pair with different IDs, 3 scene revisions and current pointer preservation PASS. Details: `docs/qualification/M2_2_ENTITY_ALIAS_CRUD.md`.

CI on Windows-qualified source: `Fabulaxiom CI` run `37831790345`, `completed/success`. **Documentary evidence commit has a new SHA and requires its own terminal exact-head CI before protected implementation merge.** Post-merge normalization remains mandatory; M2.3+ still blocked.

Branch: `feat/m2-2-entity-alias-crud-20261008`

Start base `main`: `70beb4f998ba3e587533dd7a90689eadeae4f4c3`.

Only M2.2 is authorized; no M2.3+ development.

Scope:
- Rust service models/DTOs and deterministic create/read/list/rename/delete errors;
- thin Tauri command boundary and usable React screens for six entity kinds and alias management;
- immutable kind/Universe identity, distinct IDs and restrictive referential behavior;
- transactional multi-step operations and rollback;
- fully usable with Ollama stopped.

M2.3–M2.5 and M3+ remain unauthorized until their own acceptance, merge and normalization gates.

The proposed ComfyUI image/reference atelier is tracked in issue #19 and the accepted **proposal-only** V1 roadmap addition. No image/ComfyUI implementation is authorized by M2.1 or M2.2.

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
