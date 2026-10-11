# M3.1 — Operator pre-v7 fail-closed gate (design, NOT executed)

**PROTOCOL ONLY — no Windows app/database/backup action has been performed, no release or migration v7 activated.**

## Purpose and current source authority

- Planning and independent normalization are merged, `main=6506d436357a22ee746ddce8520a4287a47652d8`.
- M3.1 draft PR #33 contains an **isolated candidate** SQL under `src-tauri/sql/m3_1_world_time_v7_candidate.sql`; it is not in the automatic migration array.
- `src-tauri/src/database.rs` still reports `CURRENT_SCHEMA_VERSION=6`, and `open_database` still automatically runs **only migrations 1–6**.
- Read-only fail-closed preflight **prototype**: `src-tauri/src/world_time_preflight.rs` is compiled under `#[cfg(test)]` only. It cannot be invoked via the shipped Tauri bridge. No source-only gate is sufficient to qualify real Windows data.

## Why this gate cannot be bypassed

The current normal app launch calls `database::open_database`, which executes all pending migrations. Simply appending 007 to that array risks an unsolicited modification of the real active restored database. Until a separately qualified explicit opt-in migration/activation boundary exists, **never register v7 in the ordinary startup runner** and never increase `CURRENT_SCHEMA_VERSION`.

SQLite's [Online Backup API](https://www.sqlite.org/backup.html) and `VACUUM INTO` permit consistent database snapshots; copying only a live SQLite main file is insufficient, particularly with WAL. SQLite [`PRAGMA integrity_check`](https://www.sqlite.org/pragma.html#pragma_integrity_check) does **not** detect foreign-key failures; independently check `foreign_key_check`. Read-only opening needs an explicit read-only mode; do not treat an `immutable=1` URI on a live database as normal proof of consistency.

## Disposable file-backed migration rehearsal

The test-only Rust module `src-tauri/src/world_time_file_migration_tests.rs` rehearses an atomic candidate upgrade on **new, disposable test databases only**. It creates a v6 database with existing immutable scene text and human fact reviews, **closes its SQLite connection before any `fs::copy`**, and applies the candidate SQL plus a simulated v7 registry record on a **separate test copy** in one transaction.

The acceptance assertions are deliberate: the new copy reaches v7 with three STRICT tables, M2 human-approved canon and Unicode historical revision preserved, both SQLite integrity checks pass, and the original v6 file and its sealed test copy remain byte-identical to their pre-test bytes. A deliberately failing migration must rollback the candidate copy to v6 and preserve legacy content. Empty v6 copy coverage is included.

**These `fs::copy` calls are suitable only for *closed disposable test databases*. Never copy a live SQLite main file this way in the operator protocol.** Actual live/restored production pre-v7 custody requires an independently qualified SQLite-consistent backup, verified non-overwriting manifest, active pointer protection, and deliberate opt-in. These tests do not generate a production-safe backup or an operator authorization.

## Strengthened closed-file and WAL test coverage

The file-backed fixture tests now take deterministic, type-tagged, row-order-independent snapshots of **every column and row of all 14 legacy v6 tables**. For the new v7 copy, the only intentional difference in the old migration registry is a new version-7 row; the original six rows must remain byte/value-identical. Both the successful upgrade and failed upgrade rollback assert the entire legacy snapshot, not merely counts or selected canonical facts. These snapshots are **test-only data comparisons, not yet production SHA-256 manifests**.

A separate test uses an actual open, disposable SQLite **WAL** source and `VACUUM INTO` to create a SQLite-consistent non-overwriting copy. The copied database is reopened in read-only mode and inspected while the source connection is still open, followed by a source comparison. This explicitly checks that a proper SQLite backup works for WAL fixtures; it does not use `fs::copy` for a live source.

