# M3.2 R3 — Real read-only sqlite3_file backed by held Win32 HANDLE (disposable Windows CI)

**30 October 2026 — SOURCE CANDIDATE; NOT YET EXACT-HEAD CI QUALIFIED.** Parent `main=a14c7826647249587604536e7c8e69a61a47ebc1`: PR #233 source CI #40986052100 completed/SUCCESS, **257 Rust / 7 Greenfield / 47 SQLite inventory / 156 continuity**. Independent postmain run #40999259593 must be checked separately at exact merge SHA before being called PASS.

## This changes what R3 demonstrates

Unlike PR #233's intentional `SQLITE_CANTOPEN` from `xOpen`, the new **Windows test-only** adapter in `src-tauri/src/m32_r3_preopened_readonly_vfs_tests.rs` implements a subclass of `sqlite3_file` with `sqlite3_io_methods` **version 1**. It owns a Win32 `File` obtained via `ReOpenFile` from an already held, FileId128-verified `File`; no Win32 VFS default path-based `xOpen` delegation occurs. Its xClose releases only its clone. xRead performs positional reads, zero-fills short reads per SQLite's contract, xFileSize reads native metadata, and xWrite/xTruncate always return `SQLITE_READONLY`. Unknown controls return `SQLITE_NOTFOUND`. File types other than MAIN_DB and any write-open attempt return `SQLITE_CANTOPEN`. The test-only named VFS is never the process default.

3 Windows-only unit tests, entirely under newly-owned `%TEMP%/fabulaxiom-r3-ro-test-*/invented.sqlite3`:
1. Seed an invented file using ordinary SQLite and close it; reopen through the preheld handle and SELECT the invented integer.
2. Rename the original while retaining its handle, create a second valid SQLite image under the original pathname, then SELECT via the held handle and require the **original** value, not the replacement.
3. Attempt a READ_WRITE SQLite open, and require refusal before any adapter-accepted file or SQL write.

SQLite source inventory requires a new reviewed `(3,0,0,0,0,3,0)` test-only file. One new source-only inventory guard #48 and continuity contract #157. **Expected after exact-head Windows CI, NOT PASS yet: 260 Rust / 7 Greenfield / 48 SQLite inventory / 157 continuity**.

## Nonadmission limits, always enforce

The test-only xLock/xUnlock/xCheckReservedLock functions assume **one newly created fixture reader** and do not acquire Windows byte-range locks; they MUST NOT be repurposed in production or used concurrently. This does **not** establish R3 atomic *production* admission, R4 WAL/SHM custody, real v7 lineage R5, Rust runtime owner R6, explicit shutdown R8, R7 crash recovery or R9 gate. SQLite's xAccess/xFullPathname callbacks inherited from the default VFS are not a verified atomic source namespace. No journal/WAL/SHM paths are admitted. No Tauri IPC, migration 007, native Windows Hello, durable marker or operator data. A0 EXISTING_PROFILE STOP; M3.2 IN_PROGRESS_NOT_ACCEPTED; writer/R1–R9 production NOT_PROVEN; G2B NOT_ACCEPTED; G2C NOT_AUTHORIZED; G3 STOP_UNAVAILABLE; historical PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED; #215/#35 DRAFT.

Sources: [SQLite VFS](https://www.sqlite.org/vfs.html), [SQLite io_methods](https://www.sqlite.org/c3ref/io_methods.html), [Microsoft ReOpenFile](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-reopenfile).

**Next**: qualify the run on exact HEAD, audit diff/reviews/threads and strict Protect main, protected squash with expected_head_sha only after SUCCESS, independent postmain run, issue #38 append-only. Then build correct Windows locking, WAL/SHM and real-v7 verification on strictly disposable fixtures before any production operation.