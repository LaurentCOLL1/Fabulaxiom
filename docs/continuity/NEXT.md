# Fabulaxiom — Next Authorized Work

## Completed milestone

**M1 — Persistence and project foundation: COMPLETE + MERGED + NORMALIZED**

M1.1 through M1.5 are qualified, merged, and post-merge normalized.

Final implementation PR:

**#15 — feat: implement M1.5 safe SQLite backup and restore baseline**

Implementation merge:

`282b325fb6c588a70df08a5128415c8fa0a0f72e`

Exact-head implementation evidence SHA:

`152b40e616f40799abc61f9ce8db142e3b19340b`

Terminal `Fabulaxiom CI`:

- run `37720676744`;
- `completed/success`;
- 13/13 frontend and 37/37 Rust PASS;
- frontend build, `cargo check --locked`, dependency locks PASS.

Real Windows qualification:

- clean source and exact Git SHAs;
- SQLite v3 and Tauri bridge PASS;
- Ollama OFF;
- app backup and controlled restore with UI reload PASS;
- 1 Universe, 1 Novel, 1 Scene, 3 revisions, 1 current head retained.

Evidence: `docs/qualification/M1_5_BACKUP_RESTORE_BASELINE.md`.

## Current milestone

**M2 — Narrative entities and canonical facts: IN PROGRESS**

Detailed planning PR: **#17 — docs: plan M2 and authorize M2.1 schema after acceptance**.

Planning merge: `4a9115ec362a0efae696ebc94b5101fa46d7a03a`.

Planning exact SHA: `44669d9070870624b845ab0825ebd555eef0dcbc`.

Terminal `Fabulaxiom CI` run `37722657799`: `completed/success`.

Accepted plan: `docs/roadmap/M2_NARRATIVE_ENTITIES_CANONICAL_FACTS.md`.

## Completed subdivision

**M2.1 — Entity registry schema and migration: COMPLETE + MERGED + NORMALIZED**

Implementation PR: #20.

Implementation merge: `6c58b3bd4f0588436da8ba45adb875f897f426b2`.

Windows-qualified source SHA: `c7a663d88ba2538714d42fdd366719cd54fe6f70`.

Evidence SHA: `88fa3b22904b92d4ecdcb32ed7fd01dc23e24a4c`.

Terminal exact-head `Fabulaxiom CI`: run `37814949619`, `completed/success`, frontend 13/13, Rust 44/44, build/check/lockfiles PASS.

Real Windows v3 → v4 qualification: PASS. Source data/scene revisions/head preserved, migration 1–4, STRICT registry tables, triggers/indexes, foreign keys/integrity PASS, backup and active marker unchanged.

Evidence: `docs/qualification/M2_1_ENTITY_REGISTRY_SCHEMA.md`.

## Completed subdivision — M2.2

**M2.2 — No-AI entity and alias CRUD: COMPLETE + MERGED + NORMALIZED** — takes effect only after this separate normalization PR merges and `main` is re-fetched.

- Implementation PR: **#23**; Windows-qualified source: `b54fffd8e1f0224372e3b99cee07cb6df3203973`.
- Qualified code CI `37831790345` and evidence-head CI `37864503602` on `a96870f823f24cb8962c9b0f43336ccb883ad5c3`: both `completed/success`, exact `pull_request` SHA confirmed.
- Protected implementation merge: `ad7211fa2f292b8bd9812e299dbb6be96214eb89`.
- Real Windows: **13/13 interactive cases**, **21/21 frontend** and **51/51 Rust** tests, `cargo check --locked` / frontend build / lockfiles: PASS; Ollama OFF.
- SQLite v4 after interactive tests: 9 entities, 8 aliases, one duplicate-name character pair with distinct IDs, 3 scene revisions / 1 pointer preserved, valid STRICT/migrations/FK/integrity, active restored database and historical backup preserved.
- Evidence: `docs/qualification/M2_2_ENTITY_ALIAS_CRUD.md`.

## Completed subdivision — M2.3

**M2.3 — Fact registry and exact revision provenance: COMPLETE + MERGED + NORMALIZED**, effective when the separate normalization PR is terminal-CI-qualified and merged.

Implementation PR #25 merged into `main=e6e80c26316f11054348a18a235fd08c600e136e` from evidence HEAD `b015f7df80f38d75375a0e2615fd62d4c40ee1b8`, after Windows-qualified source `4d3b4b6015d477c3a6a5c3750d9743174e9c44a7`.

