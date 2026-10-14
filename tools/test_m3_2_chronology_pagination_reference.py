"""Stage 23: disposable in-memory pagination, no user or SQLite file access."""
import base64
import json
import unittest

from m3_2_supersession_reference import (
    Anchor, Precedence, ProposalRejected, SyntheticSnapshot,
)
from m3_2_chronology_pagination_reference import (
    chronology_page, chronology_page_json, MAX_PAGE_SIZE,
)
from m3_2_chronology_presentation_reference import present_chronology


def unknown(identifier, universe="u1", revision=None):
    return Anchor(identifier, universe, "unknown", source_revision_id=revision)


def encoded(data):
    return base64.urlsafe_b64encode(
        json.dumps(data, separators=(",", ":")).encode("utf-8")
    ).decode("ascii")


class PaginationFixtureTests(unittest.TestCase):
    def setUp(self):
        self.base = SyntheticSnapshot((
            unknown("a"), unknown("cross", "u2"),
            Anchor("b", "u1", "exact", "fictional", exact_label="third bell"),
            unknown("c", revision="immutable-rev-3"), unknown("d"),
        ), (Precedence("p1", "u1", "a", "b"),))

    def veto(self, reason, fn):
        with self.assertRaises(ProposalRejected) as result:
            fn()
        self.assertEqual(str(result.exception), reason)

    def test_source_insertion_order_not_world_time(self):
        page = chronology_page(self.base, "u1")
        self.assertEqual([x.anchor_id for x in page.anchors], ["a", "b", "c", "d"])
        self.assertEqual(page.display_order_semantics,
                         "source_insertion_order_not_world_time")

    def test_cross_universe_excluded_on_every_page(self):
        one = chronology_page(self.base, "u1", page_size=2)
        two = chronology_page(self.base, "u1", page_size=2,
                              cursor=one.next_cursor)
        self.assertEqual([a.anchor_id for a in one.anchors], ["a", "b"])
        self.assertEqual([a.anchor_id for a in two.anchors], ["c", "d"])
        self.assertIsNone(two.next_cursor)

    def test_other_universe_has_only_its_own_anchor(self):
        page = chronology_page(self.base, "u2")
        self.assertEqual([x.anchor_id for x in page.anchors], ["cross"])

    def test_empty_universe_is_empty_page(self):
        page = chronology_page(self.base, "u3")
        self.assertEqual(page.anchors, ())
        self.assertIsNone(page.next_cursor)

    def test_513_anchors_use_multiple_pages_not_stage22_hard_veto(self):
        big = SyntheticSnapshot(tuple(unknown("a"+str(i)) for i in range(513)))
        self.veto("presentation_too_many_anchors",
                  lambda: present_chronology(big, "u1"))
        ids, cursor = [], None
        for _ in range(9):
            page = chronology_page(big, "u1", page_size=64, cursor=cursor)
            ids.extend(x.anchor_id for x in page.anchors)
            cursor = page.next_cursor
            if cursor is None:
                break
        self.assertIsNone(cursor)
        self.assertEqual(len(ids), 513)
        self.assertEqual(len(set(ids)), 513)
        self.assertEqual(ids[0], "a0")
        self.assertEqual(ids[-1], "a512")

    def test_card_values_match_previously_accepted_stage22(self):
        page = chronology_page(self.base, "u1")
        old = present_chronology(self.base, "u1")
        self.assertEqual(page.anchors, old.anchors)

    def test_replaced_card_preserves_complete_lineage(self):
        a = self.base.propose_replacement("d", unknown("d2"), "e1", "correction")
        b = a.propose_replacement("d2", unknown("d3"), "e2", "more evidence")
        cards = chronology_page(b, "u1", page_size=64).anchors
        old = next(x for x in cards if x.anchor_id == "d")
        self.assertEqual(old.status, "replaced")
        self.assertEqual(old.lineage_anchor_ids, ("d", "d2", "d3"))
        self.assertEqual(old.lineage_reasons, ("correction", "more evidence"))

    def test_withdrawn_record_not_erased(self):
        changed = self.base.propose_withdrawal("d", "event", "withdraw")
        cards = chronology_page(changed, "u1").anchors
        self.assertEqual(cards[-1].status, "withdrawn")
        self.assertEqual(cards[-1].lineage_disposition, "withdrawn")

    def test_stale_cursor_rejected_when_snapshot_changes(self):
        first = chronology_page(self.base, "u1", page_size=1)
        changed = self.base.propose_replacement("d", unknown("d2"),
                                                "evt", "corrected")
        self.veto("pagination_cursor_stale_snapshot", lambda:
                  chronology_page(changed, "u1", page_size=1,
                                  cursor=first.next_cursor))

    def test_wrong_universe_cursor_rejected(self):
        first = chronology_page(self.base, "u1", page_size=1)
        self.veto("pagination_cursor_wrong_universe", lambda:
                  chronology_page(self.base, "u2", cursor=first.next_cursor))

    def test_same_input_produces_same_cursor(self):
        first = chronology_page(self.base, "u1", page_size=1)
        repeat = chronology_page(self.base, "u1", page_size=1)
        self.assertEqual(first.next_cursor, repeat.next_cursor)

    def test_cursor_does_not_claim_authentication_or_editing(self):
        page = chronology_page(self.base, "u1", page_size=2)
        decoded = json.loads(base64.urlsafe_b64decode(page.next_cursor))
        self.assertEqual(set(decoded), {"v", "u", "fp", "offset"})
        self.assertFalse(page.edit_controls_available)
        self.assertEqual(page.data_origin, "synthetic_in_memory_reference_only")

    def test_cursor_version_mismatch_rejected(self):
        first = chronology_page(self.base, "u1", page_size=1)
        payload = json.loads(base64.urlsafe_b64decode(first.next_cursor))
        payload["v"] = 2
        self.veto("pagination_cursor_version_invalid", lambda:
                  chronology_page(self.base, "u1", cursor=encoded(payload)))

    def test_cursor_boolean_offset_rejected(self):
        first = chronology_page(self.base, "u1", page_size=1)
        payload = json.loads(base64.urlsafe_b64decode(first.next_cursor))
        payload["offset"] = True
        self.veto("pagination_cursor_offset_invalid", lambda:
                  chronology_page(self.base, "u1", cursor=encoded(payload)))

    def test_cursor_negative_offset_rejected(self):
        first = chronology_page(self.base, "u1", page_size=1)
        payload = json.loads(base64.urlsafe_b64decode(first.next_cursor))
        payload["offset"] = -1
        self.veto("pagination_cursor_offset_invalid", lambda:
                  chronology_page(self.base, "u1", cursor=encoded(payload)))

    def test_cursor_offset_at_end_rejected(self):
        first = chronology_page(self.base, "u1", page_size=1)
        payload = json.loads(base64.urlsafe_b64decode(first.next_cursor))
        payload["offset"] = 4
        self.veto("pagination_cursor_offset_invalid", lambda:
                  chronology_page(self.base, "u1", cursor=encoded(payload)))

    def test_cursor_extra_field_rejected(self):
        first = chronology_page(self.base, "u1", page_size=1)
        payload = json.loads(base64.urlsafe_b64decode(first.next_cursor))
        payload["authorized_writer"] = True
        self.veto("pagination_cursor_shape_invalid", lambda:
                  chronology_page(self.base, "u1", cursor=encoded(payload)))

    def test_cursor_malformed_base64_rejected(self):
        self.veto("pagination_cursor_invalid_encoding", lambda:
                  chronology_page(self.base, "u1", cursor="**"))

    def test_oversized_cursor_rejected(self):
        self.veto("pagination_cursor_shape_invalid", lambda:
                  chronology_page(self.base, "u1", cursor="A"*4097))

    def test_non_string_cursor_rejected(self):
        self.veto("pagination_cursor_shape_invalid", lambda:
                  chronology_page(self.base, "u1", cursor=12))

    def test_page_size_zero_refused(self):
        self.veto("pagination_page_size_invalid", lambda:
                  chronology_page(self.base, "u1", page_size=0))

    def test_page_size_boolean_refused(self):
        self.veto("pagination_page_size_invalid", lambda:
                  chronology_page(self.base, "u1", page_size=True))

    def test_page_size_too_large_refused(self):
        self.veto("pagination_page_size_invalid", lambda:
                  chronology_page(self.base, "u1", page_size=MAX_PAGE_SIZE+1))

    def test_invalid_universe_refused(self):
        self.veto("pagination_universe_required", lambda:
                  chronology_page(self.base, "  "))

    def test_invalid_snapshot_refused(self):
        self.veto("pagination_snapshot_type_invalid", lambda:
                  chronology_page({"anchors": []}, "u1"))

    def test_json_output_deterministic_no_edit(self):
        page = chronology_page(self.base, "u1", page_size=2)
        raw = chronology_page_json(page)
        self.assertEqual(raw, chronology_page_json(page))
        parsed = json.loads(raw)
        self.assertFalse(parsed["edit_controls_available"])
        self.assertEqual(parsed["anchors"][1]["exact_label"], "third bell")

    def test_wrong_page_type_rejected(self):
        self.veto("pagination_page_type_invalid", lambda:
                  chronology_page_json({"editable": True}))

    def test_snapshot_never_mutated_by_paging(self):
        before = repr(self.base)
        first = chronology_page(self.base, "u1", page_size=2)
        chronology_page(self.base, "u1", cursor=first.next_cursor)
        self.assertEqual(repr(self.base), before)


if __name__ == "__main__":
    unittest.main()
