# Fabulaxiom — Current State

## Repository

- Repository: `LaurentCOLL1/Fabulaxiom`
- Visibility: private
- Default branch: `main`
- Live main after M0 merge: `dae2c4e45536180caab564ac9b7e5493fd9c044b`
- Current normalization branch: `docs/m0-post-merge-normalization-20261007`

## Milestone state

### M0 — Environment and architecture qualification

**COMPLETE + MERGED**

- PR #2: merged
- merge commit on `main`: `dae2c4e45536180caab564ac9b7e5493fd9c044b`
- final PR head: `1692c514753eaf0a89284943e74c4e757cb9abbc`
- final PR CI run: `37562085953` — success
- deterministic implementation CI: `37561269046` — success
- architecture ADR-007: ACCEPTED
- operator Windows qualification: PASS
- Ollama loopback security gate: PASS
- dependency locks committed and enforced: PASS

### M1 — Persistence and project foundation

**AUTHORIZED — NOT STARTED**

Detailed plan:
`docs/roadmap/M1_PERSISTENCE_PROJECT_FOUNDATION.md`

First authorized subdivision:

**M1.1 — SQLite foundation and migration runner**

## Accepted architecture

- Tauri 2 desktop shell
- React + TypeScript frontend
- Rust/Tauri application core
- SQLite + FTS5 for authoritative persistence/search
- direct local Ollama integration
- no mandatory Python/FastAPI runtime for M0/M1

## Known non-blocking environment warnings

- Ollama AMD-driver warning while Vulkan inference works
- potentially incompatible external `ggml-base.dll` in PATH
- two corrupt Ollama manifests

These remain documented and do not block M1.1.

## Governance rule

Each subdivision must:

- start from fresh live `main`;
- use a dedicated branch/PR;
- keep dependency locks deterministic;
- pass exact-head CI;
- be merged before the dependent subdivision begins.
