"""M3.2 Stage 19: external provenance CLAIM triage — never attestation.

This script reads only an explicitly supplied JSON claim form. It never
reads protected databases/ACL archives, makes network calls, verifies
signatures, changes files, or authorizes any M3.2 write. The evidence
record's timestamp, URI, custodian and digest are untrusted ASSERTIONS.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import stat
import sys
from urllib.parse import urlparse

import m3_2_independent_authority_gate as source
from m3_2_operator_readonly_gate import GateStop, regular_safe

REMAINING = frozenset(source.OBSERVED_SHA256) | source.UNANCHORED_OBSERVED
assert len(REMAINING) == 5
KINDS = frozenset(("none", "recent_observation", "prior_external_claim"))
ALLOWED = frozenset((
    "root", "role", "observed_sha256", "evidence_kind", "evidence_uri",
    "recorded_at", "custodian", "record_id",
))


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip()) and len(value) <= 256


def _timestamp(value: object) -> bool:
    if not isinstance(value, str) or len(value) > 48:
        return False
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return dt.tzinfo is not None and dt.utcoffset() is not None


def _remote_reference(value: object) -> bool:
    if not isinstance(value, str) or len(value) > 2048:
        return False
    parts = urlparse(value)
    # A URL is only a lead for manual review, not a trust anchor.
    return (
        parts.scheme == "https"
        and bool(parts.hostname)
        and not parts.username
        and not parts.password
        and not parts.fragment
    )


def triage_claims(records: object) -> dict:
    """Classify exactly five missing-legal-authority roles, never promote."""
    if not isinstance(records, list) or len(records) != len(REMAINING):
        raise GateStop("provenance_exact_five_roles_required")

    found: set[tuple[str, str]] = set()
    counts = {"no_claim": 0, "recent_observation": 0,
              "unverified_prior_external_claim": 0}
    for item in records:
        if not isinstance(item, dict) or set(item) != ALLOWED:
            raise GateStop("provenance_record_shape_invalid")
        root, role = item["root"], item["role"]
        if not isinstance(root, str) or not isinstance(role, str):
            raise GateStop("provenance_role_invalid")
        key = (root, role)
        if key not in REMAINING or key in found:
            raise GateStop("provenance_role_unknown_or_duplicate")
        found.add(key)

        digest = item["observed_sha256"]
        if key in source.OBSERVED_SHA256:
            if digest != source.OBSERVED_SHA256[key]:
                raise GateStop("provenance_observed_sha_mismatch")
        elif digest is not None:
            # An external claim is never a source-verified SHA pin.
            raise GateStop("provenance_unanchored_must_not_self_pin")

        kind = item["evidence_kind"]
        if not isinstance(kind, str) or kind not in KINDS:
            raise GateStop("provenance_evidence_kind_invalid")
        fields = ("evidence_uri", "recorded_at", "custodian", "record_id")
        populated = [item[f] is not None for f in fields]
        if kind == "none":
            if any(populated):
                raise GateStop("provenance_none_must_have_no_evidence")
            counts["no_claim"] += 1
        elif kind == "recent_observation":
            if any(populated):
                raise GateStop("provenance_observation_must_not_claim_witness")
            counts["recent_observation"] += 1
        else:
            if not all(populated):
                raise GateStop("provenance_external_record_incomplete")
            if not (_remote_reference(item["evidence_uri"])
                    and _timestamp(item["recorded_at"])
                    and _nonempty(item["custodian"])
                    and _nonempty(item["record_id"])):
                raise GateStop("provenance_external_record_metadata_invalid")
            # Metadata may be forgeries; do not fetch URLs or mark verified.
            counts["unverified_prior_external_claim"] += 1
    if found != REMAINING:
        raise GateStop("provenance_scope_mismatch")

    return {
        "status": "PENDING_EXTERNAL_ATTESTATION",
        "mode": "m32_external_provenance_claim_triage_only",
        "roles_checked": len(found),
        "historically_pinned_roles_unchanged": len(source.PINNED_SHA256),
        "observed_sha_roles_unchanged": len(source.OBSERVED_SHA256),
        "unanchored_roles_unchanged": len(source.UNANCHORED_OBSERVED),
        "claims": counts,
        "independently_verified_historical_claims": 0,
        "historical_promotions": 0,
        "external_urls_fetched": False,
        "signatures_verified": False,
        "sqlite_opened": False,
        "protected_files_opened": False,
        "writes_performed": False,
        "m32_staging_authorized": False,
        "operator_live_qualified": False,
    }


# These are intentionally conservative path components; a provenance claim
# cannot be read out of production, historic custody or any source worktree.
PROTECTED_COMPONENTS = frozenset((
    "com.fabulaxiom.desktop",
    "com.fabulaxiom.m25qual35fb842c",
    "com.fabulaxiom.m31launchdb8d3278504c448084478a70ccb71cbd",
    "fabulaxiom-m31-acl-evidence-4d520e18",
))
PROTECTED_SOURCE_PREFIXES = (
    "fabulaxiom-m25-", "fabulaxiom-m31-", "fabulaxiom-m32-",
)
MAX_CLAIMS_BYTES = 16_384


def _no_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
    result: dict = {}
    for key, value in pairs:
        if key in result:
            raise GateStop("provenance_json_duplicate_key")
        result[key] = value
    return result


def _reject_non_json_constant(_value: str) -> None:
    raise GateStop("provenance_json_nonfinite_number")


def _stat_identity(path: Path) -> tuple:
    status = path.stat(follow_symlinks=False)
    if not stat.S_ISREG(status.st_mode):
        raise GateStop("provenance_claims_not_regular")
    if not 0 < status.st_size <= MAX_CLAIMS_BYTES:
        raise GateStop("provenance_claims_input_invalid")
    return (
        status.st_dev, status.st_ino, status.st_mode,
        status.st_size, status.st_mtime_ns, status.st_ctime_ns,
    )


def _read_once(path: Path) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0)
    # Stronger no-follow on platforms providing it. On Windows the pre/post
    # reparse checks are defense-in-depth, not an atomic filesystem snapshot.
    flags |= getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags)
    with os.fdopen(fd, "rb") as stream:
        opened = os.fstat(stream.fileno())
        if not stat.S_ISREG(opened.st_mode):
            raise GateStop("provenance_opened_not_regular")
        if opened.st_size > MAX_CLAIMS_BYTES:
            raise GateStop("provenance_claims_input_invalid")
        data = stream.read(MAX_CLAIMS_BYTES + 1)
        if len(data) > MAX_CLAIMS_BYTES or not data:
            raise GateStop("provenance_claims_input_invalid")
        return data


def read_claims_readonly(path: Path) -> object:
    """Bounded double-read; reject redirected ancestors and protected roots.

    Checks detect ordinary between-read changes, but don't assert an OS-level
    atomic snapshot or certify external historical witnesses.
    """
    if not path.is_absolute():
        raise GateStop("provenance_claims_absolute_path_required")
    for part in path.parts:
        component = part.casefold()
        if component in PROTECTED_COMPONENTS or any(
            component.startswith(prefix) for prefix in PROTECTED_SOURCE_PREFIXES
        ):
            raise GateStop("provenance_claims_protected_location")
    # The historic production repository is anchored at M:\\Fabulaxiom on
    # the operator's machine. Do NOT reject every path component named
    # "Fabulaxiom": GitHub Windows runners also use that directory name.
    if os.name == "nt":
        normalized = os.path.normcase(os.path.normpath(str(path)))
        local_main = os.path.normcase(os.path.normpath(r"M:\Fabulaxiom"))
        if normalized == local_main or normalized.startswith(local_main + os.sep):
            raise GateStop("provenance_claims_protected_location")
    regular_safe(path, False)
    before = _stat_identity(path)
    first = _read_once(path)
    if _stat_identity(path) != before:
        raise GateStop("provenance_claims_changed_during_read")
    regular_safe(path, False)
    second = _read_once(path)
    if second != first or _stat_identity(path) != before:
        raise GateStop("provenance_claims_changed_during_read")
    regular_safe(path, False)
    try:
        return json.loads(
            first.decode("utf-8"),
            object_pairs_hook=_no_duplicate_keys,
            parse_constant=_reject_non_json_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise GateStop("provenance_claims_invalid_utf8_json") from exc



def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--claims-json", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true", required=True)
    args = parser.parse_args(argv)
    try:
        # All checks happen before the metadata is interpreted.
        records = read_claims_readonly(args.claims_json)
        result = triage_claims(records)
    except (GateStop, OSError, UnicodeError, ValueError, TypeError) as exc:
        result = {
            "status": "FAIL",
            "reason": str(exc) if isinstance(exc, GateStop)
                      else "provenance_claims_parse_failed",
            "writes_performed": False,
            "m32_staging_authorized": False,
        }
    print(json.dumps(result, ensure_ascii=True, sort_keys=True))
    # Both triage-pending and fail are non-authorizing.
    return 2


if __name__ == "__main__":
    sys.exit(main())
