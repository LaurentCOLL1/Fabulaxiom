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
pub const CURRENT_SCHEMA_VERSION: i64 = 4;

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

const MIGRATIONS: &[Migration] = &[
    Migration {
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
    },
    Migration {
        version: 2,
        name: "002_create_project_hierarchy",
        sql: r#"
CREATE TABLE universes (
    id TEXT PRIMARY KEY NOT NULL CHECK (length(trim(id)) > 0),
    name TEXT NOT NULL CHECK (length(trim(name)) > 0)
) STRICT;

CREATE TABLE series (
    id TEXT PRIMARY KEY NOT NULL CHECK (length(trim(id)) > 0),
    universe_id TEXT NOT NULL,
    name TEXT NOT NULL CHECK (length(trim(name)) > 0),
    sort_order INTEGER NOT NULL CHECK (sort_order >= 0),
    UNIQUE (id, universe_id),
    UNIQUE (universe_id, sort_order),
    FOREIGN KEY (universe_id)
        REFERENCES universes(id)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
) STRICT;

CREATE TABLE novels (
    id TEXT PRIMARY KEY NOT NULL CHECK (length(trim(id)) > 0),
    universe_id TEXT NOT NULL,
    series_id TEXT,
    title TEXT NOT NULL CHECK (length(trim(title)) > 0),
    sort_order INTEGER NOT NULL CHECK (sort_order >= 0),
    FOREIGN KEY (universe_id)
        REFERENCES universes(id)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT,
    FOREIGN KEY (series_id, universe_id)
        REFERENCES series(id, universe_id)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
) STRICT;

CREATE INDEX idx_novels_universe_id
    ON novels(universe_id);

CREATE INDEX idx_novels_series_scope
    ON novels(series_id, universe_id)
    WHERE series_id IS NOT NULL;

CREATE UNIQUE INDEX uq_novels_series_order
    ON novels(series_id, sort_order)
    WHERE series_id IS NOT NULL;

CREATE UNIQUE INDEX uq_novels_standalone_order
    ON novels(universe_id, sort_order)
    WHERE series_id IS NULL;

CREATE TABLE chapters (
    id TEXT PRIMARY KEY NOT NULL CHECK (length(trim(id)) > 0),
    novel_id TEXT NOT NULL,
    title TEXT NOT NULL CHECK (length(trim(title)) > 0),
    sort_order INTEGER NOT NULL CHECK (sort_order >= 0),
    UNIQUE (novel_id, sort_order),
    FOREIGN KEY (novel_id)
        REFERENCES novels(id)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
) STRICT;

CREATE TABLE scenes (
    id TEXT PRIMARY KEY NOT NULL CHECK (length(trim(id)) > 0),
    chapter_id TEXT NOT NULL,
    title TEXT NOT NULL CHECK (length(trim(title)) > 0),
    sort_order INTEGER NOT NULL CHECK (sort_order >= 0),
    UNIQUE (chapter_id, sort_order),
    FOREIGN KEY (chapter_id)
        REFERENCES chapters(id)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
) STRICT;

CREATE TRIGGER universes_id_immutable
BEFORE UPDATE OF id ON universes
WHEN NEW.id <> OLD.id
BEGIN
    SELECT RAISE(ABORT, 'universe id is immutable');
END;

CREATE TRIGGER series_id_immutable
BEFORE UPDATE OF id ON series
WHEN NEW.id <> OLD.id
BEGIN
    SELECT RAISE(ABORT, 'series id is immutable');
END;

CREATE TRIGGER novels_id_immutable
BEFORE UPDATE OF id ON novels
WHEN NEW.id <> OLD.id
BEGIN
    SELECT RAISE(ABORT, 'novel id is immutable');
END;

CREATE TRIGGER chapters_id_immutable
BEFORE UPDATE OF id ON chapters
WHEN NEW.id <> OLD.id
BEGIN
    SELECT RAISE(ABORT, 'chapter id is immutable');
END;

CREATE TRIGGER scenes_id_immutable
BEFORE UPDATE OF id ON scenes
WHEN NEW.id <> OLD.id
BEGIN
    SELECT RAISE(ABORT, 'scene id is immutable');
END;
"#,
    },
    Migration {
        version: 3,
        name: "003_create_scene_text_revisions",
        sql: r#"
CREATE TABLE scene_text_revisions (
    id TEXT PRIMARY KEY NOT NULL CHECK (length(trim(id)) > 0),
    scene_id TEXT NOT NULL,
    revision_number INTEGER NOT NULL CHECK (revision_number > 0),
    content TEXT NOT NULL,
    created_at_utc TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    parent_revision_id TEXT,
    UNIQUE (id, scene_id),
    UNIQUE (scene_id, revision_number),
    FOREIGN KEY (scene_id)
        REFERENCES scenes(id)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT,
    FOREIGN KEY (parent_revision_id, scene_id)
        REFERENCES scene_text_revisions(id, scene_id)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
) STRICT;

CREATE INDEX idx_scene_text_revisions_scene
    ON scene_text_revisions(scene_id, revision_number);

CREATE INDEX idx_scene_text_revisions_parent
    ON scene_text_revisions(parent_revision_id, scene_id)
    WHERE parent_revision_id IS NOT NULL;

CREATE TABLE scene_revision_heads (
    scene_id TEXT PRIMARY KEY NOT NULL,
    revision_id TEXT NOT NULL UNIQUE,
    FOREIGN KEY (scene_id)
        REFERENCES scenes(id)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT,
    FOREIGN KEY (revision_id, scene_id)
        REFERENCES scene_text_revisions(id, scene_id)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
) STRICT;

CREATE TRIGGER scene_text_revisions_immutable
BEFORE UPDATE ON scene_text_revisions
BEGIN
    SELECT RAISE(ABORT, 'scene text revisions are immutable');
END;

CREATE TRIGGER scene_text_revisions_no_delete
BEFORE DELETE ON scene_text_revisions
BEGIN
    SELECT RAISE(ABORT, 'scene text revisions are append-only');
END;

CREATE TRIGGER scene_revision_heads_scene_id_immutable
BEFORE UPDATE OF scene_id ON scene_revision_heads
WHEN NEW.scene_id <> OLD.scene_id
BEGIN
    SELECT RAISE(ABORT, 'scene revision head scene id is immutable');
END;
"#,
    },
    Migration {
        version: 4,
        name: "004_create_narrative_entity_registry",
        sql: r#"
-- Universe-scoped entities. Distinct entities may intentionally share a name.
-- Kind and owning Universe form immutable identity; only display name can change.
CREATE TABLE narrative_entities (
    id TEXT PRIMARY KEY NOT NULL CHECK (length(trim(id)) > 0),
    universe_id TEXT NOT NULL,
    kind TEXT NOT NULL CHECK (
        kind IN (
            'character',
            'place',
            'organization',
            'object',
            'event',
            'world_rule'
        )
    ),
    name TEXT NOT NULL CHECK (length(trim(name)) > 0),
    created_at_utc TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (id, universe_id),
    FOREIGN KEY (universe_id)
        REFERENCES universes(id)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
) STRICT;

CREATE INDEX idx_narrative_entities_universe_kind
    ON narrative_entities(universe_id, kind, id);

CREATE TABLE entity_aliases (
    id TEXT PRIMARY KEY NOT NULL CHECK (length(trim(id)) > 0),
    entity_id TEXT NOT NULL,
    universe_id TEXT NOT NULL,
    alias TEXT NOT NULL CHECK (length(trim(alias)) > 0),
    UNIQUE (entity_id, alias),
    FOREIGN KEY (entity_id, universe_id)
        REFERENCES narrative_entities(id, universe_id)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
) STRICT;

CREATE INDEX idx_entity_aliases_entity_scope
    ON entity_aliases(entity_id, universe_id);

CREATE TRIGGER narrative_entities_id_immutable
BEFORE UPDATE OF id ON narrative_entities
WHEN NEW.id <> OLD.id
BEGIN
    SELECT RAISE(ABORT, 'narrative entity id is immutable');
END;

CREATE TRIGGER narrative_entities_identity_immutable
BEFORE UPDATE OF universe_id, kind ON narrative_entities
WHEN NEW.universe_id <> OLD.universe_id OR NEW.kind <> OLD.kind
BEGIN
    SELECT RAISE(ABORT, 'narrative entity ownership and kind are immutable');
END;

CREATE TRIGGER entity_aliases_id_immutable
BEFORE UPDATE OF id ON entity_aliases
WHEN NEW.id <> OLD.id
BEGIN
    SELECT RAISE(ABORT, 'entity alias id is immutable');
END;

CREATE TRIGGER entity_aliases_ownership_immutable
BEFORE UPDATE OF entity_id, universe_id ON entity_aliases
WHEN NEW.entity_id <> OLD.entity_id OR NEW.universe_id <> OLD.universe_id
BEGIN
    SELECT RAISE(ABORT, 'entity alias ownership is immutable');
END;
"#,
    },

];

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

    crate::backup::resolve_active_database_path(&app_data_dir)
        .map_err(|error| DatabaseError::Path(error.to_string()))
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

    fn migrated_memory_connection() -> Connection {
        let mut connection = memory_connection();
        run_migrations(&mut connection).expect("migrations");
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

    fn insert_universe(connection: &Connection, id: &str) {
        connection
            .execute(
                "INSERT INTO universes (id, name) VALUES (?1, ?2)",
                params![id, format!("Universe {id}")],
            )
            .expect("insert universe");
    }

    fn insert_series(connection: &Connection, id: &str, universe_id: &str, order: i64) {
        connection
            .execute(
                "INSERT INTO series (id, universe_id, name, sort_order) VALUES (?1, ?2, ?3, ?4)",
                params![id, universe_id, format!("Series {id}"), order],
            )
            .expect("insert series");
    }

    fn insert_novel(
        connection: &Connection,
        id: &str,
        universe_id: &str,
        series_id: Option<&str>,
        order: i64,
    ) {
        connection
            .execute(
                "INSERT INTO novels (id, universe_id, series_id, title, sort_order)
                 VALUES (?1, ?2, ?3, ?4, ?5)",
                params![id, universe_id, series_id, format!("Novel {id}"), order],
            )
            .expect("insert novel");
    }

    fn insert_chapter(connection: &Connection, id: &str, novel_id: &str, order: i64) {
        connection
            .execute(
                "INSERT INTO chapters (id, novel_id, title, sort_order) VALUES (?1, ?2, ?3, ?4)",
                params![id, novel_id, format!("Chapter {id}"), order],
            )
            .expect("insert chapter");
    }

    fn insert_scene(connection: &Connection, id: &str, chapter_id: &str, order: i64) {
        connection
            .execute(
                "INSERT INTO scenes (id, chapter_id, title, sort_order) VALUES (?1, ?2, ?3, ?4)",
                params![id, chapter_id, format!("Scene {id}"), order],
            )
            .expect("insert scene");
    }

    #[test]
    fn fresh_database_creates_and_applies_migrations_once() {
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

            assert_eq!(migration_count, 4);

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

        assert_eq!(migration_count, 4);
    }

    #[test]
    fn schema_v1_migrates_to_current_schema() {
        let mut connection = memory_connection();

        ensure_migration_table(&connection).expect("migration table");
        apply_migration(&mut connection, MIGRATIONS[0]).expect("migration v1");

        assert_eq!(
            current_schema_version(&connection).expect("schema version v1"),
            1
        );

        let migrated = run_migrations(&mut connection).expect("migrate to current schema");

        assert_eq!(migrated, 4);

        let hierarchy_table_count: i64 = connection
            .query_row(
                "SELECT COUNT(*) FROM sqlite_master
                 WHERE type = 'table'
                   AND name IN ('universes', 'series', 'novels', 'chapters', 'scenes')",
                [],
                |row| row.get(0),
            )
            .expect("hierarchy table count");

        assert_eq!(hierarchy_table_count, 5);
    }

    #[test]
    fn schema_v2_migrates_to_v3_with_revision_foundation() {
        let mut connection = memory_connection();

        ensure_migration_table(&connection).expect("migration table");
        apply_migration(&mut connection, MIGRATIONS[0]).expect("migration v1");
        apply_migration(&mut connection, MIGRATIONS[1]).expect("migration v2");

        assert_eq!(
            current_schema_version(&connection).expect("schema version v2"),
            2
        );

        let migrated = run_migrations(&mut connection).expect("migrate to v3");
        assert_eq!(migrated, 4);

        let revision_tables: i64 = connection
            .query_row(
                "SELECT COUNT(*) FROM pragma_table_list
                 WHERE name IN ('scene_text_revisions', 'scene_revision_heads')
                   AND strict = 1",
                [],
                |row| row.get(0),
            )
            .expect("revision tables");

        assert_eq!(revision_tables, 2);

        let trigger_count: i64 = connection
            .query_row(
                "SELECT COUNT(*) FROM sqlite_master
                 WHERE type = 'trigger'
                   AND name IN (
                     'scene_text_revisions_immutable',
                     'scene_text_revisions_no_delete',
                     'scene_revision_heads_scene_id_immutable'
                   )",
                [],
                |row| row.get(0),
            )
            .expect("revision trigger count");

        assert_eq!(trigger_count, 3);
    }

    #[test]
    fn revision_schema_enforces_append_only_history_and_same_scene_head() {
        let connection = migrated_memory_connection();

        insert_universe(&connection, "u1");
        insert_novel(&connection, "n1", "u1", None, 0);
        insert_chapter(&connection, "c1", "n1", 0);
        insert_scene(&connection, "sc1", "c1", 0);
        insert_scene(&connection, "sc2", "c1", 1);

        connection
            .execute(
                "INSERT INTO scene_text_revisions
                 (id, scene_id, revision_number, content)
                 VALUES ('r1', 'sc1', 1, 'Version one')",
                [],
            )
            .expect("insert revision");

        let cross_scene_head = connection.execute(
            "INSERT INTO scene_revision_heads (scene_id, revision_id)
             VALUES ('sc2', 'r1')",
            [],
        );
        assert!(
            cross_scene_head.is_err(),
            "head must point to a revision from the same scene"
        );

        connection
            .execute(
                "INSERT INTO scene_revision_heads (scene_id, revision_id)
                 VALUES ('sc1', 'r1')",
                [],
            )
            .expect("insert valid head");

        assert!(
            connection
                .execute(
                    "UPDATE scene_text_revisions SET content = 'mutated' WHERE id = 'r1'",
                    [],
                )
                .is_err(),
            "saved revisions must be immutable"
        );

        assert!(
            connection
                .execute("DELETE FROM scene_text_revisions WHERE id = 'r1'", [])
                .is_err(),
            "saved revisions must be append-only"
        );
    }

    #[test]
    fn schema_v3_migrates_to_v4_without_losing_revision_history() {
        let mut connection = memory_connection();
        ensure_migration_table(&connection).expect("migration table");

        for migration in &MIGRATIONS[..3] {
            apply_migration(&mut connection, *migration).expect("apply pre-v4 migration");
        }
        assert_eq!(current_schema_version(&connection).expect("v3"), 3);

        insert_universe(&connection, "u1");
        insert_novel(&connection, "n1", "u1", None, 0);
        insert_chapter(&connection, "c1", "n1", 0);
        insert_scene(&connection, "sc1", "c1", 0);

        for (id, number, parent, content) in [
            ("r1", 1, None, "Début"),
            ("r2", 2, Some("r1"), "Suite"),
            ("r3", 3, Some("r1"), "Nouvelle variante"),
        ] {
            connection
                .execute(
                    "INSERT INTO scene_text_revisions
                     (id, scene_id, revision_number, content, parent_revision_id)
                     VALUES (?1, 'sc1', ?2, ?3, ?4)",
                    params![id, number, content, parent],
                )
                .expect("insert pre-v4 text revision");
        }
        connection
            .execute(
                "INSERT INTO scene_revision_heads (scene_id, revision_id)
                 VALUES ('sc1', 'r3')",
                [],
            )
            .expect("current revision head");

        assert_eq!(run_migrations(&mut connection).expect("v4 upgrade"), 4);
        assert_eq!(run_migrations(&mut connection).expect("idempotent rerun"), 4);

        let migration_count: i64 = connection
            .query_row("SELECT COUNT(*) FROM schema_migrations", [], |row| row.get(0))
            .expect("migration count");
        assert_eq!(migration_count, 4);

        let revision_count: i64 = connection
            .query_row(
                "SELECT COUNT(*) FROM scene_text_revisions WHERE scene_id = 'sc1'",
                [],
                |row| row.get(0),
            )
            .expect("revision count");
        assert_eq!(revision_count, 3);

        let head: String = connection
            .query_row(
                "SELECT revision_id FROM scene_revision_heads WHERE scene_id = 'sc1'",
                [],
                |row| row.get(0),
            )
            .expect("current head");
        assert_eq!(head, "r3");

        let quoted: String = connection
            .query_row(
                "SELECT content FROM scene_text_revisions WHERE id = 'r1'",
                [],
                |row| row.get(0),
            )
            .expect("immutable original text");
        assert_eq!(quoted, "Début");

        let strict_count: i64 = connection
            .query_row(
                "SELECT COUNT(*) FROM pragma_table_list
                 WHERE name IN ('narrative_entities', 'entity_aliases') AND strict = 1",
                [],
                |row| row.get(0),
            )
            .expect("strict registry");
        assert_eq!(strict_count, 2);

        let failures: i64 = connection
            .query_row("SELECT COUNT(*) FROM pragma_foreign_key_check", [], |row| row.get(0))
            .expect("foreign-key check");
        assert_eq!(failures, 0);
        let integrity: String = connection
            .query_row("PRAGMA integrity_check", [], |row| row.get(0))
            .expect("integrity");
        assert_eq!(integrity, "ok");
    }

    #[test]
    fn entity_registry_accepts_six_kinds_and_duplicate_names() {
        let connection = migrated_memory_connection();
        insert_universe(&connection, "u1");
        insert_universe(&connection, "u2");

        let kinds = [
            "character",
            "place",
            "organization",
            "object",
            "event",
            "world_rule",
        ];

        for (index, kind) in kinds.iter().enumerate() {
            connection
                .execute(
                    "INSERT INTO narrative_entities (id, universe_id, kind, name)
                     VALUES (?1, 'u1', ?2, 'Same display name')",
                    params![format!("e{index}"), kind],
                )
                .expect("supported kind");
        }

        connection
            .execute(
                "INSERT INTO narrative_entities (id, universe_id, kind, name)
                 VALUES ('elsewhere', 'u2', 'character', 'Same display name')",
                [],
            )
            .expect("name duplicates across universes are allowed");

        let count: i64 = connection
            .query_row("SELECT COUNT(*) FROM narrative_entities", [], |row| row.get(0))
            .expect("entity count");
        assert_eq!(count, 7);

        assert!(
            connection
                .execute(
                    "INSERT INTO narrative_entities (id, universe_id, kind, name)
                     VALUES ('invalid', 'u1', 'creature', 'Unknown kind')",
                    [],
                )
                .is_err()
        );
        assert!(
            connection
                .execute(
                    "INSERT INTO narrative_entities (id, universe_id, kind, name)
                     VALUES ('blank', 'u1', 'character', '  ')",
                    [],
                )
                .is_err()
        );
        assert!(
            connection
                .execute(
                    "INSERT INTO narrative_entities (id, universe_id, kind, name)
                     VALUES ('missing', 'no-universe', 'place', 'Orphan')",
                    [],
                )
                .is_err()
        );

        connection
            .execute(
                "UPDATE narrative_entities SET name = 'New display name' WHERE id = 'e0'",
                [],
            )
            .expect("rename preserves entity identity");

        for sql in [
            "UPDATE narrative_entities SET id = 'new-id' WHERE id = 'e0'",
            "UPDATE narrative_entities SET universe_id = 'u2' WHERE id = 'e0'",
            "UPDATE narrative_entities SET kind = 'place' WHERE id = 'e0'",
        ] {
            assert!(connection.execute(sql, []).is_err(), "{sql}");
        }

        assert!(
            connection
                .execute("DELETE FROM universes WHERE id = 'u1'", [])
                .is_err(),
            "universe with entities must be restricted"
        );
    }

    #[test]
    fn aliases_have_distinct_immutable_identity_and_strict_owner() {
        let connection = migrated_memory_connection();
        insert_universe(&connection, "u1");
        insert_universe(&connection, "u2");

        connection
            .execute(
                "INSERT INTO narrative_entities (id, universe_id, kind, name)
                 VALUES ('e1', 'u1', 'character', 'Elise')",
                [],
            )
            .expect("first character");
        connection
            .execute(
                "INSERT INTO narrative_entities (id, universe_id, kind, name)
                 VALUES ('e2', 'u2', 'character', 'Elise')",
                [],
            )
            .expect("second character");

        connection
            .execute(
                "INSERT INTO entity_aliases (id, entity_id, universe_id, alias)
                 VALUES ('a1', 'e1', 'u1', 'Éli')",
                [],
            )
            .expect("alias");

        connection
            .execute(
                "INSERT INTO entity_aliases (id, entity_id, universe_id, alias)
                 VALUES ('a2', 'e2', 'u2', 'Éli')",
                [],
            )
            .expect("same alias may exist in other universe");

        for sql in [
            "INSERT INTO entity_aliases (id, entity_id, universe_id, alias) VALUES ('a3', 'e1', 'u1', 'Éli')",
            "INSERT INTO entity_aliases (id, entity_id, universe_id, alias) VALUES ('a3', 'e1', 'u2', 'Mismatch')",
            "INSERT INTO entity_aliases (id, entity_id, universe_id, alias) VALUES ('a3', 'missing', 'u1', 'Orphan')",
            "INSERT INTO entity_aliases (id, entity_id, universe_id, alias) VALUES ('a3', 'e1', 'u1', '   ')",
            "UPDATE entity_aliases SET id = 'new' WHERE id = 'a1'",
            "UPDATE entity_aliases SET entity_id = 'e2' WHERE id = 'a1'",
            "UPDATE entity_aliases SET universe_id = 'u2' WHERE id = 'a1'",
        ] {
            assert!(connection.execute(sql, []).is_err(), "{sql}");
        }

        connection
            .execute(
                "UPDATE entity_aliases SET alias = 'Elly' WHERE id = 'a1'",
                [],
            )
            .expect("editable alias text");

        assert!(
            connection
                .execute("DELETE FROM narrative_entities WHERE id = 'e1'", [])
                .is_err(),
            "entity with aliases cannot be deleted"
        );
    }

    #[test]
    fn entity_registry_transaction_failure_rolls_back_all_changes() {
        let mut connection = migrated_memory_connection();
        insert_universe(&connection, "u1");

        let result = with_transaction(&mut connection, |transaction| {
            transaction.execute(
                "INSERT INTO narrative_entities (id, universe_id, kind, name)
                 VALUES ('e1', 'u1', 'character', 'Name')",
                [],
            )?;
            transaction.execute(
                "INSERT INTO entity_aliases (id, entity_id, universe_id, alias)
                 VALUES ('bad', 'e1', 'unknown', 'Invalid owner')",
                [],
            )?;
            Ok(())
        });

        assert!(result.is_err(), "composite operation must fail");
        let count: i64 = connection
            .query_row("SELECT COUNT(*) FROM narrative_entities", [], |row| row.get(0))
            .expect("entity count");
        assert_eq!(count, 0, "failed transaction cannot leave a partial entity");
    }

    #[test]
    fn v4_fresh_schema_has_expected_immutable_triggers_and_indexes() {
        let connection = migrated_memory_connection();
        let trigger_count: i64 = connection
            .query_row(
                "SELECT COUNT(*) FROM sqlite_master
                 WHERE type='trigger' AND name IN (
                   'narrative_entities_id_immutable',
                   'narrative_entities_identity_immutable',
                   'entity_aliases_id_immutable',
                   'entity_aliases_ownership_immutable'
                 )",
                [],
                |row| row.get(0),
            )
            .expect("registry triggers");
        assert_eq!(trigger_count, 4);

        let index_count: i64 = connection
            .query_row(
                "SELECT COUNT(*) FROM sqlite_master
                 WHERE type='index' AND name IN (
                   'idx_narrative_entities_universe_kind',
                   'idx_entity_aliases_entity_scope'
                 )",
                [],
                |row| row.get(0),
            )
            .expect("registry indexes");
        assert_eq!(index_count, 2);

        assert!(foreign_keys_enabled(&connection).expect("foreign keys"));
    }

    #[test]
    fn valid_hierarchy_accepts_series_and_standalone_novels() {
        let connection = migrated_memory_connection();

        insert_universe(&connection, "u1");
        insert_series(&connection, "s1", "u1", 0);
        insert_novel(&connection, "n-standalone", "u1", None, 0);
        insert_novel(&connection, "n-series", "u1", Some("s1"), 0);
        insert_chapter(&connection, "c1", "n-series", 0);
        insert_chapter(&connection, "c2", "n-series", 1);
        insert_scene(&connection, "sc1", "c1", 0);

        let scene_count: i64 = connection
            .query_row("SELECT COUNT(*) FROM scenes", [], |row| row.get(0))
            .expect("scene count");

        assert_eq!(scene_count, 1);
    }

    #[test]
    fn novel_cannot_reference_series_from_another_universe() {
        let connection = migrated_memory_connection();

        insert_universe(&connection, "u1");
        insert_universe(&connection, "u2");
        insert_series(&connection, "s1", "u1", 0);

        let result = connection.execute(
            "INSERT INTO novels (id, universe_id, series_id, title, sort_order)
             VALUES ('n1', 'u2', 's1', 'Cross-universe novel', 0)",
            [],
        );

        assert!(
            result.is_err(),
            "a novel must not reference a series from another universe"
        );
    }

    #[test]
    fn deterministic_ordering_is_unique_within_each_parent() {
        let connection = migrated_memory_connection();

        insert_universe(&connection, "u1");
        insert_series(&connection, "s1", "u1", 0);

        let duplicate_series_order = connection.execute(
            "INSERT INTO series (id, universe_id, name, sort_order)
             VALUES ('s2', 'u1', 'Series 2', 0)",
            [],
        );
        assert!(duplicate_series_order.is_err());

        insert_novel(&connection, "n1", "u1", Some("s1"), 0);
        let duplicate_novel_order = connection.execute(
            "INSERT INTO novels (id, universe_id, series_id, title, sort_order)
             VALUES ('n2', 'u1', 's1', 'Novel 2', 0)",
            [],
        );
        assert!(duplicate_novel_order.is_err());

        insert_chapter(&connection, "c1", "n1", 0);
        let duplicate_chapter_order = connection.execute(
            "INSERT INTO chapters (id, novel_id, title, sort_order)
             VALUES ('c2', 'n1', 'Chapter 2', 0)",
            [],
        );
        assert!(duplicate_chapter_order.is_err());

        insert_scene(&connection, "sc1", "c1", 0);
        let duplicate_scene_order = connection.execute(
            "INSERT INTO scenes (id, chapter_id, title, sort_order)
             VALUES ('sc2', 'c1', 'Scene 2', 0)",
            [],
        );
        assert!(duplicate_scene_order.is_err());
    }

    #[test]
    fn orphaned_hierarchy_references_are_rejected() {
        let connection = migrated_memory_connection();

        let orphan_series = connection.execute(
            "INSERT INTO series (id, universe_id, name, sort_order)
             VALUES ('s1', 'missing', 'Orphan series', 0)",
            [],
        );
        assert!(orphan_series.is_err());

        let orphan_chapter = connection.execute(
            "INSERT INTO chapters (id, novel_id, title, sort_order)
             VALUES ('c1', 'missing', 'Orphan chapter', 0)",
            [],
        );
        assert!(orphan_chapter.is_err());

        let orphan_scene = connection.execute(
            "INSERT INTO scenes (id, chapter_id, title, sort_order)
             VALUES ('sc1', 'missing', 'Orphan scene', 0)",
            [],
        );
        assert!(orphan_scene.is_err());
    }

    #[test]
    fn project_hierarchy_ids_are_immutable() {
        let connection = migrated_memory_connection();

        insert_universe(&connection, "u1");
        insert_series(&connection, "s1", "u1", 0);
        insert_novel(&connection, "n1", "u1", Some("s1"), 0);
        insert_chapter(&connection, "c1", "n1", 0);
        insert_scene(&connection, "sc1", "c1", 0);

        let updates = [
            "UPDATE universes SET id = 'u2' WHERE id = 'u1'",
            "UPDATE series SET id = 's2' WHERE id = 's1'",
            "UPDATE novels SET id = 'n2' WHERE id = 'n1'",
            "UPDATE chapters SET id = 'c2' WHERE id = 'c1'",
            "UPDATE scenes SET id = 'sc2' WHERE id = 'sc1'",
        ];

        for update in updates {
            assert!(
                connection.execute(update, []).is_err(),
                "hierarchy id update must be rejected: {update}"
            );
        }
    }

    #[test]
    fn project_hierarchy_has_no_foreign_key_violations() {
        let connection = migrated_memory_connection();

        insert_universe(&connection, "u1");
        insert_series(&connection, "s1", "u1", 0);
        insert_novel(&connection, "n1", "u1", Some("s1"), 0);
        insert_chapter(&connection, "c1", "n1", 0);
        insert_scene(&connection, "sc1", "c1", 0);

        let mut statement = connection
            .prepare("PRAGMA foreign_key_check")
            .expect("foreign key check statement");
        let mut rows = statement.query([]).expect("foreign key check");

        assert!(
            rows.next().expect("foreign key check result").is_none(),
            "foreign key check must return no violations"
        );
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
