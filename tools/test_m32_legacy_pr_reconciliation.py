"""Pure source-only invariants for legacy PR #35/#215 GitHub inventory.

No network or access to operator files. The historic Git SHA overlap was
observed externally and is a dated claim, not an offline live re-fetch.
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs/qualification/M3_2_LEGACY_PR35_PR215_RECONCILIATION_20261110.md"
CHECKLIST = ROOT / "docs/continuity/M3_2_COMPLETION_MASTER_CHECKLIST_20261109.md"
VFS = ROOT / "src-tauri/src/m32_sqlite_vfs_preopen_tests.rs"
LIB = ROOT / "src-tauri/src/lib.rs"
D3B = (
    "m32_d3b_child_fixture_terminate_before_sqlite_close",
    "m32_d3b_committed_wal_abandoned_mutex_refuses_unattested_reopen",
    "m32_d3b_pending_wal_vanished_mutex_still_refuses_unattested_reopen",
    "m32_d3b_busy_close_does_not_attest_restart_even_after_final_close",
)

class LegacyPRReconciliationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = REPORT.read_text(encoding="utf-8")
        cls.checklist = CHECKLIST.read_text(encoding="utf-8")
        cls.vfs = VFS.read_text(encoding="utf-8")
        cls.lib = LIB.read_text(encoding="utf-8")

    def test_01_each_path_is_accounted_for_once_per_pr_and_bucket(self):
        for pr, expected in (("pr35", (5, 11, 68)), ("pr215", (6, 17, 0))):
            seen = []
            for category, count in zip(("identical", "different", "absent"), expected):
                rx = rf"### {pr} : {category} \({count}\)\n\n(.*?)(?=\n### |\n\*Chaque ligne|\Z)"
                match = re.search(rx, self.doc, flags=re.S)
                self.assertIsNotNone(match, (pr, category))
                paths = re.findall(r"^- `([^`]+)`$", match.group(1), re.M)
                self.assertEqual(len(paths), count, (pr, category))
                seen += paths
            self.assertEqual(len(seen), sum(expected))
            self.assertEqual(len(set(seen)), len(seen))

    def test_02_test_only_d3b_refusals_still_present_and_not_runtime(self):
        self.assertIn("#[cfg(all(test, windows))]\nmod m32_sqlite_vfs_preopen_tests;", self.lib)
        self.assertIn("mod d3b_p1_disposable_crash_refusal", self.vfs)
        for fn in D3B:
            self.assertIn(f"fn {fn}()", self.vfs)
            self.assertIn(fn, self.doc)

    def test_03_pr35_chronology_remains_cfg_test_only(self):
        self.assertIn("#[cfg(test)]\nmod m32_manual_chronology;", self.lib)
        for marker in ("src-tauri/src/m32_isolated_preflight.rs",
                       "src-tauri/src/m32_sqlite_concurrency_tests.rs",
                       "68 chemins absents"):
            self.assertIn(marker, self.doc)

    def test_04_master_checklist_not_falsely_closed(self):
        self.assertIn("- [ ] **M32-007**", self.checklist)
        self.assertNotIn("- [x] **M32-007**", self.checklist)
        tasks = re.findall(r"^- \[([ x])\] \*\*(M32-\d{3})\*\*", self.checklist, re.M)
        self.assertEqual(len(tasks), 104)
        # Only five separately documented obligations closed; historical PR #35/#215 stays OPEN.
        actual_closed = {task for state, task in tasks if state == "x"}
        self.assertEqual(actual_closed, {
            "M32-001", "M32-002", "M32-037", "M32-049",
            "M32-051", "M32-095", "M32-096",
        })
        self.assertIn("AUCUNE case nouvelle clôturée", self.doc)
        for flag in ("PRODUCT_FIRST_PARALLEL_SAFETY", "IN_PROGRESS_NOT_ACCEPTED",
                     "NOT_PROVEN", "STOP_UNAVAILABLE",
                     "PENDING_EXTERNAL_ATTESTATION(21/3/2)"):
            self.assertIn(flag, self.doc)


class Pr35UnitDispositionContract(unittest.TestCase):
    """Pure review contract, never re-fetches a private tree or runs operator code."""

    @classmethod
    def setUpClass(cls):
        cls.original = REPORT.read_text(encoding="utf-8")
        cls.triage = (ROOT / "docs/qualification/M3_2_PR35_PER_PATH_DISPOSITION_20261110.md").read_text(encoding="utf-8")
        cls.master = CHECKLIST.read_text(encoding="utf-8")
        cls.entries = re.findall(
            r"^\| \`([^\`]+)\` \| \`([A-Z_]+)\` \|",
            cls.triage, re.M
        )

    def original_paths(self, group, next_group):
        section = self.original.split("### pr35 : " + group)[1]
        if next_group == "__END__":
            section = section.split("### pr215 : ")[0]
        else:
            section = section.split("### pr35 : " + next_group)[0]
        return re.findall(r"^- \`([^\`]+)\`$", section, re.M)

    def test_06_complete_84_path_matrix_without_duplicate_or_spoof(self):
        pairs = dict(self.entries)
        self.assertEqual(len(self.entries), 84)
        self.assertEqual(len(pairs), 84)
        same = self.original_paths("identical (5)", "different (11)")
        changed = self.original_paths("different (11)", "absent (68)")
        absent = self.original_paths("absent (68)", "__END__")
        self.assertEqual((len(same), len(changed), len(absent)), (5, 11, 68))
        self.assertEqual(set(pairs), set(same + changed + absent))
        for p in same:
            self.assertEqual(pairs[p], "KEEP_IDENTICAL")
        for p in changed:
            self.assertEqual(pairs[p], "REVIEW_DIVERGENCE")
        for p in absent:
            self.assertNotIn(pairs[p], ("KEEP_IDENTICAL", "REVIEW_DIVERGENCE"))

    def test_07_68_absent_paths_are_scoped_and_not_automatically_admitted(self):
        pairs = dict(self.entries)
        absent = [p for p, status in pairs.items()
                  if status not in ("KEEP_IDENTICAL", "REVIEW_DIVERGENCE")]
        self.assertEqual(len(absent), 68)
        self.assertEqual(sum(p.startswith("docs/qualification/") for p in absent), 26)
        self.assertEqual(sum(p.startswith("tools/test_") for p in absent), 20)
        self.assertEqual(sum(p.startswith("tools/") and not p.startswith("tools/test_")
                             for p in absent), 20)
        self.assertEqual(sum(p.startswith("src-tauri/") for p in absent), 2)
        self.assertEqual(pairs["src-tauri/src/m32_isolated_preflight.rs"],
                         "BLOCK_RUNTIME_IPC")
        self.assertEqual(pairs["src-tauri/src/m32_sqlite_concurrency_tests.rs"],
                         "REVIEW_CI_ONLY")

    def test_08_live_checklist_and_operator_gates_are_not_promoted(self):
        self.assertIn("- [ ] **M32-007**", self.master)
        self.assertIn("AUCUNE case nouvelle clôturée", self.triage)
        self.assertIn("PRODUCT_FIRST_PARALLEL_SAFETY", self.triage)
        for token in ("IN_PROGRESS_NOT_ACCEPTED", "NOT_PROVEN",
                      "STOP_UNAVAILABLE", "PENDING_EXTERNAL_ATTESTATION(21/3/2)",
                      "OPEN_NOT_REMEDIATED", "writer"):
            self.assertIn(token, self.triage)
        self.assertNotIn("AUTORISATION DE WRITE", self.triage)

if __name__ == "__main__":
    unittest.main()
