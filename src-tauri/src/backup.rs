use std::{
    fs::{self, File, OpenOptions},
    io::Write,
    path::{Path, PathBuf},
    sync::atomic::{AtomicU64, Ordering},
    time::{SystemTime, UNIX_EPOCH},
};

use rusqlite::{params, Connection, OpenFlags};
use serde::Serialize;

use crate::database::{self, CURRENT_SCHEMA_VERSION, DATABASE_FILENAME};

const BACKUP_PREFIX: &str = "fabulaxiom-backup-";
const RESTORED_PREFIX: &str = "fabulaxiom-restored-";
const MARKER_PREFIX: &str = "activation-";
static UNIQUE_SEQUENCE: AtomicU64 = AtomicU64::new(0);

#[derive(Debug, Clone, Serialize, PartialEq, Eq)]
pub struct BackupErrorPayload {
    pub code: &'static str,
    pub message: String,
}

#[derive(Debug)]
pub enum BackupError {
    Validation(String),
    NotFound,
    Integrity(String),
    Io(std::io::Error),
    Sqlite(rusqlite::Error),
}

impl BackupError {
    pub fn payload(&self) -> BackupErrorPayload {
        match self {
            Self::Validation(message) => BackupErrorPayload {
                code: "validation",
                message: message.clone(),
            },
            Self::NotFound => BackupErrorPayload {
                code: "not_found",
                message: "Sauvegarde introuvable.".to_string(),
            },
            Self::Integrity(message) => BackupErrorPayload {
                code: "integrity",
                message: message.clone(),
            },
            Self::Io(_) => BackupErrorPayload {
                code: "io",
                message: "Une opération sur les fichiers locaux a échoué.".to_string(),
            },
            Self::Sqlite(_) => BackupErrorPayload {
                code: "database",
                message: "Une opération SQLite a échoué.".to_string(),
            },
        }
    }
}

impl From<std::io::Error> for BackupError {
    fn from(value: std::io::Error) -> Self {
        Self::Io(value)
    }
}

impl From<rusqlite::Error> for BackupError {
    fn from(value: rusqlite::Error) -> Self {
        Self::Sqlite(value)
    }
}

impl std::fmt::Display for BackupError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let payload = self.payload();
        write!(f, "{}: {}", payload.code, payload.message)
    }
}

impl std::error::Error for BackupError {}

#[derive(Debug, Clone, Serialize, PartialEq, Eq)]
pub struct DataCounts {
    pub universes: i64,
    pub series: i64,
    pub novels: i64,
    pub chapters: i64,
    pub scenes: i64,
    pub revisions: i64,
    pub current_heads: i64,
    pub entities: i64,
    pub aliases: i64,
}

#[derive(Debug, Clone, Serialize)]
pub struct BackupEntry {
    pub file_name: String,
    pub path: String,
    pub bytes: u64,
}

#[derive(Debug, Clone, Serialize)]
pub struct BackupStatus {
    pub active_database_path: String,
    pub default_database_path: String,
    pub backup_directory: String,
    pub backups: Vec<BackupEntry>,
}

#[derive(Debug, Clone, Serialize)]
pub struct BackupResult {
    pub backup: BackupEntry,
    pub schema_version: i64,
    pub counts: DataCounts,
}

#[derive(Debug, Clone, Serialize)]
pub struct RestoreResult {
    pub previous_database_path: String,
    pub active_database_path: String,
    pub source_backup: String,
    pub schema_version: i64,
    pub counts: DataCounts,
}

fn string_path(path: &Path) -> String {
    path.to_string_lossy().into_owned()
}

fn next_token() -> Result<String, BackupError> {
    let nanos = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map_err(|_| BackupError::Integrity("Horloge système invalide.".to_string()))?
        .as_nanos();
    let sequence = UNIQUE_SEQUENCE.fetch_add(1, Ordering::SeqCst);
    Ok(format!("{nanos:032}-{:010}-{sequence:010}", std::process::id()))
}

fn accepted_token(value: &str) -> bool {
    let parts: Vec<_> = value.split('-').collect();
    parts.len() == 3
        && parts[0].len() == 32
        && parts[1].len() == 10
        && parts[2].len() == 10
        && parts.iter().all(|part| part.bytes().all(|b| b.is_ascii_digit()))
}

