# Fabulaxiom M3.2 — P1 R2→R3 held ancestors to SQLite-opened native HANDLE

**29 October 2026 — TEST-ONLY CANDIDATE. NO EXACT-HEAD WINDOWS CI YET. NO PRODUCTION ADMISSION.**

## Ground truth / baseline

Protected [PR #224](https://github.com/LaurentCOLL1/Fabulaxiom/pull/224) merged from `73d1a2c2ca185458046de5a1275f0b9671c956b5` into **`main=c7b19ff4e695eeb88598db7274da0fda756a03c4`**. Windows source [CI #40889773089](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40889773089) and independently postmain [CI #40891993272](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40891993272) both **completed/SUCCESS**: **237 Rust / 7 Greenfield / 44 SQLite source guards / 151 continuity**. The four R2 tests are qualified on disposable CI roots only. Ruleset Protect main active, strict required Windows status, zero bypass; #215 and #35 remain draft.

## New boundary: a *real SQLite xOpen* must match an already-held preflight main

A distinct `#[cfg(all(test, windows))]` Rust file `src-tauri/src/m32_r23_sqlite_handle_boundary_tests.rs` creates only **fresh test-owned** `%TEMP%/fabulaxiom-r23-delegated-disposable-*/fictional-profile/database/invented.sqlite3`. It is a zero-byte file made with exclusive `create_new(true)`, not an existing profile. Three ancestor handles stay open during pre/post checks with `FILE_FLAG_BACKUP_SEMANTICS | FILE_FLAG_OPEN_REPARSE_POINT`, `FILE_READ_ATTRIBUTES`, and sharing READ+WRITE (no DELETE). Their `FILE_ID_INFO` volume and 128-bit IDs are revalidated before and after the SQLite call.

One audited test-only `Connection::open_with_flags(..., SQLITE_OPEN_READ_WRITE)` site (no CREATE) allows SQLite to perform its **actual Windows VFS xOpen** on that newly created empty fixture. Immediately afterward, before SQL, `sqlite3_file_control(..., SQLITE_FCNTL_WIN32_GET_HANDLE)` borrows the actual SQLite native main HANDLE and compares `FILE_ID_INFO` with the previously observed fixture main identity. The borrowed handle is never closed manually. SQLite connections are explicitly closed. **Even if the comparison succeeds, the result stops at `R4MappingUnproven`; no writer/admission token is created.** SQLite may have already had opening-time side effects, so a post-xOpen identity comparison is **not** an atomic pre-open authorization.

Four tests target:
1. Held-ancestor/FileId128 match with real SQLite-opened main HANDLE on only a new test file.
2. Wrong file at the expected name **before SQLite open**: refuse by main FileId128 comparison.
3. Unknown artificial `-wal`, `-shm`, or `-journal` sidecar: refuse before SQLite and preserve exact sentinel bytes.
4. Deterministic substitution **between successful precheck and real SQLite xOpen**: a different test-owned file appears at that name; SQLite opens it, then the FileId128 mismatch vetoes further use. No application SQL or recovery is attempted.

## Acceptance / limits

**Expected only (NOT PASS yet): 241 Rust / 7 Greenfield / 45 SQLite source guard / 152 continuity tests**, exact SHA Windows CI mandatory. Prior R2 4 fixtures, P1 5 fixtures, D3b-5 4 fixtures and historical 26 VFS witnesses must remain unchanged byte-for-byte. The new source includes **one exact reviewed SQLite opening expression** and no migration, ATTACH, backup, real SQLite recovery, Tauri commands or new IPC. The source-only inventory is an occurrence tripwire, not a full parser or formal proof.

**This is NOT an R3 atomic identity proof.** The file may be substituted *before* `xOpen`; a post-open veto happens after SQLite has already touched the substituted object. A production solution needs controlled VFS delegation or stronger OS-handle handoff preventing unauthorized opening-time effects. **R4 WAL/-shm identity, mapping, locking, and xShm callbacks are NOT_PROVEN by this test**; distinct historical D2/D3a test-only fixtures remain the witnesses for those surfaces. Real root SID/DACL and A0 existing-profile admission remain out of scope. No asserted power-failure durability, custom marker or predecessor session provenance.

No access to operator `M:\Fabulaxiom`, `%LOCALAPPDATA%\com.fabulaxiom.greenfield.v1`, production v6/v7 SQLite, sidecars, backup/ACL/journals/markers. No new UI or writer functionality. No native Windows Hello, Ollama, S3/S4 or migration 007.

**STOP:** A0 `EXISTING_PROFILE STOP`; M3.2 `IN_PROGRESS_NOT_ACCEPTED`; writer and production R1–R9 `NOT_PROVEN`; G2B `NOT_ACCEPTED`, G2C `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`; historical `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`; PRs #215/#35 `OPEN/DRAFT`. Strict Protect main, exact-head Windows CI, diff, reviews, threads, protected `expected_head_sha` merge, independent postmain CI, and issue #38 append-only required for any further promotion.

References: [Microsoft Directory Handles](https://learn.microsoft.com/en-us/windows/win32/fileio/obtaining-a-handle-to-a-directory), [GetFileInformationByHandleEx](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-getfileinformationbyhandleex), [SQLite Windows file control](https://www.sqlite.org/c3ref/c_fcntl_begin_atomic_write.html), [SQLite WAL](https://www.sqlite.org/wal.html).
