# M3.2 R4 — default SQLite Win32 WAL/SHM disposable reference (candidate)

**30 October 2026 — NON QUALIFIÉ before exact-head Windows CI.** Parent protected `main=03a2b6206e49f0e7aac5b4acbdfcee2d98737b97` after PR #241 source HEAD `69176e3845acca5f304e696a42740e63812415b9`, [source CI #41075099123](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/41075099123) completed/SUCCESS (266 Rust / 7 Greenfield / 53 SQLite inventory / 163 continuity). Independent [postmain #41082491631](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/41082491631) pending terminal SHA check.

## Witness and limit
One `#[cfg(all(test, windows))]` Rust unit test on a newly invented `%TEMP%` root, using `create_new` for main and **stock SQLite Win32 VFS** (not Fabulaxiom preopened R3 VFS). Only the invented fixture gets a temporary RW writer and separate READ_ONLY reader. Verifies WAL mode, reader's fixed transaction snapshot during a new writer commit, new snapshot after COMMIT, WAL and SHM file existence while connections live, native FileId128 equality across two independent opens of **each separate file**, and disjoint file IDs. Drops test connections and deletes just the owned root.

**DOES NOT PROVE** custom VFS `xShmMap/xShmLock/xShmBarrier/xShmUnmap`, WAL/SHM handle ownership, atomic FileId128 binding across main/WAL/SHM, checkpoint/recovery, crash durability, or R3/R4 production. A stock-VFS temporary toy writer is NEVER the unwired Fabulaxiom writer. No existing profile, real v6/v7, their journals/backups, IPC, migration 007, native Hello, marker or recovery.

Expected **267 Rust / 7 Greenfield / 54 SQLite inventory / 164 continuity**, all **NOT YET QUALIFIED**. Required gates: exact HEAD Windows CI completed/SUCCESS with logs, diff/reviews/threads, active strict Protect main bypass=[], protected merge with expected_head_sha if PASS, independent postmain, append-only #38.

STOP: M3.2 IN_PROGRESS_NOT_ACCEPTED; writer/R1–R9 NOT_PROVEN; G2B NOT_ACCEPTED; G2C NOT_AUTHORIZED; G3 STOP_UNAVAILABLE; historical PENDING_EXTERNAL_ATTESTATION(21/3/2); prospective NOT_STARTED. Next R4 custom xShm* and sidecar guard only on separate disposable fixtures.
