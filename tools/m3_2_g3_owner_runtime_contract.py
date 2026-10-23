"""M3.2 G3 hypothetical owner-service contract. No IO and NO authorization.

The model consumes invented declarations only. It cannot establish a trusted
runtime source, verify a Windows file, open SQLite, or grant a real G3 action.
"""
from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum


class Route(str, Enum):
    EXISTING_OWNER_SERVICE = "EXISTING_OWNER_SERVICE"
    VERIFIED_COLD_CUSTODY = "VERIFIED_COLD_CUSTODY"
    CURRENT_DATABASE_STATUS = "CURRENT_DATABASE_STATUS"
    CURRENT_APP_BACKUP = "CURRENT_APP_BACKUP"
    CURRENT_APP_RESTORE = "CURRENT_APP_RESTORE"
    RAW_LIVE_COPY = "RAW_LIVE_COPY"


@dataclass(frozen=True)
class HypotheticalEvidence:
    """UNTRUSTED claims for a design rehearsal; NEVER actual evidence."""
    owner_connection_already_exists: bool = False
    owner_is_bound_to_original: bool = False
    source_binding_independent_of_pathname: bool = False
    no_new_original_open: bool = False
    no_migrations_or_recovery_on_original: bool = False
    owner_session_lifetime_continuous: bool = False
    owner_access_serialized: bool = False
    all_mutation_entrypoints_mediated: bool = False
    revocation_prevents_reopen: bool = False
    consistent_sqlite_snapshot_method: bool = False
    source_size_budget_verified: bool = False
    all_writers_quiescent: bool = False
    original_and_ancestors_authenticated: bool = False
    journals_resolved_without_original_mutation: bool = False
    new_only_private_output_sealed: bool = False
    independent_third_location_restore: bool = False
    operator_specific_consent: bool = False


@dataclass(frozen=True)
class DesignVerdict:
    route: str
    status: str
    missing: tuple[str, ...]
    real_g3_authorized: bool = False


_COMMON = (
    "source_binding_independent_of_pathname",
    "no_migrations_or_recovery_on_original",
    "consistent_sqlite_snapshot_method",
    "source_size_budget_verified",
    "new_only_private_output_sealed",
    "independent_third_location_restore",
    "operator_specific_consent",
)
_OWNER = (
    "owner_is_bound_to_original",
    "no_new_original_open",
    "owner_connection_already_exists",
    "owner_session_lifetime_continuous",
    "owner_access_serialized",
    "all_mutation_entrypoints_mediated",
    "revocation_prevents_reopen",
)
_COLD = (
    "all_writers_quiescent",
    "original_and_ancestors_authenticated",
    "journals_resolved_without_original_mutation",
)
_FORBIDDEN = frozenset((
    Route.CURRENT_DATABASE_STATUS,
    Route.CURRENT_APP_BACKUP,
    Route.CURRENT_APP_RESTORE,
    Route.RAW_LIVE_COPY,
))


def review(route: Route, claims: HypotheticalEvidence) -> DesignVerdict:
    """Evaluate untrusted descriptions; no I/O and no real-world capability."""
    if not isinstance(route, Route) or not isinstance(claims, HypotheticalEvidence):
        raise TypeError("explicit synthetic Route and HypotheticalEvidence required")
    if route in _FORBIDDEN:
        return DesignVerdict(route.value, "VETO_EXISTING_EFFECTFUL_OR_UNSAFE_ROUTE",
                             ("CURRENT_COMMAND_NOT_G3_AUTHORITY",))
    if route is Route.EXISTING_OWNER_SERVICE:
        required = _COMMON + _OWNER
    elif route is Route.VERIFIED_COLD_CUSTODY:
        # Cold preservation must never be mislabeled a pre-existing owner.
        required = _COMMON + _COLD
    else:
        raise TypeError("unknown route")
    missing = tuple(item for item in required if getattr(claims, item) is not True)
    return DesignVerdict(
        route.value,
        "HYPOTHETICAL_REVIEW_ONLY" if not missing else "STOP_UNPROVEN_CONDITIONS",
        missing,
        False,  # even ALL TRUE synthetic claims are not attestation or permission
    )


def current_rust_owner_status() -> DesignVerdict:
    """Source audit: no persistent, authenticated, non-migrating owner observed."""
    return review(Route.EXISTING_OWNER_SERVICE, HypotheticalEvidence())


def self_test() -> None:
    for route in Route:
        verdict = review(route, HypotheticalEvidence())
        if verdict.real_g3_authorized:
            raise RuntimeError("G3 real access would violate fail-closed policy")
        print(f"{route.value}: {verdict.status}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="No-I/O G3 design policy fixture")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if not args.self_test:
        parser.error("ONLY --self-test, no source or destination paths")
    self_test()
