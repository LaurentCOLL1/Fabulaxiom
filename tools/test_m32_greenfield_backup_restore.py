"""Source-only Route C backup/restore boundary; not operator/runtime attestation."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUST = ROOT / "src-tauri/src/greenfield_smoke_tests.rs"
CI = ROOT / ".github/workflows/m0-ci.yml"
QUALIFICATION = ROOT / "docs/qualification/M3_2_ROUTE_C_GREENFIELD_BACKUP_RESTORE_20261026.md"


class GreenfieldBackupRestoreSourceContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rust = RUST.read_text(encoding="utf-8")
        cls.ci = CI.read_text(encoding="utf-8")
        cls.qualification = QUALIFICATION.read_text(encoding="utf-8")

    def test_01_only_test_registered_no_runtime_entrypoint(self):
        lib = (ROOT / "src-tauri/src/lib.rs").read_text(encoding="utf-8")
        self.assertIn("#[cfg(test)]\nmod greenfield_smoke_tests;", lib)
        self.assertNotIn("#[tauri::command]", self.rust)
        self.assertNotIn("tauri::AppHandle", self.rust)
        self.assertNotIn("std::process::Command", self.rust)

    def test_02_new_roots_not_operator_profile_or_historic_storage(self):
        for expected in ("std::env::temp_dir()", "fs::create_dir(&root)",
                         "fabulaxiom-ci-greenfield-", "fs::remove_dir_all"):
            self.assertIn(expected, self.rust)
        for forbidden in ("LOCALAPPDATA", "M:\\Fabulaxiom", "com.fabulaxiom.desktop",
                          "com.fabulaxiom.greenfield.v1", "migration_007", "writer_ipc"):
            self.assertNotIn(forbidden, self.rust)

    def test_03_archived_text_and_preexisting_destination_negative_matrix(self):
        for name in ("greenfield_ci_m1_m2_lifecycle_and_separate_destination_restore",
                     "greenfield_ci_corrupt_backup_cannot_activate_a_fresh_restore_root",
                     "greenfield_ci_occupied_restore_root_switches_selection_so_operator_use_is_blocked",
                     "greenfield_ci_same_profile_restore_keeps_previous_database_and_archives",
                     "greenfield_ci_same_profile_corrupt_restore_refusal_keeps_current_work",
                     "greenfield_ci_same_profile_foreign_key_invalid_backup_cannot_replace_active_work"):
            self.assertIn("fn " + name + "()", self.rust)
        for important in ("SetSceneRevisionArchivedInput", "scene_archived_revision_ids",
                          "current_schema_version", "source_bytes_before_restore",
                          "backup_bytes", "existing_bytes", "active marker"):
            self.assertIn(important, self.rust)

    def test_04_ci_runs_exact_runner_file_tests_not_wide_runtime_restore(self):
        self.assertIn("cargo test --manifest-path src-tauri/Cargo.toml --locked --lib greenfield_ci_ -- --nocapture", self.ci)
        self.assertIn('test_m32_greenfield_backup_restore.py', self.ci)
        self.assertNotIn("--target x86_64-pc-windows-msvc", self.ci)

    def test_05_no_operator_procedure_or_historic_gate_claims(self):
        for expected in ("RUNNER_ONLY", "EXISTING_PROFILE_RESTORE_BLOCKED",
                         "M3.2", "IN_PROGRESS_NOT_ACCEPTED", "G2B", "NOT_ACCEPTED",
                         "STOP_UNAVAILABLE", "OWNER_REPORTED", "NO_OPERATOR_EXECUTION",
                         "VACUUM INTO", "app_metadata", "activation"):
            self.assertIn(expected, self.qualification)
        self.assertNotIn("OWNER_REPORTED_BACKUP_RESTORE_PASS", self.qualification)

    def test_06_existing_profile_ui_requires_two_confirmations_and_reload(self):
        ui = (ROOT / "src/BackupWorkspace.tsx").read_text(encoding="utf-8")
        commands = (ROOT / "src-tauri/src/backup_commands.rs").read_text(encoding="utf-8")
        self.assertIn("Le profil de l'application restera le même", ui)
        self.assertIn("Un NOUVEAU fichier SQLite sera créé et activé dans ce profil", ui)
        self.assertIn("window.confirm(", ui)
        self.assertIn("window.prompt(", ui)
        self.assertIn('if (phrase !== "RESTAURER") return;', ui)
        self.assertIn("window.location.reload()", ui)
        self.assertIn('if input.confirmation != "RESTAURER"', commands)
        self.assertIn("backup::restore_backup(&root, &input.file_name)", commands)

    def test_07_same_profile_corrupt_backup_refusal_does_not_switch_active_file(self):
        self.assertIn("fn greenfield_ci_same_profile_corrupt_restore_refusal_keeps_current_work()", self.rust)
        for required in ("activation_dir", "markers_before", "database_names_before",
                         "healthy_bytes", "original_bytes", "selected_bytes",
                         "not a SQLite database - disposable same-profile fixture",
                         '"../not-a-backup.sqlite3"', "resolve_active_database_path"):
            self.assertIn(required, self.rust)
        self.assertIn("assert!(backup::restore_backup(&profile, &corrupt.backup.file_name).is_err())", self.rust)
        self.assertIn("assert_eq!(fs::read(&selected).unwrap(), selected_bytes)", self.rust)

    def test_08_foreign_key_invalid_backup_is_refused_after_integrity_check_ok(self):
        self.assertIn("fn greenfield_ci_same_profile_foreign_key_invalid_backup_cannot_replace_active_work()", self.rust)
        for required in ('"PRAGMA integrity_check"', '"PRAGMA foreign_key_check"',
                         '"foreign_keys", "OFF"', "'universe-missing'",
                         'assert_eq!(integrity, "ok"',
                         'assert_eq!(failure.payload().code, "integrity")',
                         'assert_eq!(names(&activation_dir), markers_before)',
                         'assert_eq!(fs::read(&selected).unwrap(), selected_bytes)',
                         'assert_eq!(fs::read(&original).unwrap(), original_bytes)'):
            self.assertIn(required, self.rust)


if __name__ == "__main__":
    unittest.main()
