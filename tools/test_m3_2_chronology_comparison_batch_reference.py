"""Stage30 independent synthetic all-or-nothing comparison batch fixtures."""
from dataclasses import FrozenInstanceError
import json
import unittest

from m3_2_chronology_navigation_reference import NavigationFilters
from m3_2_chronology_comparison_batch_reference import (
    MAX_COMPARISON_PAIRS, review_comparison_batch, comparison_batch_json,
)
from m3_2_chronology_witness_consultation_reference import (
    consult_world_order_witness,
)
from m3_2_supersession_reference import (
    Anchor, Precedence, ProposalRejected, SyntheticSnapshot,
)


def unknown(identifier, universe="u1"):
    return Anchor(identifier, universe, "unknown")


def exact(identifier, label, universe="u1"):
    return Anchor(identifier, universe, "exact",
                  calendar_id="fictional-calendar", exact_label=label)


class SyntheticComparisonBatchTests(unittest.TestCase):
    def setUp(self):
        base = SyntheticSnapshot((
            exact("a", "Tenth Bell"), unknown("b"),
            exact("c", "First Bell"), unknown("foreign", "u2"),
            unknown("old"), unknown("withdraw"), unknown("d"),
            unknown("isolated"),
        ), (
            Precedence("p-ab", "u1", "a", "b"),
            Precedence("p-bc", "u1", "b", "c"),
            Precedence("p-cd", "u1", "c", "d"),
        ))
        revised = base.propose_replacement(
            "old", unknown("new"), "r1", "human decision")
        self.snapshot = revised.propose_withdrawal(
            "withdraw", "r2", "human withdrawal")
        self.pairs = (
            ("d", "a"), ("a", "c"), ("a", "a"),
            ("b", "isolated"), ("a", "b"),
        )

    def batch(self, pairs=None, **options):
        return review_comparison_batch(
            self.snapshot, "u1",
            self.pairs if pairs is None else pairs, **options,
        )

    def veto(self, code, operation):
        with self.assertRaises(ProposalRejected) as ctx:
            operation()
        self.assertEqual(str(ctx.exception), code)

    def test_five_pairs_keep_request_order_not_source_order(self):
        value = self.batch()
        self.assertEqual(
            [(i.review.left.anchor_id, i.review.right.anchor_id)
             for i in value.items], list(self.pairs))
        self.assertEqual(
            value.request_order_semantics,
            "explicit_pair_request_order_not_world_time")

    def test_mixed_relations_do_not_imply_total_order(self):
        self.assertEqual(
            [i.review.witness_page.relation for i in self.batch().items],
            ["after", "before", "same", "incomparable", "before"])

    def test_request_ordinals_are_local_not_world_time(self):
        self.assertEqual(
            [item.request_ordinal for item in self.batch().items],
            [1, 2, 3, 4, 5])

    def test_transitive_evidence_is_one_human_path(self):
        value = self.batch((("a", "d"),), witness_page_size=4)
        self.assertEqual(
            [s.precedence_id for s in value.items[0].review.witness_page.evidence_steps],
            ["p-ab", "p-bc", "p-cd"])

    def test_after_evidence_follows_forward_authored_direction(self):
        value = self.batch((("d", "a"),), witness_page_size=1)
        step = value.items[0].review.witness_page.evidence_steps[0]
        self.assertEqual((step.before_anchor_id, step.after_anchor_id),
                         ("a", "b"))

    def test_single_pair_valid(self):
        self.assertEqual(len(self.batch((("a", "c"),)).items), 1)

    def test_sixteen_pairs_valid(self):
        pairs = (("a", "b"),) * MAX_COMPARISON_PAIRS
        value = self.batch(pairs)
        self.assertEqual(len(value.items), 16)
        self.assertEqual(value.items[-1].request_ordinal, 16)

    def test_seventeen_pairs_rejected(self):
        self.veto("batch_pair_count_or_type_invalid",
                  lambda: self.batch((("a", "b"),) * 17))

    def test_empty_batch_rejected(self):
        self.veto("batch_pair_count_or_type_invalid",
                  lambda: self.batch(()))

    def test_list_as_batch_rejected(self):
        self.veto("batch_pair_count_or_type_invalid",
                  lambda: self.batch([("a", "b")]))

    def test_none_batch_rejected(self):
        self.veto("batch_pair_count_or_type_invalid",
                  lambda: self.batch(0))

    def test_string_as_pair_rejected(self):
        self.veto("batch_pair_shape_invalid",
                  lambda: self.batch(("ab",)))

    def test_list_as_pair_rejected(self):
        self.veto("batch_pair_shape_invalid",
                  lambda: self.batch((["a", "b"],)))

    def test_one_element_pair_rejected(self):
        self.veto("batch_pair_shape_invalid",
                  lambda: self.batch((("a",),)))

    def test_three_element_pair_rejected(self):
        self.veto("batch_pair_shape_invalid",
                  lambda: self.batch((("a", "b", "c"),)))

    def test_late_invalid_pair_fails_entire_batch(self):
        self.veto("batch_pair_shape_invalid",
                  lambda: self.batch((("a", "b"), ("a", "c", "d"))))

    def test_late_missing_anchor_fails_entire_batch(self):
        self.veto("comparison_anchor_not_in_filtered_universe",
                  lambda: self.batch((("a", "b"), ("a", "missing"))))

    def test_invalid_id_type_in_pair_fails_closed(self):
        self.veto("comparison_anchor_id_invalid",
                  lambda: self.batch((("a", True),)))

    def test_repeated_pairs_are_preserved(self):
        value = self.batch((("a", "b"), ("a", "b")))
        self.assertEqual(value.items[0].review, value.items[1].review)
        self.assertNotEqual(value.items[0].request_ordinal,
                            value.items[1].request_ordinal)

    def test_reverse_pair_keeps_distinct_orientation(self):
        value = self.batch((("a", "b"), ("b", "a")))
        self.assertEqual(
            [x.review.witness_page.relation for x in value.items],
            ["before", "after"])

    def test_same_identity_has_no_fabricated_link(self):
        value = self.batch((("a", "a"),))
        self.assertEqual(value.items[0].review.witness_page.total_evidence_links, 0)

    def test_incomparable_has_no_fabricated_link(self):
        value = self.batch((("a", "isolated"),))
        self.assertEqual(value.items[0].review.witness_page.evidence_steps, ())

    def test_text_filter_applies_to_all_pairs(self):
        value = self.batch((("a", "c"),),
                           filters=NavigationFilters(text_contains="BELL"))
        self.assertEqual(value.items[0].review.filtered_anchor_count, 2)
        self.assertEqual(value.items[0].review.witness_page.relation, "before")

    def test_text_filter_late_failure_is_atomic(self):
        self.veto("comparison_anchor_not_in_filtered_universe",
                  lambda: self.batch(
                      (("a", "c"), ("a", "b")),
                      filters=NavigationFilters(text_contains="Bell")))

    def test_status_filter_active_retains_pairs(self):
        value = self.batch((("a", "d"),),
                           filters=NavigationFilters(statuses=("active",)))
        self.assertEqual(value.items[0].review.witness_page.relation, "before")

    def test_invalid_filter_rejected(self):
        self.veto("navigation_filter_type_invalid",
                  lambda: self.batch(filters={"editable": True}))

    def test_cross_universe_selection_rejected(self):
        self.veto("comparison_anchor_not_in_filtered_universe",
                  lambda: self.batch((("a", "foreign"),)))

    def test_replaced_selection_rejected(self):
        self.veto("comparison_anchor_not_active",
                  lambda: self.batch((("old", "a"),)))

    def test_withdrawn_selection_rejected(self):
        self.veto("comparison_anchor_not_active",
                  lambda: self.batch((("withdraw", "a"),)))

    def test_invalid_universe_rejected(self):
        self.veto("comparison_universe_required",
                  lambda: review_comparison_batch(self.snapshot, " ", self.pairs))

    def test_invalid_snapshot_rejected(self):
        self.veto("comparison_snapshot_type_invalid",
                  lambda: review_comparison_batch(None, "u1", self.pairs))

    def test_navigation_page_size_rejected(self):
        for width in (0, True, 65):
            with self.subTest(width=width):
                self.veto("selection_navigation_page_size_invalid",
                          lambda: self.batch(navigation_page_size=width))

    def test_witness_page_size_rejected(self):
        for width in (0, False, 65):
            with self.subTest(width=width):
                self.veto("consultation_page_size_invalid",
                          lambda: self.batch(witness_page_size=width))

    def test_navigation_across_pages_retains_source_ordinals(self):
        value = self.batch((("a", "d"),), navigation_page_size=2)
        review = value.items[0].review
        self.assertEqual(review.left.filtered_source_ordinal, 1)
        self.assertEqual(review.right.filtered_source_ordinal, 6)
        self.assertEqual(review.right.navigation_page_ordinal, 3)

    def test_first_witness_page_has_next_for_transitive_relation(self):
        value = self.batch((("a", "d"),), witness_page_size=1)
        page = value.items[0].review.witness_page
        self.assertEqual(page.total_evidence_links, 3)
        self.assertEqual(len(page.evidence_steps), 1)
        self.assertIsNotNone(page.next_cursor)

    def test_each_witness_cursor_reopens_only_its_own_pair(self):
        value = self.batch((("a", "d"), ("a", "c")),
                           witness_page_size=1)
        cursor = value.items[0].review.witness_page.next_cursor
        continued = consult_world_order_witness(
            self.snapshot, "u1", "a", "d", page_size=1, cursor=cursor)
        self.assertEqual(continued.evidence_steps[0].link_number, 2)
        self.veto("consultation_cursor_stale_context",
                  lambda: consult_world_order_witness(
                      self.snapshot, "u1", "a", "c",
                      page_size=1, cursor=cursor))

    def test_tiny_batch_still_id_only(self):
        value = comparison_batch_json(self.batch((("a", "c"),)))
        for secret in ("Tenth Bell", "First Bell", "fictional-calendar"):
            self.assertNotIn(secret, value)
        self.assertFalse(json.loads(value)["editing_authorized"])

    def test_nested_review_is_read_only(self):
        value = json.loads(comparison_batch_json(self.batch((("a", "c"),))))
        self.assertFalse(value["items"][0]["review"]["editing_authorized"])
        self.assertFalse(
            value["items"][0]["review"]["witness_page"]["editing_authorized"])
        self.assertFalse(value["partial_results_authorized"])

    def test_json_deterministic_and_non_batch_refused(self):
        value = self.batch((("a", "b"),))
        self.assertEqual(comparison_batch_json(value), comparison_batch_json(value))
        self.veto("batch_result_type_invalid",
                  lambda: comparison_batch_json({"write": True}))

    def test_frozen_result_and_unchanged_snapshot(self):
        original = repr(self.snapshot)
        value = self.batch((("a", "d"),))
        self.assertEqual(repr(self.snapshot), original)
        with self.assertRaises(FrozenInstanceError):
            value.editing_authorized = True
        with self.assertRaises(FrozenInstanceError):
            value.items[0].request_ordinal = 100

    def test_more_than_512_synthetic_anchors_supported(self):
        anchors = tuple(unknown(f"id{i}") for i in range(513))
        snapshot = SyntheticSnapshot(
            anchors, (Precedence("edge512", "u1", "id0", "id512"),))
        batch = review_comparison_batch(
            snapshot, "u1", (("id0", "id512"),),
            navigation_page_size=64)
        item = batch.items[0]
        self.assertEqual(item.review.right.filtered_source_ordinal, 513)
        self.assertEqual(item.review.witness_page.relation, "before")


if __name__ == "__main__":
    unittest.main()
