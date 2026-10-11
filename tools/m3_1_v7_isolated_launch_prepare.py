"""Prepare a UNIQUE isolated Tauri v7 refusal-launch fixture, without launching it.

Production M1.5 v6 and the original third/fourth operator copies are NEVER
opened writable. The preparer first requires the already-qualified read-only
third-copy / RAM audit; --dry-run does not write anything. Explicit --prepare
creates a new app identifier and makes exactly one isolated copied v7 database
and a Tauri --config JSON overlay in the new app-local-data root.

This is NOT a successful v7 application startup or a production migration.
Current Fabulaxiom normal v6 backend is expected to REFUSE a v7 database.
"""
from __future__ import annotations

import argparse
from contextlib import closing
import json
from pathlib import Path
import re
import shutil
import sqlite3
import sys
from uuid import uuid4

import m3_1_v6_audit as audit
import m3_1_v6_backup as backup
import m3_1_v7_copy_rehearsal as copy_v7
import m3_1_v7_final_readonly as final


class IsolatedLaunchStop(Exception):
    pass


def _check_isolated_copy(path: Path, expected_sha: str) -> None:
    audit._regular_file(path)
    audit._reject_sidecars(path)
    if audit._file_sha256(path) != expected_sha:
        raise IsolatedLaunchStop("isolated_copy_sha_mismatch")
    with closing(sqlite3.connect(path.as_uri() + "?mode=ro", uri=True, timeout=0)) as db:
        db.execute("PRAGMA query_only=ON")
        db.execute("PRAGMA foreign_keys=ON")
        if db.execute("PRAGMA foreign_keys").fetchone() != (1,):
            raise IsolatedLaunchStop("isolated_foreign_keys_disabled")
        ledger = db.execute(
            "SELECT version,name FROM schema_migrations ORDER BY version"
        ).fetchall()
        if ledger != list(enumerate(
            (*audit.MIGRATION_NAMES, "007_create_world_time_foundation"), 1
        )):
            raise IsolatedLaunchStop("isolated_copy_v7_ledger_wrong")
        if db.execute("PRAGMA integrity_check").fetchall() != [("ok",)]:
            raise IsolatedLaunchStop("isolated_integrity_failed")
        if db.execute("PRAGMA foreign_key_check").fetchone():
            raise IsolatedLaunchStop("isolated_foreign_keys_failed")
        for table in audit.CANDIDATE_TABLES:
            if db.execute(
                "SELECT type,strict FROM pragma_table_list "
                "WHERE schema='main' AND name=?", (table,),
            ).fetchall() != [("table", 1)]:
                raise IsolatedLaunchStop("isolated_v7_table_missing")
            if db.execute('SELECT COUNT(*) FROM "' + table + '"').fetchone() != (0,):
                raise IsolatedLaunchStop("isolated_candidate_not_empty")


