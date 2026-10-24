"""CI-only Rust dependency graph check, not a real SQLite custody or release gate.

The Linux GTK3/GLib GHSA remains OPEN even if Windows dependency selection excludes it.
No Cargo.lock changes, no Windows operator filesystem, no application execution.
"""
from __future__ import annotations

import re
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRIPLE = "x86_64-pc-windows-msvc"
ADVISORY = "GHSA-wrw7-89jp-8q8g"
# Detect GTK/WebKit as well as glib: a future Windows graph drift must fail closed.
GTK_PACKAGES = frozenset({
    "glib", "glib-sys", "gobject-sys", "gtk", "gtk-sys", "gdk",
    "gdk-sys", "gio", "gio-sys", "webkit2gtk", "webkit2gtk-sys",
})
CMD = (
    "cargo", "tree", "--manifest-path", "src-tauri/Cargo.toml",
    "--locked", "--offline", "--target", TRIPLE,
    "--edges", "normal,build", "--prefix", "none", "--format", "{p}",
)


def lock_glib_versions(lock_text: str) -> tuple[str, ...]:
    lock = tomllib.loads(lock_text)
    return tuple(
        str(p["version"]) for p in lock["package"] if p["name"] == "glib"
    )


def graph_packages(output: str) -> dict[str, set[str]]:
    """Parse Cargo's flat, package-version output without matching substrings."""
    packages: dict[str, set[str]] = {}
    for raw in output.splitlines():
        line = raw.strip()
        found = re.fullmatch(r"([A-Za-z0-9_-]+) v(\d+\.\d+\.\d+(?:[-+][^\s]+)?)(?:\s+.*)?", line)
        if found:
            packages.setdefault(found.group(1), set()).add(found.group(2))
    return packages


def assess_windows_graph(output: str) -> dict[str, object]:
    packages = graph_packages(output)
    if "fabulaxiom" not in packages or len(packages) < 20:
        raise ValueError("STOP: incomplete Windows target Cargo dependency graph")
    blocked = sorted(set(packages) & GTK_PACKAGES)
    if blocked:
        raise ValueError("STOP: unexpected GTK/GLib in Windows target: " + ", ".join(blocked))
    return {
        "windows_target": TRIPLE,
        "glib_in_selected_windows_target_graph": False,
        "selected_package_count": len(packages),
        "advisory": ADVISORY,
        "historical_linux_cargo_lock_advisory": "STILL_OPEN_NOT_REMEDIATED",
        "real_g3": "STOP_UNAVAILABLE",
    }


def run_ci_audit() -> dict[str, object]:
    lock_path = ROOT / "src-tauri" / "Cargo.lock"
    versions = lock_glib_versions(lock_path.read_text(encoding="utf-8"))
    if versions != ("0.18.5",):
        raise ValueError("STOP: Glib lock drift requires a new advisory review: " + repr(versions))
    result = subprocess.run(
        CMD, cwd=ROOT, capture_output=True, text=True,
        timeout=180, check=False, shell=False,
    )
    if result.returncode != 0:
        raise RuntimeError("STOP: Cargo Windows target graph unverified: " +
                           result.stderr[-1200:])
    return assess_windows_graph(result.stdout)


if __name__ == "__main__":
    try:
        result = run_ci_audit()
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print("M32_GLIB_WINDOWS_TARGET_AUDIT_STOP: " + str(exc), file=sys.stderr)
        sys.exit(1)
    print("M32_GLIB_WINDOWS_TARGET_AUDIT_PASS: " + str(result))
