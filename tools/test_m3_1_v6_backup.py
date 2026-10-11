"""Synthetic, disposable tests for the M3.1 opt-in v6 backup procedure."""
from pathlib import Path
import shutil
import sqlite3
import tempfile
import unittest

import m3_1_v6_audit as audit
import m3_1_v6_backup as backup
import test_m3_1_v6_audit as fixtures


class BackupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fabulaxiom-m31-backup-fixture-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "com.fabulaxiom.desktop"
        (self.root / "database").mkdir(parents=True)
        (self.root / "operator-qualification").mkdir()
        self.file = self.root / "database" / "fabulaxiom.sqlite3"
        fixtures.ReadOnlyAuditTests().fixture(self.file)
        # The backup tool deliberately requires an M1.5 restored-active file,
        # not the ordinary default DB.
        self.name = (
            "fabulaxiom-restored-" + "1" * 32
            + "-0000000001-0000000001.sqlite3"
        )
        restored = self.root / "database" / self.name
        self.file.replace(restored)
        self.file = restored
        activation = self.root / "database" / "activations"
        activation.mkdir()
        (activation / ("activation-" + "2" * 32 +
                       "-0000000001-0000000001.active")).write_text(
            self.name, encoding="utf-8"
        )
        self.report = audit.audit(self.root)
        self.sha = self.report["closed_file_sha256"]
        self.logical = self.report["combined_logical_sha256"]

    def run_stage(self, create):
        return backup.perform(
            self.root, self.name, self.sha, self.logical, create=create
        )

    def test_dry_run_creates_no_files(self):
        old_sha = audit._file_sha256(self.file)
        response = self.run_stage(create=False)
        self.assertEqual(response["status"], "READY")
        self.assertFalse((self.root / "operator-qualification" / "m3_1").exists())
        self.assertEqual(audit._file_sha256(self.file), old_sha)

    def test_backup_restore_and_manifest_preserve_exact_source(self):
        result = self.run_stage(create=True)
        self.assertEqual(result["status"], "PASS")
        self.assertFalse(result["v7_migration_executed"])
        self.assertEqual(result["legacy_tables"], 14)
        folder = self.root / result["relative_custody_dir"]
        dbfile = folder / "fabulaxiom-pre-m3-1-v6.sqlite3"
        restore = folder / "isolated-restore-rehearsal-v6.sqlite3"
        self.assertTrue(dbfile.is_file())
        self.assertTrue(restore.is_file())
        self.assertTrue((folder / "manifest.json").is_file())
        self.assertEqual(backup._validate_copy(dbfile, self.report)["sha256"],
                         result["backup_sha256"])
        self.assertEqual(backup._validate_copy(restore, self.report)["sha256"],
                         result["restore_sha256"])
        self.assertEqual(audit._file_sha256(self.file), self.sha)
        self.assertEqual(audit.audit(self.root), self.report)

    def test_second_backup_is_unique_and_does_not_overwrite_first(self):
        one = self.run_stage(create=True)
        first_dir = self.root / one["relative_custody_dir"]
        first_manifest = audit._file_sha256(first_dir / "manifest.json")
        two = self.run_stage(create=True)
        self.assertNotEqual(one["relative_custody_dir"], two["relative_custody_dir"])
        self.assertEqual(audit._file_sha256(first_dir / "manifest.json"), first_manifest)

    def test_source_sha_mismatch_stops_before_creating_destination(self):
        with self.assertRaisesRegex(backup.BackupStop, "source_sha256_mismatch"):
            backup.perform(self.root,self.name,"0"*64,self.logical,create=True)
        self.assertFalse((self.root / "operator-qualification" / "m3_1").exists())

    def test_missing_marker_identity_stops_before_creating_destination(self):
        with self.assertRaisesRegex(backup.BackupStop, "active_m15_file_mismatch"):
            backup.perform(self.root, self.name.replace("1"*32, "3"*32),
                           self.sha, self.logical, create=True)
        self.assertFalse((self.root / "operator-qualification" / "m3_1").exists())

    def test_wal_header_stops_before_creating_destination(self):
        with sqlite3.connect(self.file) as db:
            self.assertEqual(db.execute("PRAGMA journal_mode=WAL").fetchone()[0], "wal")
        with self.assertRaises(audit.AuditError):
            self.run_stage(create=True)
        self.assertFalse((self.root / "operator-qualification" / "m3_1").exists())

    def test_existing_stage_does_not_get_erased(self):
        stage = self.root / "operator-qualification" / "m3_1"
        stage.mkdir()
        protected = stage / "existing-operator-report.txt"
        protected.write_text("Keep", encoding="utf-8")
        result = self.run_stage(create=True)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(protected.read_text(encoding="utf-8"), "Keep")

    def test_wrong_root_name_refused_without_write(self):
        renamed = self.root.parent / "other-app"
        shutil.copytree(self.root, renamed)
        with self.assertRaisesRegex(backup.BackupStop,"production_app_root_name_mismatch"):
            backup.perform(renamed,self.name,self.sha,self.logical,create=True)
        self.assertFalse((renamed / "operator-qualification" / "m3_1").exists())


if __name__ == "__main__":
    unittest.main()
