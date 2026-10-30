# M3.2 R3 — two simultaneous read-only SQLite Win32 SHARED readers (disposable only)

**30 October 2026 — candidate, source CI NOT YET QUALIFIED.** Parent protected `main=89135b95babeebb7c2f4a15506841e9527b93a3c` after PR #240 exact-head source CI [#41069738923](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/41069738923) completed/SUCCESS 265 Rust / 7 Greenfield / 52 SQLite inventory / 162 continuity. Independent postmain CI [#41074346064](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/41074346064) must be checked separately at that merge SHA.

## Windows fixture witness

The unchanged test-only `#[cfg(all(test, windows))]` read-only SQLite VFS clones each pre-held FileId128-identical HANDLE with `ReOpenFile`. On a freshly invented `%TEMP%` database, the test `m32_r3_two_sqlite_readers_retain_shared_until_last_connection_closes` opens two independent SQLite READ_ONLY connections and starts two separate BEGIN/SELECT transactions. Both own native SHARED `LockFileEx` locks simultaneously. A third independent Win32 HANDLE cannot take overlapping EXCLUSIVE while both are alive. After dropping the first SQLite connection without COMMIT, EXCLUSIVE must still fail because the second SQLite connection continues to own SHARED. Once the second connection closes, EXCLUSIVE must succeed and release; a fresh reader succeeds afterwards. FileId128 identity and absence of `-wal`, `-shm`, `-journal` are checked. No SQLite writer opens, no database is mutated.

Previous eight R3 tests remain. **Expected, not yet qualified by new CI: 266 Rust / 7 Greenfield / 53 inventory / 163 continuity**, including source-inventory tripwire #53 and continuity contract #163.

## What this does NOT prove

Not production-grade SQLite writer `xLock` state machine, not R4 WAL/SHM sidecar ownership, not production admission, not proof of recovery. `M3.2 IN_PROGRESS_NOT_ACCEPTED`, writer/R1–R9 `NOT_PROVEN`, G2B `NOT_ACCEPTED`, G2C `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`, historical `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`. Existing profile A0 STOP. No operator v6/v7, sidecars/ACL/backup, writer IPC, migration 007, native Windows Hello, persistent marker or crash recovery.

## Qualification and next

Verify source exact-head Windows CI and logs, diff, reviews/threads, strict Protect main bypass=[], protected squash only under expected_head_sha if all PASS, then independent postmain push CI, issue #38 append-only. Continue full R3 state machine and separately R4 WAL/SHM only on fresh disposable fixtures.

References: https://www.sqlite.org/c3ref/io_methods.html ; https://www.sqlite.org/lockingv3.html ; https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-lockfileex
