# M3.2 R3 — inter-process Win32 main rename refusal (CI disposable only)

**29 October 2026 — UNQUALIFIED CANDIDATE, NO PRODUCTION ADMISSION.** Scope: two new Rust `#[test]` fixtures only in the pre-existing Windows test-only module, single already-inventoried SQLite opening site. Baseline protected `main=a93f766ffb5f142d62617cb9cecc96f9f2ef0b2f` from PR #227 (its source exact CI #40927616639 SUCCESS: 243 Rust / 7 Greenfield / 45 SQLite inventory / 152 continuity). Independent postmain push CI #40935910695 must be verified separately; never transpose source CI to postmain.

## Experiment

The preceding PR #227 proved a single-process fixture could hold the native main file HANDLE without `FILE_SHARE_DELETE` while SQLite's separate default-Windows-VFS `xOpen` reopened the same FileId128. That does NOT guarantee path-to-handle atomicity. This candidate asks whether the same denial holds when a **distinct Windows process** attempts a conflicting rename.

A bounded child mode, `m32_r3_child_rename_probe_only_fresh_disposable_main`, runs the same already-built Rust test executable with `--exact` and an explicit, validated `%TEMP%/fabulaxiom-r23-delegated-disposable-*/fictional-profile/database/invented.sqlite3` path. Without that environment variable, the child test is a no-op. The child may only try to rename this invented file to an invented sibling and terminates with a distinct test result code. No operator path or arbitrary command is accepted.

The parent `m32_r3_other_process_rename_is_refused_before_and_during_sqlite_xopen`:
1. Exclusively creates a fresh zero-byte main in its own temporary directory and records Win32 `FILE_ID_INFO`.
2. Pins the three parent directories and opens a main-file claim with share READ|WRITE **without share DELETE**.
3. Runs a separate child rename attempt; requires refusal and unchanged main identity.
4. Uses the **single previously audited test-only SQLite open site** while claim and pins remain held; compares actual SQLite handle FileId128; runs the child again and requires refusal and stable identity.
5. Explicitly closes SQLite without SQL, then releases main claim and proves the same child rename succeeds while the pinned parent-directory handles remain; verifies the displaced file retains the initial identity.

Expect **245 Rust** / **7 Greenfield** / **45 SQLite inventory** / **152 continuity** tests **ONLY IF exact-head Windows CI confirms them**; 2 new test functions, old 6 unchanged; no new SQL constructor or production writer path. Any failure or flaky sharing outcome must be reported and the PR left unmerged; never relax assertions to manufacture PASS.

## Architectural ceiling

The candidate tests one specific Win32 sharing behavior in a cooperative, same-user two-process fixture. Microsoft documents that omitting `FILE_SHARE_DELETE` prevents subsequent compatible opens requesting delete access (which includes rename). This does not prove a malicious process cannot mutate data via a separately authorized write handle, cannot exploit a hard link/reparse/namespace path, or cannot bypass app-level cooperation. It does **not** prove an atomic controlled `xOpen`, WAL/-shm `xShmMap/xShmLock/xShmUnmap` (R4), clean predecessor generation (R7), or admission of any existing profile.

### STOP and promotion
`A0 EXISTING_PROFILE STOP`; M3.2 `IN_PROGRESS_NOT_ACCEPTED`; writer and R1–R9 production `NOT_PROVEN`; G2B `NOT_ACCEPTED`; G2C `NOT_AUTHORIZED`; G3 `STOP_UNAVAILABLE`; historical `PENDING_EXTERNAL_ATTESTATION(21/3/2)`; prospective `NOT_STARTED`. No operator SQLite v6/v7, ACL, backups, WAL/shm/journal, migration 007, IPC, recovery, markers, native Hello or Ollama runtime. PR #215 and #35 remain draft. A separate R4 decision is mandatory.

Before any merge: exact-source Windows CI SUCCESS, no unreviewed change or unresolved thread, active strict Protect main zero bypass, `expected_head_sha` squash; then separate postmain push CI and an append-only factual update to issue #38. Maintain both resume prompts and continuity/roadmap.

References: [Win32 CreateFile share modes](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew), [SQLite VFS](https://www.sqlite.org/vfs.html), [SQLite WAL shared memory](https://www.sqlite.org/wal.html).
