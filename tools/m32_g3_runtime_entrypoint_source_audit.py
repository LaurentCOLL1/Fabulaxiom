"""Source-only architectural tripwire for M3.2 protected-original G3 refusal.

Never executes Rust, SQLite, OS calls, shell commands or accesses user databases.
Reads only checked-in repository Rust source text, and never grants real permission.
A mismatch is a REVIEW_REQUIRED refusal, not a claim that changed code is unsafe.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_SOURCES = {
    "database": Path("src-tauri/src/database.rs"),
    "backup": Path("src-tauri/src/backup.rs"),
    "lib": Path("src-tauri/src/lib.rs"),
}

class SourceReviewRequired(RuntimeError):
    pass

def unique_slice(text: str, begin: str, end: str) -> str:
    if type(text) is not str or not begin or not end:
        raise SourceReviewRequired("STOP: invalid source input")
    if text.count(begin) != 1:
        raise SourceReviewRequired("STOP: missing or ambiguous source start")
    i = text.index(begin)
    j = text.find(end, i + len(begin))
    if j < 0 or text.count(end, i) != 1 or j <= i:
        raise SourceReviewRequired("STOP: missing or ambiguous source end")
    return text[i:j]

def requires(fragment: str, tokens: tuple[str, ...]) -> None:
    for token in tokens:
        if token not in fragment:
            raise SourceReviewRequired("STOP: relevant Rust source drift needs explicit re-audit")

def audit_sources(database: str, backup: str, lib: str) -> dict[str, object]:
    if not all(type(x) is str for x in (database, backup, lib)):
        raise SourceReviewRequired("STOP: non-source inputs")
    opener = unique_slice(database, "pub fn open_database(path: &Path)", "pub fn configure_connection(")
    requires(opener, (
        "fs::create_dir_all(parent)?;",
        "Connection::open(path)?;",
        "configure_connection(&connection)?;",
        "run_migrations(&mut connection)?;",
    ))
    status = unique_slice(lib, "fn database_status(app: tauri::AppHandle)", '#[cfg(not(any(feature = "m31-isolated-preview"')
    requires(status, ("database::database_path(&app)", "database::open_database(&path)"))
    saver = unique_slice(backup, "pub fn create_backup(root: &Path)", "fn activate_new_database(")
    requires(saver, (
        "resolve_active_database_path(root)?;",
        "database::open_database(&source_path)",
        "reserve_unique_file(&backup_directory(root), BACKUP_PREFIX)?;",
        "vacuum_copy(&connection, &destination);",
    ))
    vacuum = unique_slice(backup, "fn vacuum_copy(connection: &Connection, destination: &Path)", "fn reserve_unique_file(")
    requires(vacuum, ('connection.execute("VACUUM INTO ?1"', "read_validated_database(destination)?;"))
    reserve = unique_slice(backup, "fn reserve_unique_file(directory: &Path, prefix: &str)", "/// App-owned backups only.")
    requires(reserve, ("create_new(true)", "drop(file);"))
    ro = unique_slice(backup, "fn read_validated_database(path: &Path)", "fn vacuum_copy(")
    requires(ro, ("Connection::open_with_flags(path, OpenFlags::SQLITE_OPEN_READ_ONLY)?;", "validate_connection(&conn)"))
    return {
        "review": "EXACT_KNOWN_SOURCE_PATTERNS_MATCH_REQUIRES_RUNTIME_AND_SOURCE_REVIEW",
        "open_database": "MAY_CREATE_AND_RUN_MIGRATIONS",
        "database_status": "CALLS_MIGRATION_CAPABLE_OPEN",
        "create_backup": "CALLS_MIGRATION_CAPABLE_OPEN_AND_VACUUM_INTO",
        "backup_reservation": "HANDLE_DROPPED_BEFORE_SQLITE_OUTPUT_OPEN",
        "read_validated_database": "READONLY_CONNECTION_NOT_PROOF_OF_SIDECAR_NONMODIFICATION",
        "writer_absence": "NOT_PROVEN",
        "real_g3": "STOP_UNAVAILABLE",
        "real_g3_authorized": False,
        "operator_command": "NOT_AUTHORIZED",
    }

def read_repository_source(root: Path = ROOT) -> dict[str, object]:
    if root != ROOT:
        raise SourceReviewRequired("STOP: only bundled repository sources permitted")
    content = {
        name: (ROOT / path).read_text(encoding="utf-8")
        for name, path in PUBLIC_SOURCES.items()
    }
    return audit_sources(content["database"], content["backup"], content["lib"])
