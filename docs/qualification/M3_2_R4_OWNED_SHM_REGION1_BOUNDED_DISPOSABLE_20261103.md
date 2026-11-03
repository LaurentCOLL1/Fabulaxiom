# M3.2 — R4 SHM region 1 (two held native pages) — Windows disposable candidate

**3 November 2026 — CANDIDATE, NOT QUALIFIED.** Parent protected `main=8a87c84647732a710dce5073c060949d95fa8c02`, PR #267 documentation-only squash, Windows postmain #41657918654 pending at candidate creation. No operator, app-runtime or writer admission.

## Test-only implementation scope

In the pre-existing `#[cfg(all(test,windows))]` **non-default** VFS (`src-tauri/src/m32_r4_registered_owned_shm_vfs_disposable_tests.rs`), the freshly `CREATE_NEW`-created **owned** `%TEMP%` SHM sidecar is exactly 64 KiB (two fixed 32 KiB WAL-index regions), and `MapViewOfFile` maps both regions from the **same retained native SHM HANDLE**. The existing xShmMap checks the pinned FileId128 with a non-atomic pathname recheck and allows only `iPg=0` or `iPg=1` with exact 32768-byte `pgsz` and `isWrite` flag 0/1. It returns a checked offset inside the 64 KiB mapped view, never an arbitrary caller offset. Negative, overflow-size, third-region, wrong-size, and unsupported extension requests return `SQLITE_IOERR_SHMMAP` with null output and a refusal counter.

New executable Windows test: `r4_owned_xshm_region_one_shared_native_mapping_and_bounded_veto_disposable`. It opens two SQLite connections in `locking_mode=NORMAL`, `journal_mode=WAL` using the already registered test-only VFS and test-owned database. It obtains **the actual `sqlite3_file*` from SQLite** via `SQLITE_FCNTL_FILE_POINTER` for each connection, invokes their genuine `xShmMap` callbacks for page 1, verifies they expose the same backing bytes (without using any production content), and checks page 0 remains usable after all invalid mapping attempts. It checks retained native main and SHM FileId128 across the request and verifies xShmUnmap is reached. Source checks should assert these callbacks are only linked into test modules, never `App.tsx`, application VFS or production IPC.

## Exactly what this DOES NOT prove

- This is a **fixed two-page** mapping, **not** general WAL-index growth, multiple maps over a changing file, high-volume use, or stress under all interleavings. Replacing SHM by name can still race the non-atomic identity check. Main/WAL/SHM are **not** atomically bound to one held native custody lifetime, and the stock Windows VFS keeps private handles for delegated files.
- Neither malicious same-SID writers, renames/reparse/ABA across all processes, recovery, crash atomicity nor V7 writer admission has been proved. Existing two-OS-process fixture covers one cooperative WAL contention scenario, not adversarial process freedom.
- **No** access to existing `%LOCALAPPDATA%\com.fabulaxiom.greenfield.v1`, `M:\Fabulaxiom` working data, operator v6/v7 SQLite, journals/backups, IPC writer, runtime migration 007, native Hello, markers or recovery. `App.tsx`, Rust production, capabilities and default VFS unchanged.

## Expected qualification — NOT ACQUIRED

Windows exact HEAD CI expected **303 Rust, 7 Greenfield, 68 inventory, 183 continuity and Chromium 85/85 normal and strict CSP**; these are expected counts, never a PASS until actual CI confirms. Review full diff, reviews/threads, `Protect main` active strict bypass=[], protected squash with `expected_head_sha` only on SUCCESS; independent postmain CI and append-only issue #38. This is an R4 fixture **subproof**, not passing R4 as a whole.

**Strategy active: PRODUCT_FIRST_PARALLEL_SAFETY**, P1/P2a/P2b/P3a–P3e fictional product tests already qualified, P4 admission separate; R4–R9 in parallel. Warn owner before strategy change. glib 0.18.5 Linux GTK3 GHSA-wrw7-89jp-8q8g / issue #160 **OPEN_NOT_REMEDIATED**; never dismiss or claim repair.

**STOP unchanged:** M3.2 IN_PROGRESS_NOT_ACCEPTED; writer/R1–R9 NOT_PROVEN; G2B NOT_ACCEPTED; G2C NOT_AUTHORIZED; G3 STOP_UNAVAILABLE; historical PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED; D3b-4/5 STOP. Fixture/CI `!=` production admission.

References: SQLite [WAL](https://www.sqlite.org/wal.html), [VFS xShmMap contract](https://sqlite.org/c3ref/io_methods.html), [SQLITE_FCNTL_FILE_POINTER](https://sqlite.org/c3ref/file_control.html).
