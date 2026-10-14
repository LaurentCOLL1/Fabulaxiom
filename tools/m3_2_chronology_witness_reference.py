"""M3.2 Stage 26: explain an explicit synthetic world-order comparison.

Only immutable in-memory Stage 20-25 objects. Never read real SQLite,
calendars, operator files, backups or build an application IPC/UI.
A witness is ONE shortest chain of authored precedence IDs, NOT a unique
world chronology, provenance attestation or an authorization token.
"""
from __future__ import annotations

from collections import deque
from dataclasses import asdict, dataclass
import json

from m3_2_chronology_comparison_reference import compare_filtered_anchors
from m3_2_chronology_navigation_reference import NavigationFilters
from m3_2_supersession_reference import ProposalRejected, SyntheticSnapshot


@dataclass(frozen=True)
class WorldOrderWitness:
    universe_id: str
    left_anchor_id: str
    right_anchor_id: str
    relation: str
    chain_anchor_ids: tuple[str, ...]
    chain_precedence_ids: tuple[str, ...]
    chain_semantics: str = "one_shortest_authored_precedence_chain"
    narration_order: str = "not_available_in_synthetic_projection"
    reader_reveal_order: str = "not_available_in_synthetic_projection"
    editing_authorized: bool = False
    data_origin: str = "synthetic_in_memory_reference_only"


def _shortest_authored_chain(
    snapshot: SyntheticSnapshot, universe_id: str, start: str, goal: str
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Breadth-first: fewest edges, stable tie by SOURCE edge insertion only."""
    graph: dict[str, list[tuple[str, str]]] = {}
    active = snapshot.active_anchor_ids
    for edge in snapshot.precedences:
        if edge.universe_id != universe_id:
            continue
        # Stage 20 snapshot prevents this, but fail closed if it ever changes.
        if (edge.before_anchor_id not in active or
                edge.after_anchor_id not in active):
            raise ProposalRejected("witness_inactive_historical_edge")
        graph.setdefault(edge.before_anchor_id, []).append(
            (edge.after_anchor_id, edge.id)
        )

    queue = deque([start])
    parents: dict[str, tuple[str, str] | None] = {start: None}
    while queue and goal not in parents:
        current = queue.popleft()
        for following, edge_id in graph.get(current, ()):
            if following in parents:
                continue
            parents[following] = (current, edge_id)
            queue.append(following)
            if following == goal:
                break

    if goal not in parents:
        raise ProposalRejected("witness_comparable_without_explicit_path")

    nodes = [goal]
    edges = []
    cursor = goal
    while cursor != start:
        parent = parents[cursor]
        if parent is None:
            raise ProposalRejected("witness_comparable_without_explicit_path")
        previous, edge_id = parent
        nodes.append(previous)
        edges.append(edge_id)
        cursor = previous
    return tuple(reversed(nodes)), tuple(reversed(edges))


def explain_filtered_world_order(
    snapshot: SyntheticSnapshot,
    universe_id: str,
    left_anchor_id: str,
    right_anchor_id: str,
    *,
    filters: NavigationFilters = NavigationFilters(),
) -> WorldOrderWitness:
    """Explain an authorized-by-selection (NOT security) Stage25 result.

    Endpoint visibility/status is revalidated through Stage25; intermediate
    IDs may fall outside the display text filter but are always in the same
    synthetic Universe. Only IDs, never source labels or protected values,
    are emitted for the shortest witness.
    """
    comparison = compare_filtered_anchors(
        snapshot, universe_id, left_anchor_id, right_anchor_id, filters=filters
    )
    if comparison.relation == "same":
        anchors = (left_anchor_id,)
        precedences: tuple[str, ...] = ()
    elif comparison.relation == "incomparable":
        anchors = ()
        precedences = ()
    else:
        # Witness always follows authored "before -> after" direction,
        # even when the selected left anchor is AFTER the selected right.
        before, after = ((left_anchor_id, right_anchor_id)
                         if comparison.relation == "before"
                         else (right_anchor_id, left_anchor_id))
        anchors, precedences = _shortest_authored_chain(
            snapshot, universe_id, before, after
        )
    return WorldOrderWitness(
        universe_id, left_anchor_id, right_anchor_id,
        comparison.relation, anchors, precedences,
    )


def world_order_witness_json(witness: WorldOrderWitness) -> str:
    """Deterministic DTO serialization; not a runtime API or signature."""
    if not isinstance(witness, WorldOrderWitness):
        raise ProposalRejected("witness_result_type_invalid")
    return json.dumps(
        asdict(witness), sort_keys=True, separators=(",", ":"),
        ensure_ascii=True, allow_nan=False,
    )
