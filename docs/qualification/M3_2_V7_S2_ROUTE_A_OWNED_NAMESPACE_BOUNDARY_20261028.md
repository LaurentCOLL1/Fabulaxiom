# M3.2 v7 — S2 Route A, controlled namespace boundary (28 October 2026)

**Candidate only; NOT CI-qualified and not atomic admission.** Base PR #207 terminal: source `13a06d9dba3a590387f76f4d489a05228ba5c680`, exact source CI #40670160771 SUCCESS, protected squash `main=14d0975def302f0856eab368026928eef73c547c`, independent postmain #40671818268 SUCCESS; both runs **197 Rust / 7 Greenfield / 41 SQLite guards / 138 handoff contracts PASS**, terminal issue #38 comment 6466735059. `Protect main` active and strict. Architectural STOP issue #38 comment 6466800502.

Laurent explicitly selected **Route A**: a bounded threat model with a private controlled namespace, rather than a custom Win32 VFS. Authorization remains S1/S2 preparatory Rust and fresh disposable Windows fixtures only. Route A does **not** authorize production runtime, a new app identity, operator access, S3/S4, writer IPC, migration 007 or native Hello.

## Threat model and explicit trust assumption

- The sole logical profile stays `com.fabulaxiom.greenfield.v1`. A **controlled namespace** means the S2 fixture creator owns a newly created unique runner temporary root and no other participant intentionally mutates it during a positive preflight. This is an explicit assumption, **not** a theorem about Windows ACLs or privileged/local adversaries.
- An untrusted pathname is never a capability. The test-only `owned_namespace_preflight` accepts only the exact expected database path derived from its own fixture root; unrelated profiles, lexical escapes and arbitrary callers are refused.
- The root, profile directory, and database directory are required to be actual directories without `FILE_ATTRIBUTE_REPARSE_POINT` observed by Windows metadata. The main file, when present, is also rejected if it has that attribute. Unknown metadata failures fail closed. The bit-predicate is separately exercised; this candidate does not claim a live junction/symlink fixture or universal detection of every Windows name indirection.
- An existing parent that disappears is refused. If an actor replaces it *after* a successful preflight, another positive path check still cannot bind the later SQLite `xOpen`; the test explicitly keeps `HandoffNotAtomic`. No new `V7WriterAdmission` constructor exists, and the writer remains unregistered with Tauri/IPC.
- Sidecar `-wal`, `-shm`, `-journal` metadata remains fail-closed; no authenticated recovery or ownership of existing sidecars has been demonstrated. External writer absence is `NOT_PROVEN` and SQLite `BEGIN IMMEDIATE` cannot prove it.

## Source-only/test-only qualification scope

Two additional Windows-only fixtures in the existing `#[cfg(all(test, windows))]` module: (1) positive owned-root preflight plus refusal of a separate fixture root and lexical escape; synthetic reparse attribute bit checks; (2) parent rename, refusal while absent, replacement and explicit refusal of any unbound handoff. **These are preflight contract checks, not a safe SQLite opener.**

Before CI at the new SHA, **199 Rust / 7 Greenfield / 41 SQLite inventory guards / 139 continuity contracts are EXPECTED, NOT PASS**. Full diff/reviews/threads, active strict `Protect main`, exact-head Windows CI, `expected_head_sha` squash, independent postmain at the new SHA and append-only issue #38 comments are mandatory. A failure remains a STOP and requires a fresh SHA/CI.

**Residual, hard STOP:** a real profile's ancestor custody/ACLs, junction/reparse resistance across the entire namespace, atomic transfer of an opened Win32 handle into SQLite's I/O stack, `xShmMap` and sidecar recovery, crash/power-loss behavior, and foreign writers remain unproved. This Route A preflight is **not atomic** and **no operator** file may be accessed. M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, external writer `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`, historical `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 OPEN/DRAFT; S3/S4 prohibited.

Official boundaries: SQLite `sqlite3_open_v2` does not make `SQLITE_OPEN_EXCLUSIVE` an exclusive create, and `SQLITE_FCNTL_WIN32_SET_HANDLE` is debug-only; Microsoft documents the distinct reparse-point and handle sharing semantics. See https://www.sqlite.org/c3ref/open.html , https://www.sqlite.org/c3ref/c_fcntl_begin_atomic_write.html , https://learn.microsoft.com/en-us/windows/win32/fileio/reparse-point-operations .
