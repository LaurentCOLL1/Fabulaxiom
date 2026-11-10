"""No-I/O M3.2 checklist contracts: no operator data, SQLite, network or writer."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "docs/continuity/M3_2_COMPLETION_MASTER_CHECKLIST_20261109.md"
SHORT = ROOT / "docs/continuity/RESUME_PROMPT_SHORT.md"
LONG = ROOT / "docs/continuity/RESUME_PROMPT.md"
TASK = re.compile(r"^- \[([ x])\] \*\*(M32-\d{3})\*\*", re.M)


class M32MasterChecklistContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.content = MASTER.read_text(encoding="utf-8")
        cls.tasks = list(TASK.finditer(cls.content))

    def test_01_104_distinct_tasks_in_order(self):
        self.assertEqual([m.group(2) for m in self.tasks],
                         [f"M32-{n:03d}" for n in range(1, 105)])

    def test_02_visible_numbers_match_exact_checkboxes(self):
        closed = sum(x.group(1) == "x" for x in self.tasks)
        opened = sum(x.group(1) == " " for x in self.tasks)
        self.assertEqual(closed + opened, 104)
        self.assertRegex(self.content, rf"104 tâches identifiées : {closed} clôturées")
        self.assertIn(f"{opened} encore ouvertes", self.content)

    def test_03_checked_tasks_have_dated_scoped_qualification(self):
        for i, m in enumerate(self.tasks):
            if m.group(1) != "x":
                continue
            end = self.tasks[i + 1].start() if i + 1 < len(self.tasks) else len(self.content)
            entry = self.content[m.start():end]
            with self.subTest(task=m.group(2)):
                self.assertIn("**Preuve de clôture :**", entry)
                self.assertIn("**Acquis", entry)
                self.assertRegex(entry, r"2026-11-\d{2}")
                self.assertRegex(entry, r"[0-9a-f]{40}")
                self.assertRegex(entry, r"#[0-9]{7,}")

    def test_04_live_safety_and_final_admission_still_unchecked(self):
        for number in (9, 11, 16, 20, 31, 39, 42, 97, 103):
            self.assertIn(f"- [ ] **M32-{number:03d}**", self.content)
        for marker in ("IN_PROGRESS_NOT_ACCEPTED", "NOT_PROVEN",
                       "STOP_UNAVAILABLE", "PENDING_EXTERNAL_ATTESTATION(21/3/2)",
                       "OPEN_NOT_REMEDIATED", "PRODUCT_FIRST_PARALLEL_SAFETY"):
            self.assertIn(marker, self.content)

    def test_05_both_resumes_link_master_checklist(self):
        for doc in (SHORT, LONG):
            with self.subTest(file=doc.name):
                content = doc.read_text(encoding="utf-8")
                self.assertIn(MASTER.name, content)
                self.assertIn("main=", content)
                self.assertIn("expected_head_sha", content)
        self.assertLess(len(SHORT.read_bytes()), 3600)

    def test_06_next_validation_requires_checklist_update(self):
        for marker in ("Chaque PR matérielle", "date", "SHA",
                       "compteurs", "preuve", "104"):
            self.assertIn(marker, self.content)
        self.assertIn("M32-002", self.content)
        self.assertIn("#42751838279", self.content)
        self.assertIn("#42754285833", self.content)


if __name__ == "__main__":
    unittest.main()
