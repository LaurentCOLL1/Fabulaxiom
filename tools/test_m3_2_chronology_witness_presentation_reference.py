"""M3.2 Stage27 synthetic-only witness presentation adversarial fixtures."""
from dataclasses import FrozenInstanceError
import json
import unittest

from m3_2_chronology_navigation_reference import NavigationFilters
from m3_2_chronology_witness_presentation_reference import (
    present_world_order_witness, witness_panel_json,
)
from m3_2_supersession_reference import (
    Anchor, Precedence, ProposalRejected, SyntheticSnapshot,
)


def exact(identifier, label, calendar="cal", universe="u1", revision=None):
    return Anchor(identifier, universe, "exact", calendar_id=calendar,
                  exact_label=label, source_revision_id=revision)


def unknown(identifier, universe="u1", revision=None):
    return Anchor(identifier, universe, "unknown", source_revision_id=revision)


class WorldOrderWitnessPresentationTests(unittest.TestCase):
    def setUp(self):
        self.initial = SyntheticSnapshot((
            exact("a", "Tenth Bell", revision="secret-revision"),
            unknown("b"),
            exact("c", "First Bell"),
            exact("unlinked", "Zeroth Bell", calendar="other"),
            unknown("old", revision="historical-revision"),
            unknown("withdraw"),
            unknown("outside", universe="u2"),
            unknown("alternative"),
        ), (
            Precedence("p-ab", "u1", "a", "b"),
            Precedence("p-bc", "u1", "b", "c"),
            Precedence("p-a-alt", "u1", "a", "alternative"),
            Precedence("p-alt-c", "u1", "alternative", "c"),
        ))
        replaced = self.initial.propose_replacement(
            "old", unknown("new", revision="new-revision"),
            "correction-1", "human decision")
        self.snapshot = replaced.propose_withdrawal(
            "withdraw", "correction-2", "human retraction")

    def view(self, left, right, **kw):
        return present_world_order_witness(
            self.snapshot, "u1", left, right, **kw
        )

    def veto(self, code, action):
        with self.assertRaises(ProposalRejected) as ctx:
            action()
        self.assertEqual(str(ctx.exception), code)

    def test_before_message_explicit(self):
        panel = self.view("a", "b")
        self.assertEqual(panel.relation, "before")
        self.assertEqual(panel.relation_message_key,
                         "left_precedes_right_by_authored_links")

    def test_direct_step_preserves_original_ids(self):
        step, = self.view("a", "b").evidence_steps
        self.assertEqual((step.link_number, step.before_anchor_id,
                          step.precedence_id, step.after_anchor_id),
                         (1, "a", "p-ab", "b"))

    def test_reverse_after_message_and_forward_edge(self):
        panel = self.view("b", "a")
        self.assertEqual(panel.relation_message_key,
                         "right_precedes_left_by_authored_links")
        self.assertEqual(panel.path_start_anchor_id, "a")
        self.assertEqual(panel.path_end_anchor_id, "b")
        self.assertEqual(panel.evidence_steps[0].precedence_id, "p-ab")

    def test_transitive_steps_preserve_original_order(self):
        panel = self.view("a", "c")
        self.assertEqual([s.precedence_id for s in panel.evidence_steps],
                         ["p-ab", "p-bc"])
        self.assertEqual([s.link_number for s in panel.evidence_steps], [1, 2])
        self.assertEqual(panel.path_start_anchor_id, "a")
        self.assertEqual(panel.path_end_anchor_id, "c")

    def test_transitive_after_is_oriented_before_to_after(self):
        panel = self.view("c", "a")
        self.assertEqual(panel.relation, "after")
        self.assertEqual([s.before_anchor_id for s in panel.evidence_steps],
                         ["a", "b"])

    def test_equal_length_path_tie_does_not_invent_time(self):
        panel = self.view("a", "c")
        self.assertEqual(panel.evidence_steps[0].precedence_id, "p-ab")
        self.assertEqual(panel.witness_semantics,
                         "example_chain_not_unique_world_order")

    def test_shortest_single_edge_overrides_longer_examples(self):
        extended = SyntheticSnapshot(
            self.initial.anchors,
            self.initial.precedences + (Precedence("direct", "u1", "a", "c"),)
        )
        panel = present_world_order_witness(extended, "u1", "a", "c")
        self.assertEqual([s.precedence_id for s in panel.evidence_steps],
                         ["direct"])

    def test_same_id_has_no_fake_precedence(self):
        panel = self.view("a", "a")
        self.assertEqual(panel.relation, "same")
        self.assertEqual(panel.evidence_steps, ())
        self.assertEqual(panel.path_start_anchor_id, "a")
        self.assertEqual(panel.path_end_anchor_id, "a")
        self.assertEqual(panel.evidence_state,
                         "same_identity_no_precedence_required")

    def test_incomparable_has_no_chain_or_paths(self):
        panel = self.view("a", "unlinked")
        self.assertEqual(panel.relation, "incomparable")
        self.assertEqual(panel.evidence_steps, ())
        self.assertIsNone(panel.path_start_anchor_id)
        self.assertIsNone(panel.path_end_anchor_id)
        self.assertEqual(panel.relation_message_key,
                         "relative_world_order_not_established")

    def test_indeterminate_does_not_mean_impossible(self):
        panel = self.view("c", "unlinked")
        self.assertEqual(panel.evidence_state,
                         "no_authored_path_either_direction")

    def test_inverted_fictional_labels_do_not_invert_authored_link(self):
        self.assertEqual(self.view("a", "c").relation, "before")

    def test_unrelated_calendars_have_no_implied_order(self):
        self.assertEqual(self.view("unlinked", "c").relation, "incomparable")

    def test_filtered_endpoints_both_visible(self):
        panel = self.view(
            "a", "c", filters=NavigationFilters(text_contains="BELL"))
        self.assertEqual(len(panel.evidence_steps), 2)

    def test_intermediate_not_matching_filter_still_id_only(self):
        panel = self.view(
            "a", "c", filters=NavigationFilters(text_contains="bell"))
        self.assertEqual(panel.evidence_steps[0].after_anchor_id, "b")
        self.assertNotIn("secret-revision", witness_panel_json(panel))

    def test_filtered_endpoint_rejected(self):
        self.veto("comparison_anchor_not_in_filtered_universe",
            lambda: self.view(
                "a", "c", filters=NavigationFilters(text_contains="Tenth")))

    def test_wrong_universe_rejected(self):
        self.veto("comparison_anchor_not_in_filtered_universe",
                  lambda: self.view("a", "outside"))

    def test_unknown_id_rejected(self):
        self.veto("comparison_anchor_not_in_filtered_universe",
                  lambda: self.view("a", "missing"))

    def test_replaced_id_rejected(self):
        self.veto("comparison_anchor_not_active",
                  lambda: self.view("old", "new"))

    def test_withdrawn_id_rejected(self):
        self.veto("comparison_anchor_not_active",
                  lambda: self.view("withdraw", "a"))

    def test_same_withdrawn_id_rejected(self):
        self.veto("comparison_anchor_not_active",
                  lambda: self.view("withdraw", "withdraw"))

    def test_invalid_universe_rejected(self):
        self.veto("comparison_universe_required",
            lambda: present_world_order_witness(self.snapshot, " ", "a", "b"))

    def test_invalid_snapshot_rejected(self):
        self.veto("comparison_snapshot_type_invalid",
            lambda: present_world_order_witness(None, "u1", "a", "b"))

    def test_invalid_filters_rejected(self):
        self.veto("navigation_filter_type_invalid",
                  lambda: self.view("a", "b", filters={"editable": True}))

    def test_more_than_512_anchors_without_full_panel(self):
        many = SyntheticSnapshot(tuple(unknown(f"id{i}") for i in range(513)),
                                 (Precedence("p512", "u1", "id0", "id512"),))
        panel = present_world_order_witness(many, "u1", "id0", "id512")
        self.assertEqual(panel.evidence_steps[0].precedence_id, "p512")

    def test_read_only_and_unavailable_orders(self):
        panel = self.view("a", "c")
        self.assertFalse(panel.editing_authorized)
        self.assertEqual(panel.narration_order,
                         "not_available_in_synthetic_projection")
        self.assertEqual(panel.reader_reveal_order,
                         "not_available_in_synthetic_projection")
        self.assertEqual(panel.data_origin,
                         "synthetic_in_memory_reference_only")

    def test_output_never_includes_raw_calendar_source_text(self):
        panel = self.view("a", "c")
        value = witness_panel_json(panel)
        self.assertNotIn("Tenth Bell", value)
        self.assertNotIn("First Bell", value)
        self.assertNotIn("secret-revision", value)
        self.assertNotIn("cal", value)

    def test_json_is_deterministic_and_structured(self):
        panel = self.view("a", "c")
        encoded = witness_panel_json(panel)
        self.assertEqual(encoded, witness_panel_json(panel))
        parsed = json.loads(encoded)
        self.assertEqual(parsed["evidence_steps"][0]["link_number"], 1)
        self.assertEqual(parsed["evidence_visibility"], "identifiers_only")

    def test_serialization_rejects_non_panel(self):
        self.veto("witness_panel_type_invalid",
                  lambda: witness_panel_json({"editable": True}))

    def test_result_and_steps_frozen(self):
        panel = self.view("a", "c")
        with self.assertRaises(FrozenInstanceError):
            panel.editing_authorized = True
        with self.assertRaises(FrozenInstanceError):
            panel.evidence_steps[0].link_number = 500

    def test_snapshot_not_modified(self):
        original = repr(self.snapshot)
        self.view("a", "c")
        self.assertEqual(repr(self.snapshot), original)


if __name__ == "__main__":
    unittest.main()
