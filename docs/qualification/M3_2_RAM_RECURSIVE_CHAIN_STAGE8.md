# M3.2 — Separate Stage8 recursive correction lineage candidate (fictional RAM only)

2026-10-22. Initial protected base `52b06099ba0cff0da15fa697b0e2043afc883a00` after source-only PR #122. Historical draft PR #35 HEAD `41ce7b915e76d22785d53d7fffe288d113dd0bf5` is **not mergeable** as a whole.

Scope: port only `src-tauri/sql/m3_2_recursive_chain_candidate.sql`, `ChainHistory`, `append_chain_correction`, `revoke_chain_correction`, `list_chain_history` and four adversarial Rust fixture tests. Each previous authored assertion must be explicitly withdrawn before one next correction is allowed; immutability, same-Universe revision ancestry, unique predecessor, active graph duplicate/cycle veto and retained history are mandatory. This is a **separate seventh imported tranche**, not part of the merged sixth-stage successor withdrawal.

Source module `m32_manual_chronology` remains behind `#[cfg(test)]`, fixtures use only `Connection::open_in_memory()`; all v6/v7 and M3.2 candidate SQL are loaded on invented RAM connections. Never apply this SQL to operator databases or register a normal SQLite migration. No Tauri writer IPC, Windows GUI, external services or production files.

Qualification requires separate PR, exact HEAD Windows `Windows frontend and Rust checks` terminal SUCCESS, adversarial logs and preservation of all safety gates. This branch must be rebased/integrated against protected main **after** separate documentary PR #123 succeeds; do not use earlier HEAD CI, and include living handoff `CURRENT.md/json` in the final PR.

STOP: M3.2 `IN_PROGRESS_NOT_ACCEPTED`; real writer absence `NOT_PROVEN`; G2B–G6 `NOT_AUTHORIZED`, real G3 `STOP_UNAVAILABLE`, historical custody `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`. PR #35 OPEN/DRAFT. No Windows operator instructions, SQLite originals, backup/ACL/sidecar/activation-marker touch, migration 007, writer IPC, M3.3, ComfyUI, release.
