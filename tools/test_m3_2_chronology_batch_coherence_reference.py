"""Stage31 deterministic pair-group consistency and fail-closed fixtures."""
from dataclasses import FrozenInstanceError, replace
import json
import unittest

from m3_2_chronology_batch_coherence_reference import (
    audit_comparison_batch, batch_coherence_json, _check_batch_consistency,
)
from m3_2_chronology_comparison_batch_reference import review_comparison_batch
from m3_2_chronology_navigation_reference import NavigationFilters
from m3_2_supersession_reference import (
    Anchor, Precedence, ProposalRejected, SyntheticSnapshot,
)


def unknown(identity, universe="u1"):
    return Anchor(identity, universe, "unknown")


def exact(identity, label, universe="u1"):
    return Anchor(identity, universe, "exact",
                  calendar_id="fictional-calendar", exact_label=label)


class BatchCoherenceTests(unittest.TestCase):
    def setUp(self):
        base = SyntheticSnapshot((
            exact("a", "Tenth Bell"), unknown("b"),
            exact("c", "First Bell"), unknown("isolated"),
            unknown("old"), unknown("withdraw"), unknown("foreign", "u2"),
        ), (
            Precedence("p-ab", "u1", "a", "b"),
            Precedence("p-bc", "u1", "b", "c"),
        ))
        revised = base.propose_replacement(
            "old", unknown("new"), "r1", "human correction")
        self.snapshot = revised.propose_withdrawal(
            "withdraw", "r2", "human withdrawal")

    def audit(self, pairs=None, **kwargs):
        if pairs is None:
            pairs = (("b", "a"), ("a", "b"), ("a", "c"),
                     ("a", "b"), ("a", "a"), ("a", "isolated"))
        return audit_comparison_batch(self.snapshot, "u1", pairs, **kwargs)

    def veto(self, code, callback):
        with self.assertRaises(ProposalRejected) as ctx:
            callback()
        self.assertEqual(str(ctx.exception), code)

    def test_request_order_unchanged(self):
        value = self.audit()
        self.assertEqual(
            [(i.left_anchor_id, i.right_anchor_id) for i in value.entries],
            [("b", "a"), ("a", "b"), ("a", "c"),
             ("a", "b"), ("a", "a"), ("a", "isolated")])

    def test_group_numbers_are_first_request_occurrence_only(self):
        self.assertEqual(
            [e.unordered_pair_group_ordinal for e in self.audit().entries],
            [1, 1, 2, 1, 3, 4])

    def test_first_request_ordinals_do_not_sort_world_time(self):
        self.assertEqual(
            [e.first_request_ordinal for e in self.audit().entries],
            [1, 1, 3, 1, 5, 6])
        self.assertEqual(self.audit().cross_pair_temporal_inference,
                         "not_attempted")

    def test_reversed_pair_is_inverse_relation(self):
        entries = self.audit().entries
        self.assertEqual(entries[0].relation, "after")
        self.assertEqual(entries[1].relation, "before")
        self.assertEqual(entries[1].orientation, "reversed")

    def test_same_orientation_repeat_keeps_relation(self):
        entries = self.audit().entries
        self.assertEqual(entries[3].orientation, "reversed")
        self.assertEqual(entries[3].first_request_ordinal, 1)
        self.assertEqual(entries[3].relation, "before")

    def test_direct_repeat_is_marked_repeated(self):
        entries = self.audit((("a", "b"), ("a", "b"))).entries
        self.assertEqual([e.orientation for e in entries], ["first", "repeated"])

    def test_self_pair_repeat_is_marked_repeated(self):
        entries = self.audit((("a", "a"), ("a", "a"))).entries
        self.assertEqual([e.relation for e in entries], ["same", "same"])
        self.assertEqual(entries[-1].orientation, "repeated")

    def test_incomparable_reverse_is_still_incomparable(self):
        entries = self.audit((("a", "isolated"), ("isolated", "a"))).entries
        self.assertEqual([e.relation for e in entries],
                         ["incomparable", "incomparable"])
        self.assertEqual(entries[-1].orientation, "reversed")

    def test_transitive_reverse_shares_precedence_ids(self):
        value = self.audit((("a", "c"), ("c", "a")), witness_page_size=2)
        first = value.batch.items[0].review.witness_page.evidence_steps
        second = value.batch.items[1].review.witness_page.evidence_steps
        self.assertEqual(
            [s.precedence_id for s in first],
            [s.precedence_id for s in second])

    def test_one_first_page_per_pair(self):
        value = self.audit((("a", "c"), ("c", "a")), witness_page_size=1)
        self.assertEqual(
            [len(i.review.witness_page.evidence_steps) for i in value.batch.items],
            [1, 1])
        self.assertTrue(all(
            i.review.witness_page.next_cursor is not None
            for i in value.batch.items))

    def test_distinct_pairs_do_not_get_inferred_relations(self):
        value = self.audit((("a", "b"), ("b", "c")))
        self.assertEqual(value.unordered_pair_group_count, 2)
        self.assertEqual(len(value.entries), 2)
        self.assertEqual(value.cross_pair_temporal_inference, "not_attempted")

    def test_single_pair_valid(self):
        self.assertEqual(len(self.audit((("a", "c"),)).entries), 1)

    def test_sixteen_same_pairs_are_bounded(self):
        value = self.audit((("a", "b"),) * 16)
        self.assertEqual(len(value.entries), 16)
        self.assertEqual(value.unordered_pair_group_count, 1)

    def test_over_sixteen_refused(self):
        self.veto("batch_pair_count_or_type_invalid",
                  lambda: self.audit((("a", "b"),) * 17))

    def test_empty_batch_refused(self):
        self.veto("batch_pair_count_or_type_invalid",
                  lambda: self.audit(()))

    def test_late_missing_endpoint_rejects_whole_batch(self):
        self.veto("comparison_anchor_not_in_filtered_universe",
                  lambda: self.audit((("a", "b"), ("a", "missing"))))

    def test_cross_universe_endpoint_refused(self):
        self.veto("comparison_anchor_not_in_filtered_universe",
                  lambda: self.audit((("a", "foreign"),)))

    def test_replaced_endpoint_refused(self):
        self.veto("comparison_anchor_not_active",
                  lambda: self.audit((("old", "a"),)))

    def test_withdrawn_endpoint_refused(self):
        self.veto("comparison_anchor_not_active",
                  lambda: self.audit((("withdraw", "a"),)))

    def test_filtered_endpoint_refused(self):
        self.veto("comparison_anchor_not_in_filtered_universe",
                  lambda: self.audit((("a", "b"),),
                      filters=NavigationFilters(text_contains="Tenth")))

    def test_both_filtered_endpoint_labels_valid(self):
        value = self.audit((("a", "c"),),
                           filters=NavigationFilters(text_contains="BELL"))
        self.assertEqual(value.entries[0].relation, "before")

    def test_invalid_filter_refused(self):
        self.veto("navigation_filter_type_invalid",
                  lambda: self.audit(filters={"write": True}))

    def test_invalid_pair_shape_refused(self):
        self.veto("batch_pair_shape_invalid",
                  lambda: self.audit((("a",),)))

    def test_invalid_navigation_width_refused(self):
        self.veto("selection_navigation_page_size_invalid",
                  lambda: self.audit(navigation_page_size=0))

    def test_invalid_witness_width_refused(self):
        self.veto("consultation_page_size_invalid",
                  lambda: self.audit(witness_page_size=65))

    def test_corrupted_batch_request_ordinal_veto(self):
        original = review_comparison_batch(self.snapshot, "u1", (("a", "b"),))
        wrong = replace(original, items=(replace(original.items[0],
                                                 request_ordinal=9),))
        self.veto("coherence_request_order_invalid",
                  lambda: _check_batch_consistency(wrong))

    def test_corrupted_batch_scope_veto(self):
        original = review_comparison_batch(self.snapshot, "u1", (("a", "b"),))
        review = replace(original.items[0].review, universe_id="u2")
        wrong = replace(original, items=(replace(original.items[0],
                                                 review=review),))
        self.veto("coherence_scope_mismatch",
                  lambda: _check_batch_consistency(wrong))

    def test_corrupted_reverse_relation_veto(self):
        original = review_comparison_batch(
            self.snapshot, "u1", (("a", "b"), ("b", "a")))
        item = original.items[1]
        w = replace(item.review.witness_page, relation="before")
        wrong = replace(original, items=(
            original.items[0], replace(item, review=replace(item.review,
                                                            witness_page=w))))
        self.veto("coherence_repeated_pair_conflict",
                  lambda: _check_batch_consistency(wrong))

    def test_corrupted_repeated_evidence_veto(self):
        original = review_comparison_batch(
            self.snapshot, "u1", (("a", "b"), ("a", "b")))
        item = original.items[1]
        witness = item.review.witness_page
        step = replace(witness.evidence_steps[0], precedence_id="invented")
        w = replace(witness, evidence_steps=(step,))
        wrong = replace(original, items=(
            original.items[0], replace(item, review=replace(item.review,
                                                            witness_page=w))))
        self.veto("coherence_repeated_pair_conflict",
                  lambda: _check_batch_consistency(wrong))

    def test_corrupted_incomparable_evidence_veto(self):
        original = review_comparison_batch(
            self.snapshot, "u1", (("a", "isolated"),))
        item = original.items[0]
        w = replace(item.review.witness_page, total_evidence_links=1)
        wrong = replace(original, items=(replace(item, review=replace(
            item.review, witness_page=w)),))
        self.veto("coherence_evidence_invalid",
                  lambda: _check_batch_consistency(wrong))

    def test_corrupted_same_identity_relation_veto(self):
        original = review_comparison_batch(self.snapshot, "u1", (("a", "a"),))
        item = original.items[0]
        w = replace(item.review.witness_page, relation="before")
        wrong = replace(original, items=(replace(item, review=replace(
            item.review, witness_page=w)),))
        self.veto("coherence_relation_invalid",
                  lambda: _check_batch_consistency(wrong))

    def test_bad_internal_batch_type_refused(self):
        self.veto("coherence_batch_type_invalid",
                  lambda: _check_batch_consistency({"fake": True}))

    def test_no_fictional_labels_in_json(self):
        value = batch_coherence_json(self.audit())
        for forbidden in ("Tenth Bell", "First Bell", "fictional-calendar"):
            self.assertNotIn(forbidden, value)

    def test_json_is_deterministic_and_readonly(self):
        report = self.audit()
        value = batch_coherence_json(report)
        self.assertEqual(value, batch_coherence_json(report))
        obj = json.loads(value)
        self.assertFalse(obj["editing_authorized"])
        self.assertFalse(obj["batch"]["editing_authorized"])
        self.assertEqual(obj["data_origin"], "synthetic_in_memory_reference_only")

    def test_bad_serialization_object_refused(self):
        self.veto("coherence_result_type_invalid",
                  lambda: batch_coherence_json({"editing_authorized": True}))

    def test_frozen_output_and_no_snapshot_mutation(self):
        snapshot_repr = repr(self.snapshot)
        report = self.audit()
        self.assertEqual(repr(self.snapshot), snapshot_repr)
        with self.assertRaises(FrozenInstanceError):
            report.editing_authorized = True
        with self.assertRaises(FrozenInstanceError):
            report.entries[0].relation = "invented"

    def test_over_512_anchors_still_bounded_by_explicit_pairs(self):
        anchors = tuple(unknown(f"id{i}") for i in range(513))
        snapshot = SyntheticSnapshot(
            anchors, (Precedence("e512", "u1", "id0", "id512"),))
        report = audit_comparison_batch(
            snapshot, "u1", (("id0", "id512"),),
            navigation_page_size=64)
        self.assertEqual(report.unordered_pair_group_count, 1)
        self.assertEqual(report.batch.items[0].review.right.filtered_source_ordinal, 513)


if __name__ == "__main__":
    unittest.main()
