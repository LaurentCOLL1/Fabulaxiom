# Fabulaxiom M3.2 v7 — D3b-5 bounded Windows CI crash-phase refusal matrix (29 October 2026)

**STATUS: NEW TEST-ONLY CANDIDATE; EXACT-HEAD CI NOT YET QUALIFIED. NO RUNTIME OR OPERATOR AUTHORIZATION.**

## Ownership and stage boundary

The owner explicitly authorized the next D3b-5 tests only on **fresh, disposable Windows CI fixtures**. The existing D2/D3a/D3b Windows tests were ported to protected `main` through PR #220 and independently postmain-qualified by CI #40856632214: **224 Rust / 7 Greenfield / 41 SQLite inventory / 148 continuity**, 26 VFS tests. Those numbers qualify **that SHA only**. Original PR #215 remains OPEN/DRAFT. D3b-4 (durable marker/replay) is **NOT IMPLEMENTED**; the provisional name D3c/R7 is a design, not a new admission gate.

This is a **bounded first D3b-5 phase matrix**, not all of the lower-level callback timing originally proposed in D3. A new `#[cfg(all(test, windows))]` Rust module creates new `%TEMP%/fabulaxiom-d3b5-disposable-*/new.sqlite3` files through OS `create_new(true)`. One child of the *same Rust test binary* may open that new, test-owned main using `SQLITE_OPEN_READ_WRITE` (no create flag), set WAL on a **new** fixture, issue fictional SQL, then exit with Win32 `TerminateProcess`. Parent performs **only filesystem metadata** inspection, refuses `RECOVERY_REQUIRED_NOT_AUTHORIZED`, and never opens SQLite on the terminated child's file. The owned temporary directory is destroyed only after the child process has exited. No WAL/-shm file is individually removed, renamed, repaired, copied or replayed.

## Observed phase brackets (not intra-callback preemption)

| CI child phase | Fixture action before child termination | Parent's asserted outcome |
|---|---|---|
| before_commit | BEGIN IMMEDIATE + fictional INSERT, no COMMIT | refuse |
| after_commit | completed fictional INSERT in WAL | refuse |
| before_checkpoint | completed fictional INSERT, no checkpoint command | refuse |
| after_checkpoint | completed fictional INSERT + PASSIVE checkpoint on same already-open fixture connection | refuse |
| before_close | completed fictional INSERT, connection remains open | refuse |
| after_close | completed fictional INSERT + successful explicit `Connection::close()`, **then** terminate process | refuse |

These are **operation-level** before/after boundaries, not precisely injected crashes *inside* SQLite's commit, WAL xSync, checkpoint xSync, SHM xShmUnmap or sqlite3_close. `PRAGMA synchronous=FULL` is used only in a new fictional CI database and does not prove that a particular VFS sync callback was hit at the moment of termination. A crash of the test child is not a disk power failure and cannot prove durable transaction survival on a real Windows machine. Any intra-callback xSync/xShmUnmap crash injection and failure-specific callback evidence **remain NOT_PROVEN**, requiring independent review and approval before claiming D3b-5 complete.

## Source guards and acceptance

1. Keep the previous **26-test VFS module unchanged byte for byte**: the historical SHA-pinned #215 → #220 proof and its contract #148 remain valid. This new module is separate, Windows test-only, never registered as runtime Tauri State/command/IPC. The new SQLite opening site is admitted **only** to the explicit textual source-inventory tuple (1,0,0,0,0,1,0), with source guard and corresponding new negative check; this audit is not a parser or OS permission proof.
2. Test child helper plus three negative matrix tests = **four** additional default Rust unit tests. Expected new totals: **228 Rust / 7 Greenfield / 42 SQLite inventory / 149 continuity**, before running exact SHA Windows CI; no numerical PASS claimed until logs confirm it.
3. Verify no path to `M:\Fabulaxiom`, `%LOCALAPPDATA%\com.fabulaxiom.greenfield.v1`, operator v6/v7 SQLite, production WAL/-shm, backups, ACL, activation marker or journals; no original source is opened, no writer activation, no durable marker, no new recovery/IPC/migration 007/Windows Hello/Ollama runtime.
4. Re-fetch `main`, check `Protect main` strict/no bypass, diff, reviews and threads, CI at **exact head SHA** and expected counts. Protected merge only with expected-head lease after qualification; independent postmain CI and issue #38 append-only. Do not confuse green CI with R1–R9 admission.

## Hard STOP and next decision

A0 `EXISTING_PROFILE STOP`; R1–R9 production and writer `NOT_PROVEN`; M3.2 `IN_PROGRESS_NOT_ACCEPTED`; G2B `NOT_ACCEPTED`; G2C `NOT_AUTHORIZED`; G3 `STOP_UNAVAILABLE`; historical `PENDING_EXTERNAL_ATTESTATION(21/3/2)`; prospective `NOT_STARTED`; #35 and #215 remain DRAFT. No automatic profile reopen or recovery, no testing on operator Windows storage, no durable witness. Even a successful SQLite close cannot attest authenticated cross-process predecessor provenance.

SQLite references: [WAL format and recovery](https://www.sqlite.org/wal.html), [WAL format](https://www.sqlite.org/walformat.html), [atomic commit and simulated power failure](https://www.sqlite.org/atomiccommit.html).
