# M3.2 v7 P1 — D3a Windows disposable WAL/SHM delegated-handle custody fixtures

**28 October 2026 — LAURENT EXPLICITLY AUTHORIZED D3a WINDOWS CI DISPOSABLE FIXTURES ONLY.** No D3b crash/restart, no production actor/writer/VFS, operator profile, SQLite v6/v7, migration 007, Tauri IPC, ACL, backup, real WAL/SHM, durable marker or Ollama runtime was authorized. The only Rust change is in **src-tauri/src/m32_sqlite_vfs_preopen_tests.rs**, already compiled solely through #[cfg(all(test, windows))]. This is a proposed CI candidate: **220 Rust / 7 Greenfield / 41 SQLite guards / 151 continuity contracts EXPECTED, NOT QUALIFIED, NOT PASS until exact source SHA Windows CI**.

This slice follows the [source-qualified D3 design](M3_2_V7_P1_D3_WAL_SHM_LIFECYCLE_CRASH_RESTART_DESIGN_20261028.md) at PR #215 SHA b1791ba59f8196bda0a95a8d55118a21d3ec9193, [Windows CI #40758512734](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40758512734) completed/SUCCESS 216/7/41/150. That prior CI qualifies the **documentary** D3 design only. D2 Windows disposable test evidence at c42a6f40 / #40753334640 SUCCESS 216/7/41/149 is also non-transferable to this new source.

## 1. Exact bounded fixture behavior

The test continues to use a freshly created DisposableRoot under the CI runner's %TEMP%, an exclusively created test-owned new.sqlite3 main file and the Windows default SQLite VFS registered under a unique test name (makeDflt=0). No operator path or existing profile can be opened. The already-approved P1 single Windows SID trusted/cooperative assumption is retained; this does not block a malicious peer under that SID.

**WAL identity boundary:** After the *default Win32 VFS* xOpen has returned a real sqlite3_file for SQLITE_OPEN_WAL, test-only xFileControl(SQLITE_FCNTL_WIN32_GET_HANDLE) retrieves the **delegated WAL native HANDLE**, and GetFileInformationByHandleEx(FileIdInfo) produces volume serial plus full FileId128. A second fs::File::open observation of the fixture-owned new.sqlite3-wal pathname is compared, along with expected -wal basename. An intentionally wrong expected ID is sourced from another disposable test-owned file. Failure => original delegated WAL xClose is called, pMethods cleared and SQLITE_CANTOPEN returned before success can reach SQLite. **The OS open and possibly sidecar creation have already happened.** Even two matching identities are not atomic pathname custody, durable origin evidence or a production write admission.

**SHM methods:** The aligned test-only io_methods tail on the main sqlite3_file wraps xShmMap, xShmLock, xShmBarrier, xShmUnmap and xClose, while delegating to the original Windows methods and observing counters. The D3a gate rejects absent xClose, xShmMap/xShmLock/xShmBarrier/xShmUnmap, version below 2, or a deliberately simulated missing xShmLock **at main xOpen** before any WAL/SHM use. An injected xShmLock refusal returns SQLITE_IOERR **before** the default lock; xShmBarrier is void and cannot signal an error mid-callback, so callback completeness must be rejected up front. No independent SHM backing-handle FileId128 is claimed from these callbacks.

**Close boundary:** The same disposable main and WAL xClose methods are wrapped separately. The positive witness uses explicit rusqlite Connection::close() before verifying xShmUnmap and successful delegated main/WAL closes. A successful close callback is **not** an authenticated clean-shutdown attestation or proof of power-loss durability. sqlite3_close_v2 deferred-resource semantics and crash/restart are outside D3a.

## 2. Four added Windows Rust tests (all new; D2 historical six preserved)

