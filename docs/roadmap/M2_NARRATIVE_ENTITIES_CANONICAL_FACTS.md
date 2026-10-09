# M2 — Narrative Entities and Canonical Facts

## Authority and prerequisites

**PLAN ACCEPTED — M2.1–M2.4 COMPLETE + MERGED + NORMALIZED after M2.4 normalization; M2.5 NEXT only then**

Planning PR #17 merged as `4a9115ec362a0efae696ebc94b5101fa46d7a03a` after exact-head `Fabulaxiom CI` run `37722657799` completed/success.

Project: Fabulaxiom. Prior milestone M1 is **COMPLETE + MERGED + NORMALIZED**.

Planning base `main`: `b16be2ed3e6326c88b565b305bcaba2a6d590462`.

This plan subdivides M2 into bounded sequential deliverables. M2.1–M2.3 have passed their qualification, protected implementation merge and (upon acceptance of the independent normalization PR) normalizations. M2.2 merged via PR #23; M2.3 merged via PR #25 at `e6e80c26316f11054348a18a235fd08c600e136e` after exact evidence CI `37961014980` succeeded. **M2.4 is implemented and protected-merged via PR #27**. **M2.5 becomes the only next possible implementation after the independent M2.4 normalization merges and normalized main is re-fetched**.

M1.1–M1.5 are preserved:
- SQLite migrations, integrity checks and backups;
- Universe → optional Series → Novel → Chapter → Scene hierarchy;
- immutable IDs, deterministic sibling ordering, parent deletion restrictions;
- immutable scene text revisions and current-revision pointers;
- application-owned backup/restore with active-database marker;
- no-AI CRUD and operator-qualified Windows behavior.

## Milestone goal

Support narrative entities and human-governed canonical facts, with exact source provenance and explicit uncertainty. A fact must not silently become canon because an AI suggested it. This milestone is useful with Ollama completely stopped.

Entity kinds in M2:
1. character;
2. place;
3. organization;
4. object;
5. event;
6. world_rule.

Each entity belongs to one Universe. A single Universe-level entity may be referred to from several Novels in that Universe; do not duplicate the entity because it appears in a sequel. Independent universes cannot share the same entity ID as a cross-Universe reference.

## Non-negotiable semantics

### Identity, names and aliases

- Stable entity IDs are immutable and independent of display names.
- Renames update the display name but do not rewrite identity/history.
- Multiple entities may have the same display name; do not use names as foreign keys.
- Aliases are separately identified and belong to exactly one entity.
- Do not globally conflate Unicode case-folding with SQLite ASCII `NOCASE`.
- All linked records must remain in the same Universe, enforced in persistence and the service boundary where applicable.
- Delete with dependents must be explicit and restrictive, never cascade away narrative evidence silently.

### Sources and provenance

- A cited passage refers to an existing immutable `scene_text_revisions` row, never merely the mutable `scene_revision_heads` pointer.
- Source anchors include a start/end span in UTF-8 byte offsets of the immutable revision's `content`, using `[start,end)` boundaries.
- Validate `0 <= start < end <= content byte length` and both offsets must be valid UTF-8 boundaries.
- Store/derive the exact quoted passage to show what text supports the fact; the revision is authoritative.
- References cannot attach a revision from an unrelated Universe/Novel to an entity's Universe without an explicit error.
- A fact may be manually entered with an explicit `unsourced` provenance state; do not fabricate a citation.
- No full-text index, embeddings, search engine, or AI extractors in M2.

### Fact status and review

Controlled status vocabulary:

- `draft`: human-entered fact not yet canon;
- `suggestion`: proposed, never automatically canon;
- `canon`: explicitly approved by a human;
- `variant`: alternative/branch value not accepted as primary canon;
- `unknown`: explicitly unresolved, not a negative assertion;
- `ambiguous`: multiple interpretations pending review;
- `contradictory`: manually flagged conflict, **not** automatically proven by an M6 consistency engine.

Treat a fact's status independently from its text and provenance. Persist explicit review lineage (who/what action and time, without inventing identities), and reject invalid transitions deterministically. Promotion to `canon` must require an explicit user action; provenance requirements and human review are specified in the relevant subdivision.

### Temporal validity

- Store optional fact validity descriptors without assuming the Universe uses a Gregorian calendar.
- Distinguish unknown/approximate/relative validity from exact dates; do not invent a real-world epoch for fictional dates.
- M2 does not implement chronology, narrator/character belief timelines or travel consistency; those belong to M3/M6.

### No-AI acceptance

