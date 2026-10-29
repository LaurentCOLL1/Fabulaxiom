# M3.2 P1 R4 — Second SQLite reader under EXCLUSIVE WAL (test-only)

**29 October 2026 — CANDIDATE, NOT QUALIFIED AT EXACT-HEAD WINDOWS CI.**

## Verified source baseline
PR #230 [source Windows CI #40943977390](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40943977390) **completed/SUCCESS** on exact source `71c28977ab7aeb7d27e6a2ddd92eb1718a3c10fd`: 250 Rust / 7 Greenfield / 46 SQLite inventory / 153 continuity, three named R4 experiments PASS. Protected squash produced `main=0db2577237874908bba5a2b1360921b2f4eb6277`; independently triggered [postmain CI #40947249730](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40947249730) must be checked on that exact SHA before being called PASS. Protect main active with strict Windows checks, no bypass.

## Why a second reader matters
With SQLite `locking_mode=EXCLUSIVE` set BEFORE WAL first access, WAL writes and reads can proceed without shared-memory callbacks. But this connection retains locks and an independent SQLite connection cannot be treated as an authorized P1 reader. SQLite's [WAL section 8](https://www.sqlite.org/wal.html) says the connection remains in EXCLUSIVE until leaving WAL, while the [PRAGMA documentation](https://www.sqlite.org/pragma.html#pragma_locking_mode) describes the lock and the limits for another process/connection.

The P1 product constraint should therefore be **one Rust SQLite owner with logical read requests** from the UI and local Ollama context retrieval, instead of silently opening more SQLite connections. This is a **candidate architectural decision**; no writer runtime/IPC implementation is enabled.

## Windows test scope
Both new tests are appended **inside the existing `r4_p1_exclusive_wal_disposable` module**, preserving the 26 original VFS fixtures and the preceding 3 R4 tests. All files are invented `%TEMP%/fabulaxiom-vfs-fixture-*/new.sqlite3`, created with `create_new(true)`. Existing `fresh_fixture(true,false)` opens the owner in exclusive WAL using the test-only VFS.

1. `m32_r4_exclusive_owner_refuses_second_sqlite_reader_without_ipc`: exactly one new scoped `Connection::open_with_flags_and_vfs(... SQLITE_OPEN_READ_ONLY ...)` reader site attempts a `SELECT` from the already live, owned fictional DB. The SQLite result must be `DatabaseBusy`, under 100 ms busy timeout; the owner continues reading normally and explicitly closes after the second reader drops. This verifies behavior of **an attempted competing SQLite reader**, not runtime security against malicious writers or a cross-process proof.
2. `m32_r4_exclusive_wal_owner_policy_refuses_normal_downgrade`: after exact-head Windows CI #40948171560 disproved the **test assumption** about the raw `PRAGMA locking_mode=NORMAL` result (`normal` was returned, versus the asserted `exclusive`), the candidate instead uses a **typed, test-only owner request dispatcher**. It rejects an explicit downgrade request *before* executing any SQLite locking-mode change; read requests still return the invented row count and the owner remains in exclusive WAL. This tests application-policy refusal only; it does **not** claim a native SQLite no-op or a production IPC guard.

**Prior exact-head CI #40948171560 FAILED** at source `e7c68509ea645a69b5d5925491b701682326e7df`: 251/252 Rust passed and the separate competing-reader test passed. The sole failure was the erroneous assumption that a raw locking_mode=NORMAL PRAGMA necessarily reports `exclusive`. That observation is retained, not reclassified as PASS. **Expected on corrective source, NOT YET CI PASS**: 252 Rust / 7 Greenfield / 47 source inventory / 154 continuity. One new SQLite opener and one `SQLITE_OPEN_READ_ONLY` token; whole-tree guard expected source fixture tuple `(24,0,0,0,0,25,0)`. Existing historical 26 tests are checked separately from the total R4 section of five tests; previous PR230 candidate facts remain historical.

## Limits, STOP and next
- Neither R3 controlled VFS `xOpen` atomicity nor R4 production custody are proven. The second connection is still a disposable CI test, not an admitted reader in Fabulaxiom.
- `A0 EXISTING_PROFILE STOP`, `M3.2 IN_PROGRESS_NOT_ACCEPTED`, production writer and R1–R9 `NOT_PROVEN`, G2B `NOT_ACCEPTED`, G2C `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`, historical `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`; #215/#35 DRAFT.
- No production v6/v7 SQLite, operator WAL/-shm, ACL, backup, S3/S4, IPC, migration 007, marker, recovery, native Windows Hello, Ollama runtime activation or external profile reading.
- Require exact-head Windows CI with both new named tests PASS, diff/reviews/threads check, strict active Protect main zero bypass, squash `expected_head_sha`, independent postmain CI and factual issue #38 append-only. Then choose a controlled SQLite VFS consuming pre-admitted HANDLE for R3, and design P1 serial reads using a single owner rather than independent SQLite file opens.
