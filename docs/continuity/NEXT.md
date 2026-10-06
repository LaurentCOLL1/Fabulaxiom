# Fabulaxiom — Next Authorized Work

## Immediate objective

Finish M0 terminalization. Do not start M1 yet.

## Qualified

- Windows/Tauri prerequisites: PASS
- React/TypeScript production build: PASS
- Tauri/Rust compilation: PASS
- Fabulaxiom desktop launch: PASS
- React → Tauri → Rust bridge: PASS
- Ollama loopback security gate: PASS
- read-only Rust → Ollama local API integration: PASS
- frontend Ollama status panel: PASS
- frontend tests: PASS
- Rust tests: PASS
- cargo check: PASS
- exact-head GitHub CI on `fe43c7dd859fda77628e569834a243e6ade21806`: PASS
- ADR-007 architecture decision: ACCEPTED

## Remaining M0 terminalization

Exactly two generated dependency locks remain to be versioned:

- `package-lock.json`
- `src-tauri/Cargo.lock`

They were generated successfully both locally and in GitHub CI.

After they are committed:

1. change CI frontend installation from `npm install` to `npm ci`;
2. run Cargo validation with `--locked`;
3. require terminal exact-head CI success;
4. record the terminal SHA and CI run;
5. mark M0 `COMPLETE`;
6. merge PR #2;
7. re-fetch `main`;
8. normalize continuity documents on `main`;
9. only then authorize M1.

## Deliberately deferred until M0 merge

Do not yet:

- add SQLite persistence;
- add project/universe CRUD;
- add generation from manuscripts;
- add a Python/FastAPI runtime service;
- commit to a vector database;
- commit to a rich-text editor;
- download an embeddings model automatically;
- design cloud synchronization;
- treat any AI-generated fact as canonical.
