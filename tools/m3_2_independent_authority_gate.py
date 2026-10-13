"""Stage 13: independently pinned source-side SHA authority for stage-12 custody.

No SQLite connection, filesystem write, profile preparation or Tauri run.
The source-controlled anchors are previous operator/qualification observations;
they are not signatures or permission to edit protected user files.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath
import re
import sys

import m3_2_multiroot_readonly as stage12
from m3_2_operator_readonly_gate import GateStop

# These values are taken from already recorded GitHub project qualification
# BEFORE a new operator request. They are not computed from currently inspected
# user files. Roles lacking a historic anchor remain explicitly OBSERVED.
PINNED_SHA256 = {
    ("production", "active_v6"): "b904731afac0b6b6135ba6d6a8a8dee3548c50daca1a5ee3a7788db85cee16ff",
    ("production", "pre_m21_v3"): "f8ec1a1f32f97a0b4f39eeb238c307e5a192854cdd6c4206a05a97b6a385c987",
    ("production", "pre_m23_v4"): "c624241080d6e820398cc502b4db206fcaba457405083ce806c302a6ce464976",
    ("production", "pre_m23_manifest"): "56be2ebd102bde7510848c94e9f00aefae05d287506e77bade8352b208bd1136",
    ("production", "pre_m24_v5"): "db02961d7a30c6a6522bd52faeab8ceb09e26c1a4a6a58be467d142806e22fee",
    ("production", "pre_m24_manifest"): "00f42d268543546782db61928ce96e999c932a45a1f7edf439ba90d0d132ed76",
    ("production", "pre_m24_early_v5"): "db02961d7a30c6a6522bd52faeab8ceb09e26c1a4a6a58be467d142806e22fee",
    ("production", "app_backup_a"): "ea83f7791bd2c16a343fce155d3cd255ecc19d1985a88e88c5e0918dad30c54d",
    ("production", "app_backup_b"): "c0c93b77fd5c937b9f111d6017a56b2e543f64a4324d6cf07d81e2415168d463",
    ("production", "m31_v6_backup"): "b2059574929e06d9966cce96df97b4f3337d0f7b56afa5734a862110af00d495",
    ("production", "m31_v6_restore"): "b2059574929e06d9966cce96df97b4f3337d0f7b56afa5734a862110af00d495",
    ("production", "m31_v6_manifest"): "819abb95ef9147bed6fd13a8189bccf09f97d808a093c1160b4d6e8957b94d59",
    ("production", "m31_third_v7"): "566db86d415b449de3f9f53145f6b830d6942ef4067c20df852ec3d722f54402",
    ("production", "m31_third_manifest"): "82da38026dee3002e9726ae1bdb92fb22c6554710f3ce74ab152449563345cc7",
    ("production", "m31_fourth_v6"): "b2059574929e06d9966cce96df97b4f3337d0f7b56afa5734a862110af00d495",
    ("production", "m31_fourth_manifest"): "353170fa726b743bd810867e612acf4ecc0530ceca2268a7a53fda92145a6b0f",
    ("m25", "pre_m25_v6"): "9e738d58519e1a0e3c1750d71726b661132fcbc0211fddea3178f6314bbfc7cf",
    ("m25", "pre_m25_manifest"): "c9b4ec93762cf2666e9235828aeb2bef2a127aded0cf408e6086f7b81ae6efd2",
    ("m31", "isolated_v7"): "566db86d415b449de3f9f53145f6b830d6942ef4067c20df852ec3d722f54402",
    ("m31", "overlay"): "e377ae9ba9a0430928fec79700c31a74b6035a6f086e75bff19055766c118edc",
    ("m31", "preparation_manifest"): "9b718667487ed5776d141358d47e9f6dbb247a93fdc4c66a68baa42780d36da9",
}

# These are recent observations ONLY, despite having known SHA values.
# A future independently approved change must be required to promote one.
OBSERVED_SHA256 = {
    ("production", "pre_m24_early_manifest"): "372f4ed68942a85f35a7a11a6c030589f9ff5b95d352899e00b154c99964b47d",
    ("acl", "original_acls"): "bed23c954f720b7aca398290dfd9bed127a316687a383d21f428ae233fa54e83",
    ("acl", "pre_repair_json"): "5fcc1d1baec1fd4b3cb39ddbd1c866e5c6328bfd0a60c95faa23b23d1163e86e",
}
UNANCHORED_OBSERVED = frozenset((
    ("production", "activation_marker"),
    ("m25", "isolated_v6"),
))

# Only use documented layouts, not arbitrary same-hash files in other folders.
EARLY = "fabulaxiom.operator-pre-m2-4-v5.20261009T185159Z-61d9d667c4584cb1854162158c0dfc10.sqlite3"
LATE = "fabulaxiom.operator-pre-m2-4-v5.20261009T200405Z-ed169c2ac6724ab6aca018024b26e8af.sqlite3"
V25 = "fabulaxiom.operator-pre-m2-5-v6.20261010T063838Z-5a1f631aa5c148e49377d0465b931706.sqlite3"
BASE31 = "operator-qualification/m3_1"
PRE31 = BASE31 + "/pre_v7_20261011T074045Z-88956f2eb16a4503a0d44d0e9bc968ab/"
THIRD31 = BASE31 + "/v7_copy_rehearsal_20261011T090737Z-d6450d9cd5f34ca4a574bb4a2eb32fd0/"
FOURTH31 = BASE31 + "/v7_rollback_rehearsal_20261011T111844Z-8e53aaaabae847f2b982b089fc7b7a57/"

EXACT_PATHS = {
    ("production", "active_v6"): "database/fabulaxiom-restored-00000000000001791428210487599800-0000025660-0000000001.sqlite3",
    ("production", "activation_marker"): "database/activations/activation-00000000000001791428210523732000-0000025660-0000000002.active",
    ("production", "pre_m21_v3"): "backups/fabulaxiom.operator-pre-m2-1-v3.20261008-170752-0746ccd626fb4030a8c1c3b35801db32.sqlite3",
    ("production", "pre_m24_v5"): "operator-qualification/m2_4/" + LATE,
    ("production", "pre_m24_manifest"): "operator-qualification/m2_4/" + LATE + ".manifest.json",
    ("production", "pre_m24_early_v5"): "operator-qualification/m2_4/" + EARLY,
    ("production", "pre_m24_early_manifest"): "operator-qualification/m2_4/" + EARLY + ".manifest.json",
    ("production", "app_backup_a"): "backups/fabulaxiom-backup-00000000000001791428029335746400-0000025660-0000000000.sqlite3",
    ("production", "app_backup_b"): "backups/fabulaxiom-backup-00000000000001791563505045194400-0000024132-0000000000.sqlite3",
    ("production", "m31_v6_backup"): PRE31 + "fabulaxiom-pre-m3-1-v6.sqlite3",
    ("production", "m31_v6_restore"): PRE31 + "isolated-restore-rehearsal-v6.sqlite3",
    ("production", "m31_v6_manifest"): PRE31 + "manifest.json",
    ("production", "m31_third_v7"): THIRD31 + "candidate-v7.sqlite3",
    ("production", "m31_third_manifest"): THIRD31 + "candidate-v7-manifest.json",
    ("production", "m31_fourth_v6"): FOURTH31 + "failed-v7-rolled-back-v6.sqlite3",
    ("production", "m31_fourth_manifest"): FOURTH31 + "rollback-manifest.json",
    ("m25", "isolated_v6"): "database/fabulaxiom.sqlite3",
    ("m25", "pre_m25_v6"): "operator-qualification/m2_5/" + V25,
    ("m25", "pre_m25_manifest"): "operator-qualification/m2_5/" + V25 + ".manifest.json",
    ("m31", "isolated_v7"): "database/fabulaxiom.sqlite3",
    ("m31", "overlay"): "tauri.m31.isolated.conf.json",
    ("m31", "preparation_manifest"): "preparation-manifest.json",
    ("acl", "original_acls"): "original-acls.txt",
    ("acl", "pre_repair_json"): "pre-repair-evidence.json",
}
# The original pre-M2.3 filename is not in the saved qualifying prose:
# require the documented custody directory and historical content SHA.
VARIABLE_PATHS = {
    ("production", "pre_m23_v4"): re.compile(
        r"operator-qualification/m2_3/fabulaxiom\.operator-pre-m2-3-v4\.[^/]+\.sqlite3\Z"
    ),
    ("production", "pre_m23_manifest"): re.compile(
        r"operator-qualification/m2_3/fabulaxiom\.operator-pre-m2-3-v4\.[^/]+\.sqlite3\.manifest\.json\Z"
    ),
}
ALL_ROLES = frozenset(
    (root, role) for root, values in stage12.ROLES.items() for role in values
)
assert set(PINNED_SHA256) | set(OBSERVED_SHA256) | set(UNANCHORED_OBSERVED) == ALL_ROLES
assert not (set(PINNED_SHA256) & set(OBSERVED_SHA256))


def validate_anchored_records(records: object) -> dict[str, int]:
    """Never trust the manifest's self-declared historical provenance."""
    if not isinstance(records, list) or len(records) != len(ALL_ROLES):
        raise GateStop("authority_required_scope_incomplete")
    found: set[tuple[str, str]] = set()
    summary = {"source_pinned": 0, "recent_observation": 0, "unanchored": 0}
    matched_paths: dict[tuple[str, str], str] = {}
    for item in records:
        if not isinstance(item, dict) or set(item) != {
            "root", "role", "path", "sha256", "authority"
        }:
            raise GateStop("authority_manifest_record_invalid")
        root, role = item["root"], item["role"]
        if not isinstance(root, str) or not isinstance(role, str):
            raise GateStop("authority_role_invalid")
        key = (root, role)
        if key not in ALL_ROLES or key in found:
            raise GateStop("authority_role_unknown_or_duplicate")
        found.add(key)

        path = item["path"]
        digest = item["sha256"]
        authority = item["authority"]
        if (
            not isinstance(path, str) or not isinstance(digest, str)
            or not isinstance(authority, str)
            or not stage12.HEX64.fullmatch(digest)
        ):
            raise GateStop("authority_manifest_value_invalid")
        if key in EXACT_PATHS:
            if path != EXACT_PATHS[key]:
                raise GateStop("authority_exact_path_mismatch")
        elif key in VARIABLE_PATHS:
            if not VARIABLE_PATHS[key].fullmatch(path):
                raise GateStop("authority_historical_directory_or_name_invalid")
            matched_paths[key] = path
        else:
            raise GateStop("authority_path_policy_missing")

        if key in PINNED_SHA256:
            if digest != PINNED_SHA256[key] or authority != "historical":
                raise GateStop("authority_source_pinned_sha_or_label_mismatch")
            summary["source_pinned"] += 1
        elif key in OBSERVED_SHA256:
            if digest != OBSERVED_SHA256[key] or authority != "observed":
                raise GateStop("authority_observed_not_independently_historical")
            summary["recent_observation"] += 1
        elif key in UNANCHORED_OBSERVED:
            if authority != "observed":
                raise GateStop("authority_unanchored_role_not_historical")
            summary["unanchored"] += 1
        else:
            raise GateStop("authority_unclassified_role")

    db = matched_paths.get(("production", "pre_m23_v4"))
    manifest = matched_paths.get(("production", "pre_m23_manifest"))
    if db is None or manifest != db + ".manifest.json":
        raise GateStop("authority_pre_m23_pair_mismatch")
    if found != ALL_ROLES:
        raise GateStop("authority_required_roles_missing")
    return summary


