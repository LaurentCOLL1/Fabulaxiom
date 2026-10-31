# M3.2 — R4 Win32 same-held-HANDLE mapping on disposable SHM-like files

**31 October 2026 — CANDIDATE, NOT QUALIFIED until exact-head Windows CI.** Parent protected `main=8f582c2f9cf1a7e0a346d3ef9b5258acc1d1d772` after PR #245; source [CI #41149090126](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/41149090126) SUCCESS at exact HEAD (279 Rust / 7 Greenfield / 57 inventory / 167 continuity); independent [postmain #41151561992](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/41151561992) completed/SUCCESS at exact merge SHA.

## New bounded experiment

Two `#[cfg(all(test,windows))]` Rust tests create brand-new `-shm`-suffixed files using `create_new(true)` in an isolated, per-test `%TEMP%` directory. Full `FileIdInfo` (volume + FileId128) is measured on the *held File HANDLE* which is passed directly to `CreateFileMappingW`, then `MapViewOfFile`; a byte in the mapped view is exercised and identity reverified, with explicit `UnmapViewOfFile` and `CloseHandle`. A separate test rejects conflation with a different fixture-owned file. No real SQLite connection, WAL or main database is opened by this new module.

Microsoft documents the [CreateFileMappingW](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-createfilemappingw) handle-to-mapping contract, [MapViewOfFile](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-mapviewoffile) and [GetFileInformationByHandleEx](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-getfileinformationbyhandleex).

This **only** proves provenance for the native mapping *this test owns*. It does **not** authenticate the actual SQLite `xShmMap` HANDLE used by default Win32 SQLite or implement native `xShm*` for R3, or prove atomic custody across main/WAL/SHM. No production writer/admission, Tauri IPC, migration 007 or operator v6/v7/profile IO. All proofs remain fixture-local.

**Expected (NOT PASS until CI):** 281 Rust / 7 Greenfield / 58 inventory / 168 continuity. Mandatory exact-head Windows terminal CI and logs; full diff, reviews/threads; active Protect main strict required checks bypass=[]; protected squash expected_head_sha if qualified; independent postmain and #38 append-only.

**STOP:** M3.2 IN_PROGRESS_NOT_ACCEPTED ; writer/R1–R9 NOT_PROVEN ; G2B NOT_ACCEPTED ; G2C NOT_AUTHORIZED ; G3 STOP_UNAVAILABLE ; historical PENDING_EXTERNAL_ATTESTATION(21/3/2) ; prospective NOT_STARTED ; D3b-4/5 STOP, D3c design-only. No original data, Greenfield existing profile, native Hello, durable marker or recovery.

**Next:** build/test an actual custom SQLite xShmMap handle-bound VFS lifecycle on brand-new disposable Windows fixtures, never by re-opening a name while assuming it is the handle SQLite mapped; preserve R3, P1, reparse, ABA, identity and epoch refusal.
