"""Source identity shortcut refusals and public Rust source drift audit.

No operator files, SQLite opens, Windows filesystem access, or app execution.
"""
from dataclasses import FrozenInstanceError, asdict, fields
from pathlib import Path
import unittest

from m3_2_g3_source_identity_boundaries import (
    Disposition, SourceCandidate, all_screened, screen,
)

ROOT = Path(__file__).resolve().parents[1]
RUST = ROOT / "src-tauri" / "src"
PRODUCTION_FILES = (
    "lib.rs",
    "database.rs",
    "backup.rs",
    "backup_commands.rs",
    "hierarchy_commands.rs",
    "entity_commands.rs",
    "fact_commands.rs",
    "review_commands.rs",
    "revision_commands.rs",
)


class SourceIdentityModelTests(unittest.TestCase):
    def test_every_known_candidate_has_explicit_non_authorizing_disposition(self):
        reports = all_screened()
        self.assertEqual(len(reports), len(SourceCandidate))
        self.assertEqual({r.candidate for r in reports}, set(SourceCandidate))
        for report in reports:
            with self.subTest(candidate=report.candidate):
                self.assertFalse(report.real_g3_authorized)
                self.assertIn(report.disposition, Disposition)
                self.assertTrue(report.missing_boundary)
                self.assertTrue(report.rationale)

    def test_path_and_migration_reopens_are_unconditional_vetoes(self):
        for candidate in (
            SourceCandidate.CURRENT_MIGRATING_APP_OPEN,
            SourceCandidate.SQLITE_PATH_READONLY_REOPEN,
            SourceCandidate.SQLITE_IMMUTABLE_URI,
        ):
            self.assertEqual(screen(candidate).disposition, Disposition.VETO_UNSAFE_SHORTCUT)

    def test_filename_cannot_be_file_identity(self):
        report = screen(SourceCandidate.SQLITE_DB_FILENAME)
        self.assertEqual(report.disposition, Disposition.NOT_SOURCE_PROVENANCE)
        self.assertIn("sqlite_connection_to_win32_object_binding", report.missing_boundary)

    def test_internal_sqlite_file_pointer_not_windows_handle(self):
        report = screen(SourceCandidate.SQLITE_FILE_POINTER)
        self.assertIn("vfs_specific_owned_handle_proof", report.missing_boundary)

    def test_raw_rusqlite_pointer_not_authenticated(self):
        self.assertEqual(
            screen(SourceCandidate.RUSQLITE_RAW_HANDLE).disposition,
            Disposition.VETO_UNSAFE_SHORTCUT,
        )

    def test_win32_id_must_bind_to_actual_sqlite_owner(self):
        report = screen(SourceCandidate.WIN32_FILE_ID_ONLY)
        self.assertIn("sqlite_connection_to_win32_object_binding", report.missing_boundary)

    def test_ram_actor_is_not_production_provenance(self):
        self.assertEqual(
            screen(SourceCandidate.RAM_ONLY_OWNER_ACTOR).disposition,
            Disposition.NOT_SOURCE_PROVENANCE,
        )

    def test_future_vfs_does_not_silently_authorize(self):
        self.assertEqual(
            screen(SourceCandidate.CUSTOM_SQLITE_VFS_PROPOSAL).disposition,
            Disposition.ARCHITECTURE_REVIEW_ONLY,
        )

    def test_future_owner_is_only_design_review(self):
        report = screen(SourceCandidate.AUTHENTICATED_PREOPENED_OWNER_PROPOSAL)
        self.assertEqual(report.disposition, Disposition.ARCHITECTURE_REVIEW_ONLY)
        self.assertFalse(report.real_g3_authorized)

    def test_authorization_flag_cannot_be_requested_or_mutated(self):
        result = screen(SourceCandidate.RAM_ONLY_OWNER_ACTOR)
        with self.assertRaises(TypeError):
            type(result)(
                result.candidate, result.disposition, result.rationale,
                result.missing_boundary, real_g3_authorized=True,
            )
        with self.assertRaises(FrozenInstanceError):
            result.real_g3_authorized = True

    def test_untyped_candidates_fail_closed(self):
        for value in ("ram_only_owner_actor", None, 0, True):
            with self.subTest(value=value), self.assertRaises(TypeError):
                screen(value)

    def test_no_authorization_or_runtime_inputs(self):
        names = {f.name for f in fields(type(screen(SourceCandidate.RAM_ONLY_OWNER_ACTOR)))}
        self.assertNotIn("operator_path", names)
        self.assertNotIn("credential", names)
        self.assertFalse(any(asdict(r)["real_g3_authorized"] for r in all_screened()))


class ProductionSourceDriftTests(unittest.TestCase):
    def read(self, name):
        return (RUST / name).read_text(encoding="utf-8")

    def test_no_undiscussed_raw_sqlite_or_vfs_source_adapters(self):
        dangerous_tokens = (
            "SQLITE_FCNTL_FILE_POINTER", "SQLITE_FCNTL_JOURNAL_POINTER",
            "sqlite3_file_control(", "sqlite3_db_filename(",
            "sqlite3_vfs_register(", "sqlite3_open_v2(",
            "from_handle_owned(", "from_handle(",
        )
        for name in PRODUCTION_FILES:
            with self.subTest(name=name):
                text = self.read(name)
                for token in dangerous_tokens:
                    self.assertNotIn(token, text, msg=f"{name}: new {token} needs a distinct review")

    def test_no_immutable_shortcut_in_production_entries(self):
        for name in PRODUCTION_FILES:
            with self.subTest(name=name):
                self.assertNotIn("immutable=1", self.read(name))

    def test_app_database_open_still_migrates(self):
        source = self.read("database.rs")
        function = source.split("pub fn open_database(", 1)[1].split("\npub fn ", 1)[0]
        self.assertIn("Connection::open(path)?", function)
        self.assertIn("run_migrations(&mut connection)?", function)

    def test_no_new_g3_ipc_or_managed_source(self):
        lib = self.read("lib.rs")
        self.assertNotIn(".manage(", lib)
        self.assertNotIn("m32_g3_capture", lib)
        self.assertNotIn("m32_g3_source_acquire", lib)

    def test_toy_owner_features_remain_test_only(self):
        lib = self.read("lib.rs")
        cargo = (ROOT / "src-tauri" / "Cargo.toml").read_text(encoding="utf-8")
        self.assertIn("default = []", cargo)
        self.assertIn(
            '#[cfg(all(feature = "m32-g3-owned-ram-toy", not(test)))]', lib,
        )
        self.assertIn("compile_error!", lib)
        self.assertIn(
            '#[cfg(all(test, feature = "m32-g3-owned-ram-toy"))]\nmod m32_owner_handoff_actor_toy;',
            lib,
        )


if __name__ == "__main__":
    unittest.main()
