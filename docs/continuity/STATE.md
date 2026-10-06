# Fabulaxiom — Current State

## Repository

- Repository: `LaurentCOLL1/Fabulaxiom`
- Visibility: private
- Default branch: `main`
- Initial baseline commit: `a5d677256a7cf7cbd1b114138021341cab12f966`
- Current working branch: `chore/bootstrap-governance-20261006`
- Current phase: M0 environment and architecture qualification

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

## M0 evidence received from the operator — 2026-10-06

The following values were executed and reported from the target Windows machine:

- Windows command output: `Windows 10 Pro`, version `2009`, build `26220`.
  - This is recorded exactly as reported; the product-name label is not used to infer the actual commercial Windows generation.
- Git: `2.55.0.windows.3`.
- Python: `3.12.4`.
- Node.js: `24.16.0`.
- npm: `11.11.0`.
- Rust/Cargo: not installed / commands not found.
- Ollama: `0.35.1`.
- Ollama model inventory: 30 installed model entries observed.
- `qwen3.5:9b` runtime:
  - reported runtime size: `7.7 GB`;
  - processor: `100% GPU`;
  - context: `65536`;
  - repeated `ollama ps` observations remained at `100% GPU`.
- A French long-form generation completed successfully with `qwen3.5:9b`.

### Evidence not yet complete

- The explicit `/api/version` test produced no visible payload in the pasted console output and must be re-run with forced JSON rendering.
- The `Win32_VideoController` query produced no visible device row in the pasted output and must be re-run with forced list/string formatting.
- GPU acceleration is proven, but the exact Ollama backend implementation (for example Vulkan vs ROCm/HIP) is not yet proven.
- Microsoft C++ Build Tools availability has not yet been verified.
- Rust/MSVC toolchain has not yet been installed and verified.

See `docs/qualification/M0_WINDOWS_OLLAMA_QUALIFICATION.md` for the detailed qualification record.

## Target hardware currently declared

- RAM: 32 GB
- GPU: AMD Radeon RX 6750 XT
- VRAM: 12 GB
- CUDA instructions are not applicable to this target GPU.

## Architecture status

The original React + Tauri + Python/FastAPI proposal is no longer the preferred starting architecture.

Current provisional M0/M1 recommendation:

- Tauri 2 desktop shell;
- React + TypeScript frontend;
- Rust/Tauri application core;
- SQLite + FTS5 for authoritative local persistence and textual search;
- direct local HTTP integration with Ollama;
- no mandatory Python/FastAPI runtime for M0/M1;
- Python may remain a development tool or become an optional sidecar later only if a concrete feature justifies the packaging cost;
- vector search remains deferred until the structured-memory foundation is working.

This recommendation remains provisional until the required Windows/Tauri toolchain is installed and a minimal desktop skeleton is built successfully.

## Development status

No production application feature code exists yet.

Repository governance is in PR #1. M0 environment qualification is partially complete.

## Acceptance rule

A milestone may only be marked complete after:

- its code exists;
- its tests have been executed;
- the observed result is recorded;
- known failures are documented;
- the next dependent milestone is not started on an unverified assumption.
