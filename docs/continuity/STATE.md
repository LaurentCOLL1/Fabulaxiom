# Fabulaxiom — Current State

## Repository

- Repository: `LaurentCOLL1/Fabulaxiom`
- Visibility: private
- Default branch: `main`
- Initial baseline commit: `a5d677256a7cf7cbd1b114138021341cab12f966`
- Current phase: project bootstrap

## Product identity

- Product name: **Fabulaxiom**
- Internal/package naming convention: `fabulaxiom`
- Name intent: `fabula` (story/narrative) + `axiom` (foundational truth)

## Confirmed product principles

Fabulaxiom is intended to be a local-first application for long-form fiction, novels, sagas and shared fictional universes.

Confirmed constraints:

1. Essential features must remain usable without Internet once dependencies and models are installed.
2. Ollama is the initial local model runtime.
3. The application must preserve original text and structured narrative facts with provenance.
4. Structured canonical facts and original source passages take precedence over summaries and embeddings.
5. AI suggestions never become canon automatically.
6. Unknown information must not be converted into a false fact.
7. The application must distinguish canon, drafts, suggestions, non-canonical variants, unknowns, ambiguities and contradictions.
8. The application must remain usable without AI.
9. Manuscripts and private local data must not be transmitted to external services without explicit consent.
10. Reliability of narrative memory and controlled modification take priority over the number of AI features.

## Target environment currently known

- Primary OS: Windows 11
- RAM: 32 GB
- GPU: AMD Radeon RX 6750 XT
- VRAM: 12 GB
- Ollama: already installed, exact version/backend still to be verified
- CUDA instructions are not applicable to the target GPU.

## Architecture status

No application architecture is final yet.

The following stack remains a candidate only:

- React + TypeScript
- Tauri desktop shell
- Python + FastAPI local backend
- SQLite
- SQLite FTS5
- local vector search
- Ollama local API

Before freezing this stack, the project must compare packaging/maintenance tradeoffs on Windows, especially the cost of shipping a Python backend inside a Tauri desktop application.

## Development status

No production application code exists yet.

The current task is repository governance and project bootstrap.

## Acceptance rule

A milestone may only be marked complete after:

- its code exists;
- its tests have been executed;
- the observed result is recorded;
- known failures are documented;
- the next dependent milestone is not started on an unverified assumption.
