# Fabulaxiom — Next Authorized Work

## Immediate objective

Run terminal deterministic M0 CI with the committed dependency lockfiles.

## Terminal CI contract

The workflow must enforce:

1. `npm ci`;
2. `cargo test --locked`;
3. `cargo check --locked`;
4. no mutation of `package-lock.json` or `src-tauri/Cargo.lock`.

If the exact-head workflow is fully `completed/success`:

1. record terminal SHA and run ID;
2. mark M0 `COMPLETE`;
3. mark PR #2 ready;
4. merge PR #2 with expected-head protection;
5. re-fetch live `main`;
6. normalize continuity documents post-merge;
7. only then authorize M1.

## Deliberately deferred

Do not yet add:

- SQLite persistence;
- Universe/Series/Novel/Chapter/Scene CRUD;
- manuscript generation;
- Python/FastAPI runtime service;
- vector database;
- rich-text editor;
- embedding downloads;
- cloud synchronization.
