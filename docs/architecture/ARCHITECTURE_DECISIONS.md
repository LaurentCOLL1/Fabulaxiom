# Fabulaxiom — Architecture Decisions

This document records architecture decisions and prevents tentative ideas from becoming accidental requirements.

## Decision log

| ID | Status | Decision |
|---|---|---|
| ADR-001 | Accepted | Fabulaxiom is local-first. Core functions must not require a cloud API. |
| ADR-002 | Accepted | Ollama is the initial local LLM runtime. Models must be configurable by role. |
| ADR-003 | Accepted | Original text and structured data remain authoritative; summaries and vector indexes are rebuildable derivatives. |
| ADR-004 | Accepted | SQLite is the preferred starting point for structured persistence unless a concrete blocker is demonstrated. |
| ADR-005 | Accepted | The data model must support stable entity identifiers independent of names. |
| ADR-006 | Accepted | AI output must be validated before it mutates canonical state. |
| ADR-007 | Open | Final desktop/web shell architecture. |
| ADR-008 | Open | Rich-text editor choice. |
| ADR-009 | Open | Local vector-search implementation. |
| ADR-010 | Open | Packaging strategy for any Python backend on Windows. |

## Candidate architecture A

- React + TypeScript frontend
- Tauri desktop shell
- Python + FastAPI backend
- SQLite + FTS5
- local vector index
- Ollama local API

### Advantages

- clear separation between UI and narrative/AI logic;
- mature Python ecosystem for NLP, validation and document processing;
- Tauri can provide a native desktop distribution with a web frontend.

### Risks to validate

- shipping and updating Python alongside Tauri on Windows;
- managing two runtime ecosystems;
- process lifecycle and IPC/local HTTP boundaries;
- installer size and diagnostics;
- cancellation and streaming across process boundaries.

## Architectural invariants

Whatever stack is selected, it must support:

- database migrations;
- transactions and referential integrity;
- backup and tested restore;
- cancellation of AI generations;
- progressive generation display;
- queued long-running jobs with progress;
- strict structured-output validation;
- context budgeting and chunking;
- cache/index invalidation;
- model-role configuration;
- sequential model loading where needed;
- unit and integration tests;
- local-only network binding by default.

## Decision method

For every open ADR, choose the simplest option that meets the constraints and can be packaged, tested and debugged reliably on Windows.
