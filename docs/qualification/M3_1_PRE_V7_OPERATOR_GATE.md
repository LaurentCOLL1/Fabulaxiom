# M3.1 — Operator pre-v7 fail-closed gate (partial Windows qualification)

**Windows operator evidence exists for the v6 backup/restore and isolated third-copy candidate-v7 migration. Production remains at v6, no application startup migration or activation was authorized. The PR remains a draft.**

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

## Source and activation-marker stability before reporting PASS

The standalone audit now brackets its read-only SQLite inspection with **full-file SHA-256 and filesystem identity checks**. It re-resolves the M1.5 active pointer after closing the connection, rejects a changed selected database or new SQLite sidecars, and refuses `PASS` when the active file or pointer changes during inspection. Two synthetic Python tests simulate a changed source digest and activation-marker switch; both must fail without repair.

These are additional race-detection controls, **not proof that the application was stopped** or that a complete operator backup exists. A successful audit remains advisory, cannot substitute for historical backup custody, and does not authorize v7.

## Independently testable operator v6 backup and restore gate (new source)

`tools/m3_1_v6_backup.py` uses the already qualified read-only M1.5 v6 inspector as a fail-closed gate. Its required command-line arguments are explicit app-data root, exact restored-active filename, **previously observed original source file SHA-256**, **previously observed v1 logical digest**, and application-stopped acknowledgement. The required `--dry-run` mode creates **no files**. The required, distinct `--create` mode is the *only* action that creates custody files.

The `--create` procedure creates a **new UUID-suffixed directory** under existing operator custody `operator-qualification/m3_1/`, never overwrites any historical file or existing source. It uses Python `sqlite3.Connection.backup` (official SQLite Online Backup API) to create a new SQLite-consistent v6 backup; reopens that backup read-only and compares **all 14 v6 tables (typed SHA-256 row hashes)**, six migration names, owner, physical integrity and foreign-key integrity against the exact preflight baseline. It then runs a **second** Online Backup API operation *from the validated backup to a separate new database* and checks all counts and digests again. The M1.5 source pointer and source SHA-256 are rechecked afterward; only then does it create a unique manifest with source/backup/restore file hashes and the standardized logical digest. The manifest and output intentionally omit absolute Windows paths and user narrative text.

**Failure semantics:** original source and historical backups must remain intact. If an exception occurs after creating the new custody directory, retain it for operator investigation (no automatic deletion or overwrite); no production restoration or v7 migration is performed. These outputs are not release artifacts. CI tests operate **exclusively on synthetic disposable SQLite databases**; an exact-head CI PASS is necessary before proposing operator invocation, but operator Windows evidence and independent backup/restore review are also required.

The Windows-only regression of the WAL refusal fixture demonstrated that the `sqlite3.Connection` context manager **does not close a connection**. The test now uses explicit `contextlib.closing` to release the temporary database handle before fixture cleanup. Destination validation also refuses any unexpected v7 candidate table and requires all 14 legacy tables to remain STRICT. A new synthetic adversarial case covers premature v7 table creation.

