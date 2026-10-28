# M3.2 v7 — D3 P1 WAL/SHM custody and crash/restart: bounded design, no executable proof

**28 October 2026 — DOCUMENTARY FOLLOW-ON ONLY, NOT D3 FIXTURE OR RUNTIME AUTHORIZATION.** Owner request "Continue" follows the separately authorized and CI-qualified **D2 disposable Windows fixtures** in [draft PR #215](https://github.com/LaurentCOLL1/Fabulaxiom/pull/215). This document specifies the *next proposed proof* and refusal criteria. It does not run Windows tests, modify Rust/SQLite, open an operator profile, approve recovery, create persistent markers, or grant writer admission.

## 1. Verified starting point and threat boundary

- Protected main remains **90142d8c78dd8a84ee3f0ee1676a753c8521d78e**, originating from merged PR #214; independent postmain [#40715995392](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40715995392) SUCCESS.
- D2's exact previous PR source **c42a6f40caca52550fa485851c0131f84859f651**, [CI #40753334640](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40753334640) attempt 1 SUCCESS: **216/216 Rust, 7/7 Greenfield, 41/41 SQLite guards, 149/149 continuity contracts**. Six new Rust Windows disposable tests passed. Earlier failed source runs #40752418946 and #40752932972 remain failed and non-transferable. Qualification was limited to those synthetic witnesses, not the production session.
- Laurent's bounded assumption remains **same Windows SID processes trusted/cooperative**; deliberate same-SID adversaries are out of threat model. This does not magically create a secure OS exclusion guarantee. **P1 one Rust-owned SQLite session/actor** remains selected, P2 isolated-principal broker deferred, A0 cross-process EXISTING_PROFILE **STOP**, writer **NOT_PROVEN**.
- D2 verified a delegated main FileId128 match, selected xOpen and xShmMap vetoes, cooperative mutex contention, and a witnessed WAIT_ABANDONED *while another handle still existed*. D2 did **not** prove full WAL/SHM callback custody, atomic path open, unambiguous close, crash durability, power loss, or safe existing-profile restart.

## 2. Newly explicit design blockers

**B1 — mutex is volatile, not restart provenance.** Microsoft documents that a named mutex is destroyed after its *last handle closes*. A future process can create a fresh, apparently free mutex following a complete process exit; the lack of WAIT_ABANDONED in that case proves **nothing** about the previous owner's SQLite close or WAL state. WAIT_ABANDONED is a useful refusal when observed, **never** the sole crash detector. Even cooperative same-SID assumptions do not change kernel object lifetime. In D3, a clean new mutex can only enter a **PROVISIONAL_CLAIM / RECOVERY_REQUIRED_NOT_AUTHORIZED** state when predecessor provenance is unverified.

**B2 — WAL is persistent database state.** SQLite states that committed transactions may reside in the -wal file until checkpoint, that a crashed/unclean exit can leave -wal on disk, and that separating or manually deleting -wal can lose transactions or corrupt data. The -shm wal-index uses shared-memory mapping and its lifecycle does not equal a separate named SQLite xOpen. Therefore, do **not** delete/rename -wal/-shm, infer their absence from a main handle, or use an automatic reopen/SQLite checkpoint as a supposedly read-only provenance probe. Any recovery itself may alter files; a STOP must precede unauthorized recovery.

**B3 — close is not a single trust signal.** A successful Rust drop is insufficient evidence of a fully completed SQLite close. sqlite3_close() can report SQLITE_BUSY while statements/BLOBs/backups remain; sqlite3_close_v2() can report SQLITE_OK while deferring destruction. The final SQLite close may itself trigger checkpoint or WAL/-shm cleanup; xClose/xShmUnmap outcomes and handle lifetime must be accounted for before release of a cooperative claim. A checkpoint attempt/return code, a clean xClose, and a durable clean-shutdown attestation are three **different** facts.

**B4 — SQLite VFS method completeness.** VFS xOpen for -wal and io_methods xShmMap/xShmLock/xShmBarrier/xShmUnmap together govern WAL-index interaction; a passing main FileId128 does not attest a mapped -shm object, locks or full WAL lineage. The wrapper must fail closed on unrecognized iVersion, unavailable callbacks, missing sidecar identity, xClose errors and unpaired/unmapped resources. Do not claim FileId128 for an SHM mapping unless an actual backing-object handle is acquired and verified via reviewed API.

## 3. Proposed D3 evidence slices — each needs new owner approval

| Slice | Synthetic Windows CI-only witness (not implemented) | Fail-closed oracle | Production conclusion |
|---|---|---|---|
| **D3a-1** | Fresh disposable main + WAL; correlate real delegated -wal handle identity and volume with expected owned root and file lineage, including post-open substitution veto. | WAL handle mismatch, wrong root or unavailable identity => xClose/refuse; account for pre-veto filesystem side effects. | R2/R3/R4 still NOT_PROVEN. |
| **D3a-2** | Exercise xShmMap, xShmLock, xShmBarrier and xShmUnmap with recorded mapped-region and lock lifetimes; test missing callback or iVersion downgrade. | Mapping/lock/unmap ambiguity, xShmUnmap failure or version downgrade => session REVOKED / STOP. | No SHM backing FileId128 claim without evidence. |
| **D3a-3** | Controlled writer + bounded reader transactions on the **same future owner actor**; track WAL checkpoint PASSIVE vs busy/incomplete without asserting sidecar deletion. | Busy/partial checkpoint => not CLOSED_ATTESTED; no manual WAL/SHM deletion or journal-mode switch. | No production checkpoint policy established. |
| **D3b-1** | Dispose a child process after committed fixture WAL write, before explicit close; preserve exact SQLite main/-wal state under fixture ownership for observation (not restoration). | New process can claim mutex but must **refuse** existing-profile admission without durable predecessor evidence. | R7 remains NOT_PROVEN. |
| **D3b-2** | Exit child while owning named mutex; one parent retains handle (WAIT_ABANDONED) versus all handles gone (fresh mutex). | BOTH branches fail closed; only first branch is observed as WAIT_ABANDONED. | Never infer cleanliness from WAIT_OBJECT_0 after process exit. |
| **D3b-3** | Inject unfinished statement, backup or BLOB, and force cancellation around close to distinguish SQLITE_BUSY, deferred close and VFS callback results. | No mutex release or successor admission on uncertain close; revoke session generation. | No authenticated clean-close attestation. |
| **D3b-4** | Replay, swap or omit a *synthetic* restart witness, if a durable witness format is separately approved in advance. | Stale/missing/wrong-generation witness => RECOVERY_REQUIRED_NOT_AUTHORIZED. | This plan **does not authorize** a durable marker format or operator marker. |
| **D3b-5** | Vary crash moments before/after commit, WAL sync, checkpoint, SHM unmap and SQLite close in test-owned directories; deterministic negative matrix with no operator data. | Every unproven state => STOP; no "SQLite opened successfully => provenance valid" assertion. | No real power-loss or operator evidence transfer. |

**Order:** D3a WAL/SHM custody is the smaller next gate. D3b crash/restart is a separate, riskier gate, preferably authorized only after D3a evidence. No proposal here authorizes either fixture. Tests must use **only** new per-run %TEMP% owned directories, random Local named objects, one CI SID, explicit cleanup of owned fixtures, and exact Windows source-SHA CI. Any code change requires a new reviewed SQLite opening-site inventory and matching continuity contract; the 18 D2 VFS tests, 216 Rust count and 41 SQLite guards must not silently drift.

## 4. Owner actor, future Ollama and UX implications

The future single Rust session actor must serialize short, typed database reads, complete read transactions and release locks before long Ollama inference. It creates a source-revision-pinned, scoped **NarrativeContextPacket** from fiches, histories, chronology, canon, character knowledge and reader reveal/spoiler horizon; it has a session generation and **becomes stale on mutation, revocation or restart**. Neither Ollama nor another frontend/worker opens SQLite, WAL, SHM or writer IPC directly. Generated creative facts are proposals requiring human **APPROVE_CANON**; no implicit cloud fallback. This protects narrative consistency without pretending model output is trusted canon, and does not authorize M4–M7 implementation.

**Proposed close order (design only):** stop new requests -> cancel/drain model-independent work -> finish/rollback short transactions and finalize all SQLite resources -> apply only separately approved WAL checkpoint policy -> await verified close and VFS unmap/close -> independently attest provenance (method undecided) -> release mutex. Any failed step revokes generation. A fresh-process restart requires a separate durable evidence format and security review **before** any EXISTING_PROFILE gate can be reconsidered; otherwise remain A0_STOP.

## 5. Decision and precise next authorization request

**Decision today: D3 DESIGN_READY_FOR_REVIEW; D3 WINDOWS FIXTURES NOT_AUTHORIZED; D3 PRODUCTION NOT_PROVEN.** D2 source CI SUCCESS remains historical evidence only for D2. A further push to draft PR #215 creates a *new source HEAD* and requires its own Windows CI; it does not invalidate the historical fact that D2 passed at c42a6f40, but no old CI can qualify the new source tree.

Suggested next owner authorization, if desired: "**J'autorise D3a, uniquement les fixtures Windows CI jetables WAL xOpen/SHM callbacks et clôture des handles ; pas de D3b crash/reprise, pas de runtime ni d'accès opérateur.**" D3b should be decided separately after reviewing D3a, especially whether an authenticated durable predecessor witness is permissible. This design supplies no executable recovery instructions and does not make such a marker.

**Unchanged STOPs:** M3.2 IN_PROGRESS_NOT_ACCEPTED; G2B NOT_ACCEPTED; G2C NOT_AUTHORIZED; real G3 STOP_UNAVAILABLE; writer NOT_PROVEN; all R1–R9 production NOT_PROVEN; historical PENDING_EXTERNAL_ATTESTATION(21/3/2); prospective NOT_STARTED; #35 OPEN/DRAFT. No S3/S4, runtime writer/VFS, Tauri IPC/CRUD, migration 007, Windows Hello native, v6/v7 operator SQLite, backups, ACL, journaling, marker, sidecar manipulation or Ollama runtime without distinct authorization. PR #215 remains OPEN/DRAFT; protected main must not be merged by this study. #38 append-only.

## Primary technical references

- [Microsoft OpenMutexW — object destroyed when last handle closes](https://learn.microsoft.com/fr-fr/windows/win32/api/synchapi/nf-synchapi-openmutexw)
- [Microsoft Win32 Mutex Objects — WAIT_ABANDONED and undefined protected state](https://learn.microsoft.com/en-us/windows/win32/sync/mutex-objects)
- [SQLite WAL — commits, checkpoint, crash persistence, and -wal/-shm lifecycle](https://www.sqlite.org/wal.html)
- [SQLite io_methods — xClose and complete xShm* method versioning](https://www.sqlite.org/c3ref/io_methods.html)
- [SQLite close vs close_v2 — SQLITE_BUSY and deferred destruction](https://www.sqlite.org/c3ref/close.html)
- [SQLite WAL checkpoint controls](https://www.sqlite.org/c3ref/wal_checkpoint_v2.html)
