"""Stage28 deterministic ID-only witness consultation and cursor fixtures."""
import base64
from dataclasses import FrozenInstanceError
import json
import unittest

from m3_2_chronology_navigation_reference import NavigationFilters
from m3_2_chronology_witness_consultation_reference import (
    consult_world_order_witness, witness_consultation_json,
)
from m3_2_supersession_reference import (
    Anchor, Precedence, ProposalRejected, SyntheticSnapshot,
)


def unknown(identifier, universe="u1"):
    return Anchor(identifier, universe, "unknown")


def exact(identifier, label, universe="u1"):
    return Anchor(identifier, universe, "exact",
                  calendar_id="fictional", exact_label=label)


class WitnessConsultationFixtures(unittest.TestCase):
    def setUp(self):
        base = SyntheticSnapshot((
            exact("a", "Tenth Bell"), unknown("b"),
            exact("c", "First Bell"), unknown("isolated"),
            unknown("old"), unknown("foreign", "u2"),
            unknown("x"), unknown("y"),
        ), (
            Precedence("p-ab", "u1", "a", "b"),
            Precedence("p-bc", "u1", "b", "c"),
        ))
        self.snapshot = base.propose_withdrawal("old", "retired", "obsolete")
        self.long = SyntheticSnapshot(
            tuple(unknown(f"n{i}") for i in range(73)),
            tuple(Precedence(f"edge{i}", "u1", f"n{i}", f"n{i+1}")
                  for i in range(72)),
        )

    def page(self, left="a", right="c", **kwargs):
        return consult_world_order_witness(
            self.snapshot, "u1", left, right, **kwargs
        )

    def veto(self, code, fn):
        with self.assertRaises(ProposalRejected) as result:
            fn()
        self.assertEqual(str(result.exception), code)

    def long_page(self, **kwargs):
        return consult_world_order_witness(
            self.long, "u1", "n0", "n72", **kwargs
        )

    def forged(self, cursor, offset):
        body = json.loads(base64.urlsafe_b64decode(cursor))
        body["offset"] = offset
        return base64.urlsafe_b64encode(
            json.dumps(body, separators=(",", ":")).encode("ascii")
        ).decode("ascii")

    def test_direct_authored_witness_one_step(self):
        page = self.page("a", "b")
        self.assertEqual(page.total_evidence_links, 1)
        self.assertEqual(page.evidence_steps[0].precedence_id, "p-ab")
        self.assertIsNone(page.next_cursor)

    def test_two_step_chain_has_original_link_numbers(self):
        page = self.page(page_size=2)
        self.assertEqual([s.link_number for s in page.evidence_steps], [1, 2])
        self.assertEqual([s.precedence_id for s in page.evidence_steps],
                         ["p-ab", "p-bc"])

    def test_reverse_selection_preserves_forward_world_links(self):
        page = self.page("c", "a", page_size=1)
        self.assertEqual(page.relation, "after")
        self.assertEqual(page.evidence_steps[0].before_anchor_id, "a")
        self.assertEqual(page.evidence_steps[0].after_anchor_id, "b")

    def test_second_page_keeps_absolute_link_number(self):
        first = self.page(page_size=1)
        last = self.page(page_size=1, cursor=first.next_cursor)
        self.assertEqual(last.evidence_steps[0].link_number, 2)
        self.assertEqual(last.evidence_steps[0].precedence_id, "p-bc")
        self.assertIsNone(last.next_cursor)

    def test_previous_page_restores_first(self):
        first = self.page(page_size=1)
        last = self.page(page_size=1, cursor=first.next_cursor)
        back = self.page(page_size=1, cursor=last.previous_cursor)
        self.assertEqual(first, back)
        self.assertIsNone(first.previous_cursor)

    def test_long_witness_72_links_over_64_maximum(self):
        first = self.long_page(page_size=64)
        second = self.long_page(page_size=64, cursor=first.next_cursor)
        self.assertEqual([len(first.evidence_steps), len(second.evidence_steps)],
                         [64, 8])
        self.assertEqual(second.evidence_steps[0].link_number, 65)
        self.assertEqual(second.evidence_steps[-1].link_number, 72)
        self.assertIsNone(second.next_cursor)

    def test_long_three_page_bidirectional_visit(self):
        cursor = None
        pages = []
        for _ in range(3):
            page = self.long_page(page_size=25, cursor=cursor)
            pages.append(page)
            cursor = page.next_cursor
        self.assertEqual([len(p.evidence_steps) for p in pages], [25, 25, 22])
        self.assertIsNone(cursor)
        ids = [s.precedence_id for p in pages for s in p.evidence_steps]
        self.assertEqual(ids, [f"edge{i}" for i in range(72)])
        back = self.long_page(page_size=25, cursor=pages[-1].previous_cursor)
        self.assertEqual(back.evidence_steps, pages[1].evidence_steps)

    def test_same_anchor_has_no_fake_link_or_cursor(self):
        page = self.page("a", "a")
        self.assertEqual(page.relation, "same")
        self.assertEqual(page.total_evidence_links, 0)
        self.assertEqual(page.evidence_steps, ())
        self.assertIsNone(page.next_cursor)
        self.assertIsNone(page.previous_cursor)

    def test_incomparable_has_no_fake_links(self):
        page = self.page("a", "isolated")
        self.assertEqual(page.relation, "incomparable")
        self.assertEqual(page.evidence_steps, ())
        self.assertEqual(page.evidence_state, "no_authored_path_either_direction")

    def test_empty_witness_rejects_non_null_cursor(self):
        cursor = self.page(page_size=1).next_cursor
        self.veto("consultation_cursor_stale_context",
                  lambda: self.page("a", "a", page_size=1, cursor=cursor))

    def test_page_size_change_refused(self):
        first = self.page(page_size=1)
        self.veto("consultation_cursor_stale_context",
                  lambda: self.page(page_size=2, cursor=first.next_cursor))

    def test_endpoint_change_refused(self):
        first = self.page(page_size=1)
        self.veto("consultation_cursor_stale_context",
                  lambda: self.page("a", "b", page_size=1,
                                    cursor=first.next_cursor))

    def test_reverse_selection_changes_cursor_scope(self):
        first = self.page(page_size=1)
        self.veto("consultation_cursor_stale_context",
                  lambda: self.page("c", "a", page_size=1,
                                    cursor=first.next_cursor))

    def test_filter_change_refused(self):
        first = self.page(page_size=1)
        self.veto("consultation_cursor_stale_context",
                  lambda: self.page(page_size=1, cursor=first.next_cursor,
                                    filters=NavigationFilters(statuses=("active",))))

    def test_snapshot_change_refused(self):
        first = self.page(page_size=1)
        changed = SyntheticSnapshot(
            self.snapshot.anchors + (unknown("additional"),),
            self.snapshot.precedences, self.snapshot.supersessions)
        self.veto("consultation_cursor_stale_context",
                  lambda: consult_world_order_witness(
                      changed, "u1", "a", "c", page_size=1,
                      cursor=first.next_cursor))

    def test_wrong_universe_cursor_refused(self):
        snapshot = SyntheticSnapshot(
            self.snapshot.anchors + (
                unknown("u2a", "u2"), unknown("u2b", "u2"),
            ),
            self.snapshot.precedences + (
                Precedence("u2edge", "u2", "u2a", "u2b"),
            ), self.snapshot.supersessions)
        initial = consult_world_order_witness(
            snapshot, "u1", "a", "c", page_size=1)
        self.veto("consultation_cursor_wrong_universe",
                  lambda: consult_world_order_witness(
                      snapshot, "u2", "u2a", "u2b", page_size=1,
                      cursor=initial.next_cursor))

    def test_out_of_universe_endpoint_refused(self):
        self.veto("comparison_anchor_not_in_filtered_universe",
                  lambda: self.page("a", "foreign"))

    def test_withdrawn_endpoint_refused(self):
        self.veto("comparison_anchor_not_active",
                  lambda: self.page("old", "a"))

    def test_bad_cursor_encoding_refused(self):
        self.veto("pagination_cursor_invalid_encoding",
                  lambda: self.page(page_size=1, cursor="??"))

    def test_boolean_cursor_offset_refused(self):
        first = self.page(page_size=1)
        self.veto("pagination_cursor_offset_invalid",
                  lambda: self.page(page_size=1,
                                    cursor=self.forged(first.next_cursor, True)))

    def test_negative_offset_refused(self):
        first = self.page(page_size=1)
        self.veto("consultation_cursor_offset_invalid",
                  lambda: self.page(page_size=1,
                                    cursor=self.forged(first.next_cursor, -1)))

    def test_non_aligned_offset_refused(self):
        first = self.long_page(page_size=3)
        self.veto("consultation_cursor_offset_invalid",
                  lambda: self.long_page(page_size=3,
                                         cursor=self.forged(first.next_cursor, 2)))

    def test_out_of_range_offset_refused(self):
        first = self.page(page_size=1)
        self.veto("consultation_cursor_offset_invalid",
                  lambda: self.page(page_size=1,
                                    cursor=self.forged(first.next_cursor, 200)))

    def test_tampered_fingerprint_refused(self):
        first = self.page(page_size=1)
        data = json.loads(base64.urlsafe_b64decode(first.next_cursor))
        data["fp"] = "0" * 64
        forged = base64.urlsafe_b64encode(
            json.dumps(data).encode("ascii")
        ).decode("ascii")
        self.veto("consultation_cursor_stale_context",
                  lambda: self.page(page_size=1, cursor=forged))

    def test_duplicate_cursor_keys_refused(self):
        first = self.page(page_size=1)
        data = json.loads(base64.urlsafe_b64decode(first.next_cursor))
        payload = ('{"v":1,"u":' + json.dumps(data["u"]) +
                   ',"fp":' + json.dumps(data["fp"]) +
                   ',"offset":1,"offset":1}')
        forged = base64.urlsafe_b64encode(payload.encode("ascii")).decode("ascii")
        self.veto("pagination_cursor_duplicate_key",
                  lambda: self.page(page_size=1, cursor=forged))

    def test_boolean_and_out_of_bounds_width_refused(self):
        for width in (True, False, 0, 65, -1, 1.0):
            with self.subTest(width=width):
                self.veto("consultation_page_size_invalid",
                          lambda: self.page(page_size=width))

    def test_wrong_snapshot_refused(self):
        self.veto("comparison_snapshot_type_invalid",
                  lambda: consult_world_order_witness(None, "u1", "a", "c"))

    def test_id_only_and_non_authoritative_transport(self):
        page = self.page(page_size=1)
        value = witness_consultation_json(page)
        for forbidden in ("Tenth Bell", "First Bell", "fictional"):
            self.assertNotIn(forbidden, value)
        obj = json.loads(value)
        self.assertFalse(obj["editing_authorized"])
        self.assertEqual(obj["data_origin"], "synthetic_in_memory_reference_only")
        self.assertEqual(obj["evidence_visibility"], "identifiers_only")
        self.assertEqual(obj["relation_message_key"],
                         "left_precedes_right_by_authored_links")

    def test_json_determinism_and_invalid_object(self):
        page = self.page(page_size=1)
        self.assertEqual(witness_consultation_json(page),
                         witness_consultation_json(page))
        self.veto("consultation_page_type_invalid",
                  lambda: witness_consultation_json({"writer": True}))

    def test_frozen_output_and_unchanged_snapshot(self):
        original = repr(self.snapshot)
        page = self.page(page_size=1)
        self.assertEqual(repr(self.snapshot), original)
        with self.assertRaises(FrozenInstanceError):
            page.editing_authorized = True
        with self.assertRaises(FrozenInstanceError):
            page.evidence_steps[0].link_number = 900


if __name__ == "__main__":
    unittest.main()