Source CI `37879358744` and evidence CI `37961014980`: terminal SUCCESS, all Windows steps PASS. Local 21/21 frontend, 61/61 Rust and 8/8 UI checks PASS with Ollama OFF. Real SQLite v4→v5 migration on M1.5 restored-active DB and independent read-only audit PASS: five exact migrations, STRICT fact/source tables, FK/integrity, full prior row digests, nine entities, eight aliases, three revisions, one head and all historical backup custodial hashes preserved. Evidence: `docs/qualification/M2_3_IMPLEMENTATION_GATE.md`.

## Completed subdivision — M2.4

**M2.4 — Canon status and human review service: COMPLETE + MERGED + NORMALIZED** only after this separate documentation normalization PR is fully exact-HEAD-CI qualified and protected-merged.

Implementation PR #27 protected-merged at `main=3a069572d00e1680c42b0f13b800e28687c5f0eb`. Windows qualified source `aad56bd59fdb87be5ac1eda99b1969452bf61a26`; evidence HEAD `b53405779b04c16525ba48a266bd096096af7020` had its exact `pull_request` run `37989040863` terminal success (13/13 Windows CI steps); source CI `37974831473` success (21/21 frontend, 71/71 Rust).

Real Windows migration to SQLite v6 and full existing data/backup integrity PASS, with pre-v6 verified backup SHA-256 `db02961d7a30c6a6522bd52faeab8ceb09e26c1a4a6a58be467d142806e22fee`, 8/8 existing GUI controls (Ollama OFF), 8/8 isolated Rust human-review tests and unchanged production v6 DB snapshot SHA-256 `67dfd9194ff884762bbffaa39d774df10fadcd74cbc9e6774e36d323e4506fc6`. Exact history/current head and nine entities/eight aliases preserved. The reviewer label is self-declared and **not** an authenticated identity. There is no Windows E2E React fact-review screen or E2E IPC invocation acceptance yet; no production fact rows created. See `docs/qualification/M2_4_CANON_REVIEW_IMPLEMENTATION_GATE.md`.

## M2.5 — Implementation merge complete; normalization pending

- PR #29 successfully protected-merged at `f1e7ea99d26ad3390c7c47bfb339f26d730a44f1` from evidence HEAD `6f55fc3fc7eab6f2288a54619c0bef70e521f47e`, after source qualification `7eaaf45ae164c9336df7e01c9da6787e4971d59e`. Exact evidence-head `pull_request` CI **38040227617**: `completed/success`, 13/13 Windows steps, frontend 32/32, Rust 72/72, `cargo check --locked`, locks unchanged.
- Real Windows operator qualification: hierarchy 8/8, stale-Universe sync correction 8/8, sourced/unsourced fact entry and exact UTF-8 historical citations 9/9, explicit human review interaction checklist 10/10. Independent v6 SQLite read-only audit: **3 facts, 2 exact source anchors, 11 append-only review events**; source revision and prior narrative contents preserved. Earlier 10-event audit script incorrect; actual 11 rows must remain untouched.
- Production restored-active v6 logical digest `67dfd9194ff884762bbffaa39d774df10fadcd74cbc9e6774e36d323e4506fc6` unchanged. Isolated v6 test database digest `cff8a04f29ec60757c02ef9ed186be40c806cfcc6a2cfd11fa8072be44f273cb`. Verified isolated pre-fact backup `9e738d58519e1a0e3c1750d71726b661132fcbc0211fddea3178f6314bbfc7cf`, all historic pre-M2.1/v4/v5 backups intact.
- Reviewer identity self-declared, not authenticated. No AI extraction, no automatic canon promotion, no new dependencies or SQLite v7. Evidence: `docs/qualification/M2_5_SOURCED_FACTS_REVIEW_UI.md`.

**ONLY CURRENTLY AUTHORIZED ACTION:** qualify and protected-merge the **separate documentary M2.5 post-merge normalization PR**, with **fresh exact-head `Fabulaxiom CI`** on all jobs, and re-fetch main after merge. M2 can be marked `COMPLETE + MERGED + NORMALIZED` **only after that gate passes**.

**Do not implement M3 or ComfyUI now.** After normalization, re-fetch `STATE.md`, `NEXT.md`, V1 roadmap, detailed M2 roadmap and architecture decisions. Evaluate/accept a bounded M3 roadmap in its own planning/governance step before any M3 code. ComfyUI visual atelier remains the proposal in issue #19, not authorized implementation.

## Governance and distribution

Keep the source-based release state unchanged. No release is authorized as part of this documentary normalization. No data migration or target-machine action is required. Preserve Tauri app identity in production, M1.5 active pointer, all existing operator backups, SQLite v6 data/history, deterministic lockfiles and independent local-only test worktrees. Never reuse CI from an earlier commit.
