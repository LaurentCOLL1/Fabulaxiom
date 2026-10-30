# M3.2 R3 — Win32 read-only SHARED failure and xClose cleanup (disposable only)

**30 October 2026: candidate, exact-head CI NOT YET QUALIFIED.** Parent protected main `3288bc5099428d2e0f758dfd4ac8eb8707737c8f`, after PR #239 exact-source [#41064116889](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/41064116889) completed/SUCCESS (263 Rust, 7 Greenfield, 51 SQLite inventory, 161 continuity). Independent PR #239 postmain [#41068824429](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/41068824429) must be confirmed terminal SUCCESS on its merge SHA separately.

## New Windows regression witnesses

Only `#[cfg(all(test, windows))]` `src-tauri/src/m32_r3_preopened_readonly_vfs_tests.rs`, actual SQLite READ_ONLY session on **fresh fictional CI-owned `%TEMP%` database**, previously held FileId128-identified Win32 HANDLE re-opened without pathname delegation.

1. `m32_r3_failed_shared_lock_drops_pending_gate_and_retry_succeeds`: competing Win32 HANDLE holds SHARED range exclusively; the new SQLite reader's `SELECT` fails BUSY, and native exclusive PENDING lock by the competitor subsequently succeeds, proving the failed SHARED attempt released the transient PENDING gate. After removing conflict, the next read succeeds with original file identity.
2. `m32_r3_sqlite_close_during_readonly_transaction_releases_native_shared`: a read-only SQLite `BEGIN/SELECT` holds native SHARED; overlapping EXCLUSIVE lock fails with `ERROR_LOCK_VIOLATION`. Dropping the SQLite session without explicit COMMIT releases SHARED via xClose; EXCLUSIVE succeeds on a separate HANDLE, and subsequent SELECT succeeds.

The fixture asserts absence of `-wal`, `-shm`, and `-journal` sidecars. No SQLite writer is opened or database bytes modified. Existing six module tests remain. **Expected before new CI: 265 Rust / 7 Greenfield / 52 SQLite inventory / 162 continuity (NOT PASSED YET).** New inventory tripwire #52 and continuity contract #162 preserve writer and operator STOP.

## Strict scope and remaining risk

This is **not** the complete Windows SQLite writer `xLock(SHARED→RESERVED→PENDING→EXCLUSIVE)` state machine, not WAL/SHM or crash recovery, not production v7 admission. The only new behavior is testing existing read-only Win32 lock release and retry.
`M3.2 IN_PROGRESS_NOT_ACCEPTED`, writer/R1–R9 `NOT_PROVEN`, G2B `NOT_ACCEPTED`, G2C `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`, historical `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`. No existing operator v6/v7 file, sidecar, backup or ACL; no writer IPC, 007, native Hello, marker or recovery.

## Gates
Review exact-head source Windows CI, diff, reviews/threads and `Protect main` strict bypass=[]; protected squash only with expected_head_sha on PASS; independently verify postmain push CI, append-only issue #38. Future work: full native state machine in disposable tests; independent R4 WAL/SHM only disposable.

References: https://www.sqlite.org/c3ref/io_methods.html ; https://www.sqlite.org/lockingv3.html ; https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-lockfileex
