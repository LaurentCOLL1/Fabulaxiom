# M3.2 / G3 — Tauri owner integration feasibility, source-only audit

**2026-10-17. Decision: `STOP_UNAVAILABLE` for real G3. Design and source tests only.**

Base authority: protected `main=3d6b69cb52e235af06cfea019cb0ec820a6ccaf0`, following the SHA-qualified merge of PR #53. This report extends [the owner-runtime contract](M3_2_G3_OWNER_RUNTIME_CONTRACT.md), rather than replacing its vetoes. No operator data or file handle is opened here.

## Actual, inspected Rust topology

| Entry point | Observed behavior | G3 eligible today? |
| --- | --- | --- |
| `database::database_path` | Resolves app-local path via current activation-path logic | **No:** pathname is not source provenance |
| `database::open_database` | Creates parent directories; `Connection::open`; configures connection; `run_migrations` | **No:** new potentially mutating source open |
| `database_status` | Reuses the above `open_database` | **No:** not a harmless G3 owner lookup |
| `hierarchy_commands::with_connection` | Per-command fresh open through `open_database` | **No:** not persistent or non-migrating |
| `entity_commands::with_connection` | Per-command fresh open through `open_database` | **No** |
| `backup::create_backup` | Reopens source through `open_database`; uses `VACUUM INTO` | **No** |
| `backup::reserve_unique_file` + `vacuum_copy` | `create_new` reservation is dropped, then destination reopened by path | **No:** output continuity not proven |
| `backup::restore_backup` | Opens backup, prepares restored destination and may activate marker | **No:** separate effects and scope |
| Normal and M3.1 Tauri `run()` | `Builder::default().invoke_handler(...)`; no `.manage(...)` or `.setup(...)` source-owner initialization | **No:** no registered authenticated persistent connection |
| Rust `m32_owned_backup_toy` / `m32_owner_lifecycle_toy` | `cfg(test)` AND disabled-by-default feature, `open_in_memory`, serialized toy connection | **Not real:** useful laboratory proof only |

These are code-level observations of the exact baseline, **not statements about what may be running on the operator's host**. The new regression tests deliberately fail if the enumerated integration assumptions change; they are not a parser, formal proof or a runtime/provenance detector. Do not make a future legitimate architectural change just to satisfy an old string assertion: instead perform a new code-and-threat-model review and revise the audit.

## Architecture decision — no manufactured owner

A Tauri `State<Mutex<Owner>>` is technically conceivable for a *future* separately authorized service. However, creating a `Connection` inside `setup`, `manage`, a G3 command, `database_status`, or a migration-capable repository function would **not** make it a pre-existing authenticated owner. The current code never hands an independently authenticated source connection to such a service. Hence **no eligible real source provider exists**.

The boundary for a future implementation should be an injected **move-only source handle**, provisioned by an independent, narrowly authorized custody operation. Its provenance must bind the exact file object and relevant ancestor namespace over the required lifetime; a resolved filename, read-only URI, in-process lease or Boolean declaration does not suffice. No new file opening is authorized by this design. If a secure handoff cannot be established, the acquisition API must remain unavailable.

Conceivable design, **not current code**:

1. **Unprovisioned / STOP:** start with no owner, no file-system scan, no SQLite open, no implicit migration, and no G3 IPC. Ordinary Fabulaxiom behavior remains unchanged.
2. **Future admission under a separate gate:** accept exactly one independently authenticated and *already opened* source. Bind its revocable external custody proof to the handle, namespace and lifetime. Reject absent/expired evidence, concurrent writers with unresolved consistency assumptions, invalid journal state, attach, unexpected schema, pending transaction and insufficient memory quota; never fall back to a pathname open.
3. **Ownership:** move the connection into a non-cloneable owner slot; serialize all access through a synchronous lock or single worker/actor. Never retain a blocking lock across `await`. Do not expose the raw connection from the owner, and do not implement a second `Connection::open` on errors.
4. **Snapshots:** only source-attached, transaction-aware Online Backup into a freshly opened **RAM** destination, with snapshot verification and bounded resources. SQLite consistency is not a cryptographic statement about source identity or permanence of a Windows namespace.
5. **Shutdown:** revoke all issued sessions, reject queued/stale requests, invalidate generations, drain/cancel in-flight requests under an explicit ordering rule, drop the source handle once and enter a terminal state. A poisoned mutex, crashed worker, failed identity check, lost source lease or failed verification must not trigger an automatic reconnect.
6. **Later output, if separately approved:** private never-before-used destination with a genuinely exclusive handle retained across the write; third-location restore and checks before any publication claim. The current `reserve_unique_file` / `VACUUM INTO` sequence is not that output mechanism.

A connection can be moved between threads under Rust ownership constraints; it cannot be shared for unsynchronized simultaneous calls. `Mutex` guards Rust accesses, **not** arbitrary external SQLite writers nor Windows path aliases. SQLite may use journal recovery on opening files, and WAL/SHM sidecars require explicit handling. The previous Windows rename and ABA counterexamples remain live threats.

## Experiment disposition

PR #51 already proved `Backup::new` RAM-to-RAM with a pre-opened invented connection. PR #52 already exercised session/revision, poison, revocation, two-thread serialization and independent snapshots on RAM fixtures. **Do not duplicate those tests merely to inflate test counts.** This PR adds a bounded, deterministic source-only topology audit instead. A new real-ish Tauri state prototype is **not yet justified**: it could falsely imply the missing provenance gate is resolved. A new RAM-only handoff fixture may be considered later if it tests genuinely new lifecycle failure modes; it would still be unavailable to production builds.

### Continuous drift audit

`tools/test_m3_2_g3_tauri_owner_integration_audit.py` checks the inspected public source for the current Tauri registration model, per-command opens, migration path, backup output-release pattern, and test-only toy isolation. It does **not** use the application's APIs, run Fabulaxiom or access the user's protected folders. Windows CI must run the suite from the precise pull-request SHA. A failed assertion means *review the changed architecture*; do not remove the check solely to get green.

### Real remaining blockers / STOP decision

- Independently authenticated and continuously pinned source/ancestor identity: **NOT DEMONSTRATED**.
- Pre-existing non-migrating owner connection for a protected original: **ABSENT FROM INSPECTED RUNTIME**.
- No-write/no-recovery assurance for any future source-open procedure: **NOT DEMONSTRATED**.
- End-to-end writer quiescence, journal/WAL provenance, rename and ABA protection: **NOT DEMONSTRATED**.
- Atomic exclusive output continuity and isolated real restore: **NOT DEMONSTRATED**.
- Separately authorized operator procedure with stop conditions: **NOT GRANTED**.

**Governance remains:** historical `PENDING_EXTERNAL_ATTESTATION (21/3/2)`; prospective `NOT_STARTED`; real G3/G4/G5/G6 `NOT_AUTHORIZED`; PR #35 `OPEN/DRAFT`. No production migration 007, marker switch, writer IPC, original opening, M3.3, release or historical-custody claim. Solo compensating controls are not independent human attestation.

## Authoritative technical references

- SQLite backup: https://www.sqlite.org/backup.html and https://www.sqlite.org/c3ref/backup_finish.html
- SQLite opening / journal recovery: https://www.sqlite.org/c3ref/open.html and https://www.sqlite.org/lockingv3.html
- SQLite WAL rules: https://www.sqlite.org/wal.html
- rusqlite backup: https://docs.rs/rusqlite/0.40.2/rusqlite/backup/struct.Backup.html
- Tauri managed state: https://tauri.app/develop/state-management/
