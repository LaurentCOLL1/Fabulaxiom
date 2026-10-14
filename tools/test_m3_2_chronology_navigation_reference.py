"""Stage24 navigation filters and cursor invariants, synthetic only."""
import base64
from dataclasses import FrozenInstanceError
import json
import unittest

from m3_2_supersession_reference import (
    Anchor, Precedence, ProposalRejected, SyntheticSnapshot,
)
from m3_2_chronology_navigation_reference import (
    NavigationFilters, navigate_chronology, navigation_json,
)


def exact(identifier, label, universe="u1", calendar="Cal"):
    return Anchor(identifier, universe, "exact",
                  calendar_id=calendar, exact_label=label)


def unknown(identifier, universe="u1", revision=None):
    return Anchor(identifier, universe, "unknown", source_revision_id=revision)


def approximate(identifier, universe="u1"):
    return Anchor(identifier, universe, "approximate",
                  calendar_id="Cal", window_start_text="Early Harvest",
                  precision_text="season")


class SyntheticNavigationTests(unittest.TestCase):
    def setUp(self):
        self.initial = SyntheticSnapshot((
            exact("e", "Third Bell"),
            unknown("old", revision="rev-original"),
            approximate("a"),
            exact("other-calendar", "First Bell", calendar="Other"),
            unknown("withdraw"),
            unknown("outside", "u2"),
            exact("b", "Tenth Bell"),
        ), (Precedence("p1", "u1", "e", "b"),))
        x = self.initial.propose_replacement(
            "old", unknown("new", revision="rev-updated"), "event1",
            "human rectification")
        self.snapshot = x.propose_withdrawal("withdraw", "event2", "retired")

    def veto(self, code, action):
        with self.assertRaises(ProposalRejected) as cm:
            action()
        self.assertEqual(str(cm.exception), code)

    def test_unfiltered_ids_preserve_insertion_order(self):
        result = navigate_chronology(self.snapshot, "u1")
        self.assertEqual([c.anchor_id for c in result.anchor_cards],
                         ["e", "old", "a", "other-calendar", "withdraw", "b", "new"])
        self.assertEqual(result.total_matches, 7)

    def test_universe_isolation(self):
        result = navigate_chronology(self.snapshot, "u2")
        self.assertEqual([c.anchor_id for c in result.anchor_cards], ["outside"])

    def test_absent_universe_empty(self):
        page = navigate_chronology(self.snapshot, "u404")
        self.assertEqual(page.anchor_cards, ())
        self.assertEqual(page.total_matches, 0)
        self.assertIsNone(page.next_cursor)

    def test_filter_active_only(self):
        page = navigate_chronology(
            self.snapshot, "u1", filters=NavigationFilters(statuses=("active",)))
        self.assertEqual([x.anchor_id for x in page.anchor_cards],
                         ["e", "a", "other-calendar", "b", "new"])

    def test_filter_replaced_only(self):
        page = navigate_chronology(
            self.snapshot, "u1", filters=NavigationFilters(statuses=("replaced",)))
        self.assertEqual([x.anchor_id for x in page.anchor_cards], ["old"])
        self.assertEqual(page.anchor_cards[0].lineage_anchor_ids, ("old", "new"))

    def test_filter_withdrawn_only(self):
        page = navigate_chronology(
            self.snapshot, "u1", filters=NavigationFilters(statuses=("withdrawn",)))
        self.assertEqual([x.anchor_id for x in page.anchor_cards], ["withdraw"])
        self.assertEqual(page.anchor_cards[0].lineage_reasons, ("retired",))

    def test_filter_multiple_statuses(self):
        page = navigate_chronology(
            self.snapshot, "u1",
            filters=NavigationFilters(statuses=("replaced", "withdrawn")))
        self.assertEqual([x.anchor_id for x in page.anchor_cards],
                         ["old", "withdraw"])

    def test_filter_exact_time_kind_only(self):
        page = navigate_chronology(
            self.snapshot, "u1", filters=NavigationFilters(time_kinds=("exact",)))
        self.assertEqual([x.anchor_id for x in page.anchor_cards],
                         ["e", "other-calendar", "b"])

    def test_filter_multiple_time_kinds(self):
        page = navigate_chronology(
            self.snapshot, "u1",
            filters=NavigationFilters(time_kinds=("exact", "approximate")))
        self.assertEqual([x.anchor_id for x in page.anchor_cards],
                         ["e", "a", "other-calendar", "b"])

    def test_filter_calendar_is_exact_not_inferred(self):
        page = navigate_chronology(
            self.snapshot, "u1", filters=NavigationFilters(calendar_id="Other"))
        self.assertEqual([x.anchor_id for x in page.anchor_cards],
                         ["other-calendar"])

    def test_filter_specific_historical_revision(self):
        page = navigate_chronology(
            self.snapshot, "u1",
            filters=NavigationFilters(source_revision_id="rev-original"))
        self.assertEqual([x.anchor_id for x in page.anchor_cards], ["old"])
        self.assertEqual(page.anchor_cards[0].source_revision_id, "rev-original")

    def test_casefold_text_literal_search(self):
        page = navigate_chronology(
            self.snapshot, "u1",
            filters=NavigationFilters(text_contains="third bell"))
        self.assertEqual([x.anchor_id for x in page.anchor_cards], ["e"])

    def test_text_search_scans_raw_approximate_window(self):
        page = navigate_chronology(
            self.snapshot, "u1",
            filters=NavigationFilters(text_contains="harvest"))
        self.assertEqual([x.anchor_id for x in page.anchor_cards], ["a"])

    def test_text_search_not_hidden_date_comparison(self):
        page = navigate_chronology(
            self.snapshot, "u1",
            filters=NavigationFilters(text_contains="First Bell"))
        self.assertEqual([x.anchor_id for x in page.anchor_cards],
                         ["other-calendar"])
        self.assertEqual(page.display_order_semantics,
                         "source_insertion_order_not_world_time")

    def test_combined_filters(self):
        page = navigate_chronology(
            self.snapshot, "u1",
            filters=NavigationFilters(statuses=("active",),
                                      time_kinds=("exact",),
                                      calendar_id="Cal",
                                      text_contains="bell"))
        self.assertEqual([x.anchor_id for x in page.anchor_cards], ["e", "b"])

    def test_no_matches_does_not_show_other_universe(self):
        page = navigate_chronology(
            self.snapshot, "u1",
            filters=NavigationFilters(source_revision_id="missing"))
        self.assertEqual(page.anchor_cards, ())
        self.assertEqual(page.total_matches, 0)

    def test_forward_pagination_on_filtered_set(self):
        f = NavigationFilters(time_kinds=("exact",))
        p1 = navigate_chronology(self.snapshot, "u1", filters=f, page_size=2)
        p2 = navigate_chronology(self.snapshot, "u1", filters=f,
                                 page_size=2, cursor=p1.next_cursor)
        self.assertEqual([x.anchor_id for x in p1.anchor_cards],
                         ["e", "other-calendar"])
        self.assertEqual([x.anchor_id for x in p2.anchor_cards], ["b"])
        self.assertIsNone(p2.next_cursor)

    def test_backward_pagination_returns_first_page(self):
        f = NavigationFilters(time_kinds=("exact",))
        first = navigate_chronology(self.snapshot, "u1", filters=f, page_size=2)
        second = navigate_chronology(self.snapshot, "u1", filters=f, page_size=2,
                                     cursor=first.next_cursor)
        again = navigate_chronology(self.snapshot, "u1", filters=f, page_size=2,
                                    cursor=second.previous_cursor)
        self.assertEqual(first.anchor_cards, again.anchor_cards)
        self.assertIsNone(first.previous_cursor)

    def test_pagination_more_than_512_anchors_without_full_panel(self):
        large = SyntheticSnapshot(tuple(unknown(f"id{i}") for i in range(513)))
        ids = []
        cursor = None
        for _ in range(9):
            page = navigate_chronology(large, "u1", page_size=64, cursor=cursor)
            ids.extend(x.anchor_id for x in page.anchor_cards)
            cursor = page.next_cursor
            if cursor is None:
                break
        self.assertEqual(len(ids), 513)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertIsNone(cursor)

    def test_cursor_refuses_filter_change(self):
        initial = navigate_chronology(
            self.snapshot, "u1", page_size=1,
            filters=NavigationFilters(statuses=("active",)))
        self.veto("navigation_cursor_stale_snapshot_or_filters", lambda:
                  navigate_chronology(self.snapshot, "u1", page_size=1,
                                     filters=NavigationFilters(statuses=("replaced",)),
                                     cursor=initial.next_cursor))

    def test_cursor_refuses_same_filter_but_changed_snapshot(self):
        original = navigate_chronology(self.snapshot, "u1", page_size=1)
        altered = self.snapshot.propose_replacement(
            "new", unknown("new2"), "event3", "another correction")
        self.veto("navigation_cursor_stale_snapshot_or_filters", lambda:
                  navigate_chronology(altered, "u1", page_size=1,
                                     cursor=original.next_cursor))

    def test_cursor_refuses_cross_universe(self):
        original = navigate_chronology(self.snapshot, "u1", page_size=1)
        self.veto("navigation_cursor_wrong_universe", lambda:
                  navigate_chronology(self.snapshot, "u2",
                                     cursor=original.next_cursor))

    def test_invalid_status_refused(self):
        self.veto("navigation_statuses_invalid", lambda:
                  navigate_chronology(self.snapshot, "u1",
                                     filters=NavigationFilters(statuses=("edited",))))

    def test_duplicate_status_refused(self):
        self.veto("navigation_statuses_invalid", lambda:
                  navigate_chronology(
                      self.snapshot, "u1",
                      filters=NavigationFilters(statuses=("active", "active"))))

    def test_invalid_time_kind_refused(self):
        self.veto("navigation_time_kinds_invalid", lambda:
                  navigate_chronology(
                      self.snapshot, "u1",
                      filters=NavigationFilters(time_kinds=("gregorian",))))

    def test_unexpected_filter_type_refused(self):
        self.veto("navigation_filter_type_invalid", lambda:
                  navigate_chronology(self.snapshot, "u1",
                                     filters={"editing": True}))

    def test_invalid_blank_literal_refused(self):
        self.veto("navigation_text_contains_invalid", lambda:
                  navigate_chronology(
                      self.snapshot, "u1",
                      filters=NavigationFilters(text_contains="  ")))

    def test_overlong_text_query_refused(self):
        self.veto("navigation_text_contains_invalid", lambda:
                  navigate_chronology(
                      self.snapshot, "u1",
                      filters=NavigationFilters(text_contains="x"*129)))

    def test_page_size_boolean_refused(self):
        self.veto("navigation_page_size_invalid", lambda:
                  navigate_chronology(self.snapshot, "u1", page_size=True))

    def test_out_of_range_page_size_refused(self):
        self.veto("navigation_page_size_invalid", lambda:
                  navigate_chronology(self.snapshot, "u1", page_size=65))

    def test_blank_universe_refused(self):
        self.veto("navigation_universe_required", lambda:
                  navigate_chronology(self.snapshot, " "))

    def test_invalid_snapshot_refused(self):
        self.veto("navigation_snapshot_type_invalid", lambda:
                  navigate_chronology([], "u1"))

    def test_json_deterministic_and_editing_disabled(self):
        panel = navigate_chronology(self.snapshot, "u1",
                                    filters=NavigationFilters(statuses=("active",)))
        self.assertEqual(navigation_json(panel), navigation_json(panel))
        value = json.loads(navigation_json(panel))
        self.assertFalse(value["editing_authorized"])
        self.assertEqual(value["data_origin"], "synthetic_in_memory_reference_only")
        self.assertEqual(value["filters"]["statuses"], ["active"])

    def test_invalid_output_object_refused(self):
        self.veto("navigation_page_type_invalid", lambda:
                  navigation_json({"editable": True}))

    def test_frozen_output_and_snapshot_not_mutated(self):
        previous = repr(self.snapshot)
        page = navigate_chronology(self.snapshot, "u1", page_size=3)
        self.assertEqual(previous, repr(self.snapshot))
        with self.assertRaises(FrozenInstanceError):
            page.editing_authorized = True


if __name__ == "__main__":
    unittest.main()
