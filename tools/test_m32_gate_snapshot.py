"""Negative tests for a dated, source-only Fabulaxiom M3.2 gate contract."""
from copy import deepcopy
import unittest

from m32_gate_snapshot import (
    GateRefusal, EXPECTED_ROLES, PROOFS, inspect_snapshot, load_snapshot,
)


class GateSnapshotRefusalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sample = load_snapshot()

    def assert_veto(self, transform):
        data = deepcopy(self.sample)
        transform(data)
        with self.assertRaises(GateRefusal):
            inspect_snapshot(data)

    def test_01_real_snapshot_source_only_and_still_blocked(self):
        decision = inspect_snapshot(self.sample)
        self.assertEqual(decision["real_G3"], "NOT_AUTHORIZED")
        self.assertEqual(decision["prospective"], "NOT_STARTED")
        self.assertEqual(decision["tauri_runtime"], "NOT_TESTED")

    def test_02_historical_three_sha_only_two_unanchored_are_distinct(self):
        roles = self.sample["historical"]["roles"]
        self.assertEqual({x["role"]: x["status"] for x in roles}, EXPECTED_ROLES)
        self.assertEqual(sum(x["status"] == "OBSERVED_SHA256_ONLY" for x in roles), 3)
        self.assertEqual(sum(x["status"] == "UNANCHORED_OBSERVED" for x in roles), 2)

    def test_03_historial_false_attestation_veto(self):
        self.assert_veto(lambda d: d["historical"].update(status="VERIFIED"))

    def test_04_an_observed_digest_cannot_become_independent_proof(self):
        self.assert_veto(lambda d: d["historical"]["roles"][0].update(status="VERIFIED"))

    def test_05_duplicate_historical_role_cannot_hide_missing_role(self):
        self.assert_veto(lambda d: d["historical"]["roles"][4].update(
            role="production/activation_marker"))

    def test_06_missing_role_cannot_shrink_scope(self):
        self.assert_veto(lambda d: d["historical"]["roles"].pop())

    def test_07_pr35_must_stay_draft(self):
        self.assert_veto(lambda d: d["development"].update(pr35="MERGED"))

    def test_08_historical_issue_cannot_be_marked_closed(self):
        self.assert_veto(lambda d: d["development"]["issues"].update({"36": "CLOSED"}))

    def test_09_operator_g2_needs_separate_authorization(self):
        self.assert_veto(lambda d: d["operator_execution"].update(G2="AUTHORIZED"))

    def test_10_real_g3_needs_separate_authorization(self):
        self.assert_veto(lambda d: d["operator_execution"].update(G3="AUTHORIZED"))

    def test_11_prospective_cannot_be_promoted_by_ci(self):
        self.assert_veto(lambda d: d["prospective"].update(status="ACCEPTED"))

    def test_12_solo_policy_does_not_mean_human_independent_review(self):
        self.assert_veto(lambda d: d["prospective"].update(
            independent_human_review="VERIFIED"))

    def test_13_core_ci_is_not_tauri_webview_runtime(self):
        self.assert_veto(lambda d: d["technical_evidence"].update(
            tauri_webview_runtime="PASS"))

    def test_14_compile_only_core_has_no_g3_source_provenance(self):
        self.assert_veto(lambda d: d["technical_evidence"].update(
            real_g3_source_provenance="VERIFIED"))

    def test_15_positive_ci_count_not_an_authorization(self):
        self.assert_veto(lambda d: d["claims"].update(real_g3_authorized=True))

    def test_16_release_not_authorized(self):
        self.assert_veto(lambda d: d["operator_execution"].update(release="AUTHORIZED"))

    def test_17_no_stale_claim_that_ci_is_current_check(self):
        self.assert_veto(lambda d: d["checkpoint"].update(
            external_live_ci_recheck="NOT_REQUIRED"))

    def test_18_unreviewed_schema_key_fails_closed(self):
        self.assert_veto(lambda d: d.update(runtime_approved=True))

    def test_19_new_main_reference_needs_another_explicit_snapshot(self):
        self.assert_veto(lambda d: d["checkpoint"].update(last_merged_pr=83))

    def test_20_evidence_categories_are_closed_vocabulary(self):
        self.assertEqual(PROOFS["ci_synthetic_sqlite"], "PASS_SYNTHETIC_ONLY")
        self.assert_veto(lambda d: d["technical_evidence"].update(
            ci_synthetic_sqlite="PASS_REAL"))

if __name__ == "__main__":
    unittest.main()
