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

## Only authorized implementation

**M2.1 — Entity registry schema and migration: WINDOWS QUALIFIED / EXACT-HEAD CI PENDING**

Implementation PR: **#20 — feat: implement M2.1 narrative entity registry schema v4**.

Branch: `feat/m2-1-entity-registry-schema-20261008`

Qualified implementation SHA: `c7a663d88ba2538714d42fdd366719cd54fe6f70`.

Pre-evidence exact-head CI run `37795098224`: `completed/success`; frontend 13/13, Rust 44/44, build/check/lockfiles PASS.

Real Windows v3→v4 qualification PASS. The actual restored active database, activation marker, v3 backup hash, M1 table rows, scene revisions/current head and SQLite v4 integrity were independently checked. Detailed report: `docs/qualification/M2_1_ENTITY_REGISTRY_SCHEMA.md`.

## Required next gates

1. commit the operator Windows qualification evidence on PR #20;
2. require **new terminal `Fabulaxiom CI` on the evidence commit exact SHA**; earlier CI is historical;
3. only with successful exact-head CI, re-fetch live main/PR and merge #20 with expected-head protection;
4. re-fetch post-merge live `main`;
5. create a separate M2.1 post-merge authority normalization PR, qualify its own exact-head CI and merge;
6. only then confirm whether M2.2 is authorized from the live normalized authorities.

**M2.2–M2.5 and M3+ remain unauthorized until the appropriate gates.**

- Schema v3 → v4, additive and migration-safe;
- `STRICT` Universe-scoped entities for six kinds: character, place, organization, object, event, world_rule;
- separately identified entity aliases;
- stable immutable IDs and ownership/kind;
- CHECK, UNIQUE, FK RESTRICT and relevant indexes;
- preserve all existing M1 data and active restored-database marker;
- deterministic Rust/schema tests and exact-head CI;
- Windows qualification with coherent backup of the **resolved active** SQLite database before migration;
- evidence requalification, protected merge and post-merge normalization.

**M2.2–M2.5 and M3+ are forbidden until their own authority gates.**

## Governance

Do not introduce entity CRUD UI, fact records, canon status, provenance extraction, FTS, search or Ollama functions in M2.1. Preserve historic and application-owned backups. Never migrate the operator's Windows database from GitHub. Re-fetch main, PR heads and exact-head CI before mutation.
