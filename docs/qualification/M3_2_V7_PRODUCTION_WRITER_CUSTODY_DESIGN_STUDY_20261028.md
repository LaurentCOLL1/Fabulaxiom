# M3.2 v7 — Production writer custody: VFS, Windows namespace, WAL/SHM and restart design study

**28 October 2026 — DESIGN STUDY ONLY; NOT IMPLEMENTATION AUTHORITY.** Laurent explicitly authorized this next architectural study after terminal PR #214. This document is a proposal to review; it has no executable Win32/SQLite runtime code, operator procedure, durable marker, schema change or writer admission. A source CI run of this document and its drift contract would qualify **documentation only**, not any safety property of a production writer.

## 1. Verified starting point and non-transferable limits

- GitHub baseline: PR [#214](https://github.com/LaurentCOLL1/Fabulaxiom/pull/214) source `20aae2656d8d0123d73cab260fd5a451559e1ab4`, Windows source CI [#40713872679](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40713872679) SUCCESS; protected squash `main=90142d8c78dd8a84ee3f0ee1676a753c8521d78e`; independent push postmain [#40715995392](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40715995392) SUCCESS. Both job logs report **210 Rust / 7 Greenfield / 41 SQLite guards / 145 continuity contracts**, and both delegated-handle xOpen witnesses pass. [Issue #38 terminal append-only comment](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6473413358). Ruleset `Protect main` #24895490 active, strict required `Windows frontend and Rust checks` integration 15368, bypass actors empty. PR #35 remains OPEN/DRAFT.
- Acquired but bounded: [the unconnected Rust single-owner v7 service](M3_2_V7_RUST_SINGLE_OWNER_WRITER_PREPARATION_20261028.md) takes an **already opened/admitted** connection; it does not open the operator database or mint a runtime `V7WriterAdmission`. [The test-only delegated-handle veto](M3_2_V7_SQLITE_XOPEN_DELEGATED_HANDLE_BOUNDARY_DECISION_20261028.md) compares volume and 128-bit file ID obtained from the *actual delegated* `sqlite3_file.xFileControl` **inside** xOpen, and closes on mismatch before returning success to SQLite. That catches the controlled precheck-to-return substitution. The OS open already occurred; it does **not** give an atomic pathname/namespace claim, account for every sidecar, prove recovery or exclude a hostile writer.
- The separate same-profile `EXISTING_PROFILE` cross-process path remains A0 STOP. A clean close observed in one process, an unclaimed mutex, absence of sidecar names, SQLite `integrity_check`, or FileId128 alone cannot confer durable provenance.

## 2. Threat model — a choice to make, not a claim already proved

| Actor / failure | Proposed treatment | What cannot be inferred |
|---|---|---|
| One Fabulaxiom-owned session, cooperative peer processes | Single writer lifecycle and named-mutex coordination may be **tested**, subject to owner identity, DACL and shutdown protocol | Mutex cannot block a peer that ignores it |
| Ordinary same-SID Windows process outside Fabulaxiom | Treat as **uncooperative writer** unless an independently reviewed narrower trust model explicitly excludes it | A DACL granting that SID access is not per-process exclusivity |
| Privileged process, administrator, backup agent, reparse-point actor | Explicitly outside a potentially bounded application trust model only after owner review; otherwise STOP | Neither FileId128 nor a user-mode mutex proves resistance |
| Crash, abandoned mutex, forced termination, power loss | `RECOVERY_REQUIRED_NOT_AUTHORIZED`; no inferred clean shutdown | No automatic `EXISTING_PROFILE` admission |
| Foreign/old schema, key, profile, ATTACH or sidecar lineage | Refuse; no migration, repair, overwrite or opportunistic cleanup | Structural SQLite validity is not authenticity |

**Owner decision required before runtime work:** choose whether the product threat model trusts all processes with the same Windows security principal, or requires an independently isolated OS principal/broker. The first is a **bounded operational assumption**, never a technical proof of external-writer absence; the second is a separate process/security architecture and IPC gate. Until one is reviewed, external writer = `NOT_PROVEN`.

## 3. Candidate architectures and decision

| Route | Outline | Potential value | Unresolved prerequisites / verdict |
|---|---|---|---|
| **A0 — fail closed (current)** | NEW_ONLY disposable preflight only; refuse cross-process `EXISTING_PROFILE`; no runtime `V7WriterAdmission` | No promotion of toy evidence to operator authority | **KEEP ACTIVE** until independently qualified and separately authorized |
| **P1 — production-owned VFS/session boundary (candidate design)** | Own one session's VFS lifetime, verify the delegated Win32 handle during `xOpen`, bind namespace/ACL/ancestor evidence, mediate applicable `xOpen` and `sqlite3_io_methods` operations including `xShmMap`, and coordinate the one authorized Rust writer | Could bind checks to the objects SQLite actually uses and expose a revocable lifecycle | Not yet implemented. Complex `xClose`, failure cleanup, journaling, versioned methods, sidecar mapping, namespace races and same-SID writer threat; **DESIGN CANDIDATE, NOT SELECTED FOR IMPLEMENTATION** |
| **P2 — separate broker/OS principal** | Dedicated storage identity/process owns database and authorizes narrow requests | May offer a stronger process boundary for same-SID threats | Requires new Windows packaging, DACL, privilege boundary, IPC/CRUD and lifecycle review; **OUT OF CURRENT AUTHORIZATION** |

P1 is the **next design candidate to pressure-test**, not an authorization to build. P2 must be compared if the owner requires exclusion of same-SID uncooperative writers. Do not mislabel the OS pathname open as atomic. `SQLITE_OPEN_EXCLUSIVE` is a VFS flag, **not** an exclusive-access switch passed through `sqlite3_open_v2`.

## 4. Mandatory P1 proof obligations (none satisfied for production)

| ID | Required invariant / evidence before admission | Fail-closed outcome |
|---|---|---|
| **R1 — principal and scope** | Single chosen profile `com.fabulaxiom.greenfield.v1`, explicit intended Windows SID/session security boundary, DACL inheritance/owner/integrity rules, normal and hostile same-SID access analysis | Unverified or overbroad principal → STOP |
| **R2 — namespace and ancestors** | Pinned owned directory chain, no unexplained junction/reparse/ADS/device namespace, parent identity held or continuously revalidated across the actual open; reject rename/ABA and path escape | Any gap between path evidence and opened object → STOP |
| **R3 — exact main handle** | The *delegated* `sqlite3_file` identity is checked before a successful xOpen return, with volume + FileId128, stable ownership and full failure cleanup; independent verification of Win32 handle semantics | Mismatch, unsupported VFS or failed `xClose`/cleanup → STOP |
| **R4 — all sidecars and I/O** | Journal/`-wal` opens, `-shm` via `xShmMap`/`xShmLock`/`xShmUnmap`, file-control and close hooks are accounted for with object identity, locking order, recovery rules and no unmediated escape | Untracked sidecar/map or unsafe fallback → STOP |
| **R5 — SQLite provenance** | Same handle/profile/schema/migrations and foreign-key lineage established separately from `integrity_check`; no foreign `ATTACH`, foreign key, implicit migration or unknown journal state | Invalid/ambiguous/foreign provenance → STOP |
| **R6 — writer custody** | Define the cooperative mutex DACL and abandoned behavior; show single actor/connection lifecycle; prove OS-level writer exclusion for the chosen threat model **or explicitly accept its bounded limitation** through independent human review | External writer absence `NOT_PROVEN` or threat model undecided → STOP |
| **R7 — crash/restart** | Authenticated durable session provenance and handoff policy, retention and recovery semantics covering close/commit/checkpoint/crash and all sidecars, including an independent attestation path; no self-minted clean-close claim | `WAIT_ABANDONED`, crash or missing durable evidence → `RECOVERY_REQUIRED_NOT_AUTHORIZED` |
| **R8 — resource safety** | Audit VFS registration lifetime, null `pMethods`, `xClose` exactly-once/error handling, method-version negotiation, handle leaks, shutdown races, bounded queue/timeouts and cancellation | Unexpected method/version/error state → revoke and STOP |
| **R9 — gate boundary** | Independently reviewed Windows disposable positive/negative matrix, exact-head CI and source audits, owner approval specifically for production writer gate, separate operator ceremony | No production `V7WriterAdmission`, Tauri State or IPC/CRUD |

`FileId128` is an object-identity observation at a point in time, not a cryptographic historical custody proof. The main-file VFS veto cannot stand in for `-shm` mapping. SQLite's WAL-index has its own shared-memory methods; extra work is required to reason about both `-wal` and `-shm` identities and recovery.

## 5. Proposed future lifecycle — specification, not code

1. **`NO_SESSION` → `NEW_ONLY_CANDIDATE`** only in a separately authorized strictly owned fresh namespace, with verified creation and original profile intent. For an already existing filename/profile, A0 immediately returns `EXISTING_PROFILE_STOP`.
2. **`OPENED_UNTRUSTED`** after Win32/SQLite has actually opened objects. No SQL, migration, revision write or durable marker may be issued during provisional verification; a failed identity check closes/revokes and STOPs. Any effects of the OS open itself must be accounted for, not described as zero-side-effect.
3. **`ADMITTED_SESSION`** is a *hypothetical future state*, reachable only when all R1–R9 proofs and a separate owner runtime gate exist. It must bind a single revocable identity/connection/worker; the current code cannot construct this state in production.
4. **`QUIESCING` → `CLOSED_ATTESTED`** would require authenticated closure evidence and journal/checkpoint state. `Drop`, named-mutex release, file disappearance or clean SQLite structure alone are insufficient cross-process. Crash, timeout, unexpected writer or abandoned lock goes to `RECOVERY_REQUIRED_NOT_AUTHORIZED`, never an automatic recovery or reopen.
5. An `EXISTING_PROFILE` restart is **not** reached by this study; it requires its own historical/durable provenance decision and independent operator gate.

## 6. Falsifiable Windows disposable matrix for a *later separately authorized* source phase

| Witness | Expected outcome |
|---|---|
| Fresh owned directory, stable main handle, clean documented journaling | Candidate may satisfy scoped R2/R3 only; **no writer admission** |
| Swap target after precheck but before delegated `xOpen` | Mismatch triggers `xClose`, null methods and `SQLITE_CANTOPEN`; no successful SQLite connection |
| Rename/ABA of parent or junction/reparse before/after open | Refuse or state explicitly **not proven** if the OS race cannot be eliminated |
| DACL mismatch, unexpected owner, same-SID uncooperative process | Refuse; demonstrate coordination limits, not false exclusivity |
| Cooperative contender and abandoned named mutex | Contender refused; abandoned yields `RECOVERY_REQUIRED_NOT_AUTHORIZED` |
| WAL sidecar substitution, SHM mapping without corresponding `xOpen` | Refuse before unsafe mapping or mark design insufficient; exercise `xShmMap` separately |
| Corrupt DB, foreign lineage, migration mismatch, foreign ATTACH/key | Refuse, never repair operator data |
| Interrupted checkpoint, hot journal, crash/restart | Refuse and require separate recovery authorization, no automatic reopen |
| VFS method mismatch, `xFileControl` failure, `xClose` failure, concurrent shutdown | Fail closed with unambiguous cleanup/telemetry; avoid double close/use-after-free |
| External process ignores mutex, accesses main/sidecars under same SID | **NOT_PROVEN** unless explicit threat-model exclusion or stronger OS-principal design is separately accepted |

All such experiments, if authorized later, use newly created disposable Windows CI/temp files only. No operator Windows action is prescribed here.

## 7. Proposed decision gates and exact next request

- **D0 (this PR):** review the documentary threat model, P1/P2 comparison, R1–R9 and negative matrix; doc/source contract CI only. No Windows binary, OS DACL, marker or SQLite execution added by the study.
- **D1 (future separate owner approval):** decide the same-SID/uncooperative-writer threat model, WAL/rollback and sidecar policy, and whether a production-owned VFS or stronger broker is viable. A design review does not authorize implementation.
- **D2 (future separate approval):** source/CI-only disposable Windows VFS/session implementation proof, explicitly scoped, with independent reviews. Its CI remains non-transferable to runtime or operator.
- **D3 (future separate approval):** only after successful D2 and independent safety review may an application writer/Tauri/IPC and later operator baseline ceremony be proposed. Never merge PR #35 or activate migration 007 via inference.

**STOP remains:** M3.2 `IN_PROGRESS_NOT_ACCEPTED`; G2B `NOT_ACCEPTED`; writer `NOT_PROVEN`; G2C `NOT_AUTHORIZED`; G3 real `STOP_UNAVAILABLE`; historical `PENDING_EXTERNAL_ATTESTATION(21/3/2)`; prospective `NOT_STARTED`; PR #35 OPEN/DRAFT. No S3/S4, IPC/CRUD, migration 007, native Hello, backup/ACL/journal/marker/SQLite operator touches, no operator execution, no persistent marker, no runtime writer. Keep #38 append-only. Any future PR requires both resume prompts, MD/JSON handoffs, protocol/history/STATE/NEXT/gate, README, both roadmaps, drift contract, exact source CI, reviews/threads, active strict `Protect main`, `expected_head_sha` protected squash, and independent postmain CI before terminal status.

## Primary technical references

- [SQLite VFS `xOpen` and open flags](https://www.sqlite.org/c3ref/vfs.html); [open flag restrictions](https://www.sqlite.org/c3ref/c_open_autoproxy.html).
- [SQLite `sqlite3_io_methods`, `xFileControl`, `xShmMap`, `xShmLock` and `xClose`](https://www.sqlite.org/c3ref/io_methods.html); [file control](https://www.sqlite.org/c3ref/file_control.html); [WAL and shared memory](https://www.sqlite.org/wal.html).
- [Microsoft `CreateFileW` and sharing/creation semantics](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew); [`FILE_ID_INFO`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_id_info); [`CreateMutexExW`](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-createmutexexw); [mutex security and abandonment](https://learn.microsoft.com/en-us/windows/win32/sync/mutex-objects).
