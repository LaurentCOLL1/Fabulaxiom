# M3.2 G3 — In-memory Rust owner lifecycle and fail-closed leases

**EXPERIMENT ONLY, NO REAL SOURCE AUTHORITY.** Protected base `d01c7a55b6b7abb7db6228d4d266da03610df9f7`; prior [PR #51](https://github.com/LaurentCOLL1/Fabulaxiom/pull/51) passed 33/33 Windows CI and 13/13 Rust owner-to-RAM tests.

The new `m32_owner_lifecycle_toy.rs` is compiled **only** under the existing `cfg(all(test, feature="m32-g3-owned-ram-toy"))` guard, and the feature cannot compile into normal application binaries due to the existing non-test `compile_error!`. No Tauri command, runtime `State`, connection file path, production DB open/migrate, or backup output is created. It has **16 tests**, all invented in-memory SQLite schemas via `Connection::open_in_memory` and independent in-memory copies via `Backup::new`.

## Lifecycle contract and limits

An `OwnerSlot` owns a **single pre-opened** synthetic SQLite source in `Option<Connection>`. Its `ToyLease` is an in-process fixture session/revision marker, **not a cryptographic identity, Windows file ID, or proof of actual source custody**. Mutable capture requires a current lease; a write through the slot increments the revision and invalidates old leases. Revocation consumes the owner and permanently prevents new backup; a failed snapshot after acquisition poisons the owner rather than silently retrying. The RAM destination is never exposed until backup completes and passes `integrity_check`, `foreign_key_check`, toy `schema_migrations`, and count/budget checks. The toy memory limit is 2 MiB.

An `Arc<Mutex<OwnerSlot>>` test demonstrates sequential access from two Rust threads using the **same session-owned connection**. Another test intentionally poisons the test mutex and verifies failure instead of an implicit recovery. No async lock is held across `await` (the experiment has no async functions). `Connection` is `Send` but not `Sync` in `rusqlite` 0.40.2; Tauri state normally requires `Send+Sync`. This demonstrates a synchronization option, NOT safety of a production long-running Tauri connection, UI/command integration, source provenance or error-recovery protocol.

## Explicit remaining STOPs

- Current application hierarchy/entity/status/backup routines open a fresh migration-capable source each call; they are not a pre-existing owner service. No production lifetime change was made.
- Concurrent writes by independent SQLite connections, WAL and hot journals on actual Windows paths, ACL/ancestor identity, and a real output directory remain **unproven**.
- A toy lease can never authenticate protected v6/v7; do not construct a new owner connection by opening the originals. The original PR #46/48 namespace findings remain relevant.
- No historical 21/3/2 custody promotion, real G3/G4, PR #35 merge, migration 007, activation switch, writer IPC or M3.3.

**Next**: Use these tests to write a no-I/O feasibility specification for a dedicated production service (per-owner lifecycle, provenance, fail-closed revocation and thread-bound access) with separate user authorization prior to any real data operation. Prefer implementation isolation over modifying normal Tauri commands.

Sources: https://docs.rs/rusqlite/0.40.2/rusqlite/struct.OpenFlags.html ; https://www.sqlite.org/c3ref/backup_finish.html ; https://docs.rs/tauri/2/tauri/struct.Builder.html .
