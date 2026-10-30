# M3.2 R3 — native Win32 PENDING-byte read-only SQLite admission (disposable)

**30 October 2026: CANDIDATE / NOT YET EXACT-HEAD CI QUALIFIED.** Parent protected `main=2d8cde651bbdd0653bab9639b2dc7ca8981ad88e` after PR #237, source CI #41040065251 SUCCESS. Independent postmain CI #41051070838 must be independently verified; do not transfer a prior CI result to this candidate.

## Scope
Only `#[cfg(all(test, windows))]` in `src-tauri/src/m32_r3_preopened_readonly_vfs_tests.rs`, fresh fictional SQLite database under `%TEMP%`. Main DB's real SQLite read-only `sqlite3_file` uses `ReOpenFile` from a pinned Win32 FileId128 HANDLE; no pathname fallback.

A new SHARED admission now obtains short `LockFileEx` shared `PENDING_BYTE`, then acquires the SHARED byte-range lock and releases PENDING on both success and failure; a PENDING release failure refuses with `SQLITE_IOERR_LOCK` and attempts to unwind SHARED. A different Win32 HANDLE holding PENDING exclusive blocks a new SQLite reader with `SQLITE_BUSY`. A held RESERVED exclusive does not block new SQLite SHARED readers. One new Windows test `m32_r3_win32_pending_lock_vetoes_new_reader_reserved_still_allows_reader` checks these transitions, stable FileId128, correct SELECT and absent `-wal`/`-shm`/`-journal`. Four earlier R3 tests remain.

**262 Rust / 7 Greenfield / 50 SQLite inventory / 160 continuity EXPECTED, NOT PASS before exact-HEAD Windows CI.** New source-inventory test #50 and continuity #160 are source-only.

## STOP
No native writer RESERVED/PENDING/EXCLUSIVE upgrades, no R4 WAL/SHM callbacks, no production R3 admission, no writer, IPC, migration 007, Windows Hello native, marker, recovery, or operator v6/v7 path, sidecars, ACL, backups. `M3.2 IN_PROGRESS_NOT_ACCEPTED`, writer/R1–R9 `NOT_PROVEN`, G2B `NOT_ACCEPTED`, G2C `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`, historical `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, existing profile STOP.

## Next
Exact-head Windows CI, diff/reviews/threads, Protect main strict no bypass, protected squash expected_head_sha only if PASS, separate postmain CI, issue #38 append-only. Next: complete native R3 lock state machine and separately R4 WAL/SHM only on newly created Windows disposable fixtures.

References: https://sqlite.org/lockingv3.html ; https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-lockfileex ; https://github.com/sqlite/sqlite/blob/master/src/os_win.c