def inspect(
    source_repo: Path, expected_head: str, expected_main: str,
    production_root: Path, m25_root: Path, m31_root: Path, acl_root: Path,
    protected_manifest: Path, expected_manifest_sha256: str,
    proposed_identity: str, app_stopped: bool,
    token_checker=stage12.prior.windows_standard_medium_token,
) -> dict:
    # First refuse incomplete source authority WITHOUT opening the protected
    # databases. Stage 12 independently checks Git, medium token, file hashes
    # and M1.5 selection (also without opening SQLite).
    if not app_stopped or not token_checker():
        raise GateStop("authority_operator_medium_token_and_shutdown_required")
    data = stage12._manifest_read(protected_manifest, expected_manifest_sha256)
    authority = validate_anchored_records(data.get("protected_files"))
    result = stage12.inspect(
        source_repo, expected_head, expected_main,
        production_root, m25_root, m31_root, acl_root,
        protected_manifest, expected_manifest_sha256,
        proposed_identity, app_stopped, token_checker=token_checker
    )
    if result.get("status") != "PENDING_HISTORICAL_AUTHORITY":
        raise GateStop("authority_expected_observation_pending")
    return {
        **result,
        "status": "PENDING_EXTERNAL_ATTESTATION",
        "mode": "m32_pinned_authority_readonly_candidate",
        "source_anchor_counts": authority,
        "m32_staging_authorized": False,
        "operator_live_qualified": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-repo", type=Path, required=True)
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--expected-main", required=True)
    parser.add_argument("--production-root", type=Path, required=True)
    parser.add_argument("--m25-root", type=Path, required=True)
    parser.add_argument("--m31-root", type=Path, required=True)
    parser.add_argument("--acl-root", type=Path, required=True)
    parser.add_argument("--protected-manifest", type=Path, required=True)
    parser.add_argument("--expected-manifest-sha256", required=True)
    parser.add_argument("--proposed-identity", required=True)
    parser.add_argument("--ack-app-stopped", action="store_true")
    parser.add_argument("--dry-run", action="store_true", required=True)
    args = parser.parse_args(argv)
    try:
        result = inspect(
            args.source_repo, args.expected_head, args.expected_main,
            args.production_root, args.m25_root, args.m31_root,
            args.acl_root, args.protected_manifest,
            args.expected_manifest_sha256, args.proposed_identity,
            args.ack_app_stopped
        )
    except (GateStop, OSError, TypeError, ValueError) as exc:
        result = {
            "status": "FAIL",
            "reason": str(exc) if isinstance(exc, GateStop)
                      else "authority_readonly_inspection_failed",
            "writes_performed": False,
            "m32_staging_authorized": False,
        }
    print(json.dumps(result, sort_keys=True, ensure_ascii=True))
    # Always nonzero because PENDING_EXTERNAL_ATTESTATION is NOT readiness.
    return 2


if __name__ == "__main__":
    sys.exit(main())
