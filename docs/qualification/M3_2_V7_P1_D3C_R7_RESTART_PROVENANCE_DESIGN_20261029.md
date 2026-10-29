# Fabulaxiom M3.2 — D3c proposed R7 restart-provenance design (DOCUMENTATION ONLY)

**29 October 2026. Status: DESIGN PROPOSAL, NOT AN AUTHORIZED WINDOWS EXPERIMENT.** Here **D3c** is a provisional label for the already-scoped D3b-4/D3b-5 R7 topics in PR #215, NOT a new canonical successor milestone. It was **not** already qualified or separately authorized for execution. No production/CI Rust code, VFS, Tauri IPC, migrations, markers, SQLite files, operator paths, or Ollama connections are created or changed by this document.

## 0. Naming reconciliation after repository-history audit (29 October 2026)

**CORRECTION — DO NOT TREAT D3c AS A NEW CANONICAL STEP.** An explicit named `D3c`, `D3d` or `D3e` stage was not found in the prior indexed PR titles/bodies/issues or the prior D3 design checked. The *substance*, however, was already scoped in [PR #215's D3 design](https://github.com/LaurentCOLL1/Fabulaxiom/blob/8203b7323877edc87ffabaad1694c52d2523023d/docs/qualification/M3_2_V7_P1_D3_WAL_SHM_LIFECYCLE_CRASH_RESTART_DESIGN_20261028.md): **D3b-4** proposed replay/swap/omission of a hypothetical restart witness (format separately authorized), **D3b-5** proposed crash timing around commit/WAL sync/checkpoint/SHM unmap/SQLite close, and **D3a-3** proposed checkpoint/busy observation. None of D3b-4/-5 was implemented or authorized by the limited D3b Windows CI proof.

Consequently the `D3c` label in this PR is **provisional shorthand for consolidating existing D3b-4/-5 R7 design work**, *not* an additional approved milestone, a fresh set of 12 mandatory tests, or a supersession of PR #215. Its 12 suggested cases are a **decomposition/mapping** of pre-existing proposed obligations and R7/R4/R8 safety analysis, not 12 newly authorized gates. Future labels `D3d` / `D3e` remain **UNDEFINED**; do not invent scope for them. The canonical source remains PR #215 until a separately reviewed naming decision. The documentation-only PR #217 completed exact-source CI #40835891337 successfully and merged under Protect main at commit `a59ff4a1aa19c06f0a8f73e6ba638c62e2c6cb72`; this qualifies only the document and does not authorize an experiment. No production writer admission follows from document review.

| Existing scope in PR #215 | Overlapping candidate analysis in PR #217 |
|---|---|
| D3b-4, missing/replayed/swapped hypothetical witness | D3c-01 to D3c-05, generation and publication ordering |
| D3b-3, close BUSY and deferred destruction | D3c-06, D3c-07 |
| D3b-5, crash-phase matrix | D3c-08, D3c-09, D3c-12 |
| D3a-3 and R4, checkpoint/WAL/SHM custody | D3c-10 |
| R2/R3 and cooperative ownership hazards | D3c-11 |

## 1. Exact observed baseline; avoid proof transfer

- Source-controlled protected `main=4fbffea526182e551cb5c19848817ba2d96417e3` after documentation-only protected PR #216; independent post-main push CI [#40830760358](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40830760358) **completed/SUCCESS**, which proves source checks for that main, not a v7 writer admission.
- Draft PR [#215](https://github.com/LaurentCOLL1/Fabulaxiom/pull/215) **OPEN/DRAFT**, exact D3b source `8203b7323877edc87ffabaad1694c52d2523023d`; Windows [#40793962533](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40793962533) SUCCESS, **224 Rust / 7 Greenfield / 41 source guards / 152 continuity contracts**, four `m32_d3b_*` witnesses individually ok. All experimental changes remain on #215, **not main**.
- D3a and D3b are **negative Windows CI disposable fixture results only**. D3b refuses restart both after a retained-handle `WAIT_ABANDONED` and after a last-handle-destroyed, newly free mutex `WAIT_OBJECT_0`. A `SQLITE_BUSY` close does not prove completion. D3b does **not** reopen the crashed SQLite file.
- Same Windows SID peer processes are owner-assumed trusted/cooperative; this does not establish adversarial same-SID exclusion. P1 single Rust-owned session selected in design; P2 deferred. No automatic qualification of R1–R9.
- **Current STOP:** A0 `EXISTING_PROFILE` cross-process refuse; R1–R9 production NOT_PROVEN; writer NOT_PROVEN; M3.2 IN_PROGRESS_NOT_ACCEPTED; G2B NOT_ACCEPTED; G2C NOT_AUTHORIZED; G3 STOP_UNAVAILABLE; historical PENDING_EXTERNAL_ATTESTATION(21/3/2); prospective NOT_STARTED; #35 OPEN/DRAFT.

## 2. Decision: what D3c can and cannot be

**Proposed D3c = a falsifiable, reviewable _restart-provenance and clean-close protocol design_, not recovery.** It answers: “what independently verifiable evidence would distinguish an authorized clean predecessor close from an ambiguous earlier owner, before any existing-profile SQLite open?”

The current safe production behavior is **deny**. A free named mutex, absence/presence of `-wal`/`-shm`, `Drop`, a process PID, one FileId128 observation, an apparent successful checkpoint, or a matching unverified marker must **never** independently unlock a successor writer.

No durable proof format is currently approved. Designing an *illustrative* manifest schema below **does not authorize its creation, persistence or replay**. In particular, this proposal does not implement D3b-4 marker replay, D3b-5 crash timing, operating-system power failure, real WAL recovery, or opening any existing SQLite v7 file. Those are distinct future gates.

## 3. Candidate state machine (paper only)

| Proposed state | Predicate | Action and fail-closed limit |
|---|---|---|
| `UNKNOWN_PREDECESSOR` | Fresh process, no independently trusted predecessor chain | Refuse all existing-profile SQLite opens |
| `CLAIM_HELD_UNADMITTED` | Cooperating mutex claim and owned namespace only | May investigate *metadata only* in a separately authorized disposable test; **not** writer admission |
| `OWNED_NEW_SESSION` | A separately authorized **NEW_ONLY disposable** object admitted under the fixture protocol | Single owner connection only in already authorized test context |
| `CLOSING` | No queued operation; outstanding statements/BLOBs/backups accounted for; claim still held | A close error, delayed destruction or unknown WAL/SHM disposition => REVOKED |
| `CLOSE_OBSERVED_NOT_ATTESTED` | `sqlite3_close()` success witnessed in owner process | This is **not** by itself a restart-capable durable claim |
| `CLEAN_HANDOFF_CANDIDATE` | *Hypothetical* authenticated, flushed, predecessor-bound witness after close and verified sidecar/namespace observations | Remains unadmitted pending independent R1–R9 gate, durable semantics validation and explicit owner authorization |
| `RECOVERY_REQUIRED_NOT_AUTHORIZED` | Crashed, abandoned, missing, stale, swapped, replayed, busy-close or mismatched evidence | No SQLite successor open, no checkpoint, no marker repair, no WAL/-shm deletion |
| `SESSION_ADMITTED` | Not reachable by D3c documents/CI; requires distinct approved runtime R1–R9 evidence | No transition granted here |

**Ordering obligation:** keep cooperative claim while the owner quiesces, completes genuine SQLite close, checks *only otherwise authorized* owned file/handle provenance, and would durably publish a close claim; release claim last. A crash at any boundary must not leave a previously trusted “clean” record falsely usable. A record written **before** close cannot attest close. Conversely, writing one **after** close still requires independent proof of its identity, durability, replay prevention, and a future process's secure association with that particular main/WAL/SHM generation.

## 4. Hypothetical witness fields — no file format adopted

A proposed witness would minimally need: versioned record type, app/profile identity, Windows principal scope, unique owner/session generation, verified main volume and FileId128 at open/close, relevant WAL lineage or checkpoint outcome, close/flush ordering status, prior-generation reference, explicit “clean only” outcome, and a checked record integrity mechanism. **No cryptographic secret or HMAC key is provisioned in this design.** A plain SHA-256 detects accidental corruption but does not authenticate an attacker who can rewrite both data and hash; an untrusted same-SID malicious writer is outside the selected threat model but error, replay and stale-generation hazards remain.

The mechanism needs a reviewed atomic/ordered publication strategy and failure analysis under Windows/NTFS semantics, not a declaration that rename+flush is automatically crash-atomic. The witness must not claim that FileId128 uniquely attests historical SQLite transactions, that a WAL pathname alone identifies a WAL generation, or that a newly free mutex means clean shutdown. Strictly prohibit any attempt to “verify” an unadmitted existing-profile witness by opening SQLite, issuing PRAGMA, checkpointing, migrating, restoring, or deleting auxiliary files.

## 5. Proposed D3c negative fixture matrix — NOT EXECUTED / NOT AUTHORIZED

All prospective tests, if *separately* approved, should be `#[cfg(all(test, windows))]` only, on **fresh per-test %TEMP% owned roots**, with fictional rows and no operator data. No persistent marker in the real app; no cross-PR transfer of CI results. These are names for test cases in a design, **not test functions already in source**.

| Candidate | Scenario | Expected negative oracle |
|---|---|---|
| D3c-01 | Missing predecessor witness / new mutex free | `RECOVERY_REQUIRED_NOT_AUTHORIZED` |
| D3c-02 | Witness from another profile/SID/volume/FileId128 | REFUSE before SQLite open |
| D3c-03 | Old generation replayed after a different generation | REFUSE even with checksum match |
| D3c-04 | Witness swapped/omitted/corrupted/truncated | REFUSE; no repair |
| D3c-05 | “Clean” record recorded before actual close | REFUSE; ordering violation |
| D3c-06 | `sqlite3_close` yields `SQLITE_BUSY` | REFUSE; claim cannot certify clean |
| D3c-07 | `sqlite3_close_v2` says OK with live resources | REFUSE; deferred destruction not certified |
| D3c-08 | Crash after close but before hypothetical durable witness publication | REFUSE even if SQLite had finished close |
| D3c-09 | Crash after witness publication but before mutex release | No automatic admission; assess provenance/ABA independently |
| D3c-10 | WAL nonempty, checkpoint incomplete or SHM identity unknown | REFUSE; no reopen/checkpoint |
| D3c-11 | Parent rename/reparse, sidecar ID swap or concurrent cooperative claim | REFUSE |
| D3c-12 | Power-loss semantics unavailable on CI runner | Record NOT_PROVEN, never substitute `TerminateProcess` for power loss |

**Positive witness gate is deliberately absent:** passing these negative tests could prove *some refusals*, not clean admission/recovery or power-loss durability. Do not add a “successfully reopened crashed DB” path until a new, explicit owner authorization and independent review of R1–R9.

## 6. Required decisions BEFORE any D3c executable slice

1. Select whether D3c remains *design only* or an explicitly bounded Windows CI disposable **negative-only** experiment is approved. D3b approval does **not** extend automatically to D3c.
2. Independently review a hypothetical durable witness protocol: generation chain, claim/close order, authenticated provenance, replay/stale protection, NTFS flush failure points, and backout. **No write to operator or persistent app directories.**
3. Partition R7 independently from R4 (WAL/SHM actual custody), R6 (single owner) and R8 (resource/close behavior); all must pass before R9 admission can even be considered.
4. Preserve the product route C Greenfield v6 user functionality while v7 writer remains behind a STOP. Future Ollama memory should be assembled from source-cited in-memory packets by the one Rust owner, not a second model-controlled SQLite writer.
5. Before a documentation-only PR can merge: source HEAD exact CI, reviews/threads, diff/inventory and `Protect main` verification; protected `expected_head_sha` merge then independent postmain CI; #38 append-only terminal checkpoint. A merged paper design does **not** authorize any D3c test or production functionality.

## Primary technical references

- SQLite [WAL file format/recovery](https://www.sqlite.org/walformat.html), [WAL overview](https://www.sqlite.org/wal.html), [checkpoint API](https://www.sqlite.org/c3ref/wal_checkpoint_v2.html), [sqlite3_close and close_v2](https://www.sqlite.org/c3ref/close.html).
- Microsoft [kernel object lifetime](https://learn.microsoft.com/en-us/windows/win32/sysinfo/kernel-objects), [mutex abandonment](https://learn.microsoft.com/en-us/windows/win32/sync/mutex-objects), [file caching / flush](https://learn.microsoft.com/en-us/windows/win32/fileio/file-caching).
- Earlier [D3 architecture](https://github.com/LaurentCOLL1/Fabulaxiom/blob/8203b7323877edc87ffabaad1694c52d2523023d/docs/qualification/M3_2_V7_P1_D3_WAL_SHM_LIFECYCLE_CRASH_RESTART_DESIGN_20261028.md), [D3b fixture](https://github.com/LaurentCOLL1/Fabulaxiom/blob/8203b7323877edc87ffabaad1694c52d2523023d/docs/qualification/M3_2_V7_P1_D3B_DISPOSABLE_WINDOWS_CRASH_RESTART_REFUSAL_FIXTURE_20261028.md), and [P1 R1–R9 ledger](https://github.com/LaurentCOLL1/Fabulaxiom/blob/8203b7323877edc87ffabaad1694c52d2523023d/docs/qualification/M3_2_V7_P1_SINGLE_OWNER_SESSION_PROOF_PLAN_20261028.md).
