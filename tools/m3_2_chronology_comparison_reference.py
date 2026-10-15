"""M3.2 Stage 25: explicit synthetic read-only filtered anchor comparison.

No real SQLite, Tauri IPC, React editor, automatic chronology or archive read.
Both selected IDs must remain visible in the SAME filtered Universe and active.
Selections are revalidated against the supplied immutable in-memory snapshot;
no cursor or presentation object is an access-control authority.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json

from m3_2_chronology_navigation_reference import (
    NavigationFilters, _matches, _validated_filters,
)
from m3_2_chronology_projection_reference import (
    inspect_anchor, relative_world_order,
)
from m3_2_supersession_reference import ProposalRejected, SyntheticSnapshot


@dataclass(frozen=True)
class FilteredOrderComparison:
    universe_id: str
    left_anchor_id: str
    right_anchor_id: str
    relation: str
    narration_order: str = "not_available_in_synthetic_projection"
    reader_reveal_order: str = "not_available_in_synthetic_projection"
    editing_authorized: bool = False
    data_origin: str = "synthetic_in_memory_reference_only"


def compare_filtered_anchors(
    snapshot: SyntheticSnapshot,
    universe_id: str,
    left_anchor_id: str,
    right_anchor_id: str,
    *,
    filters: NavigationFilters = NavigationFilters(),
) -> FilteredOrderComparison:
    """Compare two explicitly selected visible ACTIVE anchors, across pages.

    Returns same/before/after/incomparable based solely on authored precedence
    links, never source insertion, fictional date text or calendars. A selection
    may span navigation pages, but no cursor or page is trusted as authority.
    """
    if not isinstance(snapshot, SyntheticSnapshot):
        raise ProposalRejected("comparison_snapshot_type_invalid")
    if type(universe_id) is not str or not universe_id.strip():
        raise ProposalRejected("comparison_universe_required")
    selected_ids = (left_anchor_id, right_anchor_id)
    if any(type(identifier) is not str or not identifier.strip()
           or len(identifier) > 256 for identifier in selected_ids):
        raise ProposalRejected("comparison_anchor_id_invalid")
    filters = _validated_filters(filters)

    expected = set(selected_ids)
    visible = {}
    for anchor in snapshot.anchors:
        if anchor.universe_id != universe_id or anchor.id not in expected:
            continue
        view = inspect_anchor(snapshot, universe_id, anchor.id)
        if _matches(anchor, view.status, filters):
            visible[anchor.id] = view

    # Never substitute an anchor from a different Universe or a successor.
    if set(visible) != expected:
        raise ProposalRejected("comparison_anchor_not_in_filtered_universe")
    if any(view.status != "active" for view in visible.values()):
        raise ProposalRejected("comparison_anchor_not_active")

    result = relative_world_order(
        snapshot, universe_id, left_anchor_id, right_anchor_id
    )
    return FilteredOrderComparison(
        universe_id, left_anchor_id, right_anchor_id, result,
    )


def comparison_json(result: FilteredOrderComparison) -> str:
    """Deterministic DTO example, not a signed or authorized transport."""
    if not isinstance(result, FilteredOrderComparison):
        raise ProposalRejected("comparison_result_type_invalid")
    return json.dumps(
        asdict(result), ensure_ascii=True, sort_keys=True,
        separators=(",", ":"), allow_nan=False,
    )
