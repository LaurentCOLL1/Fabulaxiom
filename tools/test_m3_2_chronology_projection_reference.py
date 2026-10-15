"""Stage 21 synthetic-only read model; no user databases or UI writes."""
import unittest

from m3_2_supersession_reference import (
    Anchor, Precedence, ProposalRejected, SyntheticSnapshot,
)
from m3_2_chronology_projection_reference import (
    inspect_anchor, lineage, relative_world_order, universe_view,
)


def undated(id, universe="u1", revision=None):
    return Anchor(id, universe, "unknown", source_revision_id=revision)


def exact(id, label, universe="u1", calendar="fictional"):
    return Anchor(id, universe, "exact", calendar, exact_label=label)


class ChronologyProjectionSyntheticTests(unittest.TestCase):
    def setUp(self):
        self.base = SyntheticSnapshot((
            undated("a"), exact("b", "last", calendar="moon"),
            exact("c", "first", calendar="sun"),
            undated("d"), undated("e"),
            undated("x", "u2"),
        ), (
            Precedence("p1", "u1", "a", "b"),
            Precedence("p2", "u1", "b", "c"),
        ))

    def veto(self, code, fn):
        with self.assertRaises(ProposalRejected) as result:
            fn()
        self.assertEqual(str(result.exception), code)

    def test_universe_view_filters_other_universe(self):
        view = universe_view(self.base, "u1")
        self.assertEqual([a.anchor.id for a in view.anchors],
                         ["a", "b", "c", "d", "e"])
        self.assertTrue(all(a.anchor.universe_id == "u1" for a in view.anchors))

    def test_empty_universe_view_contains_no_cross_universe_objects(self):
        self.assertEqual(universe_view(self.base, "nonexistent").anchors, ())

    def test_unknown_universe_id_rejected(self):
        self.veto("projection_universe_required",
                  lambda: universe_view(self.base, ""))

    def test_display_order_is_input_order_not_chronology(self):
        self.assertEqual([v.anchor.id for v in universe_view(self.base, "u1").anchors],
                         ["a", "b", "c", "d", "e"])

    def test_read_model_disables_narration_reveal_and_editing(self):
        view = universe_view(self.base, "u1")
        self.assertFalse(view.narration_order_available)
        self.assertFalse(view.reader_reveal_order_available)
        self.assertFalse(view.chronology_editing_authorized)

    def test_historic_exact_label_and_calendar_not_transformed(self):
        view = universe_view(self.base, "u1")
        self.assertEqual(view.anchors[1].anchor.exact_label, "last")
        self.assertEqual(view.anchors[1].anchor.calendar_id, "moon")
        self.assertEqual(view.anchors[2].anchor.exact_label, "first")
        self.assertEqual(view.anchors[2].anchor.calendar_id, "sun")

    def test_transitive_human_before_relation(self):
        self.assertEqual(relative_world_order(self.base, "u1", "a", "c"), "before")

    def test_reverse_human_before_relation(self):
        self.assertEqual(relative_world_order(self.base, "u1", "c", "a"), "after")

    def test_same_anchor_is_not_a_new_timeline_order(self):
        self.assertEqual(relative_world_order(self.base, "u1", "a", "a"), "same")

    def test_disconnected_anchors_are_incomparable(self):
        self.assertEqual(relative_world_order(self.base, "u1", "d", "e"),
                         "incomparable")

    def test_exact_labels_never_imply_order_even_in_same_calendar(self):
        base = SyntheticSnapshot((exact("late", "999"), exact("early", "001")))
        self.assertEqual(relative_world_order(base, "u1", "early", "late"),
                         "incomparable")

    def test_different_fictional_calendars_not_compared_without_links(self):
        base = SyntheticSnapshot((exact("a", "12", calendar="A"),
                                  exact("b", "1", calendar="B")))
        self.assertEqual(relative_world_order(base, "u1", "a", "b"),
                         "incomparable")

    def test_cross_universe_inspection_does_not_leak_anchor(self):
        self.veto("projection_anchor_not_found_in_universe",
                  lambda: inspect_anchor(self.base, "u1", "x"))

    def test_cross_universe_order_query_rejected(self):
        self.veto("projection_anchor_not_found_in_universe",
                  lambda: relative_world_order(self.base, "u1", "a", "x"))

    def test_missing_anchor_rejected(self):
        self.veto("projection_anchor_not_found_in_universe",
                  lambda: lineage(self.base, "u1", "absent"))

    def test_uncorrected_anchor_is_active_with_empty_lineage(self):
        self.assertEqual(inspect_anchor(self.base, "u1", "d").status, "active")
        trail = lineage(self.base, "u1", "d")
        self.assertEqual(trail.anchor_ids, ("d",))
        self.assertEqual(trail.event_ids, ())
        self.assertEqual(trail.disposition, "active")

    def test_replacement_status_and_history_are_preserved(self):
        fixed = self.base.propose_replacement(
            "d", undated("d2", revision="immutable-revision"), "e1", "human correction")
        original = inspect_anchor(fixed, "u1", "d")
        self.assertEqual(original.status, "replaced")
        self.assertEqual(original.next_anchor_id, "d2")
        self.assertEqual(original.reason, "human correction")
        self.assertEqual(inspect_anchor(fixed, "u1", "d2").status, "active")
        self.assertEqual(inspect_anchor(self.base, "u1", "d").status, "active")

    def test_multistep_lineage_exposes_all_human_reasons(self):
        first = self.base.propose_replacement("d", undated("d2"), "e1", "first")
        second = first.propose_replacement("d2", undated("d3"), "e2", "second")
        trail = lineage(second, "u1", "d")
        self.assertEqual(trail.anchor_ids, ("d", "d2", "d3"))
        self.assertEqual(trail.event_ids, ("e1", "e2"))
        self.assertEqual(trail.reasons, ("first", "second"))
        self.assertEqual(trail.disposition, "active")

    def test_withdrawal_does_not_delete_original(self):
        retracted = self.base.propose_withdrawal("d", "e1", "withdrawal")
        self.assertEqual(inspect_anchor(retracted, "u1", "d").status, "withdrawn")
        self.assertEqual(lineage(retracted, "u1", "d").disposition, "withdrawn")
        self.assertIsNone(inspect_anchor(retracted, "u1", "d").next_anchor_id)
        self.assertEqual(len(retracted.anchors), len(self.base.anchors))

    def test_withdrawn_anchor_cannot_be_compared_as_current(self):
        retracted = self.base.propose_withdrawal("d", "e1", "retired")
        self.veto("projection_anchor_not_active",
                  lambda: relative_world_order(retracted, "u1", "d", "e"))

    def test_replaced_anchor_cannot_be_compared_as_current(self):
        corrected = self.base.propose_replacement("d", undated("d2"), "e1", "reason")
        self.veto("projection_anchor_not_active",
                  lambda: relative_world_order(corrected, "u1", "d", "e"))

    def test_new_unconnected_anchor_does_not_gain_precedences(self):
        corrected = self.base.propose_replacement("d", undated("d2"), "e1", "reason")
        self.assertEqual(relative_world_order(corrected, "u1", "d2", "e"),
                         "incomparable")

    def test_revision_identity_retained_exactly_as_authored(self):
        initial = SyntheticSnapshot((undated("a", revision="historic-rev-17"),))
        self.assertEqual(universe_view(initial, "u1").anchors[0].anchor.source_revision_id,
                         "historic-rev-17")

    def test_read_apis_do_not_change_original_snapshot(self):
        before = repr(self.base)
        inspect_anchor(self.base, "u1", "a")
        lineage(self.base, "u1", "a")
        universe_view(self.base, "u1")
        relative_world_order(self.base, "u1", "a", "c")
        self.assertEqual(repr(self.base), before)

    def test_unrelated_universe_precedences_never_leak(self):
        base = SyntheticSnapshot(
            (undated("a"), undated("b"), undated("x", "u2"),
             undated("y", "u2")),
            (Precedence("p", "u2", "x", "y"),),
        )
        self.assertEqual(relative_world_order(base, "u1", "a", "b"),
                         "incomparable")


if __name__ == "__main__":
    unittest.main()
