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
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 86)
        self.assertEqual(self.data["g2a"]["corrected_execution"], "NOT_ASSESSED")

    def test_04_pr35_and_external_issues_still_open(self):
        self.assertEqual(self.data["pr35"], "OPEN_DRAFT")
        self.assertEqual(self.data["issues"], {"36": "OPEN", "38": "OPEN"})

    def test_05_no_implicit_windows_authorization(self):
        self.assertEqual(self.data["g2a"]["exact_corrected_script_owner_approval"],
                         "REQUIRES_EXACT_BYTES_REVIEW")
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
        self.assertIn("NOT_ASSESSED", self.doc)

    def test_10_policy_requires_refetch_and_same_pr_handoff(self):
        for clause in ("Re-fetch", "HANDOFF_CURRENT.md", "HANDOFF_CURRENT.json",
                       "expected_head_sha", "autorisation"):
            self.assertIn(clause, self.policy)

if __name__ == "__main__":
    unittest.main()
