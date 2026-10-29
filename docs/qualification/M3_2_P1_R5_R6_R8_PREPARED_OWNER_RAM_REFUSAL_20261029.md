# M3.2 P1 R5/R6/R8 — prepared owner RAM-only refusal evidence

**29 octobre 2026 — CANDIDATE, NOT EXACT-HEAD CI PASS.** Protected parent `fb81eb85ec5842f9d117e9f6c64351c1f107fc23` after PR #231. Source Windows CI [#40951341500](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40951341500) and independent postmain [#40953281939](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40953281939) SUCCESS at respective exact SHA: **252 Rust, 7 Greenfield, 47 SQLite inventory, 154 continuity**.

## Bounded code change
Three new tests inside the existing prepared `m32_v7_writer_service.rs` Rust test module, using its `fictive_connection()` (RAM only, **CURRENT_SCHEMA_VERSION=6**):
1. `m32_v7_writer_prepared_r5_rejects_incomplete_migration_lineage`: delete the current migration marker; expect AdmissionRejected.
2. `m32_v7_writer_prepared_r5_rejects_foreign_keys_off`: turn FK enforcement off; expect AdmissionRejected.
3. `m32_v7_writer_prepared_r8_drop_revokes_multiple_clients`: after a valid fictional read, Drop owner then require Disconnected for two cloned clients.

The original eight prepared-owner tests are retained; continuity contract #155 pins **11 total**. **Expected at new source SHA, NOT YET QUALIFIED: 255 Rust / 7 Greenfield / 47 SQLite inventory / 155 continuity.**

## Strict interpretation
These are **R5/R6/R8 negative RAM witnesses only**, not v7 migration-lineage proof, complete FK integrity, real-file custody, multi-process shutdown or production P1. No new opener, V7WriterAdmission production constructor, Tauri State/IPC, writer, operator profile, durable marker, Windows Hello, migration 007 or recovery. R3 atomic xOpen NOT_PROVEN; R4 production NOT_PROVEN; R5/R6/R8 production NOT_PROVEN; R7/R9 separate STOP. A0 EXISTING_PROFILE STOP; M3.2 IN_PROGRESS_NOT_ACCEPTED; G2B NOT_ACCEPTED; G2C NOT_AUTHORIZED; G3 STOP_UNAVAILABLE; historical PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED; #215/#35 DRAFT.

Next: exact-head Windows CI, diff/reviews/threads, Protect main strict with zero bypass, protected expected_head_sha merge ONLY on success, independent postmain CI, issue #38 append-only; then bounded R3 real HANDLE VFS and true v7 R5 lineage in new disposable fixtures.
