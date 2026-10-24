"""Pure in-memory metadata TRIAGE for five historical M3.2 custody roles.

Not an attestation verifier. Never reads archives, files, SQLite or the network.
All input is fictitious metadata; private/operator evidence must NOT be submitted.
Even a structurally plausible claim is never a verified historical witness.
"""
from __future__ import annotations

import re

ROLES = (
    "production/pre_m24_early_manifest",
    "acl/original_acls",
    "acl/pre_repair_json",
    "production/activation_marker",
    "m25/isolated_v6",
)
ALLOWED_FIELDS = frozenset({
    "role", "origin", "proof_ref", "proof_sha256",
    "custodian_id", "preexisting_record", "role_bound",
})
SAFE_REF = re.compile(r"EXT-[A-Z0-9]{6,24}\Z")
SAFE_CUSTODIAN = re.compile(r"ext-[a-z0-9-]{3,40}\Z")
SAFE_HASH = re.compile(r"[0-9a-f]{64}\Z")
CANDIDATE_STATUS = "REVIEW_REQUIRED_NOT_VERIFIED"
REJECTED_STATUS = "REJECTED_UNTRUSTED_METADATA"
MISSING_STATUS = "MISSING_INDEPENDENT_WITNESS"


def triage_fictional_custody_claims(claims: object) -> dict[str, object]:
    """Classify invented metadata only; NEVER claim real G2B acceptance.

    Unknown or duplicate roles, payload fields and non-mapping entries veto.
    The function deliberately does not open even a caller-named path.
    """
    if not isinstance(claims, list) or len(claims) > len(ROLES):
        raise ValueError("STOP: fictional metadata list of at most five claims required")
    result = {role: MISSING_STATUS for role in ROLES}
    for claim in claims:
        if not isinstance(claim, dict):
            raise ValueError("STOP: not an invented metadata object")
        if set(claim) != ALLOWED_FIELDS:
            raise ValueError("STOP: missing, unknown or private payload metadata fields")
        role = claim["role"]
        if not isinstance(role, str) or role not in result:
            raise ValueError("STOP: unknown historical role")
        if result[role] != MISSING_STATUS:
            raise ValueError("STOP: duplicate historical role")
        safe = (
            claim["origin"] == "independent_external_record"
            and isinstance(claim["proof_ref"], str)
            and SAFE_REF.fullmatch(claim["proof_ref"]) is not None
            and isinstance(claim["proof_sha256"], str)
            and SAFE_HASH.fullmatch(claim["proof_sha256"]) is not None
            and isinstance(claim["custodian_id"], str)
            and SAFE_CUSTODIAN.fullmatch(claim["custodian_id"]) is not None
            and claim["preexisting_record"] is True
            and claim["role_bound"] is True
        )
        result[role] = CANDIDATE_STATUS if safe else REJECTED_STATUS
    return {
        "roles": result,
        "historical": "PENDING_EXTERNAL_ATTESTATION(21/3/2)",
        "g2b": "NOT_ACCEPTED",
        "writer_absence": "NOT_PROVEN",
        "real_g3": "STOP_UNAVAILABLE",
        "operator_access": False,
        "evidence_authenticated": False,
        "external_review_required": True,
    }
