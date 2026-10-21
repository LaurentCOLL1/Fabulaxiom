# M3.2 — second stage Rust decisions and revocations (test-only)

**Status at creation: CANDIDATE_NOT_CI_QUALIFIED.** On protected main `388cb745888f9f2d4d0a07fce1ed19fad9b4a548` (PR #116 MERGED, CI source #39626827246 and post-main CI #39628479487 terminal SUCCESS), import selected append-only human-authored decision functions and **unchanged source-only SQL candidate** from PR #35 historic HEAD `41ce7b915e76d22785d53d7fffe288d113dd0bf5`.

The candidate SQL is *not* part of the migration runner. It is loaded only inside the existing disposable `Connection::open_in_memory()` Rust test fixture, after v6 test migrations and the M3.1 v7 fictional candidate. Six Rust unit tests cover explicit anchor revocation and immutable history, atomic supersession and rollback, precedence revocation and preservation, refusal to attach new edges to retired anchors, cross-universe refusal and invalid action veto. Deterministic ID listing does not construct a timeline. Further active-graph/restate/chain semantics are **excluded**.

The existing module remains `#[cfg(test)]` from `src-tauri/src/lib.rs`, never a Tauri IPC command or production app module. No new SQLite opening sites in Rust, no file-backed fixture, no migration 007, no original v6/v7 access. Source inventory must remain matching. The source-only full Windows CI at the new exact HEAD is required before merge.

STOP: M3.2 IN_PROGRESS_NOT_ACCEPTED, writer real NOT_PROVEN, G2B–G6 NOT_AUTHORIZED, real G3 STOP_UNAVAILABLE, historic custody PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED. No Windows operator procedure, backup/ACL/sidecar/migration/writer IPC, M3.3, ComfyUI or release.
