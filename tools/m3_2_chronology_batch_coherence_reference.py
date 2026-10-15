"""Stage31: synthetic read-only equivalence check for explicitly requested pairs.

A group contains ONLY an identical unordered pair already requested. It is
NOT a connected component, invented time sorting, or inferred new comparison.
The source batch is recalculated from the same in-memory snapshot (Stage30).
No SQLite, operator archive, file I/O, IPC, permission or writing.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json

from m3_2_chronology_comparison_batch_reference import (
    SyntheticComparisonBatch, review_comparison_batch,
)
from m3_2_chronology_navigation_reference import NavigationFilters
from m3_2_supersession_reference import ProposalRejected, SyntheticSnapshot

_INVERSE = {
    "before": "after",
    "after": "before",
    "same": "same",
    "incomparable": "incomparable",
}


@dataclass(frozen=True)
class PairConsistencyEntry:
    request_ordinal: int
    first_request_ordinal: int
    unordered_pair_group_ordinal: int
    left_anchor_id: str
    right_anchor_id: str
    relation: str
    orientation: str


@dataclass(frozen=True)
class SyntheticBatchCoherence:
    universe_id: str
    batch: SyntheticComparisonBatch
    entries: tuple[PairConsistencyEntry, ...]
    unordered_pair_group_count: int
    grouping_semantics: str = "same_explicit_unordered_endpoint_pair_only"
    request_order_semantics: str = "source_request_order_not_world_time"
    cross_pair_temporal_inference: str = "not_attempted"
    editing_authorized: bool = False
    data_origin: str = "synthetic_in_memory_reference_only"


def _check_batch_consistency(
    batch: SyntheticComparisonBatch,
) -> tuple[tuple[PairConsistencyEntry, ...], int]:
    """Defensive internal invariant checker. Never authorization or attestation."""
    if not isinstance(batch, SyntheticComparisonBatch):
        raise ProposalRejected("coherence_batch_type_invalid")
    first_seen: dict[frozenset[str], tuple[int, int, str, str, str, tuple[str, ...]]] = {}
    entries = []
    for ordinal, item in enumerate(batch.items, 1):
        if item.request_ordinal != ordinal:
            raise ProposalRejected("coherence_request_order_invalid")
        review = item.review
        left = review.left.anchor_id
        right = review.right.anchor_id
        witness = review.witness_page
        if (review.universe_id != batch.universe_id or
                witness.universe_id != batch.universe_id or
                witness.left_anchor_id != left or
                witness.right_anchor_id != right):
            raise ProposalRejected("coherence_scope_mismatch")
        relation = witness.relation
        if relation not in _INVERSE or (left == right) != (relation == "same"):
            raise ProposalRejected("coherence_relation_invalid")
        links = tuple(step.precedence_id for step in witness.evidence_steps)
        if (relation in ("same", "incomparable") and
                (links or witness.total_evidence_links != 0)):
            raise ProposalRejected("coherence_evidence_invalid")
        if (relation in ("before", "after") and
                (not links or witness.total_evidence_links < len(links))):
            raise ProposalRejected("coherence_evidence_invalid")
        key = frozenset((left, right))
        first = first_seen.get(key)
        if first is None:
            group_number = len(first_seen) + 1
            first_seen[key] = (ordinal, group_number, left, right, relation, links)
            origin_ordinal, orientation = ordinal, "first"
        else:
            origin_ordinal, group_number, first_left, first_right, first_rel, first_links = first
            if (left, right) == (first_left, first_right):
                orientation = "repeated"
                expected_relation = first_rel
            elif (left, right) == (first_right, first_left):
                orientation = "reversed"
                expected_relation = _INVERSE[first_rel]
            else:
                raise ProposalRejected("coherence_pair_group_invalid")
            if relation != expected_relation or links != first_links:
                raise ProposalRejected("coherence_repeated_pair_conflict")
        entries.append(PairConsistencyEntry(
            ordinal, origin_ordinal, group_number, left, right,
            relation, orientation,
        ))
    return tuple(entries), len(first_seen)


def audit_comparison_batch(
    snapshot: SyntheticSnapshot, universe_id: str,
    pairs: tuple[tuple[str, str], ...], *,
    filters: NavigationFilters = NavigationFilters(),
    navigation_page_size: int = 32,
    witness_page_size: int = 16,
) -> SyntheticBatchCoherence:
    """Recompute, check, and present ONLY explicitly supplied 1..16 pairs."""
    batch = review_comparison_batch(
        snapshot, universe_id, pairs,
        filters=filters,
        navigation_page_size=navigation_page_size,
        witness_page_size=witness_page_size,
    )
    entries, group_count = _check_batch_consistency(batch)
    return SyntheticBatchCoherence(
        universe_id, batch, entries, group_count,
    )


def batch_coherence_json(report: SyntheticBatchCoherence) -> str:
    """Deterministic DTO example; not a live API, signature or proof."""
    if not isinstance(report, SyntheticBatchCoherence):
        raise ProposalRejected("coherence_result_type_invalid")
    return json.dumps(
        asdict(report), sort_keys=True, ensure_ascii=True,
        separators=(",", ":"), allow_nan=False,
    )
