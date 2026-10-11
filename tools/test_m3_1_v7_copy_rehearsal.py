"""Copy-only v6->v7 operator rehearsal: disposable synthetic data only."""
from contextlib import closing
import hashlib
from pathlib import Path
import sqlite3
import tempfile
import unittest

import m3_1_v6_audit as audit
import m3_1_v6_backup as backup
import m3_1_v7_copy_rehearsal as rehearse
import test_m3_1_v6_backup as fixture


# Inline small governed schema subset for isolated harness tests; production
# actual candidate SQL comes from source-controlled .sql with exact SHA gate.
CANDIDATE_SQL = """
CREATE TABLE fictional_calendars(
 id TEXT PRIMARY KEY, universe_id TEXT NOT NULL
) STRICT;
CREATE TABLE world_time_anchors(
 id TEXT PRIMARY KEY, universe_id TEXT NOT NULL
) STRICT;
CREATE TABLE world_time_precedences(
 id TEXT PRIMARY KEY, universe_id TEXT NOT NULL
) STRICT;
CREATE TRIGGER world_time_precedences_guard
BEFORE INSERT ON world_time_precedences
BEGIN
 SELECT CASE WHEN NEW.id='' THEN RAISE(ABORT,'no-empty-id') END;
END;
"""


class CopyOnlyRehearsalFixture(unittest.TestCase):
    def setUp(self):
        self.fixture = fixture.BackupTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.root = self.fixture.root
        self.record = self.fixture.run_stage(create=True)
        self.custody_rel = self.record["relative_custody_dir"]
        self.sql_dir = tempfile.TemporaryDirectory(prefix="fabulaxiom-m31-sql-fixture-")
        self.addCleanup(self.sql_dir.cleanup)
        self.sql = Path(self.sql_dir.name) / "candidate.sql"
        self.sql.write_text(CANDIDATE_SQL, encoding="utf-8")
        self.sql_sha = audit._file_sha256(self.sql)

    def go(self, create, **overrides):
        args = dict(
            root=self.root,
            relative=self.custody_rel,
            expected_active=self.fixture.name,
            expected_source=self.fixture.sha,
            expected_logical=self.fixture.logical,
            expected_backup=self.record["backup_sha256"],
            expected_manifest=self.record["manifest_sha256"],
            candidate_sql_file=self.sql,
            expected_sql=self.sql_sha,
            create=create,
        )
        args.update(overrides)
        return rehearse.perform(**args)

    def test_read_only_dry_run_creates_no_rehearsal(self):
        prior = set((self.root/"operator-qualification"/"m3_1").iterdir())
        result = self.go(False)
        self.assertEqual(result["status"], "READY")
        self.assertEqual(result["original_schema_version"], 6)
        self.assertEqual(
            set((self.root/"operator-qualification"/"m3_1").iterdir()), prior
        )

    def test_copy_only_upgrade_v7_preserves_production_and_safety_snapshot(self):
        source_before = audit._file_sha256(self.fixture.file)
        result = self.go(True)
        self.assertEqual(result["status"], "PASS")
        self.assertFalse(result["production_migrated"])
        self.assertFalse(result["active_pointer_modified"])
        candidate = self.root / result["relative_rehearsal_dir"] / "candidate-v7.sqlite3"
        with closing(sqlite3.connect(
            candidate.as_uri() + "?mode=ro", uri=True
        )) as db:
            self.assertEqual(
                db.execute("SELECT max(version) FROM schema_migrations").fetchone(), (7,)
            )
            for table in audit.CANDIDATE_TABLES:
                self.assertEqual(
                    db.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone(), (0,)
                )
        self.assertEqual(audit._file_sha256(self.fixture.file), source_before)
        self.assertEqual(
            audit._file_sha256(
                self.root / self.custody_rel /
                "fabulaxiom-pre-m3-1-v6.sqlite3"
            ), self.record["backup_sha256"]
        )

    def test_rejects_source_hash_drift_before_creating_files(self):
        with self.assertRaises(backup.BackupStop):
            self.go(True, expected_source="0"*64)

    def test_rejects_corrupted_backup_expected_hash(self):
        with self.assertRaises(rehearse.RehearsalStop):
            self.go(True, expected_backup="0"*64)

    def test_rejects_changed_manifest_sha(self):
        with self.assertRaises(rehearse.RehearsalStop):
            self.go(True, expected_manifest="0"*64)

    def test_rejects_unapproved_candidate_sql(self):
        with self.assertRaises(rehearse.RehearsalStop):
            self.go(True, expected_sql="0"*64)

    def test_invalid_ddl_rolls_back_only_new_copy(self):
        original = audit._file_sha256(self.fixture.file)
        before_backup = self.record["backup_sha256"]
        self.sql.write_text(
            "CREATE TABLE fictional_calendars(id TEXT PRIMARY KEY) STRICT;\n"
            "CREATE TABLE fictional_calendars(id TEXT PRIMARY KEY) STRICT;",
            encoding="utf-8",
        )
        self.sql_sha = audit._file_sha256(self.sql)
        with self.assertRaises(sqlite3.Error):
            self.go(True)
        self.assertEqual(audit._file_sha256(self.fixture.file), original)
        self.assertEqual(audit._file_sha256(
            self.root / self.custody_rel / "fabulaxiom-pre-m3-1-v6.sqlite3"
        ), before_backup)

    def test_bad_custody_path_traversal_rejected(self):
        with self.assertRaises(rehearse.RehearsalStop):
            self.go(False,relative="../../database")


if __name__ == "__main__":
    unittest.main()
