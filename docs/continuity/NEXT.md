# Fabulaxiom — Next Authorized Work

## Immediate objective

Complete the technical bootstrap before implementing product features.

## Required sequence

1. Verify the local development environment on Windows:
   - Git;
   - Python;
   - Node.js;
   - Rust/Cargo if Tauri remains a candidate;
   - Ollama version;
   - Ollama listening endpoint;
   - installed model inventory;
   - actual Ollama compute backend and observed GPU use on the AMD Radeon RX 6750 XT.

2. Decide the first architecture after comparison of:
   - desktop Tauri + frontend + packaged Python backend;
   - desktop Tauri with fewer backend boundaries;
   - local web application with Python backend;
   - any simpler architecture that preserves local-first constraints.

3. Freeze only the architecture needed for Milestone M0/M1.

4. Create the initial executable skeleton.

5. Add automated tests before moving into narrative-memory features.

## Manual evidence expected from the Windows machine

The user will run the requested PowerShell commands locally and provide their outputs. Do not claim that hardware, Ollama acceleration or packaging works until those outputs are observed.

## Not authorized yet

Do not yet:

- commit to a vector database;
- commit to a rich-text editor;
- download an embeddings model automatically;
- design cloud synchronization;
- add online services;
- treat any AI-generated fact as canonical;
- implement advanced generation before the persistence model is reliable.
