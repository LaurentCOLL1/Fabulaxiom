# Fabulaxiom — Next Authorized Work

## Current subdivision

**M1.1 — SQLite foundation and migration runner**

Status:

**QUALIFIED — FINAL EXACT-HEAD CI + MERGE REQUIRED**

## Qualified

- Windows implementation qualification: PASS
- SQLite schema/migration evidence: PASS
- dependency lock committed: PASS
- exact-head CI on `59923690d08687efd42b452e3e29976131a4be8b`: PASS
- CI run `37636677552`: `completed/success`

## Immediate sequence

1. commit the recorded qualification evidence;
2. run Fabulaxiom CI on that new exact head;
3. require every deterministic check to pass;
4. merge PR #5 with expected-head protection;
5. re-fetch live `main`;
6. create post-merge continuity normalization;
7. require normalization CI success;
8. merge normalization;
9. only then authorize M1.2.

## Not authorized

Do not yet implement:

- full Universe/Series/Novel/Chapter/Scene CRUD;
- text revision history UI;
- backup/restore UI;
- FTS search;
- embeddings/vector search;
- manuscript generation;
- automatic canonical-fact extraction.
