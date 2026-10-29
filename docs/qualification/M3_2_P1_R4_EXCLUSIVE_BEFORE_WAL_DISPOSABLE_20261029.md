# M3.2 P1 — R4 exclusive-before-WAL comparison (Windows CI disposable only)

**29 October 2026 — UNQUALIFIED EXPERIMENT, NO PRODUCTION WRITER ADMISSION.**

## Live verified base
Protected source `main=ea269a7c9e46500646a490469604c015e501f9ac` after [PR #229](https://github.com/LaurentCOLL1/Fabulaxiom/pull/229) (exact head `eeb33ab43fc5cdda2b137c41d9d91791a1aacc8a`, source [CI #40938677215](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40938677215) SUCCESS). Independent [postmain push #40940373025](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40940373025) was independently re-fetched, **completed/SUCCESS** on exact main, proving 247 Rust / 7 Greenfield / 45 SQLite inventory / 152 continuity only on that main. Active strict Protect main ruleset #24895490, no bypass; #215/#35 remain OPEN/DRAFT.

## Why R4 has a smaller testable P1 path
SQLite's [WAL documentation, section 8](https://www.sqlite.org/wal.html) states that `PRAGMA locking_mode=EXCLUSIVE` *before the first WAL access* avoids the `xShmMap/xShmLock/xShmBarrier/xShmUnmap` interface and a shared-memory wal-index file. That is a **configuration option**, not a guarantee that no `-wal` exists or that a SQLite process is a trusted owner. Once SQLite creates the shared-memory index under NORMAL locking, switching to EXCLUSIVE late does **not** undo the earlier mapping. For the selected P1 single Rust owner, the question is whether this narrower locking model is compatible with the app's intended readers and lifecycle.

## Three real SQLite Windows-only tests (NOT PASS before CI)
All changes are inside existing `#[cfg(all(test, windows))]` `m32_sqlite_vfs_preopen_tests.rs` and reuse the audited `RegisteredFixtureVfs` / D3a WAL/SHM Win32 instrumentation. A SINGLE new `Connection::open_with_flags_and_vfs(... SQLITE_OPEN_READ_WRITE)` call occurs in a local helper using `DisposableRoot::new()` and `create_new(true)`. Every case owns a new fictional SQLite database, makes one invented table and row, then explicitly closes its connection. No operator data or existing database is opened.

1. `m32_r4_exclusive_before_wal_avoids_every_wrapped_shm_callback`: order EXCLUSIVE, WAL, table/insert; WAL exists while live and native WAL identity matches; all four SHM callback counters remain zero; `-shm` never appears; explicit `xClose` observed.
2. `m32_r4_exclusive_before_wal_succeeds_with_shm_map_veto_armed`: install a wrapper that returns `SQLITE_IOERR_SHMMAP` if called; with early EXCLUSIVE, the same invented write and read succeed without triggering it.
3. `m32_r4_exclusive_after_wal_does_not_undo_existing_shm_mapping`: order NORMAL WAL, table/insert, **then** EXCLUSIVE; `-shm` and mapped/locked/barrier callbacks are witnessed and unmap occurs at close. The late switch is **not** accepted as equivalent to early EXCLUSIVE.

Expected counts at candidate head **250 Rust / 7 Greenfield / 46 SQLite source guards / 153 continuity** — **NOT PASS** until exact-head Windows CI. Old fixtures D2/D3a/D3b, PR #225–#229 remain historically qualified on their own old SHA; no retroactive rewrite of those facts. The whole-tree source inventory changes only the already reviewed R4 fixture from `(22,0,0,0,0,23,0)` to `(23,0,0,0,0,24,0)` and adds one source guard; audit occurrences, not runtime safety.

## Gate and unresolved risks
- R3 still **NOT_PROVEN**: built-in SQLite Win32 `xOpen` is pathname-based and is not given the preflight/ReOpenFile HANDLE. Exclusive locking does not fix that.
- R4 still **NOT_PROVEN for production**: the experiment does not authenticate the `-wal` generation, exclude other processes or demonstrate every lock, close, crash/restart and power-failure property. P1 exclusive mode may prohibit a future second SQLite reader; consult snapshots through the one Rust owner rather than creating independent connections. A separately authorized, complete WAL/SHM and owner/lifecycle decision is required.
- A0 existing profile STOP; M3.2 IN_PROGRESS_NOT_ACCEPTED; writer/R1–R9 production NOT_PROVEN; G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE; historical PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED. No actual `M:\\Fabulaxiom`, `%LOCALAPPDATA%\\com.fabulaxiom.greenfield.v1`, native Windows Hello, real SQLite, backup, ACL, journal, marker, migration 007, writer IPC, external process recovery or Ollama runtime.
- PRs #215/#35 stay DRAFT; #38 may receive only factual append-only evidence.

**Promotion contract:** exact-head CI all tests SUCCESS and specifically named tests PASS; review diff + reviews/threads, strict Protect main zero bypass, `expected_head_sha` merge; independently verify postmain push CI; append-only #38 and update both prompts/handoff/roadmap. Until this happens, leave candidate as NOT_QUALIFIED.

References: [SQLite WAL without shared memory](https://www.sqlite.org/wal.html), [SQLite VFS contracts](https://www.sqlite.org/vfs.html), [Win32 ReOpenFile](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-reopenfile).
