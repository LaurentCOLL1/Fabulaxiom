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

Verified on the target Windows machine:

- Git: `2.55.0.windows.3`.
- Python: `3.12.4`.
- Node.js: `24.16.0`.
- npm: `11.11.0`.
- Rustup: `1.29.1`.
- Rust compiler: `rustc 1.99.0`.
- Cargo: `1.99.0`.
- Active Rust toolchain: `stable-x86_64-pc-windows-msvc`.
- Microsoft C++ Build Tools: found at `C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools`.
- Microsoft Edge WebView2 Runtime: `154.0.4258.53`.
- Ollama: `0.35.1`.
- Ollama local HTTP API: reachable and returned version `0.35.1`.
- GPU: AMD Radeon RX 6750 XT.
- AMD driver reported by Windows: `32.0.21045.5002`.
- Ollama GPU backend: **Vulkan**.
- Ollama detected `12.0 GiB` total GPU memory.
- `qwen3.5:9b` loaded with 34/34 model layers offloaded to the GPU.
- Repeated `ollama ps` observations reported `100% GPU` with context `65536`.
- A French long-form generation completed successfully.

### Non-blocking environment warnings recorded

- Ollama logs report: `AMD driver is too old. Update your AMD driver to enable GPU inference.`
  - Despite this warning, the active Vulkan backend successfully performs GPU inference.
  - Do not interpret this warning as proof that the currently working Vulkan path is failing.
- Ollama reports a potentially incompatible `ggml-base.dll` found in the user's PATH under a WinGet llama.cpp package.
- Ollama reports corrupt manifests for:
  - `Claude-Fable5:MiniCPM5-1B-Claude-Opus-Fable5-Thinking-Q8_0.gguf`
  - `llama-mesh:LLaMA-Mesh-Q5_K_S.gguf`
- These warnings do not currently block the verified `qwen3.5:9b` Vulkan inference path.
- The `Win32_VideoController.AdapterRAM` value is not used as authoritative VRAM evidence because the Ollama runtime directly reports 12.0 GiB for the active GPU.

See `docs/qualification/M0_WINDOWS_OLLAMA_QUALIFICATION.md` for the detailed qualification record.

## Architecture status

Current provisional M0/M1 recommendation:

- Tauri 2 desktop shell;
- React + TypeScript frontend;
- Rust/Tauri application core;
- SQLite + FTS5 for authoritative local persistence and textual search;
- direct local HTTP integration with Ollama;
- no mandatory Python/FastAPI runtime for M0/M1;
- Python may remain a development tool or become an optional sidecar later only if a concrete feature justifies the packaging cost;
- vector search remains deferred until the structured-memory foundation is working.

All required local prerequisites for attempting the first Tauri skeleton are now present. The architecture remains provisional until a minimal desktop application successfully builds and launches on the target machine.

## Development status

Repository governance and M0 prerequisite qualification are in PR #1.

The next legitimate step is the first executable Tauri skeleton.

## Acceptance rule

A milestone may only be marked complete after:

- its code exists;
- its tests have been executed;
- the observed result is recorded;
- known failures are documented;
- the next dependent milestone is not started on an unverified assumption.
