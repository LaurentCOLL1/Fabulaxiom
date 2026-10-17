# M3.2 G3 — Non-migrating owner-service boundary: CODE-ONLY architecture decision

**Status: architecture feasibility, NOT implementation or operator authorization.**
Protected starting main `fd2149131c61ef94180de28c6144e18a5c76deb5` (PR #52 merged with terminal Windows CI #39001917362, 34/34 steps PASS including 18/18 RAM-only Rust lifecycle tests). This artifact documents what must be different before a future long-lived SQLite owner could be used in Fabulaxiom. It does not create such a service.

## Verified current Rust entry points and the missing trust boundary

The current `database::open_database` calls `run_migrations`; `database_status` uses the same routine. `hierarchy_commands` and `entity_commands` open a fresh connection for each operation; they do not prove any persistent owner is available. `backup::create_backup` opens the source through `database::open_database` and uses `VACUUM INTO`; an exclusive output reservation is closed before a later path open. `restore_backup` may ultimately switch the activation marker. **These entry points are not a non-migrating G3 ceremony and must never be run on the protected originals to create one.**

The default Tauri runtime currently has **no authenticated pre-existing, long-lived, non-migrating SQLite owner** demonstrated by the inspected code. An `Arc<Mutex<Connection>>` proof using invented RAM data (PR #52) proves serialization at that scale, not original identity, Win32 namespace invariance, or zero disk-side effects.

## Candidate service boundary — specification only

1. **Session provenance:** issue a source identity only from an independently verified custody ceremony. A filename, environment variable, path equality, hash supplied without trusted custody, or in-memory session token is NOT enough. Bind session identity to the exact original and its parent namespace, with an explicit revocation rule. A future service must refuse to create a session if source provenance is unavailable.
2. **Acquisition:** a trusted, already-open owner connection may be *injected* under explicit authorization. **No automatic creation** by calling current `open_database`, `database_status`, the existing backup command, or even a new `mode=ro` URI on protected originals. Any future new source opening is a distinct proposal needing a disclosed operator procedure and scrutiny for SQLite recovery/write effects.
3. **Lifecycle and isolation:** one source-owner instance, no cloning raw connection handles, serialized access and no lock across async awaits. Session revision invalidates stale requests; irreversible stop/revoke on mismatch, thread-lock poison, resource-cap breach or bad logical content. An already-completed snapshot remains independent.
4. **Snapshot:** only a transaction-aware SQLite Online Backup API on the **pre-established source connection**. Refuse an owner with a pending write transaction. Validate logical `schema_migrations`, integrity, foreign keys and data; set a realistic resource quota first. Online Backup is coherent, but does not prove that the source connection is the right historical file.
5. **Custody output:** private new-only directory and exclusive file handle; source and destination identities verified without pathname-race windows; no close-placeholder/reopen-for-write. One third-location isolated restore must pass exact image digest and migration/data checks before any later G4/G5 consideration.
6. **Approval:** do not emit or infer a real G3 authorization from a boolean vector. Require a new operator-specific procedure with paths redacted from public GitHub, explicit STOP actions and a fresh consent boundary. No independent human reviewer is available, so automated tests must be accurately described as machine evidence, not independent sign-off.

**If no authenticated existing owner is found, the owner-backup route is unavailable.** The conditional cold-custody alternative is a separate route: all writers quiescent, authentic full ancestor/file identity, WAL/hot-journal accounted for, and a no-mutation copy+restore procedure independently approved. Previous Win32 PR #46 and #48 demonstrated that endpoint-only path checking cannot be trusted as a universal invariant.

## Enforced source-code review and synthetic policy

`tools/m3_2_g3_owner_runtime_contract.py` is a **pure-data refusal policy**. No SQLite/Windows/Tauri call, file path or credentials. Even *all synthetic claims true* yield `HYPOTHETICAL_REVIEW_ONLY` and `real_g3_authorized=False`. Companion tests read only the public **repository Rust source code** to assert current migration/copy behavior and test-feature quarantine; they do **not** inspect any user runtime path. These source inspection assertions must be revised if and only if runtime architecture is deliberately changed with fresh audit.

**Governance:** historical `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, real G3–G6 `NOT_AUTHORIZED`, PR #35 OPEN/DRAFT, no production migration 007, activation marker, writer IPC, or M3.3.

**Next permissible work:** review this contract against a concrete future Rust service design and produce a dry-run **with no actual original connection**. A separate operator decision is needed before any new source opening or real custody file operation.

Sources: https://www.sqlite.org/backup.html ; https://www.sqlite.org/c3ref/backup_finish.html ; https://docs.rs/rusqlite/0.40.2/rusqlite/backup/struct.Backup.html .
