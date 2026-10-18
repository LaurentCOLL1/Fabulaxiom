"""Source-only, non-launch adversarial audit for an INERT M3.2 candidate.

The candidate is under tools/, NOT src-tauri/, never used by Tauri run(),
and cannot pass the currently guarded LAB_URL runtime validation.
"""
from copy import deepcopy
from pathlib import Path
import json
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from test_m3_2_tauri_capability_boundary import model_merge  # noqa: E402

CANDIDATE = ROOT / "tools" / "m32_static_tauri_candidate.json"
STATIC_SERVER = ROOT / "tools" / "m32_ci_precompiled_server.cjs"
ACTIVE = ROOT / "src-tauri" / "tauri.m32-synthetic-preview.conf.json"
BASE = ROOT / "src-tauri" / "tauri.conf.json"
RUST = ROOT / "src-tauri" / "src" / "m32_synthetic_preview.rs"
URL = "http://127.0.0.1:14279/m32-browser-lab.html"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def static_csp_source():
    raw = STATIC_SERVER.read_text(encoding="utf-8")
    match = re.search(r"const csp = \[\s*(.*?)\s*\]\.join\(\"; \"\)", raw, re.S)
    if not match:
        raise ValueError("STOP: source CSP declaration missing")
    entries = re.findall(r'^\s*"([^"]+)",\s*$', match.group(1), re.M)
    if len(entries) != 13:
        raise ValueError("STOP: unexpected static CSP declaration")
    return "; ".join(entries)


def reject_candidate(candidate, base, active):
    if set(candidate) != {"$schema", "productName", "identifier", "build", "app", "bundle"}:
        raise ValueError("candidate top-level drift")
    if candidate["identifier"] != active["identifier"] or candidate["identifier"] == base["identifier"]:
        raise ValueError("production or candidate identity drift")
    if set(candidate["build"]) != {
        "devUrl", "beforeDevCommand", "beforeBuildCommand", "frontendDist"
    } or candidate["build"]["devUrl"] != URL:
        raise ValueError("candidate URL or build attributes drift")
    if any(candidate["build"][key] is not None
           for key in ("beforeDevCommand", "beforeBuildCommand", "frontendDist")):
        raise ValueError("candidate inherited unsafe command/assets")
    if set(candidate["app"]) != {"windows", "security"}:
        raise ValueError("candidate application overrides")
    if len(candidate["app"]["windows"]) != 1 or candidate["app"]["windows"][0]["label"] != "m32-fiction":
        raise ValueError("candidate window is not fictional")
    security = candidate["app"]["security"]
    if set(security) != {"capabilities", "devCsp"} or security["capabilities"] != ["default"]:
        raise ValueError("unexpected runtime capabilities")
    policy = security["devCsp"]
    if not isinstance(policy, str) or policy != static_csp_source():
        raise ValueError("candidate CSP diverged from qualified static fixture server")
    if any(token in policy for token in ("unsafe-inline", "unsafe-eval", "http:", "https:", "ws:", "wss:", "ipc:", "*")):
        raise ValueError("permissive CSP source")
    if candidate["bundle"] != {"active": False}:
        raise ValueError("candidate bundle active")
    if active["build"]["devUrl"] == candidate["build"]["devUrl"] or "devCsp" in active["app"]["security"]:
        raise ValueError("candidate accidentally activated")
    if not CANDIDATE.is_relative_to(ROOT / "tools"):
        raise ValueError("candidate outside tools")
    merged = model_merge(base, candidate)
    if merged["build"]["devUrl"] != URL or any(
        key in merged["build"] for key in ("beforeDevCommand", "beforeBuildCommand", "frontendDist")
    ):
        raise ValueError("model inheritance or URL drift")
    if merged["app"]["security"].get("devCsp") != policy or merged["app"]["security"]["capabilities"] != ["default"]:
        raise ValueError("model security drift")
    return merged


