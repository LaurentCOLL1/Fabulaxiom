"""M3.1 COPY-ONLY v6 -> candidate-v7 rehearsal. NEVER migrates production.

Dry-run is read-only and creates no files. --create makes one unique new
third-party rehearsal database derived from the verified pre-v7 BACKUP, never
from the active production SQLite nor the preserved restore-rehearsal file.
No Tauri migration registration or active pointer change. Python 3.12 stdlib.
"""
from __future__ import annotations

import argparse
from contextlib import closing
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
import sys
from uuid import uuid4

import m3_1_v6_audit as audit
import m3_1_v6_backup as v6backup

CUSTODY_FOLDER = re.compile(
    r"pre_v7_[0-9]{8}T[0-9]{6}Z-[0-9a-f]{32}\Z", re.ASCII
)
V7_NAME = "007_create_world_time_foundation"
NEW_TABLES = audit.CANDIDATE_TABLES


class RehearsalStop(Exception):
    pass


def _hash(s: str) -> str:
    if not re.fullmatch(r"[0-9a-f]{64}", s):
        raise RehearsalStop("expected_sha256_invalid")
    return s


def _inventory(db: sqlite3.Connection):
    return db.execute(
        "SELECT type,name,tbl_name,COALESCE(sql,'') FROM sqlite_schema "
        "WHERE name NOT LIKE 'sqlite_stat%' ORDER BY type,name,tbl_name,sql"
    ).fetchall()


def _migration_sql(db: sqlite3.Connection, sql: str) -> None:
    if db.execute("PRAGMA foreign_keys").fetchone() != (1,):
        raise RehearsalStop("foreign_keys_disabled")
    if db.execute("SELECT max(version) FROM schema_migrations").fetchone() != (6,):
        raise RehearsalStop("source_not_v6")
    try:
        # executescript commits any pre-existing transaction, so BEGIN/COMMIT
        # are embedded in the same script to atomically apply all v7 DDL and
        # its single registry row. No production connection ever calls this.
        db.executescript(
            "BEGIN IMMEDIATE;\n" + sql + "\n"
            "INSERT INTO schema_migrations(version,name) "
            "VALUES (7,'007_create_world_time_foundation');\nCOMMIT;"
        )
    except sqlite3.Error:
        if db.in_transaction:
            db.rollback()
        raise


def _expected_v7_inventory(backup: Path, sql: str):
    with closing(sqlite3.connect(
        backup.as_uri() + "?mode=ro", uri=True, timeout=0
    )) as source:
        with closing(sqlite3.connect(":memory:")) as reference:
            source.backup(reference)
            reference.execute("PRAGMA foreign_keys=ON")
            _migration_sql(reference, sql)
            return _inventory(reference)


def _validate_v7(path: Path, baseline: dict, expected_inventory) -> dict:
    audit._regular_file(path)
    audit._reject_sidecars(path)
    with closing(sqlite3.connect(
        path.as_uri() + "?mode=ro", uri=True, timeout=0
    )) as db:
        db.execute("PRAGMA query_only=ON")
        db.execute("PRAGMA foreign_keys=ON")
        if db.execute("PRAGMA foreign_keys").fetchone() != (1,):
            raise RehearsalStop("foreign_keys_disabled")
        rows = db.execute(
            "SELECT version,name FROM schema_migrations ORDER BY version"
        ).fetchall()
        if rows != list(enumerate(audit.MIGRATION_NAMES + (V7_NAME,), 1)):
            raise RehearsalStop("v7_lineage_mismatch")
        if _inventory(db) != expected_inventory:
            raise RehearsalStop("candidate_or_legacy_schema_ddl_drift")
        if db.execute("PRAGMA integrity_check").fetchall() != [("ok",)]:
            raise RehearsalStop("v7_integrity_failed")
        if db.execute("PRAGMA foreign_key_check").fetchone() is not None:
            raise RehearsalStop("v7_foreign_key_violations")
        if db.execute(
            "SELECT value FROM app_metadata WHERE key='schema_owner'"
        ).fetchone() != ("fabulaxiom",):
            raise RehearsalStop("schema_owner_changed")
        for table in audit.LEGACY_TABLES + NEW_TABLES:
            if db.execute(
                "SELECT type,strict FROM pragma_table_list "
                "WHERE schema='main' AND name=?", (table,),
            ).fetchall() != [("table", 1)]:
                raise RehearsalStop("missing_or_nonstrict_" + table)
        for table in NEW_TABLES:
            count = db.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
            if count != 0:
                raise RehearsalStop("unexpected_v7_content_" + table)
        logical = hashlib.sha256(b"fabulaxiom-v6-typed-row-sha256-v1\0")
        for table in audit.LEGACY_TABLES:
            count, digest = audit._logical_table(db, table)
            if table == "schema_migrations":
                # v7 adds exactly one ledger row; all SIX previous rows must
                # remain identical, checked here using a scoped comparison.
                original = db.execute(
                    "SELECT version,name FROM schema_migrations WHERE version<=6 "
                    "ORDER BY version"
                ).fetchall()
                if original != list(enumerate(audit.MIGRATION_NAMES, 1)):
                    raise RehearsalStop("legacy_migration_registry_mutated")
                continue
            if baseline["legacy_tables"][table] != {
                "rows": count, "logical_sha256": digest
            }:
                raise RehearsalStop("legacy_data_mismatch_" + table)
            logical.update(table.encode("ascii") + b"\0" + bytes.fromhex(digest))
        return {
            "schema_version": 7,
            "legacy_data_preserved": True,
            "new_tables_strict": 3,
            "new_tables_empty": 3,
            "integrity": "ok",
            "foreign_keys": "ok",
            "file_sha256": audit._file_sha256(path),
        }


