# R4 two Windows OS processes, SQLite WAL NORMAL and held native SHM — CI-only candidate

1 November 2026. Parent protected `main=c6ed181e80b807eafaa6b96f193555bf873e48e4` (#255 merged), [source #255 CI #41304442868](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/41304442868) terminal SUCCESS **292 Rust / 7 Greenfield / 66 inventory / 176 continuity**; independent #255 postmain [#41307543429](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/41307543429) requires terminal recheck. This is a NEW **NOT QUALIFIED** R4 candidate. **294/7/67/177 EXPECTED ONLY** until exact source Windows CI.

## Bounded runnable scope

Under the existing `#[cfg(all(test,windows))]` non-default registered VFS only, the parent constructs a new direct `%TEMP%` `CREATE_NEW` SQLite main and native SHM, a new-only proof stamp, and starts a real child OS process using `std::env::current_exe()` with Rust test harness `--exact`. The child accepts only its fresh direct `%TEMP%` prefix and the proof stamp and never performs `Scratch::drop` cleanup on a parent's fixture.

Both processes independently call `Connection::open_with_flags_and_vfs`, each observes actual delegated SQLite main and WAL Win32 `HANDLE` FileId128 (by `SQLITE_FCNTL_WIN32_GET_HANDLE`) and each independently owns a native SHM `HANDLE`. After the parent holds `BEGIN IMMEDIATE`, the child requires `SQLITE_BUSY` (or `SQLITE_LOCKED`) rather than any generic failure, writes an invented `child-observed-wal-busy` signal, waits for bounded `parent-committed` handshake, and then commits a toy row. Parent requires final sum `11+13=24`, child successful exit, and native WAL/SHM counters. Child lifetime and signals are bounded to 20 seconds and source code has no app/runtime opening path.

**Explicit limitations:** This does NOT prove malicious same-SID contention, resistance to all interleavings, filesystem alias/reparse race freedom, atomic custody of main/-wal/-shm, independently preowned WAL by handle, stock SQLite private SHM handles, wal-index pages above region 0, or crash recovery. Child handshake files are disposable TEST markers, not an operator persistent marker. The existing name-based WAL postopen observation remains NON ATOMIC.

## Qualification gates / STOP

No promotion before exact-head terminal Windows CI/logs (new tests and **294/7/67/177**), audited file diff/reviews/threads, strict active Protect main bypass=[], squash with `expected_head_sha`, independent postmain and issue #38 append-only. No runtime VFS, Tauri IPC writer, migration 007, native Windows Hello, operator v6/v7 or existing Greenfield profile access, backups or journals, durable marker or recovery.

**M3.2 IN_PROGRESS_NOT_ACCEPTED; writer/R1–R9 NOT_PROVEN; G2B NOT_ACCEPTED; G2C NOT_AUTHORIZED; real G3 STOP_UNAVAILABLE; historical PENDING_EXTERNAL_ATTESTATION(21/3/2); prospective NOT_STARTED; D3b-4/5 STOP.** Next R4 after this candidate: wal-index SHM regions >0 and atomic handle-bound lifetime; separate from admission.

Reference: [SQLite WAL and writers](https://www.sqlite.org/wal.html), [PR #255](https://github.com/LaurentCOLL1/Fabulaxiom/pull/255).
