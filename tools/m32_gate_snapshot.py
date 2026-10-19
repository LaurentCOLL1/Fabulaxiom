"""Fail-closed public-source M3.2 authority snapshot (NO operator I/O).

Validates an intentionally dated documentation checkpoint, not live GitHub,
independent source custody, Windows permissions or Tauri runtime authority.
This module has no executor, filesystem writer, network client or promotion path.
"""
from __future__ import annotations

import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "docs" / "continuity" / "M3_2_GATE_SNAPSHOT.json"
EXPECTED_ROLES = {
    "production/pre_m24_early_manifest": "OBSERVED_SHA256_ONLY",
    "acl/original_acls": "OBSERVED_SHA256_ONLY",
    "acl/pre_repair_json": "OBSERVED_SHA256_ONLY",
    "production/activation_marker": "UNANCHORED_OBSERVED",
    "m25/isolated_v6": "UNANCHORED_OBSERVED",
}
EXECUTION_GATES = (
    "G2", "G3", "G4", "G5", "G6", "production_007", "writer_ipc",
    "pr35_merge", "M3_3", "release",
)
PROOFS = {
    "ci_core_manifests": "PASS_COMPILE_ONLY",
    "ci_core_acl_window_separation": "PASS_COMPILE_ONLY",
    "ci_synthetic_browser": "PASS_SYNTHETIC_ONLY",
    "ci_synthetic_sqlite": "PASS_SYNTHETIC_ONLY",
    "cli_config_resolution": "NOT_TESTED",
    "tauri_webview_runtime": "NOT_TESTED",
    "operator_acceptance": "NOT_PERFORMED",
    "real_g3_source_provenance": "UNAVAILABLE",
}


class GateRefusal(ValueError):
    """A dated status claim or source boundary is not compatible with M3.2."""


def require(condition: bool, explanation: str) -> None:
    if not condition:
        raise GateRefusal("STOP: " + explanation)


def inspect_snapshot(record: dict) -> dict:
    """Read-only pure validation. No decision is promoted by passing CI."""
    require(isinstance(record, dict), "snapshot is not an object")
    require(set(record) == {
        "schema_version", "as_of", "scope", "repository", "checkpoint",
        "development", "historical", "prospective", "operator_execution",
        "technical_evidence", "protected_assets", "claims",
    }, "snapshot schema changed without review")
    require(type(record["schema_version"]) is int and record["schema_version"] == 1,
            "unsupported schema version")
    require(record["as_of"] == "2026-10-19", "checkpoint date mismatch")
    require(record["scope"] == "SOURCE_ONLY_GOVERNANCE_SNAPSHOT",
            "source-only restriction missing")
    require(record["repository"] == "LaurentCOLL1/Fabulaxiom",
            "incorrect repository identity")
    checkpoint = record["checkpoint"]
    require(re.fullmatch(r"[0-9a-f]{40}", checkpoint.get("main_sha", "")) is not None,
            "main SHA malformed")
    require(re.fullmatch(r"[0-9a-f]{40}", checkpoint.get("last_pr_head", "")) is not None,
            "pull request SHA malformed")
    require(checkpoint["last_merged_pr"] == 82 and checkpoint["windows_ci_run"] == 39202144936,
            "unreviewed evidence checkpoint")
    require(checkpoint["ci_result"] == "SUCCESS" and
            checkpoint["ci_steps_passed"] == checkpoint["ci_steps_total"] == 58,
            "historical CI reference mismatched")
    require(checkpoint["external_live_ci_recheck"] == "REQUIRED_BEFORE_NEW_MERGE",
            "cannot treat static CI reference as live verification")
    require(record["development"] == {
        "pr35": "OPEN_DRAFT", "issues": {"36": "OPEN", "38": "OPEN"},
    }, "unreviewed PR or issue closure")
    history = record["historical"]
    require(history["status"] == "PENDING_EXTERNAL_ATTESTATION",
            "historic proof must remain pending")
    require((history["historically_pinned"], history["observed_sha_only"],
             history["unanchored_observed"]) == (21, 3, 2),
            "historic 21/3/2 split must not be altered")
    roles = history["roles"]
    require(isinstance(roles, list) and len(roles) == 5,
            "five distinct unresolved historical roles required")
    require(all(isinstance(entry, dict) and
                set(entry) == {"role", "status"} for entry in roles),
            "unknown historical role attributes")
    actual = {entry["role"]: entry["status"] for entry in roles}
    require(len(actual) == 5 and actual == EXPECTED_ROLES,
            "missing, duplicated, or falsely promoted historical witness")
    require(record["prospective"] == {
        "status": "NOT_STARTED", "solo_policy": "APPROVED_POLICY_ONLY",
        "independent_human_review": "NOT_PERFORMED",
    }, "prospective baseline or independent review cannot be inferred")
    require(set(record["operator_execution"]) == set(EXECUTION_GATES),
            "unreviewed operator execution gate")
    require(all(record["operator_execution"][key] == "NOT_AUTHORIZED"
                for key in EXECUTION_GATES),
            "operator execution cannot be authorized by this snapshot")
    require(record["technical_evidence"] == PROOFS,
            "synthetic/compile evidence must not be promoted to runtime proof")
    require(record["protected_assets"] == {
        "active_production_sqlite": "RESTORED_V6_DO_NOT_OPEN",
        "isolated_m31_sqlite": "V7_DO_NOT_OPEN",
        "windows_worktrees": 7,
        "originals_mutated_by_this_snapshot": False,
    }, "operator assets are not available to this source-only snapshot")
    claims = record["claims"]
    require(set(claims) == {
        "historic_attestation_proven", "prospective_reference_established",
        "real_g3_authorized", "tauri_runtime_qualified", "release_authorized",
    } and all(value is False for value in claims.values()),
            "no automatic authority promotion")
    return {
        "source_only_snapshot": "PASS",
        "historical": "PENDING_EXTERNAL_ATTESTATION(21/3/2)",
        "prospective": "NOT_STARTED",
        "real_G3": "NOT_AUTHORIZED",
        "tauri_runtime": "NOT_TESTED",
        "operator_permission": "NOT_AUTHORIZED",
    }


def load_snapshot() -> dict:
    with SNAPSHOT.open("r", encoding="utf-8") as source:
        return json.load(source)
