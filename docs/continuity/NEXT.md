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

## Only next authorized implementation

**M2.4 — Canon status and human review service: IN PROGRESS, NOT QUALIFIED.**

Starting live normalized `main=ebaaf62933dadf6f0662ca749227a0b340b8a7e3`; implementation branch `feat/m2-4-canon-status-review-20261009`. SQLite v6 is ADDITIVE and the operator's v5 database **must not** be opened with M2.4 until a new independently verified pre-v6 SQLite-consistent backup of its actual restored active file is secured after terminal exact-head CI. Do not touch historical backups or active marker. See `docs/qualification/M2_4_CANON_REVIEW_IMPLEMENTATION_GATE.md`.

Scope: a deterministic human-declared status service, append-only review events, explicit approvals/revocations, atomicity and negative-path evidence, no Ollama. M2.5 React UI, AI extraction, ComfyUI and later milestones remain unauthorized.

Bounded scope from the accepted detailed M2 roadmap:

1. Deterministic canon/draft/suggestion/variant/unknown/ambiguous/contradictory state vocabulary and allowed transitions.
2. Explicit human confirmation and durable review records; no suggestion becomes canon automatically.
3. Separate uncertain, variant and contradictory facts; auditable status history despite display-name changes.
4. Transaction/rollback, same-Universe ownership, stable error payloads, no Ollama dependency.
5. Protect SQLite v5 records, backups, activation marker and scene-provenance history; new migration only under governed Windows backup/qualification.
6. Exact-head PR CI, real Windows operator acceptance, evidence commit, protected merge and separate normalization before any M2.5 development.

Do not add a fact-editor UI, AI extractor, chronology, FTS5, embeddings or ComfyUI in M2.4 beyond its accepted review-service contract. M2.5, M3+ and the proposal-only ComfyUI visual atelier (issue #19) remain **NOT AUTHORIZED** until their own gates.

This normalization PR is **documents only**; do not start M2.4 implementation inside it.

## Governance

Always re-fetch exact live `main`, PR heads and CI before mutation. Preserve historical operator SQLite backups. Revalidate every new source/document SHA, and do not use an old CI run as authorization to merge a new HEAD.
