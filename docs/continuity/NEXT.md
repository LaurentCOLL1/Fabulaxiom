# Fabulaxiom — Next Authorized Work

## Immediate objective

Secure Ollama's network binding, then add read-only Ollama integration to the already-qualified Fabulaxiom desktop skeleton.

## Already qualified

- Windows/Tauri prerequisites: PASS
- React/TypeScript production build: PASS
- Tauri/Rust compilation: PASS
- Fabulaxiom desktop launch: PASS
- React → Tauri → Rust command bridge: PASS

## Ollama loopback security gate

The security gate is **PASS**.

Ollama 0.40.0 is bound to `127.0.0.1:11434`, and all tested non-loopback local interfaces are unable to connect.

## Next authorized implementation

The current branch is authorized to add:

1. a Rust-side read-only Ollama client fixed to `127.0.0.1:11434`;
2. a Tauri command returning availability, version and endpoint;
3. a frontend Ollama status panel;
4. strict timeout, no redirect and no proxy behavior;
5. frontend and Rust unit tests;
6. Windows GitHub CI.

Acceptance requires both:
- local operator test on the target PC;
- exact-head GitHub CI success.

No manuscript content may be transmitted during this milestone.

## Deliberately deferred

Do not yet:

- add generation from manuscripts;
- add SQLite persistence;
- add a Python/FastAPI runtime service;
- commit to a vector database;
- commit to a rich-text editor;
- download an embeddings model automatically;
- design cloud synchronization;
- treat any AI-generated fact as canonical.