| Test | Expected synthetic witness | Unproven after PASS |
|---|---|---|
| m32_d3a_wal_real_delegated_fileid_all_shm_callbacks_and_close_positive_not_admission | Delegated main identity + delegated -wal native FileId128 match against the owned pathname; calls through xShmMap/xShmLock/xShmBarrier/xShmUnmap, then explicit SQLite close and separate original xClose successes for main and -wal | OS path/ancestor atomicity; -shm backing FileId128; durable close/restart |
| m32_d3a_wrong_expected_wal_fileid_vetoes_after_delegation_and_closes | Decoy test-owned FileId128 forces WAL veto after actual delegated xOpen and original WAL xClose; no SQL success after the veto | Never asserts no WAL side effects, true hostile swap, or safe automatic repair |
| m32_d3a_shm_lock_veto_after_wal_handle_binding_refuses_sql | Matching fixture WAL handle followed by xShmLock refusal before default locking and no successful SQL after STOP; gate relaxed only for test cleanup | No production lock ownership or global SHM provenance |
| m32_d3a_missing_shm_lock_method_refuses_at_main_xopen_without_wal | Simulated unavailable SHM method vetoes at main xOpen; no WAL open, SHM mapping or database SQL | No real Windows method-version downgrade, no production ABI negotiation |

All four added calls to Connection::open_with_flags_and_vfs and four SQLITE_OPEN_READ_WRITE occurrences remain inside this single already Windows-only test module. The whole-tree source inventory baseline **(16,0,0,0,0,17,0) -> (20,0,0,0,0,21,0)** for this path alone is reviewed explicitly; other SQLite opening paths and unknown drifts remain refused. Existing D2 source test count 18 becomes **22**, and new continuity contract #151 pins the exact 22 while historical witnesses remain present. No new production Rust module or feature gate.

## 3. Required qualification and limitations

1. Verify exact PR #215 HEAD/base main, Protect main strict required Windows check, reviews/threads; inspect this diff for new **test-only** paths and no operator execution. Run Windows CI from the exact source SHA; assert **220/220 Rust, 7/7 Greenfield, 41/41 SQLite guards and 151/151 handoff contracts**, all four new tests individually ok. Until that outcome: **EXPECTED, NOT PASS**.
2. Do not infer that a WAL xOpen verification covers the mapped -shm backing file. The wrapper observes the four callbacks, not an authenticated OS handle for its mapping. Do not infer that a default SQLite close verifies independent durable journal provenance.
3. Never use an OS-open, WAL/SHM, journal, checkpoint or cleanup on %LOCALAPPDATA%/M:\ Fabulaxiom paths. Test cleanup only removes the fixture-owned fresh temp directory after all owned connections close; no individual live WAL deletion.
4. D3b remains **NOT_AUTHORIZED / NOT_EXECUTED**: no process termination, mutex-loss simulation, replay/repair, existing-profile recovery, power-loss or persistent predecessor evidence in this scope. Additional checkpoint completeness and xShmUnmap error injection are not claimed by these four witnesses.
5. No runtime Ollama access is added. Future M4–M7 creative models receive only in-memory, revision-pinned and source-cited fiches/histories/canon/chronology context from the single Fabulaxiom Rust session actor, without SQLite/SQL/writer access; generated canon requires human APPROVE_CANON.

**All production R1–R9 remain NOT_PROVEN.** M3.2 IN_PROGRESS_NOT_ACCEPTED; G2B NOT_ACCEPTED; G2C NOT_AUTHORIZED; real G3 STOP_UNAVAILABLE; writer NOT_PROVEN; A0 cross-process EXISTING_PROFILE STOP; historical PENDING_EXTERNAL_ATTESTATION(21/3/2); prospective NOT_STARTED; PR #35 OPEN/DRAFT; PR #215 OPEN/DRAFT and no postmain until a separately authorized protected merge. S3/S4, IPC/CRUD, 007, native Windows Hello, marker, operator SQLite/ACL/backups/sidecars and Ollama runtime STOP. A future D3b or production admission requires a new separate owner authorization.

## Primary technical sources

- [SQLite io_methods complete SHM callback table and failed xOpen/xClose](https://www.sqlite.org/c3ref/io_methods.html)
- [SQLite VFS xOpen and SQLITE_OPEN_WAL flags](https://www.sqlite.org/c3ref/vfs.html)
- [SQLite WAL file lifecycle and SHM wal-index](https://www.sqlite.org/wal.html)
- [SQLite SQLITE_FCNTL_WIN32_GET_HANDLE](https://www.sqlite.org/c3ref/c_fcntl_begin_atomic_write.html)
- [Microsoft GetFileInformationByHandleEx / FileIdInfo](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-getfileinformationbyhandleex)
- [SQLite sqlite3_close and sqlite3_close_v2](https://www.sqlite.org/c3ref/close.html)
