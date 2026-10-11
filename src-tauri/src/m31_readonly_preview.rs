//! Explicit opt-in DEVELOPMENT-ONLY isolated M3.1 v7 read-only preview.
//! No application write IPC commands are registered in this build flavor.
//! Never register 007 in normal startup and never inspect production identity.

use std::{fs, path::Path};
use rusqlite::{Connection, OpenFlags};
use serde::Serialize;
use tauri::Manager;

const PREFIX: &str = "com.fabulaxiom.m31launch";
const NAMES: [&str; 7] = [
    "001_create_app_metadata",
    "002_create_project_hierarchy",
    "003_create_scene_text_revisions",
    "004_create_narrative_entity_registry",
    "005_create_narrative_fact_provenance",
    "006_create_human_fact_review_log",
    "007_create_world_time_foundation",
];

#[derive(Serialize)]
pub(crate) struct PreviewStatus {
    status: &'static str,
    identity: String,
    schema_version: Option<i64>,
    integrity_ok: bool,
    foreign_keys_ok: bool,
    strict_empty_time_tables: usize,
    write_ipc_registered: bool,
    production_migrated: bool,
    error: Option<String>,
}

pub(crate) fn identity_valid(id: &str) -> bool {
    id.strip_prefix(PREFIX).is_some_and(|suffix| {
        suffix.len() == 32 && suffix.bytes().all(|b| b.is_ascii_hexdigit()
            && !b.is_ascii_uppercase())
    })
}

pub(crate) fn validate_launch(config_id: &str, expected: &str) -> Result<(), &'static str> {
    if !identity_valid(config_id) || config_id != expected {
        return Err("isolated_preview_identifier_not_authorized");
    }
    Ok(())
}

fn checked_item(path: &Path, expect_dir: bool) -> Result<(), &'static str> {
    let metadata = fs::symlink_metadata(path).map_err(|_| "isolated_path_missing")?;
    if metadata.file_type().is_symlink() || (expect_dir && !metadata.is_dir())
        || (!expect_dir && !metadata.is_file())
    {
        return Err("isolated_path_invalid_or_redirected");
    }
    Ok(())
}

