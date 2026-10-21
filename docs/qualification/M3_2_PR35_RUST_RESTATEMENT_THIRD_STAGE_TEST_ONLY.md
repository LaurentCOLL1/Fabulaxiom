# M3.2 — third-stage explicit restatement of a revoked precedence

**CANDIDATE_NOT_CI_QUALIFIED.** From historic PR #35 `41ce7b915e76d22785d53d7fffe288d113dd0bf5`, port only `restate_revoked_precedence` to the existing Rust module compiled under `#[cfg(test)]`, and the unchanged `m3_2_active_precedence_candidate.sql` schema. GitHub `main=b76e6c00c579bee36c194872e3679c48fe9788fa` already includes PR #117; both exact-head CI #39653506345 and postmerge main CI #39655214998 SUCCESS. This does not qualify operator Windows.

All SQL is loaded into a **disposable** `Connection::open_in_memory()` fixture after fictional v6 migrations, fictional v7 candidate, and the append-only decision candidate. SQLite schema migrations remain at v6. Five Rust tests cover same-Universe author-revoked prerequisite, active-cycle refusal, immutability and single restatement per source edge, current-anchor validation / live duplicate refusal, and prevention of raw insertion cycles around explicitly restated edges. Old precedences and revocations remain queryable and immutable.

Revocation of restatements, successive corrections, and any total chronology inference are excluded. No production use, no Tauri IPC, no new SQLite file opens, no writer privileges, no migration 007.

**STOP:** M3.2 `IN_PROGRESS_NOT_ACCEPTED`; writer real `NOT_PROVEN`; G2B–G6 `NOT_AUTHORIZED`, real G3 `STOP_UNAVAILABLE`; historical `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`. Do not touch Windows operator environment, private v6/v7 databases, backups, sidecars, ACL, markers, M3.3 or release.
