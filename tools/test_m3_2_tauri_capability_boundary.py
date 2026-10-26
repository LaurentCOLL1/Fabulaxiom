"""M3.2 fictional Tauri: fail-closed SOURCE-ONLY capability/config audit.

Inspects only tracked repository configuration/Rust source. Does not start a
process, open a database, run the Tauri CLI, or inspect a private Windows host.

The merge below is a conservative JSON model, NOT proof of the actual Tauri
CLI-resolved config; that distinction is an explicit pending operator gate.
"""
from copy import deepcopy
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
TAURI = ROOT / "src-tauri"
IDENTITY = "com.fabulaxiom.m32synthetic.preview"
FIXTURE_URL = "http://127.0.0.1:1420/m32-browser-lab.html"
WINDOW = "m32-fiction"
PLATFORM_FILES = {
    "tauri.windows.conf.json", "tauri.windows.conf.json5", "tauri.windows.conf.toml",
    "tauri.linux.conf.json", "tauri.macos.conf.json",
    "tauri.android.conf.json", "tauri.ios.conf.json",
}


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def model_merge(base, extra):
    """RFC 7396 JSON Merge Patch: null deletes keys, arrays replace entirely.

    Source-side reference model, NOT native Tauri CLI resolution or ACL.
    """
    if isinstance(extra, dict):
        result = deepcopy(base) if isinstance(base, dict) else {}
        for key, value in extra.items():
            if value is None:
                result.pop(key, None)
            else:
                result[key] = model_merge(result.get(key), value)
        return result
    return deepcopy(extra)


def reject_unsafe(normal: dict, overlay: dict, capability: dict, capability_names):
    """Narrow allowlist for the currently authorized, entirely fictional flavor."""
    if set(capability_names) != {"default.json"}:
        raise ValueError("unexpected capability source")
    if normal.get("identifier") != "com.fabulaxiom.desktop":
        raise ValueError("unexpected normal application")
    if [w.get("label") for w in normal.get("app", {}).get("windows", [])] != ["main"]:
        raise ValueError("unexpected normal windows")
    if set(overlay) != {"$schema", "productName", "identifier", "build", "app", "bundle"}:
        raise ValueError("unexpected overlay keys")
    if set(overlay["build"]) != {"devUrl", "beforeDevCommand", "beforeBuildCommand", "frontendDist"}:
        raise ValueError("unexpected build configuration")
    if any(overlay["build"][k] is not None for k in ("beforeDevCommand", "beforeBuildCommand", "frontendDist")):
        raise ValueError("fictional build hooks/dist must be deletion patches")
    if set(overlay["app"]) != {"windows", "security"}:
        raise ValueError("unexpected app configuration")
    if set(overlay["app"]["security"]) != {"capabilities"}:
        raise ValueError("unexpected security configuration")
    if overlay["app"]["security"]["capabilities"] != ["default"]:
        raise ValueError("capability list must be explicit and exclusive")
    if set(capability) != {"$schema", "identifier", "description", "windows", "permissions"}:
        raise ValueError("unexpected capability fields / remote / webviews")
    if capability["identifier"] != "default" or capability["windows"] != ["main"]:
        raise ValueError("capability overlaps fictional window")
    if capability["permissions"] != ["core:default"]:
        raise ValueError("normal capability changed; re-review required")
    if overlay["identifier"] != IDENTITY:
        raise ValueError("unexpected fictional identity")
    if overlay["build"]["devUrl"] != FIXTURE_URL:
        raise ValueError("unexpected fictional URL")
    if overlay["bundle"] != {"active": False}:
        raise ValueError("bundle activation forbidden")
    windows = overlay["app"]["windows"]
    if len(windows) != 1 or windows[0].get("label") != WINDOW:
        raise ValueError("unexpected fictional windows")

    merged = model_merge(normal, overlay)
    if merged["identifier"] != IDENTITY:
        raise ValueError("merged identity mismatch")
    if merged["build"]["devUrl"] != FIXTURE_URL:
        raise ValueError("merged URL mismatch")
    if any(k in merged["build"] for k in ("beforeDevCommand", "beforeBuildCommand", "frontendDist")):
        raise ValueError("inherited normal commands or frontend assets")
    if [w.get("label") for w in merged["app"]["windows"]] != [WINDOW]:
        raise ValueError("merged windows mismatch")
    if merged["app"]["security"]["capabilities"] != ["default"]:
        raise ValueError("merged capability mismatch")
    # Tauri's default capability discovery is avoided by a non-empty
    # explicit list. The selected capability targets "main", never this
    # flavor's "m32-fiction". This does NOT audit native runtime APIs.
    return merged


