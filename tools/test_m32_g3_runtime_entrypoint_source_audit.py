"""Adversarial source-only checks for currently unsafe/migrating Rust entrypoints."""
import unittest
from pathlib import Path
from m32_g3_runtime_entrypoint_source_audit import (
    ROOT, PUBLIC_SOURCES, SourceReviewRequired,
    audit_sources, read_repository_source, unique_slice,
)

def sources():
    return {name: (ROOT/path).read_text(encoding="utf-8") for name,path in PUBLIC_SOURCES.items()}

class RuntimeEntrypointAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.src = sources()

    def veto(self, key, old, new, anchor=""):
        text = self.src[key]
        start = text.find(anchor) if anchor else 0
        self.assertGreaterEqual(start, 0)
        at = text.find(old, start)
        self.assertGreaterEqual(at, 0, "mutation target not present")
        modified = dict(self.src)
        modified[key] = text[:at] + new + text[at+len(old):]
        with self.assertRaises(SourceReviewRequired):
            audit_sources(**modified)

    def test_01_real_public_rust_source_matches_and_still_g3_stop(self):
        x = read_repository_source()
        self.assertFalse(x["real_g3_authorized"])
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(x["writer_absence"], "NOT_PROVEN")

    def test_02_source_matches_are_not_runtime_authority(self):
        self.assertEqual(audit_sources(**self.src)["operator_command"], "NOT_AUTHORIZED")

    def test_03_create_dir_requires_reaudit(self):
        self.veto("database", "fs::create_dir_all(parent)?;", "// refactored")

    def test_04_default_db_open_requires_reaudit(self):
        self.veto("database", "Connection::open(path)?;", "Connection::open_with_flags(path, flags)?;")

    def test_05_migration_removal_or_refactor_requires_reaudit(self):
        self.veto("database", "run_migrations(&mut connection)?;", "safe_nonmigrating_open(&mut connection)?;")

    def test_06_configuration_rewrite_requires_reaudit(self):
        self.veto("database", "configure_connection(&connection)?;", "other_configuration(&connection)?;")

    def test_07_status_open_path_requires_reaudit(self):
        self.veto("lib", "database::open_database(&path)", "new_safe_reader(&path)")

    def test_08_backup_open_path_requires_reaudit(self):
        self.veto("backup", "database::open_database(&source_path)", "new_safe_reader(&source_path)")

    def test_09_backup_reservation_requires_reaudit(self):
        self.veto("backup", "reserve_unique_file(&backup_directory(root), BACKUP_PREFIX)?;", "new_reservation()?;")

    def test_10_backup_vacuum_invocation_requires_reaudit(self):
        self.veto("backup", "vacuum_copy(&connection, &destination);", "online_backup(&connection, &destination);")

    def test_11_vacuum_into_requires_reaudit(self):
        self.veto("backup", 'connection.execute("VACUUM INTO ?1"', 'connection.execute("OTHER INTO ?1"')

    def test_12_drop_reserved_handle_requires_reaudit(self):
        self.veto("backup", "drop(file);", "persist_handle_until_sqlite_opens(file);",
                  anchor="fn reserve_unique_file(directory: &Path")

    def test_13_readonly_connection_rework_requires_reaudit(self):
        self.veto("backup", "Connection::open_with_flags(path, OpenFlags::SQLITE_OPEN_READ_ONLY)?;",
                  "Connection::open(path)?;")

    def test_14_backup_validation_rewrite_requires_reaudit(self):
        self.veto("backup", "validate_connection(&conn)", "validate_other_way(&conn)")

    def test_15_ambiguous_signatures_stop(self):
        with self.assertRaises(SourceReviewRequired):
            unique_slice("BEGIN BEGIN END", "BEGIN", "END")

    def test_16_other_root_denied(self):
        with self.assertRaises(SourceReviewRequired):
            read_repository_source(ROOT.parent)

    def test_17_bad_input_denied(self):
        with self.assertRaises(SourceReviewRequired):
            audit_sources(None, self.src["backup"], self.src["lib"])

    def test_18_all_expected_source_patterns_never_promote_g3(self):
        x = audit_sources(**self.src)
        self.assertEqual(x["review"],
                         "EXACT_KNOWN_SOURCE_PATTERNS_MATCH_REQUIRES_RUNTIME_AND_SOURCE_REVIEW")
        self.assertFalse(x["real_g3_authorized"])

if __name__ == "__main__":
    unittest.main()
