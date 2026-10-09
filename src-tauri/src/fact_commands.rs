use crate::{database, facts::{self, CreateFactInput, FactError, FactErrorPayload, FactRecord, FactSnapshot, FactUniverseInput}};

fn with_connection<T,F>(
    app: &tauri::AppHandle, operation: F,
) -> Result<T,FactErrorPayload>
where F: FnOnce(&mut rusqlite::Connection)->Result<T,FactError> {
    let path=database::database_path(app).map_err(|_| FactErrorPayload{
        code:"database",message:"Impossible de résoudre la base active.".to_owned()
    })?;
    let mut db=database::open_database(&path).map_err(|_| FactErrorPayload{
        code:"database",message:"Impossible d'ouvrir la base SQLite.".to_owned()
    })?;
    operation(&mut db).map_err(|error|error.payload())
}

#[tauri::command]
pub fn facts_snapshot(
    app: tauri::AppHandle, input: FactUniverseInput,
)->Result<FactSnapshot,FactErrorPayload>{
    with_connection(&app,|db|facts::snapshot(db,&input.universe_id))
}

#[tauri::command]
pub fn create_narrative_fact(
    app: tauri::AppHandle, input: CreateFactInput,
)->Result<FactRecord,FactErrorPayload>{
    with_connection(&app,|db|facts::create_fact(db,input))
}
