use serde::Deserialize;

use crate::{
    database,
    revisions::{
        self, CreateSceneRevisionInput, RevisionError, RevisionErrorPayload, SceneRevisionHistory,
        SceneTextRevision, SetCurrentSceneRevisionInput,
    },
};

#[derive(Debug, Clone, Deserialize)]
pub struct SceneRevisionHistoryInput {
    pub scene_id: String,
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
