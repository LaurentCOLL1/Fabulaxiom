# Fabulaxiom — V1 Roadmap

The V1 is the complete first product target. It is intentionally larger than the first technical milestone.

## M0 — Environment and architecture qualification

**Status: COMPLETE**

Terminal qualification:

- implementation/CI qualification SHA: `6fbea03be2b6058aa14d1cddcaffc7f840ebf81c`;
- deterministic M0 CI run: `37561269046`;
- result: `completed/success`;
- architecture ADR-007: ACCEPTED;
- local Windows execution: PASS;
- Ollama loopback security: PASS;
- dependency lockfiles committed and enforced.

Deliverables:

- verified Windows development toolchain;
- verified Ollama version, endpoint and actual compute backend;
- architecture decision for the first implementation;
- runnable desktop application;
- React → Tauri → Rust bridge;
- read-only local Ollama status integration;
- frontend and Rust test runners;
- deterministic Windows CI.

## M1 — Persistence and project foundation

**Status: NOT STARTED**

Deliverables:

- SQLite schema and migrations;
- Universe → optional Series → Novel → Chapter → Scene hierarchy;
- stable IDs;
- text version history;
- transactions and integrity checks;
- backup/restore baseline;
- no-AI CRUD flow.

## M2 — Narrative entities and canonical facts

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

Special tests include homonyms, flashbacks, incorrect beliefs, asymmetric relationships, simultaneous novels, past retcons, alternate branches, approximate dates and deliberately wrong AI extraction.

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

## Completion principle

Each milestone must end in a usable, testable state. Fabulaxiom must not become a text generator whose persistent-memory and integrity model is added only at the end.
