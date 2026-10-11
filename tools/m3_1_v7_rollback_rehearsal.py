"""M3.1 fourth-copy forced-error transaction rollback rehearsal; NEVER production.

Requires exact closed-production v6 SHA, approved backup+restore+manifest
custody and exact candidate source SQL. The separate --dry-run performs no
writes; --create writes ONLY a freshly named fourth disposable copy and its
verification manifest. It MUST intentionally fail inside the BEGIN IMMEDIATE
migration transaction; unexpected success is an error, never a PASS.
"""
from __future__ import annotations

import argparse
from contextlib import closing
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sqlite3
import sys
from uuid import uuid4

import m3_1_v6_audit as audit
import m3_1_v6_backup as backup
import m3_1_v7_copy_rehearsal as v7


class RollbackStop(Exception):
    pass


def _inventory(path: Path) -> list:
    with closing(sqlite3.connect(
        path.as_uri() + "?mode=ro", uri=True, timeout=0
    )) as db:
        db.execute("PRAGMA query_only=ON")
        return v7._inventory(db)


def _intentional_failed_ddl(path: Path, sql: str) -> str:
    # This connection is exclusively to the new fourth copy. The source
    # safety backup, the prior third v7 copy and production are never opened
    # writable by this function.
    with closing(sqlite3.connect(path, timeout=1)) as conn:
        conn.execute("PRAGMA foreign_keys=ON")
        if conn.execute("PRAGMA foreign_keys").fetchone() != (1,):
            raise RollbackStop("foreign_keys_disabled")
        if conn.execute(
            "SELECT max(version) FROM schema_migrations"
        ).fetchone() != (6,):
            raise RollbackStop("fourth_copy_not_v6")
        try:
            conn.executescript("BEGIN IMMEDIATE;\n" + sql + "\n")
            if not conn.in_transaction:
                raise RollbackStop("transaction_not_active")
            for name in audit.CANDIDATE_TABLES:
                if conn.execute(
                    "SELECT type,strict FROM pragma_table_list "
                    "WHERE schema='main' AND name=?", (name,),
                ).fetchall() != [("table", 1)]:
                    raise RollbackStop("v7_ddl_not_fully_staged_" + name)
            if conn.execute(
                "SELECT type FROM sqlite_schema "
                "WHERE type='trigger' AND name='world_time_precedences_guard'"
            ).fetchone() != ("trigger",):
                raise RollbackStop("cycle_trigger_not_staged")
            # Version=6 already exists. Force a PRIMARY KEY violation AFTER
            # the exact complete candidate DDL is staged, BEFORE inserting
            # version=7 and BEFORE any COMMIT. It is never a random fault.
            try:
                conn.execute(
                    "INSERT INTO schema_migrations(version,name) "
                    "VALUES(6,'intentional_atomic_rollback_probe')"
                )
            except sqlite3.IntegrityError as error:
                if (not conn.in_transaction
                        or not error.sqlite_errorname.startswith(
                            "SQLITE_CONSTRAINT"
                        )):
                    raise RollbackStop("unexpected_constraint_state") from error
                return error.sqlite_errorname
            raise RollbackStop("intentional_failure_did_not_occur")
        finally:
            # Rollback even when a staging assertion itself fails.
            if conn.in_transaction:
                conn.rollback()


