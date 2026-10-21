# M3.2 — first-stage Rust chronology service port (candidate, test-only)

**CANDIDATE_NOT_CI_QUALIFIED at time of creation.** This scope extracts exactly five SQL-backed functions and their data structs from the historical PR #35 head `41ce7b915e76d22785d53d7fffe288d113dd0bf5`, without merging, rebasing or rewriting that PR.

The module `src-tauri/src/m32_manual_chronology.rs` is included in current `src-tauri/src/lib.rs` under `#[cfg(test)]` **only**, not in normal/debug/release builds and not exported to Tauri command invoke. It uses parameterized inserts and read-only SELECTs. Six new Rust tests create `Connection::open_in_memory()` databases, migrate only the invented RAM v6 fixture, layer the existing M3.1 v7 candidate schema **inside that RAM connection only**, and exercise two Universes, four manually declared fictional time kinds, deterministic ordering without automatic chronology, explicit before/after, cycle/self/duplicate rejection, foreign-universe guard, immutability and historical scene revisions. Production schema max stays 6; no real v7 registration or migration 007.

The material deliberately **does not** port chronology decisions/revocations/atomic supersession from PR #35 yet; these depend on additional append-only candidate SQL and will require a separate reviewed fixture-only increment. Success in CI cannot prove any Windows source ownership, sidecar quiescence, backup integrity, operator consent or product acceptance.

STOP: M3.2 IN_PROGRESS_NOT_ACCEPTED; PR #35 OPEN/DRAFT and not mergeable; writer absence NOT_PROVEN, G2B–G6 NOT_AUTHORIZED, real G3 STOP_UNAVAILABLE, historical PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED. Never access original production v6 or isolated v7 SQLite, backups, ACL, markers or journals; no runtime writer IPC, migration 007, ComfyUI, M3.3 or release.

## Source-inventory tripwire — 2026-10-21

Initial CI #39625498131 **FAILED** in the whole-tree Rust SQLite occurrence audit, correctly detecting the newly introduced test-only source. Manual code review bounded to public PR116 files found exactly 1 `Connection::open_in_memory()` and 1 `database::run_migrations()` invocation in the RAM fixture, 0 other audited opening/backup/ATTACH/VACUUM/flags. The inventory `EXPECTED` was amended **only for this new path** to `(1,0,1,0,0,0,0)`, with 3 fresh adversarial tests refusing a second open/migration and asserting RAM-only + no IPC. No change to a production opening policy or gate. A newer exact-head CI must pass before acceptance of this synthetic tranche; the previous failure remains historical and cannot be reused.

Second CI #39626066048: Python newline-escaping assertion failed while checking the existing test-only module declaration. Fix uses `chr(10)` in two tests; Rust module, source inventory and safety STOP unchanged. Requalification at newer HEAD required.
