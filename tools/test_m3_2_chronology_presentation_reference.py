"""Stage 22 Windows fixtures: bounded, synthetic, no data/files/SQLite."""
from dataclasses import FrozenInstanceError
import json
import unittest

from m3_2_supersession_reference import (
    Anchor, Precedence, ProposalRejected, SyntheticSnapshot,
)
from m3_2_chronology_presentation_reference import (
    MAX_PAIR_QUERIES, MAX_VISIBLE_ANCHORS, present_chronology,
    presentation_json,
)


def unknown(id, world="u1", source=None):
    return Anchor(id, world, "unknown", source_revision_id=source)


def exact(id, label, calendar="fictional", world="u1"):
    return Anchor(id, world, "exact", calendar_id=calendar, exact_label=label)


class ReadonlyPresentationFixtures(unittest.TestCase):
    def setUp(self):
        self.initial = SyntheticSnapshot(
            (
                exact("b", "third bell"),
                unknown("a", source="rev-historic"),
                exact("c", "first bell", calendar="another"),
                unknown("d"),
                unknown("outside", world="u2"),
            ),
            (Precedence("e", "u1", "a", "b"),),
        )

    def veto(self, code, action):
        with self.assertRaises(ProposalRejected) as err:
            action()
        self.assertEqual(str(err.exception), code)

    def test_world_only_and_source_insertion_order(self):
        panel = present_chronology(self.initial, "u1")
        self.assertEqual([x.anchor_id for x in panel.anchors],
                         ["b", "a", "c", "d"])
        self.assertEqual(panel.display_order_semantics,
                         "source_insertion_order_not_world_time")

    def test_other_universe_restricted(self):
        panel = present_chronology(self.initial, "u2")
        self.assertEqual([x.anchor_id for x in panel.anchors], ["outside"])

    def test_missing_universe_is_empty_not_leaked(self):
        self.assertEqual(present_chronology(self.initial, "missing").anchors, ())

    def test_unknown_universe_id_refused(self):
        self.veto("projection_universe_required",
                  lambda: present_chronology(self.initial, ""))

    def test_correction_is_historical_without_overwriting_original(self):
        changed = self.initial.propose_replacement(
            "d", unknown("d2", source="rev-42"), "event-1", "human correction")
        old = next(x for x in present_chronology(changed, "u1").anchors
                   if x.anchor_id == "d")
        self.assertEqual(old.status, "replaced")
        self.assertEqual(old.next_anchor_id, "d2")
        self.assertEqual(old.correction_reason, "human correction")
        self.assertEqual(old.lineage_anchor_ids, ("d", "d2"))
        self.assertEqual(old.lineage_event_ids, ("event-1",))
        self.assertEqual(old.lineage_reasons, ("human correction",))
        self.assertEqual(present_chronology(self.initial, "u1").anchors[-1].status,
                         "active")

    def test_retraction_keeps_original_card(self):
        changed = self.initial.propose_withdrawal("d", "withdraw", "retired")
        record = present_chronology(changed, "u1").anchors[-1]
        self.assertEqual(record.anchor_id, "d")
        self.assertEqual(record.status, "withdrawn")
        self.assertEqual(record.lineage_disposition, "withdrawn")
        self.assertIsNone(record.next_anchor_id)

    def test_multiple_corrections_preserve_all_reasons(self):
        first = self.initial.propose_replacement("d", unknown("d2"), "e1", "one")
        later = first.propose_replacement("d2", unknown("d3"), "e2", "two")
        original = next(x for x in present_chronology(later, "u1").anchors
                        if x.anchor_id == "d")
        self.assertEqual(original.lineage_anchor_ids, ("d", "d2", "d3"))
        self.assertEqual(original.lineage_reasons, ("one", "two"))

    def test_human_precedence_before_after(self):
        panel = present_chronology(self.initial, "u1",
                                   comparisons=(("a", "b"), ("b", "a")))
        self.assertEqual([x.result for x in panel.comparisons],
                         ["before", "after"])

    def test_disconnected_anchors_explicitly_incomparable(self):
        panel = present_chronology(self.initial, "u1",
                                   comparisons=(("b", "c"),))
        self.assertEqual(panel.comparisons[0].result, "incomparable")

    def test_same_anchor_explicitly_same(self):
        panel = present_chronology(self.initial, "u1",
                                   comparisons=(("a", "a"),))
        self.assertEqual(panel.comparisons[0].result, "same")

    def test_world_calendar_labels_not_sorted_or_parsed(self):
        panel = present_chronology(self.initial, "u1")
        self.assertEqual(panel.anchors[0].exact_label, "third bell")
        self.assertEqual(panel.anchors[2].exact_label, "first bell")
        self.assertEqual(panel.anchors[2].calendar_id, "another")

    def test_revision_id_kept_not_switched_to_latest(self):
        panel = present_chronology(self.initial, "u1")
        self.assertEqual(panel.anchors[1].source_revision_id, "rev-historic")

    def test_narration_reveal_and_editing_not_available(self):
        panel = present_chronology(self.initial, "u1")
        self.assertFalse(panel.edit_controls_available)
        self.assertEqual(panel.reader_reveal_order,
                         "not_available_in_synthetic_projection")
        self.assertEqual(panel.narration_order,
                         "not_available_in_synthetic_projection")
        self.assertEqual(panel.data_origin, "synthetic_in_memory_reference_only")

    def test_cross_universe_pair_query_fails_closed(self):
        self.veto("projection_anchor_not_found_in_universe",
                  lambda: present_chronology(
                      self.initial, "u1", comparisons=(("a", "outside"),)))

    def test_withdrawn_pair_query_refused(self):
        changed = self.initial.propose_withdrawal("d", "retire", "human")
        self.veto("projection_anchor_not_active",
                  lambda: present_chronology(
                      changed, "u1", comparisons=(("d", "b"),)))

    def test_wrong_type_comparisons_refused(self):
        self.veto("presentation_invalid_comparison_batch",
                  lambda: present_chronology(self.initial, "u1",
                                             comparisons=[("a", "b")]))

    def test_invalid_comparison_item_shape_refused(self):
        self.veto("presentation_comparison_shape_invalid",
                  lambda: present_chronology(
                      self.initial, "u1", comparisons=(("a",),)))

    def test_blank_comparison_id_refused(self):
        self.veto("presentation_comparison_shape_invalid",
                  lambda: present_chronology(
                      self.initial, "u1", comparisons=(("", "b"),)))

    def test_duplicate_pairs_refused(self):
        self.veto("presentation_duplicate_comparisons",
                  lambda: present_chronology(
                      self.initial, "u1",
                      comparisons=(("a", "b"), ("a", "b"))))

    def test_too_many_comparisons_refused(self):
        batch = tuple((str(i), str(i + 1)) for i in range(MAX_PAIR_QUERIES + 1))
        self.veto("presentation_invalid_comparison_batch",
                  lambda: present_chronology(self.initial, "u1",
                                             comparisons=batch))

    def test_too_many_anchors_refused(self):
        many = SyntheticSnapshot(tuple(unknown(f"a{i}") for i in
                                       range(MAX_VISIBLE_ANCHORS + 1)))
        self.veto("presentation_too_many_anchors",
                  lambda: present_chronology(many, "u1"))

    def test_max_anchors_accepted_without_sorting(self):
        many = SyntheticSnapshot(tuple(unknown(f"a{i}") for i in
                                       range(MAX_VISIBLE_ANCHORS)))
        panel = present_chronology(many, "u1")
        self.assertEqual(len(panel.anchors), MAX_VISIBLE_ANCHORS)
        self.assertEqual(panel.anchors[0].anchor_id, "a0")
        self.assertEqual(panel.anchors[-1].anchor_id,
                         f"a{MAX_VISIBLE_ANCHORS-1}")

    def test_payload_json_is_deterministic_and_valid(self):
        panel = present_chronology(self.initial, "u1",
                                   comparisons=(("a", "b"),))
        first = presentation_json(panel)
        self.assertEqual(first, presentation_json(panel))
        decoded = json.loads(first)
        self.assertEqual(decoded["comparisons"][0]["result"], "before")
        self.assertFalse(decoded["edit_controls_available"])

    def test_bad_panel_type_refused(self):
        self.veto("presentation_invalid_panel",
                  lambda: presentation_json({"editable": True}))

    def test_input_is_immutable_and_output_cards_are_frozen(self):
        before = repr(self.initial)
        panel = present_chronology(self.initial, "u1")
        self.assertEqual(repr(self.initial), before)
        with self.assertRaises(FrozenInstanceError):
            panel.anchors[0].status = "editable"
        with self.assertRaises(FrozenInstanceError):
            panel.edit_controls_available = True


if __name__ == "__main__":
    unittest.main()
