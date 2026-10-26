"""Route C source-only guard for the read-only Windows launch preflight.

Never starts PowerShell, Tauri or SQLite. All adversarial edits remain strings.
The native Windows behavior is checked separately on disposable CI fixture roots.
"""
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "greenfield_first_launch_preflight.ps1"
RUNBOOK = ROOT / "docs" / "qualification" / "M3_2_ROUTE_C_WINDOWS_FIRST_LAUNCH_RUNBOOK_20261026.md"


def audit(script: str, runbook: str) -> None:
    required_script = (
        "[ValidatePattern('^[a-f0-9]{40}$')]",
        "com.fabulaxiom.desktop",
        "com.fabulaxiom.greenfield.v1",
        "appDirectoriesOverride",
        "GIT_OPTIONAL_LOCKS",
        "rev-parse HEAD",
        "status --porcelain",
        "LocalApplicationData",
        "LOCALAPPDATA",
        "WindowsBuiltInRole]::Administrator",
        "GITHUB_ACTIONS",
        "RUNNER_TEMP",
        "fabulaxiom-ci-greenfield-preflight-",
        "[IO.FileAttributes]::ReparsePoint",
        "Get-Item -LiteralPath $cursor",
        "Get-ChildItem -LiteralPath $root -Force",
        "GREENFIELD_ROOT_ENTRY: ABSENT_AT_SAMPLE_TIME",
        "GREENFIELD_PREFLIGHT_STOP:",
        "GREENFIELD_PREFLIGHT_METADATA_ONLY_CANDIDATE:",
        "no atomic reservation",
    )
    for token in required_script:
        if token not in script:
            raise ValueError("Missing fail-closed preflight element: " + token)
    for forbidden in (
        "New-Item", "Set-Content", "Add-Content", "Out-File",
        "Remove-Item", "Move-Item", "Rename-Item", "Start-Process",
        "Invoke-Expression", "Invoke-RestMethod", "Invoke-WebRequest",
        "Set-Acl", "Get-Acl", "Get-ChildItem -Recurse",
        "npm ci", "tauri dev", "sqlite3", "migrate",
    ):
        if re.search(r"(?<![A-Za-z0-9])" + re.escape(forbidden), script, re.I):
            raise ValueError("Preflight contains forbidden mutating or broad operation: " + forbidden)
    if "Get-ChildItem -LiteralPath $root -Force -Recurse" in script:
        raise ValueError("Cannot recurse operator directories")
    for token in (
        "GREENFIELD_PREFLIGHT_METADATA_ONLY_CANDIDATE",
        "-ExpectedHead",
        "com.fabulaxiom.greenfield.v1",
        "npm ci",
        "tauri.cmd dev --config src-tauri/tauri.greenfield.conf.json",
        "réexécuter",
        "nouvelle",
        "AUCUNE restauration",
        "STOP",
        "aucun original",
        "M3.2",
    ):
        if token not in runbook:
            raise ValueError("Operator runbook boundary absent: " + token)


class GreenfieldFirstLaunchPreflightContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script = SCRIPT.read_text(encoding="utf-8")
        cls.runbook = RUNBOOK.read_text(encoding="utf-8")

    def deny(self, script=None, runbook=None):
        with self.assertRaises(ValueError):
            audit(
                self.script if script is None else script,
                self.runbook if runbook is None else runbook,
            )

    def test_01_checked_in_source_only_contract(self):
        audit(self.script, self.runbook)

    def test_02_reject_loss_of_fixed_greenfield_identity(self):
        self.deny(script=self.script.replace("com.fabulaxiom.greenfield.v1", "com.fabulaxiom.desktop"))

    def test_03_reject_loss_of_exact_head_binding(self):
        self.deny(script=self.script.replace("rev-parse HEAD", "rev-parse main"))

    def test_04_reject_loss_of_ancestor_reparse_guard(self):
        self.deny(script=self.script.replace("[IO.FileAttributes]::ReparsePoint", "0"))

    def test_05_reject_loss_of_leaf_absence_sample(self):
        self.deny(script=self.script.replace("Get-ChildItem -LiteralPath $root -Force", "Get-ChildItem -Path ."))

    def test_06_reject_loss_of_ci_fixture_runner_binding(self):
        self.deny(script=self.script.replace("GITHUB_ACTIONS", "GITHUB_WORKSPACE"))

    def test_07_reject_app_execution_inside_metadata_preflight(self):
        self.deny(script=self.script + "\nnpm ci\n")

    def test_08_reject_recursive_historical_enumeration(self):
        self.deny(script=self.script + "\nGet-ChildItem -Recurse\n")

    def test_09_reject_write_or_acl_mutations(self):
        for forbidden in ("New-Item", "Remove-Item", "Set-Acl", "Get-Acl"):
            with self.subTest(forbidden=forbidden):
                self.deny(script=self.script + "\n" + forbidden + " -LiteralPath $root\n")

    def test_10_reject_runbook_that_couples_restore_to_first_launch(self):
        self.deny(runbook=self.runbook.replace("AUCUNE restauration", "Restauration immédiate"))


if __name__ == "__main__":
    unittest.main()
