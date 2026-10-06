# Fabulaxiom — Next Authorized Work

## Immediate objective

Finish M0 prerequisite qualification for the provisional Tauri 2 + React/TypeScript + Rust architecture.

## Already verified

- Git is installed and operational.
- Python 3.12.4 is installed.
- Node.js 24.16.0 and npm 11.11.0 are installed.
- Ollama 0.35.1 is installed.
- Ollama has an installed local-model inventory.
- `qwen3.5:9b` successfully generated text.
- `ollama ps` reported `100% GPU` repeatedly with a `65536` context window.

## Manual checks still required on the Windows machine

1. Force visible output from the Ollama local HTTP API.
2. Force visible GPU/driver output from Windows.
3. Inspect the recent Ollama server log to identify the actual GPU backend if the log exposes it.
4. Verify Microsoft C++ Build Tools / MSVC availability.
5. Install Rust through rustup and select the stable MSVC toolchain.
6. Verify `rustc`, `cargo` and `rustup show active-toolchain`.

## Architecture qualification gate

Only after the toolchain checks above pass:

1. create the initial Tauri 2 + React/TypeScript executable skeleton;
2. prove that it launches on the target Windows machine;
3. add a minimal Rust command callable from the frontend;
4. prove local read-only communication with the Ollama HTTP API;
5. add automated frontend/Rust tests and GitHub CI;
6. then freeze the M0/M1 architecture decision.

## Deliberately deferred

Do not yet:

- add a Python/FastAPI runtime service;
- commit to a vector database;
- commit to a rich-text editor;
- download an embeddings model automatically;
- design cloud synchronization;
- add online services;
- treat any AI-generated fact as canonical;
- implement advanced generation before the persistence model is reliable.
