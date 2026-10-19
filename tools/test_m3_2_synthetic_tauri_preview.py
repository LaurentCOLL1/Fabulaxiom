"""M3.2 FICTIONAL Tauri preview: repository source-only refusal tests.

No original/backup paths, no SQLite imports, no network and no process launch.
The tests inspect only tracked source and synthetic-only configuration.
"""
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / "src-tauri" / "src" / "lib.rs"
MODULE = ROOT / "src-tauri" / "src" / "m32_synthetic_preview.rs"
OVERLAY = ROOT / "src-tauri" / "tauri.m32-synthetic-preview.conf.json"
CARGO = ROOT / "src-tauri" / "Cargo.toml"
CONFIG = ROOT / "src-tauri" / "tauri.conf.json"
FRONTEND = ROOT / "src" / "App.tsx"
LAB = ROOT / "src" / "m32BrowserLab.tsx"
LAB_HTML = ROOT / "m32-browser-lab.html"

IDENTITY = "com.fabulaxiom.m32synthetic.preview"
URL = "http://127.0.0.1:1420/m32-browser-lab.html"


class FictionalTauriPreviewPolicy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = LIB.read_text(encoding="utf-8")
        cls.source = MODULE.read_text(encoding="utf-8")
        cls.overlay = json.loads(OVERLAY.read_text(encoding="utf-8"))
        cls.normal = json.loads(CONFIG.read_text(encoding="utf-8"))
        cls.cargo = CARGO.read_text(encoding="utf-8")

    def test_01_separate_product_identity_not_production(self):
        self.assertEqual(self.overlay["identifier"], IDENTITY)
        self.assertNotEqual(self.overlay["identifier"], self.normal["identifier"])
        self.assertNotIn("m31launch", self.overlay["identifier"])
        self.assertEqual(self.overlay["bundle"]["active"], False)

    def test_02_exact_loopback_fake_html_no_main_page(self):
        self.assertEqual(self.overlay["build"]["devUrl"], URL)
        self.assertEqual(self.source.count('pub(crate) const LAB_URL:'), 1)
        self.assertIn(URL, self.source)
        self.assertIn('src="/src/m32BrowserLab.tsx"', LAB_HTML.read_text(encoding="utf-8"))
        self.assertNotIn("App.tsx", LAB_HTML.read_text(encoding="utf-8"))

    def test_03_explicit_main_only_capability_and_distinct_window(self):
        app = self.overlay["app"]
        self.assertEqual(app["security"]["capabilities"], ["default"])
        self.assertEqual(len(app["windows"]), 1)
        self.assertEqual(app["windows"][0]["label"], "m32-fiction")
        self.assertNotEqual(app["windows"][0]["label"], "main")

    def test_04_default_feature_stays_empty_and_opt_in_only(self):
        self.assertIn("default = []", self.cargo)
        self.assertRegex(self.cargo, r"(?m)^m32-synthetic-preview\s*=\s*\[\]$")
        self.assertNotIn("m32-synthetic-preview", self.normal["identifier"])

    def test_05_production_dispatch_excludes_synthetic(self):
        self.assertIn('not(any(feature = "m31-isolated-preview", feature = "m32-synthetic-preview"))', self.lib)
        self.assertIn('feature = "m32-synthetic-preview", not(feature = "m31-isolated-preview")', self.lib)
        self.assertIn('feature = "m31-isolated-preview", not(feature = "m32-synthetic-preview")', self.lib)

    def test_06_preview_compile_fails_release_and_mixed_m31(self):
        self.assertIn('feature = "m32-synthetic-preview", not(debug_assertions)', self.lib)
        self.assertIn('feature = "m31-isolated-preview", feature = "m32-synthetic-preview"', self.lib)
        self.assertIn('compile_error!("M3.2 fictional Tauri preview is DEBUG-ONLY', self.lib)

    def test_07_preview_startup_has_no_app_commands_or_plugins(self):
        begin = self.lib.index("/** Distinct DEVELOPMENT-ONLY fictional UI shell.")
        end = self.lib.index("\n#[cfg(test)]\nmod tests {", begin)
        startup = self.lib[begin:end]
        self.assertIn("tauri::Builder::default().run(context)", startup)
        for forbidden in [
            ".invoke_handler(", ".plugin(", ".manage(",
            "database::", "backup_status", "create_database_backup",
            "restore_database_backup", "ollama_status", "std::fs",
            "Connection::open", "run_migrations",
        ]:
            self.assertNotIn(forbidden, startup, forbidden)

    def test_08_preview_requires_explicit_exact_environment_identity(self):
        self.assertIn("FABULAXIOM_M32_PREVIEW_ID", self.lib)
        self.assertIn("validate_launch(actual_id, &explicit_id, actual_url, &windows)", self.lib)
        self.assertIn('pub(crate) const LAB_ID: &str = "' + IDENTITY + '"', self.source)
        self.assertIn('pub(crate) const LAB_WINDOW: &str = "m32-fiction"', self.source)
        self.assertIn("windows != [LAB_WINDOW]", self.source)

    def test_09_non_fictional_urls_and_extra_windows_refused(self):
        self.assertIn("actual_dev_url != Some(LAB_URL)", self.source)
        self.assertIn("Some(\"http://localhost:1420\")", self.source)
        self.assertIn('Some("https://example.com/m32-browser-lab.html")', self.source)
        self.assertIn('&["m32-fiction", "main"][..]', self.source)

    def test_10_no_production_ui_mount(self):
        self.assertNotIn("m32BrowserLab", FRONTEND.read_text(encoding="utf-8"))
        self.assertNotIn("M32SyntheticEventExplorer", FRONTEND.read_text(encoding="utf-8"))
        self.assertIn("M32SyntheticEventExplorer", LAB.read_text(encoding="utf-8"))

    def test_11_no_unexpected_runtime_overlay_keys(self):
        self.assertEqual(set(self.overlay), {"$schema", "productName", "identifier", "build", "app", "bundle"})
        self.assertEqual(set(self.overlay["build"]), {"devUrl", "beforeDevCommand", "beforeBuildCommand", "frontendDist"})
        for key in ("beforeDevCommand", "beforeBuildCommand", "frontendDist"):
            self.assertIsNone(self.overlay["build"][key])
        self.assertEqual(set(self.overlay["bundle"]), {"active"})
        self.assertEqual(set(self.overlay["app"]), {"windows", "security"})
        self.assertEqual(set(self.overlay["app"]["security"]), {"capabilities"})
        self.assertNotIn("appDirectoriesOverride", str(self.overlay))

    def test_12_no_real_custody_or_automatic_migration_in_new_module(self):
        source = self.source
        for disallowed in ["sqlite", "Connection", "app_local_data", "temp_dir(",
                           "fs::", "backup", "migrate", "V6", "V7",
                           "write(", "create_dir", "remove_file"]:
            self.assertNotIn(disallowed, source)
        self.assertIn("fictional", source.lower())

    def test_13_generated_core_reading_is_separate_test_only_module(self):
        expected = ('#[cfg(test)]' + chr(10) +
                    '#[path = "m32_generated_core_acl_tests.rs"]' + chr(10) +
                    'mod m32_generated_core_acl_tests;')
        self.assertIn(expected, self.source)
        generated = (ROOT / "src-tauri" / "src" /
                     "m32_generated_core_acl_tests.rs").read_text(encoding="utf-8")
        self.assertIn('std::env::var("CI")', generated)
        self.assertIn('std::env::var("RUNNER_OS")', generated)
        self.assertIn('fs::read_to_string', generated)
        self.assertIn('symlink_metadata', generated)
        for forbidden in ["tauri::Builder", "run(context)", "Connection::open",
                          "fs::write", "fs::remove", "fs::create", "sqlite3",
                          "std::process::Command", "std::process::Stdio"]:
            self.assertNotIn(forbidden, generated)



if __name__ == "__main__":
    unittest.main()
