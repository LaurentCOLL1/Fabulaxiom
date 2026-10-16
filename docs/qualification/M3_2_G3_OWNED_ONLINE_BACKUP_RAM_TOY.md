# M3.2 G3 — Existing-owner SQLite Online Backup → RAM → sealed toy restore

**Status: SYNTHETIC LAB ONLY / NOT A G3 CUSTODY AUTHORIZATION.** Starting protected `main=aaa8550dacfc88ac3f335598f66dd2928709e35e` after PR #49 (31/31 Windows CI, 24/24 policy refusal tests). This PR adds no Rust or Tauri application commands, no private paths or production code. An internal Python context manager generates *invented* v6/v7 schemas under `TemporaryDirectory` and opens its owner SQLite connection **before the backup function** is called.

## Qualified candidate under test

1. `invented_toy_owner(version)` creates a fresh fictional database and yields a **pre-existing** Python `sqlite3.Connection`. No protected operator source can be specified via CLI (only `--self-test`). The toy source is in `TemporaryDirectory`; its synthetic issuance stamp is **not** genuine provenance for real files.
2. `backup_owner_to_ram(owner)` inspects the existing connection's toy `PRAGMA database_list`, refuses attachments, an open owner transaction and an inadequate memory budget; it uses **only** `owner.connection.backup(sqlite3.connect(":memory:"))` to take a transactionally coherent SQLite snapshot. It never calls `sqlite3.connect(source_path)` during acquisition, `database::open_database`, `run_migrations` or production `VACUUM INTO`.
3. Validates `PRAGMA integrity_check`, `foreign_key_check`, deterministic toy migrations and counts **on RAM** before serialization. If a WAL source's backup yields a WAL-marked RAM serialization, tests a `VACUUM` **on the RAM destination only** to produce a standalone rollback-style SQLite image. This deliberately changes the page layout; it is **logical equivalence, NOT original-source bit identity**. Revalidate the serialized image in a separate RAM connection. Memory policy is a hard **2 MiB toy cap** and does not establish a safe real-world budget.
4. Create the toy backup and toy third-location restoration with previously qualified `_new_dir`, `_exclusive_write_once`, `restore_toy` — **new-only** folders and file handles, no overwrite of existing sentinels. Verify byte SHA-256/contents and migrations of both copies.
5. Test WAL committed/uncommitted writers, source snapshot stability after a later commit, missing migration, FK corruption, closed or replaced owner connection, destination collisions and no data overwrite. In a real application the exact existing owner connection, thread safety, lifecycle, journal behavior, cross-database consistency, permissions and independent identity must be established separately.

## Safety and scope

The test is **not** a tool to back up the user environment. Paths are generated internally, no command accepts a real path, no original SQLite files are opened, no activation markers/worktrees/backup custody touched. Python's owner object can never certify the identity of an operator's historical database. A live SQLite Online Backup is a coherent snapshot, not proof that the chosen connection points to the intended historic source or that no other application's writes are legitimate.

Do not reuse `database_status`, `open_database` or `backup::create_backup` on the protected v6/v7: current Rust implementation opens the file and runs automatic migrations, and app backup uses `VACUUM INTO` with a close/reopen destination gap. Even if all toy tests succeed, `real_g3_authorized=False`, `prospective=NOT_STARTED`, historical `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, G3–G6 `NOT_AUTHORIZED`; PR #35 stays open/draft, no production migration 007/marker/IPC writer/M3.3.

Future work: independent source owner-connection feasibility study for Fabulaxiom Tauri/Rust using code-only evidence, then separate operator consent for any original reads. Refuse, rather than re-open an original to manufacture a connection, if a trusted owner is unavailable.

References: https://www.sqlite.org/backup.html ; https://docs.python.org/3.12/library/sqlite3.html ; https://www.sqlite.org/fileformat.html ; https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew .
