"""Stage 25: in-memory, offline, explicit filtered comparison adversarial tests."""
from dataclasses import FrozenInstanceError
import json
import unittest

from m3_2_chronology_navigation_reference import NavigationFilters
from m3_2_chronology_comparison_reference import (
    compare_filtered_anchors, comparison_json,
)
from m3_2_supersession_reference import (
    Anchor, Precedence, ProposalRejected, SyntheticSnapshot,
)


def exact(identifier, label, calendar="Cal", world="u1"):
    return Anchor(identifier, world, "exact",
                  calendar_id=calendar, exact_label=label)


def unknown(identifier, world="u1", revision=None):
    return Anchor(identifier, world, "unknown", source_revision_id=revision)


class ExplicitFilteredComparisonTests(unittest.TestCase):
    def setUp(self):
        self.initial = SyntheticSnapshot((
            exact("a", "Tenth Bell"),
            exact("b", "Third Bell"),
            unknown("c", revision="historical-source"),
            exact("unlinked", "First Bell", calendar="Other"),
            unknown("old", revision="original-revision"),
            unknown("withdraw"),
            unknown("outside", world="u2"),
        ), (Precedence("p1", "u1", "a", "b"),
            Precedence("p2", "u1", "b", "c")))
        replaced = self.initial.propose_replacement(
            "old", unknown("new", revision="new-revision"),
            "event1", "human reason")
        self.snapshot = replaced.propose_withdrawal(
            "withdraw", "event2", "human withdrawal")

    def compare(self, left, right, **kwargs):
        return compare_filtered_anchors(
            self.snapshot, "u1", left, right, **kwargs)

    def veto(self, code, action):
        with self.assertRaises(ProposalRejected) as result:
            action()
        self.assertEqual(str(result.exception), code)

    def test_explicit_direct_before(self):
        self.assertEqual(self.compare("a", "b").relation, "before")

    def test_explicit_reverse_after(self):
        self.assertEqual(self.compare("b", "a").relation, "after")

    def test_explicit_transitive_before(self):
        self.assertEqual(self.compare("a", "c").relation, "before")

    def test_active_same_anchor(self):
        self.assertEqual(self.compare("a", "a").relation, "same")

    def test_disconnected_is_incomparable(self):
        self.assertEqual(self.compare("a", "unlinked").relation,
                         "incomparable")

    def test_fictional_labels_do_not_reorder_explicit_edges(self):
        # "Tenth Bell" is explicitly BEFORE "Third Bell".
        self.assertEqual(self.compare("a", "b").relation, "before")

    def test_distinct_calendars_never_imply_order(self):
        self.assertEqual(self.compare("unlinked", "b").relation,
                         "incomparable")

    def test_filters_allow_matching_active_exact_pair(self):
        filters = NavigationFilters(
            statuses=("active",), time_kinds=("exact",), calendar_id="Cal")
        self.assertEqual(self.compare("a", "b", filters=filters).relation,
                         "before")

    def test_literal_filter_matches_both_selected_labels(self):
        self.assertEqual(self.compare(
            "a", "b", filters=NavigationFilters(text_contains="bElL")
        ).relation, "before")

    def test_one_filtered_out_anchor_refused(self):
        self.veto("comparison_anchor_not_in_filtered_universe",
                  lambda: self.compare(
                      "a", "b", filters=NavigationFilters(
                          text_contains="tenth")))

    def test_different_calendar_filter_refused(self):
        self.veto("comparison_anchor_not_in_filtered_universe",
                  lambda: self.compare(
                      "a", "unlinked",
                      filters=NavigationFilters(calendar_id="Cal")))

    def test_historical_revision_filter_not_redirected(self):
        self.veto("comparison_anchor_not_in_filtered_universe",
                  lambda: self.compare(
                      "old", "new", filters=NavigationFilters(
                          source_revision_id="original-revision")))

    def test_replaced_historical_anchor_refused(self):
        self.veto("comparison_anchor_not_active",
                  lambda: self.compare("old", "new"))

    def test_withdrawn_historical_anchor_refused(self):
        self.veto("comparison_anchor_not_active",
                  lambda: self.compare("withdraw", "a"))

    def test_status_filter_never_authorizes_replaced_selection(self):
        self.veto("comparison_anchor_not_active",
                  lambda: self.compare(
                      "old", "old",
                      filters=NavigationFilters(statuses=("replaced",))))

    def test_cross_universe_selection_refused(self):
        self.veto("comparison_anchor_not_in_filtered_universe",
                  lambda: self.compare("a", "outside"))

    def test_missing_anchor_selection_refused(self):
        self.veto("comparison_anchor_not_in_filtered_universe",
                  lambda: self.compare("a", "does-not-exist"))

    def test_invalid_selection_id_refused(self):
        for value in ("", "  ", 123, True, "x" * 257):
            with self.subTest(value=value):
                self.veto("comparison_anchor_id_invalid",
                          lambda: self.compare("a", value))

    def test_invalid_universe_refused(self):
        self.veto("comparison_universe_required",
                  lambda: compare_filtered_anchors(
                      self.snapshot, " ", "a", "b"))

    def test_invalid_snapshot_refused(self):
        self.veto("comparison_snapshot_type_invalid",
                  lambda: compare_filtered_anchors(
                      None, "u1", "a", "b"))

    def test_invalid_filter_refused(self):
        self.veto("navigation_filter_type_invalid",
                  lambda: self.compare("a", "b", filters={"editable": True}))

    def test_selection_over_512_items_without_full_panel(self):
        many = SyntheticSnapshot(
            tuple(unknown(f"id{i}") for i in range(513)),
            (Precedence("edge", "u1", "id0", "id512"),))
        result = compare_filtered_anchors(
            many, "u1", "id0", "id512")
        self.assertEqual(result.relation, "before")

    def test_result_independent_of_pagination_width(self):
        # No page/cursor argument can transform a selected pair into an order.
        self.assertEqual(self.compare("a", "c").relation, "before")
        self.assertEqual(self.compare("a", "unlinked").relation,
                         "incomparable")

    def test_json_flags_are_readonly_and_orders_unavailable(self):
        item = self.compare("a", "b")
        serialized = comparison_json(item)
        self.assertEqual(serialized, comparison_json(item))
        payload = json.loads(serialized)
        self.assertEqual(payload["relation"], "before")
        self.assertFalse(payload["editing_authorized"])
        self.assertEqual(payload["narration_order"],
                         "not_available_in_synthetic_projection")
        self.assertEqual(payload["reader_reveal_order"],
                         "not_available_in_synthetic_projection")
        self.assertEqual(payload["data_origin"],
                         "synthetic_in_memory_reference_only")

    def test_bad_serialization_object_refused(self):
        self.veto("comparison_result_type_invalid",
                  lambda: comparison_json({"editing_authorized": True}))

    def test_snapshot_not_mutated_and_output_frozen(self):
        original = repr(self.snapshot)
        comparison = self.compare("a", "b")
        self.assertEqual(repr(self.snapshot), original)
        with self.assertRaises(FrozenInstanceError):
            comparison.editing_authorized = True


if __name__ == "__main__":
    unittest.main()