fn accepted_backup_file(name: &str) -> bool {
    name.strip_prefix(BACKUP_PREFIX)
        .and_then(|v| v.strip_suffix(".sqlite3"))
        .is_some_and(accepted_token)
}

fn accepted_restored_file(name: &str) -> bool {
    name.strip_prefix(RESTORED_PREFIX)
        .and_then(|v| v.strip_suffix(".sqlite3"))
        .is_some_and(accepted_token)
}

fn accepted_marker_file(name: &str) -> bool {
    name.strip_prefix(MARKER_PREFIX)
        .and_then(|v| v.strip_suffix(".active"))
        .is_some_and(accepted_token)
}

fn ensure_directory(path: &Path) -> Result<(), BackupError> {
    fs::create_dir_all(path)?;
    let metadata = fs::symlink_metadata(path)?;
    if metadata.file_type().is_symlink() || !metadata.is_dir() {
        return Err(BackupError::Validation(
            "Dossier applicatif non sécurisé.".to_string(),
        ));
    }
    Ok(())
}

fn checked_file(path: &Path) -> Result<fs::Metadata, BackupError> {
    let metadata = match fs::symlink_metadata(path) {
        Ok(metadata) => metadata,
        Err(error) if error.kind() == std::io::ErrorKind::NotFound => {
            return Err(BackupError::NotFound);
        }
        Err(error) => return Err(BackupError::Io(error)),
    };
    if metadata.file_type().is_symlink() || !metadata.is_file() {
        return Err(BackupError::Validation(
            "Lien symbolique ou fichier non régulier refusé.".to_string(),
        ));
    }
    Ok(metadata)
}

fn backup_directory(root: &Path) -> PathBuf {
    root.join("backups")
}

fn database_directory(root: &Path) -> PathBuf {
    root.join("database")
}

fn activation_directory(root: &Path) -> PathBuf {
    database_directory(root).join("activations")
}

/// Read-only pointer resolution. No file is removed or overwritten by this operation.
pub fn resolve_active_database_path(root: &Path) -> Result<PathBuf, BackupError> {
    let default = database_directory(root).join(DATABASE_FILENAME);
    let activation = activation_directory(root);
    if !activation.exists() {
        return Ok(default);
    }
    let metadata = fs::symlink_metadata(&activation)?;
    if metadata.file_type().is_symlink() || !metadata.is_dir() {
        return Err(BackupError::Integrity("Dossier d'activation invalide.".to_string()));
    }

    let mut markers = Vec::new();
    for item in fs::read_dir(&activation)? {
        let item = item?;
        let name = item.file_name().to_string_lossy().into_owned();
        if accepted_marker_file(&name) {
            markers.push((name, item.path()));
        }
    }
    markers.sort_unstable_by(|left, right| right.0.cmp(&left.0));
    let Some((_, path)) = markers.into_iter().next() else {
        return Ok(default);
    };
    checked_file(&path).map_err(|_| {
        BackupError::Integrity("Marqueur d'activation endommagé.".to_string())
    })?;

    let name = fs::read_to_string(&path)?;
    let name = name.trim();
    if !accepted_restored_file(name) {
        return Err(BackupError::Integrity(
            "Nom de base restaurée invalide dans le marqueur.".to_string(),
        ));
    }
    let restored = database_directory(root).join(name);
    checked_file(&restored).map_err(|_| {
        BackupError::Integrity("Base restaurée active introuvable.".to_string())
    })?;
    Ok(restored)
}

