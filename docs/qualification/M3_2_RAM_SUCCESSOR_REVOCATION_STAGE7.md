# M3.2 — Terminal successor revocation, sixth imported Rust tranche (RAM only)

**Date:** 2026-10-22. **Initial base:** protected main `08caad24e20eae484e94fd084edb487b5c370bd5` after PR #121 MERGED (source CI #39713440057 SUCCESS). Historical draft PR #35 source `41ce7b915e76d22785d53d7fffe288d113dd0bf5`, not to be merged wholesale.

## Strict scope
- Only historical SQL `m3_2_successor_revocations_candidate.sql`, `revoke_successor` and `list_successor_history` plus 3 adversarial Rust tests on fictitious fixtures.
- Load candidate SQL after fictitious v6/v7, decision, restatement, withdrawal and successor SQL via `Connection::open_in_memory()`, **only** within `#[cfg(test)]`.
- Immutable one-time terminal withdrawal, strict universe/revision guards and retained original/restatement/successor history. The derived active partial graph excludes withdrawn successor edges.
- Duplicate withdrawal, missing successor, wrong universe, blank reason, cross-universe scene revision, UPDATE/DELETE, illegal successor branching, cycles and active duplicates are refused.
- **No recursive chain correction**, no `m3_2_recursive_chain_candidate.sql`, no ChainHistory port, no new production migration or Tauri command.

## STOP/CI
This candidate requires its own new HEAD-bound Windows CI and review before merge. Synthetic evidence is **not** Windows operator acceptance. M3.2 `IN_PROGRESS_NOT_ACCEPTED`; real writer absence `NOT_PROVEN`; G2B–G6 `NOT_AUTHORIZED`; real G3 `STOP_UNAVAILABLE`; historic `PENDING_EXTERNAL_ATTESTATION(21/3/2)`; prospective `NOT_STARTED`. No protected local v6/v7 SQLite or backups, ACLs, sidecars, activation marker, migration 007, writer IPC, M3.3, ComfyUI or release.
