use serde::Deserialize;
use tauri::Manager;

use crate::{
    database,
    revisions::{
        self, CreateSceneRevisionInput, RevisionError, RevisionErrorPayload, SceneRevisionHistory,
        SceneTextRevision, SetCurrentSceneRevisionInput, SetSceneRevisionArchivedInput,
    },
};

#[derive(Debug, Clone, Deserialize)]
pub struct SceneRevisionHistoryInput {
    pub scene_id: String,
}

const GREENFIELD_IDENTIFIER: &str = "com.fabulaxiom.greenfield.v1";

fn is_greenfield_identifier(identifier: &str) -> bool {
    identifier == GREENFIELD_IDENTIFIER
}

fn require_greenfield(app: &tauri::AppHandle) -> Result<(), RevisionErrorPayload> {
    if is_greenfield_identifier(&app.config().identifier) {
        Ok(())
    } else {
        Err(RevisionError::GreenfieldOnly.payload())
    }
}

/// Identity-only check: no database is opened in any profile.
#[tauri::command]
pub fn greenfield_revision_archive_enabled(app: tauri::AppHandle) -> bool {
    is_greenfield_identifier(&app.config().identifier)
}

/// Fail closed before opening any SQLite connection in non-Greenfield profiles.
#[tauri::command]
pub fn scene_archived_revision_ids(
    app: tauri::AppHandle,
    input: SceneRevisionHistoryInput,
) -> Result<Vec<String>, RevisionErrorPayload> {
    require_greenfield(&app)?;
    with_connection(&app, |connection| {
        revisions::scene_archived_revision_ids(connection, &input.scene_id)
    })
}

#[tauri::command]
pub fn set_scene_revision_archived(
    app: tauri::AppHandle,
    input: SetSceneRevisionArchivedInput,
) -> Result<Vec<String>, RevisionErrorPayload> {
    require_greenfield(&app)?;
    with_connection(&app, |connection| {
        revisions::set_scene_revision_archived(connection, input)
    })
}

fn with_connection<T, F>(
    app: &tauri::AppHandle,
    operation: F,
) -> Result<T, RevisionErrorPayload>
where
    F: FnOnce(&mut rusqlite::Connection) -> Result<T, RevisionError>,
{
    let path = database::database_path(app)
        .map_err(|error| RevisionError::Database(error.to_string()).payload())?;
    let mut connection = database::open_database(&path)
        .map_err(|error| RevisionError::Database(error.to_string()).payload())?;

    operation(&mut connection).map_err(RevisionErrorPayload::from)
}

#[tauri::command]
pub fn scene_revision_history(
    app: tauri::AppHandle,
    input: SceneRevisionHistoryInput,
) -> Result<SceneRevisionHistory, RevisionErrorPayload> {
    with_connection(&app, |connection| {
        revisions::scene_revision_history(connection, &input.scene_id)
    })
}

#[tauri::command]
pub fn create_scene_text_revision(
    app: tauri::AppHandle,
    input: CreateSceneRevisionInput,
) -> Result<SceneTextRevision, RevisionErrorPayload> {
    with_connection(&app, |connection| {
        revisions::create_scene_revision(connection, input)
    })
}

#[tauri::command]
pub fn set_current_scene_revision(
    app: tauri::AppHandle,
    input: SetCurrentSceneRevisionInput,
) -> Result<SceneTextRevision, RevisionErrorPayload> {
    with_connection(&app, |connection| {
        revisions::set_current_scene_revision(connection, input)
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn archive_commands_are_identified_only_for_greenfield() {
        assert!(is_greenfield_identifier("com.fabulaxiom.greenfield.v1"));
        assert!(!is_greenfield_identifier("com.fabulaxiom.desktop"));
        assert!(!is_greenfield_identifier("com.fabulaxiom.greenfield.v1.other"));
        assert!(!is_greenfield_identifier("COM.FABULAXIOM.GREENFIELD.V1"));
    }
}
