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

## Next milestone

**M2 — Narrative entities and canonical facts**

**PLANNING AUTHORIZED ONLY — NO IMPLEMENTATION SUBDIVISION AUTHORIZED YET**

First prepare a dedicated `docs/roadmap/M2_NARRATIVE_ENTITIES_CANONICAL_FACTS.md` plan and governance proposal from live `main`. The plan must define sequenced subdivisions, scope and acceptance, especially:

1. structured entities (characters, places, organizations, objects, events, rules) with stable IDs and aliases;
2. a provenance model tied to existing scene revisions and source passages;
3. status semantics: canon, draft, suggestion, variant, unknown, ambiguous, contradictory;
4. validity times and distinctions between unknown vs false;
5. manual review and explicit promotion to canon, never silent AI updates;
6. constrained deletion and referential integrity with migrations/rollback;
7. deterministic no-AI creation, editing, queries and approval;
8. automated regression tests and Windows/operator evidence;
9. M2 subdivision boundaries with exact-head CI and post-merge normalization.

## Governance

- Do not begin M2 code solely because M1 is completed.
- Qualify and merge the detailed M2 planning authority first, then authorize its first bounded implementation subdivision.
- M3+ remain unauthorized.
- Preserve both historical operator backups and app-owned backups; do not silently reset, overwrite or delete production SQLite data.
- Re-fetch live `main`, PRs and all exact-head CI before any mutation.
