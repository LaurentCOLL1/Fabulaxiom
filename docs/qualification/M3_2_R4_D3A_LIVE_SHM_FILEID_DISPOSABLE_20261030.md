# M3.2 — R4 / D3a live SHM FileId128 (Windows fixture only)

**30 octobre 2026 — CANDIDAT NON QUALIFIÉ.** Parent protected main `fd6b7ccfd45d877ea34c5c02668660b3a17ffc27` from PR #243. Source PR #243 [Windows CI #41119276800](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/41119276800) completed/SUCCESS at exact PR head `9630eb43f4d3934b827109291c8e6c93f0036fe9`: 268 Rust / 7 Greenfield / 55 SQLite inventory / 165 continuity. Independent [postmain push #41123096907](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/41123096907) **IN_PROGRESS at drafting; re-fetch terminal SHA separately.**

## New narrowly bounded CI witness

`m32_r4_d3a_shm_fileid_stable_during_live_wrapped_wal_disposable` in `src-tauri/src/m32_sqlite_vfs_preopen_tests.rs`, reachable **ONLY** with `cfg(all(test,windows))` via existing test-only VFS Rust module. On a brand-new invented `%TEMP%` SQLite main:

- The existing D3a fixture delegates normal Win32 SQLite xOpen, checks the main FileId128 after delegated xOpen, checks WAL's delegated opened handle identity, and wraps all `xShmMap`, `xShmLock`, `xShmBarrier`, `xShmUnmap` and close.
- While the disposable WAL-mode SQL connection is alive, separately open the invented `-wal` and `-shm` with FILE_SHARE_READ|WRITE, hold FileId128 from each actual Win32 handle, ensure all three identities are distinct, issue a second **invented fixture SQL** insert and verify both held sidecar identities and freshly observed names continue matching.
- Explicitly release the test-only additional sidecar handles *before* the existing SQLite connection's close/checkpoint lifecycle; assert successful D3a SHM unmap and main/WAL xClose callbacks.

**What this does NOT prove:** SHM mapped handle ownership (xShmMap is still delegated to stock Win32 and may open its own file); atomic custody of main/WAL/SHM, protection against pathname ABA, a production preopened R3 xShm* VFS, cross-process authenticated lifecycle, repair, checkpoint durability, crash recovery, permission to use operator v6/v7 sidecars/backups or the existing Greenfield profile, native Hello, migration 007, durable marker, actual writer IPC, or M3.2 admission.

**Expected, NOT CI PASS until exact-head source CI and logs:** 269 Rust / 7 Greenfield / 56 inventory / 166 continuity. No changes to the runtime entrypoint. Only new fixtures, source guard counts, protected branch and continuity.

## Mandatory protected qualification

Exact PR HEAD, Windows status `completed/SUCCESS` and logs, full diff/reviews/threads, `Protect main` #24895490 ACTIVE strict required `Windows frontend and Rust checks`, bypass=[], protected squash using `expected_head_sha` only if admissible, independent postmain exact SHA, issue #38 append-only. Parallel code/document review allowed; never treat draft candidate as accepted.

**STOP:** M3.2 IN_PROGRESS_NOT_ACCEPTED; writer/R1–R9 production NOT_PROVEN; G2B NOT_ACCEPTED; G2C NOT_AUTHORIZED; real G3 STOP_UNAVAILABLE; historical PENDING_EXTERNAL_ATTESTATION(21/3/2); prospective NOT_STARTED; D3b-4/5 and D3b-5 STOP; D3c design-only.

**Next architecture:** prove a handle-bound `xShm*` path for preopened R3 main with WAL/SHM identity pinned throughout transitions, on *new fixtures only*; until then fail closed. SQLite [WAL](https://www.sqlite.org/wal.html) and [WAL-index](https://sqlite.org/walformat.html) are normative context, not admission.
