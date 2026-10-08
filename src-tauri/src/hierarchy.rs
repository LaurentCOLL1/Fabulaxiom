use rusqlite::{params, Connection, OptionalExtension, Row, Transaction};
use serde::{Deserialize, Serialize};
use std::fmt;

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct Universe {
    pub id: String,
    pub name: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct Series {
    pub id: String,
    pub universe_id: String,
    pub name: String,
    pub sort_order: i64,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct Novel {
    pub id: String,
    pub universe_id: String,
    pub series_id: Option<String>,
    pub title: String,
    pub sort_order: i64,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct Chapter {
    pub id: String,
    pub novel_id: String,
    pub title: String,
    pub sort_order: i64,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct Scene {
    pub id: String,
    pub chapter_id: String,
    pub title: String,
    pub sort_order: i64,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct HierarchySnapshot {
    pub universes: Vec<Universe>,
    pub series: Vec<Series>,
    pub novels: Vec<Novel>,
    pub chapters: Vec<Chapter>,
    pub scenes: Vec<Scene>,
}

#[derive(Debug, Clone, Deserialize, PartialEq, Eq)]
pub struct CreateUniverseInput {
    pub id: String,
    pub name: String,
}

#[derive(Debug, Clone, Deserialize, PartialEq, Eq)]
pub struct CreateSeriesInput {
    pub id: String,
    pub universe_id: String,
    pub name: String,
}

#[derive(Debug, Clone, Deserialize, PartialEq, Eq)]
pub struct CreateNovelInput {
    pub id: String,
    pub universe_id: String,
    pub series_id: Option<String>,
    pub title: String,
}

#[derive(Debug, Clone, Deserialize, PartialEq, Eq)]
pub struct CreateChapterInput {
    pub id: String,
    pub novel_id: String,
    pub title: String,
}

#[derive(Debug, Clone, Deserialize, PartialEq, Eq)]
pub struct CreateSceneInput {
    pub id: String,
    pub chapter_id: String,
    pub title: String,
}

#[derive(Debug, Clone, Deserialize, PartialEq, Eq)]
pub struct RenameInput {
    pub id: String,
    pub value: String,
}

#[derive(Debug, Clone, Deserialize, PartialEq, Eq)]
pub struct IdInput {
    pub id: String,
}

#[derive(Debug, Clone, Deserialize, PartialEq, Eq)]
pub struct ReorderInput {
    pub id: String,
    pub new_index: i64,
}

#[derive(Debug, Clone, Deserialize, PartialEq, Eq)]
pub struct SetNovelSeriesInput {
    pub id: String,
    pub series_id: Option<String>,
}

#[derive(Debug, Clone, Serialize, PartialEq, Eq)]
pub struct HierarchyErrorPayload {
    pub code: &'static str,
    pub message: String,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum HierarchyError {
    NotFound(&'static str),
    Validation(String),
    HasChildren {
        entity: &'static str,
        child_count: i64,
    },
    CrossUniverseSeries,
    OrderConflict(String),
    Database(String),
}

impl HierarchyError {
    pub fn payload(&self) -> HierarchyErrorPayload {
        match self {
            Self::NotFound(entity) => HierarchyErrorPayload {
                code: "not_found",
                message: format!("{entity} introuvable."),
            },
            Self::Validation(message) => HierarchyErrorPayload {
                code: "validation",
                message: message.clone(),
            },
            Self::HasChildren {
                entity,
                child_count,
            } => HierarchyErrorPayload {
                code: "has_children",
                message: format!(
                    "Suppression refusée : {entity} possède encore {child_count} élément(s) enfant(s)."
                ),
            },
            Self::CrossUniverseSeries => HierarchyErrorPayload {
                code: "cross_universe_series",
                message: "La série sélectionnée appartient à un autre univers.".to_string(),
            },
            Self::OrderConflict(message) => HierarchyErrorPayload {
                code: "order_conflict",
                message: message.clone(),
            },
            Self::Database(_) => HierarchyErrorPayload {
                code: "database",
                message: "La base locale n'a pas pu effectuer l'opération.".to_string(),
            },
        }
    }
}

impl From<HierarchyError> for HierarchyErrorPayload {
    fn from(error: HierarchyError) -> Self {
        error.payload()
    }
}

impl fmt::Display for HierarchyError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        let payload = self.payload();
        write!(formatter, "{}: {}", payload.code, payload.message)
    }
}

impl std::error::Error for HierarchyError {}

fn database_error(error: rusqlite::Error) -> HierarchyError {
    HierarchyError::Database(error.to_string())
}

fn required_text(value: String, field: &str) -> Result<String, HierarchyError> {
    let normalized = value.trim().to_string();
    if normalized.is_empty() {
        return Err(HierarchyError::Validation(format!(
            "{field} ne peut pas être vide."
        )));
    }
    Ok(normalized)
}

fn optional_id(value: Option<String>) -> Option<String> {
    value.and_then(|value| {
        let normalized = value.trim().to_string();
        (!normalized.is_empty()).then_some(normalized)
    })
}

fn row_exists(
    connection: &Connection,
    table: &str,
    id: &str,
) -> Result<bool, HierarchyError> {
    let sql = format!("SELECT EXISTS(SELECT 1 FROM {table} WHERE id = ?1)");
    let exists: i64 = connection
        .query_row(&sql, params![id], |row| row.get(0))
        .map_err(database_error)?;
    Ok(exists == 1)
}

fn ensure_absent(
    connection: &Connection,
    table: &str,
    id: &str,
    entity: &str,
) -> Result<(), HierarchyError> {
    if row_exists(connection, table, id)? {
        return Err(HierarchyError::Validation(format!(
            "Un élément {entity} avec cet identifiant existe déjà."
        )));
    }
    Ok(())
}

fn ensure_exists(
    connection: &Connection,
    table: &str,
    id: &str,
    entity: &'static str,
) -> Result<(), HierarchyError> {
    if !row_exists(connection, table, id)? {
        return Err(HierarchyError::NotFound(entity));
    }
    Ok(())
}

fn with_service_transaction<T, F>(
    connection: &mut Connection,
    operation: F,
) -> Result<T, HierarchyError>
where
    F: FnOnce(&Transaction<'_>) -> Result<T, HierarchyError>,
{
    let transaction = connection.transaction().map_err(database_error)?;
    let result = operation(&transaction)?;
    transaction.commit().map_err(database_error)?;
    Ok(result)
}

fn move_id(ids: &mut Vec<String>, id: &str, new_index: i64) -> Result<(), HierarchyError> {
    if new_index < 0 || new_index as usize >= ids.len() {
        return Err(HierarchyError::OrderConflict(format!(
            "Position cible invalide : {new_index}."
        )));
    }

    let current_index = ids
        .iter()
        .position(|candidate| candidate == id)
        .ok_or(HierarchyError::NotFound("élément"))?;

    let target_index = new_index as usize;
    if current_index == target_index {
        return Ok(());
    }

    let moved = ids.remove(current_index);
    ids.insert(target_index, moved);
    Ok(())
}

fn safe_offset(max_order: i64, count: usize) -> Result<i64, HierarchyError> {
    max_order
        .checked_add(count as i64)
        .and_then(|value| value.checked_add(1))
        .ok_or_else(|| HierarchyError::Database("sort_order overflow".to_string()))
}

fn universe_from_row(row: &Row<'_>) -> rusqlite::Result<Universe> {
    Ok(Universe {
        id: row.get(0)?,
        name: row.get(1)?,
    })
}

fn series_from_row(row: &Row<'_>) -> rusqlite::Result<Series> {
    Ok(Series {
        id: row.get(0)?,
        universe_id: row.get(1)?,
        name: row.get(2)?,
        sort_order: row.get(3)?,
    })
}

fn novel_from_row(row: &Row<'_>) -> rusqlite::Result<Novel> {
    Ok(Novel {
        id: row.get(0)?,
        universe_id: row.get(1)?,
        series_id: row.get(2)?,
        title: row.get(3)?,
        sort_order: row.get(4)?,
    })
}

fn chapter_from_row(row: &Row<'_>) -> rusqlite::Result<Chapter> {
    Ok(Chapter {
        id: row.get(0)?,
        novel_id: row.get(1)?,
        title: row.get(2)?,
        sort_order: row.get(3)?,
    })
}

fn scene_from_row(row: &Row<'_>) -> rusqlite::Result<Scene> {
    Ok(Scene {
        id: row.get(0)?,
        chapter_id: row.get(1)?,
        title: row.get(2)?,
        sort_order: row.get(3)?,
    })
}

pub fn get_universe(connection: &Connection, id: &str) -> Result<Universe, HierarchyError> {
    connection
        .query_row(
            "SELECT id, name FROM universes WHERE id = ?1",
            params![id],
            universe_from_row,
        )
        .optional()
        .map_err(database_error)?
        .ok_or(HierarchyError::NotFound("Univers"))
}

pub fn get_series(connection: &Connection, id: &str) -> Result<Series, HierarchyError> {
    connection
        .query_row(
            "SELECT id, universe_id, name, sort_order FROM series WHERE id = ?1",
            params![id],
            series_from_row,
        )
        .optional()
        .map_err(database_error)?
        .ok_or(HierarchyError::NotFound("Série"))
}

pub fn get_novel(connection: &Connection, id: &str) -> Result<Novel, HierarchyError> {
    connection
        .query_row(
            "SELECT id, universe_id, series_id, title, sort_order FROM novels WHERE id = ?1",
            params![id],
            novel_from_row,
        )
        .optional()
        .map_err(database_error)?
        .ok_or(HierarchyError::NotFound("Roman"))
}

pub fn get_chapter(connection: &Connection, id: &str) -> Result<Chapter, HierarchyError> {
    connection
        .query_row(
            "SELECT id, novel_id, title, sort_order FROM chapters WHERE id = ?1",
            params![id],
            chapter_from_row,
        )
        .optional()
        .map_err(database_error)?
        .ok_or(HierarchyError::NotFound("Chapitre"))
}

pub fn get_scene(connection: &Connection, id: &str) -> Result<Scene, HierarchyError> {
    connection
        .query_row(
            "SELECT id, chapter_id, title, sort_order FROM scenes WHERE id = ?1",
            params![id],
            scene_from_row,
        )
        .optional()
        .map_err(database_error)?
        .ok_or(HierarchyError::NotFound("Scène"))
}

pub fn list_universes(connection: &Connection) -> Result<Vec<Universe>, HierarchyError> {
    let mut statement = connection
        .prepare("SELECT id, name FROM universes ORDER BY name COLLATE NOCASE, id")
        .map_err(database_error)?;
    statement
        .query_map([], universe_from_row)
        .map_err(database_error)?
        .collect::<rusqlite::Result<Vec<_>>>()
        .map_err(database_error)
}

pub fn list_series(
    connection: &Connection,
    universe_id: &str,
) -> Result<Vec<Series>, HierarchyError> {
    let mut statement = connection
        .prepare(
            "SELECT id, universe_id, name, sort_order
             FROM series
             WHERE universe_id = ?1
             ORDER BY sort_order, id",
        )
        .map_err(database_error)?;
    statement
        .query_map(params![universe_id], series_from_row)
        .map_err(database_error)?
        .collect::<rusqlite::Result<Vec<_>>>()
        .map_err(database_error)
}

pub fn list_novels(
    connection: &Connection,
    universe_id: &str,
) -> Result<Vec<Novel>, HierarchyError> {
    let mut statement = connection
        .prepare(
            "SELECT id, universe_id, series_id, title, sort_order
             FROM novels
             WHERE universe_id = ?1
             ORDER BY
               CASE WHEN series_id IS NULL THEN 0 ELSE 1 END,
               COALESCE(series_id, ''),
               sort_order,
               id",
        )
        .map_err(database_error)?;
    statement
        .query_map(params![universe_id], novel_from_row)
        .map_err(database_error)?
        .collect::<rusqlite::Result<Vec<_>>>()
        .map_err(database_error)
}

pub fn list_chapters(
    connection: &Connection,
    novel_id: &str,
) -> Result<Vec<Chapter>, HierarchyError> {
    let mut statement = connection
        .prepare(
            "SELECT id, novel_id, title, sort_order
             FROM chapters
             WHERE novel_id = ?1
             ORDER BY sort_order, id",
        )
        .map_err(database_error)?;
    statement
        .query_map(params![novel_id], chapter_from_row)
        .map_err(database_error)?
        .collect::<rusqlite::Result<Vec<_>>>()
        .map_err(database_error)
}

pub fn list_scenes(
    connection: &Connection,
    chapter_id: &str,
) -> Result<Vec<Scene>, HierarchyError> {
    let mut statement = connection
        .prepare(
            "SELECT id, chapter_id, title, sort_order
             FROM scenes
             WHERE chapter_id = ?1
             ORDER BY sort_order, id",
        )
        .map_err(database_error)?;
    statement
        .query_map(params![chapter_id], scene_from_row)
        .map_err(database_error)?
        .collect::<rusqlite::Result<Vec<_>>>()
        .map_err(database_error)
}

fn list_all_series(connection: &Connection) -> Result<Vec<Series>, HierarchyError> {
    let mut statement = connection
        .prepare(
            "SELECT id, universe_id, name, sort_order
             FROM series
             ORDER BY universe_id, sort_order, id",
        )
        .map_err(database_error)?;
    statement
        .query_map([], series_from_row)
        .map_err(database_error)?
        .collect::<rusqlite::Result<Vec<_>>>()
        .map_err(database_error)
}

fn list_all_novels(connection: &Connection) -> Result<Vec<Novel>, HierarchyError> {
    let mut statement = connection
        .prepare(
            "SELECT id, universe_id, series_id, title, sort_order
             FROM novels
             ORDER BY universe_id,
               CASE WHEN series_id IS NULL THEN 0 ELSE 1 END,
               COALESCE(series_id, ''),
               sort_order,
               id",
        )
        .map_err(database_error)?;
    statement
        .query_map([], novel_from_row)
        .map_err(database_error)?
        .collect::<rusqlite::Result<Vec<_>>>()
        .map_err(database_error)
}

fn list_all_chapters(connection: &Connection) -> Result<Vec<Chapter>, HierarchyError> {
    let mut statement = connection
        .prepare(
            "SELECT id, novel_id, title, sort_order
             FROM chapters
             ORDER BY novel_id, sort_order, id",
        )
        .map_err(database_error)?;
    statement
        .query_map([], chapter_from_row)
        .map_err(database_error)?
        .collect::<rusqlite::Result<Vec<_>>>()
        .map_err(database_error)
}

fn list_all_scenes(connection: &Connection) -> Result<Vec<Scene>, HierarchyError> {
    let mut statement = connection
        .prepare(
            "SELECT id, chapter_id, title, sort_order
             FROM scenes
             ORDER BY chapter_id, sort_order, id",
        )
        .map_err(database_error)?;
    statement
        .query_map([], scene_from_row)
        .map_err(database_error)?
        .collect::<rusqlite::Result<Vec<_>>>()
        .map_err(database_error)
}

pub fn snapshot(connection: &Connection) -> Result<HierarchySnapshot, HierarchyError> {
    Ok(HierarchySnapshot {
        universes: list_universes(connection)?,
        series: list_all_series(connection)?,
        novels: list_all_novels(connection)?,
        chapters: list_all_chapters(connection)?,
        scenes: list_all_scenes(connection)?,
    })
}

fn validate_series_universe(
    connection: &Connection,
    series_id: &str,
    universe_id: &str,
) -> Result<(), HierarchyError> {
    let series_universe: Option<String> = connection
        .query_row(
            "SELECT universe_id FROM series WHERE id = ?1",
            params![series_id],
            |row| row.get(0),
        )
        .optional()
        .map_err(database_error)?;

    match series_universe {
        None => Err(HierarchyError::NotFound("Série")),
        Some(owner) if owner != universe_id => Err(HierarchyError::CrossUniverseSeries),
        Some(_) => Ok(()),
    }
}

pub fn create_universe(
    connection: &mut Connection,
    input: CreateUniverseInput,
) -> Result<Universe, HierarchyError> {
    let id = required_text(input.id, "L'identifiant")?;
    let name = required_text(input.name, "Le nom")?;
    ensure_absent(connection, "universes", &id, "Universe")?;

    connection
        .execute(
            "INSERT INTO universes (id, name) VALUES (?1, ?2)",
            params![id, name],
        )
        .map_err(database_error)?;

    get_universe(connection, &id)
}

pub fn rename_universe(
    connection: &mut Connection,
    input: RenameInput,
) -> Result<Universe, HierarchyError> {
    let id = required_text(input.id, "L'identifiant")?;
    let name = required_text(input.value, "Le nom")?;
    let changed = connection
        .execute(
            "UPDATE universes SET name = ?1 WHERE id = ?2",
            params![name, id],
        )
        .map_err(database_error)?;
    if changed == 0 {
        return Err(HierarchyError::NotFound("Univers"));
    }
    get_universe(connection, &id)
}

pub fn delete_universe(connection: &mut Connection, id: String) -> Result<(), HierarchyError> {
    let id = required_text(id, "L'identifiant")?;
    with_service_transaction(connection, |transaction| {
        ensure_exists(transaction, "universes", &id, "Univers")?;
        let child_count: i64 = transaction
            .query_row(
                "SELECT
                   (SELECT COUNT(*) FROM series WHERE universe_id = ?1) +
                   (SELECT COUNT(*) FROM novels WHERE universe_id = ?1)",
                params![id],
                |row| row.get(0),
            )
            .map_err(database_error)?;
        if child_count > 0 {
            return Err(HierarchyError::HasChildren {
                entity: "l'univers",
                child_count,
            });
        }
        transaction
            .execute("DELETE FROM universes WHERE id = ?1", params![id])
            .map_err(database_error)?;
        Ok(())
    })
}

pub fn create_series(
    connection: &mut Connection,
    input: CreateSeriesInput,
) -> Result<Series, HierarchyError> {
    let id = required_text(input.id, "L'identifiant")?;
    let universe_id = required_text(input.universe_id, "L'univers")?;
    let name = required_text(input.name, "Le nom")?;

    with_service_transaction(connection, |transaction| {
        ensure_exists(transaction, "universes", &universe_id, "Univers")?;
        ensure_absent(transaction, "series", &id, "Series")?;
        let max_order: Option<i64> = transaction
            .query_row(
                "SELECT MAX(sort_order) FROM series WHERE universe_id = ?1",
                params![universe_id],
                |row| row.get(0),
            )
            .map_err(database_error)?;
        let sort_order = max_order
            .unwrap_or(-1)
            .checked_add(1)
            .ok_or_else(|| HierarchyError::Database("sort_order overflow".to_string()))?;
        transaction
            .execute(
                "INSERT INTO series (id, universe_id, name, sort_order)
                 VALUES (?1, ?2, ?3, ?4)",
                params![id, universe_id, name, sort_order],
            )
            .map_err(database_error)?;
        get_series(transaction, &id)
    })
}

pub fn rename_series(
    connection: &mut Connection,
    input: RenameInput,
) -> Result<Series, HierarchyError> {
    let id = required_text(input.id, "L'identifiant")?;
    let name = required_text(input.value, "Le nom")?;
    let changed = connection
        .execute(
            "UPDATE series SET name = ?1 WHERE id = ?2",
            params![name, id],
        )
        .map_err(database_error)?;
    if changed == 0 {
        return Err(HierarchyError::NotFound("Série"));
    }
    get_series(connection, &id)
}

pub fn delete_series(connection: &mut Connection, id: String) -> Result<(), HierarchyError> {
    let id = required_text(id, "L'identifiant")?;
    with_service_transaction(connection, |transaction| {
        ensure_exists(transaction, "series", &id, "Série")?;
        let child_count: i64 = transaction
            .query_row(
                "SELECT COUNT(*) FROM novels WHERE series_id = ?1",
                params![id],
                |row| row.get(0),
            )
            .map_err(database_error)?;
        if child_count > 0 {
            return Err(HierarchyError::HasChildren {
                entity: "la série",
                child_count,
            });
        }
        transaction
            .execute("DELETE FROM series WHERE id = ?1", params![id])
            .map_err(database_error)?;
        Ok(())
    })
}

pub fn reorder_series(
    connection: &mut Connection,
    input: ReorderInput,
) -> Result<Vec<Series>, HierarchyError> {
    let id = required_text(input.id, "L'identifiant")?;
    with_service_transaction(connection, |transaction| {
        let series = get_series(transaction, &id)?;
        let mut ids: Vec<String> = list_series(transaction, &series.universe_id)?
            .into_iter()
            .map(|item| item.id)
            .collect();
        move_id(&mut ids, &id, input.new_index)?;

        let max_order: i64 = transaction
            .query_row(
                "SELECT COALESCE(MAX(sort_order), 0) FROM series WHERE universe_id = ?1",
                params![series.universe_id],
                |row| row.get(0),
            )
            .map_err(database_error)?;
        let offset = safe_offset(max_order, ids.len())?;

        transaction
            .execute(
                "UPDATE series SET sort_order = sort_order + ?1 WHERE universe_id = ?2",
                params![offset, series.universe_id],
            )
            .map_err(database_error)?;

        for (index, item_id) in ids.iter().enumerate() {
            transaction
                .execute(
                    "UPDATE series SET sort_order = ?1 WHERE id = ?2",
                    params![index as i64, item_id],
                )
                .map_err(database_error)?;
        }

        list_series(transaction, &series.universe_id)
    })
}

pub fn create_novel(
    connection: &mut Connection,
    input: CreateNovelInput,
) -> Result<Novel, HierarchyError> {
    let id = required_text(input.id, "L'identifiant")?;
    let universe_id = required_text(input.universe_id, "L'univers")?;
    let series_id = optional_id(input.series_id);
    let title = required_text(input.title, "Le titre")?;

    with_service_transaction(connection, |transaction| {
        ensure_exists(transaction, "universes", &universe_id, "Univers")?;
        ensure_absent(transaction, "novels", &id, "Novel")?;
        if let Some(series_id) = series_id.as_deref() {
            validate_series_universe(transaction, series_id, &universe_id)?;
        }

        let max_order: Option<i64> = if let Some(series_id) = series_id.as_deref() {
            transaction
                .query_row(
                    "SELECT MAX(sort_order) FROM novels WHERE series_id = ?1",
                    params![series_id],
                    |row| row.get(0),
                )
                .map_err(database_error)?
        } else {
            transaction
                .query_row(
                    "SELECT MAX(sort_order) FROM novels
                     WHERE universe_id = ?1 AND series_id IS NULL",
                    params![universe_id],
                    |row| row.get(0),
                )
                .map_err(database_error)?
        };

        let sort_order = max_order
            .unwrap_or(-1)
            .checked_add(1)
            .ok_or_else(|| HierarchyError::Database("sort_order overflow".to_string()))?;

        transaction
            .execute(
                "INSERT INTO novels (id, universe_id, series_id, title, sort_order)
                 VALUES (?1, ?2, ?3, ?4, ?5)",
                params![id, universe_id, series_id, title, sort_order],
            )
            .map_err(database_error)?;
        get_novel(transaction, &id)
    })
}

pub fn rename_novel(
    connection: &mut Connection,
    input: RenameInput,
) -> Result<Novel, HierarchyError> {
    let id = required_text(input.id, "L'identifiant")?;
    let title = required_text(input.value, "Le titre")?;
    let changed = connection
        .execute(
            "UPDATE novels SET title = ?1 WHERE id = ?2",
            params![title, id],
        )
        .map_err(database_error)?;
    if changed == 0 {
        return Err(HierarchyError::NotFound("Roman"));
    }
    get_novel(connection, &id)
}

pub fn set_novel_series(
    connection: &mut Connection,
    input: SetNovelSeriesInput,
) -> Result<Novel, HierarchyError> {
    let id = required_text(input.id, "L'identifiant")?;
    let target_series = optional_id(input.series_id);

    with_service_transaction(connection, |transaction| {
        let novel = get_novel(transaction, &id)?;
        if novel.series_id == target_series {
            return Ok(novel);
        }

        if let Some(series_id) = target_series.as_deref() {
            validate_series_universe(transaction, series_id, &novel.universe_id)?;
        }

        let max_order: Option<i64> = if let Some(series_id) = target_series.as_deref() {
            transaction
                .query_row(
                    "SELECT MAX(sort_order) FROM novels WHERE series_id = ?1",
                    params![series_id],
                    |row| row.get(0),
                )
                .map_err(database_error)?
        } else {
            transaction
                .query_row(
                    "SELECT MAX(sort_order) FROM novels
                     WHERE universe_id = ?1 AND series_id IS NULL",
                    params![novel.universe_id],
                    |row| row.get(0),
                )
                .map_err(database_error)?
        };

        let sort_order = max_order
            .unwrap_or(-1)
            .checked_add(1)
            .ok_or_else(|| HierarchyError::Database("sort_order overflow".to_string()))?;

        transaction
            .execute(
                "UPDATE novels SET series_id = ?1, sort_order = ?2 WHERE id = ?3",
                params![target_series, sort_order, id],
            )
            .map_err(database_error)?;
        get_novel(transaction, &id)
    })
}

pub fn delete_novel(connection: &mut Connection, id: String) -> Result<(), HierarchyError> {
    let id = required_text(id, "L'identifiant")?;
    with_service_transaction(connection, |transaction| {
        ensure_exists(transaction, "novels", &id, "Roman")?;
        let child_count: i64 = transaction
            .query_row(
                "SELECT COUNT(*) FROM chapters WHERE novel_id = ?1",
                params![id],
                |row| row.get(0),
            )
            .map_err(database_error)?;
        if child_count > 0 {
            return Err(HierarchyError::HasChildren {
                entity: "le roman",
                child_count,
            });
        }
        transaction
            .execute("DELETE FROM novels WHERE id = ?1", params![id])
            .map_err(database_error)?;
        Ok(())
    })
}

pub fn reorder_novel(
    connection: &mut Connection,
    input: ReorderInput,
) -> Result<Vec<Novel>, HierarchyError> {
    let id = required_text(input.id, "L'identifiant")?;
    with_service_transaction(connection, |transaction| {
        let novel = get_novel(transaction, &id)?;
        let mut scoped = list_novels(transaction, &novel.universe_id)?
            .into_iter()
            .filter(|candidate| candidate.series_id == novel.series_id)
            .collect::<Vec<_>>();
        scoped.sort_by_key(|candidate| (candidate.sort_order, candidate.id.clone()));
        let mut ids = scoped
            .iter()
            .map(|candidate| candidate.id.clone())
            .collect::<Vec<_>>();
        move_id(&mut ids, &id, input.new_index)?;

        let max_order: i64 = if let Some(series_id) = novel.series_id.as_deref() {
            transaction
                .query_row(
                    "SELECT COALESCE(MAX(sort_order), 0) FROM novels WHERE series_id = ?1",
                    params![series_id],
                    |row| row.get(0),
                )
                .map_err(database_error)?
        } else {
            transaction
                .query_row(
                    "SELECT COALESCE(MAX(sort_order), 0) FROM novels
                     WHERE universe_id = ?1 AND series_id IS NULL",
                    params![novel.universe_id],
                    |row| row.get(0),
                )
                .map_err(database_error)?
        };
        let offset = safe_offset(max_order, ids.len())?;

        if let Some(series_id) = novel.series_id.as_deref() {
            transaction
                .execute(
                    "UPDATE novels SET sort_order = sort_order + ?1 WHERE series_id = ?2",
                    params![offset, series_id],
                )
                .map_err(database_error)?;
        } else {
            transaction
                .execute(
                    "UPDATE novels SET sort_order = sort_order + ?1
                     WHERE universe_id = ?2 AND series_id IS NULL",
                    params![offset, novel.universe_id],
                )
                .map_err(database_error)?;
        }

        for (index, item_id) in ids.iter().enumerate() {
            transaction
                .execute(
                    "UPDATE novels SET sort_order = ?1 WHERE id = ?2",
                    params![index as i64, item_id],
                )
                .map_err(database_error)?;
        }

        let mut refreshed = list_novels(transaction, &novel.universe_id)?
            .into_iter()
            .filter(|candidate| candidate.series_id == novel.series_id)
            .collect::<Vec<_>>();
        refreshed.sort_by_key(|candidate| (candidate.sort_order, candidate.id.clone()));
        Ok(refreshed)
    })
}

pub fn create_chapter(
    connection: &mut Connection,
    input: CreateChapterInput,
) -> Result<Chapter, HierarchyError> {
    let id = required_text(input.id, "L'identifiant")?;
    let novel_id = required_text(input.novel_id, "Le roman")?;
    let title = required_text(input.title, "Le titre")?;

    with_service_transaction(connection, |transaction| {
        ensure_exists(transaction, "novels", &novel_id, "Roman")?;
        ensure_absent(transaction, "chapters", &id, "Chapter")?;
        let max_order: Option<i64> = transaction
            .query_row(
                "SELECT MAX(sort_order) FROM chapters WHERE novel_id = ?1",
                params![novel_id],
                |row| row.get(0),
            )
            .map_err(database_error)?;
        let sort_order = max_order
            .unwrap_or(-1)
            .checked_add(1)
            .ok_or_else(|| HierarchyError::Database("sort_order overflow".to_string()))?;
        transaction
            .execute(
                "INSERT INTO chapters (id, novel_id, title, sort_order)
                 VALUES (?1, ?2, ?3, ?4)",
                params![id, novel_id, title, sort_order],
            )
            .map_err(database_error)?;
        get_chapter(transaction, &id)
    })
}

pub fn rename_chapter(
    connection: &mut Connection,
    input: RenameInput,
) -> Result<Chapter, HierarchyError> {
    let id = required_text(input.id, "L'identifiant")?;
    let title = required_text(input.value, "Le titre")?;
    let changed = connection
        .execute(
            "UPDATE chapters SET title = ?1 WHERE id = ?2",
            params![title, id],
        )
        .map_err(database_error)?;
    if changed == 0 {
        return Err(HierarchyError::NotFound("Chapitre"));
    }
    get_chapter(connection, &id)
}

pub fn delete_chapter(connection: &mut Connection, id: String) -> Result<(), HierarchyError> {
    let id = required_text(id, "L'identifiant")?;
    with_service_transaction(connection, |transaction| {
        ensure_exists(transaction, "chapters", &id, "Chapitre")?;
        let child_count: i64 = transaction
            .query_row(
                "SELECT COUNT(*) FROM scenes WHERE chapter_id = ?1",
                params![id],
                |row| row.get(0),
            )
            .map_err(database_error)?;
        if child_count > 0 {
            return Err(HierarchyError::HasChildren {
                entity: "le chapitre",
                child_count,
            });
        }
        transaction
            .execute("DELETE FROM chapters WHERE id = ?1", params![id])
            .map_err(database_error)?;
        Ok(())
    })
}

pub fn reorder_chapter(
    connection: &mut Connection,
    input: ReorderInput,
) -> Result<Vec<Chapter>, HierarchyError> {
    let id = required_text(input.id, "L'identifiant")?;
    with_service_transaction(connection, |transaction| {
        let chapter = get_chapter(transaction, &id)?;
        let mut ids = list_chapters(transaction, &chapter.novel_id)?
            .into_iter()
            .map(|item| item.id)
            .collect::<Vec<_>>();
        move_id(&mut ids, &id, input.new_index)?;

        let max_order: i64 = transaction
            .query_row(
                "SELECT COALESCE(MAX(sort_order), 0) FROM chapters WHERE novel_id = ?1",
                params![chapter.novel_id],
                |row| row.get(0),
            )
            .map_err(database_error)?;
        let offset = safe_offset(max_order, ids.len())?;

        transaction
            .execute(
                "UPDATE chapters SET sort_order = sort_order + ?1 WHERE novel_id = ?2",
                params![offset, chapter.novel_id],
            )
            .map_err(database_error)?;

        for (index, item_id) in ids.iter().enumerate() {
            transaction
                .execute(
                    "UPDATE chapters SET sort_order = ?1 WHERE id = ?2",
                    params![index as i64, item_id],
                )
                .map_err(database_error)?;
        }

        list_chapters(transaction, &chapter.novel_id)
    })
}

pub fn create_scene(
    connection: &mut Connection,
    input: CreateSceneInput,
) -> Result<Scene, HierarchyError> {
    let id = required_text(input.id, "L'identifiant")?;
    let chapter_id = required_text(input.chapter_id, "Le chapitre")?;
    let title = required_text(input.title, "Le titre")?;

    with_service_transaction(connection, |transaction| {
        ensure_exists(transaction, "chapters", &chapter_id, "Chapitre")?;
        ensure_absent(transaction, "scenes", &id, "Scene")?;
        let max_order: Option<i64> = transaction
            .query_row(
                "SELECT MAX(sort_order) FROM scenes WHERE chapter_id = ?1",
                params![chapter_id],
                |row| row.get(0),
            )
            .map_err(database_error)?;
        let sort_order = max_order
            .unwrap_or(-1)
            .checked_add(1)
            .ok_or_else(|| HierarchyError::Database("sort_order overflow".to_string()))?;
        transaction
            .execute(
                "INSERT INTO scenes (id, chapter_id, title, sort_order)
                 VALUES (?1, ?2, ?3, ?4)",
                params![id, chapter_id, title, sort_order],
            )
            .map_err(database_error)?;
        get_scene(transaction, &id)
    })
}

pub fn rename_scene(
    connection: &mut Connection,
    input: RenameInput,
) -> Result<Scene, HierarchyError> {
    let id = required_text(input.id, "L'identifiant")?;
    let title = required_text(input.value, "Le titre")?;
    let changed = connection
        .execute(
            "UPDATE scenes SET title = ?1 WHERE id = ?2",
            params![title, id],
        )
        .map_err(database_error)?;
    if changed == 0 {
        return Err(HierarchyError::NotFound("Scène"));
    }
    get_scene(connection, &id)
}

pub fn delete_scene(connection: &mut Connection, id: String) -> Result<(), HierarchyError> {
    let id = required_text(id, "L'identifiant")?;
    with_service_transaction(connection, |transaction| {
        ensure_exists(transaction, "scenes", &id, "Scène")?;

        let revision_count: i64 = transaction
            .query_row(
                "SELECT COUNT(*) FROM scene_text_revisions WHERE scene_id = ?1",
                params![id],
                |row| row.get(0),
            )
            .map_err(database_error)?;

        if revision_count > 0 {
            return Err(HierarchyError::HasChildren {
                entity: "la scène",
                child_count: revision_count,
            });
        }

        transaction
            .execute("DELETE FROM scenes WHERE id = ?1", params![id])
            .map_err(database_error)?;
        Ok(())
    })
}

pub fn reorder_scene(
    connection: &mut Connection,
    input: ReorderInput,
) -> Result<Vec<Scene>, HierarchyError> {
    let id = required_text(input.id, "L'identifiant")?;
    with_service_transaction(connection, |transaction| {
        let scene = get_scene(transaction, &id)?;
        let mut ids = list_scenes(transaction, &scene.chapter_id)?
            .into_iter()
            .map(|item| item.id)
            .collect::<Vec<_>>();
        move_id(&mut ids, &id, input.new_index)?;

        let max_order: i64 = transaction
            .query_row(
                "SELECT COALESCE(MAX(sort_order), 0) FROM scenes WHERE chapter_id = ?1",
                params![scene.chapter_id],
                |row| row.get(0),
            )
            .map_err(database_error)?;
        let offset = safe_offset(max_order, ids.len())?;

        transaction
            .execute(
                "UPDATE scenes SET sort_order = sort_order + ?1 WHERE chapter_id = ?2",
                params![offset, scene.chapter_id],
            )
            .map_err(database_error)?;

        for (index, item_id) in ids.iter().enumerate() {
            transaction
                .execute(
                    "UPDATE scenes SET sort_order = ?1 WHERE id = ?2",
                    params![index as i64, item_id],
                )
                .map_err(database_error)?;
        }

        list_scenes(transaction, &scene.chapter_id)
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::database::{configure_connection, run_migrations};

    fn connection() -> Connection {
        let mut connection = Connection::open_in_memory().expect("in-memory SQLite");
        configure_connection(&connection).expect("configured connection");
        run_migrations(&mut connection).expect("migrated connection");
        connection
    }

    fn universe(id: &str, name: &str) -> CreateUniverseInput {
        CreateUniverseInput {
            id: id.to_string(),
            name: name.to_string(),
        }
    }

    fn series(id: &str, universe_id: &str, name: &str) -> CreateSeriesInput {
        CreateSeriesInput {
            id: id.to_string(),
            universe_id: universe_id.to_string(),
            name: name.to_string(),
        }
    }

    fn novel(
        id: &str,
        universe_id: &str,
        series_id: Option<&str>,
        title: &str,
    ) -> CreateNovelInput {
        CreateNovelInput {
            id: id.to_string(),
            universe_id: universe_id.to_string(),
            series_id: series_id.map(str::to_string),
            title: title.to_string(),
        }
    }

    fn chapter(id: &str, novel_id: &str, title: &str) -> CreateChapterInput {
        CreateChapterInput {
            id: id.to_string(),
            novel_id: novel_id.to_string(),
            title: title.to_string(),
        }
    }

    fn scene(id: &str, chapter_id: &str, title: &str) -> CreateSceneInput {
        CreateSceneInput {
            id: id.to_string(),
            chapter_id: chapter_id.to_string(),
            title: title.to_string(),
        }
    }

    #[test]
    fn universe_crud_validates_names_and_restricts_children() {
        let mut connection = connection();

        let created = create_universe(&mut connection, universe("u1", "Universe One"))
            .expect("create universe");
        assert_eq!(get_universe(&connection, "u1").expect("read universe"), created);

        let renamed = rename_universe(
            &mut connection,
            RenameInput {
                id: "u1".to_string(),
                value: "Renamed Universe".to_string(),
            },
        )
        .expect("rename universe");
        assert_eq!(renamed.name, "Renamed Universe");

        let blank = create_universe(&mut connection, universe("u2", "   "));
        assert!(matches!(blank, Err(HierarchyError::Validation(_))));

        create_series(&mut connection, series("s1", "u1", "Series")).expect("create series");
        let guarded = delete_universe(&mut connection, "u1".to_string());
        assert!(matches!(
            guarded,
            Err(HierarchyError::HasChildren { entity: "l'univers", .. })
        ));

        delete_series(&mut connection, "s1".to_string()).expect("delete series");
        delete_universe(&mut connection, "u1".to_string()).expect("delete universe");
        assert!(matches!(
            get_universe(&connection, "u1"),
            Err(HierarchyError::NotFound("Univers"))
        ));
    }

    #[test]
    fn series_crud_reorders_and_rejects_invalid_universe() {
        let mut connection = connection();
        create_universe(&mut connection, universe("u1", "Universe")).expect("create universe");

        let invalid = create_series(&mut connection, series("missing", "u404", "Invalid"));
        assert!(matches!(
            invalid,
            Err(HierarchyError::NotFound("Univers"))
        ));

        create_series(&mut connection, series("s1", "u1", "First")).expect("create first");
        create_series(&mut connection, series("s2", "u1", "Second")).expect("create second");

        let renamed = rename_series(
            &mut connection,
            RenameInput {
                id: "s2".to_string(),
                value: "Second renamed".to_string(),
            },
        )
        .expect("rename series");
        assert_eq!(renamed.name, "Second renamed");

        let reordered = reorder_series(
            &mut connection,
            ReorderInput {
                id: "s2".to_string(),
                new_index: 0,
            },
        )
        .expect("reorder series");
        assert_eq!(
            reordered.iter().map(|item| item.id.as_str()).collect::<Vec<_>>(),
            vec!["s2", "s1"]
        );
        assert_eq!(reordered[0].sort_order, 0);
        assert_eq!(reordered[1].sort_order, 1);
    }

    #[test]
    fn novel_supports_optional_series_same_universe_move_and_child_guard() {
        let mut connection = connection();
        create_universe(&mut connection, universe("u1", "One")).expect("u1");
        create_universe(&mut connection, universe("u2", "Two")).expect("u2");
        create_series(&mut connection, series("s1", "u1", "One series")).expect("s1");
        create_series(&mut connection, series("s2", "u2", "Two series")).expect("s2");

        let standalone =
            create_novel(&mut connection, novel("n1", "u1", None, "Standalone")).expect("n1");
        assert_eq!(standalone.series_id, None);

        let in_series =
            create_novel(&mut connection, novel("n2", "u1", Some("s1"), "In series"))
                .expect("n2");
        assert_eq!(in_series.series_id.as_deref(), Some("s1"));

        let moved = set_novel_series(
            &mut connection,
            SetNovelSeriesInput {
                id: "n1".to_string(),
                series_id: Some("s1".to_string()),
            },
        )
        .expect("move to series");
        assert_eq!(moved.series_id.as_deref(), Some("s1"));

        let cross = set_novel_series(
            &mut connection,
            SetNovelSeriesInput {
                id: "n1".to_string(),
                series_id: Some("s2".to_string()),
            },
        );
        assert_eq!(cross, Err(HierarchyError::CrossUniverseSeries));

        let renamed = rename_novel(
            &mut connection,
            RenameInput {
                id: "n1".to_string(),
                value: "Renamed novel".to_string(),
            },
        )
        .expect("rename novel");
        assert_eq!(renamed.title, "Renamed novel");

        let reordered = reorder_novel(
            &mut connection,
            ReorderInput {
                id: "n1".to_string(),
                new_index: 0,
            },
        )
        .expect("reorder novels");
        assert_eq!(reordered[0].id, "n1");
        assert_eq!(reordered[1].id, "n2");

        create_chapter(&mut connection, chapter("c1", "n1", "Chapter")).expect("chapter");
        let guarded = delete_novel(&mut connection, "n1".to_string());
        assert!(matches!(
            guarded,
            Err(HierarchyError::HasChildren { entity: "le roman", .. })
        ));
        delete_chapter(&mut connection, "c1".to_string()).expect("delete chapter");
        delete_novel(&mut connection, "n1".to_string()).expect("delete novel");
    }

    #[test]
    fn chapter_crud_reorders_and_restricts_scenes() {
        let mut connection = connection();
        create_universe(&mut connection, universe("u1", "One")).expect("universe");
        create_novel(&mut connection, novel("n1", "u1", None, "Novel")).expect("novel");
        create_chapter(&mut connection, chapter("c1", "n1", "One")).expect("c1");
        create_chapter(&mut connection, chapter("c2", "n1", "Two")).expect("c2");

        let renamed = rename_chapter(
            &mut connection,
            RenameInput {
                id: "c2".to_string(),
                value: "Two renamed".to_string(),
            },
        )
        .expect("rename chapter");
        assert_eq!(renamed.title, "Two renamed");

        let reordered = reorder_chapter(
            &mut connection,
            ReorderInput {
                id: "c2".to_string(),
                new_index: 0,
            },
        )
        .expect("reorder chapters");
        assert_eq!(reordered[0].id, "c2");
        assert_eq!(reordered[1].id, "c1");

        create_scene(&mut connection, scene("sc1", "c2", "Scene")).expect("scene");
        let guarded = delete_chapter(&mut connection, "c2".to_string());
        assert!(matches!(
            guarded,
            Err(HierarchyError::HasChildren {
                entity: "le chapitre",
                ..
            })
        ));
    }

    #[test]
    fn scene_crud_reorders_and_deletes() {
        let mut connection = connection();
        create_universe(&mut connection, universe("u1", "One")).expect("universe");
        create_novel(&mut connection, novel("n1", "u1", None, "Novel")).expect("novel");
        create_chapter(&mut connection, chapter("c1", "n1", "Chapter")).expect("chapter");
        create_scene(&mut connection, scene("sc1", "c1", "One")).expect("sc1");
        create_scene(&mut connection, scene("sc2", "c1", "Two")).expect("sc2");

        let renamed = rename_scene(
            &mut connection,
            RenameInput {
                id: "sc2".to_string(),
                value: "Two renamed".to_string(),
            },
        )
        .expect("rename scene");
        assert_eq!(renamed.title, "Two renamed");

        let reordered = reorder_scene(
            &mut connection,
            ReorderInput {
                id: "sc2".to_string(),
                new_index: 0,
            },
        )
        .expect("reorder scenes");
        assert_eq!(reordered[0].id, "sc2");
        assert_eq!(reordered[1].id, "sc1");

        delete_scene(&mut connection, "sc2".to_string()).expect("delete scene");
        assert!(matches!(
            get_scene(&connection, "sc2"),
            Err(HierarchyError::NotFound("Scène"))
        ));
    }

    #[test]
    fn scene_with_saved_revisions_cannot_be_deleted() {
        let mut connection = connection();
        create_universe(&mut connection, universe("u1", "One")).expect("universe");
        create_novel(&mut connection, novel("n1", "u1", None, "Novel")).expect("novel");
        create_chapter(&mut connection, chapter("c1", "n1", "Chapter")).expect("chapter");
        create_scene(&mut connection, scene("sc1", "c1", "Scene")).expect("scene");

        connection
            .execute(
                "INSERT INTO scene_text_revisions
                 (id, scene_id, revision_number, content)
                 VALUES ('r1', 'sc1', 1, 'Persistent text')",
                [],
            )
            .expect("revision");

        let result = delete_scene(&mut connection, "sc1".to_string());
        assert!(matches!(
            result,
            Err(HierarchyError::HasChildren {
                entity: "la scène",
                child_count: 1
            })
        ));
        assert_eq!(get_scene(&connection, "sc1").expect("scene remains").id, "sc1");
    }

    #[test]
    fn composed_mutation_rolls_back_completely_on_failure() {
        let mut connection = connection();
        create_universe(&mut connection, universe("u1", "One")).expect("universe");
        create_series(&mut connection, series("s1", "u1", "Original")).expect("series");

        let result: Result<(), HierarchyError> =
            with_service_transaction(&mut connection, |transaction| {
                transaction
                    .execute(
                        "UPDATE series SET name = 'Changed' WHERE id = 's1'",
                        [],
                    )
                    .map_err(database_error)?;
                Err(HierarchyError::Validation(
                    "forced transaction failure".to_string(),
                ))
            });

        assert!(matches!(result, Err(HierarchyError::Validation(_))));
        assert_eq!(
            get_series(&connection, "s1").expect("series after rollback").name,
            "Original"
        );
    }

    #[test]
    fn tauri_error_payload_serialization_is_stable() {
        let payload = HierarchyError::CrossUniverseSeries.payload();
        let json = serde_json::to_value(payload).expect("serialize error payload");

        assert_eq!(json["code"], "cross_universe_series");
        assert_eq!(
            json["message"],
            "La série sélectionnée appartient à un autre univers."
        );
    }
}
