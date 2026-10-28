# M3.2 v7 P1 D2 — integrated Windows disposable session, delegated xOpen and WAL/SHM evidence

**28 October 2026 — LAURENT EXPLICITLY AUTHORIZED D2 WINDOWS CI DISPOSABLE FIXTURES ONLY.** This qualification describes **test-only** Rust additions to `src-tauri/src/m32_sqlite_vfs_preopen_tests.rs`, which is declared under `#[cfg(all(test, windows))]` in `src-tauri/src/lib.rs`. No production Windows opener, Tauri State, IPC/CRUD, SQLite migration, database repair, persistent marker, runtime writer admission or local operator task is added. **Before exact SHA source CI: 216 Rust / 7 Greenfield / 41 SQLite guards / 149 continuity contracts EXPECTED, NOT QUALIFIED, NOT PASS.**

**Exact-head guard outcome (not transferable):** first D2 source `2bce090e7fc75aa238283b97752d971b1c7a3379`, [Windows CI #40752418946](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40752418946) **FAILED** in the early whole-tree Rust SQLite source inventory. It correctly detected **four new test-only Connection::open_with_flags_and_vfs occurrences and four SQLITE_OPEN_READ_WRITE markers** in the existing Windows cfg(test) VFS fixture: observed `(16,0,0,0,0,17,0)` vs previously pinned `(12,0,0,0,0,13,0)`. No Rust or other tests ran to completion. The revised candidate **explicitly reviews** these four opens/flags and updates only the exact-inventory baseline and existing guards for this one test-only path; unknown future opening sites must still STOP. New source CI is required; the failed run is NOT a PASS or production evidence.

## 1. Scope inherited from selected P1 and prior documentary D1

- [D1 P1-0 proof ledger](M3_2_V7_P1_SINGLE_OWNER_SESSION_PROOF_PLAN_20261028.md): user explicitly trusts cooperating processes of the same Windows user SID; malicious same-SID bypass is out of scope by threat-model decision, not technically blocked. P1 is the selected architecture; P2 isolated-principal broker deferred. R1–R9 still demand independent production evidence.
- Prior PR #215 documentary SHA `cb033fb27b5cc5a5f873d24b85c7f41864de4870`, exact [CI #40747739565](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40747739565) SUCCESS **210/7/41/148**; [issue #38 source-only comment #6477798724](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6477798724). Protected `main=90142d8c78dd8a84ee3f0ee1676a753c8521d78e`; #215 OPEN/DRAFT and #35 OPEN/DRAFT. Prior source CI does not qualify any new D2 code.
- **D2 bounds:** newly allocated %TEMP% fixture directory and random `Local\\Fabulaxiom-D2-Disposable-...` named mutex per test. Win32 named mutex is created with fixture default security only; there is **no production SID ACL/DACL** and no claim that a mutex excludes deliberate same-SID bypass. All file opens, renames and sidecars are under the fixture-owned directory. A child process is merely the same Windows CI test binary with an exact test-filter and fixture-only env vars. It never opens operator SQLite.

## 2. Integrated test-only claim, xOpen and sidecar path

The new `d2_p1_disposable_session` submodule reuses the existing `RegisteredFixtureVfs::with_policy`, `FileIdPrecheckPlan`, delegated Win32 FileId128 comparison **inside the actual xOpen callback**, and the copied `sqlite3_io_methods.xShmMap` mapping veto. The default VFS remains registered with `makeDflt=0`; fixture-specific VFS names are unique. No normal Rust build can compile these tests as a production SQLite opener. No `V7WriterAdmission` is minted.

1. **Claim:** create random `Local\\...` mutex; `WaitForSingleObject(..., 0)` only. A cooperative second process receives `WAIT_TIMEOUT` while the parent holds it, and may receive `WAIT_OBJECT_0` only after explicit close/release. An unexpected pre-existing named object is a STOP in each parent test. `WAIT_ABANDONED` means the waiter now owns a mutex but must **refuse** provenance and **not** call SQLite xOpen.
2. **Main file:** `create_new(true)` on a newly owned empty filename in the disposable directory. Observe volume + FileId128 and enforce a second comparison against the actual delegated SQLite native handle in xOpen, closing/vetoing on mismatch. The precheck-to-delegation interval remains **non-atomic** at the OS pathname level.
3. **WAL and SHM:** the fixture VFS may permit the test-only journal mode change to WAL on this fresh file and then mediate WAL via VFS xOpen and SHM via the separately wrapped xShmMap callback. Negative variants veto either one with no successful query/write after the veto. The -shm mapping **cannot** be inferred from a named -shm xOpen. Other io_methods hooks remain delegated and are **not** qualified for production.
4. **Close:** the positive fixture explicitly closes the SQLite connection before releasing the cooperative mutex, and verifies a second process can claim only afterward. This confirms an ephemeral test sequence, **not** an authenticated cross-process clean-close attestation or safe existing-profile restart.

## 3. Witness matrix (all tests new under cfg(test, windows))

| Exact Rust test | Fixture-only evidence / expected refusal | What it does not prove |
|---|---|---|
| `m32_d2_child_probe` | Child sees the same random named mutex; `contended`, `free`, `abandon` branch without opening SQLite | No operator process topology or ACL attestation |
| `m32_d2_p1_cooperative_owner_delegated_fileid_wal_shm_positive_is_not_admission` | Parent claim, child `WAIT_TIMEOUT`, delegated main FileId128 match, live fixture WAL xOpen + xShmMap delegation, explicit SQLite close and later child claim | No atomic OS open, no production writer or durable reopen provenance |
| `m32_d2_p1_identity_swap_after_cooperative_claim_vetoes_xopen` | After cooperative claim a controlled fixture rename/replacement between precheck and delegation causes delegated-handle FileId128 veto and SQLite open refusal | No prevention of arbitrary same-SID hostile namespace races |
| `m32_d2_p1_wal_veto_after_bound_main_handle_stops_before_wal_open` | Main handle can match, but selected VFS WAL xOpen returns SQLITE_CANTOPEN before its delegated WAL open; no fixture WAL sidecar created | Does not cover WAL identity verification on every possible open/close |
| `m32_d2_p1_shm_veto_after_bound_main_handle_stops_before_mapping` | Main handle can match and WAL switch may try, but xShmMap returns SQLITE_IOERR_SHMMAP before delegated mapping; no fixture SHM sidecar | Not complete xShmLock/xShmBarrier/xShmUnmap/restart coverage |
| `m32_d2_p1_abandoned_mutex_refuses_before_sqlite_xopen` | Child exits while owning fixture mutex; parent receives `WAIT_ABANDONED` and refuses before even invoking fixture SQLite xOpen | No independent crash- or power-loss-safe lifecycle proof |

The fixtures run in the existing Windows Rust test suite; they do not access `M:\\Fabulaxiom` or `%LOCALAPPDATA%\\com.fabulaxiom.greenfield.v1`. The test-owned directory is destroyed only via its `DisposableRoot` fixture ownership. The child process inherits CI user identity; no privileged process, OS credential, Hello prompt, or operator action is involved.

## 4. Interpretation and remaining R1–R9 gaps

**D2 positive may support only partial disposable witnesses** for R3 delegated main identity, a cooperative slice of R6, and separated R4 WAL-open vs SHM-map callback behavior. **All R1–R9 for production remain NOT_PROVEN**, especially:

- **R1/R2:** production SID-specific DACL/namespace and pinned ancestor identity with OS-open non-atomicity; no hostile same-SID exclusion claim.
- **R4/R5:** complete journal/WAL/SHM object identity and all I/O callbacks, lineage/authenticated profile/schema, and recovery semantics. Veto after a delegated open can itself have filesystem side effects.
- **R6/R7/R8:** durable single-owner generation, actor queue and cancellation, xClose failure propagation, abandoned/crashed process and full restart proof; no operator EXISTING_PROFILE admission from a fixture close.
- **R9:** independent source review, production security review, protected merge and **a new owner authorization** for runtime work are missing. A Windows source CI SUCCESS is not a production qualification.

**M4–M7/Ollama unchanged:** the future local model obtains source-cited fiches, histories, canon and chronology through a Fabulaxiom-controlled, read-only, versioned in-memory context packet after a bounded single-owner SQLite read. This D2 does **not** implement that pipeline or create a second SQLite reader, SQL model tool or write-capable Ollama action.

## 5. Governance and next gate

A source-only CI success can qualify these **disposable test witnesses only**, not D3, S3/S4, runtime IPC, migration 007, persistent marker, Windows Hello native, operator SQLite, ACL, backups, logs or sidecars. Keep A0 cross-process `EXISTING_PROFILE` STOP; writer `NOT_PROVEN`; M3.2 `IN_PROGRESS_NOT_ACCEPTED`; G2B `NOT_ACCEPTED`; G2C `NOT_AUTHORIZED`; G3 real `STOP_UNAVAILABLE`; historic `PENDING_EXTERNAL_ATTESTATION(21/3/2)`; prospective `NOT_STARTED`; #35 OPEN/DRAFT. A further narrow approval and proof design is required for actual WAL/SHM identity custody, durable recovery, production VFS/session and any actor/IPC integration.

**Technical references (primary):** [SQLite VFS callbacks](https://www.sqlite.org/c3ref/vfs.html), [sqlite3_io_methods and SHM](https://www.sqlite.org/c3ref/io_methods.html), [SQLite WAL/read-only/shm-index](https://www.sqlite.org/wal.html), [Win32 CreateMutexExW](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-createmutexexw), [mutex abandonment and ownership](https://learn.microsoft.com/en-us/windows/win32/sync/mutex-objects), [Win32 CreateFileW sharing/open semantics](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew), [FileId128 FILE_ID_INFO](https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_id_info).
