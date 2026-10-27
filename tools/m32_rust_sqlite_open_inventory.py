"""Source-only inventory of SQLite opening sites across the checked-in Rust tree.

This is a textual regression tripwire, NOT a complete parser, not a file-level
safety proof, and never authorizes real G2-B/G3, SQLite access or OS commands.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
TREE = ROOT / "src-tauri" / "src"
PATTERNS = {
    "connection_open": re.compile(r"\bConnection::(?:open|open_with_flags|open_in_memory)\s*\("),
    "app_open_database": re.compile(r"\bdatabase::open_database\s*\("),
    "run_migrations": re.compile(r"\brun_migrations\s*\("),
    "vacuum_into": re.compile(r"\bVACUUM\s+INTO\b", re.IGNORECASE),
    "attach_database": re.compile(r"\bATTACH\s+DATABASE\b", re.IGNORECASE),
    "open_flags": re.compile(r"\bSQLITE_OPEN_(?:READ_ONLY|READ_WRITE|CREATE|URI)\b"),
    "raw_sqlite_or_backup": re.compile(r"\b(?:sqlite3_open(?:_v2)?|sqlite3_backup_init|backup::Backup::new)\b"),
}
# Exact known *textual occurrences*: 2026-10-20 main baseline plus 2026-10-21
# independent human-readable review of the PR116 new #[cfg(test)] RAM module.
# 2026-10-25 PR173: explicitly reviewed +2 Connection::open_with_flags URI
# calls and +3 SQLITE_OPEN flags in cfg(test) toy shared mode=memory.
# Source CI #40189324812 correctly FAILED on the unreviewed old counts.
# New counts are checked-in text patterns ONLY, never claims of runtime safety.
EXPECTED = {
    "src-tauri/src/backup.rs": (10, 13, 0, 4, 0, 10, 0),
    "src-tauri/src/database.rs": (2, 0, 14, 0, 0, 0, 0),
    "src-tauri/src/entity.rs": (1, 0, 1, 0, 0, 0, 0),
    "src-tauri/src/entity_commands.rs": (0, 1, 0, 0, 0, 0, 0),
    "src-tauri/src/fact_commands.rs": (0, 1, 0, 0, 0, 0, 0),
    "src-tauri/src/facts.rs": (1, 0, 1, 0, 0, 0, 0),
    # Route C / same-profile refusal fixtures: twenty-seven reviewed calls,
    # exclusively in #[cfg(test)] and rooted under runner-created temp dirs.
    # Latest +6 cover wrong owner and forged schema lineage refusal.
    # No operator path,
    # production SQLite open, or historical G2B/G3 authorization.
    "src-tauri/src/greenfield_smoke_tests.rs": (0, 27, 0, 0, 0, 0, 0),
    "src-tauri/src/hierarchy.rs": (1, 0, 1, 0, 0, 0, 0),
    "src-tauri/src/hierarchy_commands.rs": (0, 1, 0, 0, 0, 0, 0),
    "src-tauri/src/lib.rs": (0, 1, 0, 0, 0, 0, 0),
    "src-tauri/src/m31_readonly_preview.rs": (1, 2, 0, 0, 0, 1, 0),
    "src-tauri/src/m32_manual_chronology.rs": (1, 0, 1, 0, 0, 0, 0),
    "src-tauri/src/m32_owned_backup_toy.rs": (14, 0, 0, 0, 2, 0, 0),
    "src-tauri/src/m32_preopened_query_only_toy.rs": (3, 0, 0, 0, 2, 3, 0),
    "src-tauri/src/m32_owner_handoff_actor_toy.rs": (2, 0, 0, 0, 1, 0, 0),
    "src-tauri/src/m32_owner_lifecycle_toy.rs": (4, 0, 0, 0, 1, 0, 0),
    "src-tauri/src/review_commands.rs": (0, 1, 0, 0, 0, 0, 0),
    "src-tauri/src/review_tests.rs": (1, 0, 1, 0, 0, 0, 0),
    "src-tauri/src/revision_commands.rs": (0, 1, 0, 0, 0, 0, 0),
    "src-tauri/src/revisions.rs": (1, 0, 1, 0, 0, 0, 0),
    "src-tauri/src/world_time_file_migration_tests.rs": (14, 4, 2, 2, 0, 2, 0),
    "src-tauri/src/world_time_preflight.rs": (1, 0, 1, 0, 0, 0, 0),
    "src-tauri/src/world_time_schema_tests.rs": (1, 0, 1, 0, 0, 0, 0),
}

class ReviewRequired(RuntimeError):
    pass

def counts(contents: str) -> tuple[int, ...]:
    if type(contents) is not str:
        raise ReviewRequired("STOP: source text required")
    return tuple(len(pattern.findall(contents)) for pattern in PATTERNS.values())

def audit_inventory(sources: dict[str, str]) -> dict[str, object]:
    if type(sources) is not dict or not sources:
        raise ReviewRequired("STOP: missing source inventory")
    observed = {}
    for name, contents in sources.items():
        if (type(name) is not str or not name.startswith("src-tauri/src/")
                or not name.endswith(".rs") or "../" in name):
            raise ReviewRequired("STOP: unexpected input path")
        count = counts(contents)
        if any(count):
            observed[name] = count
    if observed != EXPECTED:
        raise ReviewRequired("STOP: changed SQLite-related Rust occurrence inventory; review required")
    return {
        "scope": "PUBLIC_RUST_SOURCE_TEXT_ONLY",
        "review": "EXACT_KNOWN_TEXT_COUNTS_MATCH_NOT_EXHAUSTIVE",
        "matched_files": len(observed),
        "originals_opened": False,
        "writer_absence": "NOT_PROVEN",
        "real_g3": "STOP_UNAVAILABLE",
        "operator_execution": "NOT_AUTHORIZED",
        "real_g3_authorized": False,
    }

def repository_inventory() -> dict[str, object]:
    # Read only checked-in Rust text, no SQLite opening, no command, no process inspection.
    sources = {
        file.relative_to(ROOT).as_posix(): file.read_text(encoding="utf-8")
        for file in sorted(TREE.rglob("*.rs"))
    }
    return audit_inventory(sources)