def perform(
    root: Path, custody: str, third: str, active: str, source_sha: str,
    logical_sha: str, backup_sha: str, custody_manifest_sha: str,
    third_sha: str, third_manifest_sha: str, sql_file: Path,
    sql_sha: str, prepare: bool,
) -> dict:
    # No path may be created before the operator's exact-source and all
    # protected production/backup/third-v7 SHA, M1.5 and RAM gates pass.
    qualified = final.perform(
        root, custody, third, active, source_sha, logical_sha, backup_sha,
        custody_manifest_sha, third_sha, third_manifest_sha, sql_file, sql_sha
    )
    if qualified["status"] != "PASS" or qualified["constraint_scenarios_passed"] != 10:
        raise IsolatedLaunchStop("final_readonly_v7_audit_not_passed")

    parent = root.parent
    audit._directory(parent)
    if not root.name == "com.fabulaxiom.desktop":
        raise IsolatedLaunchStop("production_root_identity_wrong")
    if not prepare:
        return {
            "status": "READY",
            "mode": "isolated_v7_launch_dry_run",
            "third_candidate_sha256": third_sha,
            "source_schema_version": 6,
            "candidate_schema_version": 7,
            "isolated_identity_created": False,
            "tauri_launched": False,
            "production_migrated": False,
        }

    original = final._third_folder(root, third) / "candidate-v7.sqlite3"
    if audit._file_sha256(original) != third_sha:
        raise IsolatedLaunchStop("candidate_changed_before_copy")
    new_id = "com.fabulaxiom.m31launch" + uuid4().hex
    if not re.fullmatch(r"com\.fabulaxiom\.m31launch[0-9a-f]{32}", new_id):
        raise IsolatedLaunchStop("bad_isolated_identity")
    destination = parent / new_id
    # No reuse of an old identity, historical M2.5 worktree, or old user DB.
    destination.mkdir(mode=0o700, exist_ok=False)
    database_dir = destination / "database"
    database_dir.mkdir(exist_ok=False)
    isolated = database_dir / "fabulaxiom.sqlite3"
    try:
        with original.open("rb") as input_file, isolated.open("xb") as output_file:
            shutil.copyfileobj(input_file, output_file, length=1024 * 256)
        _check_isolated_copy(isolated, third_sha)
        if audit._file_sha256(original) != third_sha:
            raise IsolatedLaunchStop("original_third_copy_changed_after_copy")

        overlay = {
            "productName": "Fabulaxiom M3.1 Isolated",
            "identifier": new_id,
            "app": {
                "windows": [{
                    "label": "main",
                    "title": "Fabulaxiom M3.1 - ISOLATED v7 refusal check",
                    "width": 1100, "height": 720,
                    "minWidth": 800, "minHeight": 560,
                }],
            },
            "bundle": {"active": False},
        }
        config = destination / "tauri.m31.isolated.conf.json"
        with config.open("x", encoding="utf-8", newline="\n") as stream:
            json.dump(overlay, stream, sort_keys=True, indent=2)
            stream.write("\n")
        metadata = {
            "protocol": "m3_1_isolated_v7_launch_preparation_v1",
            "identity": new_id,
            "expected_launch_behavior": "normal_v6_runtime_refuses_v7",
            "source_production_schema_version": 6,
            "copy_schema_version": 7,
            "copy_file": "database/fabulaxiom.sqlite3",
            "copy_sha256": third_sha,
            "original_third_copy_sha256": third_sha,
            "candidate_sql_sha256": sql_sha,
            "tauri_overlay_file": config.name,
            "tauri_overlay_sha256": audit._file_sha256(config),
            "tauri_launched": False,
            "production_migrated": False,
            "active_pointer_modified": False,
        }
        manifest = destination / "preparation-manifest.json"
        with manifest.open("x", encoding="utf-8", newline="\n") as stream:
            json.dump(metadata, stream, sort_keys=True, indent=2)
            stream.write("\n")
        if json.loads(manifest.read_text(encoding="utf-8")) != metadata:
            raise IsolatedLaunchStop("manifest_roundtrip_failed")
        if audit._file_sha256(original) != third_sha:
            raise IsolatedLaunchStop("third_copy_changed_after_stage")
        if final.perform(
            root, custody, third, active, source_sha, logical_sha, backup_sha,
            custody_manifest_sha, third_sha, third_manifest_sha, sql_file, sql_sha
        )["status"] != "PASS":
            raise IsolatedLaunchStop("protected_custody_changed_after_stage")
        return {
            "status": "PASS",
            "mode": "isolated_v7_launch_prepared_not_launched",
            "identity": new_id,
            "isolated_database_sha256": audit._file_sha256(isolated),
            "overlay_sha256": audit._file_sha256(config),
            "manifest_sha256": audit._file_sha256(manifest),
            "tauri_launched": False,
            "production_migrated": False,
            "active_pointer_modified": False,
        }
    except Exception:
        # Preserve the exact new UUID-scoped directory for failure inspection.
        # Never delete, rename, repair, or overwrite any protected old input.
        raise


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--app-data-root", type=Path, required=True)
    p.add_argument("--custody-relative-dir", required=True)
    p.add_argument("--third-relative-dir", required=True)
    p.add_argument("--expected-active-file", required=True)
    p.add_argument("--expected-source-sha256", required=True)
    p.add_argument("--expected-logical-sha256", required=True)
    p.add_argument("--expected-backup-sha256", required=True)
    p.add_argument("--expected-custody-manifest-sha256", required=True)
    p.add_argument("--expected-third-sha256", required=True)
    p.add_argument("--expected-third-manifest-sha256", required=True)
    p.add_argument("--candidate-sql-file", type=Path, required=True)
    p.add_argument("--expected-candidate-sql-sha256", required=True)
    p.add_argument("--ack-app-stopped", action="store_true")
    action = p.add_mutually_exclusive_group(required=True)
    action.add_argument("--dry-run", action="store_true")
    action.add_argument("--prepare", action="store_true")
    opts = p.parse_args(argv)
    try:
        if not opts.ack_app_stopped:
            raise IsolatedLaunchStop("operator_must_acknowledge_app_stopped")
        result = perform(
            opts.app_data_root, opts.custody_relative_dir,
            opts.third_relative_dir, opts.expected_active_file,
            opts.expected_source_sha256, opts.expected_logical_sha256,
            opts.expected_backup_sha256, opts.expected_custody_manifest_sha256,
            opts.expected_third_sha256, opts.expected_third_manifest_sha256,
            opts.candidate_sql_file, opts.expected_candidate_sql_sha256,
            opts.prepare,
        )
    except (
        IsolatedLaunchStop, final.FinalAuditStop, audit.AuditError,
        backup.BackupStop, copy_v7.RehearsalStop, OSError,
        sqlite3.Error, ValueError, json.JSONDecodeError,
    ) as error:
        result = {
            "status": "FAIL",
            "reason": str(error) if isinstance(error, (
                IsolatedLaunchStop, final.FinalAuditStop, audit.AuditError,
                backup.BackupStop, copy_v7.RehearsalStop,
            )) else "isolated_preparation_error",
            "note": "preserve_any_new_identity_files_no_cleanup",
        }
    print(json.dumps(result, sort_keys=True, ensure_ascii=True))
    return 0 if result["status"] in ("READY", "PASS") else 2


if __name__ == "__main__":
    sys.exit(main())
