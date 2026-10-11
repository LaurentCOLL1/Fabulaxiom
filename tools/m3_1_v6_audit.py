"""M3.1 fail-closed, operator-invoked read-only v6 audit.

This tool NEVER creates a backup, runs migrations, writes a report or changes
the active M1.5 pointer. Explicit --app-data-root and --ack-app-stopped required.
Python 3.12 standard library only. Output is JSON on stdout with no row values
or absolute operator paths. A PASS is NOT authorization to migrate to v7.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
import stat
import struct
import sys

MIGRATION_NAMES = (
    "001_create_app_metadata",
    "002_create_project_hierarchy",
    "003_create_scene_text_revisions",
    "004_create_narrative_entity_registry",
    "005_create_narrative_fact_provenance",
    "006_create_human_fact_review_log",
)
LEGACY_TABLES = (
    "app_metadata", "schema_migrations", "universes", "series", "novels",
    "chapters", "scenes", "scene_text_revisions", "scene_revision_heads",
    "narrative_entities", "entity_aliases", "narrative_facts",
    "fact_sources", "fact_review_events",
)
CANDIDATE_TABLES = (
    "fictional_calendars", "world_time_anchors", "world_time_precedences",
)
TOKEN = r"[0-9]{32}-[0-9]{10}-[0-9]{10}"
MARKER = re.compile(rf"activation-{TOKEN}\.active\Z", re.ASCII)
RESTORED = re.compile(rf"fabulaxiom-restored-{TOKEN}\.sqlite3\Z", re.ASCII)


class AuditError(Exception):
    pass


def _regular_file(path: Path) -> None:
    try:
        metadata = path.lstat()
    except OSError as exc:
        raise AuditError("file_missing_or_unreadable") from exc
    if not stat.S_ISREG(metadata.st_mode) or path.is_symlink():
        raise AuditError("nonregular_or_symlink_file")


def _directory(path: Path) -> None:
    try:
        metadata = path.lstat()
    except OSError as exc:
        raise AuditError("directory_missing_or_unreadable") from exc
    if (not stat.S_ISDIR(metadata.st_mode)
            or path.is_symlink()
            or getattr(path, "is_junction", lambda: False)()):
        raise AuditError("nonregular_or_redirected_directory")


def resolve_active(root: Path) -> tuple[Path, str]:
    """Mirror backup.rs M1.5 marker selection without creating anything."""
    if not root.is_absolute():
        raise AuditError("app_data_root_must_be_absolute")
    _directory(root)
    database = root / "database"
    _directory(database)
    markers_dir = database / "activations"
    selected = database / "fabulaxiom.sqlite3"
    if markers_dir.exists() or markers_dir.is_symlink():
        _directory(markers_dir)
        markers = sorted(
            (p for p in markers_dir.iterdir() if MARKER.fullmatch(p.name)),
            key=lambda p: p.name,
            reverse=True,
        )
        if markers:
            _regular_file(markers[0])
            try:
                active_name = markers[0].read_text(encoding="utf-8").strip()
            except (UnicodeError, OSError) as exc:
                raise AuditError("activation_marker_unreadable") from exc
            if not RESTORED.fullmatch(active_name):
                raise AuditError("activation_marker_invalid")
            selected = database / active_name
    _regular_file(selected)
    return selected, selected.name


def _snapshot_cell(value: object) -> str:
    if value is None:
        return "N"
    if isinstance(value, int):
        return "I:" + str(value)
    if isinstance(value, float):
        return "F:" + struct.pack(">d", value).hex()
    if isinstance(value, str):
        return "T:" + value.encode("utf-8").hex()
    if isinstance(value, bytes):
        return "B:" + value.hex()
    raise AuditError("unsupported_sqlite_value")


def _logical_table(conn: sqlite3.Connection, table: str) -> tuple[int, str]:
    if table not in LEGACY_TABLES:
        raise AuditError("unapproved_table_identifier")
    # All column values, including NULLs, are type-tagged; no values are printed.
    rows = [
        hashlib.sha256(json.dumps(
            [_snapshot_cell(cell) for cell in row],
            separators=(",", ":"), ensure_ascii=True,
        ).encode("ascii")).digest()
        for row in conn.execute(f'SELECT * FROM "{table}"')
    ]
    digest = hashlib.sha256()
    for row_hash in sorted(rows):
        digest.update(row_hash)
    return len(rows), digest.hexdigest()


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def audit(root: Path) -> dict:
    file, filename = resolve_active(root)

    # Operator must stop the application. Refuse any journal sidecars rather
    # than risk reading an uncheckpointed WAL or triggering SQLite side effects.
    if any(Path(str(file) + suffix).exists()
           for suffix in ("-wal", "-shm", "-journal")):
        raise AuditError("sqlite_sidecars_present_stop_without_deleting_them")

    try:
        # as_uri handles Windows drive paths and escaping. mode=ro NEVER creates
        # a missing database file; query_only protects against accidental writes.
        conn = sqlite3.connect(file.as_uri() + "?mode=ro", uri=True, timeout=0.0)
        try:
            conn.execute("PRAGMA query_only=ON")
            conn.execute("PRAGMA foreign_keys=ON")
            if conn.execute("PRAGMA foreign_keys").fetchone()[0] != 1:
                raise AuditError("foreign_keys_disabled")
            if conn.execute("PRAGMA query_only").fetchone()[0] != 1:
                raise AuditError("query_only_disabled")

            migration_rows = conn.execute(
                "SELECT version,name FROM schema_migrations ORDER BY version"
            ).fetchall()
            if migration_rows != list(enumerate(MIGRATION_NAMES, start=1)):
                raise AuditError("migration_registry_not_exact_v6")
            owner = conn.execute(
                "SELECT value FROM app_metadata WHERE key='schema_owner'"
            ).fetchone()
            if owner != ("fabulaxiom",):
                raise AuditError("schema_owner_invalid")
            if conn.execute("PRAGMA integrity_check").fetchone() != ("ok",):
                raise AuditError("sqlite_integrity_failed")
            if conn.execute("PRAGMA foreign_key_check").fetchone() is not None:
                raise AuditError("foreign_key_violation")

            for table in LEGACY_TABLES:
                rows = conn.execute(
                    "SELECT type,strict FROM pragma_table_list "
                    "WHERE schema='main' AND name=?", (table,)
                ).fetchall()
                if rows != [("table", 1)]:
                    raise AuditError("legacy_strict_table_missing")
            for table in CANDIDATE_TABLES:
                if conn.execute(
                    "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",
                    (table,),
                ).fetchone() is not None:
                    raise AuditError("premature_v7_candidate_detected")

            tables = {}
            overall = hashlib.sha256(b"fabulaxiom-v6-typed-row-sha256-v1\0")
            for table in LEGACY_TABLES:
                count, digest = _logical_table(conn, table)
                tables[table] = {"rows": count, "logical_sha256": digest}
                overall.update(table.encode("ascii") + b"\0" + bytes.fromhex(digest))
            return {
                "status": "PASS",
                "scope": "read_only_v6_preflight_not_migration_authority",
                "schema_version": 6,
                "active_file": filename,
                "legacy_tables": tables,
                "logical_digest_algorithm": "fabulaxiom-v6-typed-row-sha256-v1",
                "combined_logical_sha256": overall.hexdigest(),
                "closed_file_sha256": _file_sha256(file),
            }
        finally:
            conn.close()
    except sqlite3.Error as exc:
        raise AuditError("sqlite_read_or_validation_failed") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app-data-root", type=Path, required=True)
    parser.add_argument("--ack-app-stopped", action="store_true",
                        help="Operator assertion only: NOT an automatic process check")
    args = parser.parse_args(argv)
    try:
        if not args.ack_app_stopped:
            raise AuditError("operator_must_acknowledge_app_stopped")
        report = audit(args.app_data_root)
    except (AuditError, OSError, ValueError) as exc:
        report = {"status": "FAIL", "reason": (
            str(exc) if isinstance(exc, AuditError) else "read_only_audit_error"
        )}
    print(json.dumps(report, ensure_ascii=True, sort_keys=True))
    return 0 if report["status"] == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