class FictionalTauriCapabilityBoundary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.normal = load("src-tauri/tauri.conf.json")
        cls.overlay = load("src-tauri/tauri.m32-synthetic-preview.conf.json")
        cls.default = load("src-tauri/capabilities/default.json")

    def safe(self, overlay=None, capability=None, names=None):
        return reject_unsafe(
            self.normal,
            self.overlay if overlay is None else overlay,
            self.default if capability is None else capability,
            ["default.json"] if names is None else names,
        )

    def test_01_explicit_nonempty_allowlist_is_not_auto_discovery(self):
        merged = self.safe()
        self.assertEqual(merged["app"]["security"]["capabilities"], ["default"])
        self.assertEqual(self.default["windows"], ["main"])
        self.assertNotIn(WINDOW, self.default["windows"])

    def test_02_only_one_tracked_capability_source(self):
        capability_dir = TAURI / "capabilities"
        candidates = sorted(p.name for p in capability_dir.iterdir() if p.is_file())
        self.assertEqual(candidates, ["default.json"])
        self.safe(names=candidates)

    def test_03_no_implicit_platform_override_hidden_from_source_model(self):
        files = {p.name for p in TAURI.iterdir() if p.is_file()}
        self.assertFalse(files & PLATFORM_FILES, files & PLATFORM_FILES)
        # Include case/format variations such as Tauri.windows.toml, not
        # just the JSON defaults. Every new override requires fresh review.
        self.assertEqual(
            {p for p in files if p.lower().startswith("tauri.")},
            {
                "tauri.conf.json",
                "tauri.m32-synthetic-preview.conf.json",
                "tauri.greenfield.conf.json",
            },
        )
        # The new source-only profile is a separately named, new-data ONLY
        # development identity, not an extra override for the fictional M3.2
        # preview. Audit its complete merge shape before allowlisting it.
        greenfield = load("src-tauri/tauri.greenfield.conf.json")
        self.assertEqual(
            set(greenfield),
            {"$schema", "productName", "identifier", "app", "bundle"},
        )
        self.assertEqual(greenfield["identifier"], "com.fabulaxiom.greenfield.v1")
        self.assertNotEqual(greenfield["identifier"], self.normal["identifier"])
        self.assertEqual(set(greenfield["app"]), {"windows"})
        self.assertEqual([w.get("label") for w in greenfield["app"]["windows"]], ["main"])
        self.assertEqual(greenfield["bundle"], {"active": False})
        self.assertNotIn("appDirectoriesOverride", self.normal["app"])
        self.assertNotIn("appDirectoriesOverride", greenfield["app"])
        merged_greenfield = model_merge(self.normal, greenfield)
        self.assertEqual(merged_greenfield["build"], self.normal["build"])
        self.assertEqual(merged_greenfield["identifier"], "com.fabulaxiom.greenfield.v1")
        self.assertEqual(merged_greenfield["bundle"], self.normal["bundle"])
        self.assertFalse(merged_greenfield["bundle"]["active"])

    def test_04_source_model_replaces_production_window_and_dev_url(self):
        merged = self.safe()
        self.assertEqual(merged["identifier"], IDENTITY)
        self.assertEqual(merged["build"]["devUrl"], FIXTURE_URL)
        self.assertEqual([x["label"] for x in merged["app"]["windows"]], [WINDOW])
        self.assertEqual(self.normal["build"]["beforeDevCommand"], "npm run dev")
        self.assertEqual(self.normal["build"]["beforeBuildCommand"], "npm run build")
        self.assertEqual(self.normal["build"]["frontendDist"], "../dist")
        for key in ("beforeDevCommand", "beforeBuildCommand", "frontendDist"):
            self.assertNotIn(key, merged["build"])
        # No CLI source-merge or WebView2 runtime permission proof is implied.
        self.assertIsNone(merged["app"]["security"]["csp"])

    def test_05_empty_capability_list_is_an_unsafe_regression(self):
        altered = deepcopy(self.overlay)
        altered["app"]["security"]["capabilities"] = []
        with self.assertRaises(ValueError):
            self.safe(overlay=altered)

    def test_06_extra_capability_or_glob_is_an_unsafe_regression(self):
        for entries in (["default", "other"], ["*"], ["main"], []):
            altered = deepcopy(self.overlay)
            altered["app"]["security"]["capabilities"] = entries
            with self.subTest(entries=entries), self.assertRaises(ValueError):
                self.safe(overlay=altered)
        with self.assertRaises(ValueError):
            self.safe(names=["default.json", "wildcard.toml"])

    def test_07_main_capability_cannot_be_extended_to_fictional_window(self):
        for windows in (["main", WINDOW], ["*"], ["m32-*"], [WINDOW]):
            altered = deepcopy(self.default)
            altered["windows"] = windows
            with self.subTest(windows=windows), self.assertRaises(ValueError):
                self.safe(capability=altered)

    def test_08_remotes_webviews_and_permissions_require_re_review(self):
        for field, value in (
            ("remote", {"urls": ["https://example.com"]}),
            ("webviews", ["*"]),
            ("local", False),
            ("platforms", ["windows"]),
        ):
            altered = deepcopy(self.default)
            altered[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.safe(capability=altered)
        altered = deepcopy(self.default)
        altered["permissions"] = ["core:default", "fs:default"]
        with self.assertRaises(ValueError):
            self.safe(capability=altered)

    def test_09_extra_window_app_override_and_nonfictional_url_rejected(self):
        mutants = []
        altered = deepcopy(self.overlay)
        altered["app"]["windows"].append({"label": "main"})
        mutants.append(altered)
        altered = deepcopy(self.overlay)
        altered["build"]["devUrl"] = "http://localhost:1420"
        mutants.append(altered)
        altered = deepcopy(self.overlay)
        altered["app"]["security"]["dangerousDisableAssetCspModification"] = True
        mutants.append(altered)
        altered = deepcopy(self.overlay)
        altered["build"]["beforeDevCommand"] = "npm run dev"
        mutants.append(altered)
        for i, candidate in enumerate(mutants):
            with self.subTest(case=i), self.assertRaises(ValueError):
                self.safe(overlay=candidate)

    def test_10_rust_builders_disjoint_and_no_synthetic_ffi_ipc_setup(self):
        lib = (TAURI / "src" / "lib.rs").read_text(encoding="utf-8")
        start = lib.index("/** Distinct DEVELOPMENT-ONLY fictional UI shell.")
        end = lib.index("\n#[cfg(test)]\nmod tests {", start)
        synthetic = lib[start:end]
        self.assertIn('FABULAXIOM_M32_PREVIEW_ID', synthetic)
        self.assertLess(synthetic.index("validate_launch("), synthetic.index("tauri::Builder::default().run(context)"))
        for disallowed in (
            ".invoke_handler(", ".plugin(", ".manage(", ".setup(",
            "database::open_database(", "std::fs", "Connection::open",
            "create_database_backup(", "restore_database_backup(",
        ):
            self.assertNotIn(disallowed, synthetic)
        self.assertIn('#[cfg(all(feature = "m32-synthetic-preview", not(debug_assertions)))]', lib)
        self.assertIn('feature = "m31-isolated-preview", feature = "m32-synthetic-preview"', lib)
        self.assertIn('not(any(feature = "m31-isolated-preview", feature = "m32-synthetic-preview"))', lib)


    def test_11_rfc7396_deletion_nested_objects_and_array_replacement(self):
        base = {"a": 1, "n": {"keep": 2, "remove": 3}, "windows": ["main"], "x": "old"}
        patch = {"a": None, "n": {"remove": None, "add": 4}, "windows": ["m32-fiction"], "x": {"ok": True}}
        result = model_merge(base, patch)
        self.assertEqual(result, {"n": {"keep": 2, "add": 4}, "windows": ["m32-fiction"], "x": {"ok": True}})
        self.assertEqual(base["a"], 1)  # never mutate input
        self.assertEqual(model_merge(None, {"to_delete": None, "new": 7}), {"new": 7})

    def test_12_inherited_commands_or_assets_cannot_reappear(self):
        for key in ("beforeDevCommand", "beforeBuildCommand", "frontendDist"):
            for value in ("npm run dev", "npm run build", "../dist", ""):
                altered = deepcopy(self.overlay)
                altered["build"][key] = value
                with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                    self.safe(overlay=altered)
            altered = deepcopy(self.overlay)
            del altered["build"][key]
            with self.subTest(key=key, value="missing"), self.assertRaises(ValueError):
                self.safe(overlay=altered)


if __name__ == "__main__":
    unittest.main()
