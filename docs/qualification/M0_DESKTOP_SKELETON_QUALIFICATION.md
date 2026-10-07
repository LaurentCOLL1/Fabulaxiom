# M0 Desktop and Local Integration Qualification — 2026-10-07

## Decision

**M0 COMPLETE**

## Scope

Qualified execution path:

`React -> Tauri -> Rust -> local Ollama status API`

M0 does not include SQLite persistence, narrative-memory features, or manuscript generation.

## Local operator qualification

Latest executable source tested locally:

`fe43c7dd859fda77628e569834a243e6ade21806`

PASS:

- exact repository/head integrity;
- generated Tauri schemas ignored correctly;
- Ollama 0.40.0 loopback API;
- frontend unit tests 2/2;
- frontend production build;
- Rust unit tests 2/2;
- cargo check;
- Tauri desktop launch;
- React → Tauri → Rust bridge;
- read-only local Ollama status check.

Observed:

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

## Security qualification

PASS:

- `OLLAMA_HOST=127.0.0.1:11434`;
- current listener loopback-only;
- non-loopback local interfaces inaccessible;
- no manuscript/prompt transmission in M0 status path.

## Reproducibility qualification

Committed lockfiles:

- `package-lock.json`;
- `src-tauri/Cargo.lock`.

Lockfile commit:

`f875cb98fcec818fea856d502ae89375b3793712`

Terminal deterministic implementation head:

`6fbea03be2b6058aa14d1cddcaffc7f840ebf81c`

GitHub Actions:

- workflow: `M0 CI`;
- run: `37561269046`;
- result: `completed/success`.

Validated:

- `npm ci`;
- frontend tests;
- frontend production build;
- `cargo test --locked`;
- `cargo check --locked`;
- lockfiles remained unchanged.

## Architecture acceptance

ADR-007 is **Accepted** for M0/M1:

- Tauri 2;
- React + TypeScript;
- Rust/Tauri core;
- SQLite + FTS5 planned for M1;
- direct local Ollama integration;
- no mandatory Python/FastAPI runtime.

## Completion boundary

M0 is functionally and deterministically complete.

M1 remains unauthorized until M0 is merged to `main` and post-merge continuity normalization is completed.
