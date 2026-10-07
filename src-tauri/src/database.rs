use std::{
    collections::BTreeSet,
    fmt,
    fs,
    path::{Path, PathBuf},
    time::Duration,
};

use rusqlite::{params, Connection, Transaction};
use tauri::Manager;

pub const DATABASE_FILENAME: &str = "fabulaxiom.sqlite3";
pub const CURRENT_SCHEMA_VERSION: i64 = 1;

const MIGRATION_TABLE_SQL: &str = r#"
CREATE TABLE IF NOT EXISTS schema_migrations (
    version INTEGER PRIMARY KEY NOT NULL CHECK (version > 0),
    name TEXT NOT NULL UNIQUE,
    applied_at_utc TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
) STRICT;
"#;

#[derive(Clone, Copy)]
struct Migration {
    version: i64,
    name: &'static str,
    sql: &'static str,
}

const MIGRATIONS: &[Migration] = &[Migration {
    version: 1,
    name: "001_create_app_metadata",
    sql: r#"
CREATE TABLE app_metadata (
    key TEXT PRIMARY KEY NOT NULL CHECK (length(trim(key)) > 0),
    value TEXT NOT NULL,
    updated_at_utc TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
) STRICT;

INSERT INTO app_metadata (key, value)
VALUES ('schema_owner', 'fabulaxiom');
"#,
}];

#[derive(Debug)]
pub enum DatabaseError {
    Io(std::io::Error),
    Sqlite(rusqlite::Error),
    Path(String),
    UnsupportedSchemaVersion(i64),
}

impl fmt::Display for DatabaseError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Io(error) => write!(formatter, "erreur fichier/base locale : {error}"),
            Self::Sqlite(error) => write!(formatter, "erreur SQLite : {error}"),
            Self::Path(error) => write!(formatter, "chemin de données indisponible : {error}"),
            Self::UnsupportedSchemaVersion(version) => write!(
                formatter,
                "version de schéma SQLite non prise en charge : {version}"
            ),
        }
    }
}

impl std::error::Error for DatabaseError {}

impl From<std::io::Error> for DatabaseError {
    fn from(error: std::io::Error) -> Self {
        Self::Io(error)
    }
}

impl From<rusqlite::Error> for DatabaseError {
    fn from(error: rusqlite::Error) -> Self {
        Self::Sqlite(error)
    }
}

pub fn database_path<R: tauri::Runtime>(
    app: &tauri::AppHandle<R>,
) -> Result<PathBuf, DatabaseError> {
    let app_data_dir = app
        .path()
        .app_local_data_dir()
        .map_err(|error| DatabaseError::Path(error.to_string()))?;

    Ok(app_data_dir.join("database").join(DATABASE_FILENAME))
}

pub fn open_database(path: &Path) -> Result<Connection, DatabaseError> {
    if let Some(parent) = path.parent() {
        if !parent.as_os_str().is_empty() {
            fs::create_dir_all(parent)?;
        }
    }

    let mut connection = Connection::open(path)?;
    configure_connection(&connection)?;
    run_migrations(&mut connection)?;

    Ok(connection)
}

pub fn configure_connection(connection: &Connection) -> Result<(), DatabaseError> {
    connection.pragma_update(None, "foreign_keys", true)?;
    connection.busy_timeout(Duration::from_secs(5))?;

    if !foreign_keys_enabled(connection)? {
        return Err(DatabaseError::Sqlite(rusqlite::Error::InvalidQuery));
    }

    Ok(())
}

pub fn foreign_keys_enabled(connection: &Connection) -> Result<bool, DatabaseError> {
    let enabled: i64 =
        connection.pragma_query_value(None, "foreign_keys", |row| row.get(0))?;

    Ok(enabled == 1)
}

pub fn current_schema_version(connection: &Connection) -> Result<i64, DatabaseError> {
    let version = connection.query_row(
        "SELECT COALESCE(MAX(version), 0) FROM schema_migrations",
        [],
        |row| row.get(0),
    )?;

    Ok(version)
}

pub fn run_migrations(connection: &mut Connection) -> Result<i64, DatabaseError> {
    ensure_migration_table(connection)?;

    let applied_versions = load_applied_versions(connection)?;

    for version in &applied_versions {
        if !MIGRATIONS
            .iter()
            .any(|migration| migration.version == *version)
        {
            return Err(DatabaseError::UnsupportedSchemaVersion(*version));
        }
    }

    for migration in MIGRATIONS {
        if !applied_versions.contains(&migration.version) {
            apply_migration(connection, *migration)?;
        }
    }

    current_schema_version(connection)
}

fn ensure_migration_table(connection: &Connection) -> Result<(), DatabaseError> {
    connection.execute_batch(MIGRATION_TABLE_SQL)?;
    Ok(())
}

