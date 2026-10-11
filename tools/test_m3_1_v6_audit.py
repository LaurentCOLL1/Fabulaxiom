"""Deterministic M3.1 audit-fixture tests. NEVER use real app-data paths."""
import contextlib
import io
import json
from pathlib import Path
import shutil
import sqlite3
import tempfile
import unittest

import m3_1_v6_audit as audit


class ReadOnlyAuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="fabulaxiom-m31-audit-fixture-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "database").mkdir()
        self.default = self.root / "database" / "fabulaxiom.sqlite3"
        self.fixture(self.default)

    def fixture(self, path):
        db = sqlite3.connect(path)
        try:
            db.execute("PRAGMA foreign_keys=ON")
            db.execute(
                "CREATE TABLE schema_migrations(version INTEGER PRIMARY KEY,"
                "name TEXT NOT NULL) STRICT"
            )
            db.execute("CREATE TABLE app_metadata(key TEXT PRIMARY KEY,"
                       "value TEXT NOT NULL) STRICT")
            db.execute("INSERT INTO app_metadata VALUES('schema_owner','fabulaxiom')")
            for v, name in enumerate(audit.MIGRATION_NAMES, start=1):
                db.execute(
                    "INSERT INTO schema_migrations VALUES(?,?)", (v, name)
                )
            db.execute(
                "CREATE TABLE universes(id TEXT PRIMARY KEY, name TEXT) STRICT"
            )
            db.execute("INSERT INTO universes VALUES('u1','Ancient 🌙')")
            for table in audit.LEGACY_TABLES:
                if table in ("schema_migrations", "app_metadata", "universes"):
                    continue
                if table == "narrative_entities":
                    db.execute(
                        "CREATE TABLE narrative_entities("
                        "id TEXT PRIMARY KEY, universe_id TEXT) STRICT"
                    )
                elif table == "entity_aliases":
                    db.execute(
                        "CREATE TABLE entity_aliases("
                        "id TEXT PRIMARY KEY, entity_id TEXT REFERENCES narrative_entities(id)) STRICT"
                    )
                else:
                    db.execute(f'CREATE TABLE "{table}"(id TEXT PRIMARY KEY) STRICT')
            db.commit()
        finally:
            db.close()

    def invoke(self, *additional):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = audit.main(
                ["--app-data-root", str(self.root), "--ack-app-stopped", *additional]
            )
        return code, json.loads(output.getvalue())

    def test_default_v6_audit_passes_without_filesystem_mutations(self):
        before = self.default.read_bytes()
        code, result = self.invoke()
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["active_file"], self.default.name)
        self.assertEqual(result["schema_version"], 6)
        self.assertEqual(len(result["legacy_tables"]), 14)
        self.assertEqual(result["legacy_tables"]["universes"]["rows"], 1)
        self.assertEqual(self.default.read_bytes(), before)

    def test_activation_pointer_chooses_latest_valid_marker_not_default(self):
        restored = "fabulaxiom-restored-" + ("7" * 32) + "-0000000001-0000000002.sqlite3"
        shutil.copyfile(self.default, self.root / "database" / restored)
        activation = self.root / "database" / "activations"
        activation.mkdir()
        (activation / ("activation-" + ("8" * 32) +
                       "-0000000001-0000000002.active")).write_text(
            restored, encoding="utf-8"
        )
        code, result = self.invoke()
        self.assertEqual(code, 0)
        self.assertEqual(result["active_file"], restored)

    def test_bad_latest_activation_marker_fails_closed(self):
        activation = self.root / "database" / "activations"
        activation.mkdir()
        (activation / ("activation-" + ("8" * 32) +
                       "-0000000001-0000000002.active")).write_text(
            "../dangerous.sqlite3", encoding="utf-8"
        )
        code, result = self.invoke()
        self.assertEqual(code, 2)
        self.assertEqual(result["reason"], "activation_marker_invalid")

    def test_wrong_v6_lineage_fails_without_fixes(self):
        conn = sqlite3.connect(self.default)
        conn.execute("UPDATE schema_migrations SET name='changed' WHERE version=6")
        conn.commit()
        conn.close()
        old = self.default.read_bytes()
        code, result = self.invoke()
        self.assertEqual(code, 2)
        self.assertEqual(result["reason"], "migration_registry_not_exact_v6")
        self.assertEqual(self.default.read_bytes(), old)

    def test_foreign_key_orphan_detected_independently_of_integrity(self):
        conn = sqlite3.connect(self.default)
        conn.execute(
            "INSERT INTO entity_aliases VALUES('bad','unknown-entity')"
        )
        conn.commit()
        conn.close()
        code, result = self.invoke()
        self.assertEqual(code, 2)
        self.assertEqual(result["reason"], "foreign_key_violation")

    def test_wal_sidecar_rejected_without_removing_it(self):
        sidecar = Path(str(self.default) + "-wal")
        sidecar.write_bytes(b"synthetic leftover")
        code, result = self.invoke()
        self.assertEqual(code, 2)
        self.assertIn("sidecars_present", result["reason"])
        self.assertEqual(sidecar.read_bytes(), b"synthetic leftover")

    def test_wal_mode_header_without_sidecars_refused_before_sqlite_open(self):
        conn = sqlite3.connect(self.default)
        self.assertEqual(
            conn.execute("PRAGMA journal_mode=WAL").fetchone()[0].lower(),
            "wal",
        )
        conn.close()
        # SQLite may or may not have removed auxiliaries on clean shutdown.
        # The header itself must still indicate WAL (bytes 18,19 are 2).
        with self.default.open("rb") as source:
            header = source.read(20)
        self.assertEqual(header[18:20], b"\x02\x02")
        before = self.default.read_bytes()
        code, result = self.invoke()
        self.assertEqual(code, 2)
        self.assertIn(result["reason"], (
            "sqlite_sidecars_present_stop_without_deleting_them",
            "wal_or_unknown_journal_header_requires_isolated_backup",
        ))
        self.assertEqual(self.default.read_bytes(), before)

    def test_absent_active_file_is_not_created(self):
        self.default.unlink()
        code, result = self.invoke()
        self.assertEqual(code, 2)
        self.assertEqual(result["reason"], "file_missing_or_unreadable")
        self.assertFalse(self.default.exists())

    def test_requires_operator_acknowledgement(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = audit.main(["--app-data-root", str(self.root)])
        self.assertEqual(code, 2)
        self.assertEqual(json.loads(output.getvalue())["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
