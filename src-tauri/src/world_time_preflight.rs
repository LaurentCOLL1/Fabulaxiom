//! M3.1 read-only, *test-only* v6 preflight prototype.
//! No Tauri command or production migration calls this module.
//! A successful result is NOT a backup manifest nor permission to migrate v7.
use rusqlite::Connection;

use crate::database;

const EXPECTED_MIGRATIONS: [&str; 6] = [
    "001_create_app_metadata",
    "002_create_project_hierarchy",
    "003_create_scene_text_revisions",
    "004_create_narrative_entity_registry",
    "005_create_narrative_fact_provenance",
    "006_create_human_fact_review_log",
];

const PRESERVED_TABLES: [&str; 14] = [
    "app_metadata",
    "schema_migrations",
    "universes",
    "series",
    "novels",
    "chapters",
    "scenes",
    "scene_text_revisions",
    "scene_revision_heads",
    "narrative_entities",
    "entity_aliases",
    "narrative_facts",
    "fact_sources",
    "fact_review_events",
];

const UNREGISTERED_CANDIDATE_TABLES: [&str; 3] = [
    "fictional_calendars",
    "world_time_anchors",
    "world_time_precedences",
];

#[derive(Debug, PartialEq, Eq)]
pub enum PreflightFailure {
    Sqlite,
    ForeignKeysDisabled,
    UnexpectedVersion(i64),
    WrongOwner,
    MigrationRegistry,
    MissingOrNonStrictTable,
    UnregisteredCandidate,
    Integrity,
    ForeignKeyViolations,
}

#[derive(Debug, PartialEq, Eq)]
pub struct V6PreflightSnapshot {
    pub schema_version: i64,
    pub table_counts: Vec<(&'static str, i64)>,
}

fn count(db: &Connection, table: &'static str) -> Result<i64, PreflightFailure> {
    // Only compile-time constant, validated identifiers: never interpolate user input.
    let statement = format!("SELECT COUNT(*) FROM \"{table}\"");
    db.query_row(&statement, [], |row| row.get(0))
        .map_err(|_| PreflightFailure::Sqlite)
}

/// Read-only checks on a provided, already-open connection, never creates or
/// migrates a file, never resolves or changes the M1.5 active DB pointer.
/// A later separate operator process must prove backups/digests before activation.
pub fn inspect_v6(db: &Connection) -> Result<V6PreflightSnapshot, PreflightFailure> {
    let foreign_keys: i64 = db
        .query_row("PRAGMA foreign_keys", [], |row| row.get(0))
        .map_err(|_| PreflightFailure::Sqlite)?;
    if foreign_keys != 1 {
        return Err(PreflightFailure::ForeignKeysDisabled);
    }

    let version = database::current_schema_version(db)
        .map_err(|_| PreflightFailure::Sqlite)?;
    if version != 6 {
        return Err(PreflightFailure::UnexpectedVersion(version));
    }

    let owner: String = db
        .query_row(
            "SELECT value FROM app_metadata WHERE key='schema_owner'",
            [],
            |row| row.get(0),
        )
        .map_err(|_| PreflightFailure::WrongOwner)?;
    if owner != "fabulaxiom" {
        return Err(PreflightFailure::WrongOwner);
    }

    let mut migrations = db
        .prepare("SELECT version, name FROM schema_migrations ORDER BY version")
        .map_err(|_| PreflightFailure::Sqlite)?;
    let found = migrations
        .query_map([], |row| Ok((row.get::<_, i64>(0)?, row.get::<_, String>(1)?)))
        .map_err(|_| PreflightFailure::Sqlite)?
        .collect::<rusqlite::Result<Vec<_>>>()
        .map_err(|_| PreflightFailure::Sqlite)?;
    if found.len() != EXPECTED_MIGRATIONS.len()
        || found.iter().zip(EXPECTED_MIGRATIONS).enumerate().any(|(index, ((v, name), expected))| {
            *v != index as i64 + 1 || name != expected
        })
    {
        return Err(PreflightFailure::MigrationRegistry);
    }

    for table in PRESERVED_TABLES {
        let strict: i64 = db
            .query_row(
                "SELECT COUNT(*) FROM pragma_table_list WHERE name=?1 AND strict=1",
                [table],
                |row| row.get(0),
            )
            .map_err(|_| PreflightFailure::Sqlite)?;
        if strict != 1 {
            return Err(PreflightFailure::MissingOrNonStrictTable);
        }
    }
    for table in UNREGISTERED_CANDIDATE_TABLES {
        let existing: i64 = db
            .query_row(
                "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name=?1",
                [table],
                |row| row.get(0),
            )
            .map_err(|_| PreflightFailure::Sqlite)?;
        if existing != 0 {
            return Err(PreflightFailure::UnregisteredCandidate);
        }
    }

    let integrity: String = db
        .query_row("PRAGMA integrity_check", [], |row| row.get(0))
        .map_err(|_| PreflightFailure::Sqlite)?;
    if integrity != "ok" {
        return Err(PreflightFailure::Integrity);
    }
    let mut foreign_key_check = db
        .prepare("PRAGMA foreign_key_check")
        .map_err(|_| PreflightFailure::Sqlite)?;
    if foreign_key_check
        .query([])
        .map_err(|_| PreflightFailure::Sqlite)?
        .next()
        .map_err(|_| PreflightFailure::Sqlite)?
        .is_some()
    {
        return Err(PreflightFailure::ForeignKeyViolations);
    }

    let table_counts = PRESERVED_TABLES
        .into_iter()
        .map(|table| Ok((table, count(db, table)?)))
        .collect::<Result<Vec<_>, PreflightFailure>>()?;
    Ok(V6PreflightSnapshot { schema_version: 6, table_counts })
}

#[cfg(test)]
mod tests {
    use super::*;

