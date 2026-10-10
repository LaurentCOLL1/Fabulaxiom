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

**Status: COMPLETE + MERGED + NORMALIZED.** All M2.1–M2.5 are normalized after protected PR #30 merge `f13b4f8c249866ff60a19d7895b6cfaede56398a`, exact-head Windows CI #38041908126 SUCCESS. V1 remains incomplete; M3 implementation not authorized.

Accepted detailed roadmap: `docs/roadmap/M2_NARRATIVE_ENTITIES_CANONICAL_FACTS.md`.

M2.1 delivered SQLite v4 and Universe-scoped entity/alias registry. M2.2 implementation PR #23 merged at `ad7211fa2f292b8bd9812e299dbb6be96214eb89` after real Windows qualification on `b54fffd8e1f0224372e3b99cee07cb6df3203973` (13/13 interactive, 21/21 frontend and 51/51 Rust PASS, Ollama stopped, restored-active SQLite/backup/revisions preserved) and evidence-head CI `37864503602` on `a96870f823f24cb8962c9b0f43336ccb883ad5c3` (terminal success). See `docs/qualification/M2_2_ENTITY_ALIAS_CRUD.md`.

**M2.3 — Fact registry and exact revision provenance: COMPLETE + MERGED + NORMALIZED** after separate post-merge normalization acceptance.

PR #25 implemented SQLite v5 STRICT narrative fact/source registry and Rust/Tauri manual create/read/list with exact immutable revision citation spans, same-Universe validation, explicit sourced/unsourced facts and atomic rollback. Qualified code `4d3b4b6015d477c3a6a5c3750d9743174e9c44a7` (21/21 React, 61/61 Rust, 8/8 Windows operator GUI checks, controlled v4→v5 and fully preserved v4 baseline/backup); exact-evidence CI `37961014980` passed on `b015f7df80f38d75375a0e2615fd62d4c40ee1b8`. Implementation merged at `e6e80c26316f11054348a18a235fd08c600e136e`. Evidence: `docs/qualification/M2_3_IMPLEMENTATION_GATE.md`.

**M2.4 — Canon status and human review service: COMPLETE + MERGED + NORMALIZED** after separate M2.4 normalization acceptance.

PR #27 added SQLite v6 STRICT append-only review events and manual Rust/Tauri review/history/status APIs with `draft` default and seven distinct status values. Explicit `APPROVE_CANON`/`REVOKE_CANON` confirmation required. Windows-qualified code `aad56bd59fdb87be5ac1eda99b1969452bf61a26`: 21/21 frontend, 71/71 Rust, 8/8 existing GUI checks, 8/8 isolated review-service Rust tests, v5→v6 controlled migration with exact data/backup preservation. Evidence-HEAD CI `37989040863` succeeded on `b53405779b04c16525ba48a266bd096096af7020`, protected implementation merge `3a069572d00e1680c42b0f13b800e28687c5f0eb`. The reviewer label is not authenticated. Neither a dedicated React review interface nor its E2E IPC acceptance is delivered. Evidence: `docs/qualification/M2_4_CANON_REVIEW_IMPLEMENTATION_GATE.md`.

**M2.5 — Usable sourced-facts and human review UI:** implementation PR #29 merged at `f1e7ea99d26ad3390c7c47bfb339f26d730a44f1` from evidence SHA `6f55fc3fc7eab6f2288a54619c0bef70e521f47e` after exact-head CI #38040227617 (32/32 frontend, 72/72 Rust, all 13 Windows steps). Real Windows isolated UI acceptance and independent SQLite v6 verification PASS: 3 facts / 2 exact historical UTF-8 sources / 11 immutable review events, 8/8 hierarchy, 8/8 corrected synchronization, 9/9 facts, 10/10 human review. Source authority is now **COMPLETE + MERGED + NORMALIZED** after protected PR #30 merge `f13b4f8c249866ff60a19d7895b6cfaede56398a` and its own exact-head CI #38041908126 SUCCESS. No M3, AI extraction or ComfyUI implementation is authorized by this milestone closure.

Deliverables:

- characters, places, organizations, objects, events and world rules;
- aliases and renames;
- provenance down to source passage/version;
- status model: canon/draft/suggestion/variant/unknown/ambiguous/contradictory;
- fact validity periods;
- human validation workflow.

## M3 — Time, knowledge and relationships

**PLANNING PR #31 MERGED; NORMALIZATION PENDING.** Planning source `5127ced6c5e175b0919c736c658036382794487e` merged into `main=68db746754e01b441870e0653f17f10ebfc7be2f` after exact-head CI run `38050865413` (`completed/success`, one Windows job, 13/13 steps). The detailed plan is `docs/roadmap/M3_TIME_KNOWLEDGE_RELATIONSHIPS.md`. Once a separate normalization PR passes its own exact-head CI, merges under `expected_head_sha` and new `main` is re-fetched, **M3.1 only** becomes authorized for implementation through a separate bounded PR. M3.2–M3.6, production SQLite v7 migration without preflight, M4+, and ComfyUI remain unauthorized.

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
