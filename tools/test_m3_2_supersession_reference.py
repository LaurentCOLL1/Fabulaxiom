"""M3.2 Stage 20 — synthetic ONLY; no SQLite or operator filesystem."""

import unittest

from m3_2_supersession_reference import (
    Anchor, Precedence, ProposalRejected, SyntheticSnapshot,
)


def exact(identifier, universe="u1", label="third bell"):
    return Anchor(identifier, universe, "exact", "fictional-calendar", exact_label=label)


def unknown(identifier, universe="u1", source_revision_id=None):
    return Anchor(identifier, universe, "unknown", source_revision_id=source_revision_id)


class SyntheticSupersessionAcceptance(unittest.TestCase):
    def assertVeto(self, code, action):
        with self.assertRaises(ProposalRejected) as captured:
            action()
        self.assertEqual(str(captured.exception), code)

    def test_replacement_retains_old_bytes_and_returns_new_snapshot(self):
        base = SyntheticSnapshot((exact("a", label="third bell"),))
        revised = base.propose_replacement("a", exact("b", label="fourth bell"), "e1", "human correction")
        self.assertEqual(base.anchors, (exact("a", label="third bell"),))
        self.assertEqual(base.supersessions, ())
        self.assertEqual(revised.anchors[0], base.anchors[0])
        self.assertEqual(revised.active_anchor_ids, frozenset({"b"}))
        self.assertEqual(revised.supersessions[0].old_anchor_id, "a")
        self.assertEqual(revised.supersessions[0].new_anchor_id, "b")

    def test_withdrawal_appends_event_without_deleting_anchor(self):
        base = SyntheticSnapshot((unknown("a"),))
        revised = base.propose_withdrawal("a", "e1", "manual retraction")
        self.assertEqual(revised.anchors, base.anchors)
        self.assertEqual(revised.active_anchor_ids, frozenset())
        self.assertIsNone(revised.supersessions[0].new_anchor_id)

    def test_replacement_chain_preserves_every_historic_revision(self):
        base = SyntheticSnapshot((exact("a"),))
        b = base.propose_replacement("a", exact("b"), "e1", "correction one")
        c = b.propose_replacement("b", unknown("c"), "e2", "uncertain instead")
        self.assertEqual(tuple(a.id for a in c.anchors), ("a", "b", "c"))
        self.assertEqual(c.active_anchor_ids, frozenset({"c"}))
        self.assertEqual(len(c.supersessions), 2)
        self.assertEqual(base.active_anchor_ids, frozenset({"a"}))

    def test_fork_from_superseded_anchor_is_refused(self):
        base = SyntheticSnapshot((exact("a"),))
        revised = base.propose_replacement("a", exact("b"), "e1", "first correction")
        self.assertVeto("supersession_old_not_current", lambda:
                        revised.propose_replacement("a", exact("c"), "e2", "fork"))

    def test_duplicate_supersession_event_id_is_refused(self):
        base = SyntheticSnapshot((exact("a"), unknown("c")))
        revised = base.propose_replacement("a", exact("b"), "event1", "corrected")
        self.assertVeto("supersession_id_duplicate_or_empty", lambda:
                        revised.propose_withdrawal("c", "event1", "retraction"))

    def test_cross_universe_replacement_is_refused(self):
        base = SyntheticSnapshot((exact("a", "u1"),))
        self.assertVeto("supersession_cross_universe", lambda:
                        base.propose_replacement("a", unknown("b", "u2"), "event1", "bad"))

    def test_old_anchor_missing_is_refused(self):
        base = SyntheticSnapshot((exact("a"),))
        self.assertVeto("supersession_old_anchor_missing", lambda:
                        base.propose_withdrawal("missing", "event1", "why"))

    def test_replacement_id_must_be_fresh(self):
        base = SyntheticSnapshot((exact("a"), unknown("b")))
        self.assertVeto("supersession_new_id_not_fresh", lambda:
                        base.propose_replacement("a", unknown("b"), "event1", "bad"))

    def test_withdrawal_cannot_be_repeated(self):
        base = SyntheticSnapshot((unknown("a"),))
        revised = base.propose_withdrawal("a", "event1", "retired")
        self.assertVeto("supersession_old_not_current", lambda:
                        revised.propose_withdrawal("a", "event2", "retired twice"))

    def test_blank_human_reason_refused(self):
        base = SyntheticSnapshot((exact("a"),))
        self.assertVeto("supersession_reason_required", lambda:
                        base.propose_replacement("a", exact("b"), "event1", "   "))

    def test_anchor_with_historical_precedence_cannot_be_replaced(self):
        base = SyntheticSnapshot(
            (unknown("a"), unknown("b")),
            (Precedence("p1", "u1", "a", "b"),),
        )
        self.assertVeto("supersession_historical_precedences_blocked", lambda:
                        base.propose_replacement("a", unknown("a2"), "event1", "cannot relink"))

    def test_anchor_with_historical_precedence_cannot_be_withdrawn(self):
        base = SyntheticSnapshot(
            (unknown("a"), unknown("b")),
            (Precedence("p1", "u1", "a", "b"),),
        )
        self.assertVeto("supersession_historical_precedences_blocked", lambda:
                        base.propose_withdrawal("b", "event1", "cannot unlink"))

    def test_historical_cycle_is_rejected_even_if_user_intends_reversal(self):
        self.assertVeto("precedence_historical_cycle", lambda:
                        SyntheticSnapshot(
                            (unknown("a"), unknown("b"), unknown("c")),
                            (Precedence("p1", "u1", "a", "b"),
                             Precedence("p2", "u1", "b", "c"),
                             Precedence("p3", "u1", "c", "a")),
                        ))

    def test_self_edge_is_rejected(self):
        self.assertVeto("precedence_self_edge", lambda:
                        SyntheticSnapshot((unknown("a"),),
                                          (Precedence("p1", "u1", "a", "a"),)))

    def test_duplicate_edge_is_rejected(self):
        self.assertVeto("precedence_duplicate_pair", lambda:
                        SyntheticSnapshot(
                            (unknown("a"), unknown("b")),
                            (Precedence("p1", "u1", "a", "b"),
                             Precedence("p2", "u1", "a", "b")),
                        ))

    def test_cross_universe_historical_precedence_is_rejected(self):
        self.assertVeto("precedence_cross_universe", lambda:
                        SyntheticSnapshot(
                            (unknown("a", "u1"), unknown("b", "u2")),
                            (Precedence("p1", "u1", "a", "b"),),
                        ))

    def test_unrelated_events_remain_unordered(self):
        base = SyntheticSnapshot((unknown("a"), unknown("b")))
        revised = base.propose_replacement("a", unknown("c"), "event1", "changed")
        self.assertEqual(revised.precedences, ())
        self.assertEqual(revised.active_anchor_ids, frozenset({"b", "c"}))

    def test_unknown_anchor_has_no_implied_gregorian_time(self):
        a = unknown("a", source_revision_id="old-immutable-revision")
        revised = SyntheticSnapshot((a,)).propose_replacement(
            "a", unknown("b", source_revision_id="old-immutable-revision"),
            "event1", "keep precise revision",
        )
        self.assertEqual(revised.anchors[-1].calendar_id, None)
        self.assertIsNone(revised.anchors[-1].exact_label)
        self.assertEqual(revised.anchors[-1].source_revision_id, "old-immutable-revision")

    def test_incorrect_exact_shape_rejected(self):
        base = SyntheticSnapshot((unknown("a"),))
        self.assertVeto("anchor_exact_shape_invalid", lambda:
                        base.propose_replacement("a", Anchor("b", "u1", "exact"),
                                                 "event1", "bad"))

    def test_incorrect_approximate_shape_rejected(self):
        base = SyntheticSnapshot((unknown("a"),))
        a = Anchor("b", "u1", "approximate", calendar_id="calendar",
                   window_start_text="early spring")
        self.assertVeto("anchor_approximate_shape_invalid", lambda:
                        base.propose_replacement("a", a, "event1", "missing precision"))

    def test_incorrect_unknown_shape_rejected(self):
        base = SyntheticSnapshot((unknown("a"),))
        self.assertVeto("anchor_undated_shape_invalid", lambda:
                        base.propose_replacement(
                            "a", Anchor("b", "u1", "unknown", exact_label="made up"),
                            "event1", "bad"))

    def test_valid_one_sided_approximate_window_preserved(self):
        base = SyntheticSnapshot((unknown("a"),))
        b = Anchor("b", "u1", "approximate", calendar_id="fictional",
                   window_end_text="late harvest", precision_text="season")
        revised = base.propose_replacement("a", b, "event1", "evidence")
        self.assertIsNone(revised.anchors[-1].window_start_text)
        self.assertEqual(revised.anchors[-1].window_end_text, "late harvest")

    def test_duplicate_historical_anchor_id_rejected(self):
        self.assertVeto("duplicate_anchor_id", lambda:
                        SyntheticSnapshot((unknown("a"), unknown("a"))))

    def test_same_display_event_names_never_join_by_names(self):
        base = SyntheticSnapshot((unknown("entity-id-1"), unknown("entity-id-2")))
        revised = base.propose_replacement(
            "entity-id-1", unknown("replacement-id"), "event1", "distinct identity"
        )
        self.assertEqual(revised.active_anchor_ids,
                         frozenset({"entity-id-2", "replacement-id"}))

    def test_invalid_assertion_does_not_mutate_original(self):
        base = SyntheticSnapshot((exact("a"), unknown("b")))
        before = repr(base)
        self.assertVeto("supersession_cross_universe", lambda:
                        base.propose_replacement("a", unknown("new", "u2"),
                                                 "event1", "failed transaction"))
        self.assertEqual(repr(base), before)
        self.assertEqual(base.supersessions, ())


if __name__ == "__main__":
    unittest.main()
