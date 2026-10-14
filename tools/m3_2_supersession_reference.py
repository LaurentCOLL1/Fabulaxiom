"""M3.2 Stage 20 — SYNTHETIC-ONLY append-only anchor supersession reference.

This pure, in-memory reference model DOES NOT connect to SQLite, import
application/Tauri code, read operator files or authorize production writes.
It is a future-schema design exercise, not an implemented editor.
"""
from __future__ import annotations

from dataclasses import dataclass


class ProposalRejected(ValueError):
    """A deterministic proposal veto, not a runtime database error."""


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise ProposalRejected(code)


def _filled(value: str | None) -> bool:
    return isinstance(value, str) and bool(value.strip())


@dataclass(frozen=True)
class Anchor:
    id: str
    universe_id: str
    time_kind: str
    calendar_id: str | None = None
    exact_label: str | None = None
    window_start_text: str | None = None
    window_end_text: str | None = None
    precision_text: str | None = None
    source_revision_id: str | None = None


@dataclass(frozen=True)
class Precedence:
    id: str
    universe_id: str
    before_anchor_id: str
    after_anchor_id: str


@dataclass(frozen=True)
class Supersession:
    id: str
    universe_id: str
    old_anchor_id: str
    new_anchor_id: str | None
    reason: str


def _validate_anchor(a: Anchor) -> None:
    _require(_filled(a.id) and _filled(a.universe_id), "anchor_identity_required")
    _require(a.time_kind in ("exact", "approximate", "relative", "unknown"),
             "anchor_time_kind_invalid")
    if a.time_kind == "exact":
        _require(_filled(a.calendar_id) and _filled(a.exact_label)
                 and a.window_start_text is None and a.window_end_text is None
                 and (a.precision_text is None or _filled(a.precision_text)),
                 "anchor_exact_shape_invalid")
    elif a.time_kind == "approximate":
        _require(_filled(a.calendar_id) and a.exact_label is None
                 and (a.window_start_text is not None or a.window_end_text is not None)
                 and (a.window_start_text is None or _filled(a.window_start_text))
                 and (a.window_end_text is None or _filled(a.window_end_text))
                 and _filled(a.precision_text), "anchor_approximate_shape_invalid")
    else:
        _require(all(x is None for x in (
            a.calendar_id, a.exact_label, a.window_start_text,
            a.window_end_text, a.precision_text,
        )), "anchor_undated_shape_invalid")


@dataclass(frozen=True)
class SyntheticSnapshot:
    """Immutable tuples represent history; every proposal returns a NEW snapshot."""

    anchors: tuple[Anchor, ...]
    precedences: tuple[Precedence, ...] = ()
    supersessions: tuple[Supersession, ...] = ()

    def __post_init__(self) -> None:
        anchors = {}
        for anchor in self.anchors:
            _validate_anchor(anchor)
            _require(anchor.id not in anchors, "duplicate_anchor_id")
            anchors[anchor.id] = anchor

        pair_ids = set()
        precedence_ids = set()
        successors = {}
        for edge in self.precedences:
            _require(_filled(edge.id), "precedence_identity_required")
            _require(edge.id not in precedence_ids, "duplicate_precedence_id")
            precedence_ids.add(edge.id)
            before, after = anchors.get(edge.before_anchor_id), anchors.get(edge.after_anchor_id)
            _require(before is not None and after is not None, "precedence_anchor_missing")
            _require(before.universe_id == after.universe_id == edge.universe_id,
                     "precedence_cross_universe")
            _require(before.id != after.id, "precedence_self_edge")
            pair = (edge.before_anchor_id, edge.after_anchor_id)
            _require(pair not in pair_ids, "precedence_duplicate_pair")
            pair_ids.add(pair)
            successors.setdefault(before.id, set()).add(after.id)

        for first in anchors:
            pending, seen = list(successors.get(first, ())), set()
            while pending:
                item = pending.pop()
                _require(item != first, "precedence_historical_cycle")
                if item in seen:
                    continue
                seen.add(item)
                pending.extend(successors.get(item, ()))

        event_ids = set()
        replaced = set()
        known_replacements = set()
        for event in self.supersessions:
            _require(_filled(event.id) and event.id not in event_ids,
                     "supersession_id_duplicate_or_empty")
            event_ids.add(event.id)
            _require(_filled(event.reason), "supersession_reason_required")
            old = anchors.get(event.old_anchor_id)
            _require(old is not None and old.universe_id == event.universe_id,
                     "supersession_old_anchor_invalid")
            _require(old.id not in replaced, "supersession_history_fork")
            # Conservarive: cannot supersede an anchor with ANY historical edge.
            _require(not any(edge.before_anchor_id == old.id or
                             edge.after_anchor_id == old.id for edge in self.precedences),
                     "supersession_historical_precedences_blocked")
            if event.new_anchor_id is not None:
                new = anchors.get(event.new_anchor_id)
                _require(new is not None and new.universe_id == event.universe_id
                         and new.id != old.id, "supersession_new_anchor_invalid")
                _require(new.id not in known_replacements, "supersession_replacement_reused")
                _require(new.id not in replaced, "supersession_replacement_not_current")
                known_replacements.add(new.id)
            replaced.add(old.id)

    @property
    def active_anchor_ids(self) -> frozenset[str]:
        old = {event.old_anchor_id for event in self.supersessions}
        return frozenset(a.id for a in self.anchors if a.id not in old)

    def propose_replacement(
        self, old_id: str, new_anchor: Anchor, event_id: str, reason: str
    ) -> "SyntheticSnapshot":
        originals = {a.id: a for a in self.anchors}
        old = originals.get(old_id)
        _require(old is not None, "supersession_old_anchor_missing")
        _require(old_id in self.active_anchor_ids, "supersession_old_not_current")
        _require(new_anchor.id not in originals, "supersession_new_id_not_fresh")
        _require(new_anchor.universe_id == old.universe_id, "supersession_cross_universe")
        _validate_anchor(new_anchor)
        event = Supersession(event_id, old.universe_id, old_id, new_anchor.id, reason)
        return SyntheticSnapshot(
            self.anchors + (new_anchor,), self.precedences,
            self.supersessions + (event,),
        )

    def propose_withdrawal(
        self, old_id: str, event_id: str, reason: str
    ) -> "SyntheticSnapshot":
        originals = {a.id: a for a in self.anchors}
        old = originals.get(old_id)
        _require(old is not None, "supersession_old_anchor_missing")
        _require(old_id in self.active_anchor_ids, "supersession_old_not_current")
        event = Supersession(event_id, old.universe_id, old_id, None, reason)
        return SyntheticSnapshot(
            self.anchors, self.precedences, self.supersessions + (event,),
        )
