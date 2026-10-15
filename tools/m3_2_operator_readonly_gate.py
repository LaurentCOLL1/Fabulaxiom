"""M3.2 stage 11: genuinely READ-ONLY Windows post-restart custody gate.

NO --prepare/--write action exists. Does not create IDs, directories,
SQLite handles, WAL files, manifests, backups, overlays, or modified Git refs.
The protected manifest must be operator-produced and SHA-verified independently;
this script NEVER invents hashes from the same data it is asked to verify.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePath
import re
import subprocess
import sys

from m3_1_v7_isolated_launch_prepare import _windows_admin_token_enabled

_HEX40 = re.compile(r"[0-9a-f]{40}\Z")
_HEX64 = re.compile(r"[0-9a-f]{64}\Z")
_M32_ID = re.compile(r"com\.fabulaxiom\.m32gate[0-9a-f]{32}\Z")
_REPARSE_ATTRIBUTE = 0x400


class GateStop(Exception):
    """Expected fail-closed result, without modifying any source."""


def windows_standard_medium_token() -> bool:
    """Reject elevated, unknown and non-medium effective Windows tokens."""
    if sys.platform != "win32":
        raise GateStop("windows_operator_required")
    if _windows_admin_token_enabled():
        raise GateStop("elevated_operator_token_forbidden")
    try:
        result = subprocess.run(
            ["whoami", "/groups", "/fo", "csv"], check=True,
            capture_output=True, text=True, timeout=12, errors="replace",
        )
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        raise GateStop("windows_integrity_probe_unavailable") from exc
    # Integrity SIDs are language independent, unlike localized group names.
    if "S-1-16-8192" not in result.stdout or any(
        value in result.stdout for value in
        ("S-1-16-12288", "S-1-16-16384", "S-1-16-20480")
    ):
        raise GateStop("operator_medium_integrity_not_proven")
    return True


def regular_safe(path: Path, directory: bool) -> None:
    """Reject symlink/junction/reparse points along every existing ancestor."""
    absolute = path.absolute()
    for node in (*reversed(absolute.parents), absolute):
        try:
            stat = node.stat(follow_symlinks=False)
        except OSError as exc:
            raise GateStop("required_path_missing_or_unreadable") from exc
        if node.is_symlink() or bool(
            getattr(stat, "st_file_attributes", 0) & _REPARSE_ATTRIBUTE
        ):
            raise GateStop("reparse_point_in_protected_path")
    if directory and not path.is_dir():
        raise GateStop("expected_directory_missing")
    if not directory and not path.is_file():
        raise GateStop("expected_regular_file_missing")


def digest_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(256 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def git_value(repo: Path, *args: str) -> str:
    try:
        answer = subprocess.run(
            ["git", "-C", str(repo), *args],
            capture_output=True, text=True, check=True, timeout=20,
            errors="replace",
        )
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        raise GateStop("git_exact_source_check_failed") from exc
    return answer.stdout.strip()


def safe_relative_file(root: Path, value: str) -> Path:
    if not isinstance(value, str) or not value or "\\" in value:
        raise GateStop("protected_manifest_relative_path_invalid")
    # PurePath is intentionally host-native. Slash paths are accepted on
    # Windows and in the synthetic tests; no UNC, drive or traversal segments.
    path = PurePath(value)
    if path.is_absolute() or path.drive or any(
        part in ("", ".", "..") for part in value.split("/")
    ):
        raise GateStop("protected_manifest_relative_path_invalid")
    return root / path


def inspect(
    source_repo: Path, expected_head: str, expected_main: str,
    production_root: Path, protected_manifest: Path,
    proposed_identity: str, app_stopped: bool,
    token_checker=windows_standard_medium_token,
) -> dict:
    # All conditions verified before even inspecting protected data.
    if not app_stopped:
        raise GateStop("operator_app_stopped_ack_required")
    if not _HEX40.fullmatch(expected_head) or not _HEX40.fullmatch(expected_main):
        raise GateStop("invalid_expected_source_sha")
    if not _M32_ID.fullmatch(proposed_identity):
        raise GateStop("unapproved_m32_identity")
    if not token_checker():
        raise GateStop("standard_medium_token_unconfirmed")

    regular_safe(source_repo, True)
    if git_value(source_repo, "rev-parse", "HEAD") != expected_head:
        raise GateStop("git_head_not_exact")
    if git_value(source_repo, "rev-parse", "refs/remotes/origin/main") != expected_main:
        raise GateStop("remote_main_not_exact_refetch_required")
    if git_value(source_repo, "status", "--porcelain", "--untracked-files=all"):
        raise GateStop("git_worktree_not_clean")

    if production_root.name != "com.fabulaxiom.desktop":
        raise GateStop("production_root_identity_wrong")
    regular_safe(production_root.parent, True)
    regular_safe(production_root, True)

    # Even a broken symlink/reserved folder at this name counts as an occupied
    # identity. Never reuse any M3.1, production, or previous M3.2 root.
    target = production_root.parent / proposed_identity
    if os.path.lexists(target):
        raise GateStop("proposed_identity_already_exists")

    regular_safe(protected_manifest, False)
    if protected_manifest.stat().st_size > 128 * 1024:
        raise GateStop("protected_manifest_too_large")
    try:
        manifest = json.loads(protected_manifest.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise GateStop("protected_manifest_invalid") from exc
    if not isinstance(manifest, dict) or (
        manifest.get("protocol") != "fabulaxiom_m32_protected_sha_manifest_v1"
    ):
        raise GateStop("protected_manifest_protocol_invalid")
    items = manifest.get("protected_files")
    if not isinstance(items, list) or len(items) < 2 or len(items) > 64:
        raise GateStop("protected_manifest_file_set_invalid")

    seen = set()
    total = 0
    for item in items:
        if not isinstance(item, dict) or set(item) != {"path", "sha256"}:
            raise GateStop("protected_manifest_item_invalid")
        relative = item["path"]
        expected = item["sha256"]
        if not isinstance(expected, str) or not _HEX64.fullmatch(expected):
            raise GateStop("protected_manifest_digest_invalid")
        if relative in seen:
            raise GateStop("protected_manifest_duplicate")
        seen.add(relative)
        candidate = safe_relative_file(production_root, relative)
        regular_safe(candidate, False)
        if digest_file(candidate) != expected:
            raise GateStop("protected_file_digest_changed")
        total += 1

    # A readiness result means "safe to REQUEST the future separate preparer",
    # not approval for staging, launch or data writing.
    return {
        "status": "READY",
        "mode": "m32_post_restart_readonly_dry_run",
        "source_head": expected_head,
        "origin_main": expected_main,
        "protected_files_verified": total,
        "isolated_identity_created": False,
        "sqlite_opened": False,
        "writes_performed": False,
        "tauri_launched": False,
        "production_migrated": False,
        "active_pointer_modified": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-repo", type=Path, required=True)
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--expected-main", required=True)
    parser.add_argument("--production-root", type=Path, required=True)
    parser.add_argument("--protected-manifest", type=Path, required=True)
    parser.add_argument("--proposed-identity", required=True)
    parser.add_argument("--ack-app-stopped", action="store_true")
    parser.add_argument("--dry-run", action="store_true", required=True)
    args = parser.parse_args(argv)
    try:
        result = inspect(
            args.source_repo, args.expected_head, args.expected_main,
            args.production_root, args.protected_manifest,
            args.proposed_identity, args.ack_app_stopped,
        )
    except (GateStop, OSError, ValueError, TypeError) as exc:
        result = {
            "status": "FAIL",
            "reason": str(exc) if isinstance(exc, GateStop)
                      else "post_restart_probe_error",
            "writes_performed": False,
        }
    print(json.dumps(result, sort_keys=True, ensure_ascii=True))
    return 0 if result["status"] == "READY" else 2


if __name__ == "__main__":
    sys.exit(main())
