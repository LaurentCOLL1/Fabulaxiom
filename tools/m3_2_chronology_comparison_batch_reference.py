"""M3.2 Stage30: bounded batch of explicit synthetic chronology comparisons.

Each pair is independently revalidated by Stages 25-29, never combined
into a total fictional timeline. Only the first witness page per pair is
returned. No real SQLite, filesystem, IPC, user data or authorization.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json

from m3_2_chronology_navigation_reference import (
    NavigationFilters, _validated_filters,
)
from m3_2_chronology_selection_review_reference import (
    SyntheticSelectionReview, review_selected_witness,
)
from m3_2_supersession_reference import ProposalRejected, SyntheticSnapshot

MAX_COMPARISON_PAIRS = 16


@dataclass(frozen=True)
class BatchComparisonItem:
    request_ordinal: int
    review: SyntheticSelectionReview


@dataclass(frozen=True)
class SyntheticComparisonBatch:
    universe_id: str
    items: tuple[BatchComparisonItem, ...]
    navigation_page_size: int
    witness_page_size: int
    request_order_semantics: str = "explicit_pair_request_order_not_world_time"
    partial_results_authorized: bool = False
    editing_authorized: bool = False
    data_origin: str = "synthetic_in_memory_reference_only"


def review_comparison_batch(
    snapshot: SyntheticSnapshot,
    universe_id: str,
    pairs: tuple[tuple[str, str], ...], *,
    filters: NavigationFilters = NavigationFilters(),
    navigation_page_size: int = 32,
    witness_page_size: int = 16,
) -> SyntheticComparisonBatch:
    """All-or-nothing review of 1..16 explicitly supplied ordered pairs.

    Repeated pairs and reversed pairs remain separate review requests. Each
    nested review is validated against the same immutable snapshot, Universe
    and raw navigation filters. This function does not accept prior cursors
    or caller-supplied witness assertions.
    """
    if type(pairs) is not tuple or not 1 <= len(pairs) <= MAX_COMPARISON_PAIRS:
        raise ProposalRejected("batch_pair_count_or_type_invalid")
    for pair in pairs:
        if type(pair) is not tuple or len(pair) != 2:
            raise ProposalRejected("batch_pair_shape_invalid")

    # Validate common conditions before constructing any output. Stage29 and
    # Stage25 will additionally reject invalid IDs, widths or historical
    # selections; no partial list is returned on an error.
    if not isinstance(snapshot, SyntheticSnapshot):
        raise ProposalRejected("comparison_snapshot_type_invalid")
    if type(universe_id) is not str or not universe_id.strip():
        raise ProposalRejected("comparison_universe_required")
    _validated_filters(filters)

    items = []
    for index, (left_id, right_id) in enumerate(pairs, 1):
        review = review_selected_witness(
            snapshot, universe_id, left_id, right_id,
            filters=filters, navigation_page_size=navigation_page_size,
            witness_page_size=witness_page_size,
        )
        items.append(BatchComparisonItem(index, review))

    return SyntheticComparisonBatch(
        universe_id, tuple(items), navigation_page_size, witness_page_size,
    )


def comparison_batch_json(batch: SyntheticComparisonBatch) -> str:
    """Deterministic sample serialization, not a live transport or token."""
    if not isinstance(batch, SyntheticComparisonBatch):
        raise ProposalRejected("batch_result_type_invalid")
    return json.dumps(asdict(batch), sort_keys=True, ensure_ascii=True,
                      separators=(",", ":"), allow_nan=False)
