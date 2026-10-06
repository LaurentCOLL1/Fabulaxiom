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
| ADR-007 | Provisional | M0/M1 preferred shell: Tauri 2 + React/TypeScript + Rust/Tauri core. Final acceptance requires a successful Windows skeleton build. |
| ADR-008 | Open | Rich-text editor choice. |
| ADR-009 | Open | Local vector-search implementation. |
| ADR-010 | Deferred | Do not ship Python/FastAPI as a mandatory runtime for M0/M1. Add a Python sidecar later only if a concrete feature justifies it. |

## Options compared

### Option A — Tauri + React/TypeScript + packaged Python/FastAPI

Advantages:

- strong Python ecosystem for NLP, validation and document tooling;
- clear HTTP boundary between UI and backend.

Costs:

- ships and updates both Rust/Tauri and Python runtime ecosystems;
- requires lifecycle management for a local backend process;
- creates an additional IPC/local-HTTP boundary;
- complicates installer, diagnostics and cancellation/streaming;
- violates the project's preference to avoid unnecessary services unless Python is actually needed.

### Option B — Tauri 2 + React/TypeScript + Rust/Tauri core — preferred for M0/M1

Core components:

- React + TypeScript user interface;
- Tauri 2 desktop shell;
- Rust commands/services for application logic;
- SQLite + FTS5;
- direct HTTP client to the local Ollama API;
- filesystem access only through explicit application services.

Advantages:

- one packaged desktop application runtime instead of Tauri plus a mandatory Python service;
- native desktop lifecycle and filesystem integration;
- Rust is already required by Tauri, so core backend logic does not introduce a third mandatory runtime;
- straightforward local-only Ollama integration over its HTTP API;
- suitable for deterministic validation rules, migrations, transactions and backup logic.

Tradeoffs:

- Rust has a steeper implementation learning curve than Python;
- some future import/export/NLP tasks may have stronger Python libraries;
- those tasks should justify an optional sidecar when they actually arrive rather than imposing it on the whole V1 today.

### Option C — React + local FastAPI web application

Advantages:

- fastest initial development using the already-installed Python runtime;
- no Rust requirement for the first prototype.

Costs:

- weaker native desktop experience;
- browser/server lifecycle remains visible;
- packaging into a polished Windows application is deferred rather than solved;
- likely creates later migration work for desktop integration.

## Provisional conclusion

Use Option B for M0/M1 if the Windows Tauri toolchain qualifies successfully.

Python 3.12 remains available for development scripts, experiments and future optional workers, but it is not part of the mandatory production runtime at this stage.

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
