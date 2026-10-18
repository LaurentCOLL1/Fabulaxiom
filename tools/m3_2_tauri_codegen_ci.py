"""Compile-time M3.2 Tauri context audit on Windows CI only.

This invokes one ignored *Rust unit test*, NEVER tauri dev/build/run or any
WebView. It feeds an exactly validated fictional config to Tauri's native
generate_context! path via TAURI_CONFIG. The merged JSON is produced by
the repository's conservative source model, NOT by Tauri CLI, so a pass
does NOT verify CLI --config ordering or runtime ACL grants.
No operator Windows files, SQLite, backups or secrets are accessed.
"""
from pathlib import Path
import json
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from test_m3_2_tauri_capability_boundary import load, reject_unsafe  # noqa: E402

IDENTITY = "com.fabulaxiom.m32synthetic.preview"
TEST = "m32_synthetic_preview::tests::compiled_fictional_context_no_runtime"


def main():
    if sys.platform != "win32" or os.environ.get("CI", "").lower() != "true":
        raise SystemExit("STOP: isolated Windows CI only; local/operator host disallowed")
    if "TAURI_CONFIG" in os.environ:
        raise SystemExit("STOP: pre-existing TAURI_CONFIG must not be inherited")
    if os.environ.get("TAURI_DEV_HOST"):
        raise SystemExit("STOP: TAURI_DEV_HOST override not authorized")
    normal = load("src-tauri/tauri.conf.json")
    overlay = load("src-tauri/tauri.m32-synthetic-preview.conf.json")
    capability = load("src-tauri/capabilities/default.json")
    capabilities = sorted(
        p.name for p in (ROOT / "src-tauri" / "capabilities").iterdir() if p.is_file()
    )
    merged = reject_unsafe(normal, overlay, capability, capabilities)
    if merged.get("identifier") != IDENTITY:
        raise SystemExit("STOP: unexpected synthetic identity")
    if merged["app"]["windows"][0]["label"] != "m32-fiction":
        raise SystemExit("STOP: unexpected window")
    if merged["app"]["security"]["capabilities"] != ["default"]:
        raise SystemExit("STOP: implicit capability discovery not accepted")
    if any(key in merged["build"] for key in ("beforeDevCommand", "beforeBuildCommand", "frontendDist")):
        raise SystemExit("STOP: inherited frontend command or production assets")
    if os.environ.get("FABULAXIOM_M32_PREVIEW_ID"):
        raise SystemExit("STOP: inherited preview identity forbidden")
    env = os.environ.copy()
    env["TAURI_CONFIG"] = json.dumps(merged, ensure_ascii=True, separators=(",", ":"))
    env["FABULAXIOM_M32_PREVIEW_ID"] = IDENTITY
    # This is cargo test --lib ONLY. Exactly one ignored test is selected,
    # which calls generate_context! and reads its config, not Builder::run.
    command = [
        "cargo", "test", "--locked", "--manifest-path",
        str(ROOT / "src-tauri" / "Cargo.toml"),
        "--features", "m32-synthetic-preview", "--lib", TEST,
        "--", "--ignored", "--exact", "--nocapture",
    ]
    print("M32_CONTEXT_CODEGEN: starting isolated Rust test compilation; no Tauri launch", flush=True)
    done = subprocess.run(
        command, cwd=ROOT / "src-tauri", env=env, check=False, timeout=1200
    )
    if done.returncode:
        raise SystemExit(f"FAIL: Tauri compiled-context test exit {done.returncode}")
    print("M32_COMPILED_CONTEXT_PASS: true (codegen only, no CLI --config or runtime)", flush=True)
    print("TAURI_RUNTIME_NOT_TESTED; OPERATOR_ACCEPTANCE_NOT_PERFORMED", flush=True)


if __name__ == "__main__":
    main()
