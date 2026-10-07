use crate::{
    database,
    hierarchy::{
        self, CreateChapterInput, CreateNovelInput, CreateSceneInput, CreateSeriesInput,
        CreateUniverseInput, HierarchyError, HierarchyErrorPayload, HierarchySnapshot, IdInput,
        RenameInput, ReorderInput, SetNovelSeriesInput,
    },
};

fn with_connection<T, F>(
    app: &tauri::AppHandle,
    operation: F,
) -> Result<T, HierarchyErrorPayload>
where
    F: FnOnce(&mut rusqlite::Connection) -> Result<T, HierarchyError>,
{
    let path = database::database_path(app)
        .map_err(|error| HierarchyError::Database(error.to_string()).payload())?;
    let mut connection = database::open_database(&path)
        .map_err(|error| HierarchyError::Database(error.to_string()).payload())?;

    operation(&mut connection).map_err(HierarchyErrorPayload::from)
}

#[tauri::command]
pub fn hierarchy_snapshot(
    app: tauri::AppHandle,
) -> Result<HierarchySnapshot, HierarchyErrorPayload> {
    with_connection(&app, |connection| hierarchy::snapshot(connection))
}

#[tauri::command]
pub fn create_universe(
    app: tauri::AppHandle,
    input: CreateUniverseInput,
) -> Result<hierarchy::Universe, HierarchyErrorPayload> {
    with_connection(&app, |connection| hierarchy::create_universe(connection, input))
}

#[tauri::command]
pub fn rename_universe(
    app: tauri::AppHandle,
    input: RenameInput,
) -> Result<hierarchy::Universe, HierarchyErrorPayload> {
    with_connection(&app, |connection| hierarchy::rename_universe(connection, input))
}

#[tauri::command]
pub fn delete_universe(
    app: tauri::AppHandle,
    input: IdInput,
) -> Result<(), HierarchyErrorPayload> {
    with_connection(&app, |connection| hierarchy::delete_universe(connection, input.id))
}

#[tauri::command]
pub fn create_series(
    app: tauri::AppHandle,
    input: CreateSeriesInput,
) -> Result<hierarchy::Series, HierarchyErrorPayload> {
    with_connection(&app, |connection| hierarchy::create_series(connection, input))
}

#[tauri::command]
pub fn rename_series(
    app: tauri::AppHandle,
    input: RenameInput,
) -> Result<hierarchy::Series, HierarchyErrorPayload> {
    with_connection(&app, |connection| hierarchy::rename_series(connection, input))
}

#[tauri::command]
pub fn reorder_series(
    app: tauri::AppHandle,
    input: ReorderInput,
) -> Result<Vec<hierarchy::Series>, HierarchyErrorPayload> {
    with_connection(&app, |connection| hierarchy::reorder_series(connection, input))
}

#[tauri::command]
pub fn delete_series(
    app: tauri::AppHandle,
    input: IdInput,
) -> Result<(), HierarchyErrorPayload> {
    with_connection(&app, |connection| hierarchy::delete_series(connection, input.id))
}

#[tauri::command]
pub fn create_novel(
    app: tauri::AppHandle,
    input: CreateNovelInput,
) -> Result<hierarchy::Novel, HierarchyErrorPayload> {
    with_connection(&app, |connection| hierarchy::create_novel(connection, input))
}

#[tauri::command]
pub fn rename_novel(
    app: tauri::AppHandle,
    input: RenameInput,
) -> Result<hierarchy::Novel, HierarchyErrorPayload> {
    with_connection(&app, |connection| hierarchy::rename_novel(connection, input))
}

#[tauri::command]
pub fn set_novel_series(
    app: tauri::AppHandle,
    input: SetNovelSeriesInput,
) -> Result<hierarchy::Novel, HierarchyErrorPayload> {
    with_connection(&app, |connection| hierarchy::set_novel_series(connection, input))
}

#[tauri::command]
pub fn reorder_novel(
    app: tauri::AppHandle,
    input: ReorderInput,
) -> Result<Vec<hierarchy::Novel>, HierarchyErrorPayload> {
    with_connection(&app, |connection| hierarchy::reorder_novel(connection, input))
}

#[tauri::command]
pub fn delete_novel(
    app: tauri::AppHandle,
    input: IdInput,
) -> Result<(), HierarchyErrorPayload> {
    with_connection(&app, |connection| hierarchy::delete_novel(connection, input.id))
}

#[tauri::command]
pub fn create_chapter(
    app: tauri::AppHandle,
    input: CreateChapterInput,
) -> Result<hierarchy::Chapter, HierarchyErrorPayload> {
    with_connection(&app, |connection| hierarchy::create_chapter(connection, input))
}

#[tauri::command]
pub fn rename_chapter(
    app: tauri::AppHandle,
    input: RenameInput,
) -> Result<hierarchy::Chapter, HierarchyErrorPayload> {
    with_connection(&app, |connection| hierarchy::rename_chapter(connection, input))
}

#[tauri::command]
pub fn reorder_chapter(
    app: tauri::AppHandle,
    input: ReorderInput,
) -> Result<Vec<hierarchy::Chapter>, HierarchyErrorPayload> {
    with_connection(&app, |connection| hierarchy::reorder_chapter(connection, input))
}

#[tauri::command]
pub fn delete_chapter(
    app: tauri::AppHandle,
    input: IdInput,
) -> Result<(), HierarchyErrorPayload> {
    with_connection(&app, |connection| hierarchy::delete_chapter(connection, input.id))
}

#[tauri::command]
pub fn create_scene(
    app: tauri::AppHandle,
    input: CreateSceneInput,
) -> Result<hierarchy::Scene, HierarchyErrorPayload> {
    with_connection(&app, |connection| hierarchy::create_scene(connection, input))
}

#[tauri::command]
pub fn rename_scene(
    app: tauri::AppHandle,
    input: RenameInput,
) -> Result<hierarchy::Scene, HierarchyErrorPayload> {
    with_connection(&app, |connection| hierarchy::rename_scene(connection, input))
}

#[tauri::command]
pub fn reorder_scene(
    app: tauri::AppHandle,
    input: ReorderInput,
) -> Result<Vec<hierarchy::Scene>, HierarchyErrorPayload> {
    with_connection(&app, |connection| hierarchy::reorder_scene(connection, input))
}

#[tauri::command]
pub fn delete_scene(
    app: tauri::AppHandle,
    input: IdInput,
) -> Result<(), HierarchyErrorPayload> {
    with_connection(&app, |connection| hierarchy::delete_scene(connection, input.id))
}