The official references are [SQLite Backup API](https://www.sqlite.org/backup.html), [VACUUM INTO](https://www.sqlite.org/lang_vacuum.html#vacuuminto) and [SQLite PRAGMAs](https://www.sqlite.org/pragma.html#pragma_integrity_check). `integrity_check` cannot replace `foreign_key_check`.

**Gate status:** all newly changed test code needs fresh terminal exact-head Windows PR CI. A previous green run remains evidence for its own commit only.

## Fail-closed automatic migration ceiling (source guard)

Normal runtime startup now has a dedicated constant `MAX_AUTOMATIC_MIGRATION_VERSION=6`, independently of `CURRENT_SCHEMA_VERSION=6`. The runtime guard refuses any future migration whose version exceeds 6 **before running that migration's SQL**, and also refuses a database already declaring an unsupported v7+ schema when entered through the ordinary `run_migrations` path. A new explicit `ExplicitMigrationRequired` diagnostic identifies the separate-authorization requirement; it does not opt in, convert, delete, downgrade or repair anything.

Two Rust in-memory tests verify both barriers using synthetic version-7 fixtures: no SQL or ledger insertion for an unapproved pending v7, and no automatic reopening/migration of a v7-marked database through the ordinary v6 runner. This is a **defense-in-depth source guard, not authorization to deploy a v7 migration**. Any future explicit migration ceremony must use a separately reviewed operator-controlled entry point, after successful backup custody and the Windows qualification gate.

## Populated legacy provenance and WAL snapshot boundary

The disposable populated v6 migration rehearsal now deliberately creates at least one row in **every one of the 14 legacy v6 tables**, including a series, entity alias, exact UTF-8 `fact_sources` quote, immutable scene revision and two human review events culminating in canon approval. The before/after comparison checks all original rows and typed column values, not merely row counts. The M2.3 citation uses the exact byte span `Éclipse` (8 UTF-8 bytes), and the source revision belongs to the same Universe.

The WAL backup test also commits a **new source record after** completing `VACUUM INTO`, then verifies that the read-only backup remains an unchanged point-in-time snapshot while the source sees the new row. All sources are disposable fixtures; the production app and its active marker are untouched.

## Explicit candidate migration idempotence (tests only)

The source-only `world_time_file_migration_tests.rs` now prototypes a **non-runtime**, explicit migration sequence that first checks the current v6 preflight, creates candidate v7 tables in a single transaction and adds the exact version-7 ledger row. A repeat invocation on an already-upgraded disposable copy validates the full seven-entry lineage, three STRICT tables and SQLite integrity before returning a **no-op**. It refuses forged version-7 ledgers lacking tables and unsupported version 8; it never attempts to repair or downgrade another schema.

Regression tests retain a human-authored time anchor, the existing 14 legacy tables and the original v6 file across a repeated request. This is *not* a production migration entry point and does not change the automatic migration ceiling of v6 or authorize operator action.

## Idempotence schema-identity veto

The test-only explicit-candidate retry gate now compares the **full SQLite DDL inventory** of the three governed time tables, their triggers, indexes and autoindexes against a freshly constructed isolated reference database at the exact candidate source SQL. This is stricter than accepting a v7 registry row plus three STRICT table names. New adversarial fixtures simulate deleting the chronology cycle-protection trigger or inserting an unreviewed index: both must refuse the second operation, without silently repairing history, changing original M2 data or mutating the closed v6 source file.

These checks are not cryptographic backup validation, nor do they authorize a Windows production migration. They protect the **test-only** candidate's structural idempotence until the production opt-in design and operator backup qualification can be independently accepted.

## Legacy v6 schema DDL identity on candidate retry

The explicit *test-only* v7 retry gate now compares **both** the three governed M3.1 tables and the complete pre-existing v6 `sqlite_schema` definitions for legacy tables, indexes, autoindexes and triggers, against pristine migrations 1–6 recreated in a disposable in-memory reference. A version-7 ledger with intact new M3 tables is insufficient if an old scene-revision append-only trigger has been dropped or an unreviewed index has appeared on a legacy table. Two targeted adversarial fixtures require refusal without schema auto-repair, data rewriting or modification to the original closed v6 source file.

This is a strict test prototype; SQLite `sqlite_stat%` statistics structures are excluded from the legacy DDL comparison because they are optimization metadata. It does not authorize production migration, create an operator backup or supersede data-content logical digests.

## Offline read-only operator audit candidate (source available, not executed)

The new standalone Python 3.12 standard-library tool `tools/m3_1_v6_audit.py` is deliberately **not** a migration command and cannot create a backup. It requires an **explicit absolute app-data root** and an explicit `--ack-app-stopped` operator assertion (not a process detector). It follows the M1.5 `database/activations/activation-*.active` pointer naming/sorting algorithm before falling back to the default database. It refuses missing or symlinked files, wrong six-version lineage, incorrect owner, unexpected v7 tables, non-STRICT legacy tables, sidecar `-wal/-shm/-journal` files, failed SQLite physical/FK integrity or any other validation error.

It opens the selected file only with SQLite URI `mode=ro` and `query_only=ON`; it never calls the app's `open_database` automatic migration runner. Its JSON output on stdout contains the **active filename only** (no absolute path or row contents), original closed-file SHA-256, per-table type-aware logical SHA-256 and row counts for all 14 legacy tables. The `fabulaxiom-v6-typed-row-sha256-v1` algorithm is a **new audit algorithm** and its digest must not be compared as if identical to older operator logical-digest algorithms. A passing dry-run does **not** verify app shutdown, historical backup custody or approval for v7.

`tools/test_m3_1_v6_audit.py` exercises eight disposable synthetic v6 fixtures, including M1.5 restored-pointer selection, invalid marker, erroneous migration registry, broken foreign key, WAL sidecar rejection, missing database refusal and non-mutating successful audit. GitHub Windows CI invokes the Python tests using a pinned 3.12 interpreter. **Do not execute the tool against the operator's actual data until an explicit preflight sequence is agreed.** No Python standard-library dependencies or lockfile changes are introduced.

## Strict WAL-header hard stop (read-only audit)

The preflight explicitly reads and validates the SQLite header's journal format bytes **before opening the database**. It accepts only the ordinary rollback-journal header bytes `01 01` and refuses `02 02` (WAL mode) even if no `-wal`/`-shm` sidecar currently exists. Existing auxiliary files also cause a hard failure; neither is removed or checkpointed. Operators must preserve any WAL content and use a separately approved, SQLite-consistent backup procedure instead of trying to fix sidecars or force-open WAL from this audit.

This behavior follows the SQLite WAL documentation: <https://www.sqlite.org/wal.html> and file format <https://www.sqlite.org/fileformat2.html>. The synthetic Python test checks WAL mode persistence after a clean close. This is intentionally conservative and may refuse a healthy database; **never treat refusal as corruption or delete files to make the audit pass**.

## Target-Windows operator prerequisites (not yet authorized to execute)

1. Announce all interactive actions in advance, including any required terminal confirmation, `q` exit, privilege prompt or app close. Confirm Fabulaxiom, Tauri and Ollama are stopped when required. No scripted `reset --hard`, mass cleanup or blind deletion.
2. Fresh exact GitHub `main`, candidate PR, workflow HEAD, own isolated Windows worktree. Keep source separate from app data; never assume `fabulaxiom.sqlite3` is active.
3. Resolve **actual active database** via the M1.5 activation marker using the existing validated resolver. Record its absolute path and do not rewrite the marker.
4. Inspect the existing v6 database **read-only**: schema owner, exact six migration names, `foreign_keys=ON`, `integrity_check=ok`, `foreign_key_check` empty, all preexisting STRICT tables and row counts, historical immutable revision heads, citations and review events.
5. Independently enumerate and hash all operator-owned backups and existing manifest files (pre-M2.1 v3, pre-M2.3 v4, pre-M2.4 v5, restored-active production v6, isolated M2.5 fixture); do not conclude corruption from a lone script mismatch. Investigate independently and halt on unexplained changes.
6. Create an **additional uniquely named, non-overwriting, SQLite-consistent v6 backup** of the resolved active database and a separate SHA-256 manifest; verify backup by reopening it and rerunning both SQLite PRAGMAs. Take full legacy table-by-table logical digests using an agreed canonicalization algorithm. Never change expected historical hashes to make a gate pass.
7. Test rollback on a separate disposable operator-owned copy, with marker and original production database unmodified. A failed migration must not switch the active file, erase history or leave a half-created v7 schema.
8. Only after independent gate acceptance should a deliberately invoked migration apply the reviewed 007 schema to a **new copy**, with explicit operator approval and verified post-v7 row/digest preservation. Recheck all scene revision pointers, Unicode citations, human review events, source links, triggers, `integrity_check`, `foreign_key_check` and the precise migration lineage.
9. CI PASS and controlled Windows PASS on an implementation SHA are separate evidence. Commit operator results without secrets or absolute personally identifying Windows paths, rerun CI on the new evidence SHA, merge with `expected_head_sha`, re-fetch `main` and normalize in an independent documentary PR.

## Current automated prototype scope

`world_time_preflight.rs` runs **only during in-memory Rust tests**. Its `inspect_v6` performs **read-only SELECT and PRAGMA queries**, checking the owner, version, ordered migration names, foreign-key enforcement, schema STRICTness, unexpected candidate tables, physical integrity, FK violations and baseline row counts. Regression fixtures deliberately simulate wrong owners, migration tampering, disabled FKs, synthetic orphan references and out-of-order staging **only on disposable in-memory databases**.

These checks intentionally **do not** replace source SHA custody, active pointer resolution, a consistent backup, verified SHA-256 manifest, full logical digests, operator/app shutdown evidence or a separately approved migration ceremony.

**Status: DESIGN / ISOLATED TEST CANDIDATE ONLY. No user-facing PowerShell commands or production SQLite changes are authorized by this document.**
