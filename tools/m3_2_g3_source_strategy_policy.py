"""M3.2 G3 strategy review policy. PURE DATA, synthetic-only, NEVER authorizes G3.

No filesystem, Win32 API, SQLite connection, environment, network, or operator
path is read. All booleans are untrusted declarations, not attestation.
This module does not implement a backup or accept a source/destination path.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Strategy(str, Enum):
    APP_OWNED_BACKUP = "APP_OWNED_BACKUP"
    VERIFIED_COLD_SNAPSHOT = "VERIFIED_COLD_SNAPSHOT"
    RAW_LIVE_COPY = "RAW_LIVE_COPY"
    READONLY_PATH_OPEN = "READONLY_PATH_OPEN"


@dataclass(frozen=True)
class Evidence:
    """Planning assertions from an INVENTED fixture, never proof of real state."""
    existing_trusted_owner_connection: bool = False
    source_binding_attested: bool = False
    no_new_source_open: bool = False
    no_automatic_migration: bool = False
    source_quiescence_attested: bool = False
    ancestors_identity_attested: bool = False
    source_handle_identity_attested: bool = False
    journal_state_resolved: bool = False
    no_source_mutation_plan: bool = False
    new_only_destination_plan: bool = False
    private_destination_plan: bool = False
    isolated_restoration_plan: bool = False
    memory_capacity_plan: bool = False
    explicit_operator_permission: bool = False


@dataclass(frozen=True)
class Decision:
    strategy: str
    design_review_candidate: bool
    real_g3_authorized: bool
    unmet_conditions: tuple[str, ...]
    disposition: str


_COMMON = (
    "source_binding_attested",
    "journal_state_resolved",
    "no_source_mutation_plan",
    "new_only_destination_plan",
    "private_destination_plan",
    "isolated_restoration_plan",
    "memory_capacity_plan",
    "explicit_operator_permission",
)

_OWNED = (
    "existing_trusted_owner_connection",
    "no_new_source_open",
    "no_automatic_migration",
)

_COLD = (
    "source_quiescence_attested",
    "ancestors_identity_attested",
    "source_handle_identity_attested",
)

# This code intentionally does NOT return permission to touch real sources.
# Future real authorization is a separate process with independently verified
# evidence and an operator-specific command; it MUST NOT reuse this classifier.


def classify(strategy: Strategy, evidence: Evidence) -> Decision:
    if not isinstance(strategy, Strategy) or not isinstance(evidence, Evidence):
        raise TypeError("Only an explicit synthetic Strategy and Evidence are accepted")
    if strategy in (Strategy.RAW_LIVE_COPY, Strategy.READONLY_PATH_OPEN):
        return Decision(
            strategy.value, False, False,
            ("UNSAFE_OR_UNQUALIFIED_SOURCE_OPEN",),
            "VETO_NO_REAL_SOURCE_ACCESS",
        )

    required = _COMMON + (_OWNED if strategy is Strategy.APP_OWNED_BACKUP else _COLD)
    missing = tuple(name for name in required if getattr(evidence, name) is not True)

    # Even claims with all booleans true are NOT a production attestation.
    candidate = not missing
    return Decision(
        strategy.value,
        candidate,
        False,
        missing,
        "SYNTHETIC_DESIGN_REVIEW_ONLY" if candidate else "VETO_MISSING_EVIDENCE",
    )


def preferred_strategy(*, app_connection_preexists: bool, source_quiescence_proven: bool) -> str:
    """Simple decision-table routing, not an authorization."""
    if app_connection_preexists:
        return Strategy.APP_OWNED_BACKUP.value
    if source_quiescence_proven:
        return Strategy.VERIFIED_COLD_SNAPSHOT.value
    return "NO_ELIGIBLE_STRATEGY_STOP"


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="G3 synthetic policy-only review")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if not args.self_test:
        parser.error("Only --self-test is supported; no paths or real backups")
    for choice in Strategy:
        decision = classify(choice, Evidence())
        if decision.real_g3_authorized:
            raise RuntimeError("production authorization invariant violated")
        print(f"{choice.value}: {decision.disposition}")
    assert preferred_strategy(
        app_connection_preexists=False, source_quiescence_proven=False
    ) == "NO_ELIGIBLE_STRATEGY_STOP"


if __name__ == "__main__":
    main()
