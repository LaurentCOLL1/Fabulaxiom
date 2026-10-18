"""M3.2 Windows CI source-only Tauri capability exposure guard.

No Tauri CLI, build, WebView2 runtime, SQLite, private paths, or IPC call.
Reports a deliberately narrow source/config model, NOT effective native ACL.
Tauri core:default grants multiple core APIs to 'main', not zero permissions.
Application invoke_handler commands must be audited separately.
"""
from fnmatch import fnmatchcase
from pathlib import Path

from test_m3_2_tauri_capability_boundary import (
    load, model_merge, reject_unsafe,
)
from test_m3_2_static_tauri_candidate import reject_candidate, load as read_candidate

ROOT = Path(__file__).resolve().parents[1]
WINDOW = "m32-fiction"
CORE_DEFAULT = "core:default"
CORE_GROUPS = (
    "app", "event", "image", "menu", "path",
    "resources", "tray", "webview", "window",
)
SOURCE_BANNER = "/** Distinct DEVELOPMENT-ONLY fictional UI shell."


def potentially_matches(capability: dict, label: str) -> bool:
    """Conservative modeling only: any selector can cause a source review veto."""
    selectors = capability.get("windows", []) + capability.get("webviews", [])
    if not isinstance(selectors, list):
        raise ValueError("capability selector is not a list")
    for selector in selectors:
        if not isinstance(selector, str):
            raise ValueError("invalid selector type")
        if fnmatchcase(label, selector):
            return True
    return False


def assess(normal: dict, active: dict, candidate: dict, cap: dict,
           available: list[str], lib: str, build_rs: str) -> dict:
    """Fail closed on sources that could widen the imaginary window's grants."""
    if available != ["default.json"]:
        raise ValueError("unreviewed capability files")
    if set(cap) != {"$schema", "identifier", "description", "windows", "permissions"}:
        raise ValueError("unexpected capability attribute, remote or webview selector")
    if cap.get("identifier") != "default" or cap.get("windows") != ["main"]:
        raise ValueError("unexpected capability window target")
    if cap.get("permissions") != [CORE_DEFAULT]:
        raise ValueError("normal core permissions changed")
    if potentially_matches(cap, WINDOW):
        raise ValueError("fictional window overlaps a Tauri capability")
    if not potentially_matches(cap, "main"):
        raise ValueError("normal main capability not accounted for")
    if build_rs.strip() != "fn main() {\n    tauri_build::build()\n}":
        raise ValueError("unreviewed custom command AppManifest/build script")
    if SOURCE_BANNER not in lib:
        raise ValueError("missing fictional builder boundary")
    shell = lib.split(SOURCE_BANNER, 1)[1].split("\n#[cfg(test)]\nmod tests {", 1)[0]
    if not shell.strip() or shell.count("tauri::Builder::default().run(context)") != 1:
        raise ValueError("fictional builder changed")
    if shell.count("validate_launch(") != 1 or shell.index("validate_launch(") > shell.index(
        "tauri::Builder::default().run(context)"
    ):
        raise ValueError("fictional admission guard removed or reordered")
    for forbidden in (
        ".invoke_handler(", ".plugin(", ".manage(", ".setup(",
        "database::open_database(", "Connection::open(",
        "create_database_backup(", "restore_database_backup(",
    ):
        if forbidden in shell:
            raise ValueError("synthetic Tauri builder gained an application command or source")
    reject_unsafe(normal, active, cap, available)
    # Candidate is a tools/-only JSON file; reject_candidate compares CSP with
    # the checked-in fictional static server. Both paths remain unlaunchable.
    reject_candidate(candidate, normal, active)
    reports = []
    for name, overlay in (("inactive_candidate", candidate), ("current_preview", active)):
        merged = model_merge(normal, overlay)
        windows = [w.get("label") for w in merged["app"]["windows"]]
        refs = merged["app"]["security"].get("capabilities")
        if windows != [WINDOW] or refs != ["default"]:
            raise ValueError("fictional merged window or capability reference widened")
        if any(isinstance(r, dict) for r in refs):
            raise ValueError("unexpected inline capability")
        reports.append((name, windows[0], tuple(refs)))
    return {
        "selected_capability": "default",
        "normal_window": "main",
        "normal_core_groups": CORE_GROUPS,
        "fictional_window": WINDOW,
        "fictional_matching_capabilities_in_source_model": (),
        "inspected_overlays": tuple(reports),
        "native_runtime_evaluated": False,
        "application_commands_exposed_by_fictional_builder": False,
    }


def audit_repository() -> dict:
    cap_dir = ROOT / "src-tauri" / "capabilities"
    if cap_dir.is_symlink():
        raise ValueError("capabilities directory symlink")
    children = sorted(cap_dir.iterdir())
    if any(not p.is_file() or p.is_symlink() for p in children):
        raise ValueError("unreviewed capability directory entry")
    return assess(
        load("src-tauri/tauri.conf.json"),
        load("src-tauri/tauri.m32-synthetic-preview.conf.json"),
        read_candidate(ROOT / "tools" / "m32_static_tauri_candidate.json"),
        load("src-tauri/capabilities/default.json"),
        [x.name for x in children],
        (ROOT / "src-tauri" / "src" / "lib.rs").read_text(encoding="utf-8"),
        (ROOT / "src-tauri" / "build.rs").read_text(encoding="utf-8"),
    )
