# Fabulaxiom M3.2 — R3 held main HANDLE without FILE_SHARE_DELETE (Win32 disposable-only)

**29 October 2026 — NEW CANDIDATE, exact-head Windows CI NOT YET QUALIFIED. NO ADMISSION OR WRITER.**

## Source authority
Live protected main at design time: `ba51ea692a9079a968dd1f54a8d9ea6d87559d50` (documentation-only PR #226), postmain [#40909071737](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40909071737) completed/SUCCESS. Active ruleset `Protect main` 24895490, strict Windows check, zero bypass. PR #215 and PR #35 remain OPEN/DRAFT. Previous R2->R3 test evidence is [PR #225](https://github.com/LaurentCOLL1/Fabulaxiom/pull/225) and [R23 qualification](M3_2_P1_R2_R3_DISPOSABLE_SQLITE_HANDLE_BOUNDARY_20261029.md); passing its post-open FileId128 match alone does not prove pre-open atomicity.

## Narrow falsifiable R3 improvement
The existing `src-tauri/src/m32_r23_sqlite_handle_boundary_tests.rs` pins the three ancestors with handles excluding DELETE sharing, but the `before` main-file observation is released before SQLite's default path-based `xOpen`. That leaves a deterministically demonstrated substitution gap.

The new tests keep **a second, independent main FILE HANDLE** open through preflight and actual SQLite `xOpen`, with `OpenOptionsExt::share_mode(FILE_SHARE_READ | FILE_SHARE_WRITE)` (no `FILE_SHARE_DELETE`). They check:
1. **Negative rename** on a newly created `%TEMP%` test file: `std::fs::rename` of the held main must fail, its FileId128 and pathname must remain stable, and the same rename should succeed once the main claim is released. No SQLite or SQL is invoked in this test.
2. **Positive SQLite compatibility**: the existing SINGLE inventoried `Connection::open_with_flags(...SQLITE_OPEN_READ_WRITE)` site can open the *fresh, zero-byte, claim-held* file while the three parent handles and main claim remain held. The actual SQLite HANDLE's FileId128 matches that claim. The connection closes without SQL; R4 explicitly still returns `R4MappingUnproven`.

All data are entirely fictional and freshly created; the two tests are `#[cfg(all(test, windows))]` via the already guarded module in `lib.rs`. Rust expectation is **243** tests (241 + 2), Greenfield **7**, source SQLite inventory **45**, continuity **152**, **EXPECTED NOT PASS UNTIL EXACT-HEAD CI**. The source inventory maintains **exactly one** SQLite open call in this file, adds no new production/IPC entrypoints and checks six tests. Counts are not evidence of production safety.

## Architectural limits and next discriminating experiment
A Win32 handle that excludes `FILE_SHARE_DELETE` should block a compliant rename/delete that conflicts with that held open, but **this is not proof of a fully atomic and controlled SQLite VFS `xOpen`**. The default VFS still reopens by path, and the experiment does not prove protection against reparse/hard links, sharing modes of a concurrent actor, parent namespace attacks, all `xAccess/xDelete/xFullPathname` calls, SQLite sidecars, failed open cleanup, or a hostile same-SID process. The trusted-cooperative same-SID assumption is a product choice, not a Windows identity guarantee. Results may vary by file system and sharing semantics.

**Decision for R3: NOT_PROVEN production, even if both tests pass.** Next: test simultaneous two-process sharing/rename with fail-closed ownership, test false assumptions on the same initial path and pinned ancestors, and design a controlled VFS or OS-handle handoff which *does not delegate any unauthenticated open*. If path-based default VFS delegation remains raceable, retain STOP. A custom SQLite VFS requires correctly implementing and reviewing all necessary `sqlite3_vfs`/`sqlite3_io_methods` contracts and WAL/SHM handling (R4), not simply comparing IDs post-open.

## STOP / governance
A0 `EXISTING_PROFILE STOP`; M3.2 `IN_PROGRESS_NOT_ACCEPTED`; writer and production R1–R9 `NOT_PROVEN`; G2B `NOT_ACCEPTED`; G2C `NOT_AUTHORIZED`; G3 `STOP_UNAVAILABLE`; historical `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`. No operator v6/v7, `M:\\Fabulaxiom`, `%LOCALAPPDATA%\\com.fabulaxiom.greenfield.v1` (documentary paths only), ACLs, backups, journals/sidecars, durable markers, D3b-4, recovery, native Hello, writer IPC, S3/S4 or migration 007. No reuse of an existing fixture.

Merge only after exact-head Windows CI SUCCESS, diff/reviews/threads, active strict `Protect main`, `expected_head_sha`; then independently verify postmain push CI, append-only #38, both resume prompts/handoff/roadmap. If CI fails, leave open and report failure instead of asserting PASS.

## Technical references
- [SQLite VFS](https://www.sqlite.org/vfs.html) and [xOpen contract](https://www.sqlite.org/c3ref/vfs.html).
- [SQLite I/O methods](https://www.sqlite.org/c3ref/io_methods.html).
- [Microsoft CreateFile and share modes](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew) and [GetFileInformationByHandleEx](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-getfileinformationbyhandleex).
