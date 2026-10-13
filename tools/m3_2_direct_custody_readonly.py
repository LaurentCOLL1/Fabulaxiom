"""M3.2 stage 16: source-anchored, manifest-free four-root READ-ONLY audit.

No operator-generated trust manifest required. Pinned digests are from checked-in
historical qualification, not from the files this audit reads. Recent/unanchored
evidence NEVER becomes historically trusted. No SQLite connections or writes.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys

import m3_2_independent_authority_gate as authority
import m3_2_multiroot_readonly as multi
from m3_2_operator_readonly_gate import GateStop
import m3_2_operator_readonly_gate as common

M31_NAME = "com.fabulaxiom.m31launchdb8d3278504c448084478a70ccb71cbd"
M25_NAME = "com.fabulaxiom.m25qual35fb842c"
ACL_NAME = "Fabulaxiom-M31-ACL-Evidence-4d520e18"


def check_roots(
    production_root: Path, m25_root: Path, m31_root: Path, acl_root: Path,
    proposed_identity: str,
) -> dict[str, Path]:
    roots = {
        "production": production_root, "m25": m25_root,
        "m31": m31_root, "acl": acl_root,
    }
    if (
        production_root.name != "com.fabulaxiom.desktop"
        or m25_root.name != M25_NAME
        or m31_root.name != M31_NAME
        or acl_root.name != ACL_NAME
        or production_root.parent != m25_root.parent
        or production_root.parent != m31_root.parent
        or not all(x.is_absolute() for x in roots.values())
    ):
        raise GateStop("direct_custody_root_identity_invalid")
    for directory in roots.values():
        common.regular_safe(directory, True)
    if os.path.lexists(production_root.parent / proposed_identity):
        raise GateStop("direct_proposed_identity_occupied")
    return roots


def source_paths(roots: dict[str, Path]) -> dict[tuple[str, str], Path]:
    """Bind each role to a source-defined name, never search by SHA alone."""
    expected = authority.ALL_ROLES
    paths = {
        key: roots[key[0]] / relative
        for key, relative in authority.EXACT_PATHS.items()
    }
    folder = roots["production"] / "operator-qualification" / "m2_3"
    common.regular_safe(folder, True)
    # Original v4 name is not specified in the saved source document.
    # Select by strict historic basename shape, never by a matching SHA in
    # arbitrary custody directories or from a user-supplied manifest.
    matches = sorted(
        p for p in folder.iterdir()
        if p.is_file() and authority.VARIABLE_PATHS[
            ("production", "pre_m23_v4")
        ].fullmatch(p.relative_to(roots["production"]).as_posix())
    )
    if len(matches) != 1:
        raise GateStop("direct_pre_m23_exact_v4_name_not_unique")
    v4 = matches[0]
    paths[("production", "pre_m23_v4")] = v4
    paths[("production", "pre_m23_manifest")] = v4.with_name(
        v4.name + ".manifest.json"
    )
    if set(paths) != expected:
        raise GateStop("direct_required_roles_incomplete")
    names = [str(path.absolute()).casefold() for path in paths.values()]
    if len(names) != len(set(names)):
        raise GateStop("direct_duplicate_file_path")
    return paths


def enforce_activation_inventory(paths: dict[tuple[str, str], Path]) -> None:
    """Reject any activation pointer not accounted for by M1.5 historic custody.

    Runtime M1.5 chooses a marker from its activation directory, so checking
    only the SHA of one old marker is not sufficient if a newer one exists.
    This function reads names and file metadata only; never opens SQLite.
    """
    marker = paths[("production", "activation_marker")]
    folder = marker.parent
    common.regular_safe(folder, True)
    candidates = [
        path for path in folder.iterdir()
        if path.name.lower().startswith("activation-")
        or path.name.lower().endswith(".active")
    ]
    if len(candidates) != 1 or candidates[0].name != marker.name:
        raise GateStop("direct_unexpected_activation_marker_inventory")
    common.regular_safe(marker, False)


def inspect(
    source_repo: Path, expected_head: str, expected_main: str,
    production_root: Path, m25_root: Path, m31_root: Path, acl_root: Path,
    proposed_identity: str, app_stopped: bool,
    token_checker=common.windows_standard_medium_token,
) -> dict:
    if not app_stopped:
        raise GateStop("direct_operator_app_stopped_ack_required")
    if not common._HEX40.fullmatch(expected_head) or not common._HEX40.fullmatch(expected_main):
        raise GateStop("direct_source_sha_invalid")
    if not common._M32_ID.fullmatch(proposed_identity):
        raise GateStop("direct_proposed_identity_invalid")
    if not token_checker():
        raise GateStop("direct_standard_medium_token_required")
    common.regular_safe(source_repo, True)
    if common.git_value(source_repo, "rev-parse", "HEAD") != expected_head:
        raise GateStop("direct_source_head_mismatch")
    if common.git_value(source_repo, "rev-parse", "refs/remotes/origin/main") != expected_main:
        raise GateStop("direct_origin_main_stale")
    if common.git_value(source_repo, "status", "--porcelain", "--untracked-files=all"):
        raise GateStop("direct_dirty_source")
    roots = check_roots(
        production_root, m25_root, m31_root, acl_root, proposed_identity
    )
    paths = source_paths(roots)
    enforce_activation_inventory(paths)

    seen_counts = {"historical_pinned": 0, "recent_observation": 0, "unanchored_observation": 0}
    initial_digests: dict[tuple[str, str], str] = {}
    for key in sorted(authority.ALL_ROLES):
        path = paths[key]
        common.regular_safe(path, False)
        if path.stat().st_size > 512 * 1024 * 1024:
            raise GateStop("direct_excessive_file_size")
        first = common.digest_file(path)
        second = common.digest_file(path)
        if first != second:
            raise GateStop("direct_during_read_content_change")
        initial_digests[key] = first
        if key in authority.PINNED_SHA256:
            if first != authority.PINNED_SHA256[key]:
                raise GateStop("direct_historical_pin_mismatch")
            seen_counts["historical_pinned"] += 1
        elif key in authority.OBSERVED_SHA256:
            if first != authority.OBSERVED_SHA256[key]:
                raise GateStop("direct_recent_observation_mismatch")
            seen_counts["recent_observation"] += 1
        elif key in authority.UNANCHORED_OBSERVED:
            seen_counts["unanchored_observation"] += 1
        else:
            raise GateStop("direct_unclassified_role")
        if key[1] in multi.SQLITE_ROLES and any(
            os.path.lexists(str(path) + ext)
            for ext in ("-wal", "-shm", "-journal")
        ):
            raise GateStop("direct_sqlite_sidecar_present")

    marker = paths[("production", "activation_marker")]
    active = paths[("production", "active_v6")]
    try:
        selected = marker.read_text(encoding="utf-8").strip()
    except (OSError, UnicodeError) as exc:
        raise GateStop("direct_active_marker_unreadable") from exc
    if selected != active.name or common.digest_file(marker) != initial_digests[
        ("production", "activation_marker")
    ]:
        raise GateStop("direct_m15_active_selection_changed")
    pre_repair = paths[("acl", "pre_repair_json")]
    try:
        metadata = json.loads(pre_repair.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError) as exc:
        raise GateStop("direct_acl_archive_json_invalid") from exc
    if (
        not isinstance(metadata, dict)
        or metadata.get("identity") != m31_root.name
        or metadata.get("original_owner_sid") != "S-1-5-32-544"
        or not isinstance(metadata.get("original_sddl"), str)
        or not metadata["original_sddl"]
        or common.digest_file(pre_repair) != initial_digests[
            ("acl", "pre_repair_json")
        ]
    ):
        raise GateStop("direct_acl_archive_metadata_mismatch")

    # Recheck enumeration after hashing and marker/ACL metadata reads, so a
    # new activation entry introduced during the audit cannot be ignored.
    enforce_activation_inventory(paths)
    return {
        "status": "PENDING_EXTERNAL_ATTESTATION",
        "mode": "m32_manifest_free_source_pins_readonly",
        "source_head": expected_head,
        "origin_main": expected_main,
        "roots_inspected": len(roots),
        "roles_checked": len(paths),
        "authority_counts": seen_counts,
        "historical_acl_attestation_proven": False,
        "sqlite_opened": False,
        "writes_performed": False,
        "tauri_launched": False,
        "production_migrated": False,
        "m32_staging_authorized": False,
        "operator_live_qualified": False,
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
        result = inspect(
            args.source_repo, args.expected_head, args.expected_main,
            args.production_root, args.m25_root, args.m31_root, args.acl_root,
            args.proposed_identity, args.ack_app_stopped,
        )
    except (GateStop, OSError, UnicodeError, TypeError, ValueError) as exc:
        result = {
            "status": "FAIL",
            "reason": str(exc) if isinstance(exc, GateStop)
                      else "direct_readonly_probe_error",
            "writes_performed": False,
            "m32_staging_authorized": False,
        }
    print(json.dumps(result, sort_keys=True, ensure_ascii=True))
    # Even a complete byte comparison remains pending external attestations.
    return 2


if __name__ == "__main__":
    sys.exit(main())
