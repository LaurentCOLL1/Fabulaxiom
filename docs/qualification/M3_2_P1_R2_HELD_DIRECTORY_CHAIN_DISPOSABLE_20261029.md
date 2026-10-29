# Fabulaxiom M3.2 — P1 R2 held Windows ancestor-chain CI experiment

**2026-10-29 — NEW SOURCE CANDIDATE, NOT YET QUALIFIED BY EXACT-HEAD CI. TEST-ONLY. NEVER OPERATOR ADMISSION.**

## Verified immediate baseline

Protected [PR #223](https://github.com/LaurentCOLL1/Fabulaxiom/pull/223) merged with exact head `236a75b224800975ab88d3320bdc8fcf03db011b` into `main=5c656ea0a0463e13835b7ff50482b11fed3d53fb`. Source Windows [CI #40881357491](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40881357491) SUCCESS, followed by independent [postmain CI #40883026858](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40883026858) **completed/SUCCESS** at the exact merged SHA. The source run passed **233 Rust / 7 Greenfield / 43 SQLite opening-site guards / 150 continuity contracts** including five new P1 prefix Win32 tests. All 26 earlier VFS tests remained byte-identical. #215 and #35 stay OPEN/DRAFT. Ruleset `Protect main` is active, requires strict `Windows frontend and Rust checks`, zero bypass.

## The next smallest missing R2 proof

PR #223 explicitly ended at `R2AncestorsNotPinned` after a new, empty test-only main FileId128 and cooperative Local mutex. This candidate uses **four separate `#[cfg(all(test, windows))]` unit tests** to bind one new fixture-owned ancestor *chain* while keeping the mutex and native FileId checks:

- New unique `%TEMP%/fabulaxiom-r2-held-chain-*/fictional-profile/database/new.sqlite3` is created exclusively via Windows filesystem operations; this is **not** the operator's `com.fabulaxiom.greenfield.v1` profile and contains no SQLite content.
- Open file handles for the *three fixture-owned* ancestors (root, fictional-profile, database) use `FILE_FLAG_BACKUP_SEMANTICS | FILE_FLAG_OPEN_REPARSE_POINT`, `FILE_READ_ATTRIBUTES`, and `FILE_SHARE_READ | FILE_SHARE_WRITE` **without `FILE_SHARE_DELETE`**. Obtain real `GetFileInformationByHandleEx(FILE_ID_INFO)` volume and 128-bit IDs for each held handle, then re-open and compare these objects. Distinguish successful handle observations from atomic namespace proof.
- A new test-only named Local mutex is held across the observations. A positive R2 prefix (including matching new fixture main FileId128 and absent sidecar names) **always stops at `R4ShmMappingUnproven`**; no V7 token can be created.
- Negative witnesses: attempt parent-directory rename while pinned; if the filesystem disallows it, preserve the tested binding; if it permits the move, the validator must STOP and the fixture is restored. Swap the main name while directory parents remain pinned; reject via `MainFileChanged`. Create never-SQLite synthetic `-wal`, `-shm`, and `-journal` files; reject without modifying sentinel bytes.

This is stronger than a lexical or two-instant preflight, **but not** sufficient to claim R2 production. The parent of the disposable root (OS temp namespace), a different future profile, hostile same-SID processes, memory-mapped sidecar identity, the writer's actual SQLite `xOpen` and the handoff to that operation are outside this fixture. Even pinned objects and revalidation cannot make a separate pathname-based SQLite open atomic; a future live VFS boundary must bind actual delegated SQLite handles to authenticated ancestors and sidecars, under its own reviewed scope. No IPC, no migration, no model runtime. Official references: [Microsoft directory handles](https://learn.microsoft.com/en-us/windows/win32/fileio/obtaining-a-handle-to-a-directory), [CreateFileW sharing and reparse behavior](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew), [FILE_ID_INFO](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-getfileinformationbyhandleex), [SQLite WAL/index](https://sqlite.org/walformat.html).

## Separate test status

Source: `src-tauri/src/m32_r2_held_parent_chain_tests.rs` (test-only, **zero SQLite opening sites**, no production module imports), plus `#[cfg(all(test, windows))]` in lib.rs. New SQLite-opening-site test #44 confirms the zero count; continuity contract #151 preserves the hard STOPs and the successful #223 postmain. Neither old source inventory nor 26 VFS tests nor 5 tests of PR #223 need alteration.

**Expected, NOT yet PASSED:** **237 Rust / 7 Greenfield / 44 SQLite guard / 151 continuity**, four new native Win32 R2 tests. The exact new HEAD must pass the full Windows workflow, with immutable diff, reviews/threads and `Protect main` audit before considering a protected merge with `expected_head_sha`. After any merge, independently run postmain CI on the new SHA and append evidence to issue #38. Do not reuse CI of an earlier head.

## Boundary / hard STOP

R2 fixture-level held handle observation **does not** prove authenticated production parent namespace; R3 real production delegated SQLite xOpen **NOT_PROVEN**; R4 WAL/-shm mapping/locking **NOT_PROVEN**; R5 schema lineage, R6 owner actor admitted, R7 prior-generation policy, R8 production resource ownership, R9 independent release **NOT_PROVEN**. The prepared Rust writer remains intentionally unwired.

**A0 EXISTING_PROFILE STOP; M3.2 IN_PROGRESS_NOT_ACCEPTED; writer and production R1–R9 NOT_PROVEN; G2B NOT_ACCEPTED; G2C NOT_AUTHORIZED; real G3 STOP_UNAVAILABLE; historical PENDING_EXTERNAL_ATTESTATION(21/3/2); prospective NOT_STARTED.** No operator SQLite v6/v7, -wal/-shm/-journal, ACL, backups, markers, real recovery, S3/S4, migration 007, Tauri writer IPC, native Windows Hello or Ollama model access. PR #215 and #35 remain draft. The owner prioritizes Greenfield Fabulaxiom usability, but this fixture does not itself activate a product feature.
