use serde::Deserialize;
use tauri::Manager;

use crate::backup::{self, BackupError, BackupErrorPayload, BackupResult, BackupStatus, RestoreResult};

#[derive(Debug, Clone, Deserialize)]
pub struct RestoreDatabaseInput {
    pub file_name: String,
    pub confirmation: String,
}

fn app_root(app: &tauri::AppHandle) -> Result<std::path::PathBuf, BackupErrorPayload> {
    app.path()
        .app_local_data_dir()
        .map_err(|error| BackupError::Integrity(format!("Dossier applicatif inaccessible : {error}")).payload())
}

#[tauri::command]
pub fn backup_status(app: tauri::AppHandle) -> Result<BackupStatus, BackupErrorPayload> {
    let root = app_root(&app)?;
    backup::status(&root).map_err(|error| error.payload())
}

#[tauri::command]
pub fn create_database_backup(app: tauri::AppHandle) -> Result<BackupResult, BackupErrorPayload> {
    let root = app_root(&app)?;
    backup::create_backup(&root).map_err(|error| error.payload())
}

#[tauri::command]
pub fn restore_database_backup(
    app: tauri::AppHandle,
    input: RestoreDatabaseInput,
) -> Result<RestoreResult, BackupErrorPayload> {
    if input.confirmation != "RESTAURER" {
        return Err(BackupError::Validation(
            "Saisissez RESTAURER pour confirmer l'activation d'une sauvegarde.".to_string()
        ).payload());
    }
    let root = app_root(&app)?;
    backup::restore_backup(&root, &input.file_name).map_err(|error| error.payload())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn restore_command_requires_exact_confirmation_phrase() {
        let input = RestoreDatabaseInput {
            file_name: "fabulaxiom-backup-00000000000000000000000000000000-0000000001-0000000001.sqlite3".to_string(),
            confirmation: "restaurer".to_string(),
        };
        assert_ne!(input.confirmation, "RESTAURER");
    }
}