fn validate_connection(connection: &Connection) -> Result<DataCounts, BackupError> {
    let integrity: String = connection.query_row("PRAGMA integrity_check", [], |r| r.get(0))?;
    if integrity != "ok" {
        return Err(BackupError::Integrity("Échec du contrôle SQLite integrity_check.".to_string()));
    }

    let foreign_key_issues = connection
        .prepare("PRAGMA foreign_key_check")?
        .query_map([], |_| Ok(()))?
        .collect::<rusqlite::Result<Vec<()>>>()?;
    if !foreign_key_issues.is_empty() {
        return Err(BackupError::Integrity(
            "Violations de clés étrangères détectées.".to_string(),
        ));
    }

    let owner: String = connection
        .query_row(
            "SELECT value FROM app_metadata WHERE key = 'schema_owner'",
            [],
            |r| r.get(0),
        )
        .map_err(|_| BackupError::Integrity("Propriétaire de la base inconnu.".to_string()))?;
    if owner != "fabulaxiom" {
        return Err(BackupError::Integrity("Base non Fabulaxiom.".to_string()));
    }
    let migrations = connection
        .prepare("SELECT version, name FROM schema_migrations ORDER BY version")?
        .query_map([], |r| Ok((r.get::<_, i64>(0)?, r.get::<_, String>(1)?)))?
        .collect::<rusqlite::Result<Vec<_>>>()?;
    let expected = [
        (1, "001_create_app_metadata"),
        (2, "002_create_project_hierarchy"),
        (3, "003_create_scene_text_revisions"),
        (4, "004_create_narrative_entity_registry"),
    ];
    // M1.5 application backups created before schema v4 remain restorable.
    // Every version and name must form an exact supported migration prefix.
    let supported_version = migrations.len() == CURRENT_SCHEMA_VERSION as usize
        || migrations.len() == (CURRENT_SCHEMA_VERSION - 1) as usize;
    if !supported_version
        || migrations.iter().zip(expected).any(|((version, name), (v, n))| *version != v || name != n)
    {
        return Err(BackupError::Integrity(
            "Version ou lineage de migrations non prise en charge.".to_string(),
        ));
    }
    let has_entity_registry = migrations.len() == CURRENT_SCHEMA_VERSION as usize;
    fn count(connection: &Connection, table: &str) -> Result<i64, BackupError> {
        // Names in this match are fixed by the application, never supplied by callers.
        let sql = match table {
            "universes" => "SELECT COUNT(*) FROM universes",
            "series" => "SELECT COUNT(*) FROM series",
            "novels" => "SELECT COUNT(*) FROM novels",
            "chapters" => "SELECT COUNT(*) FROM chapters",
            "scenes" => "SELECT COUNT(*) FROM scenes",
            "scene_text_revisions" => "SELECT COUNT(*) FROM scene_text_revisions",
            "scene_revision_heads" => "SELECT COUNT(*) FROM scene_revision_heads",
            _ => return Err(BackupError::Validation("Table invalide.".to_string())),
        };
        Ok(connection.query_row(sql, [], |r| r.get(0))?)
    }
    Ok(DataCounts {
        universes: count(connection, "universes")?,
        series: count(connection, "series")?,
        novels: count(connection, "novels")?,
        chapters: count(connection, "chapters")?,
        scenes: count(connection, "scenes")?,
        revisions: count(connection, "scene_text_revisions")?,
        current_heads: count(connection, "scene_revision_heads")?,
        entities: if has_entity_registry {
            connection.query_row("SELECT COUNT(*) FROM narrative_entities", [], |r| r.get(0))?
        } else {
            0
        },
        aliases: if has_entity_registry {
            connection.query_row("SELECT COUNT(*) FROM entity_aliases", [], |r| r.get(0))?
        } else {
            0
        },
    })
}

fn read_validated_database(path: &Path) -> Result<DataCounts, BackupError> {
    checked_file(path)?;
    // Never run automatic migrations when inspecting/restoring a backup.
    let conn = Connection::open_with_flags(path, OpenFlags::SQLITE_OPEN_READ_ONLY)?;
    validate_connection(&conn)
}

fn vacuum_copy(connection: &Connection, destination: &Path) -> Result<DataCounts, BackupError> {
    // An already existing *empty* file, reserved via create_new, is allowed by SQLite.
    let sql_path = destination
        .to_str()
        .ok_or_else(|| BackupError::Validation("Chemin de destination non UTF-8.".to_string()))?;
    connection.execute("VACUUM INTO ?1", params![sql_path])?;
    let counts = read_validated_database(destination)?;
    // Windows FlushFileBuffers requires a writable file handle.
    OpenOptions::new().write(true).open(destination)?.sync_all()?;
    Ok(counts)
}