fn inspect(root: &Path, identity: &str) -> Result<PreviewStatus, &'static str> {
    if !identity_valid(identity) || root.file_name().and_then(|v| v.to_str()) != Some(identity) {
        return Err("isolated_root_identity_mismatch");
    }
    checked_item(root, true)?;
    let db_dir = root.join("database");
    checked_item(&db_dir, true)?;
    let file = db_dir.join("fabulaxiom.sqlite3");
    let manifest = root.join("preparation-manifest.json");
    checked_item(&file, false)?;
    checked_item(&manifest, false)?;
    for extra in ["-wal", "-shm", "-journal"] {
        if file.with_file_name(format!("fabulaxiom.sqlite3{extra}")).exists() {
            return Err("isolated_sqlite_sidecar_present");
        }
    }

    let body = fs::read_to_string(&manifest).map_err(|_| "manifest_read_error")?;
    let data: serde_json::Value =
        serde_json::from_str(&body).map_err(|_| "manifest_invalid_json")?;
    if data["protocol"].as_str() != Some("m3_1_isolated_v7_launch_preparation_v1")
        || data["identity"].as_str() != Some(identity)
        || data["copy_file"].as_str() != Some("database/fabulaxiom.sqlite3")
        || data["copy_schema_version"].as_i64() != Some(7)
        || data["expected_launch_behavior"].as_str() != Some("normal_v6_runtime_refuses_v7")
        || data["tauri_launched"].as_bool() != Some(false)
        || data["production_migrated"].as_bool() != Some(false)
        || data["active_pointer_modified"].as_bool() != Some(false)
    {
        return Err("isolated_preparation_manifest_invalid");
    }

    let db = Connection::open_with_flags(&file, OpenFlags::SQLITE_OPEN_READ_ONLY)
        .map_err(|_| "readonly_database_open_refused")?;
    db.pragma_update(None, "query_only", "ON")
        .map_err(|_| "readonly_query_only_refused")?;
    db.pragma_update(None, "foreign_keys", "ON")
        .map_err(|_| "readonly_foreign_keys_refused")?;
    let ledger: Vec<(i64, String)> = db
        .prepare("SELECT version,name FROM schema_migrations ORDER BY version")
        .map_err(|_| "migration_ledger_missing")?
        .query_map([], |row| Ok((row.get(0)?, row.get(1)?)))
        .map_err(|_| "migration_ledger_query_failed")?
        .collect::<rusqlite::Result<Vec<_>>>()
        .map_err(|_| "migration_ledger_invalid")?;
    if ledger.len() != 7 || ledger.iter().enumerate().any(|(i, (v, name))| {
        *v != i as i64 + 1 || name != NAMES[i]
    }) {
        return Err("isolated_v7_migrations_not_exact");
    }
    let strict: i64 = db.query_row(
        "SELECT COUNT(*) FROM pragma_table_list WHERE schema='main'
         AND name IN ('fictional_calendars','world_time_anchors','world_time_precedences')
         AND type='table' AND strict=1",
        [], |row| row.get(0),
    ).map_err(|_| "isolated_time_schema_unavailable")?;
    if strict != 3 {
        return Err("isolated_strict_tables_incomplete");
    }
    for table in ["fictional_calendars", "world_time_anchors", "world_time_precedences"] {
        let count: i64 = db.query_row(
            &format!("SELECT COUNT(*) FROM \"{table}\""), [],
            |row| row.get(0),
        ).map_err(|_| "isolated_time_table_query_failed")?;
        if count != 0 {
            return Err("isolated_time_tables_not_empty");
        }
    }
    let owner: String = db.query_row(
        "SELECT value FROM app_metadata WHERE key='schema_owner'", [],
        |row| row.get(0),
    ).map_err(|_| "isolated_schema_owner_missing")?;
    if owner != "fabulaxiom" {
        return Err("isolated_wrong_schema_owner");
    }
    let integrity: String = db.query_row(
        "PRAGMA integrity_check", [], |row| row.get(0),
    ).map_err(|_| "isolated_integrity_check_failed")?;
    let fk_count: i64 = db.query_row(
        "SELECT COUNT(*) FROM pragma_foreign_key_check", [], |row| row.get(0),
    ).map_err(|_| "isolated_foreign_key_check_failed")?;
    if integrity != "ok" || fk_count != 0 {
        return Err("isolated_integrity_or_foreign_keys_bad");
    }
    Ok(PreviewStatus {
        status: "PASS",
        identity: identity.to_owned(),
        schema_version: Some(7),
        integrity_ok: true,
        foreign_keys_ok: true,
        strict_empty_time_tables: 3,
        write_ipc_registered: false,
        production_migrated: false,
        error: None,
    })
}

