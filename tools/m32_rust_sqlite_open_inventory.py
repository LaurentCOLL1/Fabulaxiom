"""Source-only inventory of SQLite opening sites across the checked-in Rust tree.

This is a textual regression tripwire, NOT a complete parser, not a file-level
safety proof, and never authorizes real G2-B/G3, SQLite access or OS commands.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
TREE = ROOT / "src-tauri" / "src"
PATTERNS = {
    "connection_open": re.compile(r"\bConnection::(?:open|open_with_flags|open_with_flags_and_vfs|open_in_memory)\s*\("),
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
    # Registered explicitly named VFS on disposable Windows test paths only.
    # The default VFS is never replaced; no operator opener is exposed.
    # +3 explicit RW opens for Windows fixture-only 128-bit FileId
    # predelegation positive/stale refusal/controlled postcheck swap witness.
    # +2 more explicitly claimed disposable RW connections test WAL refusal
    # and xShmMap's absence from the xOpen-only interception surface.
    # +2 further RW fixture calls exercise an aligned test-only io_methods
    # xShmMap wrapper, one fail-closed and one controlled delegation.
    # 2026-10-28: +2 explicitly reviewed disposable Windows VFS
    # open_with_flags_and_vfs calls and +2 RW flags for in-xOpen delegated
    # native handle veto/mismatch witnesses, never a production opener.
    # D2 P1-0 owner-authorized Windows CI disposable fixture: +4 reviewed
    # Connection::open_with_flags_and_vfs and +4 SQLITE_OPEN_READ_WRITE
    # occurrences, all in the already cfg(all(test, windows)) module.
    # Six new Rust tests share one random Local mutex/owned temp directory
    # and existing delegated FileId128 + WAL/xShmMap VFS wrappers. Source-only
    # count is not a production writer/external-writer-absence proof.
    # D3a adds exactly four cfg(test,windows) fixture-only SQLite RW opens:
    # real delegated -wal FileId128 match, wrong expected WAL ID xClose veto,
    # xShmLock refusal, and synthetic missing-method xOpen STOP.
    # D3b adds exactly two more Windows cfg(test) RW SQLite open sites:
    # one forced-termination CHILD on a fresh CI temp-owned main, one busy
    # sqlite3_close() fixture. Successor parents DO NOT reopen a crashed DB.
    # D3b has no production opener, existing-profile recovery or marker.
    # PR230 R4 Windows CI-only: ONE extra opening expression in the new
    # exclusive-before-WAL helper; not a runtime/production writer path.
    # Historical PR232: "src-tauri/src/m32_sqlite_vfs_preopen_tests.rs": (24, 0, 0, 0, 0, 25, 0)
    # PR233: one more Windows cfg(test) SQLite attempt; callback always
    # clones the preopened handle then refuses before default xOpen.
    "src-tauri/src/m32_sqlite_vfs_preopen_tests.rs": (26, 0, 0, 0, 0, 27, 0),
    # D3b-5 distinct Windows test-only phase fixture: one owned-file opener,
    # no successor SQLite open; historical 26 VFS witnesses unchanged.
    "src-tauri/src/m32_d3b5_phase_matrix_tests.rs": (1, 0, 0, 0, 0, 1, 0),
    # R2/R3 test-only: ONE RW SQLite opening on a *fresh* CI-owned file,
    # followed by actual SQLITE_FCNTL_WIN32_GET_HANDLE FileId128 verification.
    # A post-xOpen check is NOT atomic admission or WAL/SHM ownership.
    "src-tauri/src/m32_r23_sqlite_handle_boundary_tests.rs": (1, 0, 0, 0, 0, 1, 0),
    # PR234 Windows cfg(test): real read-only sqlite3_file against *fresh* CI
    # files, 1 seed open + 1 read-only VFS open + 1 refused write-open site;
    # SQL-open flags: READ_ONLY, READ_WRITE, and an explicit denied CREATE.
    # This is NOT real locking, operator access or a production writer.
    # R4 negative NORMAL-WAL refusal: one additional test-only stock writer
    # open on a brand-new %TEMP% file. Custom R3 VFS is READ_ONLY and has
    # no xShm* methods; never a production WAL or writer path.
    "src-tauri/src/m32_r3_preopened_readonly_vfs_tests.rs": (5, 0, 0, 0, 0, 4, 0),
    # R4 stock Windows SQLite VFS, freshly invented %TEMP% main, test-only.
    # One temporary RW fixture and one READ_ONLY reader, no custom xShm* proof.
    "src-tauri/src/m32_r4_wal_shm_disposable_tests.rs": (2, 0, 0, 0, 0, 1, 0),
    # R4 RAM-only design contract intentionally ABSENT from EXPECTED:
    # audit_inventory() only lists sources having nonzero SQLite occurrences.
    # 2026-10-28: an UNWIRED writer core owns an ALREADY admitted connection.
    # Two RAM-only constructors, migration and ATTACH are confined to its
    # #[cfg(test)] fictional fixture; no production path opening is added.
    "src-tauri/src/m32_v7_writer_service.rs": (2, 0, 1, 0, 1, 0, 0),
    # 2026-10-28 S1/S2 follow-up: five SQLite constructor mentions (two
    # additional connections for disposable WAL concurrency) and three open
    # flag names only in #[cfg(all(test, windows))] disposable preflight.
    # This path cannot mint V7WriterAdmission and is NOT a runtime opener.
    # S1 lifecycle decision fixture adds one explicitly reviewed SQLite open
    # inside #[cfg(all(test, windows))], on a newly owned disposable root;
    # it closes immediately and never constructs an admission runtime token.
    # S1: two more Connection::open calls only under Windows cfg(test):
    # explicit-close vs implicit-Drop disposable fixture, never production.
    # A2+A3 S1/S2 disposable Windows experiment: +3 test-only constructors
    # (clean fixture, read-only corrupted candidate, ambiguous WAL fixture)
    # and +1 READ_ONLY flag; absolutely no runtime opener added.
    "src-tauri/src/m32_v7_admission_preflight_tests.rs": (11, 0, 0, 0, 0, 4, 0),
    "src-tauri/src/m32_owner_handoff_actor_toy.rs": (2, 0, 0, 0, 1, 0, 0),
    "src-tauri/src/m32_owner_lifecycle_toy.rs": (4, 0, 0, 0, 1, 0, 0),
    "src-tauri/src/review_commands.rs": (0, 1, 0, 0, 0, 0, 0),
    "src-tauri/src/review_tests.rs": (1, 0, 1, 0, 0, 0, 0),
    "src-tauri/src/revision_commands.rs": (0, 1, 0, 0, 0, 0, 0),
    "src-tauri/src/revisions.rs": (1, 0, 1, 0, 0, 0, 0),
    # 2026-10-27: +2 explicitly scoped open_with_flags RW and +2 READ_WRITE
    # for close/reopen of a fresh disposable candidate file in #[cfg(test)].
    # Counts do not attest runtime ownership or operator-side execution.
    # 2026-10-27 next new-only gate: +2 READ_WRITE opens (one exclusive
    # claim handoff, one explicit reopen) and +1 v1..v6 migration runner call,
    # strictly after OS create_new in #[cfg(test)] runner-owned fixtures.
    # Still NOT a production v7 opener or proof against path substitution.
    # Follow-up fixture pins Windows no-delete-share handles over the file
    # handoff and records a negative parent-namespace replacement witness;
    # exact SQLite opening-site counts remain unchanged (NO new runtime path).
    # Next Windows fixture-only directory-chain pins and lexical escape veto
    # introduce no additional Connection::open or migration occurrences.
    # One more SQLite RW opening site is restricted to a Windows-only fixture
    # post-xOpen native HANDLE identity probe; NOT atomic authorization.
    # Win32 test-only FileIdInfo 128-bit observes one further disposable
    # post-xOpen RW test connection; it never constitutes atomic admission.
    "src-tauri/src/world_time_file_migration_tests.rs": (20, 4, 3, 2, 0, 8, 0),
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
