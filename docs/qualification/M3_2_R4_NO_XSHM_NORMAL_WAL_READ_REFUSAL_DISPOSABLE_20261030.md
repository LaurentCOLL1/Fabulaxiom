# M3.2 R4 — normal WAL read refusal without xShm* (disposable candidate)

**30 October 2026 — UNQUALIFIED until exact-head Windows CI.** Base main `6166a256e479ef7cd3c1a6cacdaccaadb68cfb49` after PR #242 protected squash, exact PR #242 source [#41084067311](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/41084067311) completed/SUCCESS 267 Rust / 7 Greenfield / 54 SQLite inventory / 164 continuity. [Independent postmain #41110676555](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/41110676555) was IN_PROGRESS at drafting; independently re-check its terminal outcome.

## Bounded negative witness

New test `m32_r4_readonly_preopened_vfs_without_xshm_refuses_live_wal_disposable` only in `#[cfg(all(test, windows))]`. Creates an invented SQLite `%TEMP%` database and holds the standard SQLite Win32 writer on that **new test file only** while WAL and SHM exist. Attempts `NORMAL` locking read with the existing Fabulaxiom **test-only READ_ONLY** VFS using `sqlite3_io_methods.iVersion=1`, `xShmMap=None`, `xShmLock=None` and no custom WAL custody. Requires SQLite to refuse WAL reading (on open or first query) and verifies stock writer still reads unchanged invented content. No data outside test's unique new root is accessed.

SQLite's [WAL documentation](https://www.sqlite.org/wal.html) says a VFS without shared-memory methods cannot normally read a WAL database in NORMAL mode. The EXCLUSIVE-before-first-access exception **does not authorize bypassing R4** and is not used here.

**Expected, NOT PASS until CI:** 268 Rust / 7 Greenfield / 55 SQLite inventory / 165 continuity.

This negative result does **not** prove positive xShm* forwarding, atomic WAL/SHM FileId128 custody, multi-process correctness, checkpoint, crash recovery, real R1–R9, or writer admission. No production change, no operator v6/v7 or existing Greenfield profile, IPC, migration 007, Windows Hello native, persistent marker or recovery.

**STOP:** M3.2 IN_PROGRESS_NOT_ACCEPTED ; writer/R1–R9 NOT_PROVEN ; G2B NOT_ACCEPTED ; G2C NOT_AUTHORIZED ; G3 STOP_UNAVAILABLE ; historical PENDING_EXTERNAL_ATTESTATION(21/3/2) ; prospective NOT_STARTED. D3b-4/5 and D3b-5 STOP, D3c design only.

**Next:** exact HEAD Windows CI, diff/reviews/threads, active strict Protect main bypass=[], protected expected_head_sha squash if PASS, independent postmain and #38 append-only; then positive xShm* sidecar ownership on new fixtures, never promotion to production.
