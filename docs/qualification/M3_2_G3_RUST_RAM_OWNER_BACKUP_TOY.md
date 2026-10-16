# M3.2 G3 — Rust rusqlite Backup from an existing owner, isolated RAM-only unit tests

**Scope: TEST-ONLY, PURE IN-MEMORY FICTIONAL SQLITE; REAL G3 STILL BLOCKED.** Exact GitHub protected base `e1039395fb720b0e7624b066191db7a34984d063`, after [PR #50](https://github.com/LaurentCOLL1/Fabulaxiom/pull/50) merged with terminal Windows CI #38974991843 **32/32 PASS, 23/23 Python toy transactional backup tests**.

## Feature isolation

`src-tauri/Cargo.toml` adds `m32-g3-owned-ram-toy = ["rusqlite/backup"]`, **NOT part of default features**. `lib.rs` includes `m32_owned_backup_toy` only under `cfg(all(test, feature = "m32-g3-owned-ram-toy"))`, and has a **compile_error** if this feature is enabled in a non-test library. No Tauri command, no `AppHandle`, runtime backing file, REST API, updater, migration or activation code is touched. No new crate dependency: rust `rusqlite 0.40.2` documents feature `backup = []`, so the existing locked graph should remain compatible, to be verified by Windows CI with `--locked`.

## New test contract

`invented_owner(6|7)` builds the entire **imaginary** schema in `Connection::open_in_memory()` and inserts toy books, facts and a toy `schema_migrations` table. `backup_preopened_ram_owner(&source, &mut dest, version, max_bytes)` accepts **only existing Connection references**; it does not accept or open any filesystem path. It rejects attached DBs, non-memory source/destination, open owner transactions, unexpected migration versions, nonempty output databases, FK or integrity failures, and a toy 2 MiB page-size budget.

`Backup::new(source, &mut dest)` calls SQLite's [Online Backup API](https://sqlite.org/backup.html) in bounded page steps, without reopening the source, and the output is verified as a **logically consistent independent RAM snapshot**. Source writes after finishing do not alter the captured RAM copy. Tests run with:
`cargo test --locked --features m32-g3-owned-ram-toy --lib m32_owned_backup_toy -- --nocapture`
on the Windows CI runner; the baseline `cargo test --all-targets --locked` and `cargo check --locked` must also pass.

These **13** focused Rust tests are deliberately not evidence of real source provenance, historical file custody, WAL behavior under actual Win32 contention, on-disk serialization, third-location recovery or safe Tauri connection lifecycle. Python PR #50 already separately qualified transactional WAL and toy no-overwrite disk scenarios. Rust remains a distinct **memory-only feasibility test**, not a combined production implementation.

**Do not invoke `database::open_database`, `database_status`, `backup::create_backup` or `restore_backup` on the protected originals for G3.** Current commands can run migrations and make target mutations, while the current app lacks a demonstrated durable non-migrating owner handle. No real G3, G4/G5/G6 or PR #35 merge. `historical=PENDING_EXTERNAL_ATTESTATION(21/3/2)`, `prospective=NOT_STARTED`, no migration 007, activation change, writer IPC or M3.3.

Primary APIs: https://docs.rs/rusqlite/0.40.2/rusqlite/backup/struct.Backup.html , https://docs.rs/crate/rusqlite/0.40.2/source/Cargo.toml.orig , https://www.sqlite.org/backup.html .
