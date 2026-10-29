# Fabulaxiom M3.2 — P1 R1–R4 Windows integrated prefix refusal (29 October 2026)

**CANDIDATE / EXACT WINDOWS CI PENDING. NOT PRODUCTION ADMISSION.**

## Proven baseline and new scope

Protected [PR #222](https://github.com/LaurentCOLL1/Fabulaxiom/pull/222) was merged via exact-head squash to `main=35036c09f62e12d96639ac318b074b9b72f5f1e3`; source [CI #40862474803](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40862474803) SUCCESS (228 Rust, 7 Greenfield, 42 SQLite inventory, 149 continuity), including the four D3b-5 fixture tests. Independently, [postmain CI #40867166160](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40867166160) is completed/SUCCESS at precisely that main SHA. Main is protected by active strict ruleset `Protect main`, no bypass.

This new *test-only* `#[cfg(all(test, windows))]` module `src-tauri/src/m32_p1_integrated_prefix_tests.rs` combines **actual Windows kernel objects** and FileId128 observations under newly created, owned `%TEMP%/fabulaxiom-p1-prefix-fixture-*` roots. The five tests deliberately use **no SQLite connection**, no new or existing database opener, and no runtime writer. A test-owned `new.sqlite3` is just an empty file created with `create_new(true)`, not a Fabulaxiom profile. The test-only mutex uses an unpredictable `Local\\Fabulaxiom-P1-Prefix-*` name. A successful mutex claim and observed volume/FileId128 match only lead to `R2AncestorsNotPinned`, never `SESSION_ADMITTED`.

## Five executable boundaries (Windows CI only)

| Test | What is observed | Fail-closed oracle |
|---|---|---|
| Fresh claim / identity | fresh Local mutex + Win32 FILE_ID_INFO on the open main file + lexical root and empty sidecar names | **R2 ancestors not pinned; no SQLite open** |
| Main-name substitution | renaming a newly created empty file, replacing its name with another `create_new` file | identity mismatch => STOP |
| Unexpected sidecars | artificial, never-SQLite `-wal`, `-shm`, `-journal` containing sentinel bytes | refuse; sentinel bytes unchanged |
| Lost mutex provenance | drop the last handle, create a fresh apparently-free named mutex | refuse cross-process predecessor attribution despite mutex success |
| Path escape | file name `new.sqlite3` under a different lexical descendant | refuse unowned path |

These tests are an **early prefix integration**, not a claim that R1–R4 are qualified for production. In particular:

- **R1**: actual current-process cooperative named-mutex claim is observed; SID/ACL/integrity and stronger external-process contention are **not authenticated** by this module.
- **R2**: a reparse-attribute / lexical-root negative check is performed. Ancestor *handles* and atomic namespace binding are **NOT_PROVEN**.
- **R3**: native Win32 FileId128/volume is compared for a pre-open fixture handle, but **no delegated SQLite xOpen**, no guarantee against TOCTOU and no SQLite side effects are exercised here. Existing separate D2/D3a VFS fixtures remain the only test-only witness for delegated xOpen.
- **R4**: artificial sidecar *names* cause refusal; actual WAL xOpen, SHM mappings, locks and callbacks are **NOT_PROVEN** by this module. D3a separate tests remain unchanged.
- **R5–R9**: authenticated schema/lineage, owner actor custody, crash/restart/admission, C ABI lifecycle and release decision remain **NOT_PROVEN**. A0 `EXISTING_PROFILE STOP` is mandatory.

No power-loss proof, no R7 marker replay D3b-4 (NOT IMPLEMENTED), no application-level durable provenance marker. SQLite's own WAL recovery and the application's authority to open a profile are distinct. WAL recovery is not performed by these tests. References: [SQLite WAL](https://www.sqlite.org/wal.html), [WAL recovery format](https://www.sqlite.org/walformat.html).

## Source guard, expected CI and operator boundary

The module has **five Windows test functions, zero SQLite opening sites**; it is visible only to Windows Rust unit tests and requires a new inventory negative guard. Expected full Windows CI totals after this candidate: **233 Rust / 7 Greenfield / 43 source-inventory / 150 continuity**, **NOT PASS until exact-head logs**. Original 26 VFS Windows fixture tests and four D3b-5 tests must stay byte-identical. All changes are in a protected PR reviewed against exact current `main`, with reviews/threads and strict status check, only then `expected_head_sha` merge, independent postmain CI, and issue #38 append-only.

**Forbidden:** opening or changing the Windows operator's `M:\\Fabulaxiom`, `%LOCALAPPDATA%\\com.fabulaxiom.greenfield.v1`, v6/v7 SQLite, operator WAL/-shm/journal, backup/ACL/marker, S3/S4, new IPC, migration 007, Windows Hello native, model/Ollama runtime or any production admission. Local operator machine paths are documentary only, not accessed by GitHub CI.

**STOP status:** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, writer and production R1–R9 `NOT_PROVEN`, G2B `NOT_ACCEPTED`, G2C `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`, historical `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`. PR #215 and #35 remain draft.
