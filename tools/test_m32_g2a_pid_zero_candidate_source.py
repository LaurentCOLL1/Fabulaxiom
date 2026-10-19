"""Verify PID-0 review proposal is the PR86 script plus one reviewed change; no OS interaction."""
import unittest
from pathlib import Path
from m32_g2a_exact_block_source import DOC, CandidateStop, extract, check

PID_DOC = Path(__file__).resolve().parents[1] / "docs/qualification/M3_2_G2A_PID_ZERO_CANDIDATE_REVIEW.md"
OLD = """      $byPid = @{}
      foreach ($item in $inventory) {
        $id = [int]$item.ProcessId
        if ($id -le 0 -or $byPid.ContainsKey($id)) {
          throw 'AMBIGUOUS_PROCESS_ID'
        }
        $byPid[$id] = $item
      }"""
NEW = """      $byPid = @{}
      $idleSeen = $false
      foreach ($item in $inventory) {
        $id = [int]$item.ProcessId
        if ($id -eq 0) {
          if ($idleSeen -or $item.Name -cne 'System Idle Process') {
            throw 'AMBIGUOUS_PROCESS_ID'
          }
          $idleSeen = $true
          continue
        }
        if ($id -lt 0 -or $byPid.ContainsKey($id)) {
          throw 'AMBIGUOUS_PROCESS_ID'
        }
        $byPid[$id] = $item
      }"""

def validate_candidate(script):
    historic = extract(DOC.read_text(encoding="utf-8"))
    if historic.count(OLD) != 1 or script != historic.replace(OLD, NEW):
        raise CandidateStop("STOP: unexpected changes outside narrow PID-zero fix")
    return check(script)

class PidZeroCandidateSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = PID_DOC.read_text(encoding="utf-8")
        cls.script = extract(cls.raw)

    def deny(self, a, b):
        self.assertIn(a, self.script)
        with self.assertRaises(CandidateStop):
            validate_candidate(self.script.replace(a, b))

    def test_01_one_exact_fence_no_execution(self):
        self.assertEqual(validate_candidate(self.script)["operator_execution"], "NOT_AUTHORIZED")

    def test_02_historic_script_remains_separate(self):
        self.assertNotEqual(self.script, extract(DOC.read_text(encoding="utf-8")))

    def test_03_no_duplicate_zero_exception(self):
        self.deny("if ($idleSeen -or", "if ($false -or")

    def test_04_exact_system_idle_identity(self):
        self.deny("$item.Name -cne 'System Idle Process'", "$item.Name -cne 'msedgewebview2.exe'")

    def test_05_no_zero_ancestor_alias(self):
        self.deny("          continue", "          $byPid[$id] = $item")

    def test_06_negative_pid_still_stops(self):
        self.deny("if ($id -lt 0 -or", "if ($id -lt -1 -or")

    def test_07_missing_parent_remains_stop(self):
        self.deny("throw 'PROCESS_PARENT_MISSING'", "break")

    def test_08_sqlite_writer_absence_unproven(self):
        self.deny("PROCESS_WRITER_ABSENCE: NOT_PROVEN", "PROCESS_WRITER_ABSENCE: PROVEN")

    def test_09_no_laundering_into_gates(self):
        self.deny("G2B_G2C_G2D_G3_G4_G5_G6: NOT_AUTHORIZED", "G2B_G2C_G2D_G3_G4_G5_G6: AUTHORIZED")

    def test_10_extra_code_block_refused(self):
        with self.assertRaises(CandidateStop):
            extract(self.raw + "\n" + chr(96)*3 + "powershell\n& { }\n" + chr(96)*3)

    def test_11_other_process_logic_identical(self):
        self.deny("throw 'RELATED_OR_AMBIGUOUS_PROCESS'", "Write-Output 'IGNORE'")

if __name__ == "__main__":
    unittest.main()
