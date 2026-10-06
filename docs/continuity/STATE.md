# Fabulaxiom — Current State

## Repository

- Repository: `LaurentCOLL1/Fabulaxiom`
- Visibility: private
- Default branch: `main`
- Current working branch: `feat/m0-tauri-skeleton-20261006`
- Current phase: M0 desktop skeleton and local-integration qualification

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
- Ollama previously qualified at `0.35.1`; after restart on 2026-10-06 the local API reported `0.40.0`
- Ollama local HTTP API reachable
- GPU: AMD Radeon RX 6750 XT
- active Ollama compute backend: Vulkan
- Ollama observed 12.0 GiB GPU memory
- qwen3.5:9b real generation completed with 100% GPU reported

Detailed evidence remains in:
`docs/qualification/M0_WINDOWS_OLLAMA_QUALIFICATION.md`.

## M0 desktop skeleton qualification — 2026-10-06

The first Fabulaxiom executable skeleton has now been tested on the target Windows machine.

Observed:

- exact branch head before test:
  `cc9626c54e00787aa97e3e02af5491d4faed78f6`
- `npm install`: PASS
- npm audit result: 0 vulnerabilities
- `npm run build`: PASS
- Vite production build: PASS
- `npm run tauri dev`: PASS
- Rust/Tauri compile: PASS
- `target\debug\fabulaxiom.exe` launched successfully
- frontend button `Tester le pont Rust` returned:
  - `PASS`
  - `Fabulaxiom`
  - `M0 desktop skeleton`
  - `React -> Tauri -> Rust operational`

Therefore the React → Tauri → Rust bridge is **QUALIFIED** on the target machine.

Detailed evidence:
`docs/qualification/M0_DESKTOP_SKELETON_QUALIFICATION.md`.

## Architecture status

Current M0/M1 architecture:

- Tauri 2 desktop shell
- React + TypeScript frontend
- Rust/Tauri application core
- SQLite + FTS5 for authoritative local persistence and textual search
- direct local HTTP integration with Ollama
- no mandatory Python/FastAPI runtime for M0/M1
- Python remains available for development tooling or a future optional sidecar if justified
- vector search remains deferred until the structured-memory foundation works

The executable desktop architecture is now proven on the target machine.

ADR-007 remains provisional until M0 also proves:
- read-only Ollama communication from inside the application
- automated frontend/Rust checks and CI

## Security gate before Ollama application integration

Loopback remediation has started.

Operator-observed evidence now confirms:

- user-level `OLLAMA_HOST`: `127.0.0.1:11434`
- machine-level `OLLAMA_HOST`: not defined
- Ollama was restarted after applying the user-level value
- local API responded successfully on `http://127.0.0.1:11434/api/version`
- the restarted API reported Ollama `0.40.0`

The first listener-verification method using `Get-NetTCPConnection` returned no matching CIM object even though the HTTP request had just succeeded. This is treated as **inconclusive listener evidence**, not as proof of a network failure.

The loopback gate remains open until an independent socket check confirms that no `0.0.0.0:11434` / `[::]:11434` listener exists.

## Known non-blocking environment warnings

- Ollama AMD-driver warning while Vulkan inference still works
- potentially incompatible external `ggml-base.dll` in PATH
- two corrupt Ollama manifests

These warnings remain recorded and must not be silently erased.

## Development status

- PR #1: COMPLETE + MERGED
- PR #2: active M0 desktop qualification
- desktop skeleton: PASS on target Windows machine
- next required operator action: bind Ollama to loopback and verify it

## Acceptance rule

A milestone may only be marked complete after:

- its code exists;
- its tests have been executed;
- the observed result is recorded;
- known failures are documented;
- the next dependent milestone is not started on an unverified assumption.
