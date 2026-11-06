# M3.2 R4 — preheld WAL/native triad, disposable-only candidate

6 November 2026. Candidate, not qualified. Parent main c3d2bded3c9e562f35db5a8dfd575658e36f2a89, independent postmain #42151182149 SUCCESS.

A Windows cfg(test) experiment in the already nondefault R4 VFS test module uses freshly invented %TEMP% files. Held native main, WAL, and SHM FileId128 values are checked against matching paths. It substitutes the WAL name with a different FileId128 decoy, observes refusal, then restores the original name. A sticky test-only refusal prevents reacceptance after this observed ABA.

Expected 323 Rust / 7 Greenfield / 69 inventory / 183 continuity / 373 Vitest / 85/85 Chromium normal and CSP / 19 fictional blobs, not yet qualified.

This is an identity-lifetime test model, NOT integrated in SQLite WAL xOpen; no atomic main/WAL/SHM custody, no protection against unseen ABA between checks, no production writer or real P4 admission, and no recovery.

PRODUCT_FIRST_PARALLEL_SAFETY unchanged; notify before strategy changes. M3.2 IN_PROGRESS_NOT_ACCEPTED, estimated 45% (40–50%). R1–R9 NOT_PROVEN, G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE. Historical PENDING_EXTERNAL_ATTESTATION(21/3/2); prospective NOT_STARTED. glib issue #160 OPEN. No operator data, profile, runtime writer IPC, migration 007, Windows Hello native, backup, journal or recovery.

Qualify exact-HEAD Windows CI, reviews, threads, Protect main strict bypass=[], guarded squash expected_head_sha, independent postmain, and issue #38 append-only. Fixture CI != real admission.
