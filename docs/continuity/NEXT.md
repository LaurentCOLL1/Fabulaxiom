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

## Only authorized implementation

**M2.2 — No-AI entity and alias CRUD: AUTHORIZED**

The M2 roadmap's M2.2 contract is now the only implementation scope:

1. Rust service models/DTOs for all six kinds of narrative entity, plus alias records.
2. Create/read/list/rename/delete without changing entity ID, owning Universe or kind.
3. Explicit restrictions for deleting entities with aliases, no silent cascade.
4. Preserve same-name distinct identities; no name-based foreign keys.
5. Thin Tauri commands and usable React forms for Universe-scoped entity/alias management.
6. Deterministic errors, explicit transactions where needed, rollback and negative-path tests.
7. Preserve M1/M2.1 schema, revision history, active database, backups, and deterministic lockfiles.
8. No Ollama dependency; prove real UI CRUD works with Ollama stopped.
9. Qualify the exact PR source on GitHub and operator Windows, document evidence, requalify its new SHA.
10. Protected merge and separate post-merge M2.2 normalization before M2.3.

Do not implement fact storage, canon review, source anchors, timeline, automatic narrative AI, image galleries or ComfyUI in M2.2. These belong to future, separately authorized work.

**M2.3–M2.5 and M3+ remain unauthorized.** The ComfyUI visual reference extension is still proposal-only.

## Governance

Always re-fetch exact live `main`, PR heads and CI before mutation. Preserve historical operator SQLite backups. Revalidate every new source/document SHA, and do not use an old CI run as authorization to merge a new HEAD.
