# Fabulaxiom — Current State

## Repository

- Repository: `LaurentCOLL1/Fabulaxiom`
- Visibility: private
- Default branch: `main`

## Milestone state

### M0 — Environment and architecture qualification

**COMPLETE + MERGED + NORMALIZED**

Authoritative evidence:

- PR #2: merged
- M0 merge commit: `dae2c4e45536180caab564ac9b7e5493fd9c044b`
- final PR head: `1692c514753eaf0a89284943e74c4e757cb9abbc`
- final PR CI run: `37562085953` — `completed/success`
- deterministic implementation CI:
  - SHA `6fbea03be2b6058aa14d1cddcaffc7f840ebf81c`
  - run `37561269046`
  - `completed/success`
- architecture ADR-007: ACCEPTED
- operator Windows qualification: PASS
- Ollama loopback security gate: PASS
- dependency locks committed and deterministic: PASS
- post-merge continuity baseline commit: `5a822ae7803a8711f97f7c8920cc441ab2aea2c2`

M0 is closed. No further M0 feature work is authorized.

### M1 — Persistence and project foundation

**AUTHORIZED — M1.1 ONLY**

Detailed authority:

`docs/roadmap/M1_PERSISTENCE_PROJECT_FOUNDATION.md`

Current authorized subdivision:

**M1.1 — SQLite foundation and migration runner**

Later M1 subdivisions remain unauthorized until M1.1 is merged and normalized.

## Accepted architecture

- Tauri 2 desktop shell
- React + TypeScript frontend
- Rust/Tauri application core
- SQLite + FTS5 for authoritative persistence/search
- direct local Ollama integration
- no mandatory Python/FastAPI runtime for M0/M1

## Reproducibility contract

- `package-lock.json` is committed
- `src-tauri/Cargo.lock` is committed
- CI uses `npm ci`
- Rust CI uses Cargo `--locked`
- lockfile mutation is rejected in CI

## Known non-blocking environment warnings

- Ollama AMD-driver warning while Vulkan inference works
- potentially incompatible external `ggml-base.dll` in PATH
- two corrupt Ollama manifests

These remain documented and do not block M1.1.

## Governance rule

Every subdivision must:

- begin from freshly fetched live `main`;
- use a dedicated branch and pull request;
- preserve deterministic dependency locks;
- pass exact-head CI;
- receive required Windows operator qualification when local behavior is part of acceptance;
- be merged and normalized before a dependent subdivision begins.
