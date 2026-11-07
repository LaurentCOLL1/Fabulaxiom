# M3.2 R4 — Post-delegate native WAL veto stays poisoned (disposable)

7 November 2026 — CANDIDATE NOT QUALIFIED. Parent protected main `591af5e965944e89e3038a43753b1d096d75f4dc`; independent parent postmain Windows #42343723351 must reach terminal SUCCESS exact SHA before merge.

Only the existing non-default Windows #[cfg(all(test,windows))] SQLite VFS under fresh %TEMP% CREATE_NEW. A native WAL HANDLE mismatch or injected veto detected **after** delegated SQLite WAL xOpen now latches the preheld WAL refusal. Two new Rust tests check the post-delegate veto cannot be undone by removing the synthetic fault flag and that an already-latched refusal blocks WAL xOpen before delegated HANDLE admission. Positive NORMAL-WAL path and all other test-only behavior remain isolated.

**Expected, not qualified:** 326 Rust / 7 Greenfield / 69 SQLite source inventory / 183 continuity / 373 Vitest / Chromium 85/85 normal+CSP / 19 fictional blobs. No success may be claimed until final source SHA Windows CI terminal/SUCCESS.

This test validates persistent rejection of *detected* mismatches, not an atomically held main/WAL/SHM unit, not unseen ABA/TOCTOU, and not resistance to a hostile same-user Windows writer. No production VFS or P4 runtime/writer admission. SQLite VFS xOpen's associated-main file-object constraint is still honored.

PRODUCT_FIRST_PARALLEL_SAFETY unchanged (notify before strategy changes); M3.2 IN_PROGRESS_NOT_ACCEPTED (~45% estimate), R1–R9 NOT_PROVEN, real P4 STOP, G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE, historical PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED, glib issue #160 OPEN_NOT_REMEDIATED. Do not touch operator v6/v7 or Greenfield profile, backups/journals, runtime IPC writer, migration 007, native Hello, marker or recovery.

Exact final HEAD Windows CI, parent postmain, reviews/threads, Protect main ACTIVE strict bypass=[], guarded squash expected_head_sha, independent postmain, issue #38 append-only. Fixture CI != admission.
