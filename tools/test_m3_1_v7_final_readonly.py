"""Independent M3.1 v7 constraints against EXACT six Rust-defined v6 migrations.

Only temporary operator-independent synthetic files; never user application data.
Unlike the tiny historical audit fixture, these tables have the actual
composite keys, revision ancestry and immutability triggers required by v7.
"""
from contextlib import closing
from pathlib import Path
import re
import sqlite3
import tempfile
import unittest

import m3_1_v6_audit as audit
import m3_1_v6_backup as backup
import m3_1_v7_copy_rehearsal as copy_v7
import m3_1_v7_final_readonly as final


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REAL_RUST = PROJECT_ROOT / "src-tauri" / "src" / "database.rs"
CANDIDATE_SQL = PROJECT_ROOT / "src-tauri" / "sql" / "m3_1_world_time_v7_candidate.sql"
MIGRATIONS = re.compile(
    r'Migration\s*\{\s*version:\s*(\d+),\s*name:\s*"([^"]+)",'
    r'\s*sql:\s*r#"(.*?)"#,?\s*\}', re.DOTALL
)
MIGRATION_LEDGER = re.compile(
    r'const MIGRATION_TABLE_SQL:\s*&str\s*=\s*r#"(.*?)"#;',
    re.DOTALL
)


def real_v6(path: Path) -> None:
    rust = REAL_RUST.read_text(encoding="utf-8")
    table = MIGRATION_LEDGER.search(rust)
    entries = MIGRATIONS.findall(rust)
    if table is None or [(int(v), n) for v, n, _ in entries] != list(
        enumerate(audit.MIGRATION_NAMES, 1)
    ):
        raise AssertionError("Rust migration definition differs from governed v6")
    if "pub const CURRENT_SCHEMA_VERSION: i64 = 6;" not in rust:
        raise AssertionError("Expected runtime v6 guard absent")
    if "pub const MAX_AUTOMATIC_MIGRATION_VERSION: i64 = 6;" not in rust:
        raise AssertionError("Automatic v7 guard absent")

    with closing(sqlite3.connect(path)) as db:
        db.execute("PRAGMA foreign_keys=ON")
        db.executescript(table.group(1))
        for version, name, sql in entries:
            db.executescript(sql)
            db.execute(
                "INSERT INTO schema_migrations(version,name) VALUES(?,?)",
                (int(version), name),
            )
            db.commit()
        db.execute("INSERT INTO universes(id,name) VALUES('u1','Memory Universe')")
        db.execute(
            "INSERT INTO series(id,universe_id,name,sort_order)"
            " VALUES('series1','u1','Memory series',0)"
        )
        db.execute(
            "INSERT INTO novels(id,universe_id,series_id,title,sort_order)"
            " VALUES('n1','u1','series1','Memory novel',0)"
        )
        db.execute(
            "INSERT INTO chapters(id,novel_id,title,sort_order)"
            " VALUES('c1','n1','Memory chapter',0)"
        )
        db.execute(
            "INSERT INTO scenes(id,chapter_id,title,sort_order)"
            " VALUES('s1','c1','Memory scene',0)"
        )
        db.execute(
            "INSERT INTO scene_text_revisions"
            "(id,scene_id,revision_number,content)"
            " VALUES('r1','s1',1,'Ancient moon text')"
        )
        db.execute(
            "INSERT INTO scene_revision_heads(scene_id,revision_id)"
            " VALUES('s1','r1')"
        )
        db.execute(
            "INSERT INTO narrative_entities(id,universe_id,kind,name)"
            " VALUES('e1','u1','event','Memory event')"
        )
        db.commit()
        if db.execute("PRAGMA integrity_check").fetchall() != [("ok",)]:
            raise AssertionError("Synthetic Rust migration integrity failed")
        if db.execute("PRAGMA foreign_key_check").fetchall():
            raise AssertionError("Synthetic Rust migration foreign keys failed")


class RealV7FinalReadOnlyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(
            prefix="fabulaxiom-m31-real-schema-only-"
        )
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "com.fabulaxiom.desktop"
        db_dir = self.root / "database"
        activation = db_dir / "activations"
        activation.mkdir(parents=True)
        (self.root / "operator-qualification").mkdir()
        self.name = (
            "fabulaxiom-restored-" + "1" * 32
            + "-0000000001-0000000001.sqlite3"
        )
        self.file = db_dir / self.name
        real_v6(self.file)
        (activation / (
            "activation-" + "2" * 32
            + "-0000000001-0000000001.active"
        )).write_text(self.name, encoding="utf-8")
        self.original = audit.audit(self.root)
        self.sha = self.original["closed_file_sha256"]
        self.logical = self.original["combined_logical_sha256"]
        self.safety = backup.perform(
            self.root, self.name, self.sha, self.logical, create=True
        )
        self.assertEqual(self.safety["status"], "PASS")
        self.sql_sha = audit._file_sha256(CANDIDATE_SQL)
        self.copy = copy_v7.perform(
            self.root, self.safety["relative_custody_dir"],
            self.name, self.sha, self.logical, self.safety["backup_sha256"],
            self.safety["manifest_sha256"], CANDIDATE_SQL, self.sql_sha,
            create=True
        )
        self.assertEqual(self.copy["status"], "PASS")

    def run_audit(self, **overrides):
        args = dict(
            root=self.root,
            custody=self.safety["relative_custody_dir"],
            third=self.copy["relative_rehearsal_dir"],
            active=self.name,
            source_sha=self.sha,
            logical_sha=self.logical,
            backup_sha=self.safety["backup_sha256"],
            custody_manifest_sha=self.safety["manifest_sha256"],
            third_sha=self.copy["candidate_sha256"],
            third_manifest_sha=self.copy["manifest_sha256"],
            sql_file=CANDIDATE_SQL,
            sql_sha=self.sql_sha,
        )
        args.update(overrides)
        return final.perform(**args)

    def test_real_candidate_constraints_ram_only(self):
        source_before = audit._file_sha256(self.file)
        third = self.root/self.copy["relative_rehearsal_dir"]/"candidate-v7.sqlite3"
        third_before = audit._file_sha256(third)
        response = self.run_audit()
        self.assertEqual(response["status"], "PASS")
        self.assertEqual(response["constraint_scenarios_passed"], 10)
        self.assertFalse(response["on_disk_sqlite_writes"])
        self.assertEqual(audit._file_sha256(self.file), source_before)
        self.assertEqual(audit._file_sha256(third), third_before)

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
