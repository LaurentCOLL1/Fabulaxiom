"""Adversarial test-only mutation suite: no PowerShell invocation."""
import unittest
from m32_g2a_exact_block_source import CandidateStop, DOC, extract, check, check_repository

class CandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = DOC.read_text(encoding="utf-8")
        cls.script = extract(cls.source)

    def veto(self, old, new):
        with self.assertRaises(CandidateStop):
            check(self.script.replace(old,new))

    def test_01_source_passes_without_execution(self):
        self.assertEqual(check_repository()["operator_execution"],"NOT_AUTHORIZED")

    def test_02_second_code_block_refused(self):
        with self.assertRaises(CandidateStop):
            extract(self.source + "\n" + chr(96)*3 + "powershell\n" +
                    "& { Write-Output 'bad' }\n" + chr(96)*3)

    def test_03_stop_error_policy_required(self):
        self.veto("$ErrorActionPreference = 'Stop'", "$ErrorActionPreference = 'Continue'")

    def test_04_system_executable_directory_required(self):
        self.veto("[Environment]::SystemDirectory", "$env:PATH")

    def test_05_no_whoami_all_details(self):
        self.veto("/groups /fo csv /nh", "/all /fo csv /nh")

    def test_06_medium_sid_only(self):
        self.veto("'S-1-16-8192'", "'S-1-16-12288'")

    def test_07_no_ambiguous_webview_omission(self):
        self.veto("'Fabulaxiom','ollama','msedgewebview2'", "'Fabulaxiom','ollama'")

    def test_08_get_process_errors_must_stop(self):
        self.veto("Get-Process -ErrorAction Stop", "Get-Process -ErrorAction SilentlyContinue")

    def test_09_absence_of_writer_not_proven(self):
        self.veto("PROCESS_WRITER_ABSENCE: NOT_PROVEN", "PROCESS_WRITER_ABSENCE: PROVEN")

    def test_10_github_network_not_done(self):
        self.veto("PUBLIC_GITHUB_CHECK: NOT_ASSESSED_BY_THIS_BLOCK", "PUBLIC_GITHUB_CHECK: PASS")

    def test_11_downstream_gates_not_authorized(self):
        self.veto("G2B_G2C_G2D_G3_G6: NOT_AUTHORIZED", "G2B_G2C_G2D_G3_G6: AUTHORIZED")

    def test_12_catch_must_exist(self):
        self.veto("catch {", "finally {")

    def test_13_related_process_must_stop(self):
        self.veto("throw 'RELATED_OR_AMBIGUOUS_PROCESS'", "Write-Output 'PASS'")

    def test_14_no_ps_process_spawn(self):
        with self.assertRaises(CandidateStop):
            check(self.script.replace("$stage = 'CLOCK'", "Start-Process cmd.exe\n $stage = 'CLOCK'"))

    def test_15_no_sqlite_read(self):
        with self.assertRaises(CandidateStop):
            check(self.script.replace("$stage = 'CLOCK'", "sqlite3 database.sqlite\n $stage = 'CLOCK'"))

    def test_16_no_git_mutation(self):
        with self.assertRaises(CandidateStop):
            check(self.script.replace("$stage = 'CLOCK'", "git fetch\n $stage = 'CLOCK'"))

    def test_17_no_acl_read(self):
        with self.assertRaises(CandidateStop):
            check(self.script.replace("$stage = 'CLOCK'", "Get-Acl example\n $stage = 'CLOCK'"))

    def test_18_no_output_to_file(self):
        with self.assertRaises(CandidateStop):
            check(self.script.replace("$stage = 'CLOCK'", "Write-Output bad > log.txt\n $stage = 'CLOCK'"))

    def test_19_no_script_prompt(self):
        with self.assertRaises(CandidateStop):
            check(self.script.replace("$stage = 'CLOCK'", "Read-Host fake\n $stage = 'CLOCK'"))

    def test_20_stop_output_required(self):
        self.veto("Write-Output 'G2A_LOCAL_METADATA: STOP'", "Write-Output 'CONTINUE'")

if __name__ == "__main__":
    unittest.main()
