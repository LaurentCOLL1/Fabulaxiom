"""M3.1 gated operator v6 safety snapshot + isolated restore rehearsal.

This is NOT the M3.1 v7 migration. Requires a positive operator action
(--create) and a previously audited exact source SHA-256, logical SHA-256 and
M1.5-selected active file name. Existing sources, M1.5 activation markers and
old operator backups are NEVER written. Only new uniquely named custody files
are created. On failure, quarantine output IN PLACE; never auto-delete it.

Use Python 3.12 standard library only. Do not execute on operator data before
exact-head Windows CI and an explicit operator readiness check.
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


class BackupStop(Exception):
    pass


def _verify_hash(value: str) -> str:
    if len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
        raise BackupStop("expected_sha256_invalid")
    return value


def _check_baseline(root: Path, expected_file: str, expected_sha: str,
                    expected_logical: str) -> dict:
    if root.name != "com.fabulaxiom.desktop":
        raise BackupStop("production_app_root_name_mismatch")
    baseline = audit.audit(root)
    if baseline["active_file"] != expected_file:
        raise BackupStop("active_m15_file_mismatch")
    if baseline["closed_file_sha256"] != expected_sha:
        raise BackupStop("source_sha256_mismatch")
    if baseline["combined_logical_sha256"] != expected_logical:
        raise BackupStop("source_logical_sha256_mismatch")
    if baseline["schema_version"] != 6:
        raise BackupStop("not_production_sqlite_v6")
    return baseline


def _validate_copy(path: Path, original: dict) -> dict:
    audit._regular_file(path)
    audit._reject_sidecars(path)
    with path.open("rb") as stream:
        header = stream.read(20)
    if header[:16] != b"SQLite format 3\x00" or header[18:20] != b"\x01\x01":
        raise BackupStop("copy_header_not_rollback_sqlite")
    with closing(sqlite3.connect(path.as_uri() + "?mode=ro", uri=True, timeout=0)) as db:
        db.execute("PRAGMA query_only=ON")
        db.execute("PRAGMA foreign_keys=ON")
        if db.execute("PRAGMA foreign_keys").fetchone() != (1,):
            raise BackupStop("copy_foreign_keys_disabled")
        if db.execute("PRAGMA integrity_check").fetchall() != [("ok",)]:
            raise BackupStop("copy_integrity_failure")
        if db.execute("PRAGMA foreign_key_check").fetchone() is not None:
            raise BackupStop("copy_foreign_key_violation")
        migrations = db.execute(
            "SELECT version,name FROM schema_migrations ORDER BY version"
        ).fetchall()
        if migrations != list(enumerate(audit.MIGRATION_NAMES, 1)):
            raise BackupStop("copy_migration_lineage_mismatch")
        if db.execute(
            "SELECT value FROM app_metadata WHERE key='schema_owner'"
        ).fetchone() != ("fabulaxiom",):
            raise BackupStop("copy_owner_mismatch")
        for table in audit.LEGACY_TABLES:
            definition = db.execute(
                "SELECT type,strict FROM pragma_table_list "
                "WHERE schema='main' AND name=?", (table,)
            ).fetchall()
            if definition != [("table", 1)]:
                raise BackupStop("copy_legacy_strict_table_missing_" + table)
        for table in audit.CANDIDATE_TABLES:
            if db.execute(
                "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",
                (table,),
            ).fetchone() is not None:
                raise BackupStop("premature_v7_candidate_detected")
        combined = audit.hashlib.sha256(b"fabulaxiom-v6-typed-row-sha256-v1\0")
        tables = {}
        for table in audit.LEGACY_TABLES:
            rows, digest = audit._logical_table(db, table)
            if original["legacy_tables"][table] != {
                "rows": rows, "logical_sha256": digest
            }:
                raise BackupStop("copy_legacy_table_mismatch_" + table)
            combined.update(table.encode("ascii") + b"\0" + bytes.fromhex(digest))
            tables[table] = rows
        if combined.hexdigest() != original["combined_logical_sha256"]:
            raise BackupStop("copy_logical_digest_mismatch")
    return {
        "sha256": audit._file_sha256(path),
        "bytes": path.stat().st_size,
        "combined_logical_sha256": combined.hexdigest(),
        "legacy_table_counts": tables,
        "integrity": "ok",
        "foreign_key_check": "ok",
    }


def _snapshot(source: Path, target: Path) -> None:
    if target.exists() or target.is_symlink():
        raise BackupStop("destination_already_exists")
    with closing(sqlite3.connect(source.as_uri() + "?mode=ro", uri=True, timeout=1)) as src:
        src.execute("PRAGMA query_only=ON")
        with closing(sqlite3.connect(target)) as dest:
            # Official SQLite online backup API; never fs.copy on live source.
            src.backup(dest)


def perform(root: Path, expected_file: str, expected_sha: str,
            expected_logical: str, create: bool) -> dict:
    _verify_hash(expected_sha)
    _verify_hash(expected_logical)
    if "/" in expected_file or "\\" in expected_file or not audit.RESTORED.fullmatch(expected_file):
        raise BackupStop("expected_active_filename_invalid")
    before = _check_baseline(root, expected_file, expected_sha, expected_logical)
    custody = root / "operator-qualification"
    audit._directory(custody)
    stage = custody / "m3_1"
    if stage.exists() or stage.is_symlink():
        audit._directory(stage)
    if not create:
        return {
            "status": "READY",
            "mode": "dry_run_no_files_written",
            "schema_version": 6,
            "source_sha256": before["closed_file_sha256"],
            "source_logical_sha256": before["combined_logical_sha256"],
            "active_file": before["active_file"],
            "destination_parent_exists": stage.is_dir(),
        }

    # The only new parent permitted: stage/m3_1, under the existing operator
    # custody folder. No overwrite or deletion, including on failure.
    if not stage.exists():
        stage.mkdir(exist_ok=False)
    audit._directory(stage)
    unique = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid4().hex
    target_dir = stage / ("pre_v7_" + unique)
    target_dir.mkdir(exist_ok=False)
    dbpath = target_dir / "fabulaxiom-pre-m3-1-v6.sqlite3"
    restored = target_dir / "isolated-restore-rehearsal-v6.sqlite3"
    manifest = target_dir / "manifest.json"
    source, selected = audit.resolve_active(root)
    if selected != expected_file:
        raise BackupStop("active_pointer_changed_before_backup")
    _snapshot(source, dbpath)
    backup_result = _validate_copy(dbpath, before)

    # Independent restore rehearsal: backup -> separate never-before-existing
    # SQLite file. DO NOT change the application activation pointer.
    _snapshot(dbpath, restored)
    restore_result = _validate_copy(restored, before)
    if restore_result["combined_logical_sha256"] != backup_result["combined_logical_sha256"]:
        raise BackupStop("restore_rehearsal_logical_mismatch")

    after = _check_baseline(root, expected_file, expected_sha, expected_logical)
    if before != after:
        raise BackupStop("source_changed_during_backup")
    if backup_result["sha256"] != audit._file_sha256(dbpath):
        raise BackupStop("backup_changed_after_validation")

    record = {
        "protocol": "m3_1_operator_pre_v7_v6_backup_and_restore_v1",
        "source": {
            "active_file": expected_file,
            "sha256": expected_sha,
            "logical_sha256": expected_logical,
            "logical_algorithm": "fabulaxiom-v6-typed-row-sha256-v1",
            "schema_version": 6,
        },
        "backup": {"file": dbpath.name, **backup_result},
        "restore_rehearsal": {"file": restored.name, **restore_result},
        "active_pointer_modified": False,
        "migration_v7_executed": False,
    }
    with manifest.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(record, handle, ensure_ascii=True, sort_keys=True, indent=2)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    if json.loads(manifest.read_text(encoding="utf-8")) != record:
        raise BackupStop("manifest_reopen_mismatch")
    return {
        "status": "PASS",
        "mode": "backup_created_and_restore_rehearsal_verified",
        "source_sha256": expected_sha,
        "backup_sha256": backup_result["sha256"],
        "restore_sha256": restore_result["sha256"],
        "logical_sha256": backup_result["combined_logical_sha256"],
        "schema_version": 6,
        "legacy_tables": len(before["legacy_tables"]),
        "relative_custody_dir": str(Path("operator-qualification") / "m3_1" / target_dir.name),
        "manifest_sha256": audit._file_sha256(manifest),
        "v7_migration_executed": False,
        "active_pointer_modified": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app-data-root", type=Path, required=True)
    parser.add_argument("--expected-active-file", required=True)
    parser.add_argument("--expected-source-sha256", required=True)
    parser.add_argument("--expected-logical-sha256", required=True)
    parser.add_argument("--ack-app-stopped", action="store_true")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--dry-run", action="store_true")
    action.add_argument("--create", action="store_true")
    opts = parser.parse_args(argv)
    try:
        if not opts.ack_app_stopped:
            raise BackupStop("operator_must_acknowledge_app_stopped")
        report = perform(
            opts.app_data_root, opts.expected_active_file,
            opts.expected_source_sha256, opts.expected_logical_sha256,
            create=opts.create,
        )
    except (BackupStop, audit.AuditError, OSError, sqlite3.Error, ValueError) as exc:
        report = {
            "status": "FAIL",
            "reason": str(exc) if isinstance(exc, (BackupStop, audit.AuditError))
            else "operator_backup_or_rehearsal_error",
            "warning": "new_custody_files_if_any_preserved_for_inspection_no_cleanup",
        }
    print(json.dumps(report, sort_keys=True, ensure_ascii=True))
    return 0 if report["status"] in ("READY", "PASS") else 2


if __name__ == "__main__":
    sys.exit(main())
