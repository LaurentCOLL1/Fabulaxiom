# Fabulaxiom — Next Authorized Work

## Immediate objective

Secure Ollama's network binding, then add read-only Ollama integration to the already-qualified Fabulaxiom desktop skeleton.

## Already qualified

- Windows/Tauri prerequisites: PASS
- React/TypeScript production build: PASS
- Tauri/Rust compilation: PASS
- Fabulaxiom desktop launch: PASS
- React → Tauri → Rust command bridge: PASS

## Required operator step before Ollama integration

Ollama currently listens on:

`0.0.0.0:11434`

This exposes the server beyond loopback.

Before Fabulaxiom may connect to Ollama, rebind the Ollama server to:

`127.0.0.1:11434`

Then verify:

1. the user-level `OLLAMA_HOST` value;
2. Ollama restarts successfully;
3. `http://127.0.0.1:11434/api/version` responds;
4. Windows shows the listener on loopback rather than `0.0.0.0`;
5. a real local model still runs with GPU acceleration.

## After the loopback gate passes

The next code change is authorized to add:

1. a Rust-side read-only Ollama client;
2. a Tauri command returning:
   - availability;
   - Ollama version;
   - configured local endpoint;
3. a frontend status panel;
4. strict timeout/error handling;
5. no cloud endpoint and no manuscript transmission.

Then add automated frontend/Rust tests and GitHub CI.

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
