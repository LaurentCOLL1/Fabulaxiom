"""M3.2 Stage 23 — synthetic-only, bounded read-only chronology pagination.

No SQLite, filesystem, React/Tauri IPC or production identity. Cursor digests
are consistency guards for snapshots, NOT signatures or access authorization.
"""
from __future__ import annotations

import base64
from dataclasses import asdict, dataclass
import hashlib
import json

from m3_2_chronology_projection_reference import lineage
from m3_2_chronology_presentation_reference import AnchorCard
from m3_2_supersession_reference import ProposalRejected, SyntheticSnapshot

MAX_PAGE_SIZE = 64
MAX_CURSOR_BYTES = 4096
CURSOR_VERSION = 1


@dataclass(frozen=True)
class ChronologyPage:
    universe_id: str
    anchors: tuple[AnchorCard, ...]
    next_cursor: str | None
    display_order_semantics: str = "source_insertion_order_not_world_time"
    edit_controls_available: bool = False
    data_origin: str = "synthetic_in_memory_reference_only"


def _fingerprint(snapshot: SyntheticSnapshot) -> str:
    # Deterministic snapshot identity, *not* a security MAC or authority hash.
    return hashlib.sha256(repr(snapshot).encode("utf-8")).hexdigest()


def _strict_object(pairs: list[tuple[str, object]]) -> dict:
    result: dict = {}
    for key, value in pairs:
        if key in result:
            raise ProposalRejected("pagination_cursor_duplicate_key")
        result[key] = value
    return result


def _bad_constant(_value: str) -> None:
    raise ProposalRejected("pagination_cursor_invalid_constant")


def _decode_cursor(cursor: str) -> dict:
    if not isinstance(cursor, str) or not 0 < len(cursor) <= MAX_CURSOR_BYTES:
        raise ProposalRejected("pagination_cursor_shape_invalid")
    try:
        raw = base64.b64decode(cursor.encode("ascii"), altchars=b"-_", validate=True)
        if not 0 < len(raw) <= MAX_CURSOR_BYTES:
            raise ValueError("cursor too long")
        data = json.loads(raw.decode("utf-8"), object_pairs_hook=_strict_object,
                          parse_constant=_bad_constant)
    except (ValueError, UnicodeError, base64.binascii.Error) as exc:
        raise ProposalRejected("pagination_cursor_invalid_encoding") from exc
    if not isinstance(data, dict) or set(data) != {"v", "u", "fp", "offset"}:
        raise ProposalRejected("pagination_cursor_shape_invalid")
    if type(data["v"]) is not int or data["v"] != CURSOR_VERSION:
        raise ProposalRejected("pagination_cursor_version_invalid")
    if not isinstance(data["u"], str) or not isinstance(data["fp"], str):
        raise ProposalRejected("pagination_cursor_shape_invalid")
    if type(data["offset"]) is not int:
        raise ProposalRejected("pagination_cursor_offset_invalid")
    return data


def _encode_cursor(universe: str, fingerprint: str, offset: int) -> str:
    obj = {"v": CURSOR_VERSION, "u": universe, "fp": fingerprint,
           "offset": offset}
    raw = json.dumps(obj, sort_keys=True, ensure_ascii=True,
                     separators=(",", ":")).encode("ascii")
    if len(raw) > MAX_CURSOR_BYTES:
        raise ProposalRejected("pagination_cursor_too_long")
    return base64.urlsafe_b64encode(raw).decode("ascii")


def chronology_page(snapshot: SyntheticSnapshot, universe: str, *,
                    page_size: int = 32,
                    cursor: str | None = None) -> ChronologyPage:
    """Paginate *presentation order only*, never fictional chronological order."""
    if not isinstance(snapshot, SyntheticSnapshot):
        raise ProposalRejected("pagination_snapshot_type_invalid")
    if not isinstance(universe, str) or not universe.strip():
        raise ProposalRejected("pagination_universe_required")
    if type(page_size) is not int or not 1 <= page_size <= MAX_PAGE_SIZE:
        raise ProposalRejected("pagination_page_size_invalid")

    scoped = tuple(a for a in snapshot.anchors if a.universe_id == universe)
    fingerprint = _fingerprint(snapshot)
    offset = 0
    if cursor is not None:
        parsed = _decode_cursor(cursor)
        if parsed["u"] != universe:
            raise ProposalRejected("pagination_cursor_wrong_universe")
        if parsed["fp"] != fingerprint:
            raise ProposalRejected("pagination_cursor_stale_snapshot")
        offset = parsed["offset"]
        if offset < 0 or offset >= len(scoped):
            raise ProposalRejected("pagination_cursor_offset_invalid")

    # The source snapshot was already validated by Stage 20; it is never
    # modified or partially reconstructed for a page.
    cards = []
    supersessions = {e.old_anchor_id: e for e in snapshot.supersessions}
    for anchor in scoped[offset:offset + page_size]:
        event = supersessions.get(anchor.id)
        trail = lineage(snapshot, universe, anchor.id)
        cards.append(AnchorCard(
            anchor.id, anchor.universe_id, anchor.time_kind,
            anchor.calendar_id, anchor.exact_label, anchor.window_start_text,
            anchor.window_end_text, anchor.precision_text,
            anchor.source_revision_id,
            "active" if event is None else (
                "withdrawn" if event.new_anchor_id is None else "replaced"),
            None if event is None else event.new_anchor_id,
            None if event is None else event.reason,
            trail.anchor_ids, trail.event_ids, trail.reasons,
            trail.disposition,
        ))
    new_offset = offset + len(cards)
    next_cursor = (_encode_cursor(universe, fingerprint, new_offset)
                   if new_offset < len(scoped) else None)
    return ChronologyPage(universe, tuple(cards), next_cursor)


def chronology_page_json(page: ChronologyPage) -> str:
    if not isinstance(page, ChronologyPage):
        raise ProposalRejected("pagination_page_type_invalid")
    return json.dumps(asdict(page), sort_keys=True,
                      ensure_ascii=True, separators=(",", ":"), allow_nan=False)
