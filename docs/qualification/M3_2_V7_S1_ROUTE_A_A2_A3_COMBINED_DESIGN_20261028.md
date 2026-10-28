# M3.2 v7 S1 — Route A, A2 + A3 combined design study (28 October 2026)

## Consent, exact scope, provenance

Laurent explicitly approves **the A2 + A3 design study only**. No implementation of Windows locks, named objects, database openers, persistent marker, IPC, SQLite operator recovery or writer admission is approved; **no operator execution**. Prior #211 terminal: source `52178c527f59194affa08837ca319b71ccb647e0`, CI #40689412991 SUCCESS; protected `main=f96a44d6d02d6510cd13736741112cc0682a5bd8`, independent postmain #40691190713 SUCCESS, **203 Rust / 7 Greenfield / 41 SQLite guards / 142 continuity contracts**, issue #38 terminal 6469667735. This is a document-only *architecture candidate*, not a release or proof of S1 admission.

The only logical profile remains `com.fabulaxiom.greenfield.v1` (same profile for NEW_ONLY and EXISTING_PROFILE). Route A assumes a namespace created and controlled by Fabulaxiom and explicitly excludes resistance to an administrator, a privileged process, a malicious process with effective owner access, a foreign filesystem, or arbitrary handle replacement. That assumption needs an independent review before production use.

## A2 — contemplated cooperating-instance coordination

**Preferred design subject for subsequent approval:** an OS-managed, scoped **named mutex** with a reviewed security descriptor, rather than a persistent filesystem lock/marker. A Windows mutex can coordinate *cooperating* instances across a process boundary; its existence says nothing about the authentic identity of a SQLite file or the correctness of its contents. The design must define exact name derivation tied to the one logical profile, local versus global namespace scope, DACL/owner, process identity, lifetime/hold ordering and denial of unexpected pre-existing named objects. No concrete security descriptor or name is approved yet.

Conceptual, **not implemented** outcomes:

| Mutex outcome | S1 policy |
|---|---|
| Newly acquired uncontended, expected owner/scope | May proceed to *separate negative checks*, never immediately mint admission |
| Contended / timeout / wrong owner, namespace or DACL | STOP: `COORDINATION_UNPROVEN` |
| Abandoned owner / crash inference | STOP: `RECOVERY_REQUIRED_NOT_AUTHORIZED`, never infer clean shutdown |
| Access denied / API anomaly | STOP: `COORDINATION_UNPROVEN` |

Holding a kernel mutex **cannot exclude SQLite writer processes that do not cooperate**. If a future design instead selects `CreateFile` share-mode or `LockFileEx`, it must distinguish OS share compatibility from SQLite locks and prove deadlock-free ordering; keeping an unrelated file handle or path precheck does **not** atomically bind the delegated SQLite VFS `xOpen` handle. Do not equate `WAIT_ABANDONED` with a clean close. This document issues no Win32 API calls.

## A3 — contemplated provenance, integrity and recovery vetoes

All checks would apply **only after a separately authorized, isolated, already-opened fixture connection** and before any writer capability. A3 is a *veto layer*, not authentication:

1. Expected one-profile schema owner and exact migration lineage (not `user_version=7` alone). Unknown or forged lineage -> `FOREIGN_PROVENANCE` STOP. An attacker able to edit the database could forge these fields.
2. `PRAGMA integrity_check` structural check and **separate** `PRAGMA foreign_key_check`; a clean integrity check does not cover FK violations. Any error -> `INVALID_FIXTURE` STOP.
3. Inventory `-wal`, `-shm`, `-journal` and journal mode as observed state only. **No sidecar presence or absence proves clean close**; a crash may require SQLite recovery and an exclusive lock. Any ambiguous recovery state -> `RECOVERY_REQUIRED_NOT_AUTHORIZED` STOP. Read-only opening is not assumed side-effect-free under every WAL configuration.
4. When schema/lineage and SQLite checks pass, the result remains `STRUCTURALLY_CONSISTENT_UNAUTHENTICATED`. It must not become `V7WriterAdmission` or a claim of a unique external writer.

Source references: [SQLite PRAGMA integrity and FK distinction](https://www.sqlite.org/pragma.html), [SQLite WAL recovery and cleanup](https://www.sqlite.org/wal.html), [SQLite transaction locking](https://www.sqlite.org/lang_transaction.html), [SQLite VFS/open flags](https://www.sqlite.org/c3ref/c_open_autoproxy.html), [Microsoft CreateFileW sharing semantics](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew), [Microsoft FILE_ID_INFO](https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_id_info), [Microsoft CreateMutexW](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-createmutexw) and [WaitForSingleObject](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-waitforsingleobject).

## Proposed order and the unsolved binding problem

Design sequence only: A2 contender identity/namespace check -> A2 exclusive cooperative ownership while held -> S1 filesystem preflight in controlled fixture -> **separately-authorized SQLite fixture opening** -> A3 schema/FK/integrity/sidecar vetoes -> explicit `HandoffNotAtomic` STOP. Any restart of the owner process begins with **unknown clean-close provenance**, even if the A2 mutex can be obtained. A2 and A3 combined do **not** pin the actual delegated SQLite handle and do not prove absence of an external writer. No Tauri State, writer IPC, CRUD, migration 007 or operator DB access is reachable from this design.

| Scenario to falsify later, disposable Windows only | Expected refusal / observation |
|---|---|
| Two cooperative contenders, same profile | At most one A2 lease in a modeled interval, no writer admission |
| Crash/abandoned mutex | `RECOVERY_REQUIRED_NOT_AUTHORIZED` |
| Wrong DACL or pre-created mutex | `COORDINATION_UNPROVEN` |
| Foreign schema owner, forged migration or broken FK | `FOREIGN_PROVENANCE` / `INVALID_FIXTURE` |
| WAL recovery / sidecar ambiguity | `RECOVERY_REQUIRED_NOT_AUTHORIZED` |
| Parent/file substitution between A2/A3 and xOpen | `HandoffNotAtomic` — remains unsolved |
| Non-cooperating or privileged writer | `NOT_PROVEN`, not a passing test of exclusion |

## Implementation gate — not granted

The next owner decision, if desired, is a **separate S1/S2 disposable Windows proof authorization** for a specific A2 OS coordination primitive plus an A3 *negative* fixture matrix, with review of the name/DACL and recovery behavior. Even that would not authorize persistent markers, production SQLite opener, runtime `V7WriterAdmission`, S3/S4, IPC, operator profile access or Hello. If there is no further authorization, retain **A0: cross-process EXISTING_PROFILE refused**. The difficult xOpen handle binding must be resolved in its own architectural gate; more green path-only tests cannot silently close it.

## Unchanged STOP

M3.2 `IN_PROGRESS_NOT_ACCEPTED`; G2B `NOT_ACCEPTED`; writer/external process `NOT_PROVEN`; G2C `NOT_AUTHORIZED`; real G3 `STOP_UNAVAILABLE`; historical `PENDING_EXTERNAL_ATTESTATION(21/3/2)`; prospective `NOT_STARTED`; #35 OPEN/DRAFT. No operator SQLite v6/v7, backup, ACL, sidecar, journal, marker, migration 007, native Windows Hello, S3/S4, Tauri writer IPC/CRUD or operator execution.
