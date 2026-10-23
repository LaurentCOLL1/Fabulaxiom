"""Fail-closed PR changed-files gate for Fabulaxiom resume prompts.

This module reads only newline-delimited *fictional or git-reported file names*
from stdin. No SQLite, network, operator paths, git mutation or runtime calls.
GitHub Actions supplies paths from an exact-base git diff.
"""
from __future__ import annotations

import re
import sys

SHORT = "docs/continuity/RESUME_PROMPT_SHORT.md"
LONG = "docs/continuity/RESUME_PROMPT.md"
HANDOFFS = ("docs/continuity/HANDOFF_CURRENT.md",
            "docs/continuity/HANDOFF_CURRENT.json")
MATERIAL = re.compile(
    r"^(src/|src-tauri/src/|src-tauri/capabilities/|tools/|"
    r"docs/qualification/|[.]github/workflows/)"
)


def check_changed_paths(paths: list[str]) -> tuple[bool, tuple[str, ...]]:
    """Pure, synthetic-friendly check. Exact paths are never inferred."""
    changed = {p for p in paths if p}
    reasons: list[str] = []
    for path in (SHORT, LONG):
        if path not in changed:
            reasons.append(f"STOP missing required resume prompt in this PR: {path}")
    if any(MATERIAL.match(path) for path in changed):
        for path in HANDOFFS:
            if path not in changed:
                reasons.append(f"STOP M3.2 handoff missing from material PR: {path}")
    return (not reasons, tuple(reasons))


def main() -> int:
    # Fail closed for an empty list, including an accidental empty diff.
    paths = [line.rstrip("\r\n") for line in sys.stdin]
    passed, reasons = check_changed_paths(paths)
    if not passed:
        for reason in reasons:
            print(reason, file=sys.stderr)
        return 1
    print("M32_BOTH_RESUME_PROMPTS_EVERY_PR_PASS")
    print("M32_HANDOFF_SAME_PR_REQUIRED_PASS: material changes have both continuity files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
