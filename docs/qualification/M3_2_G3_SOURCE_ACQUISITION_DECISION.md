# Fabulaxiom M3.2 — G3 source acquisition architecture decision (16 Oct 2026)

**Decision status: SELECTED STRATEGY, NOT EXECUTION AUTHORIZATION.** Protected base `74933c49229ab9efeae5e7c017a61b28525d3fd3`, PR #48 merged after Windows exact-head CI #38962554003 30/30 (11/11 ABA fixture tests). `main` and PR #35 must be re-fetched again before any later mutation. The real active v6 and isolated v7 stay fully outside this development step.

## Source-code audit — current commands are explicitly unsafe as G3 ceremonies

Fresh source review on the exact base showed:
- `src-tauri/src/database.rs::open_database` (around lines 509–520) calls `Connection::open` and then **`run_migrations`**. Its versioning derives from the `schema_migrations` table.
- `src-tauri/src/lib.rs::database_status` (around lines 163–193) invokes `database::open_database`, so even a seemingly observational status command is **not** an acceptable non-migrating entry point for a protected v6.
- `src-tauri/src/backup.rs::create_backup` (around lines 455–463) invokes `database::open_database`, then `vacuum_copy`. This is **not** an already-open owner connection; it opens a new SQLite connection to the active original.
- `vacuum_copy` (around lines 387–396) uses **`VACUUM INTO`**, not the proposed backup-to-RAM transaction flow. `reserve_unique_file` (around lines 399–410) closes the exclusive reservation handle before SQLite reopens the target and uses a separate writable flush open. This creates a close/reopen interval unsuitable as proof against destination substitution.
- `restore_backup` can prepare/migrate a restored copy and finally change the activation marker. It is **not** a G3 read-only audit.

**Decision consequence:** DO NOT invoke `database_status`, `create_database_backup`, `restore_database_backup`, `open_database` or `create_backup` on the protected source for G3. Future work must qualify a **dedicated non-migrating, source-bound owner connection and no-overwrite output mechanism** separately on synthetic data before a new operator-specific approval. The classifier includes a required `dedicated_non_migrating_backup_path` field, which defaults to FALSE; a caller cannot promote a general app backup command into a historical preservation authority.

## Decision: prefer SQLite-owned Online Backup from an EXISTING, trusted connection

An *existing, authenticated and already-open application-owned SQLite source connection* offers the most direct way to avoid a separate path-based source open for G3 while exploiting SQLite's transactional snapshot semantics. It is the **preferred architecture to investigate**, not yet a facility shown to be present or safe in Fabulaxiom. The source connection must be bound to the intended exact original identity through application/runtime provenance, must not require auto-starting the application, reopening the original by a path, invoking a migration, recovering a hot journal, or changing the production activation marker solely to do a backup. If no such source connection currently exists, **the preferred route is UNAVAILABLE**. Application-level source writes caused by ongoing legitimate activity must be examined separately; the user's non-mutation policy remains controlling.

SQLite's [Online Backup API](https://www.sqlite.org/backup.html) produces a transactionally consistent copy of a source database despite concurrent writers, provided its calls complete successfully. It can also replace existing destination contents. Therefore, the candidate plan is: source-to-IN-MEMORY destination via backup API (with explicit capacity safeguards), validate the in-memory SQLite data, serialize to bytes, then publish bytes through a newly and exclusively created destination handle (never opening an existing target for write). A trusted owner connection / checkpoint safety model, serialization behavior and actual memory budget all require separate **synthetic** qualification before any operator command.

## Conditional second route: verifiably quiescent cold image

If there is **no trusted open owner connection**, an offline physical acquisition through a single retained Win32 source handle is only conditionally reviewable if the complete source/ancestor identity and ACLs are authenticated, all writers excluded, rollback/WAL/hot-journal state resolved without modifying originals, and an authentic stable source is established. Existing toy PR #45–48 controls are **insufficient for the real original**. PR #46 originally demonstrated a directory rename can succeed despite missing FILE_SHARE_DELETE; #48 showed a particular configured handle lease refused its rename, and detected transient fake sidecar via directory metadata veto, not a general guarantee.

**Blocked options:** treating `mode=ro` or `immutable=1` as automatically harmless on historical originals; opening the source by an unbound pathname; copying live physical SQLite bytes while another process can write; running the application's normal auto-migrate on the active v6; allowing SQLite backup to overwrite an existing destination; inferring historical 21/3/2 provenance from a fixture or merely matching hashes. No process termination, journal deletion, VACUUM/PRAGMA migration, 007, IPC writer, activation switch or PR #35 merge.

## Exact gates to satisfy before requesting permission for any real G3

1. **Source custody & provenance:** independent, exact original identity is established, with source path and all ancestor substitutions prevented or a stronger handle-binding scheme. Seven worktrees and marker observations are only historical metadata, not continuous active-process proof.
2. **Transaction-aware capture route:** demonstrate the application-owned backup API uses a pre-existing trusted source connection, or prove a fully cold and safe source with journals accounted for. No opening an original just to see if a read-only SQLite URI happens to work.
3. **Negative behavior:** fail-closed on any hot journal/WAL ambiguity, sharing conflict, writer/quiescence uncertainty, source identity change or new-path substitution. Ensure no automatic fallback to a riskier method.
4. **Destination:** reserve a private, never-before-existing directory, atomic new-only file; verify ACL, identity, content SHA-256 and postflight, with no overwrite of an existing backup. The previous Windows G3 destination metadata preflight (191.13 GiB available, fixed NTFS) did **not** test the actual directory creation permission.
5. **Validation & recovery:** migration lineage from `schema_migrations`, `integrity_check`, foreign keys, logical counts and full cold restore to a *third* new location. Never claim cross-DB atomicity across v6 and v7.
6. **Operator permission:** exact source and destination private Windows paths, expected operations, interactions/elevation/key presses/process shutdown and STOP cases must be disclosed and separately approved; no claimed independent reviewer, no real data leaked into CI/GitHub. Until then, **NO real G3**.

## Pure synthetic decision model

`tools/m3_2_g3_source_strategy_policy.py` is a **pure planning model** with no filesystem access, no SQLite connection, no credentials, no operator paths and a CLI accepting **only `--self-test`**. Tests verify that every unknown/missing condition vetoes candidate review. Even a synthetic all-TRUE condition vector returns only `SYNTHETIC_DESIGN_REVIEW_ONLY` with `real_g3_authorized=False`: setting all booleans is NOT evidence.

The current state supplies neither an attested live trusted owner connection nor complete real offline quiescence/ancestor identity. Consequently, the only defensible real-world disposition is **NO_ELIGIBLE_STRATEGY_STOP**; all real G3/G4 remain `NOT_AUTHORIZED`. Historical `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 OPEN/DRAFT, no migration 007 or M3.3.

Primary sources: [SQLite Online Backup API](https://www.sqlite.org/backup.html), [SQLite rollback hot journals](https://www.sqlite.org/lockingv3.html), [SQLite URI mode and immutable warnings](https://www.sqlite.org/uri.html), [Microsoft CreateFileW sharing](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew).
