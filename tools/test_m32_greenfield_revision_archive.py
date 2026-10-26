"""Route C irreversible-history guard: source-only, no SQLite/operator execution."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class GreenfieldRevisionArchiveSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.commands = (ROOT / "src-tauri/src/revision_commands.rs").read_text(encoding="utf-8")
        cls.revisions = (ROOT / "src-tauri/src/revisions.rs").read_text(encoding="utf-8")
        cls.database = (ROOT / "src-tauri/src/database.rs").read_text(encoding="utf-8")
        cls.ui = (ROOT / "src/RevisionWorkspace.tsx").read_text(encoding="utf-8")
        cls.qualification = (ROOT / "docs/qualification/M3_2_ROUTE_C_REVISION_ARCHIVE_20261026.md").read_text(encoding="utf-8")

    def test_01_commands_refuse_non_greenfield_before_opening_sqlite(self):
        self.assertIn('const GREENFIELD_IDENTIFIER: &str = "com.fabulaxiom.greenfield.v1"', self.commands)
        self.assertIn("Err(RevisionError::GreenfieldOnly.payload())", self.commands)
        for name in ("scene_archived_revision_ids", "set_scene_revision_archived"):
            match = re.search(r"pub fn " + name + r"\([^)]*\)[^{]*\{([^}]+)", self.commands, re.S)
            self.assertIsNotNone(match, name)
            self.assertLess(match.group(1).find("require_greenfield(&app)?;"),
                            match.group(1).find("with_connection(&app"), name)

    def test_02_metadata_only_status_never_opens_sqlite(self):
        match = re.search(r"pub fn greenfield_revision_archive_enabled\([^)]*\)[^{]*\{([^}]+)", self.commands, re.S)
        self.assertIsNotNone(match)
        self.assertNotIn("with_connection", match.group(1))
        self.assertIn("is_greenfield_identifier", match.group(1))

    def test_03_append_only_revision_guard_preserved(self):
        self.assertIn("CREATE TRIGGER scene_text_revisions_no_delete", self.database)
        self.assertIn("RAISE(ABORT, 'scene text revisions are append-only')", self.database)
        self.assertIn("CREATE TRIGGER scene_text_revisions_immutable", self.database)
        source = self.revisions.split("#[cfg(test)]")[0]
        self.assertNotIn("DELETE FROM scene_text_revisions", source)
        self.assertNotIn("UPDATE scene_text_revisions", source)

    def test_04_archive_uses_existing_metadata_and_no_new_migration(self):
        self.assertIn('const ARCHIVE_KEY_PREFIX: &str = "greenfield_revision_archive:"', self.revisions)
        self.assertIn("INSERT INTO app_metadata(key, value)", self.revisions)
        self.assertIn("DELETE FROM app_metadata", self.revisions)
        self.assertIn("pub const CURRENT_SCHEMA_VERSION: i64 = 6", self.database)
        self.assertIn("pub const MAX_AUTOMATIC_MIGRATION_VERSION: i64 = 6", self.database)

    def test_05_current_revision_and_scene_identity_guards(self):
        self.assertIn("if revision.scene_id != scene_id", self.revisions)
        self.assertIn("La révision courante ne peut pas être archivée.", self.revisions)
        self.assertIn("with_revision_transaction(connection", self.revisions)

    def test_06_ui_only_displays_archive_controls_for_greenfield(self):
        self.assertIn('invoke<boolean>("greenfield_revision_archive_enabled")', self.ui)
        self.assertIn("{archiveEnabled &&", self.ui)
        self.assertIn("visibleSceneRevisions(history, archivedIds, showArchived)", self.ui)
        self.assertIn("Archiver (masquer)", self.ui)
        self.assertIn("Désarchiver", self.ui)

    def test_07_scope_documented_without_historical_promotion(self):
        self.assertIn("Aucune migration", self.qualification)
        self.assertIn("M3.2 `IN_PROGRESS_NOT_ACCEPTED`", self.qualification)
        self.assertIn("G3 réel `STOP_UNAVAILABLE`", self.qualification)


if __name__ == "__main__":
    unittest.main()
