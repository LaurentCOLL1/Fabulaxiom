# M3.2 — after G2-B1: source-custody route decision (25 October 2026)

**STATUS: SOURCE-ONLY DECISION. NOT AN OPERATOR PROCEDURE. NO G2B ACCEPTANCE, NO G3 AUTHORIZATION.**

## Proven, observed and unknown must stay separate

Live protected starting `main=a33600120f78f20477f4680737e87cb9fabf818b` following [PR #171](https://github.com/LaurentCOLL1/Fabulaxiom/pull/171): exact source `6912ba98ebbd558ac86a5669a497f757df990db2`, [source CI #40166867332](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40166867332) completed/SUCCESS; independent [postmain #40169967245](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40169967245) completed/SUCCESS, **81 Windows steps**, 105 continuity contracts, 96 fictional Vitest, Chromium 82/82 in both modes, 132 Rust. `Protect main` active. The prior source CI #40166775316 failed on an old HEAD (short-prompt historical token), not reusable as a successful qualification.

[Owner-reported G2-B0](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6393215331) found four *.sqlite3 **filenames** in M1.5 and one in M2.5, and no STOP from the exact limited scan. [Owner-reported G2-B1](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6395247470) subsequently reported `ACTIVATION_MARKER_COUNT: 1`, `SELECTOR_KIND: RESTORED`, `SELECTED_FILENAME_MATCH: ONE_OBSERVED`, `OBSERVED_PARTIAL_ONLY`. **These are user reports**, neither an independent attestation nor inspection by CI/assistant. A selected filename is not a continuous file-object identity, authenticated provenance, a v6 schema proof or a reader-safe custody mechanism. B1 read only one tiny activation marker locally; the owner's exact B1 consent was consumed. Do not prompt for repeating B0/B1.

**Current STOP**: `G2B=NOT_ACCEPTED`, `G2B_SOURCE_IDENTITY=PARTIAL_LOCAL_IDENTITY_ONLY`, `SQLITE_WRITER_ABSENCE=NOT_PROVEN`, `G2C=NOT_AUTHORIZED`, `G3_REAL=STOP_UNAVAILABLE`, `M3.2=IN_PROGRESS_NOT_ACCEPTED`, `HISTORICAL=PENDING_EXTERNAL_ATTESTATION(21/3/2)`, `PROSPECTIVE=NOT_STARTED`, PR #35 OPEN/DRAFT; M3.1 isolated v7 and other roles not assessed by B1.

## Decision: stop *metadata accumulation*, qualify a transaction-safe source custody design

| Possible route | Gate prerequisite, missing on protected original | Current verdict |
| --- | --- | --- |
| **A. Already-open trusted SQLite owner + Online Backup into RAM** | Prove a pre-existing, authenticated and non-migrating original-bound owner connection, complete write-channel mediation, revocation/lifetime, checked journal/transaction assumptions, fresh private destination outside originals. No new `Connection::open` to manufacture a trusted owner. | `UNAVAILABLE_NOT_PROVEN` |
| **B. Verifiably cold, quiescent custody** | Independently authenticated exact file/ancestor handles and identity, all writer-channel and replacement exclusion **throughout** a bounded capture, complete WAL/rollback/hot-journal treatment, read without recovery/write side effects, safe new-only target. Metadata-only FileId and FILE_READ_ATTRIBUTES/share flags cannot establish this. | `NOT_PROVEN` |
| **C. Independent *new* prospective synthetic/greenfield development** | A wholly new invented SQLite/Universe/isolated v7 artifact (no original source or protected role claims), full regression test and no released writer IPC / production switch. Any eventual real prospective baseline needs its own separate custody G2–G5 consent and acceptance. | `DEVELOPMENT_ONLY`, not real G2B/G3 |

**Best next engineering task:** audit *source-only* whether any genuinely pre-existing non-migrating owner in the actual Tauri runtime can satisfy Route A. Existing [Tauri owner integration audit](M3_2_G3_TAURI_OWNER_INTEGRATION_AUDIT.md) presently says **none is registered**. Do **not** add an opener, route through `database_status`, `open_database`, `create_backup`, `VACUUM INTO` or startup to fabricate one. Unless that architectural fact materially changes under a separately gated proposal, Route A remains STOP. Route B requires a separate adversarial Windows/SQLite fixture evaluation, with source-bound identity and all writer/journal conditions; another read of process names, file counts or stable hashes is *not* an evidence upgrade. Route C can proceed on invented data while A/B are blocked, without asserting production acceptance.

## Fail-closed discriminators for any future design

1. **Identity/custody:** original vs backup vs rehearsal vs isolated role must be individually authenticated, not inferred from the selected M1.5 filename. A stable `FileIdInfo` is not a historical witness nor immutable content; account for ancestors, rename and ABA across the entire acquisition window.
2. **Writer model:** take account of application commands and *external* SQLite/OS handles, bypass connections, journaling and checkpoints. A single `Get-Process` snapshot or `FILE_READ_ATTRIBUTES` handle using `FILE_SHARE_WRITE` does not exclude writers; prior invented Win32 tests expressly disproved that leap.
3. **Transaction correctness:** WAL `-wal/-shm` and rollback *hot journal* state must be considered. Never delete/checkpoint/recover an original to force an apparent clean result. `mode=ro` may have side effects on WAL metadata; `immutable=1` is not a shortcut for mutable sources. Cross-database atomicity is **not** inferred.
4. **Destination/lifecycle:** use source-consistent backup only with approved bound owner or independent cold proof, new-only private destination, bounded RAM/disk, source postflight, failed/partial backup veto, third-location restore and validation, no overwrite or fallback to raw copy.
5. **Consent:** broad willingness to perform future procedures does not substitute for the exact newly described procedure and its risks, paths, keyboard/UAC/process/effects, privacy and STOP conditions. No current Windows script proposed by this decision; no original should be opened.
6. **Evidence class:** a GitHub/CI pass over fictional bytes is engineering evidence only. Historic five missing independent witnesses in [issue #36](https://github.com/LaurentCOLL1/Fabulaxiom/issues/36) cannot be manufactured. SOLO prospective acceptance is a separate future G5 decision, not already present.

## No automatic escalation

Even if every future **synthetic** Boolean gate were true, it would authorize **design review only**, not real original use. If routes A and B remain unavailable, do not force G2C or G3; continue safe isolated feature development and gather genuine independently pre-existing historical witness material **only if available without unauthorized local source access**.

**Primary references:** [SQLite Online Backup](https://www.sqlite.org/backup.html); [SQLite WAL and checkpoints](https://www.sqlite.org/wal.html); [SQLite rollback/hot journal](https://www.sqlite.org/lockingv3.html); [Microsoft CreateFileW share semantics](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew). Compare prior [FileId writer counterexample](M3_2_G2B_WIN32_FILEID_WRITER_COUNTEREXAMPLE.md) and [G2B→G3 disposition](M3_2_G2B_G3_EVIDENCE_DECISION_AFTER_FILEID.md).
