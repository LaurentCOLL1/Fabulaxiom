# Fabulaxiom — V1 Roadmap

The V1 is the complete first product target. It is intentionally larger than the first technical milestone.

## M0 — Environment and architecture qualification

**Status: COMPLETE + MERGED + NORMALIZED**

Deliverables completed:

- verified Windows development toolchain;
- verified Ollama endpoint and Vulkan compute backend;
- accepted Tauri 2 + React/TypeScript + Rust architecture;
- runnable desktop application;
- React → Tauri → Rust bridge;
- loopback-only read-only Ollama status integration;
- frontend and Rust tests;
- committed dependency locks;
- deterministic Windows CI.

## M1 — Persistence and project foundation

**Status: COMPLETE + MERGED + NORMALIZED**

Detailed plan:
`docs/roadmap/M1_PERSISTENCE_PROJECT_FOUNDATION.md`

Subdivision status:

- M1.1 — SQLite foundation and migration runner: **COMPLETE + MERGED + NORMALIZED**
- M1.2 — Project hierarchy schema: **COMPLETE + MERGED + NORMALIZED**
- M1.3 — No-AI CRUD service: **COMPLETE + MERGED + NORMALIZED**
- M1.4 — Text revisions and provenance foundation: **COMPLETE + MERGED + NORMALIZED**
- M1.5 — Backup and restore baseline: **COMPLETE + MERGED + NORMALIZED**

M1 deliverables overall:

- SQLite schema and migrations;
- Universe → optional Series → Novel → Chapter → Scene hierarchy;
- stable IDs;
- no-AI hierarchy CRUD;
- text version history;
- transactions and integrity checks;
- backup/restore baseline.

## M2 — Narrative entities and canonical facts

**Status: IN PROGRESS — M2.1 and M2.2 COMPLETE + MERGED + NORMALIZED; M2.3 NEXT AUTHORIZED after normalization merge**

Accepted detailed roadmap: `docs/roadmap/M2_NARRATIVE_ENTITIES_CANONICAL_FACTS.md`.

M2.1 delivered SQLite v4 and Universe-scoped entity/alias registry. M2.2 implementation PR #23 merged at `ad7211fa2f292b8bd9812e299dbb6be96214eb89` after real Windows qualification on `b54fffd8e1f0224372e3b99cee07cb6df3203973` (13/13 interactive, 21/21 frontend and 51/51 Rust PASS, Ollama stopped, restored-active SQLite/backup/revisions preserved) and evidence-head CI `37864503602` on `a96870f823f24cb8962c9b0f43336ccb883ad5c3` (terminal success). See `docs/qualification/M2_2_ENTITY_ALIAS_CRUD.md`.

**M2.3 — Fact registry and exact revision provenance** becomes the sole next authorized implementation only after this independent M2.2 normalization PR is CI-qualified and merged. M2.4–M2.5 and M3+ remain blocked; visual ComfyUI extension remains proposal-only.

Deliverables:

- characters, places, organizations, objects, events and world rules;
- aliases and renames;
- provenance down to source passage/version;
- status model: canon/draft/suggestion/variant/unknown/ambiguous/contradictory;
- fact validity periods;
- human validation workflow.

## M3 — Time, knowledge and relationships

Deliverables:

- chronology distinct from narration order and reader reveal order;
- exact, approximate and relative dates;
- asymmetric evolving relationships;
- character knowledge/beliefs;
- narrator knowledge and reader-spoiler state;
- possessions, locations, injuries and life-state changes.

## M4 — Retrieval and narrative memory

Deliverables:

- SQLite FTS5 search;
- hierarchical summaries;
- rebuildable embeddings/indexes;
- local semantic retrieval;
- question-answering over the universe with cited sources;
- targeted context builder.

## M5 — Ollama integration

Deliverables:

- configurable model roles for writing, planning, extraction, summaries and consistency;
- model metadata inspection;
- streaming output;
- cancellation;
- task queue;
- strict JSON validation and bounded retries;
- context/memory budgeting;
- graceful Ollama failure handling.

## M6 — Consistency engine

Deliverables:

- deterministic contradiction rules;
- AI-assisted analysis where useful;
- separation of proven contradictions, suspicions and insufficient information;
- source-linked alerts;
- severity and proposed fixes;
- no automatic manuscript correction.

## M7 — Assisted writing

Deliverables:

- free editing without AI;
- scene goals and planning;
- continuation proposals;
- rewrite selection;
- style variants;
- dialogue assistance;
- targeted retrieval of relevant facts;
- post-generation consistency checks;
- extraction of proposed new facts followed by user validation.

## M8 — Advanced V1 narrative management

Deliverables:

- relationship map at a chosen time;
- shared multi-novel timeline;
- plot-thread tracking;
- clue/mystery/promise/reveal tracking;
- isolated “what if” branches;
- retcon impact analysis;
- spoiler management;
- dashboards for contradictions and pending validations.

## Extension proposée — Atelier de références visuelles et ComfyUI local

**PROPOSAL ONLY — NOT AUTHORIZED FOR IMPLEMENTATION**

See `docs/roadmap/V1_VISUAL_REFERENCES_COMFYUI_PROPOSAL.md` and issue #19.

The user requests images of narrative characters, scenes, events and situations as optional inspiration and visual evaluation aids. Potential phases: local image import/gallery and associations after narrative identity foundation; then an opt-in ComfyUI local connector and variation/consistency workflows. The exact milestone and subdivision authorization must be accepted through a separate roadmap governance PR. This proposal does not change M2.1's schema-only boundaries or authorize any ComfyUI code.

## M9 — Import, export, resilience and distribution

Deliverables:

- assisted import of existing text;
- Markdown export;
- DOCX export;
- EPUB export;
- documented full-universe export/reimport;
- local visual references;
- automatic/exportable backups;
- tested restore;
- Windows packaging and installer;
- release qualification.
