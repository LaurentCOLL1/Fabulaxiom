# Fabulaxiom — Current State

## Repository

- Repository: `LaurentCOLL1/Fabulaxiom`
- Visibility: private
- Default branch: `main`
- Current working branch: `feat/m0-tauri-skeleton-20261006`
- Current phase: M0 terminal deterministic qualification

## M0 acceptance summary

- Windows/Tauri prerequisites: PASS
- React/TypeScript build: PASS
- Tauri/Rust compile and launch: PASS
- React → Tauri → Rust bridge: PASS
- Ollama loopback security gate: PASS
- read-only Rust → Ollama 0.40.0 status check: PASS
- frontend tests: PASS
- Rust tests: PASS
- cargo check: PASS
- ADR-007 architecture: ACCEPTED

## Reproducibility inputs

Committed lockfiles:

- `package-lock.json`
  - name: `fabulaxiom`
  - version: `0.1.0`
  - lockfileVersion: `3`
  - root package entry present
- `src-tauri/Cargo.lock`
  - lockfile version: `4`
  - `cargo metadata --locked`: PASS

Lockfile commit:

`f875cb98fcec818fea856d502ae89375b3793712`

## Architecture

Accepted M0/M1 architecture:

- Tauri 2 desktop shell
- React + TypeScript frontend
- Rust/Tauri application core
- SQLite + FTS5 planned for M1
- direct local Ollama integration
- no mandatory Python/FastAPI runtime for M0/M1

## Ollama security

- `OLLAMA_HOST=127.0.0.1:11434`
- Ollama version: `0.40.0`
- listener: loopback only
- tested non-loopback local interfaces: not accessible
- active GPU backend: Vulkan on AMD Radeon RX 6750 XT

## Known non-blocking environment warnings

- Ollama AMD-driver warning while Vulkan inference works
- potentially incompatible external `ggml-base.dll` in PATH
- two corrupt Ollama manifests

## M0 terminalization status

Functional acceptance: PASS  
Security acceptance: PASS  
Architecture acceptance: PASS  
Dependency lockfiles committed: PASS

Remaining gate: terminal deterministic CI must pass on the exact current head using:

- `npm ci`
- Cargo `--locked`
- lockfile mutation check

M0 is not `COMPLETE` until that terminal exact-head CI passes.

## Development status

- PR #1: COMPLETE + MERGED
- PR #2: active, M0 terminal deterministic qualification
- M1: NOT AUTHORIZED
