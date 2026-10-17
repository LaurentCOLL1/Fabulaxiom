# M3.2 G3 — Test-only Rust RAM owner handoff actor

**Status: PROPOSED SYNTHETIC QUALIFICATION. Real G3 remains STOP_UNAVAILABLE / NOT_AUTHORIZED.**

Starting protected base: `main=8cbb8671194afee48d96194aae7863ddd46e9b3d` after PR #54. The [code-only Tauri feasibility audit](M3_2_G3_TAURI_OWNER_INTEGRATION_AUDIT.md) confirms no authenticated, durable non-migrating source is available in normal runtime. This new test fixture explores a *different* technical property: moving ownership of a **pre-opened invented RAM connection** across a Rust thread boundary and relinquishing it irreversibly. It does **not** implement authentication, Tauri State or production G3.

## Precisely scoped experiment

`src-tauri/src/m32_owner_handoff_actor_toy.rs` is reachable **only** under `cfg(test)` plus the already-disabled-by-default `m32-g3-owned-ram-toy` Cargo feature. Normal binary compilation of this feature remains explicitly rejected by `compile_error!`. The fictional `InventedSource` constructor only calls `Connection::open_in_memory`. A single, uncloneable source connection is validated for purely invented migrations 1–6/7, integral RAM schema, limited pages, no transaction, no additional `ATTACH` and FK/integrity checks. It then **moves** to a dedicated `std::thread`.

A bounded synchronous channel carries requests; clients may clone the sender but never the source. A single worker executes `Backup::new(&source, &mut destination)` with a **new RAM destination**, returns only an invented test value and never hands out the raw `Connection`. There are no `std::fs`, path parameters, `Connection::open(path)`, Tauri registration, network calls, operator documents, actual database bytes, activation marker or production migrations.

## New failure modes and tests versus PR #51/#52

Earlier tests already proved backup, `Mutex` serialisation and toy session revocation. This actor adds **eleven** narrow Rust tests for a different boundary: ownership moved into a separate worker, pre-admission transaction veto, foreign `ATTACH` veto, foreign-key orphan veto, schema gap veto, invalid version, bad ticket without harming valid ticket, multiple independent producers/one SQLite owner, terminal revocation, terminal simulated poisoning, and shutdown with stale client senders. There is no claim that a session token is a cryptographic or Win32 identity.

The worker drops the source on revoke, poison or stop, and does not include any reconnect/open branch. A poisoned actor refuses remaining snapshot attempts; even after a successful RAM snapshot, nothing about an original Windows database's provenance or exclusive writer control has been shown.

## Trust gap and architectural decision

Rust can move a `Send` (but not `Sync`) `rusqlite::Connection` into a worker. Tauri `State` or an actor can serialize access, but neither can **produce an independently authenticated original**. The current application's open paths call migrations and would violate the no-new-opening/no-mutation source-custody gate. `Connection::open_in_memory()` intentionally provides zero evidence about any actual operator original.

A real future handoff would need, **before creating this actor in production**: externally established file/ancestor identity and provenance, an operator-authorized source-open or bona fide preexisting source handle, continuous revocation/lifetime, validated journal/WAL and writer assumptions, no source mutations, bounded snapshot, sealed new-only output, separate restore and a second consent boundary. No such authority is granted. It might be impossible to achieve under current constraints; in that case retain `STOP_UNAVAILABLE` rather than making the admission predicate weaker.

### CI acceptance

The isolated Windows `pull_request` job must run `cargo test --locked --features m32-g3-owned-ram-toy --lib m32_owner_handoff_actor_toy -- --nocapture` on the **exact PR HEAD**, report all eleven new tests green and preserve normal Rust and existing G3 tests. Any HEAD change invalidates prior checks. Review the six-file diff and branch protections before fusion.

**Governance unchanged:** historical `PENDING_EXTERNAL_ATTESTATION(21/3/2)`; prospective `NOT_STARTED`; real G3/G4/G5/G6 `NOT_AUTHORIZED`; PR #35 `OPEN/DRAFT`; no 007 production, activation, writer IPC, M3.3 or release. No independent human signoff claimed.

## Official references

- https://docs.rs/rusqlite/0.40.2/rusqlite/struct.Connection.html
- https://docs.rs/rusqlite/0.40.2/rusqlite/backup/struct.Backup.html
- https://www.sqlite.org/c3ref/backup_finish.html
- https://tauri.app/develop/state-management/
