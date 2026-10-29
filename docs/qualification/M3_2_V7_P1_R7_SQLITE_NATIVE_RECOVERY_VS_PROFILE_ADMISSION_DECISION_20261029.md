# Fabulaxiom M3.2 v7 — R7 architectural decision candidate: SQLite native recovery ≠ application profile admission

**29 October 2026. Scope: DESIGN / DECISION PROPOSAL ONLY. NO WINDOWS TEST, SQLITE REOPEN, RECOVERY, MARKER, IPC, MIGRATION OR PRODUCTION AUTHORIZATION.**

## 1. Source-qualified checkpoint and problem statement

- Protected `main=209d20f1faa85273ef7c1c7ef32100ecc4c2c0c0`; source [PR #218](https://github.com/LaurentCOLL1/Fabulaxiom/pull/218) CI [#40841412326](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40841412326) SUCCESS; independently [postmain #40842896686](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40842896686) `push/completed/SUCCESS`, attempt 1, same SHA. This qualifies source documents only, not the v7 writer.
- Draft [PR #215](https://github.com/LaurentCOLL1/Fabulaxiom/pull/215), source `8203b7323877edc87ffabaad1694c52d2523023d`, [CI #40793962533](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40793962533) SUCCESS for **D3a/D3b negative disposable Windows fixtures**. Original [D3 R7 plan](https://github.com/LaurentCOLL1/Fabulaxiom/blob/8203b7323877edc87ffabaad1694c52d2523023d/docs/qualification/M3_2_V7_P1_D3_WAL_SHM_LIFECYCLE_CRASH_RESTART_DESIGN_20261028.md) enumerates **D3b-4** (hypothetical restart-witness replay/swap/omission, no marker authorized) and **D3b-5** (pre-/post-commit, WAL sync, checkpoint, SHM-unmap and close crash phases). Those subparts are **not executed**. [P1 R1–R9 ledger](https://github.com/LaurentCOLL1/Fabulaxiom/blob/8203b7323877edc87ffabaad1694c52d2523023d/docs/qualification/M3_2_V7_P1_SINGLE_OWNER_SESSION_PROOF_PLAN_20261028.md) remains on unmerged #215.
- D3c is a *provisional label for this existing R7 scope*, NOT a new gate. D3d/D3e are not verified canonical stages.
- Trust boundary: peer Windows processes running under the same SID are assumed **cooperative**, not adversarial. P1 one Rust-owned SQLite session/actor with source-cited read packets for future Ollama is the **selected architectural direction**, not a granted production writer.

### Two distinct assertions must never be conflated

**R7-SQLITE — transactional recovery correctness.** SQLite's WAL contains committed frames not yet checkpointed. Following an unclean last-connection exit, SQLite's **first eligible new connection** can reconstruct the WAL-index, validating WAL checksums and recovering valid commit frames under SQLite's locks. The `-shm` file is **not durable transaction data** and is not needed as the recovery source. This does not authorize Fabulaxiom to make that new connection. No manual deletion, rename or replay of WAL/-shm.

**R7-ADMISSION — whether Fabulaxiom may touch that profile.** Before permitting SQLite to open an existing profile, the app independently needs profile, namespace, owned root, principal scope, main FileId128/handle identity, sidecar association, prior-generation uncertainty handling, cooperative owner exclusion, schema/migration gate, error semantics, and a reviewed operator/recovery policy. An OS mutex is volatile; an apparently free mutex cannot certify a predecessor's clean close. Passing SQLite's eventual recovery cannot retrospectively prove provenance of the file opened. A0 `EXISTING_PROFILE` cross-process STOP remains binding.

**Decision candidate:** Do **not** build a new durable clean-close marker as a precondition to *SQLite's own transaction recovery* unless a concrete extra application-level invariant is identified that SQLite does not already ensure. A custom marker can be replayed, swapped or partially published and increases failure modes. This is a proposed **simplification**, not approval to omit R1–R9, to drop crash tests, or to open any existing-profile file. When in doubt, remain in `RECOVERY_REQUIRED_NOT_AUTHORIZED`.

## 2. Verified dependency and relevant upstream behavior (not a Windows runtime claim)

At `main`, `src-tauri/Cargo.toml` specifies `rusqlite=0.40.2` with `features=["bundled"]`; `src-tauri/Cargo.lock` pins `rusqlite=0.40.2` and `libsqlite3-sys=0.38.2`. The exact published `libsqlite3-sys 0.38.2` bundled source is SQLite **3.53.2**, according to upstream documentation. SQLite says its rare **WAL-reset race**, involving multiple concurrent connections writing/checkpointing, affects pre-fix releases through 3.51.2 and is fixed in **3.51.3+**. The bundled-version audit is **SOURCE_ONLY**; the exact SQLite version and compile/runtime behavior of the deployed Windows binary are **NOT_ATTESTED**. A later isolated, explicitly authorized fixture may assert `sqlite3_libversion_number()` and link provenance without opening operator files.

Official SQLite documents:
- WAL recovery, index and locks: https://www.sqlite.org/walformat.html
- WAL lifecycle, `SQLITE_BUSY`, WAL-reset bug and fixed versions: https://www.sqlite.org/wal.html
- `sqlite3_close` vs deferred `close_v2`: https://www.sqlite.org/c3ref/close.html
- Alternative rollback journal DELETE and its own hot-journal recovery: https://www.sqlite.org/pragma.html and https://www.sqlite.org/atomiccommit.html
- Bundled libsqlite3-sys 0.38.2: https://docs.rs/crate/libsqlite3-sys/0.38.2

SQLite `DELETE` journal mode replaces `-wal`/`-shm` with rollback-journal semantics; it is **not** a remedy for path identity, concurrent owner, atomic OS-open or existing-profile authorization. **No journal_mode switch is proposed or permitted here**. The chosen product path remains compatible with WAL pending a separate review; no claim of durability under power loss or benchmark gain without evidence. `synchronous` and user-data retention policy must be qualified separately.

## 3. Minimal policy proposal: 2 gates and 1 owner, never conflated

| Stage / state | Observed prerequisite | Allowed behavior in this proposal |
|---|---|---|
| `DISCOVERED_UNADMITTED` | Filename/selector exists; no trusted owner lineage yet | Metadata-only operations *only if independently approved*; no SQLite open, PRAGMA or checkpoint |
| `CLAIM_PROVISIONAL` | Cooperative mutex claim and independently validated owned directory are observed | No existing-profile SQLite open; a free mutex is not clean-shutdown evidence |
| `IDENTITY_BOUND_UNADMITTED` | Main and sidecar provenance observed via reviewed atomic/handle-aware sequence, R1–R4 checks | **Still STOP** until full R1–R9 review, policy and explicit owner authorization |
| `SQLITE_RECOVERY_POTENTIALLY_REQUIRED` | Previous process crashed / WAL exists / incomplete close | **Not executed**. Later authorized owner may allow SQLite to handle recovery; never an application-side manual repair |
| `SESSION_ADMITTED` | *Hypothetical* separate operator approval and all R1–R9 admitted with recovery policy | Not reachable from this design or existing CI |
| `REVOKED` | Lineage ambiguity, `SQLITE_BUSY`, incomplete close, missing handle proof, policy mismatch, unsupported version | Fail closed; no SQLite open/reopen or writes to sidecars |

Candidate normal owner lifecycle after distinct admission: one Rust connection/actor, serialized state changes, SQLite-managed transaction/sidecars, no model-driven SQL, quiesce on shutdown, finalize statements/backups/BLOBs, close with verified result while claim held, then relinquish cooperative claim. **A successful close is not itself a cross-process identity attestation; a failed or deferred close cannot be called clean.** Persisting a custom clean-close witness is not in this candidate unless demonstrated necessary for *application-level* lineage and separately approved.

## 4. D3b-4 and D3b-5: what to prove next, without duplicating D3c

| Existing scope | Current evidence | Proposed next decision / oracle |
|---|---|---|
| **D3b-4** synthetic marker replay/swap/omission | **NOT_IMPLEMENTED**, durable format **NOT_AUTHORIZED** | First decide whether any marker exists. If native SQLite recovery + independent path identity suffice, **do not add a marker** or artificial replay suite; instead prove no unexpected marker dependency. If an application-specific marker becomes necessary, separately approve its format, creation and replay-negative tests on fresh disposable fixtures only |
| **D3b-5** crash phase timing | **NOT_IMPLEMENTED**, beyond current D3b approval | Future *separately approved* Windows CI fixture: terminate test child at bounded phases; distinguish committed vs uncommitted state, never claim actual power loss; refused successor opening until R1–R9/recovery authorization |
| **R4** WAL/SHM / sidecars | D3a fixture observations only | Keep identity and xShm* checks independent; do not infer `-shm` is durable recovery state |
| **R7** predecessor/new owner | D3b refusal proven only | Document conditions of eligible recovery; permission to open is separate from SQLite's ability to recover |
| **R9** release admission gate | NOT_PROVEN | Cannot be reached from these proposed documents or synthetic CI alone |

### Explicit STOP / non-goals

No attempt is made to access `M:\Fabulaxiom` or the operator's `%LOCALAPPDATA%\com.fabulaxiom.greenfield.v1` files, backups, ACLs, markers, WAL/-shm, historical or v7 databases. No v7 schema migration 007, no writer activation, no Tauri IPC, Windows Hello native, model runtime, SQLite journal changes, durable marker, recovery/reopen, S3/S4, or PR #215/#35 merge. New experiments require distinct, exact-scoped owner approval.

**Current authoritative statuses:** M3.2 `IN_PROGRESS_NOT_ACCEPTED`; writer and production R1–R9 `NOT_PROVEN`; A0 `EXISTING_PROFILE STOP`; G2B `NOT_ACCEPTED`; G2C `NOT_AUTHORIZED`; real G3 `STOP_UNAVAILABLE`; historical `PENDING_EXTERNAL_ATTESTATION(21/3/2)`; prospective `NOT_STARTED`. All docs/CI are subordinate to a fresh source SHA and protected ruleset review.

## 5. Gate for making this a real design choice

This is a **source-only study**, not a completed architecture approval. A design reviewer should evaluate (1) whether application-level cross-process lineage really needs a durable marker, (2) what minimal independently authenticated profile identity is achievable prior to SQLite xOpen, (3) exact single-SID cooperative-owner assumption, (4) SQLite version proof, (5) data-loss tolerance and `synchronous`, and (6) which disposable negative/positive crash experiments would require explicit owner approval. Favor the smallest experiment that answers a real uncertainty and **do not** repeat the already-qualified D3b refusal tests. Retain existing v6 Greenfield functionality while v7 remains blocked.