    fn new_v6() -> Connection {
        let mut db = Connection::open_in_memory().expect("in-memory only");
        database::configure_connection(&db).expect("foreign keys ON");
        assert_eq!(database::run_migrations(&mut db).expect("v6 setup"), 6);
        db
    }

    #[test]
    fn preflight_on_new_v6_is_read_only_and_lists_all_legacy_tables() {
        let db = new_v6();
        let changes_before: i64 = db
            .query_row("SELECT total_changes()", [], |row| row.get(0))
            .expect("change counter");
        let snap = inspect_v6(&db).expect("unmodified v6");
        let changes_after: i64 = db
            .query_row("SELECT total_changes()", [], |row| row.get(0))
            .expect("change counter");
        assert_eq!(changes_before, changes_after);
        assert_eq!(snap.schema_version, 6);
        assert_eq!(snap.table_counts.len(), 14);
        assert!(snap.table_counts.iter().all(|(_, count)| *count >= 0));
    }

    #[test]
    fn preflight_rejects_disabled_foreign_keys_and_unknown_schema() {
        let db = new_v6();
        db.pragma_update(None, "foreign_keys", false)
            .expect("disable in disposable memory");
        assert_eq!(inspect_v6(&db), Err(PreflightFailure::ForeignKeysDisabled));
        db.pragma_update(None, "foreign_keys", true).expect("restore FK");
        db.execute("DELETE FROM schema_migrations WHERE version=6", [])
            .expect("synthetic old version");
        assert_eq!(inspect_v6(&db), Err(PreflightFailure::UnexpectedVersion(5)));
    }

    #[test]
    fn preflight_rejects_wrong_owner_and_tampered_migration_lineage() {
        let db = new_v6();
        db.execute("UPDATE app_metadata SET value='someone-else' WHERE key='schema_owner'", [])
            .expect("fixture ownership drift");
        assert_eq!(inspect_v6(&db), Err(PreflightFailure::WrongOwner));
        db.execute("UPDATE app_metadata SET value='fabulaxiom' WHERE key='schema_owner'", [])
            .expect("restore test owner");
        db.execute("UPDATE schema_migrations SET name='changed' WHERE version=6", [])
            .expect("synthetic migration tamper");
        assert_eq!(inspect_v6(&db), Err(PreflightFailure::MigrationRegistry));
    }

    #[test]
    fn preflight_rejects_undocumented_candidate_tables_before_v7_authorization() {
        let mut db = new_v6();
        db.execute_batch(include_str!("../sql/m3_1_world_time_v7_candidate.sql"))
            .expect("isolated candidate only");
        assert_eq!(inspect_v6(&db), Err(PreflightFailure::UnregisteredCandidate));
    }

    #[test]
    fn preflight_detects_foreign_key_violations_even_if_integrity_check_is_ok() {
        let db = new_v6();
        db.pragma_update(None, "foreign_keys", false)
            .expect("disabled only in disposable memory fixture");
        db.execute(
            "INSERT INTO entity_aliases(id,entity_id,universe_id,alias)
             VALUES ('orphan','missing-entity','missing-universe','Invalid')",
            [],
        ).expect("synthetic orphan");
        db.pragma_update(None, "foreign_keys", true).expect("restore FK");
        let integrity: String = db
            .query_row("PRAGMA integrity_check", [], |row| row.get(0))
            .expect("integrity");
        assert_eq!(integrity, "ok", "integrity_check alone cannot find FK violations");
        assert_eq!(inspect_v6(&db), Err(PreflightFailure::ForeignKeyViolations));
    }
}