#[tauri::command]
pub(crate) fn m31_readonly_preview_status(app: tauri::AppHandle) -> PreviewStatus {
    let identity = app.config().identifier.as_str();
    let answer = std::env::var("FABULAXIOM_M31_PREVIEW_ID")
        .map_err(|_| "preview_environment_ack_missing")
        .and_then(|expected| validate_launch(identity, &expected))
        .and_then(|_| {
            let root = app.path().app_local_data_dir()
                .map_err(|_| "isolated_local_directory_unavailable")?;
            inspect(&root, identity)
        });
    answer.unwrap_or_else(|reason| PreviewStatus {
        status: "FAIL",
        identity: identity.to_owned(),
        schema_version: None,
        integrity_ok: false,
        foreign_keys_ok: false,
        strict_empty_time_tables: 0,
        write_ipc_registered: false,
        production_migrated: false,
        error: Some(reason.to_string()),
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::database;
    use std::{path::PathBuf, process, time::{SystemTime, UNIX_EPOCH}};

    struct TempDir(PathBuf);
    impl TempDir {
        fn new() -> Self {
            let ns = SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_nanos();
            let parent = std::env::temp_dir().join(format!(
                "fabulaxiom-m31-v7-preview-{}-{ns}", process::id()
            ));
            fs::create_dir(&parent).unwrap();
            Self(parent)
        }
    }
    impl Drop for TempDir {
        fn drop(&mut self) { fs::remove_dir_all(&self.0).unwrap(); }
    }

    fn id() -> &'static str { "com.fabulaxiom.m31launchdb8d3278504c448084478a70ccb71cbd" }

    #[test]
    fn rejects_production_and_wrong_environment_identity() {
        assert!(!identity_valid("com.fabulaxiom.desktop"));
        assert!(identity_valid(id()));
        assert!(validate_launch(id(), id()).is_ok());
        assert!(validate_launch(id(), "com.fabulaxiom.desktop").is_err());
        assert!(validate_launch("com.fabulaxiom.desktop", id()).is_err());
        assert!(!identity_valid("com.fabulaxiom.m31launch../prod"));
    }

    #[test]
    fn never_accepts_v6_without_explicit_v7_and_manifest() {
        let temp = TempDir::new();
        let root = temp.0.join(id());
        fs::create_dir(&root).unwrap();
        fs::create_dir(root.join("database")).unwrap();
        let db = root.join("database/fabulaxiom.sqlite3");
        let conn = database::open_database(&db).unwrap();
        drop(conn);
        fs::write(root.join("preparation-manifest.json"), r#"{
          "protocol":"m3_1_isolated_v7_launch_preparation_v1",
          "identity":"com.fabulaxiom.m31launchdb8d3278504c448084478a70ccb71cbd",
          "copy_file":"database/fabulaxiom.sqlite3","copy_schema_version":7,
          "expected_launch_behavior":"normal_v6_runtime_refuses_v7",
          "tauri_launched":false,"production_migrated":false,
          "active_pointer_modified":false
        }"#).unwrap();
        let original = fs::read(&db).unwrap();
        assert!(inspect(&root, id()).is_err());
        assert_eq!(fs::read(&db).unwrap(), original);
    }

    #[test]
    fn accepts_real_candidate_v7_disposable_database_without_mutation() {
        let temp = TempDir::new();
        let root = temp.0.join(id());
        fs::create_dir(&root).unwrap();
        fs::create_dir(root.join("database")).unwrap();
        let file = root.join("database/fabulaxiom.sqlite3");
        let mut db = database::open_database(&file).unwrap();
        let tx = db.transaction().unwrap();
        tx.execute_batch(include_str!("../sql/m3_1_world_time_v7_candidate.sql")).unwrap();
        tx.execute(
            "INSERT INTO schema_migrations(version,name) VALUES (7,'007_create_world_time_foundation')",
            [],
        ).unwrap();
        tx.commit().unwrap();
        drop(db);
        fs::write(root.join("preparation-manifest.json"), r#"{
          "protocol":"m3_1_isolated_v7_launch_preparation_v1",
          "identity":"com.fabulaxiom.m31launchdb8d3278504c448084478a70ccb71cbd",
          "copy_file":"database/fabulaxiom.sqlite3","copy_schema_version":7,
          "expected_launch_behavior":"normal_v6_runtime_refuses_v7",
          "tauri_launched":false,"production_migrated":false,
          "active_pointer_modified":false
        }"#).unwrap();
        let bytes = fs::read(&file).unwrap();
        let view = inspect(&root, id()).unwrap();
        assert_eq!(view.status, "PASS");
        assert_eq!(view.schema_version, Some(7));
        assert_eq!(view.strict_empty_time_tables, 3);
        assert!(!view.write_ipc_registered);
        assert_eq!(fs::read(&file).unwrap(), bytes);
    }
}