class StaticCandidateRefusal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.candidate, cls.base, cls.active = load(CANDIDATE), load(BASE), load(ACTIVE)

    def good(self, value=None):
        return reject_candidate(self.candidate if value is None else value, self.base, self.active)

    def test_01_candidate_is_valid_but_never_active(self):
        self.good()
        self.assertNotEqual(self.candidate["build"]["devUrl"], self.active["build"]["devUrl"])
        self.assertNotIn("devCsp", self.active["app"]["security"])
        self.assertIn(self.active["build"]["devUrl"], RUST.read_text(encoding="utf-8"))

    def test_02_strict_csp_exact_source_match(self):
        self.assertEqual(self.good()["app"]["security"]["devCsp"], static_csp_source())
        self.assertIn("connect-src 'none'", static_csp_source())

    def test_03_reject_relaxed_and_remote_csp(self):
        for change in ("; script-src 'unsafe-inline'", "; connect-src https:", "; connect-src ipc:",
                       "; script-src *", "; style-src 'unsafe-eval'"):
            altered = deepcopy(self.candidate)
            altered["app"]["security"]["devCsp"] += change
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.good(altered)

    def test_04_reject_wrong_port_urls(self):
        for url in ("http://127.0.0.1:1420/m32-browser-lab.html",
                    "http://localhost:14279/m32-browser-lab.html",
                    "http://0.0.0.0:14279/m32-browser-lab.html",
                    "https://example.invalid/m32-browser-lab.html"):
            altered = deepcopy(self.candidate)
            altered["build"]["devUrl"] = url
            with self.subTest(url=url), self.assertRaises(ValueError):
                self.good(altered)

    def test_05_reject_hook_and_production_assets(self):
        for field, val in (("beforeDevCommand", "npm run dev"), ("beforeBuildCommand", "npm run build"),
                           ("frontendDist", "../dist")):
            altered = deepcopy(self.candidate)
            altered["build"][field] = val
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.good(altered)

    def test_06_reject_implicit_or_wildcard_capabilities(self):
        for list_value in ([], ["*"], ["default", "other"]):
            altered = deepcopy(self.candidate)
            altered["app"]["security"]["capabilities"] = list_value
            with self.subTest(value=list_value), self.assertRaises(ValueError):
                self.good(altered)

    def test_07_reject_main_and_extra_windows(self):
        for windows in ([{"label": "main"}], [{"label": "m32-fiction"}, {"label": "main"}]):
            altered = deepcopy(self.candidate)
            altered["app"]["windows"] = windows
            with self.assertRaises(ValueError):
                self.good(altered)

    def test_08_reject_extra_security_fields_and_release_bundle(self):
        for field, value in (("dangerousDisableAssetCspModification", True), ("csp", None),
                             ("assetProtocol", {"enable": True})):
            altered = deepcopy(self.candidate)
            altered["app"]["security"][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.good(altered)
        altered = deepcopy(self.candidate)
        altered["bundle"]["active"] = True
        with self.assertRaises(ValueError):
            self.good(altered)

    def test_09_runtime_still_refuses_candidate_url(self):
        code = RUST.read_text(encoding="utf-8")
        self.assertIn('pub(crate) const LAB_URL: &str = "http://127.0.0.1:1420/m32-browser-lab.html"', code)
        self.assertIn("actual_dev_url != Some(LAB_URL)", code)
        self.assertNotIn(f'pub(crate) const LAB_URL: &str = "{URL}"', code)

    def test_10_candidate_unreferenced_by_non_test_runtime(self):
        for rel in ("src-tauri/src/lib.rs", "src-tauri/Cargo.toml",
                    "src-tauri/tauri.conf.json", "src-tauri/tauri.m32-synthetic-preview.conf.json",
                    "package.json"):
            self.assertNotIn(CANDIDATE.name, (ROOT / rel).read_text(encoding="utf-8"), rel)


if __name__ == "__main__":
    unittest.main()
