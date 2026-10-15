"""M3.2 Stage 21: pure synthetic read-only world chronology projection.

Not an application UI, SQLite query, migration or operator-data audit.
Never infer Gregorian order, narration order, or reader reveal order.
"""
from __future__ import annotations

from dataclasses import dataclass

from m3_2_supersession_reference import Anchor, ProposalRejected, SyntheticSnapshot


@dataclass(frozen=True)
class AnchorView:
    """Assertion in a single Universe; no edit action or invented timestamp."""

    anchor: Anchor
    status: str  # active | replaced | withdrawn
    next_anchor_id: str | None
    reason: str | None


@dataclass(frozen=True)
class LineageView:
    """Ordered, immutable identifiers and human reasons in a correction chain."""

    anchor_ids: tuple[str, ...]
    event_ids: tuple[str, ...]
    reasons: tuple[str, ...]
    disposition: str  # active | withdrawn


@dataclass(frozen=True)
class UniverseView:
    """Display-order is source insertion order; NOT fictional chronology."""

    universe_id: str
    anchors: tuple[AnchorView, ...]
    narration_order_available: bool = False
    reader_reveal_order_available: bool = False
    chronology_editing_authorized: bool = False


def _scoped_anchor(snapshot: SyntheticSnapshot, universe: str, anchor_id: str,
                   *, current: bool = False) -> Anchor:
    anchor = next((a for a in snapshot.anchors
                   if a.id == anchor_id and a.universe_id == universe), None)
    if anchor is None:
        raise ProposalRejected("projection_anchor_not_found_in_universe")
    if current and anchor_id not in snapshot.active_anchor_ids:
        raise ProposalRejected("projection_anchor_not_active")
    return anchor


def _events(snapshot: SyntheticSnapshot) -> dict[str, object]:
    return {event.old_anchor_id: event for event in snapshot.supersessions}


def inspect_anchor(snapshot: SyntheticSnapshot, universe: str,
                   anchor_id: str) -> AnchorView:
    anchor = _scoped_anchor(snapshot, universe, anchor_id)
    event = _events(snapshot).get(anchor_id)
    if event is None:
        return AnchorView(anchor, "active", None, None)
    return AnchorView(
        anchor, "withdrawn" if event.new_anchor_id is None else "replaced",
        event.new_anchor_id, event.reason,
    )


def universe_view(snapshot: SyntheticSnapshot, universe: str) -> UniverseView:
    if not isinstance(universe, str) or not universe.strip():
        raise ProposalRejected("projection_universe_required")
    views = tuple(inspect_anchor(snapshot, universe, a.id)
                  for a in snapshot.anchors if a.universe_id == universe)
    # No names, dates, revision heads or implicit sort are consulted.
    return UniverseView(universe, views)


def lineage(snapshot: SyntheticSnapshot, universe: str,
            origin_anchor_id: str) -> LineageView:
    _scoped_anchor(snapshot, universe, origin_anchor_id)
    events = _events(snapshot)
    ids = [origin_anchor_id]
    event_ids: list[str] = []
    reasons: list[str] = []
    visited = set()
    cursor = origin_anchor_id
    while cursor in events:
        if cursor in visited:
            raise ProposalRejected("projection_lineage_cycle")
        visited.add(cursor)
        event = events[cursor]
        event_ids.append(event.id)
        reasons.append(event.reason)
        if event.new_anchor_id is None:
            return LineageView(tuple(ids), tuple(event_ids), tuple(reasons),
                               "withdrawn")
        _scoped_anchor(snapshot, universe, event.new_anchor_id)
        ids.append(event.new_anchor_id)
        cursor = event.new_anchor_id
    return LineageView(tuple(ids), tuple(event_ids), tuple(reasons), "active")


def _reachable(edges: dict[str, set[str]], start: str, target: str) -> bool:
    pending = list(edges.get(start, ()))
    visited: set[str] = set()
    while pending:
        item = pending.pop()
        if item == target:
            return True
        if item in visited:
            continue
        visited.add(item)
        pending.extend(edges.get(item, ()))
    return False


def relative_world_order(snapshot: SyntheticSnapshot, universe: str,
                         left_anchor_id: str, right_anchor_id: str) -> str:
    """Return same / before / after / incomparable from HUMAN links only.

    Both endpoints must be active within the requested Universe. The existing
    synthetic snapshot already rejects cross-Universe links and cycles.
    """
    _scoped_anchor(snapshot, universe, left_anchor_id, current=True)
    _scoped_anchor(snapshot, universe, right_anchor_id, current=True)
    if left_anchor_id == right_anchor_id:
        return "same"
    edges: dict[str, set[str]] = {}
    for edge in snapshot.precedences:
        if edge.universe_id == universe:
            # Stage 20 forbids superseding endpoints with historical links.
            # Fail closed if a future model ever violates this invariant.
            if (edge.before_anchor_id not in snapshot.active_anchor_ids or
                    edge.after_anchor_id not in snapshot.active_anchor_ids):
                raise ProposalRejected("projection_inactive_historical_edge")
            edges.setdefault(edge.before_anchor_id, set()).add(
                edge.after_anchor_id
            )
    if _reachable(edges, left_anchor_id, right_anchor_id):
        return "before"
    if _reachable(edges, right_anchor_id, left_anchor_id):
        return "after"
    return "incomparable"
