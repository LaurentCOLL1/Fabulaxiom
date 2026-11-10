"""M3.2 security-only lock contract for GHSA-p4f5-76q4-ffq7.

Runs on CI source files. No dev server launch, operator data, network or SQLite.
A successful test does not close Dependabot issue #160 or admit M3.2.
"""
from __future__ import annotations
from copy import deepcopy
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
LOCK = json.loads((ROOT / "package-lock.json").read_text(encoding="utf-8"))
VITE = "8.1.7"
ROLLDOWN = "1.1.7"


def validate(manifest: dict, lock: dict) -> None:
    packages = lock["packages"]
    if manifest["devDependencies"].get("vite") != VITE:
        raise ValueError("vite_manifest_not_patched")
    if packages[""].get("devDependencies", {}).get("vite") != VITE:
        raise ValueError("vite_lock_root_not_patched")
    if packages["node_modules/vite"].get("version") != VITE:
        raise ValueError("vite_lock_package_not_patched")
    if packages["node_modules/vite"].get("dependencies", {}).get("rolldown") != "~1.1.7":
        raise ValueError("vite_rolldown_constraint_unpatched")
    if packages["node_modules/rolldown"].get("version") != ROLLDOWN:
        raise ValueError("rolldown_package_not_patched")
    binaries = packages["node_modules/rolldown"].get("optionalDependencies", {})
    if not binaries or not {"@rolldown/binding-win32-x64-msvc",
                            "@rolldown/binding-win32-arm64-msvc"} <= set(binaries):
        raise ValueError("rolldown_windows_binding_missing")
    for name, version in binaries.items():
        if version != ROLLDOWN:
            raise ValueError("rolldown_binding_constraint_unpatched")
        pkg = packages.get("node_modules/" + name)
        if pkg is None or pkg.get("version") != ROLLDOWN:
            raise ValueError("rolldown_binding_lock_unpatched")
        if not re.fullmatch(r"sha512-[A-Za-z0-9+/=]+", pkg.get("integrity", "")):
            raise ValueError("rolldown_binding_integrity_missing")
    for name in ("node_modules/vite", "node_modules/rolldown"):
        if not re.fullmatch(r"sha512-[A-Za-z0-9+/=]+",
                            packages[name].get("integrity", "")):
            raise ValueError("core_integrity_missing")


class ViteSecurityLockContract(unittest.TestCase):
    def veto(self, code: str, manifest: dict, lock: dict) -> None:
        with self.assertRaisesRegex(ValueError, "^" + code + "$"):
            validate(manifest, lock)

    def test_01_actual_patch_and_platform_bindings(self):
        self.assertEqual(LOCK.get("lockfileVersion"), 3)
        validate(MANIFEST, LOCK)

    def test_02_manifest_mismatch_refused(self):
        m = deepcopy(MANIFEST)
        m["devDependencies"]["vite"] = "8.1.6"
        self.veto("vite_manifest_not_patched", m, LOCK)

    def test_03_lock_root_mismatch_refused(self):
        x = deepcopy(LOCK)
        x["packages"][""]["devDependencies"]["vite"] = "8.1.6"
        self.veto("vite_lock_root_not_patched", MANIFEST, x)

    def test_04_vite_package_downgrade_refused(self):
        x = deepcopy(LOCK)
        x["packages"]["node_modules/vite"]["version"] = "8.1.6"
        self.veto("vite_lock_package_not_patched", MANIFEST, x)

    def test_05_rolldown_constraint_downgrade_refused(self):
        x = deepcopy(LOCK)
        x["packages"]["node_modules/vite"]["dependencies"]["rolldown"] = "~1.1.5"
        self.veto("vite_rolldown_constraint_unpatched", MANIFEST, x)

    def test_06_binary_version_downgrade_refused(self):
        x = deepcopy(LOCK)
        x["packages"]["node_modules/@rolldown/binding-win32-x64-msvc"]["version"] = "1.1.5"
        self.veto("rolldown_binding_lock_unpatched", MANIFEST, x)

    def test_07_rolldown_version_downgrade_refused(self):
        x = deepcopy(LOCK)
        x["packages"]["node_modules/rolldown"]["version"] = "1.1.5"
        self.veto("rolldown_package_not_patched", MANIFEST, x)

    def test_08_missing_windows_binary_refused(self):
        x = deepcopy(LOCK)
        del x["packages"]["node_modules/rolldown"]["optionalDependencies"][
            "@rolldown/binding-win32-x64-msvc"]
        self.veto("rolldown_windows_binding_missing", MANIFEST, x)

    def test_09_missing_integrity_refused(self):
        x = deepcopy(LOCK)
        x["packages"]["node_modules/vite"].pop("integrity", None)
        self.veto("core_integrity_missing", MANIFEST, x)

    def test_10_default_dev_host_is_not_wildcard(self):
        # This is a code-only default, not evidence of operator environment state.
        config = (ROOT / "vite.config.ts").read_text(encoding="utf-8")
        self.assertIn("host: host || false", config)
        self.assertIn("process.env.TAURI_DEV_HOST", config)
        self.assertNotIn('host: "0.0.0.0"', config)


if __name__ == "__main__":
    unittest.main()
