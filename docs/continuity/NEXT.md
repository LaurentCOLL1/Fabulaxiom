# Fabulaxiom — Next Authorized Work

## Current milestone

**M1 — Persistence and project foundation**

## Current subdivision

**M1.2 — Project hierarchy schema**

Status:

**WINDOWS QUALIFIED — TERMINAL CI + MERGE REQUIRED**

## Completed qualification

Implementation SHA:

`3d4b2eaf95e13bfa93580a4295ac20e93a076798`

Deterministic CI:

- run `37644123751`;
- completed/success;
- 13 Rust tests PASS;
- frontend tests/build PASS;
- lockfiles unchanged.

Windows qualification:

- schema-v1 production database backed up;
- production migration v1 → v2 PASS;
- migrations 1 + 2 PASS;
- hierarchy tables 5/5 PASS;
- STRICT 5/5 PASS;
- immutable-ID triggers 5/5 PASS;
- foreign keys ON;
- foreign-key check empty;
- integrity check OK;
- final worktree clean.

## Immediate sequence

1. commit the Windows qualification evidence;
2. require Fabulaxiom CI on that new exact head;
3. if every deterministic check is successful, merge PR #9 with expected-head protection;
4. re-fetch live `main`;
5. create and qualify M1.2 post-merge normalization;
6. merge normalization;
7. only then authorize M1.3.

## M1.3 remains unauthorized

Do not yet implement:

- hierarchy CRUD services;
- hierarchy editing UI;
- text revision history;
- backup/restore;
- FTS;
- embeddings;
- manuscript generation;
- canonical-fact extraction.
