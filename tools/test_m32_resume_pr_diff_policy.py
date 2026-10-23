"""Source-only adversarial PR diff matrices: no actual git repos or SQLite."""
from pathlib import Path
import subprocess
import sys
import unittest

from m32_resume_pr_diff_policy import (
    HANDOFFS, LONG, SHORT, check_changed_paths,
)

SCRIPT = Path(__file__).with_name("m32_resume_pr_diff_policy.py")
BOTH = [SHORT, LONG]
FULL = [SHORT, LONG, *HANDOFFS]


class ResumePolicyNegativeMatrix(unittest.TestCase):
    def call(self, paths):
        return subprocess.run(
            [sys.executable, str(SCRIPT)],
            input="\n".join(paths) + "\n", text=True,
            capture_output=True, check=False,
        )

    def test_01_docs_only_both_prompts_pass(self):
        result = self.call(BOTH + ["docs/continuity/STATE.md"])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("M32_BOTH_RESUME_PROMPTS_EVERY_PR_PASS", result.stdout)

    def test_02_material_with_both_handoffs_pass(self):
        result = self.call(FULL + ["src/synthetic_preview.tsx"])
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_03_short_only_fails(self):
        result = self.call([SHORT, "docs/continuity/NEXT.md"])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(LONG, result.stderr)

    def test_04_long_only_fails(self):
        result = self.call([LONG, "docs/continuity/STATE.md"])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(SHORT, result.stderr)

    def test_05_both_missing_docs_only_fails(self):
        result = self.call(["docs/continuity/README.md"])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(SHORT, result.stderr)
        self.assertIn(LONG, result.stderr)

    def test_06_empty_list_fails_closed(self):
        result = self.call([])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("STOP missing required resume prompt", result.stderr)

    def test_07_material_missing_both_handoffs_fails(self):
        result = self.call(BOTH + ["src-tauri/src/toy.rs"])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(HANDOFFS[0], result.stderr)
        self.assertIn(HANDOFFS[1], result.stderr)

    def test_08_material_missing_one_handoff_fails(self):
        result = self.call(BOTH + [HANDOFFS[0], "tools/synthetic_guard.py"])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(HANDOFFS[1], result.stderr)

    def test_09_workflow_change_is_material(self):
        result = self.call(BOTH + [".github/workflows/m0-ci.yml"])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(HANDOFFS[0], result.stderr)

    def test_10_qualification_doc_change_is_material(self):
        result = self.call(BOTH + ["docs/qualification/synthetic.md"])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(HANDOFFS[1], result.stderr)

    def test_11_missing_exact_short_path_never_passes(self):
        result = self.call([SHORT + ".bak", LONG])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(SHORT, result.stderr)

    def test_12_duplicate_or_extra_files_do_not_bypass(self):
        ok, reasons = check_changed_paths([LONG, LONG, "docs/continuity/STATE.md"])
        self.assertFalse(ok)
        self.assertTrue(any(SHORT in line for line in reasons))


if __name__ == "__main__":
    unittest.main()
