"""Source-only G2-A operator authorization packet guard.

This validator checks an inert public proposal. It NEVER validates or runs an
operator PowerShell block and does not make a real-world authorization decision.
"""
from __future__ import annotations

import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "docs" / "qualification" / "M3_2_G2A_OPERATOR_REVIEW_PROPOSAL.json"
OBSERVATIONS = {
    "windows_token_integrity": "CURRENT_PROCESS_METADATA",
    "powershell_version": "CURRENT_SESSION_METADATA",
    "clock_context": "CURRENT_SESSION_METADATA",
    "process_presence": "PROCESS_NAMES_ONLY",
    "git_reference_review": "PUBLIC_GITHUB_READ_ONLY",
}
EFFECTS = {
    "operator_filesystem_read": "NOT_AUTHORIZED",
    "operator_filesystem_write": "PROHIBITED",
    "protected_sqlite_open": "PROHIBITED",
    "sqlite_sidecars": "NO_ACCESS",
    "acl_read": "NOT_AUTHORIZED",
    "process_stop": "PROHIBITED",
    "elevation": "PROHIBITED",
    "interactive_input": "NONE",
    "remote_network_on_operator_machine": "NOT_AUTHORIZED",
    "local_git_mutation": "PROHIBITED",
    "tauri_webview_launch": "PROHIBITED",
    "log_upload": "PROHIBITED",
}
ABORTS = {
    "fail_or_unknown": "STOP",
    "unexpected_process": "STOP_AND_REVIEW",
    "unexpected_integrity": "STOP_AND_REVIEW",
    "ambiguous_git_ref": "STOP_AND_REVIEW",
    "private_path_needed": "STOP_REQUEST_SEPARATE_G2_B_AUTHORIZATION",
    "any_command_not_preapproved": "STOP",
}


class PacketStop(ValueError):
    """Fail-closed public proposal integrity veto."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise PacketStop("STOP: " + message)


def validate_packet(p: dict) -> dict:
    require(isinstance(p, dict), "invalid proposal object")
    require(set(p) == {"schema_version", "as_of", "scope", "title",
                      "authority", "packet", "proposed_observations",
                      "effect_contract", "abort_policy", "operator_fields",
                      "results"}, "unreviewed packet field")
    require(type(p["schema_version"]) is int and p["schema_version"] == 1,
            "schema version changed")
    require(p["as_of"] == "2026-10-19" and
            p["scope"] == "G2_A_OPERATOR_REVIEW_PROPOSAL_ONLY",
            "not the approved, dated nonexecuting proposal")
    require(p["title"] == "Fabulaxiom M3.2 G2-A observation préliminaire",
            "proposal identity changed")
    authority = p["authority"]
    require(set(authority) == {
        "reference_main", "continuity_snapshot", "historical",
        "prospective", "g2_real", "g3_real", "tauri_runtime",
    }, "authority schema changed")
    require(re.fullmatch(r"[0-9a-f]{40}", authority["reference_main"]) is not None,
            "missing Git identity")
    require(authority["continuity_snapshot"] ==
            "docs/continuity/M3_2_GATE_SNAPSHOT.json",
            "continuity authority displaced")
    require(authority["historical"] == "PENDING_EXTERNAL_ATTESTATION(21/3/2)"
            and authority["prospective"] == "NOT_STARTED"
            and authority["g2_real"] == "NOT_AUTHORIZED"
            and authority["g3_real"] == "NOT_AUTHORIZED"
            and authority["tauri_runtime"] == "NOT_TESTED",
            "historical/runtime/G2/G3 status improperly promoted")
    expected_packet = {
        "commands_included": False, "script_sha256": None,
        "operator_paths_included": False, "private_data_included": False,
        "auto_execution": False, "auto_scheduling": False,
        "operator_approval": "NOT_REQUESTED",
        "execution_approval": "NOT_GRANTED",
        "requires_distinct_reviewed_command": True,
    }
    require(p["packet"] == expected_packet,
            "inert proposal became a script or an approval")
    observations = p["proposed_observations"]
    require(isinstance(observations, list) and len(observations) == 5,
            "G2-A observation set changed")
    require(all(isinstance(x, dict) and set(x) == {"id", "purpose", "scope", "execution"}
                and isinstance(x["purpose"], str) and x["purpose"].strip()
                and len(x["purpose"]) <= 240 for x in observations),
            "invalid observation shape")
    require(all(x["execution"] == "PROPOSAL_ONLY" for x in observations),
            "an observation was silently scheduled or executed")
    ids = [x["id"] for x in observations]
    require(len(set(ids)) == 5 and
            {x["id"]: x["scope"] for x in observations} == OBSERVATIONS,
            "unreviewed observation request, scope or duplicate")
    for x in observations:
        require(not any(tok in x["purpose"].lower() for tok in
                        ("powershell.exe", "cmd.exe", "sqlite3", "get-acl",
                         "get-filehash", "invoke-expression", "start-process",
                         "remove-item", "stop-process", "git fetch")),
                "commands or protected reads hidden in a purpose")
    require(p["effect_contract"] == EFFECTS,
            "non-invasive contract has been broadened")
    require(p["abort_policy"] == ABORTS,
            "abort reason removed or changed")
    require(p["operator_fields"] == {
        "confirmed_will_review_effects": False,
        "confirmed_no_automatic_execution": False,
        "approved_exact_command_sha256": None,
        "authorized_run_id": None,
    }, "real-world operator approval cannot be encoded in public proposal")
    require(p["results"] == {
        "g2a_runtime": "NOT_ASSESSED",
        "g2b": "NOT_AUTHORIZED", "g2c": "NOT_AUTHORIZED",
        "g2d": "NOT_AUTHORIZED", "g3": "NOT_AUTHORIZED",
        "real_g2a_authorized": False,
    }, "no G2 result or authorization is present")
    return {"source_only_packet": "PASS",
            "operator_approval": "NOT_REQUESTED",
            "g2a_execution": "NOT_AUTHORIZED",
            "downstream": "NOT_AUTHORIZED"}


def load_packet() -> dict:
    with PACKET.open("r", encoding="utf-8") as stream:
        return json.load(stream)
