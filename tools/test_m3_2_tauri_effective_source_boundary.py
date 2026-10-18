"""Adversarial source-only fictional Tauri capability isolation tests."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from m32_tauri_effective_source_boundary import (
    CORE_GROUPS, WINDOW, assess, audit_repository, potentially_matches,
)
from test_m3_2_tauri_capability_boundary import load
from test_m3_2_static_tauri_candidate import load as load_candidate

class CoreCapabilitySourceBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.normal = load("src-tauri/tauri.conf.json")
        cls.active = load("src-tauri/tauri.m32-synthetic-preview.conf.json")
        cls.candidate = load_candidate(ROOT / "tools" / "m32_static_tauri_candidate.json")
        cls.cap = load("src-tauri/capabilities/default.json")
        cls.lib = (ROOT / "src-tauri" / "src" / "lib.rs").read_text(encoding="utf-8")
        cls.build = (ROOT / "src-tauri" / "build.rs").read_text(encoding="utf-8")

    def check(self, **changes):
        inputs = dict(normal=deepcopy(self.normal), active=deepcopy(self.active),
                      candidate=deepcopy(self.candidate), cap=deepcopy(self.cap),
                      available=["default.json"], lib=self.lib, build_rs=self.build)
        inputs.update(changes)
        return assess(**inputs)

    def test_01_actual_sources_no_matching_core_grant_to_fictional_window(self):
        r = audit_repository()
        self.assertEqual(r["fictional_matching_capabilities_in_source_model"], ())
        self.assertEqual(r["fictional_window"], WINDOW)
        self.assertEqual(r["normal_window"], "main")
        self.assertEqual(r["inspected_overlays"][0][0], "inactive_candidate")

    def test_02_core_default_is_broad_and_belongs_to_main_not_fictional(self):
        r = self.check()
        self.assertEqual(len(r["normal_core_groups"]), 9)
        self.assertIn("path", CORE_GROUPS)
        self.assertIn("webview", CORE_GROUPS)
        self.assertIn("window", CORE_GROUPS)
        self.assertFalse(r["native_runtime_evaluated"])
        self.assertFalse(r["application_commands_exposed_by_fictional_builder"])

    def test_03_exact_and_wildcard_window_match_risk_is_visible(self):
        for match in (WINDOW, "*", "m32-*", "m32-fiction"):
            self.assertTrue(potentially_matches({"windows":[match]}, WINDOW))
        self.assertFalse(potentially_matches({"windows":["main"]}, WINDOW))
        self.assertTrue(potentially_matches({"webviews":[WINDOW]}, WINDOW))

    def test_04_reject_fictional_window_wildcard_and_glob_capabilities(self):
        for windows in ([WINDOW], ["main", WINDOW], ["*"], ["m32-*"], ["main", "*"]):
            cap=deepcopy(self.cap); cap["windows"]=windows
            with self.subTest(windows=windows), self.assertRaises(ValueError):
                self.check(cap=cap)

    def test_05_reject_webview_remote_and_platform_overrides(self):
        for key,value in (("webviews",[WINDOW]), ("remote",{"urls":["https://evil.invalid"]}),
                          ("platforms",["windows"]), ("local",True)):
            cap=deepcopy(self.cap);cap[key]=value
            with self.subTest(field=key),self.assertRaises(ValueError):
                self.check(cap=cap)

    def test_06_reject_core_default_changes_and_plugin_grants(self):
        for permissions in ([], ["fs:default"], ["core:default","fs:default"],
                            ["core:path:default"], ["core:default","core:webview:allow-create-webview-window"]):
            cap=deepcopy(self.cap);cap["permissions"]=permissions
            with self.subTest(permissions=permissions),self.assertRaises(ValueError):
                self.check(cap=cap)

    def test_07_reject_auto_discovery_and_new_capabilities(self):
        for names in ([], ["default.json","fiction.json"], ["default.toml"]):
            with self.subTest(names=names),self.assertRaises(ValueError):
                self.check(available=names)
        active=deepcopy(self.active)
        active["app"]["security"]["capabilities"]=[]
        with self.assertRaises(ValueError): self.check(active=active)

    def test_08_reject_inline_capability_and_multiple_reference_union(self):
        for refs in (["default","fiction"], [{"identifier":"fiction","windows":[WINDOW],
                     "permissions":["fs:default"]}], ["*"]):
            active=deepcopy(self.active);active["app"]["security"]["capabilities"]=refs
            with self.subTest(refs=refs),self.assertRaises(ValueError):
                self.check(active=active)

    def test_09_reject_candidate_window_or_security_gain(self):
        for ref in ([{"label":"main"}],[{"label":WINDOW},{"label":"main"}]):
            candidate=deepcopy(self.candidate);candidate["app"]["windows"]=ref
            with self.assertRaises(ValueError):self.check(candidate=candidate)
        candidate=deepcopy(self.candidate)
        candidate["app"]["security"]["capabilities"]=["default","other"]
        with self.assertRaises(ValueError):self.check(candidate=candidate)

    def test_10_reject_fictional_builder_commands_plugins_and_database(self):
        for added in (".invoke_handler(fake)", ".plugin(fake)", ".manage(fake)",
                      ".setup(fake)", "database::open_database(fake)"):
            text=self.lib.replace("tauri::Builder::default().run(context)",
                                  "tauri::Builder::default()"+added+".run(context)")
            with self.subTest(added=added),self.assertRaises(ValueError):
                self.check(lib=text)

    def test_11_reject_build_script_app_manifest_and_extra_sources(self):
        with self.assertRaises(ValueError):
            self.check(build_rs=self.build.replace("tauri_build::build()",
                                "tauri_build::try_build(tauri_build::Attributes::new().app_manifest(fake))"))
        with self.assertRaises(ValueError):
            self.check(lib=self.lib.replace("m32_synthetic_preview::validate_launch",
                                            "m32_synthetic_preview::unchecked_launch"))

    def test_12_source_only_is_not_native_acl_or_operator_permission(self):
        r=self.check()
        self.assertEqual(r["selected_capability"],"default")
        self.assertEqual(r["normal_core_groups"],CORE_GROUPS)
        self.assertFalse(r["native_runtime_evaluated"])

if __name__=="__main__":
    unittest.main()
