# Fabulaxiom — Next Authorized Work

## Current subdivision

**M1.1 — SQLite foundation and migration runner**

Status: **IMPLEMENTATION PREPARED — LOCK + WINDOWS QUALIFICATION REQUIRED**

## Immediate sequence

1. fetch the exact M1.1 branch head on the target Windows machine;
2. resolve the new `rusqlite` dependency and update only `src-tauri/Cargo.lock`;
3. run frontend tests and production build;
4. run Rust tests;
5. run Cargo check;
6. launch Fabulaxiom;
7. use `Vérifier la base locale`;
8. record the database path, schema version and foreign-key state;
9. prove the database path is outside the repository and installation directory;
10. prove the database status path does not require Ollama;
11. commit only the intended dependency-lock change;
12. push the exact branch head;
13. restore/enforce deterministic `--locked` CI;
14. require exact-head CI success before M1.1 completion.

## Not authorized

Do not yet implement:

- full Universe/Series/Novel/Chapter/Scene CRUD;
- text revision history UI;
- backup/restore UI;
- FTS search;
- embeddings/vector search;
- manuscript generation;
- automatic canonical-fact extraction.
