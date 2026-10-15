"""Stage32 ID-only read-only UI-contract demonstration, adversarial tests."""
from dataclasses import FrozenInstanceError
import json
import unittest

from m3_2_chronology_navigation_reference import NavigationFilters
from m3_2_chronology_readonly_handoff_reference import (
    build_readonly_chronology_handoff, readonly_handoff_json,
)
from m3_2_supersession_reference import (
    Anchor, Precedence, ProposalRejected, SyntheticSnapshot,
)


def unknown(identifier, universe="u1"):
    return Anchor(identifier, universe, "unknown")


def exact(identifier, label):
    return Anchor(identifier, "u1", "exact",
                  calendar_id="fictional-calendar", exact_label=label)


class ReadonlyHandoffTests(unittest.TestCase):
    def setUp(self):
        initial = SyntheticSnapshot((
            exact("a", "Tenth Bell"), unknown("b"),
            exact("c", "First Bell"), unknown("isolated"),
            unknown("old"), unknown("withdraw"), unknown("foreign", "u2"),
        ), (
            Precedence("p-ab", "u1", "a", "b"),
            Precedence("p-bc", "u1", "b", "c"),
        ))
        replaced = initial.propose_replacement(
            "old", unknown("new"), "correction-1", "human correction")
        self.snapshot = replaced.propose_withdrawal(
            "withdraw", "correction-2", "human withdrawal")
        self.pairs = (
            ("b", "a"), ("a", "b"), ("a", "c"),
            ("a", "b"), ("a", "a"), ("a", "isolated"),
        )

    def handoff(self, pairs=None, **kwargs):
        return build_readonly_chronology_handoff(
            self.snapshot, "u1", self.pairs if pairs is None else pairs,
            **kwargs,
        )

    def veto(self, code, callback):
        with self.assertRaises(ProposalRejected) as caught:
            callback()
        self.assertEqual(str(caught.exception), code)

    def test_requested_pair_order_preserved(self):
        handoff = self.handoff()
        self.assertEqual(
            [(x.left_anchor_id, x.right_anchor_id) for x in handoff.comparisons],
            list(self.pairs))

    def test_explicit_relations_without_total_sort(self):
        self.assertEqual(
            [r.relation for r in self.handoff().comparisons],
            ["after", "before", "before", "before", "same", "incomparable"])

    def test_message_keys_are_not_calendar_interpretation(self):
        keys = [r.relation_message_key for r in self.handoff().comparisons]
        self.assertEqual(keys[0], "explicit_right_precedes_left")
        self.assertEqual(keys[1], "explicit_left_precedes_right")
        self.assertEqual(keys[4], "same_selected_anchor")
        self.assertEqual(keys[5], "no_relative_world_order_established")

    def test_reversed_and_repeated_group_id(self):
        self.assertEqual(
            [r.unordered_pair_group_ordinal for r in self.handoff().comparisons],
            [1, 1, 2, 1, 3, 4])

    def test_first_occurrence_is_only_request_ordinal(self):
        self.assertEqual(
            [r.first_request_ordinal for r in self.handoff().comparisons],
            [1, 1, 3, 1, 5, 6])

    def test_mixed_orientations_are_kept(self):
        self.assertEqual(
            [r.orientation for r in self.handoff().comparisons],
            ["first", "reversed", "first", "reversed", "first", "first"])

    def test_original_authored_link_ids_not_labels(self):
        self.assertEqual(
            self.handoff(witness_page_size=2).comparisons[2].first_page_precedence_ids,
            ("p-ab", "p-bc"))

    def test_after_link_is_not_reversed(self):
        self.assertEqual(
            self.handoff().comparisons[0].first_page_precedence_ids, ("p-ab",))

    def test_short_witness_has_no_more_pages(self):
        item = self.handoff().comparisons[0]
        self.assertFalse(item.evidence_continues)
        self.assertEqual(item.total_evidence_links, 1)

    def test_transitive_witness_page_is_bounded(self):
        item = self.handoff(witness_page_size=1).comparisons[2]
        self.assertEqual(item.first_page_precedence_ids, ("p-ab",))
        self.assertEqual(item.total_evidence_links, 2)
        self.assertTrue(item.evidence_continues)

    def test_same_has_no_fabricated_evidence(self):
        item = self.handoff().comparisons[4]
        self.assertEqual(item.first_page_precedence_ids, ())
        self.assertEqual(item.total_evidence_links, 0)
        self.assertFalse(item.evidence_continues)

    def test_incomparable_has_no_fabricated_evidence(self):
        item = self.handoff().comparisons[5]
        self.assertEqual(item.first_page_precedence_ids, ())
        self.assertEqual(item.total_evidence_links, 0)

    def test_source_positions_do_not_redefine_temporal_relation(self):
        value = self.handoff((("c", "a"),))
        self.assertGreater(
            value.comparisons[0].left_filtered_source_ordinal,
            value.comparisons[0].right_filtered_source_ordinal)
        self.assertEqual(value.comparisons[0].relation, "after")
        self.assertEqual(value.navigation_order,
                         "filtered_source_insertion_not_world_time")

    def test_filtered_endpoints_and_hidden_middle_link(self):
        value = self.handoff((("a", "c"),),
                             filters=NavigationFilters(text_contains="bell"))
        self.assertEqual(value.comparisons[0].total_evidence_links, 2)

    def test_filtered_out_endpoint_refused(self):
        self.veto("comparison_anchor_not_in_filtered_universe",
                  lambda: self.handoff(
                      (("a", "b"),),
                      filters=NavigationFilters(text_contains="Tenth")))

    def test_historical_replaced_endpoint_refused(self):
        self.veto("comparison_anchor_not_active",
                  lambda: self.handoff((("old", "a"),)))

    def test_historical_withdrawn_endpoint_refused(self):
        self.veto("comparison_anchor_not_active",
                  lambda: self.handoff((("withdraw", "a"),)))

    def test_other_universe_endpoint_refused(self):
        self.veto("comparison_anchor_not_in_filtered_universe",
                  lambda: self.handoff((("a", "foreign"),)))

    def test_late_bad_pair_refuses_entire_handoff(self):
        self.veto("comparison_anchor_not_in_filtered_universe",
                  lambda: self.handoff((("a", "b"), ("a", "missing"))))

    def test_empty_pairs_refused(self):
        self.veto("batch_pair_count_or_type_invalid",
                  lambda: self.handoff(()))

    def test_seventeen_pairs_refused(self):
        self.veto("batch_pair_count_or_type_invalid",
                  lambda: self.handoff((("a", "b"),) * 17))

    def test_sixteen_pairs_accepted(self):
        value = self.handoff((("a", "b"),) * 16)
        self.assertEqual(value.number_of_requests, 16)
        self.assertEqual(value.number_of_unordered_pair_groups, 1)

    def test_malformed_pair_shape_refused(self):
        self.veto("batch_pair_shape_invalid",
                  lambda: self.handoff((("a",),)))

    def test_invalid_snapshot_refused(self):
        self.veto("comparison_snapshot_type_invalid",
                  lambda: build_readonly_chronology_handoff(
                      None, "u1", (("a", "b"),)))

    def test_invalid_filter_refused(self):
        self.veto("navigation_filter_type_invalid",
                  lambda: self.handoff(filters={"enable_writer": True}))

    def test_invalid_width_refused(self):
        self.veto("selection_navigation_page_size_invalid",
                  lambda: self.handoff(navigation_page_size=0))
        self.veto("consultation_page_size_invalid",
                  lambda: self.handoff(witness_page_size=65))

    def test_runtime_never_claimed_available(self):
        handoff = self.handoff()
        self.assertEqual(handoff.runtime_integration, "not_implemented")
        self.assertEqual(handoff.database_access, "none")
        self.assertEqual(handoff.write_commands, ())

    def test_external_attestation_never_promoted(self):
        handoff = self.handoff()
        self.assertFalse(handoff.external_attestation_verified)
        self.assertFalse(handoff.operator_acceptance_verified)
        self.assertEqual(len(handoff.blocked_requirements), 3)

    def test_no_narrative_or_reader_reveal_inference(self):
        handoff = self.handoff()
        self.assertEqual(
            handoff.narration_order, "not_available_in_synthetic_projection")
        self.assertEqual(
            handoff.reader_reveal_order, "not_available_in_synthetic_projection")

    def test_json_has_no_raw_source_labels_or_revisions(self):
        value = readonly_handoff_json(self.handoff())
        for forbidden in (
            "Tenth Bell", "First Bell", "fictional-calendar", "human correction",
        ):
            self.assertNotIn(forbidden, value)

    def test_readonly_json_flags_and_determinism(self):
        h = self.handoff()
        self.assertEqual(readonly_handoff_json(h), readonly_handoff_json(h))
        parsed = json.loads(readonly_handoff_json(h))
        self.assertFalse(parsed["editing_authorized"])
        self.assertFalse(parsed["external_attestation_verified"])
        self.assertEqual(parsed["data_origin"], "synthetic_in_memory_reference_only")

    def test_bad_serialization_object_rejected(self):
        self.veto("handoff_result_type_invalid",
                  lambda: readonly_handoff_json({"editable": True}))

    def test_frozen_dto_and_snapshot_unchanged(self):
        snapshot = repr(self.snapshot)
        h = self.handoff()
        self.assertEqual(snapshot, repr(self.snapshot))
        with self.assertRaises(FrozenInstanceError):
            h.editing_authorized = True
        with self.assertRaises(FrozenInstanceError):
            h.comparisons[0].relation = "invented"

    def test_513_anchors_explicit_pair_only(self):
        many = tuple(unknown(f"id{i}") for i in range(513))
        snapshot = SyntheticSnapshot(
            many, (Precedence("p512", "u1", "id0", "id512"),))
        handoff = build_readonly_chronology_handoff(
            snapshot, "u1", (("id0", "id512"),),
            navigation_page_size=64)
        self.assertEqual(len(handoff.comparisons), 1)
        self.assertEqual(handoff.comparisons[0].right_filtered_source_ordinal, 513)


if __name__ == "__main__":
    unittest.main()
