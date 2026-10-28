# M3.2 v7 — S1 contract and S2 disposable Windows preflight candidate (28 October 2026)

**Candidate, not CI-qualified or admitted.** Base `main=5f2a47f13715de5fb34d838daa869bb108e2ddfe` (PR #205 terminal: source `0f54d6dfe553c7d9b7a27a36b4e852ae550d5faa`, source CI #40657401464 and independent postmain #40658931404 SUCCESS; 189 Rust / 7 Greenfield / 41 SQLite guards / 136 continuity contracts). Owner authorization in the conversation is limited to S1/S2 Rust preparation and disposable Windows fixtures. It grants **no** S3/S4, operator SQLite/backup/ACL/sidecar/journal/marker, IPC, migration 007 or native Windows Hello.

**First-source negative evidence (retain, do not transfer):** PR #206 SHA `60ea6fa5ab4bc4fdca5d501514e72640e1460b67`, Windows CI #40664955879 **FAILURE** at Rust step: 189 baseline PASS, five new tests FAIL before assertions at fixture line 80 (`create_dir` could not create nested `database/` because the same-profile parent had not yet been created). No operator path or admission used. Candidate correction uses `create_dir_all` exclusively beneath a unique runner-owned fixture root; a fresh exact-SHA CI is mandatory. This is fixture setup correction, **not** an admission security relaxation.

## S1 — admission contract

- Same logical `com.fabulaxiom.greenfield.v1` profile only; no alternate application identity. `NEW_ONLY` requires an absent main file and exclusive `create_new` reservation; `EXISTING_PROFILE` requires a pre-existing regular main file from this exact profile and forbids creating it.
- The intended identity must bind an **actually opened SQLite handle** and its directory/namespace ancestors through the entire handoff; a pathname, lexical canonicalization or FileId128 measured before/after `xOpen` is not an atomic guarantee. Reparse/junction and rename races are STOP until this is proved.
- `-wal`, `-shm`, `-journal` are part of the lifecycle and recovery decision. For NEW_ONLY pre-existing sidecars are a refusal. For EXISTING_PROFILE sidecars require independently proven origin, locking/recovery state and non-mutating inspection before any admission; unrecognized sidecars STOP.
- A reopened existing profile must validate expected schema owner, migration lineage and integrity/foreign keys; `user_version` alone cannot authenticate provenance. No automatic migration, checkpoint, journal mode change or recovery of operator files.
- Single in-process Rust owner serializes its own commands, **not** unknown external writers. No connection is eligible for the current sealed `V7WriterAdmission` token until a separately reviewed atomic opener and sidecar policy exist. Failure revokes candidate; shutdown cannot silently reopen by path.

## S2 — deliberately bounded fixture testimony

`src-tauri/src/m32_v7_admission_preflight_tests.rs` is `#[cfg(all(test, windows))]`. It creates fresh unique roots under the runner temporary directory, with no operator path resolution and no invocation from Tauri. Tests distinguish absent/present main, exclusive creation and repeated claim failure, pre-existing WAL/SHM/journal refusal without mutation, controlled substitution after precheck, foreign schema, and inconsistent foreign key data. A positive preflight **does not** authorize a connection or mint the writer token: every unbound handoff returns `HandoffNotAtomic`.

**Unresolved, hard STOP before admission:** Win32 chain of ancestor handles and reparse/junction defense; atomic binding of SQLite's actual open file to the validated identity; genuine sidecar lifecycle and crash recovery; external writer exclusivity; full foreign schema-owner/lineage check; production `EXISTING_PROFILE` consent. The fixture is an honest negative witness, not completion of all S2 security properties. A later positive implementation requires a new review and evidence at its own SHA.

## Qualification protocol

Expected on this candidate: **194 Rust tests** (189 prior + 5 Windows-only), 7 Greenfield, 41 SQLite guards, **137 continuity contracts** (136 prior + one refusal/drift contract), subject to Windows CI logs at the exact candidate SHA. These numbers are targets, **not PASS**. Review full diff, reviews and threads, active strict `Protect main`, then protected squash with `expected_head_sha`, independent postmain CI on the resulting SHA, and append-only issue #38 source/terminal evidence. No inherited CI qualifies new code.

Gates remain M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, external writer `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, real G3 `STOP_UNAVAILABLE`, historical `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`; PR #35 remains OPEN/DRAFT.
