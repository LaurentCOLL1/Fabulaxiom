"""M3.1 forced-rollback fourth-copy fixtures; exclusively disposable SQLite."""
from contextlib import closing
from pathlib import Path
import sqlite3
import unittest

import m3_1_v6_audit as audit
import m3_1_v6_backup as backup
import m3_1_v7_rollback_rehearsal as rollback
import test_m3_1_v7_copy_rehearsal as fixtures


class RollbackFixtureTests(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.CopyOnlyRehearsalFixture()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.root = self.fixture.root

    def run_case(self, create=False, **updates):
        args = dict(
            root=self.root,
            relative=self.fixture.custody_rel,
            expected_active=self.fixture.fixture.name,
            expected_source=self.fixture.fixture.sha,
            expected_logical=self.fixture.fixture.logical,
            expected_backup=self.fixture.record["backup_sha256"],
            expected_manifest=self.fixture.record["manifest_sha256"],
            candidate_sql_file=self.fixture.sql,
            expected_sql=self.fixture.sql_sha,
            create=create,
        )
        args.update(updates)
        return rollback.perform(**args)

    def test_read_only_dry_run_writes_nothing(self):
        stage = self.root / "operator-qualification" / "m3_1"
        original = set(stage.iterdir())
        report = self.run_case()
        self.assertEqual(report["status"], "READY")
        self.assertEqual(report["mode"], "fourth_copy_rollback_dry_run")
        self.assertFalse(report["forced_failure_executed"])
        self.assertEqual(set(stage.iterdir()), original)

    def test_forced_rollback_retains_full_v6_and_original_custody(self):
        old_source = audit._file_sha256(self.fixture.fixture.file)
        v6 = self.root/self.fixture.custody_rel/"fabulaxiom-pre-m3-1-v6.sqlite3"
        old_backup = audit._file_sha256(v6)
        result = self.run_case(create=True)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["rolled_back_schema_version"], 6)
        self.assertEqual(result["legacy_tables_preserved"], 14)
        self.assertTrue(result["intentional_error"].startswith("SQLITE_CONSTRAINT"))
        result_dir = self.root/result["relative_rehearsal_dir"]
        fourth = result_dir/"failed-v7-rolled-back-v6.sqlite3"
        self.assertEqual(audit._file_sha256(fourth), old_backup)
        self.assertTrue((result_dir/"rollback-manifest.json").is_file())
        backup._validate_copy(fourth,self.fixture.fixture.report)
        self.assertEqual(audit._file_sha256(self.fixture.fixture.file),old_source)
        self.assertEqual(audit._file_sha256(v6),old_backup)

    def test_refuse_changed_backup_before_new_folder(self):
        stage = self.root/"operator-qualification"/"m3_1"
        old = set(stage.iterdir())
        with self.assertRaises(Exception):
            self.run_case(create=True,expected_backup="0"*64)
        self.assertEqual(set(stage.iterdir()),old)

    def test_refuse_changed_sql_hash_before_new_folder(self):
        stage=self.root/"operator-qualification"/"m3_1"
        old=set(stage.iterdir())
        with self.assertRaises(Exception):
            self.run_case(create=True,expected_sql="0"*64)
        self.assertEqual(set(stage.iterdir()),old)

    def test_invalid_candidate_ddl_fails_and_retains_new_copy(self):
        original = audit._file_sha256(self.fixture.fixture.file)
        stage=self.root/"operator-qualification"/"m3_1"
        before=set(stage.iterdir())
        self.fixture.sql.write_text(
            "CREATE TABLE fictional_calendars(id TEXT PRIMARY KEY) STRICT;\n"
            "CREATE TABLE fictional_calendars(id TEXT PRIMARY KEY) STRICT;",
            encoding="utf-8"
        )
        self.fixture.sql_sha=audit._file_sha256(self.fixture.sql)
        with self.assertRaises(sqlite3.Error):
            self.run_case(create=True)
        new=list(set(stage.iterdir())-before)
        self.assertEqual(len(new),1)
        self.assertTrue((new[0]/"failed-v7-rolled-back-v6.sqlite3").exists())
        self.assertEqual(audit._file_sha256(self.fixture.fixture.file),original)

    def test_unexpected_active_file_is_refused(self):
        stage=self.root/"operator-qualification"/"m3_1"
        old=set(stage.iterdir())
        with self.assertRaises(backup.BackupStop):
            self.run_case(create=True,expected_active=(
                self.fixture.fixture.name.replace("1"*32,"3"*32)
            ))
        self.assertEqual(set(stage.iterdir()),old)


if __name__ == "__main__":
    unittest.main()
