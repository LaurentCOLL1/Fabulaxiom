use rusqlite::{params, Connection, OptionalExtension, Row, Transaction};
use serde::{Deserialize, Serialize};
use std::fmt;

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct SceneTextRevision {
    pub id: String,
    pub scene_id: String,
    pub revision_number: i64,
    pub content: String,
    pub created_at_utc: String,
    pub parent_revision_id: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct SceneRevisionHistory {
    pub scene_id: String,
    pub current_revision_id: Option<String>,
    pub revisions: Vec<SceneTextRevision>,
}

#[derive(Debug, Clone, Deserialize, PartialEq, Eq)]
pub struct CreateSceneRevisionInput {
    pub id: String,
    pub scene_id: String,
    pub content: String,
}

#[derive(Debug, Clone, Deserialize, PartialEq, Eq)]
pub struct SetCurrentSceneRevisionInput {
    pub scene_id: String,
    pub revision_id: String,
}

#[derive(Debug, Clone, Deserialize, PartialEq, Eq)]
pub struct SetSceneRevisionArchivedInput {
    pub scene_id: String,
    pub revision_id: String,
    pub archived: bool,
}

// Stored in the existing v1 metadata table. Never modify or delete a revision.
const ARCHIVE_KEY_PREFIX: &str = "greenfield_revision_archive:";

#[derive(Debug, Clone, Serialize, PartialEq, Eq)]
pub struct RevisionErrorPayload {
    pub code: &'static str,
    pub message: String,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum RevisionError {
    NotFound(&'static str),
    Validation(String),
    CrossSceneRevision,
    GreenfieldOnly,
    Database(String),
}

impl RevisionError {
    pub fn payload(&self) -> RevisionErrorPayload {
        match self {
            Self::NotFound(entity) => RevisionErrorPayload {
                code: "not_found",
                message: format!("{entity} introuvable."),
            },
            Self::Validation(message) => RevisionErrorPayload {
                code: "validation",
                message: message.clone(),
            },
            Self::CrossSceneRevision => RevisionErrorPayload {
                code: "cross_scene_revision",
                message: "La révision sélectionnée appartient à une autre scène.".to_string(),
            },
            Self::GreenfieldOnly => RevisionErrorPayload {
                code: "greenfield_only",
                message: "L'archivage est réservé au profil PROJETS NEUFS.".to_string(),
            },
            Self::Database(_) => RevisionErrorPayload {
                code: "database",
                message: "La base locale n'a pas pu effectuer l'opération de révision.".to_string(),
            },
        }
    }
}

impl From<RevisionError> for RevisionErrorPayload {
    fn from(error: RevisionError) -> Self {
        error.payload()
    }
}

impl fmt::Display for RevisionError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        let payload = self.payload();
        write!(formatter, "{}: {}", payload.code, payload.message)
    }
}

impl std::error::Error for RevisionError {}

fn database_error(error: rusqlite::Error) -> RevisionError {
    RevisionError::Database(error.to_string())
}

fn required_id(value: String, field: &str) -> Result<String, RevisionError> {
    let normalized = value.trim().to_string();
    if normalized.is_empty() {
        return Err(RevisionError::Validation(format!(
            "{field} ne peut pas être vide."
        )));
    }
    Ok(normalized)
}

fn scene_exists(connection: &Connection, scene_id: &str) -> Result<bool, RevisionError> {
    let exists: i64 = connection
        .query_row(
            "SELECT EXISTS(SELECT 1 FROM scenes WHERE id = ?1)",
            params![scene_id],
            |row| row.get(0),
        )
        .map_err(database_error)?;
    Ok(exists == 1)
}

fn revision_exists(connection: &Connection, revision_id: &str) -> Result<bool, RevisionError> {
    let exists: i64 = connection
        .query_row(
            "SELECT EXISTS(SELECT 1 FROM scene_text_revisions WHERE id = ?1)",
            params![revision_id],
            |row| row.get(0),
        )
        .map_err(database_error)?;
    Ok(exists == 1)
}

fn ensure_scene(connection: &Connection, scene_id: &str) -> Result<(), RevisionError> {
    if !scene_exists(connection, scene_id)? {
        return Err(RevisionError::NotFound("Scène"));
    }
    Ok(())
}

fn revision_from_row(row: &Row<'_>) -> rusqlite::Result<SceneTextRevision> {
    Ok(SceneTextRevision {
        id: row.get(0)?,
        scene_id: row.get(1)?,
        revision_number: row.get(2)?,
        content: row.get(3)?,
        created_at_utc: row.get(4)?,
        parent_revision_id: row.get(5)?,
    })
}

fn current_revision_id(
    connection: &Connection,
    scene_id: &str,
) -> Result<Option<String>, RevisionError> {
    connection
        .query_row(
            "SELECT revision_id FROM scene_revision_heads WHERE scene_id = ?1",
            params![scene_id],
            |row| row.get(0),
        )
        .optional()
        .map_err(database_error)
}

fn next_revision_number(
    connection: &Connection,
    scene_id: &str,
) -> Result<i64, RevisionError> {
    let max_number: Option<i64> = connection
        .query_row(
            "SELECT MAX(revision_number)
             FROM scene_text_revisions
             WHERE scene_id = ?1",
            params![scene_id],
            |row| row.get(0),
        )
        .map_err(database_error)?;

    max_number
        .unwrap_or(0)
        .checked_add(1)
        .ok_or_else(|| RevisionError::Database("revision number overflow".to_string()))
}

fn with_revision_transaction<T, F>(
    connection: &mut Connection,
    operation: F,
) -> Result<T, RevisionError>
where
    F: FnOnce(&Transaction<'_>) -> Result<T, RevisionError>,
{
    let transaction = connection.transaction().map_err(database_error)?;
    let result = operation(&transaction)?;
    transaction.commit().map_err(database_error)?;
    Ok(result)
}

pub fn get_revision(
    connection: &Connection,
    revision_id: &str,
) -> Result<SceneTextRevision, RevisionError> {
    connection
        .query_row(
            "SELECT id, scene_id, revision_number, content, created_at_utc, parent_revision_id
             FROM scene_text_revisions
             WHERE id = ?1",
            params![revision_id],
            revision_from_row,
        )
        .optional()
        .map_err(database_error)?
        .ok_or(RevisionError::NotFound("Révision"))
}

pub fn scene_revision_history(
    connection: &Connection,
    scene_id: &str,
) -> Result<SceneRevisionHistory, RevisionError> {
    ensure_scene(connection, scene_id)?;

    let mut statement = connection
        .prepare(
            "SELECT id, scene_id, revision_number, content, created_at_utc, parent_revision_id
             FROM scene_text_revisions
             WHERE scene_id = ?1
             ORDER BY revision_number DESC, id",
        )
        .map_err(database_error)?;

    let revisions = statement
        .query_map(params![scene_id], revision_from_row)
        .map_err(database_error)?
        .collect::<rusqlite::Result<Vec<_>>>()
        .map_err(database_error)?;

    Ok(SceneRevisionHistory {
        scene_id: scene_id.to_string(),
        current_revision_id: current_revision_id(connection, scene_id)?,
        revisions,
    })
}

pub fn create_scene_revision(
    connection: &mut Connection,
    input: CreateSceneRevisionInput,
) -> Result<SceneTextRevision, RevisionError> {
    let id = required_id(input.id, "L'identifiant de révision")?;
    let scene_id = required_id(input.scene_id, "La scène")?;
    let content = input.content;

    with_revision_transaction(connection, |transaction| {
        ensure_scene(transaction, &scene_id)?;

        if revision_exists(transaction, &id)? {
            return Err(RevisionError::Validation(
                "Une révision avec cet identifiant existe déjà.".to_string(),
            ));
        }

        let parent_revision_id = current_revision_id(transaction, &scene_id)?;
        let revision_number = next_revision_number(transaction, &scene_id)?;

        transaction
            .execute(
                "INSERT INTO scene_text_revisions
                 (id, scene_id, revision_number, content, parent_revision_id)
                 VALUES (?1, ?2, ?3, ?4, ?5)",
                params![
                    id,
                    scene_id,
                    revision_number,
                    content,
                    parent_revision_id
                ],
            )
            .map_err(database_error)?;

        let head_updated = transaction
            .execute(
                "UPDATE scene_revision_heads
                 SET revision_id = ?1
                 WHERE scene_id = ?2",
                params![id, scene_id],
            )
            .map_err(database_error)?;

        if head_updated == 0 {
            transaction
                .execute(
                    "INSERT INTO scene_revision_heads (scene_id, revision_id)
                     VALUES (?1, ?2)",
                    params![scene_id, id],
                )
                .map_err(database_error)?;
        }

        get_revision(transaction, &id)
    })
}

pub fn set_current_scene_revision(
    connection: &mut Connection,
    input: SetCurrentSceneRevisionInput,
) -> Result<SceneTextRevision, RevisionError> {
    let scene_id = required_id(input.scene_id, "La scène")?;
    let revision_id = required_id(input.revision_id, "La révision")?;

    with_revision_transaction(connection, |transaction| {
        ensure_scene(transaction, &scene_id)?;
        let revision = get_revision(transaction, &revision_id)?;

        if revision.scene_id != scene_id {
            return Err(RevisionError::CrossSceneRevision);
        }

        let head_updated = transaction
            .execute(
                "UPDATE scene_revision_heads
                 SET revision_id = ?1
                 WHERE scene_id = ?2",
                params![revision_id, scene_id],
            )
            .map_err(database_error)?;

        if head_updated == 0 {
            transaction
                .execute(
                    "INSERT INTO scene_revision_heads (scene_id, revision_id)
                     VALUES (?1, ?2)",
                    params![scene_id, revision_id],
                )
                .map_err(database_error)?;
        }

        Ok(revision)
    })
}

/// Return only visibility preferences for this scene. The revision history remains complete.
pub fn scene_archived_revision_ids(
    connection: &Connection,
    scene_id: &str,
) -> Result<Vec<String>, RevisionError> {
    ensure_scene(connection, scene_id)?;
    let mut statement = connection
        .prepare(
            "SELECT r.id FROM scene_text_revisions r
             JOIN app_metadata m ON m.key = ?2 || r.id AND m.value = '1'
             WHERE r.scene_id = ?1 ORDER BY r.revision_number DESC",
        )
        .map_err(database_error)?;
    let rows = statement
        .query_map(params![scene_id, ARCHIVE_KEY_PREFIX], |row| row.get(0))
        .map_err(database_error)?;
    let archived = rows
        .collect::<rusqlite::Result<Vec<String>>>()
        .map_err(database_error)?;
    Ok(archived)
}

/// Hide/unhide a *non-current* revision by changing only the existing metadata table.
/// The immutable text, provenance, review and source anchors are never changed.
pub fn set_scene_revision_archived(
    connection: &mut Connection,
    input: SetSceneRevisionArchivedInput,
) -> Result<Vec<String>, RevisionError> {
    let scene_id = required_id(input.scene_id, "La scène")?;
    let revision_id = required_id(input.revision_id, "La révision")?;
    with_revision_transaction(connection, |transaction| {
        ensure_scene(transaction, &scene_id)?;
        let revision = get_revision(transaction, &revision_id)?;
        if revision.scene_id != scene_id {
            return Err(RevisionError::CrossSceneRevision);
        }
        if input.archived
            && current_revision_id(transaction, &scene_id)?.as_deref()
                == Some(revision_id.as_str())
        {
            return Err(RevisionError::Validation(
                "La révision courante ne peut pas être archivée.".to_string(),
            ));
        }

        let key = format!("{ARCHIVE_KEY_PREFIX}{revision_id}");
        if input.archived {
            transaction
                .execute(
                    "INSERT INTO app_metadata(key, value) VALUES (?1, '1')
                     ON CONFLICT(key) DO UPDATE SET value = '1', updated_at_utc = CURRENT_TIMESTAMP",
                    params![key],
                )
                .map_err(database_error)?;
        } else {
            transaction
                .execute("DELETE FROM app_metadata WHERE key = ?1", params![key])
                .map_err(database_error)?;
        }
        scene_archived_revision_ids(transaction, &scene_id)
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
            .execute("INSERT INTO universes (id, name) VALUES ('u1', 'Universe')", [])
            .expect("universe");
        connection
            .execute(
                "INSERT INTO novels (id, universe_id, series_id, title, sort_order)
                 VALUES ('n1', 'u1', NULL, 'Novel', 0)",
                [],
            )
            .expect("novel");
        connection
            .execute(
                "INSERT INTO chapters (id, novel_id, title, sort_order)
                 VALUES ('c1', 'n1', 'Chapter', 0)",
                [],
            )
            .expect("chapter");
        connection
            .execute(
                "INSERT INTO scenes (id, chapter_id, title, sort_order)
                 VALUES ('sc1', 'c1', 'Scene one', 0),
                        ('sc2', 'c1', 'Scene two', 1)",
                [],
            )
            .expect("scenes");

        connection
    }

    fn input(id: &str, scene_id: &str, content: &str) -> CreateSceneRevisionInput {
        CreateSceneRevisionInput {
            id: id.to_string(),
            scene_id: scene_id.to_string(),
            content: content.to_string(),
        }
    }

    #[test]
    fn revision_creation_is_append_only_and_advances_current_head() {
        let mut connection = connection();

        let first =
            create_scene_revision(&mut connection, input("r1", "sc1", "Version one"))
                .expect("first revision");
        assert_eq!(first.revision_number, 1);
        assert_eq!(first.parent_revision_id, None);

        let second =
            create_scene_revision(&mut connection, input("r2", "sc1", "Version two"))
                .expect("second revision");
        assert_eq!(second.revision_number, 2);
        assert_eq!(second.parent_revision_id.as_deref(), Some("r1"));

        let history = scene_revision_history(&connection, "sc1").expect("history");
        assert_eq!(history.current_revision_id.as_deref(), Some("r2"));
        assert_eq!(
            history
                .revisions
                .iter()
                .map(|revision| revision.id.as_str())
                .collect::<Vec<_>>(),
            vec!["r2", "r1"]
        );
    }

    #[test]
    fn restoring_current_revision_preserves_newer_history() {
        let mut connection = connection();

        create_scene_revision(&mut connection, input("r1", "sc1", "Version one"))
            .expect("first");
        create_scene_revision(&mut connection, input("r2", "sc1", "Version two"))
            .expect("second");

        let restored = set_current_scene_revision(
            &mut connection,
            SetCurrentSceneRevisionInput {
                scene_id: "sc1".to_string(),
                revision_id: "r1".to_string(),
            },
        )
        .expect("restore first");

        assert_eq!(restored.id, "r1");

        let history = scene_revision_history(&connection, "sc1").expect("history");
        assert_eq!(history.current_revision_id.as_deref(), Some("r1"));
        assert_eq!(history.revisions.len(), 2);
        assert!(history.revisions.iter().any(|revision| revision.id == "r2"));

        let third =
            create_scene_revision(&mut connection, input("r3", "sc1", "Branch from version one"))
                .expect("third");
        assert_eq!(third.revision_number, 3);
        assert_eq!(third.parent_revision_id.as_deref(), Some("r1"));
    }

    #[test]
    fn current_pointer_rejects_revision_from_another_scene() {
        let mut connection = connection();

        create_scene_revision(&mut connection, input("r1", "sc1", "Scene one"))
            .expect("scene one revision");
        create_scene_revision(&mut connection, input("r2", "sc2", "Scene two"))
            .expect("scene two revision");

        let result = set_current_scene_revision(
            &mut connection,
            SetCurrentSceneRevisionInput {
                scene_id: "sc1".to_string(),
                revision_id: "r2".to_string(),
            },
        );

        assert_eq!(result, Err(RevisionError::CrossSceneRevision));
        assert_eq!(
            scene_revision_history(&connection, "sc1")
                .expect("history")
                .current_revision_id
                .as_deref(),
            Some("r1")
        );
    }

    #[test]
    fn invalid_scene_and_duplicate_revision_ids_are_rejected() {
        let mut connection = connection();

        let invalid =
            create_scene_revision(&mut connection, input("r404", "missing", "No scene"));
        assert!(matches!(invalid, Err(RevisionError::NotFound("Scène"))));

        create_scene_revision(&mut connection, input("r1", "sc1", "First")).expect("first");
        let duplicate =
            create_scene_revision(&mut connection, input("r1", "sc1", "Duplicate id"));

        assert!(matches!(duplicate, Err(RevisionError::Validation(_))));
    }

    #[test]
    fn failed_head_update_rolls_back_inserted_revision() {
        let mut connection = connection();

        create_scene_revision(&mut connection, input("r1", "sc1", "First")).expect("first");

        connection
            .execute_batch(
                r#"
CREATE TRIGGER test_abort_revision_head_update
BEFORE UPDATE OF revision_id ON scene_revision_heads
BEGIN
    SELECT RAISE(ABORT, 'forced head failure');
END;
"#,
            )
            .expect("failure trigger");

        let result =
            create_scene_revision(&mut connection, input("r2", "sc1", "Must rollback"));
        assert!(matches!(result, Err(RevisionError::Database(_))));

        assert!(
            !revision_exists(&connection, "r2").expect("r2 existence"),
            "revision insert must roll back when head update fails"
        );

        let history = scene_revision_history(&connection, "sc1").expect("history");
        assert_eq!(history.current_revision_id.as_deref(), Some("r1"));
        assert_eq!(history.revisions.len(), 1);
    }

    #[test]
    fn revision_error_payload_serialization_is_stable() {
        let payload = RevisionError::CrossSceneRevision.payload();
        let json = serde_json::to_value(payload).expect("serialize revision error");

        assert_eq!(json["code"], "cross_scene_revision");
        assert_eq!(
            json["message"],
            "La révision sélectionnée appartient à une autre scène."
        );
    }

    fn archive_input(scene_id: &str, revision_id: &str, archived: bool) -> SetSceneRevisionArchivedInput {
        SetSceneRevisionArchivedInput {
            scene_id: scene_id.to_string(),
            revision_id: revision_id.to_string(),
            archived,
        }
    }

    #[test]
    fn greenfield_archive_is_reversible_and_never_changes_revision_history() {
        let mut db = connection();
        create_scene_revision(&mut db, input("r1", "sc1", "Keep exact source text"))
            .expect("old revision");
        create_scene_revision(&mut db, input("r2", "sc1", "Current text"))
            .expect("current revision");
        let original = scene_revision_history(&db, "sc1").expect("before archive");

        assert_eq!(
            set_scene_revision_archived(&mut db, archive_input("sc1", "r1", true))
                .expect("archive"),
            vec!["r1"]
        );
        // Repeating the same request cannot add duplicates or touch immutable rows.
        assert_eq!(
            set_scene_revision_archived(&mut db, archive_input("sc1", "r1", true))
                .expect("idempotent archive"),
            vec!["r1"]
        );
        assert_eq!(scene_revision_history(&db, "sc1").unwrap(), original);
        assert_eq!(
            db.query_row("SELECT COUNT(*) FROM schema_migrations", [], |r| r.get::<_, i64>(0))
                .unwrap(),
            6,
            "archive must not add or run a migration"
        );
        assert_eq!(
            set_scene_revision_archived(&mut db, archive_input("sc1", "r1", false))
                .expect("unarchive"),
            Vec::<String>::new()
        );
        assert_eq!(scene_revision_history(&db, "sc1").unwrap(), original);
    }

    #[test]
    fn archiving_current_cross_scene_or_missing_revision_fails_without_side_effects() {
        let mut db = connection();
        create_scene_revision(&mut db, input("r1", "sc1", "Scene one"))
            .expect("first");
        create_scene_revision(&mut db, input("r2", "sc2", "Scene two"))
            .expect("second");

        let current = set_scene_revision_archived(&mut db, archive_input("sc1", "r1", true));
        assert!(matches!(current, Err(RevisionError::Validation(_))));
        let cross = set_scene_revision_archived(&mut db, archive_input("sc1", "r2", true));
        assert_eq!(cross, Err(RevisionError::CrossSceneRevision));
        let missing = set_scene_revision_archived(&mut db, archive_input("sc1", "absent", true));
        assert!(matches!(missing, Err(RevisionError::NotFound("Révision"))));
        assert!(scene_archived_revision_ids(&db, "sc1").unwrap().is_empty());
        assert!(scene_archived_revision_ids(&db, "sc2").unwrap().is_empty());
    }

    #[test]
    fn archiving_preserves_lineage_and_does_not_remove_archived_revisions_from_queries() {
        let mut db = connection();
        create_scene_revision(&mut db, input("r1", "sc1", "Fact source text"))
            .expect("first");
        create_scene_revision(&mut db, input("r2", "sc1", "Second"))
            .expect("second");
        create_scene_revision(&mut db, input("r3", "sc1", "Third"))
            .expect("third");
        set_scene_revision_archived(&mut db, archive_input("sc1", "r1", true))
            .expect("archive ancestor");
        set_scene_revision_archived(&mut db, archive_input("sc1", "r2", true))
            .expect("archive middle");
        assert_eq!(scene_archived_revision_ids(&db, "sc1").unwrap(), vec!["r2", "r1"]);

        let history = scene_revision_history(&db, "sc1").unwrap();
        assert_eq!(history.revisions.len(), 3);
        assert_eq!(history.current_revision_id.as_deref(), Some("r3"));
        assert_eq!(get_revision(&db, "r1").unwrap().content, "Fact source text");
        assert_eq!(get_revision(&db, "r3").unwrap().parent_revision_id.as_deref(), Some("r2"));

        let deleted = db.execute("DELETE FROM scene_text_revisions WHERE id='r1'", []);
        assert!(deleted.is_err(), "database-level append-only guard remains active");
    }
}
