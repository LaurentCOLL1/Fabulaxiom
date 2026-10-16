# M3.2 G3 — Win32 source read-lease qualification (toy SQLite ONLY)

**DRAFT / SYNTHETIC-ONLY / NOT A REAL G3 BACKUP.** Exact predecessor: G3 exclusive-stream synthetic PR #42 merged at main cac59154d9e5628e9ab8411bbd8d896d164dedd6, Windows CI #38914716036 25/25 PASS. Operator preflights G2-A/B/C and corrected physical-header G2-D (3x SQLite ROLLBACK with 4096-byte pages and user_version 0) were supplied as local output. Operator G3 destination preflight confirmed fixed NTFS, ~191.13 GiB free and intended destination absent **at observation time**. None of these checks proves actual SQLite integrity, writer-quiescence or permission to create a real snapshot.

## Motivation and technical controls under test

SQLite's [rollback/hot-journal rules](https://www.sqlite.org/lockingv3.html) describe a potentially **writing recovery operation even before a read** if a database has a hot journal. The absence of a sidecar during an earlier observation does not by itself certify a future open. The read-only URI option does not settle every possible file-system side effect.

This tool **generates disposable invented SQLite tables** only under a new temporary root and never accepts an external database source path on its CLI. Tests exercise:

- Strict fixture basename/root, symlink/reparse rejection for toy path, sidecar screening for \`-wal\`, \`-shm\`, \`-journal\`, and rollback-mode 100-byte header screening (WAL header bytes rejected even without sidecars).
- Windows \`CreateFileW(GENERIC_READ, FILE_SHARE_READ, OPEN_EXISTING, FILE_FLAG_OPEN_REPARSE_POINT)\` handle, held throughout a toy SQLite \`mode=ro\` and \`PRAGMA query_only=ON\` audit. Reader tests assert that a second Win32 GENERIC_WRITE open receives \`ERROR_SHARING_VIOLATION\`, and that an existing writer blocks the proposed lease.
- Toy-only SQLite \`PRAGMA integrity_check\`, \`foreign_key_check\`, real fixture \`schema_migrations\` (six toy rows, **not** header \`user_version\`), and before/after byte digest + length/time comparison.
- Adversarial fixtures for sidecar sentinels, WAL header, malformed magic, wrong basename/root, nonexistent file, and source symlink.

## Non-proven barriers / STOP for operator data

**This is not a safe general-purpose operator-source reader.** The OS source handle share-mode constrains cooperating kernel file opens but does NOT prove that ancestor directories and reparse points cannot be swapped between checks and path-based SQLite open, or that arbitrary third-party writers and device/filter drivers cannot affect bytes. It does not hold all parent directory handles, validate a stable file ID against SQLite's internal handle, or prove absence of hot journals created during a race. The resulting toy evidence cannot be treated as verified independent custody or a source-safe-open certificate for a preserved v6/v7 original.

Some operating systems or SQLite VFS configurations may refuse the source read-only open under this lease; that outcome is a **valid fail-closed compatibility result**, not a reason to reopen without the lease, change ACL, remove journals or use \`immutable=1\` on a mutable source.

**No operator path or identifier, protected SQLite, original ACL/backup/marker, migration 007, IPC writer, seven worktrees or novel content was used by these tests.** CLI is \`--self-test\` only. No changes to production code.

## Gate disposition

If Windows CI succeeds on the PR's **exact head**, the only conclusion is **WIN32_LEASE_TOY_QUALIFIED**. Real G3 stays \`NOT_AUTHORIZED\`; prospective \`NOT_STARTED\`; historic custody \`PENDING_EXTERNAL_ATTESTATION 21/3/2\`; PR #35 remains OPEN/DRAFT. Before any actual G3, design a stable directory/file-ID source open and Windows no-overwrite destination, qualify real schema/ram budget on separate allowed copies, and obtain an exact operator authorization for creating **new** outputs only. No automatic import of this module into application/runtime.

References: [SQLite hot journals](https://www.sqlite.org/lockingv3.html), [SQLite file format](https://sqlite.org/fileformat.html), [Microsoft CreateFileW](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew), [Microsoft reparse behavior](https://learn.microsoft.com/en-us/windows/win32/fileio/reparse-points-and-file-operations).
