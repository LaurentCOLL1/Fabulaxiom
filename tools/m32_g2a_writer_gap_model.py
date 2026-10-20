"""Refusal-only source evidence model for M3.2; NEVER a real gate authorization.

No Windows, SQLite, network or filesystem I/O. Inputs are invented booleans.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class SourceOnlyEvidence:
    g2a_metadata_pass: bool = False
    process_names_absent: bool = False
    no_sidecars_seen: bool = False
    hashes_stable: bool = False
    exclusive_handle_toy: bool = False
    file_identity_toy: bool = False
    preopened_owner_toy: bool = False
    all_fictional_checks_true: bool = False

def evaluate(evidence: SourceOnlyEvidence) -> dict[str, object]:
    if type(evidence) is not SourceOnlyEvidence:
        raise TypeError("STOP: unsupported evidence object")
    if any(type(value) is not bool for value in vars(evidence).values()):
        raise TypeError("STOP: evidence flags must be plain booleans")
    return {
        "g2a_metadata_observation": "OBSERVED_ONLY" if evidence.g2a_metadata_pass else "UNASSESSED",
        "process_writer_absence": "NOT_PROVEN",
        "source_identity_authenticated": False,
        "trusted_nonmigrating_owner_established": False,
        "cold_quiescence_and_journals_established": False,
        "historic_custody": "PENDING_EXTERNAL_ATTESTATION(21/3/2)",
        "prospective_baseline": "NOT_STARTED",
        "real_g3": "STOP_UNAVAILABLE",
        "downstream": "NOT_AUTHORIZED",
        "operator_permission": "NEW_EXPLICIT_APPROVAL_REQUIRED",
        "real_g3_authorized": False,
    }
