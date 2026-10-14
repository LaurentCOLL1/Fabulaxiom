"""M3.2 Stage 24: purely synthetic read-only chronology navigation/filtering.

This references only the accepted Stage20-23 immutable in-memory model.
No SQLite, filesystem, network, React, Tauri IPC or operator data access.
Cursors identify a synthetic snapshot+filter combination for consistency,
not authentication, digital signatures or independent evidence attestation.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json

from m3_2_chronology_pagination_reference import (
    MAX_PAGE_SIZE, _decode_cursor, _encode_cursor, _fingerprint,
)
from m3_2_chronology_presentation_reference import AnchorCard
from m3_2_chronology_projection_reference import inspect_anchor, lineage
from m3_2_supersession_reference import ProposalRejected, SyntheticSnapshot

VALID_STATUSES = frozenset(("active", "replaced", "withdrawn"))
VALID_TIME_KINDS = frozenset(("exact", "approximate", "relative", "unknown"))
MAX_QUERY_CHARACTERS = 128


@dataclass(frozen=True)
class NavigationFilters:
    statuses: tuple[str, ...] = ()
    time_kinds: tuple[str, ...] = ()
    calendar_id: str | None = None
    source_revision_id: str | None = None
    text_contains: str | None = None


@dataclass(frozen=True)
class NavigationPage:
    universe_id: str
    filters: NavigationFilters
    anchor_cards: tuple[AnchorCard, ...]
    total_matches: int
    next_cursor: str | None
    previous_cursor: str | None
    display_order_semantics: str = "source_insertion_order_not_world_time"
    editing_authorized: bool = False
    data_origin: str = "synthetic_in_memory_reference_only"


def _validate_selection(values: object, allowed: frozenset[str], name: str) -> None:
    if (not isinstance(values, tuple) or len(values) > len(allowed)
            or any(type(value) is not str or value not in allowed
                   for value in values)
            or len(set(values)) != len(values)):
        raise ProposalRejected(f"navigation_{name}_invalid")


def _validated_filters(filters: NavigationFilters) -> NavigationFilters:
    if not isinstance(filters, NavigationFilters):
        raise ProposalRejected("navigation_filter_type_invalid")
    _validate_selection(filters.statuses, VALID_STATUSES, "statuses")
    _validate_selection(filters.time_kinds, VALID_TIME_KINDS, "time_kinds")
    for name, value in (("calendar_id", filters.calendar_id),
                        ("source_revision_id", filters.source_revision_id)):
        if value is not None and (type(value) is not str or not value.strip()
                                  or len(value) > 256):
            raise ProposalRejected(f"navigation_{name}_invalid")
    if filters.text_contains is not None and (
        type(filters.text_contains) is not str
        or not filters.text_contains.strip()
        or len(filters.text_contains) > MAX_QUERY_CHARACTERS
    ):
        raise ProposalRejected("navigation_text_contains_invalid")
    return filters


def _filter_fingerprint(snapshot: SyntheticSnapshot,
                        filters: NavigationFilters) -> str:
    representation = json.dumps(
        {"snapshot": _fingerprint(snapshot), "filters": asdict(filters)},
        ensure_ascii=True, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    )
    return hashlib.sha256(representation.encode("utf-8")).hexdigest()


def _matches(anchor, status: str, filters: NavigationFilters) -> bool:
    if filters.statuses and status not in filters.statuses:
        return False
    if filters.time_kinds and anchor.time_kind not in filters.time_kinds:
        return False
    if filters.calendar_id is not None and anchor.calendar_id != filters.calendar_id:
        return False
    if (filters.source_revision_id is not None
            and anchor.source_revision_id != filters.source_revision_id):
        return False
    if filters.text_contains is not None:
        term = filters.text_contains.strip().casefold()
        fields = (anchor.exact_label, anchor.window_start_text,
                  anchor.window_end_text, anchor.precision_text)
        if not any(isinstance(value, str) and term in value.casefold()
                   for value in fields):
            return False
    return True


def navigate_chronology(
    snapshot: SyntheticSnapshot, universe_id: str, *,
    filters: NavigationFilters = NavigationFilters(),
    page_size: int = 32,
    cursor: str | None = None,
) -> NavigationPage:
    """Filter before slicing; preserve source order as display order ONLY."""
    if not isinstance(snapshot, SyntheticSnapshot):
        raise ProposalRejected("navigation_snapshot_type_invalid")
    if type(universe_id) is not str or not universe_id.strip():
        raise ProposalRejected("navigation_universe_required")
    if type(page_size) is not int or not 1 <= page_size <= MAX_PAGE_SIZE:
        raise ProposalRejected("navigation_page_size_invalid")
    filters = _validated_filters(filters)
    fp = _filter_fingerprint(snapshot, filters)

    matching = []
    for anchor in snapshot.anchors:
        if anchor.universe_id != universe_id:
            continue
        row = inspect_anchor(snapshot, universe_id, anchor.id)
        if _matches(anchor, row.status, filters):
            matching.append(row)
    total = len(matching)

    offset = 0
    if cursor is not None:
        decoded = _decode_cursor(cursor)
        if decoded["u"] != universe_id:
            raise ProposalRejected("navigation_cursor_wrong_universe")
        if decoded["fp"] != fp:
            raise ProposalRejected("navigation_cursor_stale_snapshot_or_filters")
        offset = decoded["offset"]
        if offset < 0 or offset >= total:
            raise ProposalRejected("navigation_cursor_offset_invalid")

    cards = []
    for row in matching[offset:offset + page_size]:
        anchor = row.anchor
        history = lineage(snapshot, universe_id, anchor.id)
        cards.append(AnchorCard(
            anchor.id, anchor.universe_id, anchor.time_kind,
            anchor.calendar_id, anchor.exact_label, anchor.window_start_text,
            anchor.window_end_text, anchor.precision_text,
            anchor.source_revision_id, row.status,
            row.next_anchor_id, row.reason, history.anchor_ids,
            history.event_ids, history.reasons, history.disposition,
        ))
    next_offset = offset + len(cards)
    return NavigationPage(
        universe_id=universe_id,
        filters=filters,
        anchor_cards=tuple(cards),
        total_matches=total,
        next_cursor=(_encode_cursor(universe_id, fp, next_offset)
                     if next_offset < total else None),
        previous_cursor=(_encode_cursor(universe_id, fp, max(0, offset - page_size))
                         if offset > 0 else None),
    )


def navigation_json(page: NavigationPage) -> str:
    if not isinstance(page, NavigationPage):
        raise ProposalRejected("navigation_page_type_invalid")
    return json.dumps(asdict(page), ensure_ascii=True, sort_keys=True,
                      separators=(",", ":"), allow_nan=False)
