# M3.2 R3 — Preopened HANDLE inside SQLite xOpen, fail-closed (30 October 2026)

**CANDIDATE, NOT YET EXACT-HEAD WINDOWS CI PASS.** Baseline PR #232 merged protected to `main=c9441844db4e897c171cac11b886bc306059acb1`, source CI #40958814457 and independently triggered postmain CI #40960445573 both completed/SUCCESS **255 Rust / 7 Greenfield / 47 SQLite inventory / 155 continuity**. This note does not authorize the production writer.

## New actual SQLite callback probe, without SQLite admission

Only in `src-tauri/src/m32_sqlite_vfs_preopen_tests.rs`, already `#[cfg(all(test, windows))]`, one new reviewed `Connection::open_with_flags_and_vfs` site targets a new, test-owned `%TEMP%/fabulaxiom-vfs-fixture-*/new.sqlite3`. Registered test VFS is non-default. `with_preopened_r3` accepts an already-held Win32 `fs::File`, not a path. Its actual SQLite `fixture_xopen` callback invokes Windows `ReOpenFile` on that handle and checks 128-bit file identity. It closes the cloned HANDLE via Rust File, sets `sqlite3_file.pMethods=NULL`, and returns `SQLITE_CANTOPEN` **before any default Windows VFS xOpen**, for MAIN_DB and all other file types.

Two new tests:
- `m32_r3_sqlite_xopen_reopens_preheld_handle_without_path_delegation`: one callback identity match, zero default main xOpen, main unchanged, no WAL/-shm.
- `m32_r3_sqlite_xopen_held_handle_survives_replaced_name_but_vetoes`: controlled test-only rename + `create_new` replacement; callback clones original held object, not the replacement path; still denies SQLite.

Historical 26 pre-R4 VFS and five R4 tests preserved. One new source SQLite opener expression, source inventory count changes **(24,0,0,0,0,25,0) to (25,0,0,0,0,26,0)**. New continuity contract #156. **257 Rust / 7 Greenfield / 47 SQLite inventory / 156 continuity EXPECTED, NOT PASS until exact-head CI**.

## Limits and next

SQLite requires a complete `sqlite3_file` implementation on successful xOpen; a HANDLE probe is **not** a working file adapter. See [SQLite VFS](https://www.sqlite.org/c3ref/vfs.html), [SQLite io_methods](https://www.sqlite.org/c3ref/io_methods.html), and [Win32 ReOpenFile](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-reopenfile). `SQLITE_FCNTL_WIN32_SET_HANDLE` is debug-only and not used.

R3 atomic admission NOT_PROVEN; R4 WAL/SHM production NOT_PROVEN; R5 actual v7 lineage / R6 owner runtime / R8 shutdown production NOT_PROVEN; R7 recovery and R9 admission remain separate. A0 EXISTING_PROFILE STOP; M3.2 IN_PROGRESS_NOT_ACCEPTED; G2B NOT_ACCEPTED; G2C NOT_AUTHORIZED; G3 STOP_UNAVAILABLE; historical PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED; #215/#35 DRAFT. No operator SQLite v6/v7, WAL, ACL/backups, marker, IPC, 007, Hello, actual recovery or writer.

**Next**: build test-only genuine `sqlite3_file` and `sqlite3_io_methods` on preopened Win32 HANDLE with read/write/sync/lock/unlock/close correctness; fail-closed handling of all ancillary file types; disposable identity swaps and WAL/SHM/exclusive mode. No production promotion without R1–R9. Exact-head CI, diff, reviews/threads, strict Protect main zero bypass, protected `expected_head_sha` merge only after PASS, independent postmain CI and append-only issue #38.