# M3.2 — G3 invented shared-RAM foreign-writer counterexample (25 October 2026)

**TYPE:** runnable Rust **TEST-ONLY**, in-memory and invented values only. **NOT** an operator Windows command, production database reader, custodial witness, G2B acceptance, or real G3 authorization.

## Why this regression adds a new technical fact

After PR #172 [source #40178558404](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40178558404), protected [main=51e4264b463f60bd8186d09a8ac306315b39d79d](https://github.com/LaurentCOLL1/Fabulaxiom/commit/51e4264b463f60bd8186d09a8ac306315b39d79d) and [postmain #40179336243](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40179336243), both SUCCESS on their **own exact SHAs** (81 Windows steps, 106 handoff contracts, 96 fictional Vitest, Chromium 82/82 each mode, 132 Rust), the source-custody routes remain A `UNAVAILABLE_NOT_PROVEN` and B `NOT_PROVEN`. No original access or Windows operator procedure.

The already-existing `src-tauri/src/m32_preopened_query_only_toy.rs` tests prove that `PRAGMA query_only=ON` rejects writes attempted **through the same connection**, and that checking `total_changes()` can notice writes through that connection. **This does not exclude a different writer connection to the same database.** The next negative must be an *actual SQL write against an invented, shared, RAM-only DB*, not an untrusted Boolean.

## Exact source-only test and expected negative result

Two new `#[test]` Rust cases (`toy_14`, `toy_15`) in the existing `#[cfg(all(test, feature = "m32-g3-owned-ram-toy"))]` module, using `Connection::open_with_flags` for a unique URI `file:m32-invented-foreign-writer-<n>?mode=memory&cache=shared`. SQLite allocates no database file; any test data, migrations, events and values are invented. **Neither test opens `database::open_database`, uses an operator source/path, calls migrations 007, launches the app, writes an IPC, backup or marker, or adds a production module.** The unique counter mitigates collisions between parallel tests.

- **Case 14 — negative witness:** the first connection sets `query_only=ON`, passes the existing `PreopenedFictionalReader::new` guard, and retains its `total_changes`. The second independently opened in-memory SQLite connection then commits an update to one invented event's *text* (not the count, not the version). Expected result: the reader's `total_changes` is **unchanged**, `read_again()` still returns `Ok` with unchanged count/lineage, **but the event text is different**. A PASS in CI means *the guard failed to detect a real same-database external modification in the invented fixture*, not that it has become safe.
- **Case 15 — bounded detection:** another invented writer deletes its only fictional event. The reader's local change count is unchanged; this time `read_again()` rejects, because its count validator sees the drift. This demonstrates *selective* detection, not comprehensive prevention of foreign writers.

**Technical grounding:** [SQLite `PRAGMA query_only`](https://www.sqlite.org/pragma.html#pragma_query_only) is about the connection; [SQLite `total_changes()`](https://www.sqlite.org/lang_corefunc.html#total_changes) counts changes to its connection only. Neither attests to another connection. [SQLite Online Backup](https://www.sqlite.org/backup.html) provides a consistent completed snapshot when used correctly but no independent source provenance or global absence-of-writer proof. [SQLite WAL documentation](https://www.sqlite.org/wal.html) warns that sidecar state matters, and [Microsoft CreateFileW](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew) governs Windows open/share compatibility.

## Security consequence

A hypothetical future G3 owner must mediate **all** write channels (including independent connection and external-process writers), authenticate the exact original, bind source file identity over a bounded custody lifetime, and handle transaction/journal semantics. `query_only` and `total_changes` are useful local checks but **cannot serve as global writer-exclusion proofs**. The test's output is strictly **`SYNTHETIC_COUNTEREXAMPLE_ONLY`** and it adds no Windows procedure.

**Gates preserved:** `G2B=NOT_ACCEPTED`, `SOURCE_IDENTITY=PARTIAL_LOCAL_IDENTITY_ONLY`, `SQLITE_WRITER_ABSENCE=NOT_PROVEN`, `G2C=NOT_AUTHORIZED`, `G3_REAL=STOP_UNAVAILABLE`, `M3.2=IN_PROGRESS_NOT_ACCEPTED`, historical `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 OPEN/DRAFT. M3.1 v7 and other roles still not assessed by B1; the old B0/B1 consents are consumed. Linux selected `glib=0.18.5` advisory remains `OPEN_NOT_REMEDIATED`.

**CI expectations, not claims:** before protected merge, require the full latest-HEAD Windows job terminal SUCCESS, *at least two new `m32_preopened_query_only_toy` tests*, 107th handoff contract and no skipped tests. After merge, require independent postmain terminal SUCCESS on the exact new `main`. Do not carry old CI conclusions into the new HEAD.
