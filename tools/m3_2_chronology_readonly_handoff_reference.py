"""M3.2 Stage32: compact ID-only reference for a FUTURE read-only UI.

Pure in-memory Python, NOT a Tauri command, React UI, SQLite accessor or
permission to read protected operator sources. Snapshot and pair selections
are revalidated by Stage31; no caller-supplied serialized "proof" is trusted.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json

from m3_2_chronology_batch_coherence_reference import audit_comparison_batch
from m3_2_chronology_navigation_reference import NavigationFilters
from m3_2_supersession_reference import ProposalRejected, SyntheticSnapshot


_MESSAGES = {
    "before": "explicit_left_precedes_right",
    "after": "explicit_right_precedes_left",
    "same": "same_selected_anchor",
    "incomparable": "no_relative_world_order_established",
}

_BLOCKERS = (
    "external_history_attestation_not_verified_by_this_reference",
    "operator_offline_acceptance_not_performed_by_this_reference",
    "runtime_activation_not_authorized_by_this_reference",
)


@dataclass(frozen=True)
class ReadonlyComparisonPreview:
    request_ordinal: int
    unordered_pair_group_ordinal: int
    first_request_ordinal: int
    orientation: str
    left_anchor_id: str
    right_anchor_id: str
    left_filtered_source_ordinal: int
    right_filtered_source_ordinal: int
    relation: str
    relation_message_key: str
    first_page_precedence_ids: tuple[str, ...]
    total_evidence_links: int
    evidence_continues: bool


@dataclass(frozen=True)
class ReadonlyChronologyHandoff:
    universe_id: str
    comparisons: tuple[ReadonlyComparisonPreview, ...]
    number_of_requests: int
    number_of_unordered_pair_groups: int
    world_time_basis: str = "explicit_authored_precedence_only"
    navigation_order: str = "filtered_source_insertion_not_world_time"
    narration_order: str = "not_available_in_synthetic_projection"
    reader_reveal_order: str = "not_available_in_synthetic_projection"
    runtime_integration: str = "not_implemented"
    database_access: str = "none"
    write_commands: tuple[str, ...] = ()
    editing_authorized: bool = False
    external_attestation_verified: bool = False
    operator_acceptance_verified: bool = False
    blocked_requirements: tuple[str, ...] = _BLOCKERS
    data_origin: str = "synthetic_in_memory_reference_only"


def build_readonly_chronology_handoff(
    snapshot: SyntheticSnapshot,
    universe_id: str,
    pairs: tuple[tuple[str, str], ...],
    *,
    filters: NavigationFilters = NavigationFilters(),
    navigation_page_size: int = 32,
    witness_page_size: int = 16,
) -> ReadonlyChronologyHandoff:
    """Return UI-shaped sample data without enabling any UI.

    Only explicitly supplied 1..16 pairs. Requests are never sorted or
    automatically generated. Each pair is checked by Stages 25–31 against a
    single in-memory snapshot; any error rejects the whole handoff.
    """
    report = audit_comparison_batch(
        snapshot, universe_id, pairs, filters=filters,
        navigation_page_size=navigation_page_size,
        witness_page_size=witness_page_size,
    )
    if len(report.entries) != len(report.batch.items):
        raise ProposalRejected("handoff_report_length_inconsistent")

    rows: list[ReadonlyComparisonPreview] = []
    for entry, item in zip(report.entries, report.batch.items):
        review = item.review
        page = review.witness_page
        if (
            entry.request_ordinal != item.request_ordinal
            or entry.left_anchor_id != review.left.anchor_id
            or entry.right_anchor_id != review.right.anchor_id
            or entry.relation != page.relation
            or page.relation not in _MESSAGES
        ):
            raise ProposalRejected("handoff_comparison_mismatch")
        links = tuple(step.precedence_id for step in page.evidence_steps)
        if page.total_evidence_links < len(links):
            raise ProposalRejected("handoff_evidence_count_invalid")
        if page.relation in ("same", "incomparable") and (
            links or page.total_evidence_links
        ):
            raise ProposalRejected("handoff_evidence_count_invalid")
        rows.append(ReadonlyComparisonPreview(
            request_ordinal=entry.request_ordinal,
            unordered_pair_group_ordinal=entry.unordered_pair_group_ordinal,
            first_request_ordinal=entry.first_request_ordinal,
            orientation=entry.orientation,
            left_anchor_id=entry.left_anchor_id,
            right_anchor_id=entry.right_anchor_id,
            left_filtered_source_ordinal=review.left.filtered_source_ordinal,
            right_filtered_source_ordinal=review.right.filtered_source_ordinal,
            relation=page.relation,
            relation_message_key=_MESSAGES[page.relation],
            first_page_precedence_ids=links,
            total_evidence_links=page.total_evidence_links,
            evidence_continues=page.next_cursor is not None,
        ))
    return ReadonlyChronologyHandoff(
        universe_id=universe_id,
        comparisons=tuple(rows),
        number_of_requests=len(rows),
        number_of_unordered_pair_groups=report.unordered_pair_group_count,
    )


def readonly_handoff_json(handoff: ReadonlyChronologyHandoff) -> str:
    """Deterministic demonstration DTO, not a signed transport or API."""
    if not isinstance(handoff, ReadonlyChronologyHandoff):
        raise ProposalRejected("handoff_result_type_invalid")
    return json.dumps(
        asdict(handoff), sort_keys=True, ensure_ascii=True,
        separators=(",", ":"), allow_nan=False,
    )
