"""CI-only Linux selected-dependency advisory evidence, NOT a vulnerability fix.

Read the pinned cross-platform Cargo graph WITHOUT building or running the app.
The confirmed glib 0.18.5 Linux GTK3 risk MUST remain OPEN_NOT_REMEDIATED.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from m32_glib_target_audit import graph_packages, lock_glib_versions

ROOT = Path(__file__).resolve().parents[1]
TRIPLE = "x86_64-unknown-linux-gnu"
ADVISORY = "GHSA-wrw7-89jp-8q8g"
CMD = (
    "cargo", "tree", "--manifest-path", "src-tauri/Cargo.toml",
    "--locked", "--offline", "--target", TRIPLE,
    "--edges", "normal,build", "--prefix", "none", "--format", "{p}",
)
# A clean Windows runner lacks Linux-only crate archives (e.g. atk 0.18.2).
# Download LOCKED source archives into disposable CI Cargo cache; no build/scripts.
# The subsequent target-selected graph check remains strictly --offline.
FETCH_CMD = (
    "cargo", "fetch", "--manifest-path", "src-tauri/Cargo.toml",
    "--locked", "--target", TRIPLE,
)

EXPECTED = {
    "glib": "0.18.5",
    "gtk": "0.18.2",
    "webkit2gtk": "2.0.2",
}


def assess_linux_graph(output: str) -> dict[str, object]:
    packages = graph_packages(output)
    if "fabulaxiom" not in packages or len(packages) < 20:
        raise ValueError("STOP: incomplete Linux target Cargo graph")
    for name, expected in EXPECTED.items():
        observed = packages.get(name)
        if observed != {expected}:
            raise ValueError(
                "STOP: Linux GTK advisory dependency drift: "
                + name + " expected " + expected + " observed " + repr(observed)
            )
    return {
        "linux_target": TRIPLE,
        "selected_package_count": len(packages),
        "selected_glib": EXPECTED["glib"],
        "selected_gtk": EXPECTED["gtk"],
        "selected_webkit2gtk": EXPECTED["webkit2gtk"],
        "advisory": ADVISORY,
        "linux_risk_status": "OPEN_NOT_REMEDIATED",
        "not_a_runtime_reachability_proof": True,
        "not_a_linux_build": True,
        "operator_windows_access": False,
        "real_g3": "STOP_UNAVAILABLE",
    }


def run_ci_audit() -> dict[str, object]:
    lock = (ROOT / "src-tauri" / "Cargo.lock").read_text(encoding="utf-8")
    versions = lock_glib_versions(lock)
    if versions != ("0.18.5",):
        raise ValueError("STOP: source GLib versions changed; fresh security review required " + repr(versions))
    fetched = subprocess.run(
        FETCH_CMD, cwd=ROOT, capture_output=True, text=True,
        timeout=300, check=False, shell=False,
    )
    if fetched.returncode:
        raise RuntimeError("STOP: locked Linux crate archive prefetch failed: " +
                           fetched.stderr[-1200:])
    result = subprocess.run(
        CMD, cwd=ROOT, capture_output=True, text=True,
        timeout=180, check=False, shell=False,
    )
    if result.returncode:
        raise RuntimeError("STOP: Linux selected graph unavailable (do not claim safety): "
                           + result.stderr[-1200:])
    return assess_linux_graph(result.stdout)


if __name__ == "__main__":
    try:
        report = run_ci_audit()
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print("M32_GLIB_LINUX_EXPOSURE_AUDIT_STOP: " + str(exc), file=sys.stderr)
        sys.exit(1)
    print("M32_GLIB_LINUX_EXPOSURE_AUDIT_PASS: " + repr(report))