SQLite sources: [Python sqlite3 Connection.backup](https://docs.python.org/3.12/library/sqlite3.html#sqlite3.Connection.backup), [SQLite Online Backup API](https://www.sqlite.org/backup.html), [SQLite integrity & FK checks](https://www.sqlite.org/pragma.html).

## Operator copy-only v7 rehearsal (source gate, NOT executed)

Following the successful real Windows operator v6 backup and independent restore rehearsal of 2026-10-11 (original production unchanged), `tools/m3_1_v7_copy_rehearsal.py` introduces a separately authorized **third database** rehearsal. Its input is the qualified `fabulaxiom-pre-m3-1-v6.sqlite3` safety backup, not the active production SQLite, not the preserved restore rehearsal and not an old historic backup. It refuses to run unless the active M1.5 v6 source filename, original file SHA-256 and v1 logical digest match; the backup, preserved restore and custody manifest SHA-256 are each independently verified; the candidate `.sql` file must match its expected SHA-256. Normal app startup remains capped at v6.

The distinct `--dry-run` mode writes nothing. After a separate reviewed operator step, `--create` makes a *new* UUID-scoped sibling directory under existing `operator-qualification/m3_1/`, uses SQLite Online Backup API to produce a third derivative, verifies the copied source v6, and applies the exact candidate v7 DDL + version-7 migration ledger row in **one explicit transaction**. On error the transaction rolls back; the new derivative remains for investigation and is never activated. The rehearsed v7 is validated against an independent in-memory expected schema inventory; the old 14-table row digests (except the one intentional additional version-7 ledger row) and existing owner, FK integrity, physical integrity, three STRICT new tables and their initial empty state are verified. A second read-only validation confirms stable idempotent observations. Only the new derivative and its own evidence manifest are written; the operator's safety backup, rehearsal v6 restore, historical backups, active pointer, and production v6 are rechecked as unchanged.

Tests are disposable synthetic fixtures on Windows CI, not operator Windows acceptance. **No `--create` command is approved to run on a real operator machine merely because source CI passes**; complete a read-only rehearsal dry-run first, and independently qualify all SHA and evidence gates. The existing tool deliberately has no Tauri invocation or automatic v7 registration.

## Fourth-copy forced rollback acceptance gate (source-only)

`tools/m3_1_v7_rollback_rehearsal.py` adds a **distinct** operator process for a *fourth* disposable derivative of the already SHA-qualified M3.1 v6 safety backup. It imports and reruns the existing M1.5 active-source audit and v6 backup/restore/manifest/candidate-SQL SHA checks before any new files can be created. Its `--dry-run` is genuinely no-write; `--create` makes a never-before-existing UUID-scoped directory, derives a fourth v6 file using SQLite's Online Backup API, and snapshots its exact physical SHA, legacy 14-table logical values and complete schema DDL inventory.

On the new fourth file only, it explicitly starts `BEGIN IMMEDIATE`, stages the **complete exact candidate 007 SQL** without committing, checks all three STRICT tables and the cycle trigger inside the open transaction, then deliberately attempts to insert the **already existing migration version 6**, requiring a SQLite `SQLITE_CONSTRAINT` error and rolling back that open transaction. It must reopen the fourth file in read-only mode and prove **v6 lineage, every legacy table/digest, both SQLite integrity checks, full DDL identity and exact pre-failure file SHA-256**. A separate manifest captures the observed deliberate constraint error and before/after custody fingerprints. Unexpected commit/no error/partial schema/bytes changed always FAIL; never auto-repair or delete failed rehearsal files.

The **six deterministic synthetic Windows CI cases** cover dry-run, successful deliberate failure and rollback, source/SQL tampering, invalid candidate SQL and unexpected active-file selection. Source CI success on the **new HEAD** is required before any operator Windows step. A real `--create` is not pre-authorized by adding source, and must follow a separately verified operator `--dry-run`. No active production DB, its M1.5 activation marker, old backups, prior v6 restore or successful third-copy v7 file may be migrated or modified.

This confirms SQLite's explicit transaction semantics, not an app startup v7 migration: https://www.sqlite.org/lang_transaction.html ; Python `sqlite3.executescript` requires transaction control in the script itself: https://docs.python.org/3.12/library/sqlite3.html#sqlite3.Connection.executescript .

## Independent third-copy read-only and RAM-only temporal audit (new source)

`tools/m3_1_v7_final_readonly.py` is an operator-invoked read-only procedure, **not** a migration. It verifies exact M1.5 production v6 active filename, original SHA/logical digest, v6 safety backup+restore SHA, both pre-v7/third-v7 custody manifests, exact reviewed candidate SQL and **third v7 candidate SHA**, before reading v7 through `mode=ro` with `PRAGMA query_only=ON`. The candidate's full DDL inventory is checked against an independently reconstructed **RAM candidate** derived from the verified v6 backup; all fourteen legacy table digests are checked (with exactly one allowed new migration ledger row), SQLite integrity/FKs and three new empty STRICT tables.

For semantic constraints, the tool uses SQLite Online Backup API **read-only third copy → fresh `:memory:` connection**, then performs positive and negative DML probes *only inside RAM savepoints that are rolled back*. Tests cover raw fictional exact/approximate/unknown representations without Gregorian parsing, required precision/calendar, same-Universe event and immutable revision scope, cross-Universe calendar/event/revision rejection, partial precedence ordering, cycle/self/cross-Universe rejection and immutability UPDATE/DELETE rejection. These probes never write to the protected third v7 file. The final output includes scenario count, SHA-256 and booleans; no fiction text or absolute operator paths. Source SHA and all protected input hashes are rechecked after the read-only audit.

Synthetic Windows CI **uses the real governed v7 SQL file** (not a simplified stand-in) on wholly disposable SQLite fixtures. Exact-head CI must PASS before any actual operator execution. Production v7 startup, migration 007 registration, PR merge and M3.2 remain separately gated.

## Target-Windows acceptance requirements (copy and rollback qualified; final gate pending)

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

**Current status (2026-10-11):** Operator third-copy candidate v7 migration **PASS**, fourth-copy forced-error rollback **PASS** (`SQLITE_CONSTRAINT_PRIMARYKEY`, no partial v7 schema), and final real third-v7 read-only audit **PASS** (14/14 legacy tables, 10/10 RAM-only time constraints, eight original custody SHA-256 values intact). Detailed operator output and file hashes are recorded in `docs/qualification/M3_1_WINDOWS_OPERATOR_EVIDENCE.md`. This documentation revision requires **its own** exact-head terminal `pull_request` CI and fresh PR scope review. The roadmap's controlled-launch/post-v7 gate is not equivalent to the candidate-copy trial and remains separately unresolved. PR #33 is not merged or normalized. Production stays v6; automatic migration 007 is NOT authorized; M3.2+ remains blocked.

## Normal v6 startup refusal and explicit read-only v7 inspection (source test only)

The test-only Rust module `src-tauri/src/world_time_file_migration_tests.rs` now includes `controlled_readonly_launch_refuses_auto_v7_without_changing_disposable_files`. It creates a **new closed disposable v6** file with representative M2 historical text, entity, exact UTF-8 citation and human canon reviews; copies it only after closing SQLite; applies candidate 007 to the new owned copy only. It then closes that test copy and **calls the unchanged real production `database::open_database` function on this v7 file**. Correct behavior is `ExplicitMigrationRequired(7)` with byte-identical v7 file and original v6 source. Thus a normal startup cannot silently downgrade, repair or begin running against v7.

Separately, the test opens that already-created disposable v7 file with SQLite `SQLITE_OPEN_READ_ONLY`, verifies the existing 14 legacy tables/records, v7 ledger, three time tables (new anchors empty), physical and foreign-key integrity, and refuses an attempted direct DML write. Source and copy must still be byte-identical to their baseline after all checks. This is a **source-only controlled-launch boundary test**, not a successful *Tauri graphical launch* on a distinct Windows identity and not an operator production migration.

**Critical unresolved roadmap distinction:** the application is intentionally still incapable of launching normally on a v7 active pointer. Neither this source test nor the operator's third-copy SQLite v7 read-only audit satisfies the roadmap's eventual *controlled application launch + post-v7 audit* acceptance alone. Before merging/normalizing M3.1 or authorizing M3.2, the controlled Windows application/isolated-identity launch boundary and explicit v7 activation policy must be separately approved, built and qualified (without touching restored-active production v6 or historical custody). `MAX_AUTOMATIC_MIGRATION_VERSION=6` and `CURRENT_SCHEMA_VERSION=6` are retained; no v7 Tauri IPC, startup auto-upgrade or production activation is added.

Official SQLite docs: [transactions](https://www.sqlite.org/lang_transaction.html), [read-only connection flags](https://www.sqlite.org/c3ref/open.html).

