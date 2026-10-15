"""M3.2 Stage27: synthetic read-only presentation of authored order witnesses.

No interface, IPC, SQLite, files, authenticated permission or date conversion.
A witness is recomputed from a single immutable synthetic snapshot and a
validated Stage25/26 endpoint selection; we do not trust caller-supplied proof.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json

from m3_2_chronology_navigation_reference import NavigationFilters
from m3_2_chronology_witness_reference import explain_filtered_world_order
from m3_2_supersession_reference import ProposalRejected, SyntheticSnapshot

RELATION_MESSAGES = {
    "same": "same_selected_anchor_id",
    "before": "left_precedes_right_by_authored_links",
    "after": "right_precedes_left_by_authored_links",
    "incomparable": "relative_world_order_not_established",
}
RELATION_EVIDENCE = {
    "same": "same_identity_no_precedence_required",
    "before": "one_shortest_authored_chain",
    "after": "one_shortest_authored_chain",
    "incomparable": "no_authored_path_either_direction",
}


@dataclass(frozen=True)
class WitnessDisplayStep:
    """Link number means witness-path position, NOT a world-time coordinate."""

    link_number: int
    before_anchor_id: str
    precedence_id: str
    after_anchor_id: str


@dataclass(frozen=True)
class WorldOrderWitnessPanel:
    universe_id: str
    left_anchor_id: str
    right_anchor_id: str
    relation: str
    relation_message_key: str
    evidence_state: str
    evidence_steps: tuple[WitnessDisplayStep, ...]
    path_start_anchor_id: str | None
    path_end_anchor_id: str | None
    witness_semantics: str = "example_chain_not_unique_world_order"
    evidence_visibility: str = "identifiers_only"
    narration_order: str = "not_available_in_synthetic_projection"
    reader_reveal_order: str = "not_available_in_synthetic_projection"
    editing_authorized: bool = False
    data_origin: str = "synthetic_in_memory_reference_only"


def present_world_order_witness(
    snapshot: SyntheticSnapshot,
    universe_id: str,
    left_anchor_id: str,
    right_anchor_id: str,
    *,
    filters: NavigationFilters = NavigationFilters(),
) -> WorldOrderWitnessPanel:
    """Revalidate endpoints and show only one human-authored shortest chain.

    Filter selection is not permission. Intermediate anchors can be outside
    display text filters; this synthetic DTO intentionally returns IDs only.
    """
    witness = explain_filtered_world_order(
        snapshot, universe_id, left_anchor_id, right_anchor_id, filters=filters
    )
    relation = witness.relation
    if relation not in RELATION_MESSAGES:
        raise ProposalRejected("witness_panel_relation_invalid")
    node_ids = witness.chain_anchor_ids
    edge_ids = witness.chain_precedence_ids
    if relation in ("before", "after"):
        if len(node_ids) != len(edge_ids) + 1 or not edge_ids:
            raise ProposalRejected("witness_panel_chain_invalid")
        steps = tuple(
            WitnessDisplayStep(index + 1, node_ids[index], edge_id,
                               node_ids[index + 1])
            for index, edge_id in enumerate(edge_ids)
        )
        path_start, path_end = node_ids[0], node_ids[-1]
    elif relation == "same":
        if node_ids != (left_anchor_id,) or edge_ids:
            raise ProposalRejected("witness_panel_chain_invalid")
        steps = ()
        path_start = path_end = left_anchor_id
    else:
        if node_ids or edge_ids:
            raise ProposalRejected("witness_panel_chain_invalid")
        steps = ()
        path_start = path_end = None
    return WorldOrderWitnessPanel(
        universe_id, left_anchor_id, right_anchor_id,
        relation, RELATION_MESSAGES[relation], RELATION_EVIDENCE[relation],
        steps, path_start, path_end,
    )


def witness_panel_json(panel: WorldOrderWitnessPanel) -> str:
    """Deterministic JSON sample, NOT an enabled API, proof or auth token."""
    if not isinstance(panel, WorldOrderWitnessPanel):
        raise ProposalRejected("witness_panel_type_invalid")
    return json.dumps(
        asdict(panel), sort_keys=True, ensure_ascii=True,
        separators=(",", ":"), allow_nan=False,
    )
