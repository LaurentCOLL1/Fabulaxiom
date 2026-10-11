"""Actual governed v7 SQL, copied synthetic SQLite only; no operator paths."""
from pathlib import Path
import sqlite3
import unittest

import m3_1_v6_audit as audit
import m3_1_v7_final_readonly as final
import test_m3_1_v7_copy_rehearsal as fixtures


class RealV7FinalReadOnlyTests(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.CopyOnlyRehearsalFixture()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.root = self.fixture.root
        self.sql = Path(__file__).resolve().parents[1] / (
            "src-tauri/sql/m3_1_world_time_v7_candidate.sql"
        )
        self.assertTrue(self.sql.is_file())
        self.fixture.sql = self.sql
        self.fixture.sql_sha = audit._file_sha256(self.sql)
        self.result = self.fixture.go(True)
        self.assertEqual(self.result["status"], "PASS")

    def run_audit(self, **overrides):
        args = dict(
            root=self.root,
            custody=self.fixture.custody_rel,
            third=self.result["relative_rehearsal_dir"],
            active=self.fixture.fixture.name,
            source_sha=self.fixture.fixture.sha,
            logical_sha=self.fixture.fixture.logical,
            backup_sha=self.fixture.record["backup_sha256"],
            custody_manifest_sha=self.fixture.record["manifest_sha256"],
            third_sha=self.result["candidate_sha256"],
            third_manifest_sha=self.result["manifest_sha256"],
            sql_file=self.sql,
            sql_sha=self.fixture.sql_sha,
        )
        args.update(overrides)
        return final.perform(**args)

    def test_real_candidate_constraints_ram_only(self):
        old_source = audit._file_sha256(self.fixture.fixture.file)
        old_third = self.result["candidate_sha256"]
        response = self.run_audit()
        self.assertEqual(response["status"], "PASS")
        self.assertEqual(response["constraint_scenarios_passed"], 10)
        self.assertEqual(audit._file_sha256(self.fixture.fixture.file), old_source)
        third = self.root/self.result["relative_rehearsal_dir"]/"candidate-v7.sqlite3"
        self.assertEqual(audit._file_sha256(third), old_third)

    def test_unexpected_third_sha_rejected(self):
        with self.assertRaises(final.FinalAuditStop):
            self.run_audit(third_sha="0"*64)

    def test_wrong_sql_hash_rejected(self):
        with self.assertRaises(final.FinalAuditStop):
            self.run_audit(sql_sha="0"*64)

    def test_mismatched_third_manifest_rejected(self):
        with self.assertRaises(final.FinalAuditStop):
            self.run_audit(third_manifest_sha="0"*64)

    def test_path_traversal_rejected(self):
        with self.assertRaises(final.FinalAuditStop):
            self.run_audit(third="../../database")

    def test_legacy_production_fingerprint_rejected(self):
        with self.assertRaises(Exception):
            self.run_audit(source_sha="0"*64)


if __name__ == "__main__":
    unittest.main()
