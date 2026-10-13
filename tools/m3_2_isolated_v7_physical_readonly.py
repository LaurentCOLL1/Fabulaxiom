"""M3.2 Stage 18 — isolated M3.1 v7 physical SQLite read-only source candidate.

There is NO approval to run this candidate on the operator computer yet.
Only a previously SHA-pinned M3.1 *isolated* v7 source is eligible; normal
production v6 is never connected. No backup, migration, profile, ACL, or write.
"""
from __future__ import annotations

import argparse
from contextlib import closing
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import sys

import m3_1_v6_audit as v6
import m3_2_direct_custody_readonly as direct
import m3_2_independent_authority_gate as pins
from m3_2_operator_readonly_gate import GateStop, regular_safe

EXPECTED_V7_NAME = "007_create_world_time_foundation"
EXPECTED_LEDGER = list(enumerate((*v6.MIGRATION_NAMES, EXPECTED_V7_NAME), start=1))
EXPECTED_CANDIDATE_SHA = pins.PINNED_SHA256[("m31", "isolated_v7")]
EXPECTED_LEGACY_LOGICAL = (
    "38a610da9d6d9fcaa7842ebcbfa4f2c644d892c7968797de5f9ba21a258b2269"
)


def _reject_sidecars(path: Path) -> None:
    if any(os.path.lexists(str(path) + suffix)
           for suffix in ("-wal", "-shm", "-journal")):
        raise GateStop("isolated_v7_sqlite_sidecars_present")


def _snapshot_file(path: Path) -> tuple:
    regular_safe(path, False)
    info = path.stat()
    if not 0 < info.st_size <= 512 * 1024 * 1024:
        raise GateStop("isolated_v7_invalid_file_size")
    return (
        info.st_dev, info.st_ino, info.st_mode, info.st_size,
        info.st_mtime_ns, info.st_ctime_ns
    )


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _typed_v6_logical(conn: sqlite3.Connection) -> str:
    # Reuse the exact source-controlled M3.1 typed-row v1 algorithm.
    h = hashlib.sha256(b"fabulaxiom-v6-typed-row-sha256-v1\0")
    for table in v6.LEGACY_TABLES:
        _count, value = v6._logical_table(conn, table)
        h.update(table.encode("ascii") + b"\0" + bytes.fromhex(value))
    return h.hexdigest()


def inspect_file_readonly(
    file: Path, expected_file_sha256: str, expected_logical_sha256: str,
) -> dict:
    """Testable physical gate: synthetic disposable files ONLY until authorized."""
    if not file.is_absolute():
        raise GateStop("isolated_v7_file_path_not_absolute")
    if not all(
        isinstance(v, str) and len(v) == 64 and
        all(c in "0123456789abcdef" for c in v)
        for v in (expected_file_sha256, expected_logical_sha256)
    ):
        raise GateStop("isolated_v7_expected_digest_invalid")
    before_id = _snapshot_file(file)
    _reject_sidecars(file)
    with file.open("rb") as stream:
        header = stream.read(20)
    if len(header) != 20 or header[:16] != b"SQLite format 3\x00":
        raise GateStop("isolated_v7_invalid_sqlite_header")
    # Never open WAL-backed database: read-only connections may create SHM.
    if header[18:20] != b"\x01\x01":
        raise GateStop("isolated_v7_wal_or_unknown_header")
    before_hash = _sha256(file)
    if before_hash != expected_file_sha256:
        raise GateStop("isolated_v7_source_sha_mismatch")

    try:
        # mode=ro, no immutable=1. SQLite retains standard locking/change
        # detection, unlike immutable=1. The V7 isolated source stays protected.
        with closing(sqlite3.connect(
            file.as_uri() + "?mode=ro&cache=private", uri=True, timeout=0.0
        )) as con:
            con.execute("PRAGMA query_only=ON")
            con.execute("PRAGMA foreign_keys=ON")
            con.execute("PRAGMA temp_store=MEMORY")
            if con.execute("PRAGMA query_only").fetchone() != (1,):
                raise GateStop("isolated_v7_query_only_not_enabled")
            if con.execute("PRAGMA foreign_keys").fetchone() != (1,):
                raise GateStop("isolated_v7_foreign_keys_not_enabled")
            ledger = con.execute(
                "SELECT version,name FROM schema_migrations ORDER BY version"
            ).fetchall()
            if ledger != EXPECTED_LEDGER:
                raise GateStop("isolated_v7_migration_ledger_not_exact")
            owner = con.execute(
                "SELECT value FROM app_metadata WHERE key='schema_owner'"
            ).fetchone()
            if owner != ("fabulaxiom",):
                raise GateStop("isolated_v7_schema_owner_invalid")
            if con.execute("PRAGMA integrity_check").fetchall() != [("ok",)]:
                raise GateStop("isolated_v7_integrity_check_failed")
            if con.execute("PRAGMA foreign_key_check").fetchone() is not None:
                raise GateStop("isolated_v7_foreign_key_check_failed")
            for name in (*v6.LEGACY_TABLES, *v6.CANDIDATE_TABLES):
                entries = con.execute(
                    "SELECT type,strict FROM pragma_table_list "
                    "WHERE schema='main' AND name=?", (name,)
                ).fetchall()
                if entries != [("table", 1)]:
                    raise GateStop("isolated_v7_expected_strict_table_missing")
            for name in v6.CANDIDATE_TABLES:
                if con.execute('SELECT COUNT(*) FROM "' + name + '"').fetchone() != (0,):
                    raise GateStop("isolated_v7_candidate_table_not_empty")
            actual_logical = _typed_v6_logical(con)
            if actual_logical != expected_logical_sha256:
                raise GateStop("isolated_v7_legacy_logical_digest_mismatch")
    except sqlite3.Error as exc:
        raise GateStop("isolated_v7_sqlite_readonly_scan_failed") from exc

    _reject_sidecars(file)
    if _snapshot_file(file) != before_id or _sha256(file) != before_hash:
        raise GateStop("isolated_v7_changed_during_readonly_scan")
    return {
        "physical_integrity": "ok",
        "foreign_key_violations": 0,
        "schema_version": 7,
        "legacy_strict_tables": len(v6.LEGACY_TABLES),
        "candidate_strict_empty_tables": len(v6.CANDIDATE_TABLES),
        "typed_v6_logical_sha256_match": True,
        "isolated_source_sha256_match": True,
        "isolated_source_modified": False,
        "sqlite_opened_readonly": True,
        "sqlite_written": False,
    }


