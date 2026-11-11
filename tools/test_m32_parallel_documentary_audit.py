"""Independent M3.2 documentary checks: repository sources and SQLite :memory: only."""
from pathlib import Path
import json
import re
import sqlite3
import unittest

ROOT = Path(__file__).resolve().parents[1]
AUDIT = (ROOT / "docs/qualification/M3_2_PARALLEL_DOCUMENTARY_AUDIT_20261111.md").read_text(encoding="utf-8")
CHECK = (ROOT / "docs/continuity/M3_2_COMPLETION_MASTER_CHECKLIST_20261109.md").read_text(encoding="utf-8")
SQL = (ROOT / "src-tauri/sql/m3_1_world_time_v7_candidate.sql").read_text(encoding="utf-8")


class DocumentaryGates(unittest.TestCase):
    def test_037_historical_limit_is_recorded_without_promotion(self):
        self.assertIn("PENDING_EXTERNAL_ATTESTATION(21/3/2)", AUDIT)
        for role in ("production/pre_m24_early_manifest", "acl/original_acls",
                     "acl/pre_repair_json", "production/activation_marker", "m25/isolated_v6"):
            self.assertIn(role, AUDIT)
        self.assertIn("issue #36", AUDIT.lower())
        self.assertIn("- [x] **M32-037**", CHECK)

    def test_049_greenfield_and_existing_have_different_authority(self):
        self.assertIn("NEW_ONLY", AUDIT)
        self.assertIn("EXISTING_PROFILE", AUDIT)
        self.assertIn("NOT_STARTED", (ROOT / "docs/qualification/M3_2_PROSPECTIVE_TRUST_BASELINE_DECISION.md").read_text(encoding="utf-8"))
        self.assertIn("Aucune SQLite originale", (ROOT / "docs/qualification/M3_2_GREENFIELD_NEW_ONLY_DISPOSABLE_V7_CHRONOLOGY_PERSISTENCE_20261027.md").read_text(encoding="utf-8"))
        self.assertIn("- [x] **M32-049**", CHECK)

    def test_051_v7_schema_exact_and_memory_negative_cases(self):
        self.assertIn("DO NOT register in the automatic migration runner", SQL)
        self.assertEqual(SQL.count(") STRICT;"), 3)
        for table in ("fictional_calendars", "world_time_anchors", "world_time_precedences"):
            self.assertIn("CREATE TABLE " + table, SQL)
            self.assertIn(table + "_no_update", SQL)
            self.assertIn(table + "_no_delete", SQL)
        db = sqlite3.connect(":memory:")
        try:
            db.execute("PRAGMA foreign_keys=ON")
            db.executescript("""
                CREATE TABLE universes(id TEXT PRIMARY KEY);
                CREATE TABLE narrative_entities(
                    id TEXT PRIMARY KEY, universe_id TEXT, kind TEXT,
                    UNIQUE(id, universe_id));
                CREATE TABLE novels(id TEXT PRIMARY KEY, universe_id TEXT);
                CREATE TABLE chapters(id TEXT PRIMARY KEY, novel_id TEXT);
                CREATE TABLE scenes(id TEXT PRIMARY KEY, chapter_id TEXT);
                CREATE TABLE scene_text_revisions(id TEXT PRIMARY KEY, scene_id TEXT);
            """)
            db.executescript(SQL)
            db.executemany("INSERT INTO universes VALUES (?)", [("u1",), ("u2",)])
            db.execute("INSERT INTO fictional_calendars(id,universe_id,name,definition_text) VALUES('cal1','u1','F','Temps fictif')")
            db.execute("INSERT INTO fictional_calendars(id,universe_id,name,definition_text) VALUES('cal2','u2','F','Temps fictif')")
            db.execute("INSERT INTO novels VALUES('novel1','u1')")
            db.execute("INSERT INTO chapters VALUES('ch1','novel1')")
            db.execute("INSERT INTO scenes VALUES('scene1','ch1')")
            db.execute("INSERT INTO scene_text_revisions VALUES('revision1','scene1')")
            db.execute("""INSERT INTO world_time_anchors(id,universe_id,calendar_id,time_kind,exact_label,source_revision_id)
                          VALUES('exact1','u1','cal1','exact','Cycle 1','revision1')""")
            db.execute("""INSERT INTO world_time_anchors(id,universe_id,calendar_id,time_kind,window_start_text,precision_text)
                          VALUES('approx1','u1','cal1','approximate','Cycle 2','imprécis')""")
            db.execute("INSERT INTO world_time_anchors(id,universe_id,time_kind) VALUES('relative1','u1','relative')")
            db.execute("INSERT INTO world_time_anchors(id,universe_id,time_kind) VALUES('unknown1','u1','unknown')")
            self.assertEqual({x[0] for x in db.execute("SELECT time_kind FROM world_time_anchors")},
                             {"exact", "approximate", "relative", "unknown"})
            with self.assertRaises(sqlite3.IntegrityError):
                db.execute("""INSERT INTO world_time_anchors(id,universe_id,calendar_id,time_kind,exact_label)
                              VALUES('badcross','u1','cal2','exact','bad')""")
            with self.assertRaises(sqlite3.IntegrityError):
                db.execute("INSERT INTO world_time_anchors(id,universe_id,time_kind) VALUES('badexact','u1','exact')")
            db.execute("""INSERT INTO world_time_precedences(id,universe_id,before_anchor_id,after_anchor_id,reason)
                          VALUES('p1','u1','exact1','approx1','déclaré')""")
            db.execute("""INSERT INTO world_time_precedences(id,universe_id,before_anchor_id,after_anchor_id,reason)
                          VALUES('p2','u1','approx1','relative1','déclaré')""")
            with self.assertRaises(sqlite3.IntegrityError):
                db.execute("""INSERT INTO world_time_precedences(id,universe_id,before_anchor_id,after_anchor_id,reason)
                              VALUES('p3','u1','relative1','exact1','cycle')""")
            with self.assertRaises(sqlite3.IntegrityError):
                db.execute("UPDATE world_time_anchors SET exact_label='changed' WHERE id='exact1'")
            with self.assertRaises(sqlite3.IntegrityError):
                db.execute("DELETE FROM fictional_calendars WHERE id='cal1'")
            self.assertEqual(db.execute("PRAGMA foreign_key_check").fetchall(), [])
            self.assertEqual(db.execute("PRAGMA integrity_check").fetchone()[0], "ok")
        finally:
            db.close()
        self.assertIn("- [x] **M32-051**", CHECK)

    def test_095_security_decisions_keep_glib_open(self):
        pkg = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
        lock = (ROOT / "src-tauri/Cargo.lock").read_text(encoding="utf-8")
        self.assertEqual(pkg["devDependencies"]["vite"], "8.1.7")
        self.assertRegex(lock, r'name = "glib"\nversion = "0\.18\.5"')
        self.assertIn("OPEN_NOT_REMEDIATED", AUDIT)
        self.assertIn("Distribution Linux NON AUTORISÉE", AUDIT)
        self.assertIn("- [x] **M32-095**", CHECK)

    def test_096_hello_is_future_policy_not_native_runtime(self):
        policy = (ROOT / "docs/qualification/M3_2_SINGLE_USER_WINDOWS_HELLO_SENSITIVE_CONSENT_POLICY_20261027.md").read_text(encoding="utf-8")
        lib = (ROOT / "src-tauri/src/lib.rs").read_text(encoding="utf-8")
        rust = (ROOT / "src-tauri/src/m32_sensitive_action_consent_tests.rs").read_text(encoding="utf-8")
        self.assertIn("AUCUN compte Fabulaxiom supplémentaire", policy)
        self.assertRegex(lib, r'#\[cfg\(test\)\]\s*mod m32_sensitive_action_consent_tests;')
        self.assertIn("NEVER invokes Windows Hello", rust)
        self.assertNotIn("#[tauri::command]", rust)
        self.assertIn("- [x] **M32-096**", CHECK)


if __name__ == "__main__":
    unittest.main()
