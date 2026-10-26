"""Source-only guard for a proposed new-data Tauri identity.

Never starts Tauri, opens SQLite, enumerates operator directories or creates a profile.
All mutations used by the tests are to in-memory Python dictionaries/strings.
"""
import copy
import json
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "src-tauri" / "tauri.conf.json"
GREENFIELD = ROOT / "src-tauri" / "tauri.greenfield.conf.json"
DATABASE = ROOT / "src-tauri" / "src" / "database.rs"
BACKUP = ROOT / "src-tauri" / "src" / "backup.rs"

DEFAULT_ID = "com.fabulaxiom.desktop"
GREENFIELD_ID = "com.fabulaxiom.greenfield.v1"


def assert_separated(default, profile, database_text, backup_text):
    """Fail closed on accidental config/path regression; no runtime guarantee."""
    if default.get("identifier") != DEFAULT_ID:
        raise ValueError("Default Tauri identity changed unexpectedly")
    if profile.get("identifier") != GREENFIELD_ID:
        raise ValueError("Greenfield identity must be fixed and distinct")
    if profile["identifier"] == default["identifier"]:
        raise ValueError("Greenfield may not share the protected default identity")
    if default.get("app", {}).get("appDirectoriesOverride") is not None:
        raise ValueError("Default directory override requires a new safety review")
    if profile.get("app", {}).get("appDirectoriesOverride") is not None:
        raise ValueError("Greenfield directory override is forbidden")
    if profile.get("bundle") != {"active": False}:
        raise ValueError("Greenfield packaging/release is not authorized")
    if any(key in profile for key in ("build", "plugins")):
        raise ValueError("Greenfield must inherit the current local build, with no plugins")
    windows = profile.get("app", {}).get("windows", [])
    if len(windows) != 1 or windows[0].get("label") != "main":
        raise ValueError("Unexpected window topology")
    if "PROJETS NEUFS" not in windows[0].get("title", ""):
        raise ValueError("Development-only identity must be visible")
    if "app_local_data_dir()" not in database_text or not re.search(
        r"resolve_active_database_path\s*\(\s*&app_data_dir\s*\)", database_text
    ):
        raise ValueError("Database resolver no longer derives from Tauri app local data")
    if not re.search(r'root\.join\s*\(\s*"database"\s*\)', backup_text):
        raise ValueError("Database subdirectory no longer rooted in app local data")
    if not re.search(r'database_directory\s*\(\s*root\s*\)\.join\s*\(\s*"activations"\s*\)', backup_text):
        raise ValueError("Activation directory no longer under app local data")
    if not re.search(r"MAX_AUTOMATIC_MIGRATION_VERSION:\s*i64\s*=\s*6\s*;", database_text):
        raise ValueError("Greenfield reuse cannot silently allow v7+ migration")


class GreenfieldSourceContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.default = json.loads(DEFAULT.read_text(encoding="utf-8"))
        cls.profile = json.loads(GREENFIELD.read_text(encoding="utf-8"))
        cls.database_text = DATABASE.read_text(encoding="utf-8")
        cls.backup_text = BACKUP.read_text(encoding="utf-8")

    def assert_valid(self, default=None, profile=None, database=None, backup=None):
        assert_separated(
            self.default if default is None else default,
            self.profile if profile is None else profile,
            self.database_text if database is None else database,
            self.backup_text if backup is None else backup,
        )

    def test_current_exact_source_contract(self):
        self.assert_valid()

    def test_reject_same_identity(self):
        profile = copy.deepcopy(self.profile)
        profile["identifier"] = DEFAULT_ID
        with self.assertRaises(ValueError):
            self.assert_valid(profile=profile)

    def test_reject_modified_greenfield_identity(self):
        profile = copy.deepcopy(self.profile)
        profile["identifier"] = "com.fabulaxiom.other"
        with self.assertRaises(ValueError):
            self.assert_valid(profile=profile)

    def test_reject_directory_override_in_either_config(self):
        for candidate in ("default", "profile"):
            with self.subTest(candidate=candidate):
                default, profile = copy.deepcopy(self.default), copy.deepcopy(self.profile)
                (default if candidate == "default" else profile).setdefault("app", {})[
                    "appDirectoriesOverride"
                ] = {"localData": "C:/fiction/other"}
                with self.assertRaises(ValueError):
                    self.assert_valid(default=default, profile=profile)

    def test_reject_bundling(self):
        profile = copy.deepcopy(self.profile)
        profile["bundle"]["active"] = True
        with self.assertRaises(ValueError):
            self.assert_valid(profile=profile)

    def test_reject_profile_build_or_plugin_override(self):
        for field in ("build", "plugins"):
            with self.subTest(field=field):
                profile = copy.deepcopy(self.profile)
                profile[field] = {"devUrl": "https://example.invalid"}
                with self.assertRaises(ValueError):
                    self.assert_valid(profile=profile)

    def test_reject_ambiguous_windows(self):
        profile = copy.deepcopy(self.profile)
        profile["app"]["windows"][0]["label"] = "historic"
        with self.assertRaises(ValueError):
            self.assert_valid(profile=profile)

    def test_reject_lost_tauri_local_data_binding(self):
        with self.assertRaises(ValueError):
            self.assert_valid(database=self.database_text.replace(
                "app_local_data_dir()", "app_data_dir()"
            ))

    def test_reject_lost_activation_root_binding(self):
        with self.assertRaises(ValueError):
            self.assert_valid(backup=self.backup_text.replace(
                'database_directory(root).join("activations")',
                'std::path::PathBuf::from("historic-activations")'
            ))

    def test_reject_v7_automatic_migration(self):
        with self.assertRaises(ValueError):
            self.assert_valid(database=self.database_text.replace(
                "MAX_AUTOMATIC_MIGRATION_VERSION: i64 = 6;",
                "MAX_AUTOMATIC_MIGRATION_VERSION: i64 = 7;"
            ))


if __name__ == "__main__":
    unittest.main()