fn reserve_unique_file(directory: &Path, prefix: &str) -> Result<(String, PathBuf), BackupError> {
    ensure_directory(directory)?;
    for _ in 0..5 {
        let file_name = format!("{prefix}{}.sqlite3", next_token()?);
        let path = directory.join(&file_name);
        match OpenOptions::new().write(true).create_new(true).open(&path) {
            Ok(file) => {
                drop(file);
                return Ok((file_name, path));
            }
            Err(err) if err.kind() == std::io::ErrorKind::AlreadyExists => {}
            Err(err) => return Err(BackupError::Io(err)),
        }
    }
    Err(BackupError::Validation(
        "Impossible de réserver un nom de fichier inédit.".to_string(),
    ))
}

/// App-owned backups only. Historical operator files outside this exact directory are untouched.
pub fn list_backups(root: &Path) -> Result<Vec<BackupEntry>, BackupError> {
    let dir = backup_directory(root);
    if !dir.exists() {
        return Ok(Vec::new());
    }
    let metadata = fs::symlink_metadata(&dir)?;
    if !metadata.is_dir() || metadata.file_type().is_symlink() {
        return Err(BackupError::Validation("Répertoire de sauvegardes invalide.".to_string()));
    }
    let mut entries = Vec::new();
    for entry in fs::read_dir(dir)? {
        let entry = entry?;
        let name = entry.file_name().to_string_lossy().into_owned();
        if !accepted_backup_file(&name) {
            continue;
        }
        let metadata = checked_file(&entry.path())?;
        entries.push(BackupEntry {
            file_name: name,
            path: string_path(&entry.path()),
            bytes: metadata.len(),
        });
    }
    entries.sort_unstable_by(|a, b| b.file_name.cmp(&a.file_name));
    Ok(entries)
}

pub fn status(root: &Path) -> Result<BackupStatus, BackupError> {
    Ok(BackupStatus {
        active_database_path: string_path(&resolve_active_database_path(root)?),
        default_database_path: string_path(&database_directory(root).join(DATABASE_FILENAME)),
        backup_directory: string_path(&backup_directory(root)),
        backups: list_backups(root)?,
    })
}

pub fn create_backup(root: &Path) -> Result<BackupResult, BackupError> {
    let source_path = resolve_active_database_path(root)?;
    let connection = database::open_database(&source_path)
        .map_err(|err| BackupError::Integrity(format!("Source SQLite inaccessible : {err}")))?;
    validate_connection(&connection)?;

    let (name, destination) = reserve_unique_file(&backup_directory(root), BACKUP_PREFIX)?;
    let result = vacuum_copy(&connection, &destination);
    match result {
        Ok(counts) => {
            let bytes = checked_file(&destination)?.len();
            Ok(BackupResult {
                backup: BackupEntry {
                    file_name: name,
                    path: string_path(&destination),
                    bytes,
                },
                schema_version: CURRENT_SCHEMA_VERSION,
                counts,
            })
        }
        Err(error) => {
            // This is solely the empty or partial file reserved by *this invocation*.
            let _ = fs::remove_file(&destination);
            Err(error)
        }
    }
}

fn activate_new_database(root: &Path, restored_file: &str) -> Result<(), BackupError> {
    if !accepted_restored_file(restored_file) {
        return Err(BackupError::Validation("Nom de restauration invalide.".to_string()));
    }
    let dir = activation_directory(root);
    ensure_directory(&dir)?;
    let token = next_token()?;
    let pending = dir.join(format!("{MARKER_PREFIX}{token}.pending"));
    let committed = dir.join(format!("{MARKER_PREFIX}{token}.active"));
    let mut file = OpenOptions::new().write(true).create_new(true).open(&pending)?;
    if let Err(error) = (|| -> std::io::Result<()> {
        file.write_all(restored_file.as_bytes())?;
        file.sync_all()?;
        Ok(())
    })() {
        drop(file);
        let _ = fs::remove_file(pending);
        return Err(BackupError::Io(error));
    }
    drop(file);
    // Commit point: the old database and all earlier activation markers stay intact.
    // Reader ignores *.pending files after a crash; no existing marker is overwritten.
    fs::rename(&pending, &committed)?;
    Ok(())
}