def _custody(root: Path, relative: str) -> Path:
    # No absolute or traversal paths and no ambiguity about the owning app.
    p = Path(relative.replace("\\", "/"))
    if len(p.parts) != 3 or p.parts[:2] != (
        "operator-qualification", "m3_1"
    ) or not CUSTODY_FOLDER.fullmatch(p.parts[2]):
        raise RehearsalStop("invalid_custody_relative_path")
    path = root
    for part in p.parts:
        path = path / part
        audit._directory(path)
    return path


def perform(
    root: Path, relative: str, expected_active: str,
    expected_source: str, expected_logical: str,
    expected_backup: str, expected_manifest: str,
    candidate_sql_file: Path, expected_sql: str, create: bool,
) -> dict:
    for s in (expected_source, expected_logical, expected_backup,
              expected_manifest, expected_sql):
        _hash(s)
    if not audit.RESTORED.fullmatch(expected_active):
        raise RehearsalStop("unexpected_active_filename")
    if root.name != "com.fabulaxiom.desktop":
        raise RehearsalStop("unexpected_app_root")
    baseline = v6backup._check_baseline(
        root, expected_active, expected_source, expected_logical
    )
    folder = _custody(root, relative)
    backup_file = folder / "fabulaxiom-pre-m3-1-v6.sqlite3"
    restored = folder / "isolated-restore-rehearsal-v6.sqlite3"
    manifest_file = folder / "manifest.json"
    for item in (backup_file, restored, manifest_file, candidate_sql_file):
        audit._regular_file(item)
    if audit._file_sha256(candidate_sql_file) != expected_sql:
        raise RehearsalStop("candidate_sql_sha256_mismatch")
    if audit._file_sha256(manifest_file) != expected_manifest:
        raise RehearsalStop("custody_manifest_sha256_mismatch")
    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    if manifest.get("protocol") != "m3_1_operator_pre_v7_v6_backup_and_restore_v1":
        raise RehearsalStop("custody_protocol_mismatch")
    if manifest.get("source", {}).get("sha256") != expected_source:
        raise RehearsalStop("custody_source_sha256_mismatch")
    if manifest.get("source", {}).get("logical_sha256") != expected_logical:
        raise RehearsalStop("custody_source_logical_mismatch")
    for key, name in (
        ("backup", backup_file.name),
        ("restore_rehearsal", restored.name),
    ):
        item = manifest.get(key, {})
        if item.get("file") != name or item.get("sha256") != expected_backup:
            raise RehearsalStop("custody_"+key+"_mismatch")
    if audit._file_sha256(backup_file) != expected_backup:
        raise RehearsalStop("backup_bytes_changed")
    if audit._file_sha256(restored) != expected_backup:
        raise RehearsalStop("restore_bytes_changed")
    v6backup._validate_copy(backup_file, baseline)
    v6backup._validate_copy(restored, baseline)
    sql = candidate_sql_file.read_text(encoding="utf-8")
    if not create:
        return {
            "status": "READY", "mode": "read_only_copy_rehearsal_dry_run",
            "original_schema_version": 6,
            "backup_sha256": expected_backup,
            "candidate_sql_sha256": expected_sql,
            "source_unchanged": True, "migration_v7_executed": False,
        }

    # Never apply v7 SQL to the backup or restore rehearsal. Only a third,
    # newly created derivative in a sibling UUID-scoped directory may change.
    stage = root / "operator-qualification" / "m3_1"
    audit._directory(stage)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    new_name = "v7_copy_rehearsal_" + timestamp + "-" + uuid4().hex
    destination_dir = stage / new_name
    destination_dir.mkdir(exist_ok=False)
    destination = destination_dir / "candidate-v7.sqlite3"
    result_manifest = destination_dir / "candidate-v7-manifest.json"

    v6backup._snapshot(backup_file, destination)
    v6backup._validate_copy(destination, baseline)
    expected_ddl = _expected_v7_inventory(backup_file, sql)
    with closing(sqlite3.connect(destination)) as target:
        target.execute("PRAGMA foreign_keys=ON")
        _migration_sql(target, sql)
    result = _validate_v7(destination, baseline, expected_ddl)
    # Second idempotent validation is deliberately read-only; no SQL rerun.
    if _validate_v7(destination, baseline, expected_ddl) != result:
        raise RehearsalStop("v7_second_validation_changed")
    # Recheck all guarded inputs: production, restored original and custody.
    if v6backup._check_baseline(
        root, expected_active, expected_source, expected_logical
    ) != baseline:
        raise RehearsalStop("production_source_changed")
    if audit._file_sha256(backup_file) != expected_backup:
        raise RehearsalStop("original_v6_backup_changed")
    if audit._file_sha256(restored) != expected_backup:
        raise RehearsalStop("original_v6_restore_changed")
    if audit._file_sha256(manifest_file) != expected_manifest:
        raise RehearsalStop("original_v6_manifest_changed")
    if audit._file_sha256(candidate_sql_file) != expected_sql:
        raise RehearsalStop("candidate_sql_changed")
    record = {
        "protocol": "m3_1_copy_only_v7_rehearsal_v1",
        "candidate_sql_sha256": expected_sql,
        "source_production_sha256": expected_source,
        "source_v6_backup_sha256": expected_backup,
        "source_custody_manifest_sha256": expected_manifest,
        "baseline_legacy_logical_sha256": expected_logical,
        "copy_file": destination.name,
        "copy": result,
        "v7_applied_to_disposable_copy_only": True,
        "production_schema_version": 6,
        "production_migrated": False,
        "active_pointer_modified": False,
    }
    with result_manifest.open("x", encoding="utf-8", newline="\n") as out:
        json.dump(record, out, indent=2, sort_keys=True)
        out.write("\n")
        out.flush()
        os.fsync(out.fileno())
    if json.loads(result_manifest.read_text(encoding="utf-8")) != record:
        raise RehearsalStop("new_manifest_verify_failed")
    return {
        "status": "PASS", "mode": "v7_copy_only_rehearsal",
        "relative_rehearsal_dir": str(
            Path("operator-qualification") / "m3_1" / new_name
        ),
        "candidate_sha256": result["file_sha256"],
        "candidate_sql_sha256": expected_sql,
        "manifest_sha256": audit._file_sha256(result_manifest),
        "legacy_data_preserved": True,
        "source_unchanged": True,
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
    exclusive = parser.add_mutually_exclusive_group(required=True)
    exclusive.add_argument("--dry-run", action="store_true")
    exclusive.add_argument("--create", action="store_true")
    args = parser.parse_args(argv)
    try:
        if not args.ack_app_stopped:
            raise RehearsalStop("operator_must_acknowledge_app_stopped")
        report = perform(
            args.app_data_root, args.custody_relative_dir,
            args.expected_active_file, args.expected_source_sha256,
            args.expected_logical_sha256, args.expected_backup_sha256,
            args.expected_manifest_sha256, args.candidate_sql_file,
            args.expected_candidate_sql_sha256, args.create,
        )
    except (RehearsalStop, audit.AuditError, v6backup.BackupStop,
            OSError, ValueError, sqlite3.Error, json.JSONDecodeError) as exc:
        report = {
            "status": "FAIL",
            "reason": str(exc) if isinstance(exc, (
                RehearsalStop, audit.AuditError, v6backup.BackupStop
            )) else "copy_rehearsal_failure",
            "note": "retain_any_new_rehearsal_files_for_investigation",
        }
    print(json.dumps(report, sort_keys=True, ensure_ascii=True))
    return 0 if report["status"] in ("READY", "PASS") else 2


if __name__ == "__main__":
    sys.exit(main())
