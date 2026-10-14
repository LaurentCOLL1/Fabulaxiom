"""M3.2 Stage29: coherent synthetic selection review across navigation pages.

Pure in-memory ID-only presentation. Filtered-source position is NOT world
chronology. Cursors are consistency hints, not permission, signed evidence,
or a React/Tauri IPC interface. No filesystem, SQLite or operator state.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json

from m3_2_chronology_comparison_reference import compare_filtered_anchors
from m3_2_chronology_navigation_reference import (
    NavigationFilters, _filter_fingerprint, _matches, navigate_chronology,
)
from m3_2_chronology_pagination_reference import MAX_PAGE_SIZE, _encode_cursor
from m3_2_chronology_projection_reference import inspect_anchor
from m3_2_chronology_witness_consultation_reference import (
    WitnessConsultationPage, consult_world_order_witness,
)
from m3_2_supersession_reference import ProposalRejected, SyntheticSnapshot


@dataclass(frozen=True)
class SelectedAnchorLocation:
    anchor_id: str
    filtered_source_ordinal: int
    navigation_page_ordinal: int
    ordinal_on_navigation_page: int
    navigation_cursor: str | None


@dataclass(frozen=True)
class SyntheticSelectionReview:
    universe_id: str
    left: SelectedAnchorLocation
    right: SelectedAnchorLocation
    filtered_anchor_count: int
    navigation_page_size: int
    witness_page: WitnessConsultationPage
    display_order_semantics: str = "source_insertion_order_not_world_time"
    selection_semantics: str = "two_explicit_active_filtered_ids"
    editing_authorized: bool = False
    data_origin: str = "synthetic_in_memory_reference_only"


def review_selected_witness(
    snapshot: SyntheticSnapshot, universe_id: str,
    left_anchor_id: str, right_anchor_id: str, *,
    filters: NavigationFilters = NavigationFilters(),
    navigation_page_size: int = 32,
    witness_page_size: int = 16,
    witness_cursor: str | None = None,
) -> SyntheticSelectionReview:
    """Locate explicit selections in Stage24 navigation and Stage28 evidence.

    Each locator is rechecked against the current Stage24 navigation page.
    Switching navigation page width changes locators but NOT authored world
    precedence; switching witness page width invalidates its own old cursor.
    """
    if type(navigation_page_size) is not int or not 1 <= navigation_page_size <= MAX_PAGE_SIZE:
        raise ProposalRejected("selection_navigation_page_size_invalid")

    # Stage25 independently validates active same-Universe filtered endpoint
    # identities; no selection token or page cursor is treated as authority.
    pair = compare_filtered_anchors(
        snapshot, universe_id, left_anchor_id, right_anchor_id, filters=filters
    )
    witness_page = consult_world_order_witness(
        snapshot, universe_id, left_anchor_id, right_anchor_id,
        filters=filters, page_size=witness_page_size, cursor=witness_cursor,
    )
    if (witness_page.relation != pair.relation or
            witness_page.left_anchor_id != left_anchor_id or
            witness_page.right_anchor_id != right_anchor_id):
        raise ProposalRejected("selection_witness_mismatch")

    positions: dict[str, int] = {}
    matched_count = 0
    targets = {left_anchor_id, right_anchor_id}
    for anchor in snapshot.anchors:
        if anchor.universe_id != universe_id:
            continue
        current = inspect_anchor(snapshot, universe_id, anchor.id)
        if _matches(anchor, current.status, filters):
            if anchor.id in targets:
                positions[anchor.id] = matched_count
            matched_count += 1
    if set(positions) != targets:
        raise ProposalRejected("selection_location_not_filtered")

    nav_fp = _filter_fingerprint(snapshot, filters, navigation_page_size)

    def locate(anchor_id: str) -> SelectedAnchorLocation:
        offset = positions[anchor_id]
        page_start = (offset // navigation_page_size) * navigation_page_size
        nav_cursor = (_encode_cursor(universe_id, nav_fp, page_start)
                      if page_start else None)
        # Explicitly assert parity with Stage24, not an invented alternate sort.
        page = navigate_chronology(
            snapshot, universe_id, filters=filters,
            page_size=navigation_page_size, cursor=nav_cursor,
        )
        within = offset - page_start
        if page.anchor_cards[within].anchor_id != anchor_id:
            raise ProposalRejected("selection_navigation_inconsistent")
        return SelectedAnchorLocation(
            anchor_id=anchor_id,
            filtered_source_ordinal=offset + 1,
            navigation_page_ordinal=page_start // navigation_page_size + 1,
            ordinal_on_navigation_page=within + 1,
            navigation_cursor=nav_cursor,
        )

    return SyntheticSelectionReview(
        universe_id, locate(left_anchor_id), locate(right_anchor_id),
        matched_count, navigation_page_size, witness_page,
    )


def selection_review_json(review: SyntheticSelectionReview) -> str:
    """Deterministic DTO example; no live IPC, authorization or attestation."""
    if not isinstance(review, SyntheticSelectionReview):
        raise ProposalRejected("selection_review_type_invalid")
    return json.dumps(
        asdict(review), ensure_ascii=True, sort_keys=True,
        separators=(",", ":"), allow_nan=False,
    )
