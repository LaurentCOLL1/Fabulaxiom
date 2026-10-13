"""M3.2 stage 14: archived M3.1 manifest *semantic* cross-check (read-only).

This is not a SQLite audit or cryptographic signature of operator history.
There is no create/prepare/write action; status is always pending or FAIL.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import m3_2_independent_authority_gate as pinned
from m3_1_v6_audit import LEGACY_TABLES
from m3_2_operator_readonly_gate import GateStop, digest_file, regular_safe

SOURCE = pinned.PINNED_SHA256[("production", "active_v6")]
V6 = pinned.PINNED_SHA256[("production", "m31_v6_backup")]
V6_MANIFEST = pinned.PINNED_SHA256[("production", "m31_v6_manifest")]
V7 = pinned.PINNED_SHA256[("production", "m31_third_v7")]
SQL007 = "d66c26349e0bbfe0a9b9d610516c6ebe8d241d01f9506d0613f4152d25cd1212"
LOGICAL_V6 = "38a610da9d6d9fcaa7842ebcbfa4f2c644d892c7968797de5f9ba21a258b2269"
M31_ID = "com.fabulaxiom.m31launchdb8d3278504c448084478a70ccb71cbd"
EXPECTED_FILES = {
    "backup": ("production", "m31_v6_manifest"),
    "third": ("production", "m31_third_manifest"),
    "rollback": ("production", "m31_fourth_manifest"),
    "preparation": ("m31", "preparation_manifest"),
    "overlay": ("m31", "overlay"),
}


def require(value: bool, code: str) -> None:
    if not value:
        raise GateStop("m31_semantic_" + code)


def is_exact_int(value: object, expected: int) -> bool:
    return type(value) is int and value == expected


def child(obj: object, key: str) -> dict:
    require(isinstance(obj, dict) and isinstance(obj.get(key), dict),
            "missing_object_" + key)
    return obj[key]


def expect(obj: dict, key: str, expected: object) -> None:
    actual = obj.get(key)
    require(type(actual) is type(expected) and actual == expected, "invalid_" + key)


def validate_documents(docs: dict[str, dict], identity: str) -> dict:
    """Only prove consistency of previously SHA-checked JSON evidence."""
    require(set(docs) == set(EXPECTED_FILES), "document_set")
    require(identity == M31_ID, "isolated_identity")
    backup = docs["backup"]
    third = docs["third"]
    rollback = docs["rollback"]
    preparation = docs["preparation"]
    overlay = docs["overlay"]
    require(all(isinstance(v, dict) for v in docs.values()), "nonobject_document")

    expect(backup, "protocol", "m3_1_operator_pre_v7_v6_backup_and_restore_v1")
    source = child(backup, "source")
    expect(source, "active_file", Path(pinned.EXACT_PATHS[("production", "active_v6")]).name)
    expect(source, "sha256", SOURCE)
    expect(source, "logical_sha256", LOGICAL_V6)
    expect(source, "logical_algorithm", "fabulaxiom-v6-typed-row-sha256-v1")
    expect(source, "schema_version", 6)
    for key, name in (
        ("backup", "fabulaxiom-pre-m3-1-v6.sqlite3"),
        ("restore_rehearsal", "isolated-restore-rehearsal-v6.sqlite3")
    ):
        item = child(backup, key)
        expect(item, "file", name)
        expect(item, "sha256", V6)
        expect(item, "combined_logical_sha256", LOGICAL_V6)
        expect(item, "integrity", "ok")
        expect(item, "foreign_key_check", "ok")
        counts = item.get("legacy_table_counts")
        require(isinstance(counts, dict) and len(counts) == len(LEGACY_TABLES),
                key + "_table_count")
        require(set(counts) == set(LEGACY_TABLES), key + "_table_names")
        require(all(type(n) is int and n >= 0 for n in counts.values()),
                key + "_table_values")
        require(type(item.get("bytes")) is int and item["bytes"] > 0,
                key + "_file_bytes")
    saved = child(backup, "backup")
    restored = child(backup, "restore_rehearsal")
    require(saved["legacy_table_counts"] == restored["legacy_table_counts"],
            "backup_restore_table_inventory_mismatch")
    require(saved["bytes"] == restored["bytes"],
            "backup_restore_byte_count_mismatch")
    expect(backup, "active_pointer_modified", False)
    expect(backup, "migration_v7_executed", False)

    expect(third, "protocol", "m3_1_copy_only_v7_rehearsal_v1")
    expect(third, "candidate_sql_sha256", SQL007)
    expect(third, "source_production_sha256", SOURCE)
    expect(third, "source_v6_backup_sha256", V6)
    expect(third, "source_custody_manifest_sha256", V6_MANIFEST)
    expect(third, "baseline_legacy_logical_sha256", LOGICAL_V6)
    expect(third, "copy_file", "candidate-v7.sqlite3")
    copy = child(third, "copy")
    expect(copy, "schema_version", 7)
    expect(copy, "file_sha256", V7)
    expect(copy, "legacy_data_preserved", True)
    expect(copy, "new_tables_strict", 3)
    expect(copy, "new_tables_empty", 3)
    expect(copy, "integrity", "ok")
    expect(copy, "foreign_keys", "ok")
    expect(third, "v7_applied_to_disposable_copy_only", True)
    expect(third, "production_schema_version", 6)
    expect(third, "production_migrated", False)
    expect(third, "active_pointer_modified", False)

    expect(rollback, "protocol", "m3_1_fourth_copy_forced_rollback_v1")
    expect(rollback, "original_production_schema_version", 6)
    expect(rollback, "original_source_sha256", SOURCE)
    expect(rollback, "original_v6_backup_sha256", V6)
    expect(rollback, "original_v6_manifest_sha256", V6_MANIFEST)
    expect(rollback, "candidate_sql_sha256", SQL007)
    expect(rollback, "forced_sqlite_error", "SQLITE_CONSTRAINT_PRIMARYKEY")
    expect(rollback, "rolled_back_file", "failed-v7-rolled-back-v6.sqlite3")
    expect(rollback, "rolled_back_file_sha256", V6)
    expect(rollback, "rolled_back_schema_version", 6)
    expect(rollback, "legacy_logical_sha256", LOGICAL_V6)
    for flag in (
        "all_14_legacy_tables_preserved",
        "schema_inventory_identical_to_pre_failure",
        "fourth_copy_bytes_identical_to_pre_failure"
    ):
        expect(rollback, flag, True)
    expect(rollback, "production_migrated", False)
    expect(rollback, "active_pointer_modified", False)
    require(type(rollback.get("rolled_back_file_bytes")) is int and
            rollback["rolled_back_file_bytes"] > 0, "rollback_bytes")
    require(rollback["rolled_back_file_bytes"] == saved["bytes"],
            "rollback_backup_byte_count_mismatch")

    expect(preparation, "protocol", "m3_1_isolated_v7_launch_preparation_v1")
    expect(preparation, "identity", identity)
    expect(preparation, "expected_launch_behavior", "normal_v6_runtime_refuses_v7")
    expect(preparation, "source_production_schema_version", 6)
    expect(preparation, "copy_schema_version", 7)
    expect(preparation, "copy_file", "database/fabulaxiom.sqlite3")
    expect(preparation, "copy_sha256", V7)
    expect(preparation, "original_third_copy_sha256", V7)
    expect(preparation, "candidate_sql_sha256", SQL007)
    expect(preparation, "tauri_overlay_file", "tauri.m31.isolated.conf.json")
    expect(preparation, "tauri_overlay_sha256",
           pinned.PINNED_SHA256[("m31", "overlay")])
    expect(preparation, "tauri_launched", False)
    expect(preparation, "production_migrated", False)
    expect(preparation, "active_pointer_modified", False)

    expect(overlay, "identifier", identity)
    expect(overlay, "productName", "Fabulaxiom M3.1 Isolated")
    expect(child(overlay, "bundle"), "active", False)
    windows = child(overlay, "app").get("windows")
    require(isinstance(windows, list) and len(windows) == 1 and
            isinstance(windows[0], dict) and windows[0].get("label") == "main",
            "overlay_main_window")
    return {
        "semantic_m31_manifests_verified": 4,
        "semantic_m31_config_verified": True,
        "production_migration_authorized": False,
        "sqlite_integrity_retested": False,
    }


def read_anchored_document(root: Path, role: tuple[str, str]) -> dict:
    relative = pinned.EXACT_PATHS[role]
    path = root / relative
    regular_safe(path, False)
    if path.stat().st_size > 128 * 1024:
        raise GateStop("m31_semantic_document_oversize")
    expected = pinned.PINNED_SHA256[role]
    if digest_file(path) != expected:
        raise GateStop("m31_semantic_digest_before_changed")
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError) as exc:
        raise GateStop("m31_semantic_json_invalid") from exc
    if digest_file(path) != expected:
        raise GateStop("m31_semantic_digest_after_changed")
    if not isinstance(obj, dict):
        raise GateStop("m31_semantic_json_not_object")
    return obj


def inspect(
    source_repo: Path, expected_head: str, expected_main: str,
    production_root: Path, m25_root: Path, m31_root: Path, acl_root: Path,
    protected_manifest: Path, expected_manifest_sha256: str,
    proposed_identity: str, app_stopped: bool,
    token_checker=pinned.stage12.prior.windows_standard_medium_token
) -> dict:
    previous = pinned.inspect(
        source_repo, expected_head, expected_main, production_root,
        m25_root, m31_root, acl_root, protected_manifest,
        expected_manifest_sha256, proposed_identity, app_stopped,
        token_checker=token_checker
    )
    require(previous["status"] == "PENDING_EXTERNAL_ATTESTATION",
            "prior_authority_gate_not_pending")
    roots = {"production": production_root, "m31": m31_root}
    docs = {
        name: read_anchored_document(roots[role[0]], role)
        for name, role in EXPECTED_FILES.items()
    }
    verified = validate_documents(docs, m31_root.name)
    return {
        **previous, **verified,
        "status": "PENDING_EXTERNAL_ATTESTATION",
        "mode": "m32_m31_semantic_readonly_candidate",
        "m32_staging_authorized": False,
        "operator_live_qualified": False,
        "writes_performed": False,
        "sqlite_opened": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in (
        "source-repo", "production-root", "m25-root", "m31-root",
        "acl-root", "protected-manifest"
    ):
        parser.add_argument("--" + name, type=Path, required=True)
    for name in ("expected-head", "expected-main",
                 "expected-manifest-sha256", "proposed-identity"):
        parser.add_argument("--" + name, required=True)
    parser.add_argument("--ack-app-stopped", action="store_true")
    parser.add_argument("--dry-run", action="store_true", required=True)
    args = parser.parse_args(argv)
    try:
        output = inspect(
            args.source_repo, args.expected_head, args.expected_main,
            args.production_root, args.m25_root, args.m31_root, args.acl_root,
            args.protected_manifest, args.expected_manifest_sha256,
            args.proposed_identity, args.ack_app_stopped
        )
    except (GateStop, OSError, ValueError, TypeError) as exc:
        output = {
            "status": "FAIL",
            "reason": str(exc) if isinstance(exc, GateStop)
                      else "m31_semantic_readonly_error",
            "m32_staging_authorized": False,
            "writes_performed": False,
        }
    print(json.dumps(output, sort_keys=True, ensure_ascii=True))
    # Pending can never be used as a process-level success authorization.
    return 2


if __name__ == "__main__":
    sys.exit(main())
