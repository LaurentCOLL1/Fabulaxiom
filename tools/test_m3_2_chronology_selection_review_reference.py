"""Stage29 ID-only selection location and witness coherence fixtures."""
from dataclasses import FrozenInstanceError
import json
import unittest

from m3_2_chronology_navigation_reference import (
    NavigationFilters, navigate_chronology,
)
from m3_2_chronology_selection_review_reference import (
    review_selected_witness, selection_review_json,
)
from m3_2_supersession_reference import (
    Anchor, Precedence, ProposalRejected, SyntheticSnapshot,
)


def unknown(identifier, universe="u1"):
    return Anchor(identifier, universe, "unknown")


def exact(identifier, label, universe="u1"):
    return Anchor(identifier, universe, "exact",
                  calendar_id="fictional", exact_label=label)


class SelectionReviewFixtures(unittest.TestCase):
    def setUp(self):
        initial = SyntheticSnapshot((
            exact("a", "Tenth Bell"), unknown("withdraw"), unknown("b"),
            unknown("foreign", "u2"), unknown("old"),
            exact("c", "First Bell"), unknown("isolated"), unknown("d"),
        ), (
            Precedence("a-b", "u1", "a", "b"),
            Precedence("b-c", "u1", "b", "c"),
        ))
        changed = initial.propose_replacement(
            "old", unknown("new"), "supersede", "human correction")
        self.snapshot = changed.propose_withdrawal(
            "withdraw", "remove", "human decision")

    def review(self, left="a", right="c", **kwargs):
        return review_selected_witness(
            self.snapshot, "u1", left, right, **kwargs
        )

    def veto(self, code, operation):
        with self.assertRaises(ProposalRejected) as result:
            operation()
        self.assertEqual(str(result.exception), code)

    def open_location(self, location, **kwargs):
        return navigate_chronology(
            self.snapshot, "u1", page_size=kwargs.get("page_size", 2),
            filters=kwargs.get("filters", NavigationFilters()),
            cursor=location.navigation_cursor,
        )

    def test_selected_locations_are_source_order_only(self):
        result = self.review(navigation_page_size=2)
        self.assertEqual(result.left.filtered_source_ordinal, 1)
        self.assertEqual(result.right.filtered_source_ordinal, 5)
        self.assertEqual(result.display_order_semantics,
                         "source_insertion_order_not_world_time")

    def test_navigation_cross_page_cursor_points_to_selected_id(self):
        result = self.review(navigation_page_size=2)
        page = self.open_location(result.right)
        self.assertEqual(page.anchor_cards[0].anchor_id, "c")

    def test_first_navigation_page_has_null_cursor(self):
        result = self.review(navigation_page_size=2)
        self.assertIsNone(result.left.navigation_cursor)

    def test_second_anchor_on_third_page(self):
        result = self.review(navigation_page_size=2)
        self.assertEqual(result.right.navigation_page_ordinal, 3)
        self.assertEqual(result.right.ordinal_on_navigation_page, 1)

    def test_different_navigation_page_width_changes_locator_not_world_relation(self):
        narrow = self.review(navigation_page_size=2)
        wide = self.review(navigation_page_size=6)
        self.assertEqual(narrow.right.navigation_page_ordinal, 3)
        self.assertEqual(wide.right.navigation_page_ordinal, 1)
        self.assertEqual(narrow.witness_page.relation, wide.witness_page.relation)
        self.assertEqual(narrow.witness_page.evidence_steps,
                         wide.witness_page.evidence_steps)

    def test_same_page_both_selection_locations(self):
        result = self.review(navigation_page_size=8)
        self.assertEqual(result.left.navigation_page_ordinal, 1)
        self.assertEqual(result.right.navigation_page_ordinal, 1)

    def test_filtered_active_omits_historical_anchors(self):
        filters = NavigationFilters(statuses=("active",))
        result = self.review(filters=filters, navigation_page_size=2)
        self.assertEqual(result.left.filtered_source_ordinal, 1)
        self.assertEqual(result.right.filtered_source_ordinal, 3)
        self.assertEqual(result.filtered_anchor_count, 6)

    def test_filtered_navigation_cursor_resumes_with_exact_filter(self):
        filters = NavigationFilters(statuses=("active",))
        result = self.review(filters=filters, navigation_page_size=2)
        page = self.open_location(result.right, page_size=2, filters=filters)
        self.assertEqual(page.anchor_cards[0].anchor_id, "c")

    def test_text_filter_both_endpoints_and_hidden_intermediate(self):
        filters = NavigationFilters(text_contains="BELL")
        result = self.review(filters=filters, navigation_page_size=1)
        self.assertEqual(result.filtered_anchor_count, 2)
        self.assertEqual(result.right.filtered_source_ordinal, 2)
        self.assertEqual([s.precedence_id for s in result.witness_page.evidence_steps],
                         ["a-b", "b-c"])

    def test_text_filter_hiding_one_selected_endpoint_refused(self):
        self.veto("comparison_anchor_not_in_filtered_universe",
                  lambda: self.review(
                      filters=NavigationFilters(text_contains="Tenth")))

    def test_selection_same_id_has_same_location_and_no_evidence(self):
        result = self.review("a", "a")
        self.assertEqual(result.left, result.right)
        self.assertEqual(result.witness_page.relation, "same")
        self.assertEqual(result.witness_page.total_evidence_links, 0)

    def test_incomparable_selectors_keep_distinct_locations(self):
        result = self.review("a", "isolated")
        self.assertEqual(result.witness_page.relation, "incomparable")
        self.assertEqual(result.witness_page.evidence_steps, ())
        self.assertNotEqual(result.left, result.right)

    def test_swapped_selection_changes_witness_relation_not_positions(self):
        forward = self.review("a", "c")
        reverse = self.review("c", "a")
        self.assertEqual(forward.witness_page.relation, "before")
        self.assertEqual(reverse.witness_page.relation, "after")
        self.assertEqual(forward.left, reverse.right)
        self.assertEqual(forward.right, reverse.left)

    def test_fictional_labels_cannot_override_human_links(self):
        result = self.review("a", "c")
        self.assertEqual(result.witness_page.relation, "before")

    def test_witness_second_page_preserves_locations(self):
        first = self.review(witness_page_size=1, navigation_page_size=2)
        later = self.review(
            witness_page_size=1, navigation_page_size=2,
            witness_cursor=first.witness_page.next_cursor,
        )
        self.assertEqual(first.left, later.left)
        self.assertEqual(first.right, later.right)
        self.assertEqual(later.witness_page.evidence_steps[0].link_number, 2)

    def test_witness_back_cursor_preserves_locations(self):
        first = self.review(witness_page_size=1)
        last = self.review(witness_page_size=1,
                           witness_cursor=first.witness_page.next_cursor)
        again = self.review(witness_page_size=1,
                            witness_cursor=last.witness_page.previous_cursor)
        self.assertEqual(first, again)

    def test_changed_witness_page_width_invalidates_old_cursor(self):
        first = self.review(witness_page_size=1)
        self.veto("consultation_cursor_stale_context",
                  lambda: self.review(
                      witness_page_size=2,
                      witness_cursor=first.witness_page.next_cursor))

    def test_changed_filters_invalidate_old_witness_cursor(self):
        first = self.review(witness_page_size=1)
        self.veto("consultation_cursor_stale_context",
                  lambda: self.review(
                      witness_page_size=1,
                      filters=NavigationFilters(statuses=("active",)),
                      witness_cursor=first.witness_page.next_cursor))

    def test_changed_selection_invalidates_witness_cursor(self):
        first = self.review(witness_page_size=1)
        self.veto("consultation_cursor_stale_context",
                  lambda: self.review("c", "a", witness_page_size=1,
                      witness_cursor=first.witness_page.next_cursor))

    def test_navigation_cursor_stale_on_width_change(self):
        initial = self.review(navigation_page_size=2)
        self.veto("navigation_cursor_stale_snapshot_or_filters",
                  lambda: self.open_location(initial.right, page_size=3))

    def test_navigation_cursor_stale_on_filter_change(self):
        initial = self.review(navigation_page_size=2)
        self.veto("navigation_cursor_stale_snapshot_or_filters",
                  lambda: self.open_location(
                      initial.right, filters=NavigationFilters(
                          statuses=("active",))))

    def test_navigation_cursor_stale_on_snapshot_change(self):
        initial = self.review(navigation_page_size=2)
        changed = SyntheticSnapshot(
            self.snapshot.anchors + (unknown("append"),),
            self.snapshot.precedences, self.snapshot.supersessions)
        self.veto("navigation_cursor_stale_snapshot_or_filters",
                  lambda: navigate_chronology(
                      changed, "u1", page_size=2,
                      cursor=initial.right.navigation_cursor))

    def test_outside_universe_endpoint_refused(self):
        self.veto("comparison_anchor_not_in_filtered_universe",
                  lambda: self.review("a", "foreign"))

    def test_withdrawn_endpoint_refused(self):
        self.veto("comparison_anchor_not_active",
                  lambda: self.review("withdraw", "a"))

    def test_replaced_endpoint_refused(self):
        self.veto("comparison_anchor_not_active",
                  lambda: self.review("old", "a"))

    def test_invalid_navigation_page_sizes_refused(self):
        for size in (True, False, 0, 65, -1, 2.0, None):
            with self.subTest(size=size):
                self.veto("selection_navigation_page_size_invalid",
                          lambda: self.review(navigation_page_size=size))

    def test_witness_width_still_validated(self):
        self.veto("consultation_page_size_invalid",
                  lambda: self.review(witness_page_size=65))

    def test_large_navigation_across_more_than_512_anchors(self):
        items = tuple(unknown(f"id{i}") for i in range(513))
        snap = SyntheticSnapshot(
            items, (Precedence("edge512", "u1", "id0", "id512"),))
        result = review_selected_witness(
            snap, "u1", "id0", "id512", navigation_page_size=64)
        self.assertEqual(result.right.filtered_source_ordinal, 513)
        self.assertEqual(result.right.navigation_page_ordinal, 9)
        self.assertEqual(result.right.ordinal_on_navigation_page, 1)
        self.assertEqual(result.witness_page.evidence_steps[0].precedence_id,
                         "edge512")

    def test_id_only_output_and_no_edit_control(self):
        result = self.review()
        encoded = selection_review_json(result)
        for secret in ("Tenth Bell", "First Bell", "fictional"):
            self.assertNotIn(secret, encoded)
        value = json.loads(encoded)
        self.assertFalse(value["editing_authorized"])
        self.assertFalse(value["witness_page"]["editing_authorized"])
        self.assertEqual(value["data_origin"],
                         "synthetic_in_memory_reference_only")

    def test_json_deterministic_and_invalid_object_refused(self):
        result = self.review()
        self.assertEqual(selection_review_json(result),
                         selection_review_json(result))
        self.veto("selection_review_type_invalid",
                  lambda: selection_review_json({"editable": True}))

    def test_frozen_objects_and_input_snapshot_preserved(self):
        before = repr(self.snapshot)
        result = self.review()
        self.assertEqual(repr(self.snapshot), before)
        with self.assertRaises(FrozenInstanceError):
            result.editing_authorized = True
        with self.assertRaises(FrozenInstanceError):
            result.left.filtered_source_ordinal = 999

    def test_selection_refuses_invalid_id(self):
        self.veto("comparison_anchor_id_invalid",
                  lambda: self.review("a", ""))

    def test_empty_or_wrong_universe_refused(self):
        self.veto("comparison_universe_required",
                  lambda: review_selected_witness(
                      self.snapshot, " ", "a", "c"))

    def test_wrong_snapshot_refused(self):
        self.veto("comparison_snapshot_type_invalid",
                  lambda: review_selected_witness(None, "u1", "a", "c"))


if __name__ == "__main__":
    unittest.main()
