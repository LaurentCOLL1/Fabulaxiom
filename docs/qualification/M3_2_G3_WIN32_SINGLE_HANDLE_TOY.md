# Fabulaxiom M3.2 — G3 Win32 single-source-handle physical read + SQLite RAM deserialize

**DRAFT / TOY-ONLY / NOT AUTHORIZED FOR ACTUAL OPERATOR DATA.** This PR is a new technical experiment from protected main \`7173b6dddaa9d783533475af72fad41ab7efd25b\`. Prior PRs #42 and #43 passed exact-head Windows CI only for fictional sources, NOT real data.

## Narrow test hypothesis

On an isolated Windows fixture, open a **single** source handle through \`CreateFileW(GENERIC_READ, FILE_SHARE_READ, OPEN_EXISTING, FILE_FLAG_OPEN_REPARSE_POINT)\`, read all physical SQLite bytes exclusively via \`ReadFile\` on **that same handle**, compare \`GetFileInformationByHandle\` identity before/after, and validate the captured **bytes in memory** using Python \`sqlite3.Connection.deserialize()\`. Unlike PR #43, no \`sqlite3.connect(real_source_path)\` or other SQLite source-path reopen occurs at any stage of source inspection; \`sqlite3.connect(':memory:')\` is used only after bytes are captured. The only source SQL connections in this file are in the **fixture constructor** which invents a toy database.

The unit tests cover invented migration versions 6 and 7; file-ID stability on a retained handle; existing/new writer conflicts; sidecar WAL/journal sentinels; a WAL header even without sidecars; wrong \`schema_migrations\` value; memory cap; invalid SQLite magic; foreign-key orphan; rejected symlinks, missing and unexpected toy files. All temporary files are disposable. CLI has **only \`--self-test\`**, no operator path support.

## Non-demonstrated guarantees

- This fixture does not qualify an untrusted ancestor or network path, names changed by a same-user adversary, hardlink/file system filter behavior, alternate streams, time-of-check/use between parent checks and handle open, or cross-directory reparse. The held file ID proves which file its own \`ReadFile\` consumed, not that this file was **the intended historic operator source**. Windows volume/file-index can be reused after close and does not establish independent custody. The fixture tests no robust ACL pinning.
- Single-handle physical bytes from a **live** SQLite source may still be inconsistent even with an observed ROLLBACK header and absent sidecars. Hot journals, existing shared handles, concurrent writes and unresolved filesystem snapshots remain blockers. It does not replace SQLite Online Backup API for genuine concurrency-safe snapshots.
- SQLite's \`deserialize\` verifies only that the supplied bytes can be interpreted/queried; logical integrity and foreign keys must still be tested and cannot establish historical provenance.
- Memory consumption is bounded here by a **toy-only 2 MiB cap**. The real 237568/311296 byte observations do not establish a production limit or rule out growth, corrupted pages, transient writers or more complex database shapes.
- The current code **does not write a destination**, grant G3 production access, authenticate a private manifest, restore to a third location, merge PR #35 or advance to M3.3. Protected actual v6/v7 files/ACLs/markers/worktrees have not been touched. No migration 007 or IPC writer.

## Next gates

Require exact-source terminal Windows pull_request CI on this new HEAD. Then separately design and qualify parent-directory identity and origin-to-file-ID binding on **toy adversarial paths**, complete no-overwrite G3 destination design and private evidence scheme, and request a separate operator approval for any actual G3 observation/write. Historical \`PENDING_EXTERNAL_ATTESTATION 21/3/2\` and prospective \`NOT_STARTED\` remain.

References: https://www.sqlite.org/lockingv3.html ; https://www.sqlite.org/fileformat.html ; https://docs.python.org/3.12/library/sqlite3.html ; https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-getfileinformationbyhandle ; https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew .
