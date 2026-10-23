# M3.2 — Same-connection data_version is not a writer-exclusion proof (23 October 2026)

**STRICTLY TEST-ONLY / RAM-ONLY. NO REAL OPERATOR SQLITE, ORIGINAL DATABASE, FILE ACCESS, MIGRATION OR TAURI IPC.**

## The negative witness

The feature-gated Rust test `m32_owner_lifecycle_data_version_same_connection_write_not_revision_guard_negative_witness` creates a fresh invented v6 SQLite database through the existing `OwnerSlot::new_invented(6)` RAM-only fixture.

1. The toy owner obtains an issued lease and an initial transactional RAM backup.
2. The test records `PRAGMA data_version` from **the already-owned connection**.
3. A fictitious `UPDATE invented_facts` is executed directly on that connection, *bypassing* `edit_fixture()`, and is committed in autocommit mode.
4. `PRAGMA data_version` is measured again on that **same** connection. It remains unchanged, as SQLite documents for same-connection commits.
5. The old fictitious revision lease remains equal and can capture another valid RAM snapshot, which contains the changed invented fact while the prior snapshot is unchanged.

This falsifies an unsafe shortcut: checking `PRAGMA data_version` on the owner connection would **not** prove that all its own mutation paths advanced an application revision counter. Values from different connections cannot be compared as absolute revisions either.

## Evidence boundary and design consequence

SQLite officially specifies that `data_version` changes when **other connections** commit, *not* for writes committed by the same connection: https://www.sqlite.org/pragma.html#pragma_data_version. The official Online Backup documentation describes transactional copies and concurrent writes but does not authenticate original provenance or grant exclusive ownership: https://www.sqlite.org/backup.html.

The test is a negative **design-only fixture**. It does not establish a production writer inventory, a trusted nonmigrating preexisting owner, file identity, writer quiescence or historical custody. The hypothetical owner-policy `all_mutation_entrypoints_mediated` still defaults to `False`; all synthetic claims never authorize real G3.

## Dated GitHub checkpoint

PR #139 source `f9d28610bac2a97f517a39e9bceb5b0b4d85a96e` CI #39915173862 SUCCESS, merge `26e533c97d34ae36d25226730c7f74a7f0ee2e3f` and postmain #39916772343 later verified SUCCESS. PR #140 source `9d859cb5b61f87782cede0db1c9e59a3a113948d` CI #39917211662 SUCCESS (75 Windows, 75 handoff, 132 Rust, Chromium 53/53 each mode and indirect trigger witness PASS), merge `main=f5a255e6687c68c1e6095d8e3a8c20277415741c`. PR #140 postmain #39920611327 was **IN_PROGRESS_AT_CHECKPOINT** during drafting: verify its terminal state separately.

The present new test requires its **own terminal exact-SHA CI**; the earlier PR CI cannot qualify a new commit. No source files, operator workstation files, backup, marker, ACL, sidecars or SQLite originals were inspected for this witness.

M3.2 `IN_PROGRESS_NOT_ACCEPTED`; G2B global `NOT_ACCEPTED`; original source `PARTIAL_LOCAL_IDENTITY_ONLY`; writer absence `NOT_PROVEN`; G2C `NOT_AUTHORIZED`; real G3 `STOP_UNAVAILABLE`; G2B–G6 `NOT_AUTHORIZED`; historic `PENDING_EXTERNAL_ATTESTATION(21/3/2)`; prospective `NOT_STARTED`; PR #35 `OPEN/DRAFT`.