fn load_applied_versions(connection: &Connection) -> Result<BTreeSet<i64>, DatabaseError> {
    let mut statement =
        connection.prepare("SELECT version FROM schema_migrations ORDER BY version")?;

    let versions = statement
        .query_map([], |row| row.get::<_, i64>(0))?
        .collect::<Result<BTreeSet<_>, _>>()?;

    Ok(versions)
}

fn apply_migration(
    connection: &mut Connection,
    migration: Migration,
) -> Result<(), DatabaseError> {
    with_transaction(connection, |transaction| {
        transaction.execute_batch(migration.sql)?;
        transaction.execute(
            "INSERT INTO schema_migrations (version, name) VALUES (?1, ?2)",
            params![migration.version, migration.name],
        )?;

        Ok(())
    })
}

pub fn with_transaction<T, F>(
    connection: &mut Connection,
    operation: F,
) -> Result<T, DatabaseError>
where
    F: FnOnce(&Transaction<'_>) -> rusqlite::Result<T>,
{
    let transaction = connection.transaction()?;

    match operation(&transaction) {
        Ok(value) => {
            transaction.commit()?;
            Ok(value)
        }
        Err(error) => Err(DatabaseError::Sqlite(error)),
    }
}

#[cfg(test)]
mod tests {
    use std::{
        process,
        time::{SystemTime, UNIX_EPOCH},
    };

    use super::*;

    fn memory_connection() -> Connection {
        let connection = Connection::open_in_memory().expect("in-memory SQLite");
        configure_connection(&connection).expect("configured connection");
        connection
    }

    fn unique_test_root(name: &str) -> PathBuf {
        let nanos = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .expect("system time")
            .as_nanos();

        std::env::temp_dir().join(format!(
            "fabulaxiom-{name}-{}-{nanos}",
            process::id()
        ))
    }

    #[test]
    fn fresh_database_creates_and_applies_migration_once() {
        let root = unique_test_root("fresh-database");
        let database = root.join("nested").join(DATABASE_FILENAME);

        {
            let connection = open_database(&database).expect("open database");

            assert!(database.exists());
            assert_eq!(
                current_schema_version(&connection).expect("schema version"),
                CURRENT_SCHEMA_VERSION
            );

            let migration_count: i64 = connection
                .query_row("SELECT COUNT(*) FROM schema_migrations", [], |row| row.get(0))
                .expect("migration count");

            assert_eq!(migration_count, 1);

            let owner: String = connection
                .query_row(
                    "SELECT value FROM app_metadata WHERE key = 'schema_owner'",
                    [],
                    |row| row.get(0),
                )
                .expect("schema owner");

            assert_eq!(owner, "fabulaxiom");
        }

        fs::remove_dir_all(root).expect("remove temporary database");
    }

    #[test]
    fn migrations_are_idempotent() {
        let mut connection = memory_connection();

        let first = run_migrations(&mut connection).expect("first migration run");
        let second = run_migrations(&mut connection).expect("second migration run");

        assert_eq!(first, CURRENT_SCHEMA_VERSION);
        assert_eq!(second, CURRENT_SCHEMA_VERSION);

        let migration_count: i64 = connection
            .query_row("SELECT COUNT(*) FROM schema_migrations", [], |row| row.get(0))
            .expect("migration count");

        assert_eq!(migration_count, 1);
    }

    #[test]
    fn foreign_keys_are_enforced_for_every_configured_connection() {
        let connection = memory_connection();

        assert!(foreign_keys_enabled(&connection).expect("foreign key status"));

        connection
            .execute_batch(
                r#"
CREATE TABLE parent (
    id INTEGER PRIMARY KEY
);

CREATE TABLE child (
    id INTEGER PRIMARY KEY,
    parent_id INTEGER NOT NULL REFERENCES parent(id)
);
"#,
            )
            .expect("foreign-key fixture");

        let result = connection.execute(
            "INSERT INTO child (id, parent_id) VALUES (1, 999)",
            [],
        );

        assert!(result.is_err(), "invalid foreign key must be rejected");
    }

    #[test]
    fn failed_transaction_rolls_back_partial_schema_work() {
        let mut connection = memory_connection();

        let result = with_transaction(&mut connection, |transaction| {
            transaction.execute_batch(
                r#"
CREATE TABLE rollback_probe (
    id INTEGER PRIMARY KEY
);
"#,
            )?;

            transaction.execute(
                "INSERT INTO table_that_does_not_exist (id) VALUES (1)",
                [],
            )?;

            Ok(())
        });

        assert!(result.is_err());

        let table_count: i64 = connection
            .query_row(
                "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table' AND name = 'rollback_probe'",
                [],
                |row| row.get(0),
            )
            .expect("rollback probe lookup");

        assert_eq!(table_count, 0);
    }
}
