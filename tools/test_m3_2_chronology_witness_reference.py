"""M3.2 Stage26: authored-chain witness, deterministic synthetic tests."""
from dataclasses import FrozenInstanceError
import json
import unittest

from m3_2_chronology_navigation_reference import NavigationFilters
from m3_2_chronology_witness_reference import (
    explain_filtered_world_order, world_order_witness_json,
)
from m3_2_supersession_reference import (
    Anchor, Precedence, ProposalRejected, SyntheticSnapshot,
)


def exact(identifier, label, calendar="cal", universe="u1", revision=None):
    return Anchor(identifier, universe, "exact", calendar_id=calendar,
                  exact_label=label, source_revision_id=revision)


def unknown(identifier, universe="u1", revision=None):
    return Anchor(identifier, universe, "unknown", source_revision_id=revision)


class SyntheticWorldOrderWitnessTests(unittest.TestCase):
    def setUp(self):
        self.initial = SyntheticSnapshot((
            exact("a", "Tenth Bell", revision="rev-historic"),
            unknown("b"),
            exact("c", "First Bell"),
            exact("unlinked", "Zeroth Bell", calendar="other"),
            unknown("old", revision="rev-old"),
            unknown("withdraw"),
            unknown("outside", universe="u2"),
            unknown("alternate"),
        ), (
            Precedence("p-ab", "u1", "a", "b"),
            Precedence("p-bc", "u1", "b", "c"),
            Precedence("p-a-alt", "u1", "a", "alternate"),
            Precedence("p-alt-c", "u1", "alternate", "c"),
        ))
        changed = self.initial.propose_replacement(
            "old", unknown("new", revision="rev-new"),
            "event-1", "human correction")
        self.snapshot = changed.propose_withdrawal(
            "withdraw", "event-2", "human withdrawal")

    def witness(self, left, right, **kw):
        return explain_filtered_world_order(
            self.snapshot, "u1", left, right, **kw
        )

    def veto(self, code, fn):
        with self.assertRaises(ProposalRejected) as error:
            fn()
        self.assertEqual(str(error.exception), code)

    def test_direct_before_has_original_edge_id(self):
        result = self.witness("a", "b")
        self.assertEqual(result.relation, "before")
        self.assertEqual(result.chain_anchor_ids, ("a", "b"))
        self.assertEqual(result.chain_precedence_ids, ("p-ab",))

    def test_direct_after_uses_forward_world_edge(self):
        result = self.witness("b", "a")
        self.assertEqual(result.relation, "after")
        self.assertEqual(result.chain_anchor_ids, ("a", "b"))
        self.assertEqual(result.chain_precedence_ids, ("p-ab",))

    def test_transitive_before_preserves_both_human_links(self):
        result = self.witness("a", "c")
        self.assertEqual(result.relation, "before")
        self.assertEqual(result.chain_anchor_ids, ("a", "b", "c"))
        self.assertEqual(result.chain_precedence_ids, ("p-ab", "p-bc"))

    def test_transitive_after_preserves_forward_witness(self):
        result = self.witness("c", "a")
        self.assertEqual(result.relation, "after")
        self.assertEqual(result.chain_anchor_ids, ("a", "b", "c"))
        self.assertEqual(result.chain_precedence_ids, ("p-ab", "p-bc"))

    def test_ambiguous_equal_hop_path_is_stable_in_source_order(self):
        self.assertEqual(self.witness("a", "c").chain_anchor_ids,
                         ("a", "b", "c"))
        self.assertEqual(self.witness("a", "c").chain_precedence_ids,
                         ("p-ab", "p-bc"))

    def test_direct_edge_is_shorter_than_transitive_path(self):
        direct = SyntheticSnapshot(self.initial.anchors,
            self.initial.precedences +
            (Precedence("p-ac", "u1", "a", "c"),))
        result = explain_filtered_world_order(direct, "u1", "a", "c")
        self.assertEqual(result.chain_anchor_ids, ("a", "c"))
        self.assertEqual(result.chain_precedence_ids, ("p-ac",))

    def test_same_active_id_needs_no_precedence(self):
        result = self.witness("a", "a")
        self.assertEqual(result.relation, "same")
        self.assertEqual(result.chain_anchor_ids, ("a",))
        self.assertEqual(result.chain_precedence_ids, ())

    def test_incomparable_has_no_invented_witness(self):
        result = self.witness("unlinked", "a")
        self.assertEqual(result.relation, "incomparable")
        self.assertEqual(result.chain_anchor_ids, ())
        self.assertEqual(result.chain_precedence_ids, ())

    def test_incomparable_not_claimed_equal_or_impossible(self):
        result = self.witness("c", "unlinked")
        self.assertEqual(result.relation, "incomparable")
        self.assertEqual(result.chain_precedence_ids, ())

    def test_calendar_text_does_not_invert_authored_order(self):
        self.assertEqual(self.witness("a", "c").relation, "before")

    def test_different_calendars_do_not_infer_any_witness(self):
        self.assertEqual(self.witness("c", "unlinked").chain_anchor_ids, ())

    def test_status_filter_active_keeps_valid_witness(self):
        result = self.witness("a", "c",
                              filters=NavigationFilters(statuses=("active",)))
        self.assertEqual(result.chain_precedence_ids, ("p-ab", "p-bc"))

    def test_text_filter_applies_to_endpoints_only(self):
        result = self.witness("a", "c",
                              filters=NavigationFilters(text_contains="Bell"))
        self.assertEqual(result.chain_anchor_ids, ("a", "b", "c"))

    def test_intermediate_data_is_id_only_no_label(self):
        result = self.witness("a", "c")
        data = json.loads(world_order_witness_json(result))
        self.assertNotIn("Tenth Bell", str(data))
        self.assertNotIn("rev-historic", str(data))

    def test_filter_excludes_one_endpoint_fail_closed(self):
        self.veto("comparison_anchor_not_in_filtered_universe",
            lambda: self.witness("a", "c",
                filters=NavigationFilters(text_contains="Tenth")))

    def test_cross_universe_endpoint_rejected(self):
        self.veto("comparison_anchor_not_in_filtered_universe",
                  lambda: self.witness("a", "outside"))

    def test_nonexistent_endpoint_rejected(self):
        self.veto("comparison_anchor_not_in_filtered_universe",
                  lambda: self.witness("a", "missing"))

    def test_replaced_anchor_rejected(self):
        self.veto("comparison_anchor_not_active",
                  lambda: self.witness("old", "new"))

    def test_withdrawn_anchor_rejected(self):
        self.veto("comparison_anchor_not_active",
                  lambda: self.witness("withdraw", "a"))

    def test_same_withdrawn_anchor_rejected(self):
        self.veto("comparison_anchor_not_active",
                  lambda: self.witness("withdraw", "withdraw"))

    def test_invalid_universe_rejected(self):
        self.veto("comparison_universe_required",
            lambda: explain_filtered_world_order(self.snapshot," ","a","b"))

    def test_invalid_snapshot_rejected(self):
        self.veto("comparison_snapshot_type_invalid",
            lambda: explain_filtered_world_order(None,"u1","a","b"))

    def test_invalid_id_type_rejected(self):
        for candidate in (None, True, 4, "", "  ", "x" * 257):
            with self.subTest(candidate=candidate):
                self.veto("comparison_anchor_id_invalid",
                          lambda: self.witness("a", candidate))

    def test_invalid_filter_rejected(self):
        self.veto("navigation_filter_type_invalid",
                  lambda: self.witness("a", "c", filters={"date": "today"}))

    def test_more_than_512_anchors_without_full_panel(self):
        items = tuple(unknown(f"id{i}") for i in range(513))
        large = SyntheticSnapshot(items,
            (Precedence("edge-512", "u1", "id0", "id512"),))
        result = explain_filtered_world_order(
            large, "u1", "id0", "id512")
        self.assertEqual(result.chain_precedence_ids, ("edge-512",))

    def test_chain_node_count_matches_edge_count(self):
        result = self.witness("a", "c")
        self.assertEqual(len(result.chain_anchor_ids),
                         len(result.chain_precedence_ids) + 1)

    def test_chain_semantics_not_total_chronology(self):
        result = self.witness("a", "c")
        self.assertEqual(result.chain_semantics,
                         "one_shortest_authored_precedence_chain")
        self.assertFalse(result.editing_authorized)
        self.assertEqual(result.data_origin,
                         "synthetic_in_memory_reference_only")

    def test_narration_and_reader_reveal_unavailable(self):
        result = self.witness("a", "c")
        self.assertEqual(result.narration_order,
                         "not_available_in_synthetic_projection")
        self.assertEqual(result.reader_reveal_order,
                         "not_available_in_synthetic_projection")

    def test_json_deterministic(self):
        result = self.witness("a", "c")
        self.assertEqual(world_order_witness_json(result),
                         world_order_witness_json(result))

    def test_invalid_output_rejected(self):
        self.veto("witness_result_type_invalid",
                  lambda: world_order_witness_json({"editable": True}))

    def test_result_frozen(self):
        result = self.witness("a", "c")
        with self.assertRaises(FrozenInstanceError):
            result.editing_authorized = True

    def test_original_snapshot_unchanged(self):
        before = repr(self.snapshot)
        self.witness("a", "c")
        self.assertEqual(repr(self.snapshot), before)


if __name__ == "__main__":
    unittest.main()
