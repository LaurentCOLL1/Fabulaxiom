"""M3.2 Stage 22 — bounded read-only chronology presentation DTO (synthetic).

All work is PURE IN MEMORY on Stage 20/21 frozen snapshots. This is not a
React view, an authorized Rust IPC contract, SQLite access or a migration.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json

from m3_2_chronology_projection_reference import (
    inspect_anchor, lineage, relative_world_order, universe_view,
)
from m3_2_supersession_reference import ProposalRejected, SyntheticSnapshot

MAX_VISIBLE_ANCHORS = 512
MAX_PAIR_QUERIES = 128


@dataclass(frozen=True)
class AnchorCard:
    anchor_id: str
    universe_id: str
    time_kind: str
    calendar_id: str | None
    exact_label: str | None
    window_start_text: str | None
    window_end_text: str | None
    precision_text: str | None
    source_revision_id: str | None
    status: str
    next_anchor_id: str | None
    correction_reason: str | None
    lineage_anchor_ids: tuple[str, ...]
    lineage_event_ids: tuple[str, ...]
    lineage_reasons: tuple[str, ...]
    lineage_disposition: str


@dataclass(frozen=True)
class OrderComparison:
    left_anchor_id: str
    right_anchor_id: str
    result: str


@dataclass(frozen=True)
class ChronologyReadPanel:
    universe_id: str
    display_order_semantics: str
    anchors: tuple[AnchorCard, ...]
    comparisons: tuple[OrderComparison, ...]
    narration_order: str
    reader_reveal_order: str
    edit_controls_available: bool
    data_origin: str


def present_chronology(
    snapshot: SyntheticSnapshot,
    universe_id: str,
    *,
    comparisons: tuple[tuple[str, str], ...] = (),
) -> ChronologyReadPanel:
    """Describe existing synthetic assertions only; never imply an ordered list.

    Presentation is explicitly *source insertion order*, not story-world time.
    Every requested comparison uses human precedence edges, not text or dates.
    """
    if not isinstance(comparisons, tuple) or len(comparisons) > MAX_PAIR_QUERIES:
        raise ProposalRejected("presentation_invalid_comparison_batch")
    if any(not isinstance(item, tuple) or len(item) != 2 or
           any(not isinstance(value, str) or not value for value in item)
           for item in comparisons):
        raise ProposalRejected("presentation_comparison_shape_invalid")
    if len(set(comparisons)) != len(comparisons):
        raise ProposalRejected("presentation_duplicate_comparisons")

    view = universe_view(snapshot, universe_id)
    if len(view.anchors) > MAX_VISIBLE_ANCHORS:
        raise ProposalRejected("presentation_too_many_anchors")

    items: list[AnchorCard] = []
    for row in view.anchors:
        a = row.anchor
        history = lineage(snapshot, universe_id, a.id)
        items.append(AnchorCard(
            a.id, a.universe_id, a.time_kind, a.calendar_id,
            a.exact_label, a.window_start_text, a.window_end_text,
            a.precision_text, a.source_revision_id, row.status,
            row.next_anchor_id, row.reason,
            history.anchor_ids, history.event_ids, history.reasons,
            history.disposition,
        ))
    findings = tuple(
        OrderComparison(left, right, relative_world_order(
            snapshot, universe_id, left, right))
        for left, right in comparisons
    )
    return ChronologyReadPanel(
        universe_id=universe_id,
        display_order_semantics="source_insertion_order_not_world_time",
        anchors=tuple(items),
        comparisons=findings,
        narration_order="not_available_in_synthetic_projection",
        reader_reveal_order="not_available_in_synthetic_projection",
        edit_controls_available=False,
        data_origin="synthetic_in_memory_reference_only",
    )


def presentation_json(panel: ChronologyReadPanel) -> str:
    """Deterministic JSON transport example; no filesystem or IPC calls."""
    if not isinstance(panel, ChronologyReadPanel):
        raise ProposalRejected("presentation_invalid_panel")
    return json.dumps(asdict(panel), ensure_ascii=True,
                      sort_keys=True, separators=(",", ":"), allow_nan=False)
