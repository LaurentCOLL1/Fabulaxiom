# M3.2 R4 — SQLite WAL xOpen native associated-main file-object evidence (Windows disposable only)

5 November 2026. **CANDIDATE / NON QUALIFIÉ**, pending exact-head Windows CI and independently qualified protected merge. Parent protected `main=2d2d873a1110e2de934f4a1cb6abbe05ca99e218` from #294; independent postmain #42120910359 **NOT YET QUALIFIED** at authored checkpoint.

## Bounded mechanism

In the existing uniquely named **non-default** SQLite VFS, compiled only as `#[cfg(all(test,windows))]` and used exclusively on fresh `%TEMP%` `CREATE_NEW` fixtures, the `xOpen` callback now calls `ffi::sqlite3_database_file_object(name)` **only if the original SQLite flags include `SQLITE_OPEN_WAL`**, with the exact untouched `sqlite3_filename` passed by SQLite. This is the documented contract; NEVER call it for main, temporary, or unrelated strings.

The returned live associated main `sqlite3_file*` is interrogated using its own `xFileControl(SQLITE_FCNTL_WIN32_GET_HANDLE)`, followed by native Win32 `GetFileInformationByHandleEx(FileIdInfo)`. The real FileId128 must equal the independently held, newly invented main fixture identity before invoking delegated WAL `xOpen`. A missing owner object, absent handle, mismatched FileId128 or injected test-only negative flag returns `SQLITE_CANTOPEN` **before** the default WAL xOpen. A monotonic per-fixture counter records a successful main-owner match.

Two tests: an existing real delegated main/WAL native-identity test now asserts the counter; a new `r4_wal_xopen_sqlite_main_file_object_native_owner_veto_disposable` forces the test-only negative flag and verifies WAL SQL refusal, zero delegated WAL native matches and refusal counters. No runtime access or new VFS registration; default VFS remains unchanged.

The source-only SQLite-opening tripwire is explicitly reviewed **13 to 14** RW open sites/flags for this already `cfg(all(test,windows))` module, plus a new negative **inventory test_69** to ensure this code stays test-only and production writer remains `NOT_PROVEN`.

## Proof boundary

This proves, **if exact-head Windows CI passes**, an association of a WAL xOpen to a live SQLite main object and a refused injected owner mismatch. It does **not** replace delegated pathname-based WAL `xOpen`, atomically pin the WAL object, prove SHM provenance, guarantee indivisible main/WAL/SHM custody, eliminate unobserved ABA/TOCTOU, provide all WAL-index page lifetimes, or authorize hostile same-SID writers, recovery or production writer admission. The separate observed SHM ABA poison latch remains test-only and independent.

**EXPECTED, NOT PASS:** 322 Rust / 7 Greenfield / 69 SQLite inventory / 183 continuity / 373 Vitest, Chromium 85/85 normal+CSP, 19 pinned invented Git blobs. Qualification requires terminal CI at exact HEAD, audit complete diff/reviews/threads and active strict Protect main bypass=[], guarded squash `expected_head_sha`, independent postmain CI, #38 append-only.

**STOP:** `PRODUCT_FIRST_PARALLEL_SAFETY` unchanged, notify before changing strategy. `M3.2 IN_PROGRESS_NOT_ACCEPTED` (~45%, 40–50% engineering estimate); writer/R1–R9 `NOT_PROVEN`, real P4 STOP, G2B `NOT_ACCEPTED`, G2C `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`, historical `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`; glib #160 `OPEN_NOT_REMEDIATED`. No operator v6/v7, existing `%LOCALAPPDATA%\com.fabulaxiom.greenfield.v1`, backups/journals, IPC writer, runtime 007, native Hello, marker or recovery.

References: https://www.sqlite.org/c3ref/database_file_object.html ; https://www.sqlite.org/c3ref/file_control.html ; https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-getfileinformationbyhandleex