All M2 foundational CRUD, facts, review and inspection must remain usable when Ollama is stopped. The presence of AI-origin metadata never permits automatic writes to canon.

## Subdivision order and acceptance

### M2.1 — Entity registry schema and migration

**COMPLETE + MERGED + NORMALIZED**

Implementation PR #20 merged at `6c58b3bd4f0588436da8ba45adb875f897f426b2`; terminal evidence-head CI run `37814949619` completed/success and real Windows v3→v4 migration/integrity qualified. Evidence: `docs/qualification/M2_1_ENTITY_REGISTRY_SCHEMA.md`.

Scope:
- additive SQLite migration from current schema v3 to v4, with `STRICT` entity/alias tables;
- common `narrative_entities` registry scoped by Universe and kind;
- `entity_aliases` with separate immutable IDs, parent/entity FK and required nonempty alias text;
- stable entity IDs and immutable kind/owner identity; name is editable later;
- reject unknown entity kinds;
- `ON UPDATE RESTRICT` / `ON DELETE RESTRICT` for meaningful relationships;
- indexes on Universe, kind and alias FK;
- deterministic schema tests covering all six kinds, duplicates, foreign keys, immutable IDs, invalid kinds and migration re-runs.

Acceptance:
- existing v3 data and all M1 tables/revision pointers remain untouched;
- fresh v1/v2/v3 and production v3 upgrade paths produce v4 exactly once;
- `PRAGMA foreign_key_check` empty and `PRAGMA integrity_check` `ok`;
- no loss of a saved text revision or of the active restored database selection;
- source checkout, lockfiles and migration version evidence tied to exact SHA;
- Windows operator backs up the **resolved active database**, not assumed default `fabulaxiom.sqlite3`, before v3→v4;
- deterministic tests and Windows CI must pass, then target-machine migration qualification, evidence SHA, exact-head requalification, implementation merge and post-merge normalization.

Boundary: **schema/migration only**; do not add entity CRUD UI, facts, aliases editing service, Ollama calls or M2.2+ functionality.

### M2.2 — No-AI entity and alias CRUD

**COMPLETE + MERGED + NORMALIZED** (effective after independent normalization PR merge).

Qualified Windows code `b54fffd8e1f0224372e3b99cee07cb6df3203973`; operator interactive 13/13 PASS with Ollama OFF; frontend 21/21, Rust 51/51 PASS; postinteractive SQLite v4 integrity and source history/backup preservation PASS. Evidence: `docs/qualification/M2_2_ENTITY_ALIAS_CRUD.md`. Exact-head documentary CI `37864503602` on `a96870f823f24cb8962c9b0f43336ccb883ad5c3`: `completed/success`. Protected PR #23 implementation merge: `ad7211fa2f292b8bd9812e299dbb6be96214eb89`.

Scope:
- Rust service models/DTOs and deterministic errors for create/read/list/rename/delete;
- entity kind/Universe owner immutable;
- alias create/list/update/delete without changing entity identity;
- thin Tauri boundary and usable React forms for six entity kinds;
- no duplicate names prohibition unless identity semantics warrant it;
- ownership / foreign-key enforcement, transaction rollback and child guards.

Acceptance:
- all six kinds, multiple Universes, alias/rename, same-name distinct IDs;
- delete with dependent alias/fact restrictions;
- no Ollama dependency;
- all M1 tests preserved plus targeted Windows UI qualification and exact-head CI.

### M2.3 — Fact registry and exact revision provenance

**COMPLETE + MERGED + NORMALIZED — after independent post-merge normalization PR approval.**

Implementation PR #25 merged at `e6e80c26316f11054348a18a235fd08c600e136e`; qualified Windows code `4d3b4b6015d477c3a6a5c3750d9743174e9c44a7`; evidence-head CI `37961014980` terminal SUCCESS on `b015f7df80f38d75375a0e2615fd62d4c40ee1b8`. Pre-v5 backup SHA-256 `c624241080d6e820398cc502b4db206fcaba457405083ce806c302a6ce464976`; real v4→v5, 9 entities, 8 aliases, 3 scene revisions/current head and all old table digests preserved. UI 8/8 PASS; frontend 21/21, Rust 61/61 PASS. See `docs/qualification/M2_3_IMPLEMENTATION_GATE.md`. No fact-editor React UI or canon state is delivered.

Scope:
- normalized structured fact records with stable IDs and associated entity IDs;
- optional source anchors tied to immutable Scene revision + byte span;
- explicit sourced vs unsourced provenance;
- rigid same-Universe checks across fact/entity/revision;
- payload validation for offsets, source excerpts and nonempty fact value;
- optional time-validity descriptors without a calendar engine;
- atomic multi-row source/fact writes.

