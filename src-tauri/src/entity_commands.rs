use crate::{
    database,
    entity::{
        self, CreateAliasInput, CreateEntityInput, EntityError, EntityErrorPayload, EntitySnapshot,
        IdInput, RenameAliasInput, RenameEntityInput, UniverseInput,
    },
};

fn with_connection<T, F>(
    app: &tauri::AppHandle,
    operation: F,
) -> Result<T, EntityErrorPayload>
where
    F: FnOnce(&mut rusqlite::Connection) -> Result<T, EntityError>,
{
    let path = database::database_path(app).map_err(|error| EntityErrorPayload {
        code: "database",
        message: format!("Base locale indisponible : {error}"),
    })?;
    let mut db = database::open_database(&path).map_err(|_| EntityErrorPayload {
        code: "database",
        message: "Impossible d'ouvrir la base SQLite.".to_string(),
    })?;
    operation(&mut db).map_err(|error| error.payload())
}

#[tauri::command]
pub fn entity_snapshot(
    app: tauri::AppHandle,
    input: UniverseInput,
) -> Result<EntitySnapshot, EntityErrorPayload> {
    with_connection(&app, |db| entity::snapshot(db, &input.universe_id))
}

#[tauri::command]
pub fn create_narrative_entity(
    app: tauri::AppHandle,
    input: CreateEntityInput,
) -> Result<entity::NarrativeEntity, EntityErrorPayload> {
    with_connection(&app, |db| entity::create_entity(db, input))
}

#[tauri::command]
pub fn rename_narrative_entity(
    app: tauri::AppHandle,
    input: RenameEntityInput,
) -> Result<entity::NarrativeEntity, EntityErrorPayload> {
    with_connection(&app, |db| entity::rename_entity(db, input))
}

#[tauri::command]
pub fn delete_narrative_entity(
    app: tauri::AppHandle,
    input: IdInput,
) -> Result<(), EntityErrorPayload> {
    with_connection(&app, |db| entity::delete_entity(db, &input.id))
}

#[tauri::command]
pub fn create_entity_alias(
    app: tauri::AppHandle,
    input: CreateAliasInput,
) -> Result<entity::EntityAlias, EntityErrorPayload> {
    with_connection(&app, |db| entity::create_alias(db, input))
}

#[tauri::command]
pub fn rename_entity_alias(
    app: tauri::AppHandle,
    input: RenameAliasInput,
) -> Result<entity::EntityAlias, EntityErrorPayload> {
    with_connection(&app, |db| entity::rename_alias(db, input))
}

#[tauri::command]
pub fn delete_entity_alias(
    app: tauri::AppHandle,
    input: IdInput,
) -> Result<(), EntityErrorPayload> {
    with_connection(&app, |db| entity::delete_alias(db, &input.id))
}
