# Fabulaxiom — Current State

## Repository

- Repository: `LaurentCOLL1/Fabulaxiom`
- Visibility: private
- Default branch: `main`
- Current working branch: `feat/m0-tauri-skeleton-20261006`
- Current phase: M0 terminalization

## Product identity

- Product name: **Fabulaxiom**
- Internal/package naming convention: `fabulaxiom`
- Name intent: `fabula` (story/narrative) + `axiom` (foundational truth)

## Confirmed product principles

Fabulaxiom is a local-first application for long-form fiction, novels, sagas and shared fictional universes.

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

## M0 prerequisite qualification

Verified on the target Windows machine:

- Git: `2.55.0.windows.3`
- Python: `3.12.4`
- Node.js: `24.16.0`
- npm: `11.11.0`
- Rustup: `1.29.1`
- Rust compiler: `1.99.0`
- Cargo: `1.99.0`
- active Rust toolchain: `stable-x86_64-pc-windows-msvc`
- Microsoft C++ Build Tools present
- Microsoft Edge WebView2 Runtime present
- Ollama: `0.40.0`
- Ollama local HTTP API reachable
- GPU: AMD Radeon RX 6750 XT
- active Ollama compute backend: Vulkan
- Ollama observed 12.0 GiB GPU memory
- qwen3.5:9b real generation completed with 100% GPU reported

Detailed prerequisite evidence:
`docs/qualification/M0_WINDOWS_OLLAMA_QUALIFICATION.md`.

## M0 desktop and local-integration qualification

The executable Fabulaxiom stack is now operator-qualified on the target Windows machine.

Latest exact source SHA tested locally:

`fe43c7dd859fda77628e569834a243e6ade21806`

Observed on that exact SHA:

- exact HEAD check: PASS
- generated `src-tauri/gen/` correctly ignored by Git: PASS
- Ollama local API `0.40.0`: PASS
- `npm install`: PASS
- npm audit: 0 vulnerabilities
- frontend Vitest suite: 2/2 PASS
- `npm run build`: PASS
- Vite production build: PASS
- Rust unit tests: 2/2 PASS
- `cargo check`: PASS
- `npm run tauri dev`: PASS
- `target\debug\fabulaxiom.exe` launched successfully
- frontend button `Tester le pont Rust`: PASS
- frontend button `Vérifier Ollama local`: PASS
- observed Ollama status:
  `Ollama 0.40.0 disponible sur http://127.0.0.1:11434`

No manuscript, prompt or narrative content is transmitted by the M0 Ollama status path.

Detailed evidence:
`docs/qualification/M0_DESKTOP_SKELETON_QUALIFICATION.md`.

## Exact-head GitHub CI

For exact head:

`fe43c7dd859fda77628e569834a243e6ade21806`

GitHub Actions:

- workflow: `M0 CI`
- run: `37542052212`
- result: `completed/success`
- frontend tests: PASS
- frontend production build: PASS
- Rust tests: PASS
- Rust check: PASS
- dependency-lock artifact generation: PASS

## Architecture status

ADR-007 is now **Accepted**.

M0/M1 architecture:

- Tauri 2 desktop shell
- React + TypeScript frontend
- Rust/Tauri application core
- SQLite + FTS5 for authoritative local persistence and textual search
- direct local HTTP integration with Ollama
- no mandatory Python/FastAPI runtime for M0/M1
- Python remains available for development tooling or a future optional sidecar if justified
- vector search remains deferred until the structured-memory foundation works

This architecture is proven by both operator execution and exact-head CI.

## Ollama loopback security gate

The Ollama network-security gate is **PASS**.

Final operator-observed evidence:

- user-level `OLLAMA_HOST`: `127.0.0.1:11434`
- machine-level `OLLAMA_HOST`: not defined
- local API version: `0.40.0`
- Windows listener: `127.0.0.1:11434`
- current server log: `Listening on 127.0.0.1:11434 (version 0.40.0)`
- all tested non-loopback local interfaces: not accessible

The former all-interface exposure was caused by Ollama Desktop's **Expose Ollama to the network** setting and has been corrected.

## Known non-blocking environment warnings

- Ollama AMD-driver warning while Vulkan inference works
- potentially incompatible external `ggml-base.dll` in PATH
- two corrupt Ollama manifests

These warnings remain recorded and must not be silently erased.

## M0 terminalization status

Functional and security acceptance is **PASS**.

M0 is not marked `COMPLETE` yet because dependency lockfiles still need to be committed:

- `package-lock.json`
- `src-tauri/Cargo.lock`

After those lockfiles are committed, CI must use the committed locks deterministically and pass on the terminal exact head before PR #2 is merged.

## Development status

- PR #1: COMPLETE + MERGED
- PR #2: active, M0 terminalization
- architecture: ACCEPTED
- local functional qualification: PASS
- Ollama security gate: PASS
- exact-head CI on pre-lock terminal candidate: PASS
- remaining: commit dependency locks, deterministic final CI, merge/normalize M0

## Acceptance rule

A milestone may only be marked complete after:

- its code exists;
- its tests have been executed;
- the observed result is recorded;
- known failures are documented;
- reproducibility inputs are versioned;
- terminal exact-head CI passes;
- the next dependent milestone is not started on an unverified assumption.
