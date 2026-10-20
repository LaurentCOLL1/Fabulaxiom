"""Offline handoff policy checks; not a live GitHub or operator authorization."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / "docs" / "continuity"

class HandoffContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((DIRECTORY / "HANDOFF_CURRENT.json").read_text(encoding="utf-8"))
        cls.doc = (DIRECTORY / "HANDOFF_CURRENT.md").read_text(encoding="utf-8")
        cls.policy = (DIRECTORY / "HANDOFF_PROTOCOL.md").read_text(encoding="utf-8")
        cls.index = (DIRECTORY / "README.md").read_text(encoding="utf-8")

    def test_01_dated_non_authorizing_checkpoint(self):
        self.assertEqual(self.data["status_kind"], "DATED_PUBLIC_SOURCE_HANDOFF_ONLY")
        self.assertTrue(self.data["live_refetch_required"])

    def test_02_repo_and_sha_format(self):
        self.assertEqual(self.data["repository"], "LaurentCOLL1/Fabulaxiom")
        for key in ("last_confirmed_main_before_handoff", "last_verified_pr_head"):
            self.assertRegex(self.data[key], r"^[0-9a-f]{40}$")

    def test_03_latest_verified_merge_not_promoted_to_runtime(self):
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 91)
        self.assertEqual(self.data["g2a"]["corrected_execution"], "STOP_WEBVIEW2_PARENTAGE")

    def test_04_pr35_and_external_issues_still_open(self):
        self.assertEqual(self.data["pr35"], "OPEN_DRAFT")
        self.assertEqual(self.data["issues"], {"36": "OPEN", "38": "OPEN"})

    def test_05_no_implicit_windows_authorization(self):
        self.assertEqual(self.data["g2a"]["exact_corrected_script_owner_approval"],
                         "APPROVED_FOR_ONE_MANUAL_RUN_CONSUMED")
        self.assertEqual(self.data["g2a"]["future_script_approval"],
                         "NEW_EXPLICIT_APPROVAL_REQUIRED_FOR_ANY_FURTHER_MANUAL_RUN")
        self.assertEqual(self.data["g2a"]["absence_of_sqlite_writer"], "NOT_PROVEN")

    def test_06_prospective_and_historical_not_promoted(self):
        self.assertEqual(self.data["governance"]["prospective"], "NOT_STARTED")
        self.assertEqual(self.data["governance"]["historic"], "PENDING_EXTERNAL_ATTESTATION(21/3/2)")
        self.assertEqual(self.data["governance"]["tauri_runtime"], "NOT_TESTED")

    def test_07_required_stop_scope(self):
        required = {"G2B", "G2C", "G2D", "G3", "G4", "G5", "G6",
                    "MIGRATION_007", "WRITER_IPC", "PR35_MERGE", "RELEASE"}
        self.assertTrue(required.issubset(set(self.data["prohibited"])))

    def test_08_all_critical_documents_in_index(self):
        for filename in ("HANDOFF_CURRENT.md", "HANDOFF_CURRENT.json",
                         "HANDOFF_PROTOCOL.md", "HANDOFF_HISTORY.md",
                         "NEXT.md", "STATE.md", "RESUME_PROMPT.md"):
            self.assertIn(filename, self.index)
            self.assertTrue((DIRECTORY / filename).is_file(), filename)

    def test_09_handoff_points_to_current_source(self):
        self.assertIn("SearchHost.exe", self.doc)
        self.assertIn("PR #86", self.doc)
        self.assertIn(self.data["last_confirmed_main_before_handoff"], self.doc)
        self.assertIn("STOP_WEBVIEW2_PARENTAGE", self.doc)

    def test_10_operator_stop_cannot_promote_any_gate(self):
        g = self.data['g2a']
        self.assertEqual(g['pr86_historic_stop']['stage'], 'WEBVIEW2_PARENTAGE')
        self.assertEqual(g['pr86_historic_stop']['reason'], 'UNEXPECTED_OR_UNSAFE')
        self.assertEqual(g['pr86_historic_stop']['subcause'], 'NOT_IDENTIFIABLE_FROM_SANITIZED_OUTPUT')
        self.assertEqual(g['absence_of_sqlite_writer'], 'NOT_PROVEN')
        self.assertEqual(self.data['governance']['prospective'], 'NOT_STARTED')
        self.assertEqual(self.data['governance']['tauri_runtime'], 'NOT_TESTED')
        self.assertIn('STOP_STAGE: WEBVIEW2_PARENTAGE', self.doc)
        self.assertIn('STOP_PROCESS_NAMES', self.doc)

    def test_11_new_candidate_stays_unexecuted_and_separate(self):
        c = self.data["g2a"]["future_candidate"]
        self.assertEqual(c["operator_execution"], "PASS_METADATA_ONLY_OWNER_REPORTED_SINGLE_RUN")
        self.assertEqual(c["cause_of_operator_stop"], "UNKNOWN_HISTORIC_PR86")
        self.assertEqual(c["review"], "EXACT_SCRIPT_REVIEWED_AND_ONE_TIME_RUN_CONSUMED")
        self.assertEqual(c["development_status"], "SOURCE_MERGED_AND_OWNER_REPORTED_LOCAL_METADATA_PASS")
        self.assertEqual(c["ci_run"], 39339365546)
        self.assertEqual(c["source_review_completed"], True)
        self.assertTrue((ROOT / c["path"]).is_file())
        self.assertIn("M3_2_G2A_PID_ZERO_CANDIDATE_REVIEW.md", self.index)
        self.assertIn("STOP_WEBVIEW2_PARENTAGE", self.doc)

    def test_12_local_metadata_pass_stays_tightly_bounded(self):
        g = self.data["g2a"]
        observation = g["latest_operator_observation"]
        self.assertEqual(observation["g2a_local_metadata"], "PASS")
        self.assertEqual(observation["webview2_searchhost_lineage"], 6)
        self.assertEqual(observation["lineage_evidence"], "OBSERVED_METADATA_ONLY")
        self.assertEqual(observation["webview2_ownership_authenticated"], "NO")
        self.assertEqual(observation["process_writer_absence"], "NOT_PROVEN")
        self.assertEqual(observation["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(observation["tauri_runtime"], "NOT_TESTED")
        self.assertEqual(observation["authorized_single_manual_execution"], "CONSUMED")
        self.assertEqual(g["absence_of_sqlite_writer"], "NOT_PROVEN")
        self.assertEqual(g["pr86_historic_stop"]["actual_runtime"], "STOP_WEBVIEW2_PARENTAGE")
        self.assertIn("G2A_LOCAL_METADATA: PASS", self.doc)
        self.assertIn("G2B_G2C_G2D_G3_G4_G5_G6: NOT_AUTHORIZED", self.doc)

    def test_13_writer_gap_is_source_only_refusal(self):
        review = self.data["g2a"]["writer_absence_review"]
        self.assertEqual(review["writer_absence"], "NOT_PROVEN")
        self.assertEqual(review["operator_execution"], "NOT_PERFORMED_NOT_AUTHORIZED")
        self.assertEqual(review["trusted_nonmigrating_owner"], "NOT_ESTABLISHED")
        self.assertEqual(review["even_all_fictional_checks_true"], "REAL_G3_STILL_STOP_UNAVAILABLE")
        self.assertEqual(review["open_private_sqlite_or_sidecars"], "PROHIBITED")
        self.assertEqual(self.data["g2a"]["latest_operator_observation"]["g2a_local_metadata"], "PASS")
        self.assertIn("M3_2_G2A_WRITER_ABSENCE_GAP_SOURCE_REVIEW.md", self.doc)
        self.assertIn("M3_2_G2A_WRITER_ABSENCE_GAP_SOURCE_REVIEW.md", self.index)
        self.assertIn("PROCESS_WRITER_ABSENCE: NOT_PROVEN", self.doc)

    def test_14_runtime_entrypoint_source_audit_is_not_g3_permission(self):
        d = self.data["g2a"]["runtime_entrypoint_source_audit"]
        self.assertTrue(d["source_only"])
        self.assertEqual(d["original_sqlite_access"], "PROHIBITED")
        self.assertEqual(d["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(d["writer_absence"], "NOT_PROVEN")
        self.assertEqual(d["operator_execution"], "NOT_AUTHORIZED")
        self.assertIn("TEXTUAL", d["warning"])
        self.assertTrue((ROOT / d["document"]).is_file())
        self.assertTrue((ROOT / d["script"]).is_file())
        self.assertTrue((ROOT / d["tests"]).is_file())
        self.assertIn("M3_2_G3_RUNTIME_ENTRYPOINT_SOURCE_AUDIT.md", self.doc)
        self.assertIn("M3_2_G3_RUNTIME_ENTRYPOINT_SOURCE_AUDIT.md", self.index)

    def test_15_current_gate_decision_cannot_promote_a_downstream_gate(self):
        d = self.data["gate_decision_current"]
        self.assertEqual(d["status"], "DATED_PUBLIC_SOURCE_HANDOFF_ONLY")
        self.assertEqual(d["scope"], "DOCUMENTARY_DECISION_NOT_EXECUTABLE")
        self.assertEqual(d["g2a"], "PASS_METADATA_ONLY_OWNER_REPORTED")
        for gate in ("g2b", "g2c", "g2d", "g4", "g5", "g6"):
            self.assertEqual(d[gate], "NOT_AUTHORIZED")
        self.assertEqual(d["g3"], "STOP_UNAVAILABLE_NOT_AUTHORIZED")
        self.assertEqual(d["process_writer_absence"], "NOT_PROVEN")
        self.assertEqual(d["historical"], "PENDING_EXTERNAL_ATTESTATION(21/3/2)")
        self.assertEqual(d["prospective"], "NOT_STARTED")
        self.assertEqual(d["last_operator_consent"], "SINGLE_G2A_PID_ZERO_RUN_CONSUMED")
        self.assertTrue((ROOT / d["document"]).is_file())
        self.assertIn("M3_2_GATE_DECISION_CURRENT.md", self.index)
        self.assertIn("M3_2_GATE_DECISION_CURRENT.md", self.doc)

    def test_16_wide_rust_sqlite_inventory_never_permits_real_g3(self):
        i = self.data["g2a"]["wide_rust_sqlite_inventory"]
        self.assertEqual(i["operator_execution"], "NOT_AUTHORIZED")
        self.assertEqual(i["actual_sqlite_access"], "NONE")
        self.assertEqual(i["absence_of_writer"], "NOT_PROVEN")
        self.assertEqual(i["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(i["gate_promotion"], "NEVER_AUTOMATIC")
        self.assertEqual(i["baseline_matched_files"], 21)
        self.assertEqual(i["test_count"], 18)
        self.assertTrue((ROOT / i["document"]).is_file())
        self.assertTrue((ROOT / i["scanner"]).is_file())
        self.assertTrue((ROOT / i["tests"]).is_file())
        self.assertIn("M3_2_WIDE_RUST_SQLITE_SITE_INVENTORY.md", self.doc)
        self.assertIn("M3_2_WIDE_RUST_SQLITE_SITE_INVENTORY.md", self.index)

    def test_17_preopened_ram_reader_only_toy_no_operator_access(self):
        t = self.data["g2a"]["preopened_ram_query_only_toy"]
        self.assertEqual(t["gates"], "CFG_TEST_AND_NONDEFAULT_FEATURE_ONLY")
        self.assertEqual(t["test_count"], 13)
        self.assertEqual(t["migration_invoked"], "NO")
        self.assertEqual(t["disk_source_opened"], "NONE")
        self.assertEqual(t["operator_execution"], "NOT_AUTHORIZED")
        self.assertEqual(t["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(t["absence_of_real_writer"], "NOT_PROVEN")
        self.assertEqual(t["permission_promotion"], "NEVER")
        self.assertTrue((ROOT / t["document"]).is_file())
        self.assertTrue((ROOT / t["rust_module"]).is_file())
        self.assertIn("M3_2_PREOPENED_QUERY_ONLY_RAM_READER_TOY.md", self.doc)
        self.assertIn("M3_2_PREOPENED_QUERY_ONLY_RAM_READER_TOY.md", self.index)

    def test_18_policy_requires_refetch_and_same_pr_handoff(self):
        for clause in ("Re-fetch", "HANDOFF_CURRENT.md", "HANDOFF_CURRENT.json",
                       "expected_head_sha", "autorisation"):
            self.assertIn(clause, self.policy)

if __name__ == "__main__":
    unittest.main()
