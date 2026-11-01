# R4 — next gate: Windows multiprocess and three-file custody — DESIGN ONLY

1 November 2026. Parent protected main `7185adf3394b6d20d2c81a831c9226e8fa823f47`. **No new executable fixture, no runtime authorization, no production proof.**

## Verified baseline
PR #254, exact source `d965f883e47b0b60c653f479df1731897e8d656a`: [Windows source CI](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/41293719994) completed/success **292/7/66/176**; [independent postmain CI](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/41294534621) completed/success at `7185adf3394b6d20d2c81a831c9226e8fa823f47`, same counts. Both new tests of native delegated SQLite main and WAL Win32 HANDLE and FileId128 rejection passed. Reviews=[], threads=[], Protect main active strict bypass=[].

The registered NON-DEFAULT `#[cfg(all(test,windows))]` VFS returns xOpen SQLite files after actual `SQLITE_FCNTL_WIN32_GET_HANDLE` inspection, but WAL's expected FileId is checked via a separate by-name observation after open. This is NON ATOMIC. Native retained SHM is separate, not stock SQLite's private SHM handle. No atomic binding of main/WAL/SHM has been proved.

## Next candidate Windows CI fixture (NOT IMPLEMENTED)
1. Use only brand-new per-test `%TEMP%` artifacts, created with `CREATE_NEW`; retain native HANDLEs. Check volume serial + FileId128 for main/-wal/-shm when present. Never access operator SQLite v6/v7, pre-existing Greenfield, logs or backups.
2. Run two **OS processes** rather than two connections in one process. Both use the same named non-default test VFS in SQLite WAL NORMAL. Coordinate parent/child with bounded waits; writer A holds `BEGIN IMMEDIATE`, B must encounter lock refusal and later commit only after A commits. Verify toy rows in both processes, deterministic cleanup and fail-closed timeouts.
3. Capture each process's actual delegated `sqlite3_file` main/WAL native Win32 HANDLE identity and owned SHM FileId128, across xOpen, xShmMap, xShmLock, xShmBarrier, xShmUnmap, xClose; forbid missing or inconsistent identity. Test a WAL-index mapping beyond region 0 with explicit bounds/offset checks.
4. Under controlled timing on **disposable** files only, rename/replace a filename with a new-FileId decoy, document which live HANDLE remains stable, prove refusal where implemented and describe remaining TOCTOU race. A controlled interleaving does NOT prove freedom from all races.
5. Require an enforceable handle-bound lifetime and atomic identity binding or continue to refuse writer admission. Merely rechecking by pathname after xOpen is not atomic. The cooperative same-SID assumption is a threat-model premise, not a witness of writer absence.

## Qualification and STOP
Any future change needs exact-head Windows CI terminal success and job logs, diff/reviews/threads, active strict Protect main bypass=[], protected squash with expected_head_sha, independent postmain, and #38 append-only. R5/R6/R8 and R7/R9 remain independent gates. All proposed proof is CI-only.

**M3.2 IN_PROGRESS_NOT_ACCEPTED; writer/R1–R9 NOT_PROVEN; G2B NOT_ACCEPTED; G2C NOT_AUTHORIZED; real G3 STOP_UNAVAILABLE; historical PENDING_EXTERNAL_ATTESTATION(21/3/2); prospective NOT_STARTED; D3b-4/5 STOP.** No Tauri IPC writer, migration 007, native Windows Hello, durable marker, crash recovery, or operator access.

Primary APIs: [SQLite WAL](https://www.sqlite.org/wal.html); [SQLite Windows native handle file control](https://www.sqlite.org/c3ref/c_fcntl_begin_atomic_write.html); [Microsoft FILE_ID_INFO](https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_id_info).
