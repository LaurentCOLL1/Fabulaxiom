# R4 — real SQLite xShmMap callback region-0 vs held live SHM bytes — test-only

**31 October 2026 — CANDIDATE, NOT QUALIFIED until exact-head Windows CI.** Protected parent `main=f71952119874b45555fbe9ea6dd2151f52123207`. PR #247 [source CI #41204712973](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/41204712973) SUCCESS 281 Rust / 7 Greenfield / 59 inventory / 169 continuity, independent [postmain #41205668071](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/41205668071) SUCCESS at exact main.

## New bounded experiment

The existing test-only Win32 VFS wrapper (D2/D3a) already intercepts and delegates the **real SQLite** `xShmMap/xShmLock/xShmBarrier/xShmUnmap`. Extend its main-file `xShmMap` callback to capture region-0 memory pointer and declared size only on `SQLITE_OK`. Add exactly one NEW Rust test on a brand-new `%TEMP%` invented SQLite WAL database, whose main and WAL handles pass the previously established D3a fixture gates. While SQLite remains open but is idle after committed fictional SQL, copy **136 bytes** from the actual region-0 pointer into an owned buffer; read 136 bytes from the separately held live `-shm` via FileExt and compare exact equality, native-order iVersion=3007000 at both copies and initialized flag; compare held FileId128 before and after. Drop held file before clean SQLite close and verify xShmUnmap/close successes. Never read mapping after SQLite close.

**Precise limitation:** Passing does not authenticate the **internal OS HANDLE** of stock SQLite's `winShmNode.hSharedShm`, nor prove that a separately opened pathname is atomically the mapped file at every point in time. Equality of 136 WAL-index bytes and a stable separately held FileId128 is NOT atomic custody of main/-wal/-shm. No custom runtime writer or operator opening, no crash recovery.

**Expected, not PASS until CI:** 282 Rust / 7 Greenfield / 60 SQLite source inventory / 170 continuity. One new reviewed SQLite opener inside `#[cfg(all(test,windows))]` and one `SQLITE_OPEN_READ_WRITE` flag. Keep fail-closed whole-tree inventory, previous tests and stops; full diff and reviews, strict active Protect main bypass=[], protected squash expected_head_sha only after success, independent postmain, issue #38 append-only.

**STOP:** M3.2 IN_PROGRESS_NOT_ACCEPTED, writer/R1–R9 NOT_PROVEN, G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE, historical PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED. No operator v6/v7/backups, existing Greenfield profile, migration 007, writer IPC, native Hello, persistent marker or recovery.

References: [SQLite WAL-index](https://www.sqlite.org/walformat.html), [SQLite xShm methods](https://www.sqlite.org/c3ref/io_methods.html), [SQLite Win32 source](https://github.com/sqlite/sqlite/blob/master/src/os_win.c).
