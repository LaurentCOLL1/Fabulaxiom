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
