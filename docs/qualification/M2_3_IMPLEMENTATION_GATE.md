# M2.3 — Fact registry and immutable revision provenance (implementation qualification plan)

## State
**IMPLEMENTATION / CI IN PROGRESS — NOT WINDOWS QUALIFIED, NOT MERGED**

Base live normalized `main`: `70d8c5ca079eb94ef93ae7f5ee684503f99400cd`.
Branch `feat/m2-3-fact-registry-exact-provenance-20261009`. Database migration **v4→v5 has NOT run on operator Windows**.

## Bounded scope
- Add `narrative_facts` and `fact_sources` as SQLite STRICT tables with FK restrictions and immutable fact/source provenance.
- Atomic manual Rust/Tauri source/fact creation and read/list, all local and independent from Ollama.
- The explicit `sourced` / `unsourced` provenance classification is **not** a canon-review state. No automatic canon promotion or IA extraction.
- Source anchored to an immutable `scene_text_revisions.id` rather than `scene_revision_heads`; UTF-8 `[start,end)` byte offset and exact quoted passage verified against the immutable revision text.
- Cross-Universe citations prohibited; optional `exact|approximate|relative|unknown` validity descriptors, no calendar engine.
- Backup path resolution and support for old application v3/v4 backups must remain non-destructive. The v5 migration is additive.
- No source extraction UI, FTS5, chronology, M2.4/M2.5, AI generation or ComfyUI.

## CI and mandatory tests
- `npm ci`; frontend tests/build; Rust tests `--locked`; `cargo check --locked`; unchanged lockfiles.
- Fresh v1–v5 schema, explicit v4→v5 migration preserving entity/alias, scene revisions and current head.
- Source span validation: invalid boundaries inside UTF-8 graphemes/code points, negative/empty/out-of-range offsets, incorrect exact quote, wrong Universe/revision, absent entity, duplicate source IDs, second-row transaction rollback.
- No canon promotion; no assumed Gregorian calendar; multiple Universes distinct identities and strict foreign keys; SQLite `foreign_key_check=[]`, `integrity_check=ok`.
- Existing application backups and restored active database must be preserved. Verify legacy v3 and v4 backup restoration into **new** migrated v5 files with unchanged original files.

## Windows operator boundary (DO NOT START MIGRATION YET)
1. Re-fetch live `main`, the M2.3 branch/PR, HEAD and all `pull_request` jobs on the exact source SHA. Stop on any non-success.
2. Before opening any M2.3 executable, fully exit Fabulaxiom. Read the live M1.5 activation marker and derive the **actual** restored-active SQLite path, not the default filename. Verify the same marker reported by the app.
3. Create a NEW separate **SQLite-consistent backup** of the active v4 database with Python's SQLite backup API, a collision-resistant path, exclusive-create semantics, SHA256, owner/migration/FK/integrity/revision digests. Do not overwrite prior M1.2/M1.4/M1.5 or pre-M2.1 backups.
4. Only after backing up and qualifying the pristine v4 source may the v5 app run and apply migration v4→v5 exactly once. Do not force migrations manually.
5. With Ollama stopped, confirm UI hierarchy, entity/alias CRUD, revisions, backups and diagnostics still work. M2.3 has no human fact-review UI yet; inspect API/schema and tests separately.
6. After app exit, inspect the actual active SQLite read-only: v5, five migration rows, new STRICT fact/source tables, FK/triggers/indexes, exact-preserved original nine entities/eight aliases (unless operator intentionally changed data), three scene revisions, one current pointer; source/content and backup SHA256 unchanged; both integrity PRAGMAs pass.
7. Operator reports concrete logs and any warning. Only then record qualification evidence commit, invalidate old SHA CI, requalify the exact evidence-head CI, merge protected, and normalize in a separate PR.

## Deferred
- M2.4 human canon status/review, M2.5 sourced-fact UI, all later milestones, and optional local ComfyUI image references (issue #19) are excluded.
