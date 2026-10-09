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

## Only next authorized implementation

**M2.3 — Fact registry and exact revision provenance: AUTHORIZED ONLY AFTER M2.2 NORMALIZATION MERGES.**

The future dedicated M2.3 PR must start by re-fetching live `main`, `STATE.md`, `NEXT.md`, the detailed M2 roadmap and the M2.2 evidence report. M2.3 scope (nothing beyond):

1. Stable structured fact IDs and entity associations in the correct Universe.
2. Explicit sourced/unsourced provenance; optional citations to immutable Scene revision rows, not merely current-head pointers.
3. UTF-8 `[start,end)` byte offsets, exact excerpt/source fidelity and bounds checks.
4. Same-Universe consistency across entities, revisions and cited material.
5. Atomic multi-row writes and deterministic rollback/negative-path tests.
6. No Ollama required; no invented citations and no automatic canon promotion.
7. Preserve all historical backups, SQLite restored-active pointer, revision lineage, dependency lockfiles and prior UX.
8. Windows operator qualification, evidence commit, exact-head PR CI, protected merge and separate post-merge normalization before M2.4.

**M2.4–M2.5, M3+ and ComfyUI remain NOT AUTHORIZED.** Visual references via optional local ComfyUI and manual import are retained as proposal-only in issue #19 and `docs/roadmap/V1_VISUAL_REFERENCES_COMFYUI_PROPOSAL.md`.

Do not implement M2.3 inside the M2.2 normalization PR.

## Governance

Always re-fetch exact live `main`, PR heads and CI before mutation. Preserve historical operator SQLite backups. Revalidate every new source/document SHA, and do not use an old CI run as authorization to merge a new HEAD.