def inspect(
    source_repo: Path, expected_head: str, expected_main: str,
    production_root: Path, m25_root: Path, m31_root: Path, acl_root: Path,
    proposed_identity: str, app_stopped: bool,
    token_checker=direct.common.windows_standard_medium_token
) -> dict:
    # Mandatory full 26-role SHA, safe-path, detached source, medium token and
    # M1.5 active-marker checks BEFORE opening even the protected isolated v7.
    parent = direct.inspect(
        source_repo, expected_head, expected_main, production_root,
        m25_root, m31_root, acl_root, proposed_identity, app_stopped,
        token_checker=token_checker,
    )
    if parent["status"] != "PENDING_EXTERNAL_ATTESTATION":
        raise GateStop("isolated_v7_custody_prerequisite_not_pending")
    if m31_root.name != direct.M31_NAME:
        raise GateStop("isolated_v7_wrong_m31_identity")
    isolated = m31_root / pins.EXACT_PATHS[("m31", "isolated_v7")]
    verified = inspect_file_readonly(
        isolated, EXPECTED_CANDIDATE_SHA, EXPECTED_LEGACY_LOGICAL
    )
    return {
        **parent, **verified,
        "status": "PENDING_EXTERNAL_ATTESTATION",
        "mode": "m32_existing_isolated_v7_physical_readonly_candidate",
        "m32_staging_authorized": False,
        "operator_live_qualified": False,
        "sqlite_opened": True,
        "production_sqlite_opened": False,
        "production_migrated": False,
        "writes_performed": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in (
        "source-repo", "production-root", "m25-root", "m31-root", "acl-root"
    ):
        parser.add_argument("--" + name, type=Path, required=True)
    for name in ("expected-head", "expected-main", "proposed-identity"):
        parser.add_argument("--" + name, required=True)
    parser.add_argument("--ack-app-stopped", action="store_true")
    parser.add_argument("--dry-run", action="store_true", required=True)
    args = parser.parse_args(argv)
    try:
        report = inspect(
            args.source_repo, args.expected_head, args.expected_main,
            args.production_root, args.m25_root, args.m31_root,
            args.acl_root, args.proposed_identity, args.ack_app_stopped
        )
    except (GateStop, OSError, ValueError, TypeError) as exc:
        report = {
            "status": "FAIL",
            "reason": str(exc) if isinstance(exc, GateStop)
                      else "isolated_v7_physical_readonly_error",
            "m32_staging_authorized": False,
            "writes_performed": False,
        }
    print(json.dumps(report, sort_keys=True, ensure_ascii=True))
    # PENDING is not operator write authorization; both pending and FAIL exit 2.
    return 2


if __name__ == "__main__":
    sys.exit(main())