def perform(
    root: Path, relative: str, expected_active: str,
    expected_source: str, expected_logical: str,
    expected_backup: str, expected_manifest: str,
    candidate_sql_file: Path, expected_sql: str, create: bool,
) -> dict:
    # Reuse *all* source/custody/SQL gates from the qualified copy-v7 runner
    # in no-write mode. A hash/name mismatch must stop before new files.
    ready = v7.perform(
        root, relative, expected_active, expected_source, expected_logical,
        expected_backup, expected_manifest, candidate_sql_file,
        expected_sql, create=False,
    )
    if ready["status"] != "READY":
        raise RollbackStop("preflight_not_ready")
    if not create:
        return {
            "status": "READY",
            "mode": "fourth_copy_rollback_dry_run",
            "source_schema_version": 6,
            "backup_sha256": expected_backup,
            "candidate_sql_sha256": expected_sql,
            "forced_failure_executed": False,
            "new_copy_created": False,
        }

    baseline = backup._check_baseline(
        root, expected_active, expected_source, expected_logical
    )
    old_dir = v7._custody(root, relative)
    old_backup = old_dir / "fabulaxiom-pre-m3-1-v6.sqlite3"
    old_restore = old_dir / "isolated-restore-rehearsal-v6.sqlite3"
    old_manifest = old_dir / "manifest.json"
    sql = candidate_sql_file.read_text(encoding="utf-8")
    stage = root / "operator-qualification" / "m3_1"
    audit._directory(stage)
    dirname = (
        "v7_rollback_rehearsal_"
        + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        + "-" + uuid4().hex
    )
    folder = stage / dirname
    folder.mkdir(exist_ok=False)
    fourth = folder / "failed-v7-rolled-back-v6.sqlite3"
    manifest_file = folder / "rollback-manifest.json"

    backup._snapshot(old_backup, fourth)
    backup._validate_copy(fourth, baseline)
    initial_hash = audit._file_sha256(fourth)
    initial_inventory = _inventory(fourth)
    error_name = _intentional_failed_ddl(fourth, sql)
    if _inventory(fourth) != initial_inventory:
        raise RollbackStop("partial_v7_schema_survived_rollback")
    verified = backup._validate_copy(fourth, baseline)
    if audit._file_sha256(fourth) != initial_hash:
        raise RollbackStop("fourth_copy_bytes_changed_after_rollback")

    # Keep source custody and any earlier v7 copy exactly as-is. The former
    # active file/pointer is re-resolved and content-hashed by this check.
    if backup._check_baseline(
        root, expected_active, expected_source, expected_logical
    ) != baseline:
        raise RollbackStop("production_modified_during_rehearsal")
    if audit._file_sha256(old_backup) != expected_backup:
        raise RollbackStop("original_backup_modified")
    if audit._file_sha256(old_restore) != expected_backup:
        raise RollbackStop("preserved_restore_modified")
    if audit._file_sha256(old_manifest) != expected_manifest:
        raise RollbackStop("source_manifest_modified")
    if audit._file_sha256(candidate_sql_file) != expected_sql:
        raise RollbackStop("candidate_sql_modified")
    record = {
        "protocol": "m3_1_fourth_copy_forced_rollback_v1",
        "original_production_schema_version": 6,
        "original_source_sha256": expected_source,
        "original_v6_backup_sha256": expected_backup,
        "original_v6_manifest_sha256": expected_manifest,
        "candidate_sql_sha256": expected_sql,
        "forced_sqlite_error": error_name,
        "rolled_back_file": fourth.name,
        "rolled_back_file_sha256": verified["sha256"],
        "rolled_back_file_bytes": verified["bytes"],
        "rolled_back_schema_version": 6,
        "legacy_logical_sha256": verified["combined_logical_sha256"],
        "all_14_legacy_tables_preserved": True,
        "schema_inventory_identical_to_pre_failure": True,
        "fourth_copy_bytes_identical_to_pre_failure": True,
        "production_migrated": False,
        "active_pointer_modified": False,
    }
    with manifest_file.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(record, stream, indent=2, sort_keys=True)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    if json.loads(manifest_file.read_text(encoding="utf-8")) != record:
        raise RollbackStop("manifest_reopen_mismatch")
    return {
        "status": "PASS",
        "mode": "fourth_copy_forced_rollback",
        "relative_rehearsal_dir": str(
            Path("operator-qualification") / "m3_1" / dirname
        ),
        "intentional_error": error_name,
        "rolled_back_schema_version": 6,
        "rolled_back_file_sha256": verified["sha256"],
        "manifest_sha256": audit._file_sha256(manifest_file),
        "legacy_tables_preserved": 14,
        "production_migrated": False,
        "active_pointer_modified": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app-data-root", type=Path, required=True)
    parser.add_argument("--custody-relative-dir", required=True)
    parser.add_argument("--expected-active-file", required=True)
    parser.add_argument("--expected-source-sha256", required=True)
    parser.add_argument("--expected-logical-sha256", required=True)
    parser.add_argument("--expected-backup-sha256", required=True)
    parser.add_argument("--expected-manifest-sha256", required=True)
    parser.add_argument("--candidate-sql-file", type=Path, required=True)
    parser.add_argument("--expected-candidate-sql-sha256", required=True)
    parser.add_argument("--ack-app-stopped", action="store_true")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--dry-run", action="store_true")
    action.add_argument("--create", action="store_true")
    args = parser.parse_args(argv)
    try:
        if not args.ack_app_stopped:
            raise RollbackStop("operator_must_acknowledge_app_stopped")
        result = perform(
            args.app_data_root, args.custody_relative_dir,
            args.expected_active_file, args.expected_source_sha256,
            args.expected_logical_sha256, args.expected_backup_sha256,
            args.expected_manifest_sha256, args.candidate_sql_file,
            args.expected_candidate_sql_sha256, args.create,
        )
    except (RollbackStop, audit.AuditError, backup.BackupStop, v7.RehearsalStop,
            OSError, sqlite3.Error, ValueError) as error:
        result = {
            "status": "FAIL",
            "reason": str(error) if isinstance(
                error, (RollbackStop, audit.AuditError, backup.BackupStop,
                        v7.RehearsalStop)
            ) else "rollback_rehearsal_error",
            "note": "preserve_any_new_fourth_copy_files_no_cleanup",
        }
    print(json.dumps(result, sort_keys=True, ensure_ascii=True))
    return 0 if result["status"] in ("READY", "PASS") else 2


if __name__ == "__main__":
    sys.exit(main())