pub fn restore_backup(root: &Path, backup_name: &str) -> Result<RestoreResult, BackupError> {
    if !accepted_backup_file(backup_name) {
        return Err(BackupError::Validation(
            "Choisissez une sauvegarde Fabulaxiom créée dans l'application.".to_string(),
        ));
    }
    let previous = resolve_active_database_path(root)?;
    let backup_path = backup_directory(root).join(backup_name);
    // Reject links, corrupted databases, unrelated SQLite files and unsupported schema versions.
    let source_counts = read_validated_database(&backup_path)?;
    let source = Connection::open_with_flags(&backup_path, OpenFlags::SQLITE_OPEN_READ_ONLY)?;
    let source_version: i64 = source.query_row(
        "SELECT COALESCE(MAX(version), 0) FROM schema_migrations",
        [],
        |row| row.get(0),
    )?;

    let (file_name, restored) =
        reserve_unique_file(&database_directory(root), RESTORED_PREFIX)?;
    // The activation marker is deliberately not modified until this entire
    // copy/upgrade/verification sequence has succeeded.
    let copy_and_upgrade = (|| -> Result<DataCounts, BackupError> {
        let copy_counts = vacuum_copy(&source, &restored)?;
        if copy_counts != source_counts {
            return Err(BackupError::Integrity(
                "La restauration ne conserve pas tous les compteurs.".to_string(),
            ));
        }
        if source_version < CURRENT_SCHEMA_VERSION {
            // Upgrade only the fresh restored file, NEVER the original backup.
            let migrated = database::open_database(&restored)
                .map_err(|error| BackupError::Integrity(format!(
                    "Migration de la copie restaurée impossible : {error}"
                )))?;
            drop(migrated);
        }
        let verified = read_validated_database(&restored)?;
        if verified != source_counts {
            return Err(BackupError::Integrity(
                "Les données de la restauration migrée ont changé.".to_string(),
            ));
        }
        OpenOptions::new().write(true).open(&restored)?.sync_all()?;
        Ok(verified)
    })();
    let result = match copy_and_upgrade {
        Ok(result) => result,
        Err(error) => {
            // The new, still-inactive restore file is owned by this attempt.
            let _ = fs::remove_file(&restored);
            return Err(error);
        }
    };
    activate_new_database(root, &file_name)?;
    Ok(RestoreResult {
        previous_database_path: string_path(&previous),
        active_database_path: string_path(&restored),
        source_backup: backup_name.to_string(),
        schema_version: CURRENT_SCHEMA_VERSION,
        counts: result,
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::time::{SystemTime, UNIX_EPOCH};

    fn root(name: &str) -> PathBuf {
        let n = SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_nanos();
        std::env::temp_dir().join(format!("fabulaxiom-m15-{name}-{n}-{}", std::process::id()))
    }

    fn seeded(root: &Path) -> PathBuf {
        let path = resolve_active_database_path(root).unwrap();
        let connection = database::open_database(&path).unwrap();
        connection.execute("INSERT INTO universes (id,name) VALUES ('u1','Example')", []).unwrap();
        connection.execute("INSERT INTO novels (id,universe_id,title,sort_order) VALUES ('n1','u1','Book',0)", []).unwrap();
        connection.execute("INSERT INTO chapters (id,novel_id,title,sort_order) VALUES ('c1','n1','Chapter',0)", []).unwrap();
        connection.execute("INSERT INTO scenes (id,chapter_id,title,sort_order) VALUES ('s1','c1','Scene',0)", []).unwrap();
        connection.execute("INSERT INTO scene_text_revisions (id,scene_id,revision_number,content) VALUES ('r1','s1',1,'Original text')", []).unwrap();
        connection.execute("INSERT INTO scene_revision_heads (scene_id,revision_id) VALUES ('s1','r1')", []).unwrap();
        path
    }

    #[test]
    fn backup_is_consistent_and_does_not_modify_live_database() {
        let dir = root("backup");
        let live = seeded(&dir);
        let created = create_backup(&dir).unwrap();
        assert!(Path::new(&created.backup.path).exists());
        assert_eq!(created.schema_version, 4);
        assert_eq!(created.counts.revisions, 1);
        assert_eq!(created.counts.current_heads, 1);
        assert_eq!(list_backups(&dir).unwrap().len(), 1);
        let db = database::open_database(&live).unwrap();
        assert_eq!(validate_connection(&db).unwrap().revisions, 1);
        drop(db);
        fs::remove_dir_all(dir).unwrap();
    }

    #[test]
    fn v4_backup_restore_preserves_entity_registry_and_aliases() {
        let dir = root("entity-registry");
        let live = seeded(&dir);
        {
            let connection = database::open_database(&live).expect("v4 database");
            connection
                .execute(
                    "INSERT INTO narrative_entities (id, universe_id, kind, name)
                     VALUES ('entity-1', 'u1', 'character', 'Ariane')",
                    [],
                )
                .expect("entity");
            connection
                .execute(
                    "INSERT INTO entity_aliases (id, entity_id, universe_id, alias)
                     VALUES ('alias-1', 'entity-1', 'u1', 'Ari')",
                    [],
                )
                .expect("alias");
        }

        let saved = create_backup(&dir).expect("backup");
        assert_eq!(saved.schema_version, 4);
        assert_eq!(saved.counts.entities, 1);
        assert_eq!(saved.counts.aliases, 1);
        assert_eq!(saved.counts.revisions, 1);

        let restored = restore_backup(&dir, &saved.backup.file_name).expect("restore");
        assert_eq!(restored.schema_version, 4);
        assert_eq!(restored.counts.entities, 1);
        assert_eq!(restored.counts.aliases, 1);
        let active = database::open_database(Path::new(&restored.active_database_path))
            .expect("active restored");
        let alias: String = active
            .query_row(
                "SELECT alias FROM entity_aliases WHERE id = 'alias-1'",
                [],
                |row| row.get(0),
            )
            .expect("persisted alias");
        assert_eq!(alias, "Ari");
        drop(active);
        fs::remove_dir_all(dir).expect("cleanup temp fixture");
    }

    #[test]
    fn legacy_v3_backup_restores_into_new_v4_copy_without_changing_backup() {
        let dir = root("legacy-v3-to-v4");
        let live = seeded(&dir);

        {
            let connection = database::open_database(&live).expect("seeded v4");
            connection
                .execute_batch(
                    "DROP TABLE entity_aliases;
                     DROP TABLE narrative_entities;
                     DELETE FROM schema_migrations WHERE version = 4;",
                )
                .expect("prepare legacy v3 fixture");
        }

        let (backup_name, legacy_backup) =
            reserve_unique_file(&backup_directory(&dir), BACKUP_PREFIX)
                .expect("reserved legacy backup");
        {
            let connection = Connection::open_with_flags(&live, OpenFlags::SQLITE_OPEN_READ_ONLY)
                .expect("legacy v3 source");
            let destination = legacy_backup.to_str().expect("test path is UTF-8");
            connection
                .execute("VACUUM INTO ?1", params![destination])
                .expect("legacy application backup");
        }
        assert_eq!(
            read_validated_database(&legacy_backup)
                .expect("legacy backup accepted")
                .revisions,
            1
        );
        let original_bytes = fs::read(&legacy_backup).expect("legacy bytes");
        let restored = restore_backup(&dir, &backup_name).expect("safe legacy restore");

        assert_ne!(restored.active_database_path, restored.previous_database_path);
        assert_eq!(restored.schema_version, 4);
        assert_eq!(restored.counts.revisions, 1);
        assert_eq!(restored.counts.entities, 0);
        assert_eq!(restored.counts.aliases, 0);
        assert_eq!(
            resolve_active_database_path(&dir).expect("activation marker"),
            PathBuf::from(&restored.active_database_path)
        );

        let upgraded = database::open_database(Path::new(&restored.active_database_path))
            .expect("upgraded restored database");
        assert_eq!(
            database::current_schema_version(&upgraded).expect("new schema"),
            4
        );
        let head: String = upgraded
            .query_row(
                "SELECT revision_id FROM scene_revision_heads WHERE scene_id = 's1'",
                [],
                |row| row.get(0),
            )
            .expect("revision head");
        assert_eq!(head, "r1");
        drop(upgraded);

        assert_eq!(
            fs::read(&legacy_backup).expect("unchanged backup"),
            original_bytes
        );
        let old = Connection::open_with_flags(&live, OpenFlags::SQLITE_OPEN_READ_ONLY)
            .expect("old database");
        assert_eq!(
            database::current_schema_version(&old).expect("old schema unchanged"),
            3
        );
        drop(old);

        fs::remove_dir_all(dir).expect("remove isolated test fixtures");
    }

    #[test]
    fn restore_activates_new_file_and_preserves_original_and_provenance() {
        let dir = root("restore");
        let live = seeded(&dir);
        let saved = create_backup(&dir).unwrap();
        let db = database::open_database(&live).unwrap();
        db.execute("UPDATE universes SET name = 'Modified' WHERE id = 'u1'", []).unwrap();
        drop(db);

        let restored = restore_backup(&dir, &saved.backup.file_name).unwrap();
        assert_ne!(restored.active_database_path, restored.previous_database_path);
        assert_eq!(resolve_active_database_path(&dir).unwrap(), PathBuf::from(&restored.active_database_path));
        assert_eq!(restored.counts.revisions, 1);
        let active = database::open_database(&PathBuf::from(restored.active_database_path)).unwrap();
        let text: String = active.query_row("SELECT content FROM scene_text_revisions WHERE id = 'r1'", [], |r|r.get(0)).unwrap();
        let head: String = active.query_row("SELECT revision_id FROM scene_revision_heads WHERE scene_id='s1'", [], |r|r.get(0)).unwrap();
        let universe: String = active.query_row("SELECT name FROM universes WHERE id='u1'", [], |r|r.get(0)).unwrap();
        assert_eq!((text,head,universe), ("Original text".into(),"r1".into(),"Example".into()));
        let old = database::open_database(&live).unwrap();
        let original_name: String = old.query_row("SELECT name FROM universes WHERE id='u1'", [], |r|r.get(0)).unwrap();
        assert_eq!(original_name,"Modified");
        drop(active);
        drop(old);
        fs::remove_dir_all(dir).unwrap();
    }

    #[test]
    fn backup_names_are_unique_and_never_overwritten() {
        let dir = root("unique");
        seeded(&dir);
        let first = create_backup(&dir).unwrap();
        let contents_before = fs::read(&first.backup.path).unwrap();
        let second = create_backup(&dir).unwrap();
        assert_ne!(first.backup.file_name, second.backup.file_name);
        assert_eq!(fs::read(first.backup.path).unwrap(), contents_before);
        fs::remove_dir_all(dir).unwrap();
    }

    #[test]
    fn rejects_path_traversal_and_does_not_switch_active_database() {
        let dir = root("invalid-name");
        let live = seeded(&dir);
        let error = restore_backup(&dir, "../fabulaxiom.sqlite3").unwrap_err();
        assert_eq!(error.payload().code, "validation");
        assert_eq!(resolve_active_database_path(&dir).unwrap(), live);
        fs::remove_dir_all(dir).unwrap();
    }

    #[test]
    fn corrupt_backup_is_rejected_without_activation() {
        let dir = root("corrupt");
        let live = seeded(&dir);
        let created = create_backup(&dir).unwrap();
        fs::write(&created.backup.path, b"Not an SQLite database").unwrap();
        assert!(restore_backup(&dir, &created.backup.file_name).is_err());
        assert_eq!(resolve_active_database_path(&dir).unwrap(), live);
        fs::remove_dir_all(dir).unwrap();
    }

    #[test]
    fn failed_activation_keeps_old_database_active() {
        let dir = root("activation");
        let live = seeded(&dir);
        let backup = create_backup(&dir).unwrap();
        // Ensure activation-directory creation cannot succeed.
        fs::write(activation_directory(&dir), "not a directory").unwrap();
        assert!(restore_backup(&dir, &backup.backup.file_name).is_err());
        // No active marker was committed; the default database was not replaced.
        assert!(live.exists());
        fs::remove_dir_all(dir).unwrap();
    }

    #[test]
    fn payload_serialization_is_deterministic() {
        let p = BackupError::NotFound.payload();
        let value = serde_json::to_value(p).unwrap();
        assert_eq!(value["code"], "not_found");
    }
}
