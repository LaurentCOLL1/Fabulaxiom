use crate::{database, review::{
    self, ReviewError, ReviewErrorPayload, ReviewFactInput, ReviewHistory,
    ReviewHistoryInput, ReviewSnapshot, ReviewUniverseInput,
}};

fn with_connection<T, F>(
    app: &tauri::AppHandle, operation: F,
) -> Result<T, ReviewErrorPayload>
where
    F: FnOnce(&mut rusqlite::Connection) -> Result<T, ReviewError>,
{
    let path = database::database_path(app).map_err(|_| ReviewErrorPayload {
        code: "database",
        message: "Impossible de résoudre la base locale active.".to_owned(),
    })?;
    let mut db = database::open_database(&path).map_err(|_| ReviewErrorPayload {
        code: "database",
        message: "Impossible d'ouvrir la base SQLite de revue.".to_owned(),
    })?;
    operation(&mut db).map_err(|error| error.payload())
}

#[tauri::command]
pub fn review_fact_history(
    app: tauri::AppHandle, input: ReviewHistoryInput,
) -> Result<ReviewHistory, ReviewErrorPayload> {
    with_connection(&app, |db| review::history(db, &input.fact_id, &input.universe_id))
}

#[tauri::command]
pub fn fact_review_snapshot(
    app: tauri::AppHandle, input: ReviewUniverseInput,
) -> Result<ReviewSnapshot, ReviewErrorPayload> {
    with_connection(&app, |db| review::snapshot(db, &input.universe_id))
}

/// Explicit operator-initiated command. This does not authenticate the declared
/// reviewer identity or infer human approval from Ollama/AI metadata.
#[tauri::command]
pub fn review_narrative_fact(
    app: tauri::AppHandle, input: ReviewFactInput,
) -> Result<ReviewHistory, ReviewErrorPayload> {
    with_connection(&app, |db| review::review(db, input))
}
