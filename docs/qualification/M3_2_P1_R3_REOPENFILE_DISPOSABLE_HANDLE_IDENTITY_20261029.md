# M3.2 R3 — Win32 ReOpenFile from an already held file object (test-only)

**29 October 2026 — CANDIDATE NOT YET QUALIFIED ON EXACT-HEAD WINDOWS CI; NO SQLITE PRODUCTION ADMISSION.**

## Ground truth
Previous PR #228 protected squash `main=cc975bcb34e77e0c2507d3de7ebcd3b3392800db`, source SHA `252a823b307e5f0fb9ee70ffd180ea53645b5757`, exact source CI [#40936630691](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40936630691) completed/SUCCESS **245 Rust / 7 Greenfield / 45 SQLite inventory / 152 continuity** including both inter-process R3 tests. Independent postmain push CI #40938029139 is a distinct run and must be checked terminal separately; its state is not inherited from source.

[Microsoft's ReOpenFile](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-reopenfile) takes an existing `HANDLE` created with CreateFile and returns a new opened `HANDLE` for that object, with requested access/sharing/flags. It does not accept the pathname as input. This offers a concrete alternative to default SQLite's second name-based `xOpen`, whose FileId128 has only been verified *after* open in earlier candidates.

## Falsifiable Windows CI fixtures
Two new `#[test]` functions under the already `#[cfg(all(test, windows))]` module `m32_r23_sqlite_handle_boundary_tests.rs`:
1. **Stable held object:** `m32_r3_reopenfile_preserves_live_disposable_main_identity_without_path_lookup` exclusively creates a fresh `%TEMP%/fabulaxiom-r23-delegated-disposable-*/fictional-profile/database/invented.sqlite3`, holds a Win32 main handle without FILE_SHARE_DELETE, and calls `ReOpenFile`. Both HANDLE FileId128 values must match and rename must be denied while held.
2. **Controlled pathname substitution:** `m32_r3_reopenfile_binds_original_file_even_after_name_replacement` creates a new test-owned main with delete sharing expressly enabled, renames that main to a sibling, creates a distinct replacement at the same original pathname, then calls `ReOpenFile` **on the original handle**. The reopened FileId128 must be the old original, not the new pathname occupant. All handles close under Rust `File` ownership; the original HANDLE is never closed by the ReOpenFile wrapper.

No SQLite access, SQL, VFS registration, WAL/-shm/-journal, marker, IPC, migration 007, operator file or runtime writer in these new tests. The pre-existing single SQLite opening expression in this file is unchanged. Expected **247 Rust / 7 Greenfield / 45 source inventory / 152 continuity** only; **not PASS until new exact-head CI**. All prior eight R2/R3 tests retained without rewriting.

## Limit and next architecture gate
Even if the OS-level result passes, **SQLite's built-in Windows VFS does not automatically consume the ReOpenFile HANDLE**. An adapter must correctly implement the complete `sqlite3_vfs` / `sqlite3_file` / `sqlite3_io_methods` contract, ensure main file handle is the owned and admitted one, avoid fallback to unauthenticated pathname opens, and bind WAL/-shm identities and all `xShmMap/xShmLock/xShmBarrier/xShmUnmap/xClose` callbacks to the exact same session. That is a separate R3/R4 design and test decision, not demonstrated here. It must refuse every ambiguous/unhandled file type before delegating and cannot silently promise the Windows default VFS will take an already opened HANDLE. ReOpenFile does not prove protection against unrelated write-capable handles or malicious same-SID actors.

**STOP remains:** A0 EXISTING_PROFILE STOP; M3.2 IN_PROGRESS_NOT_ACCEPTED; writer and production R1–R9 NOT_PROVEN; G2B NOT_ACCEPTED; G2C NOT_AUTHORIZED; G3 STOP_UNAVAILABLE; historical PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED; #215/#35 draft. No real operator databases/sidecars/ACL/backups, durable marker, recovery, S3/S4, writer IPC, native Hello, Ollama runtime or migration 007.

Any merge requires exact-head CI SUCCESS, reviewed changed-file diff, reviews/threads, active strict Protect main and zero bypass, squash with `expected_head_sha`, postmain independent CI, issue #38 append-only and both resume prompts/handoffs/roadmap updated. Do not rewrite prior historic proofs.

References: [ReOpenFile](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-reopenfile), [Win32 sharing](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew), [SQLite VFS](https://www.sqlite.org/vfs.html), [SQLite WAL](https://www.sqlite.org/wal.html).
