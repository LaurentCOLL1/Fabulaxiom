# Fabulaxiom — Current State

## Repository

- Repository: `LaurentCOLL1/Fabulaxiom`
- Visibility: private
- Default branch: `main`
- Current working branch: `feat/m0-tauri-skeleton-20261006`
- Current phase: M0 COMPLETE, pending PR merge and post-merge normalization

## M0 status

**M0 — Environment and architecture qualification: COMPLETE**

Terminal implementation/CI qualification:

- exact SHA: `6fbea03be2b6058aa14d1cddcaffc7f840ebf81c`;
- workflow: `M0 CI`;
- run: `37561269046`;
- result: `completed/success`.

The deterministic CI contract passed:

- `npm ci`: PASS;
- frontend tests: PASS;
- frontend production build: PASS;
- `cargo test --locked`: PASS;
- `cargo check --locked`: PASS;
- dependency lockfiles unchanged: PASS.

## Operator qualification

Target Windows execution is PASS for:

- exact source checkout;
- React/TypeScript build;
- Tauri/Rust compile and launch;
- React → Tauri → Rust command bridge;
- read-only Rust → Ollama 0.40.0 status integration;
- frontend tests;
- Rust tests;
- cargo check.

Observed application results:

```text
PASS
Fabulaxiom
M0 desktop skeleton
React -> Tauri -> Rust operational
```

```text
PASS
Ollama 0.40.0 disponible sur http://127.0.0.1:11434
```

## Reproducibility

Committed:

- `package-lock.json` — lockfileVersion 3;
- `src-tauri/Cargo.lock` — lockfile version 4.

CI is locked to those dependency graphs.

## Architecture

ADR-007: **Accepted**

M0/M1 architecture:

- Tauri 2 desktop shell;
- React + TypeScript frontend;
- Rust/Tauri application core;
- SQLite + FTS5 planned for M1 authoritative persistence/search;
- direct local Ollama HTTP integration;
- no mandatory Python/FastAPI runtime for M0/M1.

## Ollama security

Security gate: **PASS**

- Ollama Desktop network exposure: OFF;
- `OLLAMA_HOST=127.0.0.1:11434`;
- Ollama 0.40.0;
- listener loopback-only;
- tested non-loopback local interfaces unavailable;
- active compute backend: Vulkan;
- GPU: AMD Radeon RX 6750 XT.

## Known non-blocking environment warnings

- Ollama AMD-driver warning while Vulkan inference works;
- potentially incompatible external `ggml-base.dll` in PATH;
- two corrupt Ollama manifests.

These warnings remain recorded.

## Development status

- PR #1: COMPLETE + MERGED;
- PR #2: M0 COMPLETE, pending final docs-head CI and merge;
- M1: NOT AUTHORIZED until PR #2 is merged and post-merge continuity normalization is complete.

## Acceptance rule

No dependent milestone starts before the completed milestone is merged and normalized on live `main`.
