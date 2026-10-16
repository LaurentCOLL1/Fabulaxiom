# M3.2 G3/G4 — Fully synthetic Windows source → new-only snapshot → isolated restore

**Scope: DISPOSABLE FICTIONAL SQLITE ONLY.** Protected base `e80422922e54195ea48fd27457c895bc08adf699`. PR #46 revealed an actual Windows directory rename can be permitted even when `FILE_SHARE_DELETE` was omitted, and a transient rename/restore might evade boundary checks. The corrected 13/13 fixture tests do not resolve this.

This experiment composes previously individually qualified toy mechanisms:
1. Create an *invented* SQLite database with `schema_migrations` and invented books/facts **in TemporaryDirectory**.
2. Acquire its bytes through a single retained Win32 file HANDLE while comparing a held toy-directory HANDLE identity and pathname at checkpoints. Validate the physical image through `sqlite3.Connection.deserialize` in RAM, including `integrity_check`, `foreign_key_check`, toy migration lineage and toy counts. **No SQLite connection to a preserved operator source.**
3. Create a **new-only** toy custody directory. Output the image via one `os.open(O_CREAT|O_EXCL)` write handle, kept until fsync, without a close-placeholder/reopen-for-write window. Reject preexisting empty/sentinel outputs and directory collisions.
4. Read and validate the disposable snapshot; create a second **new-only** toy directory for the G4 rehearsal and exclusively write the byte image there. Check SHA-256, byte equality and logical toy schema/migrations in RAM.
5. Confirm toy source bytes are unchanged and record that `real_g3_authorized=False`.

**No trust promotion.** This is NOT a proof that physical copying of a live SQLite database is consistent. SQLite on-disk journals/WAL can be part of the logical database state. We reject all observed sidecars and WAL headers but cannot prove no concurrent writer or hot journal race in real operator files. The pinned directory is a temporary toy root only: even in the toy CI, rename may be allowed. Ancestors, ACL inheritance, same-user malicious substitution and transient rename/restore are unproven. The experiment does NOT reserve a real Windows backup destination or create a real privately signed manifest; the toy `O_EXCL` exercise is not a complete Windows custody ceremony.

This CI verifies 16 fixture tests, including both toy versions, directory/file collisions, restoration collision refusal, corrupted output, WAL/journal, FK orphan, wrong migrations, memory cap, and source preservation. The module's CLI accepts **only `--self-test`** and never operator paths or credentials.

Historical `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, real G3/G4/G5/G6 `NOT_AUTHORIZED`, PR #35 OPEN/DRAFT, no migration 007, writer IPC or activation marker changes.

Sources: https://www.sqlite.org/backup.html ; https://www.sqlite.org/fileformat.html ; https://docs.python.org/3.12/library/sqlite3.html ; https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew .
