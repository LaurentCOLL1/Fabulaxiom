# M3.2 G3 — Sealed in-memory SQLite snapshot to exclusive stream (synthetic only)

**Status: PROTOTYPE / SYNTHETIC-ONLY / NOT AUTHORIZED FOR OPERATOR DATA.** The operator's real Windows destination-only preflight reported medium integrity PASS, fixed NTFS PASS, 191.13 GiB free, no examined-parent reparse, readable parent ACL, target directory absent. This is **not** proof of exclusive creation, source access safety, database integrity, or successful real capture.

## Why this experiment

The previous synthetic laboratory calls `os.open(...O_EXCL)` to reserve `snapshot.sqlite`, closes that handle, and then lets `sqlite3.connect()` reopen the target. **That leaves a create-to-reopen substitution window**. The real SQLite Online Backup API can overwrite a preexisting destination, as documented at https://www.sqlite.org/backup.html. Do not treat the earlier 24/24 CI as an end-to-end exclusive file safety proof.

This experiment uses **fresh fictitious toy databases only**, created internally in a `TemporaryDirectory`. It backs up the toy source to an in-memory SQLite connection using `Connection.backup()`, validates in-memory integrity/FK, obtains a serialized image, then writes the image in **one continuous write-capable `os.open(O_CREAT|O_EXCL)` file descriptor**. It never closes an exclusive placeholder then reopens it for SQLite writing. A new-only fixture subdirectory is created; colliding file/dir names, empty preexisting files, sentinel-filled files, incorrect names/images, memory budget, missing folder, and symlinked output folder are tested with fail-closed behavior. Python CLI accepts **only** `--self-test`, never operator paths.

## Boundaries not proven / required before any real backup

1. The toy schema and its `schema_migrations` are **not** the Fabulaxiom production schema. This fixture correctly demonstrates `PRAGMA user_version=0` with application migration version 6.
2. In-memory serialization has a memory cost; this toy uses a 1 MiB **fixture-only** cap. Actual capacity, SQLite compile flags, API version and application database schema are **not** qualified.
3. Windows per-directory identity/ACL inheritance, open-handle identity controls, atomic no-reparse semantics and protections against an adversarial same-user process remain **not proven**. Reopening for read and checking `st_ino` is diagnostic, not a security guarantee against replacement.
4. The toy read-only SQLite source connection **cannot** be used on preserved operator data. Actual rollback-mode source-safe opening, hot journal, concurrent writers and WAL handling have not been qualified. The operator's G2-D header-only ROLLBACK PASS on three sources does **not** eliminate the open-source risk.
5. No real source, private path, user ID, story, history, ACL, marker, archive or protected worktree is embedded, read or written by CI.
6. There is no proof of a global atomic snapshot across two independent SQLite databases. No source is migrated. No protected activation marker is touched. No existing backup or historical evidence is promoted.

## Next controlled work

After exact-head Windows CI PASS and code review, consider a **separate** production design for source-safe-open + Windows sealed destination identity, and only then a separately reviewed operator G3 execution block (paths, allowed new outputs, credential/UAC/process/keyboard interactions and STOP cases). A synthetic test PASS is **not** permission to execute on real files.

States: `historical=PENDING_EXTERNAL_ATTESTATION(21/3/2)`; `prospective=NOT_STARTED`; `real_G3=NOT_AUTHORIZED`; `PR35=OPEN/DRAFT`. No normal production migration 007, writer IPC, marker switch, merge of #35 or M3.3.

Sources: https://www.sqlite.org/backup.html ; https://www.sqlite.org/c3ref/backup_finish.html ; https://learn.microsoft.com/en-us/windows/desktop/FileIO/creating-and-opening-files .
