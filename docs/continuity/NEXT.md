# Fabulaxiom — Next Authorized Work

## Immediate objective

Create and qualify the first executable Fabulaxiom desktop skeleton.

## M0 prerequisites now verified

- Git installed and operational.
- Python 3.12.4 installed.
- Node.js 24.16.0 and npm 11.11.0 installed.
- Microsoft C++ Build Tools present.
- Microsoft Edge WebView2 Runtime present.
- Rustup 1.29.1 installed.
- Rust 1.99.0 / Cargo 1.99.0 installed.
- Active Rust toolchain is `stable-x86_64-pc-windows-msvc`.
- Ollama 0.35.1 installed.
- Ollama HTTP API reachable.
- AMD Radeon RX 6750 XT detected.
- Ollama active compute backend identified as Vulkan.
- Real local generation proven with GPU acceleration.

## Architecture qualification gate

Next sequence:

1. create the initial Tauri 2 + React/TypeScript executable skeleton;
2. prove that it launches on the target Windows machine;
3. add a minimal Rust command callable from the frontend;
4. prove local read-only communication with the Ollama HTTP API;
5. add automated frontend/Rust tests and GitHub CI;
6. only then mark ADR-007 accepted and complete M0.

## Known non-blocking issues to retain

- Ollama AMD-driver warning;
- potentially incompatible external `ggml-base.dll` in PATH;
- two corrupt Ollama manifests;
- these issues must be handled separately and must not be silently erased from project state.

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
