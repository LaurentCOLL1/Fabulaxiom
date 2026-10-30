# M3.2 R3 — native Win32 RESERVED/PENDING/EXCLUSIVE conflict phase matrix

**30 October 2026 — candidate ONLY, not exact-head CI qualified.** Parent protected main `e2014d455e74a58a8a88ef03382d35c16eb8b9cd` after PR #238. Source CI #41052238454 **completed/SUCCESS** for 262 Rust / 7 Greenfield / 50 SQLite inventory / 160 continuity. Independent postmain #41063135914 must be checked at the exact merge SHA. Those results do not qualify this candidate.

## New disposable Windows test

The existing `src-tauri/src/m32_r3_preopened_readonly_vfs_tests.rs` is compiled only under `#[cfg(all(test, windows))]`. It uses a freshly created fictional SQLite file in the runner-owned `%TEMP%` directory. The real SQLite VFS session remains READ_ONLY, based on the original FileId128-identified, held Win32 handle via `ReOpenFile`, never MAIN_DB pathname fallback. The new `m32_r3_win32_native_reserved_pending_exclusive_phase_matrix_without_sqlite_writer` test exercises native `LockFileEx` calls on separate independently opened READ handles:
- An existing SQLite `BEGIN`/`SELECT` maintains SHARED while another native HANDLE acquires RESERVED exclusively; a second owner cannot acquire RESERVED.
- Another SQLite reader still reads under RESERVED. After the native owner acquires PENDING exclusively, a new reader returns BUSY, while the earlier SHARED reader can still read.
- Native EXCLUSIVE across SHARED_FIRST..SHARED_SIZE fails while that original reader holds SHARED. After `COMMIT` releases the last reader lock, EXCLUSIVE succeeds.
- The native owner then releases EXCLUSIVE, PENDING and RESERVED, new read-only SELECT succeeds, FileId128 identity is unchanged and `-wal`/`-shm`/`-journal` sidecars were not created.

This is a witness of **Win32 byte-range lock interoperability**, not a complete SQLite writer state machine. Neither `xLock(RESERVED/PENDING/EXCLUSIVE)` nor `xUnlock` writer transitions are implemented in the read-only VFS; all write operations remain rejected.

**Expected, not yet qualified:** 263 Rust, 7 Greenfield, 51 SQLite inventory, 161 continuity. Newly added Python inventory test #51 and handoff contract test #161 do not replace the real Windows Rust test.

## Strict STOP
M3.2 `IN_PROGRESS_NOT_ACCEPTED`, writer/R1–R9 `NOT_PROVEN`, G2B `NOT_ACCEPTED`, G2C `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`, historical `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`. No production R3 admission or R4 WAL/SHM. No operator v6/v7 DB, sidecars, ACL, backups, migration 007, writer IPC, native Windows Hello, activation marker, or recovery. A0 EXISTING_PROFILE STOP.

## Mandatory next gates
Windows CI completed/SUCCESS on the exact new PR head; review full diff and reviews/threads; `Protect main` active/strict/bypass=[]; protected squash with `expected_head_sha` only if all criteria pass; independent postmain push CI at merge SHA; append-only update to issue #38. Continue full native lock-state handling and independent R4 WAL/SHM only on further new disposable Windows fixtures, not on operator files.

References: [SQLite locking states](https://sqlite.org/lockingv3.html), [SQLite io_methods](https://sqlite.org/c3ref/io_methods.html), [Microsoft LockFileEx](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-lockfileex).
