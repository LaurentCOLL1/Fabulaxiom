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

Independent verification has now proven that Ollama is still exposed on all interfaces.

Observed:

- `Get-NetTCPConnection`: `:: :11434`;
- current server log: `OLLAMA_HOST:http://0.0.0.0:11434`;
- current server log: `Listening on [::]:11434`;
- local network address `192.168.1.200:11434`: accessible;
- local adapter address `172.24.96.1:11434`: accessible.

Root cause: the Ollama desktop setting **Expose Ollama to the network** is enabled. In current Ollama source code, that setting explicitly overwrites `OLLAMA_HOST` with `0.0.0.0`.

Required operator sequence:

1. open the Ollama desktop application;
2. open Settings;
3. turn **Expose Ollama to the network** OFF;
4. fully quit Ollama from its tray/taskbar menu;
5. restart Ollama from the Windows Start menu;
6. verify the current log reports a loopback bind and no all-interface bind;
7. verify non-loopback local addresses can no longer connect to port 11434;
8. verify local API and GPU inference still work.

Do not add Ollama client code to Fabulaxiom until this gate passes.

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