Acceptance:
- exact quoted text preserved after scene head changes/restores;
- invalid UTF-8 boundaries, out-of-range spans and cross-Universe anchors rejected;
- transaction failure rolls back fact and source together;
- no fabricated provenance, no automatic canon promotion;
- existing data preserved, deterministic and Windows-integrity qualification PASS.

### M2.4 — Canon status and review service

**COMPLETE + MERGED + NORMALIZED after separate post-merge normalization acceptance.**

Implementation PR #27 protected-merged at `3a069572d00e1680c42b0f13b800e28687c5f0eb`. Qualified source `aad56bd59fdb87be5ac1eda99b1969452bf61a26`, evidence HEAD `b53405779b04c16525ba48a266bd096096af7020`, evidence `Fabulaxiom CI` `37989040863` terminal SUCCESS (13/13 Windows CI steps); source run `37974831473` terminal SUCCESS (21/21 React, 71/71 Rust). Controlled SQLite v5→v6 after separate SHA-256 verified backup, exact data-integrity audit and existing GUI 8/8 PASS; isolated real Windows Rust review tests 8/8 PASS with no production SQLite changes. New append-only STRICT `fact_review_events`, status/history and deliberate approve/revoke operations. **Not a React fact-review UI nor an authenticated human identity claim.** See `docs/qualification/M2_4_CANON_REVIEW_IMPLEMENTATION_GATE.md`.

Scope:
- deterministic status lifecycle with vocabulary above;
- explicit human action required to make a fact canonical;
- durable review records and auditable status changes;
- separate uncertain, contradicted and alternate facts;
- prevent unreviewed suggestions from being presented as accepted canon.

Acceptance:
- transitions require appropriate input and produce stable errors;
- `suggestion` never becomes `canon` automatically;
- review history preserved even if display name changes;
- no AI dependency, rollback, exact-head CI and Windows tests.

### M2.5 — Usable sourced-facts and human review UI

**NEXT AUTHORIZED ONLY AFTER M2.4 NORMALIZATION MERGES AND CURRENT MAIN IS RE-FETCHED — NOT IMPLEMENTED IN THIS DOCUMENTARY PR**

Scope:
- React flow for entering facts, attaching/verifying source passages and viewing cited revision;
- browsing sources, validity descriptors and status;
- explicit canon approval/rejection controls showing consequences;
- clear differentiation of `unknown`, `ambiguous` and `contradictory`;
- read-only history for previously reviewed changes.

Acceptance:
- manual end-to-end workflow over multiple Novels and Universes;
- exact passage/scene revision remains stable across scene revisions;
- no Ollama calls for manual workflow;
- Windows operator qualification with backups and integrity verification;
- exact-head terminal CI, merge and post-merge normalization.

## Milestone completion rule

M2 can be marked **COMPLETE + MERGED + NORMALIZED** only when M2.1 through M2.5 each pass deterministic exact-head CI, required real Windows qualifications, evidence requalification, merge and their own post-merge normalization.

Do not begin M3 or future M2 subdivisions merely because a preceding PR appears complete.

## Explicitly excluded

- M3: evolving relationships, character/narrator/reader knowledge, full timeline/calendars and causal order;
- M4: SQLite FTS5, semantic search, embeddings/vector index, RAG;
- M5: Ollama generation, model selection, streaming or AI fact extraction;
- M6: automatic contradiction detection/scoring;
- M7+: assisted writing, manuscript generation, export and packaging.

## Implementation governance

1. Re-fetch private GitHub `main`, live PRs, roadmaps and HEADs before any mutation.
2. One authorized subdivision at a time; dedicated branch from exact live `main`.
3. Retain `rusqlite`, Rust/Tauri and React wherever sufficient; no reflexive new dependencies.
4. Preserve `package-lock.json` and `src-tauri/Cargo.lock` with `npm ci`, `cargo test --locked` and `cargo check --locked`.
5. CI `pull_request` proof is valid only for the exact current PR SHA.
6. For migrations, do not touch production data through GitHub. Back up the **actual active** SQLite database on the operator Windows host after verifying its active marker and integrity.
7. If any operation requires UI confirmation, new credentials, elevation or local data mutation, explain manual interactions before presenting a PowerShell block.
8. Revalidate backup, revision history and current-head fidelity after every migration.
9. Windows evidence commit creates a fresh SHA and requires new terminal CI before merge.
10. No next subdivision without post-merge normalization of the current one.
