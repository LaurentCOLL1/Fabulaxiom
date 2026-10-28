# M3.2 v7 S1 — Route A, lifecycle decision model (28 October 2026)

## Candidate scope / no qualification before exact Windows CI

Owner confirmed Route A: **controlled private namespace**, bounded threat model, Rust preparation and strictly disposable Windows fixtures (S1/S2). Base `main=90cb86aa6873135890ea762f95eb9480fd9d917c`; PR #208 source `aef3d137762eeea111e67f57d85acf23307f8a4f`, source #40675104745 SUCCESS, independent postmain #40676661192 SUCCESS, both **199 Rust / 7 Greenfield / 41 SQLite guards / 139 continuity contracts**, issue #38 terminal comment 6467450836.

This next change is test-only `#[cfg(all(test, windows))]`: a **pure lifecycle observation-to-preflight-mode decision** plus two new Rust Windows tests. `Absent` yields only `NewOnly` candidate; `CleanlyClosed` yields only `ExistingProfile` candidate for the **same** `com.fabulaxiom.greenfield.v1`; `UncertainAfterCrash`, `Active`, or `Foreign` refuse with `LifecycleUnproven`. The clean-close disposable SQLite fixture demonstrates that mode selection and filesystem checks can succeed, while `HandoffNotAtomic` still refuses the admission handoff. The unknown-lifecycle fixture demonstrates that a passing path check does not authenticate the lifecycle.

`CleanlyClosed` is an **input observation in a toy model**, not a trustworthy runtime evidence source, persisted clean-shutdown proof, ownership lease, recovery protocol, or operator attestation. A crash may leave WAL/SHM or ambiguous provenance and requires separate recovery design. No SQLite writer admission, no `V7WriterAdmission` runtime constructor, no atomic VFS/`xOpen` binding, no writer-exclusion proof, no claim of re-opening an actual profile. This candidate deliberately does not invent a clean-shutdown marker.

Expected new source CI counts: **201 Rust / 7 Greenfield / 41 guards / 140 contracts** — **NOT PASS** until exact-head Windows run and independent postmain. The next authorized S1/S2 decision should concern *how* a clean stop and profile provenance could be proven under Route A, explicitly without operator files; another negative fixture alone will not resolve the admission gate.

## STOP remain

M3.2 `IN_PROGRESS_NOT_ACCEPTED`; G2B `NOT_ACCEPTED`; external writer `NOT_PROVEN`; G2C `NOT_AUTHORIZED`; real G3 `STOP_UNAVAILABLE`; historical `PENDING_EXTERNAL_ATTESTATION(21/3/2)`; prospective `NOT_STARTED`; #35 OPEN/DRAFT. **S3/S4 prohibited**, no IPC/CRUD writer, migration 007, native Hello, operator access or modification of operator SQLite v6/v7, backups, ACL, sidecars, logs, journal, marker. Source/fixture evidence does not transfer to production.
