"""M3.2 stage 12: multi-root *read-only* custody audit, source candidate only.

This tool performs no preparation, SQLite connection, Tauri launch or write.
An operator-supplied digest is NEVER proof of its own historical authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys

import m3_2_operator_readonly_gate as prior

PROTOCOL = "fabulaxiom_m32_multiroot_custody_v1"
M31_ID = re.compile(r"com\.fabulaxiom\.m31launch[0-9a-f]{32}\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
MARKER = re.compile(r"database/activations/activation-[0-9]{32}-[0-9]{10}-[0-9]{10}\.active\Z")
ACTIVE = re.compile(r"database/fabulaxiom-restored-[0-9]{32}-[0-9]{10}-[0-9]{10}\.sqlite3\Z")

# Exact role coverage is required. No SHA-only lookup: two distinct historical
# backup names may (and in the real acceptance do) have identical content.
ROLES = {
    "production": frozenset((
        "active_v6", "activation_marker", "pre_m21_v3", "pre_m23_v4",
        "pre_m23_manifest", "pre_m24_v5", "pre_m24_manifest",
        "pre_m24_early_v5", "pre_m24_early_manifest",
        "app_backup_a", "app_backup_b", "m31_v6_backup",
        "m31_v6_restore", "m31_v6_manifest", "m31_third_v7",
        "m31_third_manifest", "m31_fourth_v6", "m31_fourth_manifest",
    )),
    "m25": frozenset(("isolated_v6", "pre_m25_v6", "pre_m25_manifest")),
    "m31": frozenset(("isolated_v7", "overlay", "preparation_manifest")),
    "acl": frozenset(("original_acls", "pre_repair_json")),
}
SQLITE_ROLES = frozenset((
    "active_v6", "pre_m21_v3", "pre_m23_v4", "pre_m24_v5",
    "pre_m24_early_v5", "app_backup_a", "app_backup_b",
    "m31_v6_backup", "m31_v6_restore", "m31_third_v7",
    "m31_fourth_v6", "isolated_v6", "pre_m25_v6", "isolated_v7",
))
ALLOWED_AUTHORITIES = frozenset(("historical", "observed"))


def _manifest_read(path: Path, expected_sha: str) -> dict:
    prior.regular_safe(path, False)
    if path.stat().st_size > 128 * 1024 or not HEX64.fullmatch(expected_sha):
        raise prior.GateStop("multi_root_manifest_size_or_digest_invalid")
    if prior.digest_file(path) != expected_sha:
        raise prior.GateStop("multi_root_manifest_sha_mismatch")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError) as exc:
        raise prior.GateStop("multi_root_manifest_invalid_json") from exc
    if not isinstance(data, dict) or set(data) != {
        "protocol", "expected_head", "expected_main", "protected_files"
    } or data["protocol"] != PROTOCOL:
        raise prior.GateStop("multi_root_manifest_protocol_invalid")
    return data


def inspect(
    source_repo: Path, expected_head: str, expected_main: str,
    production_root: Path, m25_root: Path, m31_root: Path, acl_root: Path,
    protected_manifest: Path, expected_manifest_sha256: str,
    proposed_identity: str, app_stopped: bool,
    token_checker=prior.windows_standard_medium_token,
) -> dict:
    if not app_stopped:
        raise prior.GateStop("operator_app_stopped_ack_required")
    if not prior._HEX40.fullmatch(expected_head) or not prior._HEX40.fullmatch(expected_main):
        raise prior.GateStop("invalid_expected_source_sha")
    if not prior._M32_ID.fullmatch(proposed_identity):
        raise prior.GateStop("unapproved_m32_identity")
    if not token_checker():
        raise prior.GateStop("standard_medium_token_unconfirmed")

    prior.regular_safe(source_repo, True)
    if prior.git_value(source_repo, "rev-parse", "HEAD") != expected_head:
        raise prior.GateStop("git_head_not_exact")
    if prior.git_value(source_repo, "rev-parse", "refs/remotes/origin/main") != expected_main:
        raise prior.GateStop("remote_main_not_exact_refetch_required")
    if prior.git_value(source_repo, "status", "--porcelain", "--untracked-files=all"):
        raise prior.GateStop("git_worktree_not_clean")

    roots = {
        "production": production_root,
        "m25": m25_root,
        "m31": m31_root,
        "acl": acl_root,
    }
    if (
        production_root.name != "com.fabulaxiom.desktop"
        or m25_root.name != "com.fabulaxiom.m25qual35fb842c"
        or not M31_ID.fullmatch(m31_root.name)
        or acl_root.name != "Fabulaxiom-M31-ACL-Evidence-4d520e18"
    ):
        raise prior.GateStop("unapproved_custody_root_identity")
    if (
        production_root.parent != m25_root.parent
        or production_root.parent != m31_root.parent
        or not all(root.is_absolute() for root in roots.values())
    ):
        raise prior.GateStop("unapproved_custody_root_location")
    for root in roots.values():
        prior.regular_safe(root, True)
    if os.path.lexists(production_root.parent / proposed_identity):
        raise prior.GateStop("proposed_identity_already_exists")

    manifest = _manifest_read(protected_manifest, expected_manifest_sha256)
    if manifest["expected_head"] != expected_head or manifest["expected_main"] != expected_main:
        raise prior.GateStop("multi_root_manifest_git_sha_mismatch")
    records = manifest["protected_files"]
    total_roles = sum(map(len, ROLES.values()))
    if not isinstance(records, list) or len(records) != total_roles:
        raise prior.GateStop("multi_root_required_file_set_incomplete")

    seen_paths: set[str] = set()
    roles_seen: dict[str, set[str]] = {name: set() for name in ROLES}
    authority_counts = {"historical": 0, "observed": 0}
    inspected: dict[str, dict[str, Path]] = {name: {} for name in ROLES}

    for item in records:
        if not isinstance(item, dict) or set(item) != {
            "root", "role", "path", "sha256", "authority"
        }:
            raise prior.GateStop("multi_root_manifest_item_invalid")
        root_id, role = item["root"], item["role"]
        if root_id not in ROLES or role not in ROLES[root_id]:
            raise prior.GateStop("multi_root_unapproved_role")
        if role in roles_seen[root_id]:
            raise prior.GateStop("multi_root_duplicate_role")
        relative, digest, authority = item["path"], item["sha256"], item["authority"]
        if not isinstance(relative, str) or ":" in relative or "\x00" in relative:
            raise prior.GateStop("multi_root_relative_path_invalid")
        if not isinstance(digest, str) or not HEX64.fullmatch(digest):
            raise prior.GateStop("multi_root_digest_invalid")
        if authority not in ALLOWED_AUTHORITIES:
            raise prior.GateStop("multi_root_authority_invalid")
        if root_id == "production" and role == "active_v6" and not ACTIVE.fullmatch(relative):
            raise prior.GateStop("multi_root_active_v6_name_invalid")
        if root_id == "production" and role == "activation_marker" and not MARKER.fullmatch(relative):
            raise prior.GateStop("multi_root_activation_marker_name_invalid")
        if role in SQLITE_ROLES and not relative.endswith(".sqlite3"):
            raise prior.GateStop("multi_root_sqlite_role_invalid")
        if role == "original_acls" and relative != "original-acls.txt":
            raise prior.GateStop("multi_root_acl_archive_name_invalid")
        if role == "pre_repair_json" and relative != "pre-repair-evidence.json":
            raise prior.GateStop("multi_root_acl_json_name_invalid")

        candidate = prior.safe_relative_file(roots[root_id], relative)
        key = os.path.normcase(str(candidate.absolute())).casefold()
        if key in seen_paths:
            raise prior.GateStop("multi_root_duplicate_file")
        seen_paths.add(key)
        prior.regular_safe(candidate, False)
        if prior.digest_file(candidate) != digest:
            raise prior.GateStop("multi_root_protected_file_digest_changed")
        if role in SQLITE_ROLES and any(
            os.path.lexists(str(candidate) + suffix)
            for suffix in ("-wal", "-shm", "-journal")
        ):
            raise prior.GateStop("multi_root_sqlite_sidecar_present")

        roles_seen[root_id].add(role)
        inspected[root_id][role] = candidate
        authority_counts[authority] += 1

    if any(roles_seen[root] != ROLES[root] for root in ROLES):
        raise prior.GateStop("multi_root_required_roles_missing")

    # The genuine M1.5 marker must select the protected restored-active name.
    marker = inspected["production"]["activation_marker"]
    active = inspected["production"]["active_v6"]
    try:
        selected = marker.read_text(encoding="utf-8").strip()
    except (OSError, UnicodeError) as exc:
        raise prior.GateStop("multi_root_marker_unreadable") from exc
    if selected != active.name:
        raise prior.GateStop("multi_root_activation_mismatch")

    # Only inspect the archived metadata; never apply an archived ACL.
    try:
        acl_metadata = json.loads(
            inspected["acl"]["pre_repair_json"].read_text(encoding="utf-8")
        )
    except (OSError, UnicodeError, ValueError) as exc:
        raise prior.GateStop("multi_root_acl_metadata_invalid") from exc
    if not isinstance(acl_metadata, dict) or (
        acl_metadata.get("identity") != m31_root.name
        or acl_metadata.get("original_owner_sid") != "S-1-5-32-544"
        or not isinstance(acl_metadata.get("original_sddl"), str)
        or not acl_metadata.get("original_sddl")
    ):
        raise prior.GateStop("multi_root_acl_metadata_mismatch")

    # This status is NOT a staging or write grant. Observed-only hashes
    # explicitly prevent even the more limited 'verified-scope' status.
    status = "PENDING_HISTORICAL_AUTHORITY" if authority_counts["observed"] else "VERIFIED_SCOPE_ONLY"
    return {
        "status": status,
        "mode": "m32_multi_root_readonly_source_candidate",
        "source_head": expected_head,
        "origin_main": expected_main,
        "file_count": total_roles,
        "root_count": len(roots),
        "authority_counts": authority_counts,
        "sqlite_opened": False,
        "writes_performed": False,
        "tauri_launched": False,
        "production_migrated": False,
        "m32_staging_authorized": False,
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source-repo", type=Path, required=True)
    p.add_argument("--expected-head", required=True)
    p.add_argument("--expected-main", required=True)
    p.add_argument("--production-root", type=Path, required=True)
    p.add_argument("--m25-root", type=Path, required=True)
    p.add_argument("--m31-root", type=Path, required=True)
    p.add_argument("--acl-root", type=Path, required=True)
    p.add_argument("--protected-manifest", type=Path, required=True)
    p.add_argument("--expected-manifest-sha256", required=True)
    p.add_argument("--proposed-identity", required=True)
    p.add_argument("--ack-app-stopped", action="store_true")
    p.add_argument("--dry-run", action="store_true", required=True)
    args = p.parse_args(argv)
    try:
        result = inspect(
            args.source_repo, args.expected_head, args.expected_main,
            args.production_root, args.m25_root, args.m31_root, args.acl_root,
            args.protected_manifest, args.expected_manifest_sha256,
            args.proposed_identity, args.ack_app_stopped,
        )
    except (prior.GateStop, OSError, ValueError, TypeError) as exc:
        result = {
            "status": "FAIL",
            "reason": str(exc) if isinstance(exc, prior.GateStop)
                      else "multi_root_readonly_probe_error",
            "writes_performed": False,
            "m32_staging_authorized": False,
        }
    print(json.dumps(result, sort_keys=True, ensure_ascii=True))
    return 0 if result["status"] == "VERIFIED_SCOPE_ONLY" else 2


if __name__ == "__main__":
    sys.exit(main())
