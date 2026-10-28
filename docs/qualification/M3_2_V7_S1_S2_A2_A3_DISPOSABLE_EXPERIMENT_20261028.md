# M3.2 v7 S1/S2 — A2 + A3 Windows disposable experiment (28 October 2026)

## Consent and source qualification boundary

Laurent expressly authorized an **experimental A2 + A3 proof on strictly disposable Windows fixtures** following the design-only PR #212: source `9c35d205af0efd47505533a47285f2b0ab3bb525`, CI #40694186183 SUCCESS, protected main `422b17955154085fba0eecee9cdff639d3b0fa14`, independent postmain #40695996216 SUCCESS (203 Rust, 7 Greenfield, 41 guards, 143 contracts), #38 terminal 6470411910. This new PR is **NOT PASS** until its own exact HEAD CI and independent postmain qualify it.

The sole product profile remains `com.fabulaxiom.greenfield.v1` for NEW_ONLY and EXISTING_PROFILE. Experimental process mutex names are randomly generated under `Local\\Fabulaxiom-A2-Disposable-*`, never derived from operator directories or production profile names. All SQLite files, `-wal`/`-shm`/`-journal`, and related writes exist only under fresh per-test `%TEMP%` roots created by the Windows CI account. No operator file is opened or inspected.

## A2: what is actually demonstrated, and what is not

- One parent process acquires a named Win32 mutex, one separately launched cooperating Rust test process observes `WAIT_TIMEOUT`, and after release another separately launched test process acquires it. This tests cooperation only.
- A second test checks a preexisting named object is observed, then has a child process exit abruptly while owning the mutex; the parent observes `WAIT_ABANDONED` and deliberately retains `LifecycleUnproven` and `HandoffNotAtomic` STOP. The child has no SQLite handle.
- The fixture uses an OS-default security descriptor ONLY because its unpredictable name is transient and never used for authentication. A reviewed security descriptor/DACL, per-user/SID and session namespace derivation, named-object squatting resistance, timeout policy, and different-identity adversarial proof are still **NOT_PROVEN**. A production design **must STOP** if the descriptor cannot be independently validated. `WAIT_ABANDONED` is not a clean-close certificate.
- No mutex is used by the application, no persistent lock or marker is created, and an external SQLite process need not participate in the mutex. Named object ownership does **not** atomically identify the handle delegated at SQLite VFS `xOpen`.

## A3: read-only negative verdicts, not provenance

- A fresh SQLite file is explicitly closed and then deliberately replaced with invalid bytes in its own disposable fixture; read-only open failure or `PRAGMA integrity_check` failure causes refusal. A3 returns no positive writer token.
- A separate freshly closed SQLite file receives an invented `-wal` sentinel; preflight refuses it without opening for recovery and without altering the sentinel. This is a conservative **ambiguous WAL** refusal, not evidence of actual WAL recovery correctness.
- Existing tests already veto a `foreign_owner` schema and a broken foreign key via `pragma_foreign_key_check`; `integrity_check` is not a substitute for foreign key validation. Passing both would remain `STRUCTURALLY_CONSISTENT_UNAUTHENTICATED`.
- The absence of sidecars at one instant, a clean close in one process, a mutex lease, and an A3 read-only veto cannot close the preflight-to-`xOpen` TOCTOU gap. No atomic delegated-handle proof exists. Default **A0 refuses cross-process EXISTING_PROFILE**; NEW_ONLY also has no runtime writer admission.

## Strict STOP and expected evidence

Expected, **NOT PASS** until this source PR's own CI: **208 Rust / 7 Greenfield / 41 SQLite guards / 144 continuity contracts** (four new parent tests plus one child helper counted by Rust). No fabricated PASS; source and independent postmain logs must determine the exact final count.

M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, writer `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, real G3 `STOP_UNAVAILABLE`, historical `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, #35 OPEN/DRAFT. No S3/S4, no IPC/CRUD, no operator access, no real SQLite/backup/ACL/sidecars/journals/marker, no migration 007, no native Hello. `HandoffNotAtomic` and `COORDINATION_UNPROVEN` remain explicit architectural stops.

Proof sources: [Microsoft WaitForSingleObject](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-waitforsingleobject), [Microsoft CreateMutexW](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-createmutexw), [SQLite PRAGMA](https://www.sqlite.org/pragma.html), [SQLite WAL](https://www.sqlite.org/wal.html).

Per-PR: both resume prompts, MD/JSON handoffs, history/protocol/state/next/gate, README and both roadmaps; source CI at exact HEAD, diff/reviews/threads, `Protect main`, protected squash with `expected_head_sha`, independent postmain PUSH CI, and #38 append-only qualification.
