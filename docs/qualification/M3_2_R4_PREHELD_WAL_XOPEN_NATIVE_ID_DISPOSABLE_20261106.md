# R4 — Preheld WAL native FileId128 at actual disposable SQLite xOpen

6 November 2026. Candidate only, NOT QUALIFIED. Parent main af94ef1499663a6f6656c1ea4ae24436cc1d6b8f (#298); independent parent postmain #42292721400 pending.

Opt-in test-only WAL preheld HANDLE/FileId128 is created using CREATE_NEW under the freshly invented TEMP scratch directory. On the real SQLite WAL xOpen, after validating the associated main sqlite3_file object, compare the preheld WAL identity against the named WAL before delegating to SQLite's default VFS. The delegated native Win32 WAL HANDLE FileId128 is then compared to the same preheld identity. One existing positive NORMAL WAL test is strengthened, one new standalone negative ABA helper test asserts permanent refusal after observed name substitution and restoration. The default VFS is never replaced; non-opted tests remain unchanged.

Expected only, NOT PASS: 324 Rust, 7 Greenfield, 69 SQLite inventory, 183 continuity, 373 Vitest, Chromium 85/85 normal and CSP, 19 fictional Git blobs. A preexisting WAL may interact with SQLite's normal lifecycle; review CI errors before any merge.

This DOES NOT close the time-of-check/time-of-use interval between name comparison and delegated path xOpen; three-file main/-wal/-shm native custody is not indivisible, unseen ABA cannot be excluded, a hostile same-SID writer and recovery are not proven. No production VFS, IPC writer, real P4, migrations 007, native Windows Hello or operator v6/v7/profile, logs/backups, markers/recovery.

M3.2 IN_PROGRESS_NOT_ACCEPTED ~45% engineering estimate, writer/R1–R9 NOT_PROVEN, G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE, historical PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED; glib #160 OPEN_NOT_REMEDIATED. PRODUCT_FIRST_PARALLEL_SAFETY unchanged, notify before change. Must qualify parent postmain #42292721400, source Windows CI terminal SUCCESS exact final HEAD, reviews/threads, Protect main strict bypass=[], guarded squash expected_head_sha, independent postmain, issue #38 append-only. CI fixtures != admission real.
