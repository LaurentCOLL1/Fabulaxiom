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

The desired user-level setting is now present:

`OLLAMA_HOST=127.0.0.1:11434`

and the restarted local API returned Ollama `0.40.0`.

Remaining loopback qualification:

1. verify the actual listener with an independent socket inspection method;
2. reject any `0.0.0.0:11434` or `[::]:11434` listener;
3. confirm a loopback listener on `127.0.0.1:11434` or `[::1]:11434`;
4. confirm a real local model still runs with GPU acceleration.

Do not treat the failed `Get-NetTCPConnection` lookup as proof that Ollama is unavailable because the HTTP API request succeeded immediately beforehand.

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
