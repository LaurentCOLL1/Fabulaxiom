"""M3.2 Stage28: bounded synthetic read-only consultation of witness links.

The complete Stage27 ID-only witness is recomputed from one immutable in-memory
snapshot BEFORE slicing into display pages. No SQLite, files, React/Tauri IPC,
auth, archive attestation, fictional time sorting, or production integration.
Cursors are consistency hints, NEVER signatures or access credentials.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json

from m3_2_chronology_navigation_reference import NavigationFilters
from m3_2_chronology_pagination_reference import (
    MAX_PAGE_SIZE, _decode_cursor, _encode_cursor, _fingerprint,
)
from m3_2_chronology_witness_presentation_reference import (
    WitnessDisplayStep, present_world_order_witness,
)
from m3_2_supersession_reference import ProposalRejected, SyntheticSnapshot


@dataclass(frozen=True)
class WitnessConsultationPage:
    universe_id: str
    left_anchor_id: str
    right_anchor_id: str
    relation: str
    relation_message_key: str
    evidence_state: str
    evidence_steps: tuple[WitnessDisplayStep, ...]
    total_evidence_links: int
    next_cursor: str | None
    previous_cursor: str | None
    witness_semantics: str = "example_chain_not_unique_world_order"
    evidence_visibility: str = "identifiers_only"
    narration_order: str = "not_available_in_synthetic_projection"
    reader_reveal_order: str = "not_available_in_synthetic_projection"
    editing_authorized: bool = False
    data_origin: str = "synthetic_in_memory_reference_only"


def _consultation_fingerprint(
    snapshot: SyntheticSnapshot, filters: NavigationFilters,
    left_id: str, right_id: str, page_size: int,
) -> str:
    """Raw selection+filter+width+snapshot binding, not authentication."""
    value = json.dumps(
        {"snapshot": _fingerprint(snapshot), "filters": asdict(filters),
         "left": left_id, "right": right_id, "page_size": page_size},
        sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    )
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def consult_world_order_witness(
    snapshot: SyntheticSnapshot, universe_id: str,
    left_anchor_id: str, right_anchor_id: str, *,
    filters: NavigationFilters = NavigationFilters(),
    page_size: int = 16, cursor: str | None = None,
) -> WitnessConsultationPage:
    """Page original link IDs in witness-path order, NOT world-time order."""
    if type(page_size) is not int or not 1 <= page_size <= MAX_PAGE_SIZE:
        raise ProposalRejected("consultation_page_size_invalid")

    # Stage27 revalidates the same-Universe, active, filtered endpoints and
    # independently recomputes Stage26 evidence; caller cannot supply proof.
    panel = present_world_order_witness(
        snapshot, universe_id, left_anchor_id, right_anchor_id, filters=filters
    )
    all_steps = panel.evidence_steps
    total = len(all_steps)
    fp = _consultation_fingerprint(
        snapshot, filters, left_anchor_id, right_anchor_id, page_size
    )
    offset = 0
    if cursor is not None:
        decoded = _decode_cursor(cursor)
        if decoded["u"] != universe_id:
            raise ProposalRejected("consultation_cursor_wrong_universe")
        if decoded["fp"] != fp:
            raise ProposalRejected("consultation_cursor_stale_context")
        offset = decoded["offset"]
        if offset < 0 or offset >= total or offset % page_size:
            raise ProposalRejected("consultation_cursor_offset_invalid")

    page_steps = all_steps[offset:offset + page_size]
    next_offset = offset + len(page_steps)
    return WitnessConsultationPage(
        universe_id, left_anchor_id, right_anchor_id,
        panel.relation, panel.relation_message_key, panel.evidence_state,
        page_steps, total,
        (_encode_cursor(universe_id, fp, next_offset)
         if next_offset < total else None),
        (_encode_cursor(universe_id, fp, offset - page_size)
         if offset > 0 else None),
    )


def witness_consultation_json(page: WitnessConsultationPage) -> str:
    """Deterministic JSON example, not an enabled runtime transport/API."""
    if not isinstance(page, WitnessConsultationPage):
        raise ProposalRejected("consultation_page_type_invalid")
    return json.dumps(
        asdict(page), sort_keys=True, ensure_ascii=True,
        separators=(",", ":"), allow_nan=False,
    )
