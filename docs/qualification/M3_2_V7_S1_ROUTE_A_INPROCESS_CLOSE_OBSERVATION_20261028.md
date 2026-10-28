# M3.2 v7 S1 — In-process explicit close observation, Route A (28 October 2026)

## Exact boundary — CANDIDATE NOT QUALIFIED

Base PR #209 terminal: source `eaece112657c6b8f48f7a3ff2765c003ed71653c`, source Windows CI #40680131261 SUCCESS, protected squash `main=d9addd56caccdb1e5206d0838d3437e60cb63a6b`, independent postmain #40681546576 SUCCESS, **201 Rust / 7 Greenfield / 41 SQLite guards / 140 continuity contracts** on both, issue #38 terminal comment 6468161590. Route A controlled private namespace; owner authorizes S1/S2 Rust and strictly disposable Windows fixtures only.

The following candidate does **not** build a persisted clean-stop marker. Two new `#[cfg(all(test, windows))]` Rust witnesses use *only newly created disposable SQLite connections*:

- Explicit `Connection::close()` success yields `CleanlyClosed` **only as an in-process observation**. That permits selecting an `ExistingProfile` **preflight candidate** for the same `com.fabulaxiom.greenfield.v1`, never an admission token.
- Implicit Drop has no observable explicit-success result. Even if the disposable path exists and passes the filesystem preflight, simulated unknown lifecycle must be refused. This is **not a crash test**; after real crash, WAL recovery and provenance require a distinct design.

These are 2 additional test-only SQLite opening sites, reviewed in the static inventory. No runtime code, no trusted source of a prior-process clean-stop observation, no durable record, no operator marker, no real SQLite, no VFS, no atomic xOpen file identity, no absence of foreign writer. This test deliberately does not infer clean shutdown from missing `-wal`, `-shm`, or `-journal` files: SQLite WAL last-close cleanup and crash recovery have concurrent locking behavior (official SQLite WAL documentation). An `Ok(())` from a toy `close` does **not** authorize reopening an operator profile.

Expected CI after this change: **203 Rust / 7 Greenfield / 41 SQLite guards / 141 continuity contracts** — **NOT PASS until source SHA and independent postmain prove it**. At this point S1 can represent the concept, but safe provenance across restarts is still unproven. Any durable marker/protocol or runtime activation is outside this PR and requires fresh scope review and authorization.

## STOP unchanged

M3.2 `IN_PROGRESS_NOT_ACCEPTED`; G2B `NOT_ACCEPTED`; writer `NOT_PROVEN`; G2C `NOT_AUTHORIZED`; G3 `STOP_UNAVAILABLE`; historical `PENDING_EXTERNAL_ATTESTATION(21/3/2)`; prospective `NOT_STARTED`; #35 OPEN/DRAFT. No S3/S4, IPC/CRUD writer, migration 007, native Windows Hello, operator SQLite v6/v7, backup, ACL, sidecar, log, journal, or marker access. No operator execution.
