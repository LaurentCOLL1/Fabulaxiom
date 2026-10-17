# M3.2 G3 — Source provenance and acquisition: no-shortcut decision

**Date: 2026-10-17. Status: `STOP_UNAVAILABLE` for actual original-file G3. Code/design only.**

Starting authority: protected `main=e159b994b2ae09f852416540d3243b3a0d35dec3` after SHA-qualified PR #55, with 11/11 new handoff actor tests and Windows CI #39029700107 completed/success. PR #55 **proved move-only ownership of an invented RAM connection**, not historic Windows file provenance.

## What official interfaces do — and do not — prove

| Proposed shortcut | Documented capability | Why G3 remains blocked |
|---|---|---|
| `sqlite3_db_filename` | Reports the VFS-normalized absolute pathname of a connection's database | A pathname is not a pinned Windows file identity and says nothing about its ancestors or rename/ABA races |
| `sqlite3_file_control(... SQLITE_FCNTL_FILE_POINTER ...)` | Returns a pointer to SQLite's `sqlite3_file` associated with the named database | A `sqlite3_file*` is an internal VFS object, **not** a documented portable Windows `HANDLE`; it does not by itself prove file identity or lifetime |
| rusqlite `unsafe handle/from_handle(_owned)` | Accesses or wraps the SQLite database connection pointer under safety/ownership requirements | The pointer identifies a SQLite connection, not independently authenticated underlying operator bytes; adoption would require a distinct unsafe-code audit |
| Win32 `GetFileInformationByHandleEx(FileIdInfo)` | Supplies metadata about the specific handle being inspected | Does not prove that **that same handle** is the file SQLite currently uses; parent/sidecar provenance still unproven |
| `Connection::open_with_flags(SQLITE_OPEN_READ_ONLY)` or `mode=ro` | Opens a **new** SQLite connection by path | Not a handoff of a preexisting owner; journal/recovery/side-effect questions require a separate operator review |
| `immutable=1` | Promises SQLite that the source never changes and skips locking/change detection | Not an authenticity check; unsafe assumption if an external writer can change the file |
| Current `database::open_database` | Creates parent directories, opens source and runs migrations | Explicitly vetoed for protected G3 |
| RAM actor from PR #55 | Transfers a pre-opened invented `:memory:` SQLite connection between Rust threads | Does not identify or authenticate any operator original |
| Custom SQLite VFS | Conceptually offers a place for coordinated `xOpen` / `sqlite3_file` / sidecar behavior | Possible **research direction only**, not implemented or qualified; custom VFS security, handle ownership, WAL/journal, namespace races and migration must be independently demonstrated |
| Independently attested pre-opened owner | Proposed future acquisition boundary, **absent from current production runtime** | Requires an actual independently verified source/session and separate operator authorization; cannot be manufactured by self-declared boolean claims |

SQLite documentation explicitly says the `sqlite3_db_filename` result is produced by VFS `xFullPathname`. Its `FILE_POINTER` opcode returns `sqlite3_file*`, whereas a VFS owns `xOpen` and other I/O methods. Microsoft documents FileIdInfo *for the handle queried*; it makes no guarantee tying it to a distinct SQLite connection. SQLite warns that `immutable=1` suppresses locking and change detection. These are interface facts, **not** a proof that all authenticated transfer mechanisms are impossible. A new owner could be qualified only under newly approved authority.

## Decision on real sources and next design option

**No existing Fabulaxiom Rust/Tauri path currently supplies both an independently authenticated and continuously pinned original and a preexisting non-migrating SQLite connection to it.** The application migration/backup/status paths are expressly excluded, and the synthetic actor is intentionally unconnected to production.

A genuinely source-bound VFS or an independently provisioned already-open owner remains a **proposal**, not a viable implementation today. Investigate only by a separate design and disposable, invented-file experiment that explicitly covers SQLite's main file, relevant ancestor namespace, WAL/hot-journal, nonmutation/recovery guarantees, writer/quiescence and ownership/close semantics. It must **not** open real originals, alter the active v6 marker, execute migration 007, or activate any writer. The selected strategy could remain impossible under current constraints; then keep `STOP_UNAVAILABLE` and resume isolated fictional M3.2 application work, without forcing G3.

## Deterministic, source-only CI guard

`tools/m3_2_g3_source_identity_boundaries.py` provides a **typed negative-only** list of candidate routes. It has no filesystem or SQLite calls, no operator-provided paths and no decision that can authorize real G3. `tools/test_m3_2_g3_source_identity_boundaries.py` also audits the **public repository Rust source only** for unexpected introduction of raw pointer/VFS/file-control shortcuts, `immutable=1`, G3 IPC or default feature activation. These string-drift checks are deliberately narrow; they are not a full parser, VFS security analysis, file provenance check, or runtime guarantee. A deliberate change should trigger a fresh technical review, not deletion of an inconvenient assertion.

Even with all tests green, real G3/G4/G5/G6 stay `NOT_AUTHORIZED`, historical `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 `OPEN/DRAFT`. No independent human review is claimed. No private Windows paths, hashes, ACLs, keys or database contents may be published.

## Official references

- https://www.sqlite.org/c3ref/db_filename.html
- https://www.sqlite.org/c3ref/file_control.html
- https://www.sqlite.org/vfs.html
- https://www.sqlite.org/uri.html
- https://www.sqlite.org/wal.html
- https://www.sqlite.org/backup.html
- https://docs.rs/rusqlite/0.40.2/rusqlite/struct.Connection.html
- https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-getfileinformationbyhandleex
