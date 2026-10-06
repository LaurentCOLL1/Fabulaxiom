# M0 Desktop and Local Integration Qualification — 2026-10-07

## Scope

This qualification proves the initial executable Fabulaxiom desktop foundation:

`React -> Tauri -> Rust -> local Ollama status API`

It does not qualify SQLite, manuscript persistence, narrative-memory features or text generation from user content.

## Repository

Repository:
`LaurentCOLL1/Fabulaxiom`

Branch:
`feat/m0-tauri-skeleton-20261006`

Latest exact source SHA tested locally:
`fe43c7dd859fda77628e569834a243e6ade21806`

## Operator-observed qualification on the exact SHA

### Repository integrity

- origin:
  `https://github.com/LaurentCOLL1/Fabulaxiom.git`
- exact expected source SHA matched local HEAD
- generated Tauri directory `src-tauri/gen/` was correctly ignored
- result: **PASS**

### Ollama local API

Observed:

```json
{
  "version": "0.40.0"
}
```

Endpoint:

`http://127.0.0.1:11434`

Result: **PASS**

### JavaScript dependencies

`npm install`

Observed:

- installation completed successfully
- 0 vulnerabilities

Result: **PASS**

### Frontend unit tests

`npm run test:ci`

Observed:

- test files: 1 passed
- tests: 2 passed
- failures: 0

Result: **PASS**

### Frontend production build

`npm run build`

Observed:

- TypeScript compile completed
- Vite 8.0.16 production build completed
- 19 modules transformed

Result: **PASS**

### Rust tests

`cargo test --manifest-path src-tauri/Cargo.toml --all-targets`

Observed:

- `ollama_version_response_deserializes`: PASS
- `ollama_endpoint_is_fixed_to_ipv4_loopback`: PASS
- Rust tests: 2 passed, 0 failed

Result: **PASS**

### Rust compile validation

`cargo check --manifest-path src-tauri/Cargo.toml`

Result: **PASS**

### Tauri desktop launch

`npm run tauri dev`

Observed:

- Vite dev server started on localhost:1420
- Fabulaxiom Rust crate compiled
- executable started:
  `target\debug\fabulaxiom.exe`

Result: **PASS**

### Frontend to Rust bridge

The operator clicked:

`Tester le pont Rust`

Observed:

```text
PASS
Fabulaxiom
M0 desktop skeleton
React -> Tauri -> Rust operational
```

Result: **PASS**

### Read-only local Ollama integration

The operator clicked:

`Vérifier Ollama local`

Observed:

```text
PASS
Ollama 0.40.0 disponible sur http://127.0.0.1:11434
```

The M0 path sends no manuscript or prompt content. It only queries the local Ollama version endpoint.

Result: **PASS**

## Exact-head GitHub CI

Exact SHA:
`fe43c7dd859fda77628e569834a243e6ade21806`

Workflow:
`M0 CI`

Run:
`37542052212`

Observed:

- frontend install: PASS
- frontend tests: PASS
- frontend production build: PASS
- Rust tests: PASS
- Rust check: PASS
- dependency lock artifact: PASS
- overall result: `completed/success`

## Architecture acceptance

The Tauri 2 + React/TypeScript + Rust/Tauri architecture is **ACCEPTED** for M0/M1.

## Remaining terminalization gate

Functional M0 qualification is complete, but M0 remains open until the two dependency lockfiles are committed and a deterministic final CI passes:

- `package-lock.json`
- `src-tauri/Cargo.lock`

After versioning them, CI must use locked dependency installation/resolution and succeed on the terminal exact head.
