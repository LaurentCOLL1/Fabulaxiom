# M3.2 — G2-B Win32 FileId metadata: synthetic writer counterexample (22 October 2026)

**SOURCE-ONLY / FICTIONAL GITHUB CI / NO OPERATOR DB PATHS.** This experiment tests a narrow logical gap after owner-reported G2-B checks. It is **not** a G2-B final PASS, historical attestation, or G2-C / G3 authorization.

## Observation and why it is insufficient

The operator reported four separately bounded PowerShell checks: one restored v6 *candidate* and one M1.5 activation marker; that marker matched the candidate name; isolated v7 filename present; no `-wal/-shm/-journal` names observed beside the two selected files; size, creation/modified timestamps stable across two reads on fixed NTFS; ancestor and three-file FileIdInfo stable across two `FILE_READ_ATTRIBUTES, FILE_SHARE_READ|FILE_SHARE_WRITE|FILE_SHARE_DELETE` openings. This is **owner-supplied sanitized output**, never an independent attestation and never proof that the schemas are v6/v7. No secrets, paths, file IDs or hashes belong in GitHub.

The exact sharing flags in the user-reported script permit a separate handle requesting `GENERIC_WRITE`. A stable FileId on the original metadata handle can coexist with mutated bytes of the *same synthetic file*. This is the point of the new adversarial regression; positive FileId stability is **not** writer exclusion.

## Exact bounded regression

`tools/test_m32_g2b_fileid_writer_counterexample.py` contains **8 tests**, of which four are pure-data refusal checks and four use freshly invented ordinary **non-SQLite** bytes under a disposable `TemporaryDirectory`, **only when Windows GitHub Actions** runs them. They cannot be supplied an operator path, do not call SQLite, do not enumerate app-data or production, do not inspect marker contents, and do not create persistent evidence files. CI disposes of each toy fixture.

The Windows tests check: (1) a `FILE_READ_ATTRIBUTES, SHARE_ALL` monitoring handle allows a second `GENERIC_WRITE` open, (2) synthetic bytes are replaced while the retained monitor's volume + FileId remains identical, (3) an existing writer is compatible with the metadata monitor, and (4) a separate experimental `SHARE_READ` handle blocks a fresh writer open on this toy. **This last experiment does not prove that SQLite hot journals, prior writers, alternate identities or real protected ancestors are safe.** A pure denial verdict remains `NOT_PROVEN`, `NOT_AUTHORIZED` or `STOP_UNAVAILABLE` even if every fictional input flag is true.

## Boundaries and next gates

- **Real source identity:** only `PARTIAL_LOCAL_IDENTITY_ONLY` from owner-reported checks. File IDs are local identity observations, not historical provenance, immutable content or a guarantee of no further writes.
- **No source-access promotion:** no production v6, isolated v7, backups, ACL exports, activation marker, sidecars, seven worktrees, SQL, Tauri IPC, migration 007, release or ComfyUI touched.
- **Decision:** G2B partial metadata observation only; `SQLITE_WRITER_ABSENCE=NOT_PROVEN`; `G2C=NOT_AUTHORIZED`; `G3_REAL=STOP_UNAVAILABLE`; `M3.2=IN_PROGRESS_NOT_ACCEPTED`; historic `PENDING_EXTERNAL_ATTESTATION(21/3/2)`; prospective `NOT_STARTED`; PR #35 remains DRAFT.
- **Next technical prerequisite:** define a separate source-bound and transaction-aware custody route with explicit operator review; ordinary filesystem share tests cannot substitute for verified quiescence or SQLite Online Backup API guarantees.

Authoritative technical references: [Microsoft CreateFileW sharing flags](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew), [Windows file-open compatibility](https://learn.microsoft.com/en-us/windows/win32/fileio/creating-and-opening-files), [SQLite backup API](https://www.sqlite.org/backup.html), [SQLite WAL](https://www.sqlite.org/wal.html).
