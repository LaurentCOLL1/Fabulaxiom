use rusqlite::{params, Connection, OptionalExtension, Row, Transaction};
use serde::{Deserialize, Serialize};
use std::fmt;

pub const ENTITY_KINDS: &[&str] = &[
    "character", "place", "organization", "object", "event", "world_rule",
];

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct NarrativeEntity {
    pub id: String,
    pub universe_id: String,
    pub kind: String,
    pub name: String,
    pub created_at_utc: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct EntityAlias {
    pub id: String,
    pub entity_id: String,
    pub universe_id: String,
    pub alias: String,
}

#[derive(Debug, Clone, Serialize, PartialEq, Eq)]
pub struct EntitySnapshot {
    pub entities: Vec<NarrativeEntity>,
    pub aliases: Vec<EntityAlias>,
}

#[derive(Debug, Clone, Deserialize, PartialEq, Eq)]
pub struct UniverseInput {
    pub universe_id: String,
}

#[derive(Debug, Clone, Deserialize, PartialEq, Eq)]
pub struct CreateEntityInput {
    pub id: String,
    pub universe_id: String,
    pub kind: String,
    pub name: String,
}

#[derive(Debug, Clone, Deserialize, PartialEq, Eq)]
pub struct CreateAliasInput {
    pub id: String,
    pub entity_id: String,
    pub alias: String,
}

#[derive(Debug, Clone, Deserialize, PartialEq, Eq)]
pub struct RenameEntityInput {
    pub id: String,
    pub name: String,
}

#[derive(Debug, Clone, Deserialize, PartialEq, Eq)]
pub struct RenameAliasInput {
    pub id: String,
    pub alias: String,
}

#[derive(Debug, Clone, Deserialize, PartialEq, Eq)]
pub struct IdInput {
    pub id: String,
}

#[derive(Debug, Clone, Serialize, PartialEq, Eq)]
pub struct EntityErrorPayload {
    pub code: &'static str,
    pub message: String,
}

#[derive(Debug)]
pub enum EntityError {
    NotFound(&'static str),
    Validation(String),
    HasChildren { count: i64 },
    HasFacts { count: i64 },
    Database(rusqlite::Error),
}

impl EntityError {
    pub fn payload(&self) -> EntityErrorPayload {
        match self {
            Self::NotFound(name) => EntityErrorPayload {
                code: "not_found",
                message: format!("{name} introuvable."),
            },
            Self::Validation(message) => EntityErrorPayload {
                code: "validation",
                message: message.clone(),
            },
            Self::HasChildren { count } => EntityErrorPayload {
                code: "has_children",
                message: format!(
                    "Suppression refusée : cette entité possède encore {count} alias."
                ),
            },
            Self::HasFacts { count } => EntityErrorPayload {
                code: "has_facts",
                message: format!("Suppression refusée : cette entité possède encore {count} faits."),
            },
            Self::Database(_) => EntityErrorPayload {
                code: "database",
                message: "La base locale ne peut pas effectuer cette opération.".to_string(),
            },
        }
    }
}

impl fmt::Display for EntityError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let payload = self.payload();
        write!(f, "{}: {}", payload.code, payload.message)
    }
}

impl std::error::Error for EntityError {}

impl From<rusqlite::Error> for EntityError {
    fn from(value: rusqlite::Error) -> Self {
        Self::Database(value)
    }
}

fn text(value: &str, label: &str) -> Result<String, EntityError> {
    let value = value.trim();
    if value.is_empty() {
        return Err(EntityError::Validation(format!("{label} ne peut pas être vide.")));
    }
    Ok(value.to_owned())
}

fn kind(value: &str) -> Result<String, EntityError> {
    let kind = text(value, "Le type")?;
    if !ENTITY_KINDS.contains(&kind.as_str()) {
        return Err(EntityError::Validation("Type d'entité inconnu.".to_string()));
    }
    Ok(kind)
}

fn entity_from_row(row: &Row<'_>) -> rusqlite::Result<NarrativeEntity> {
    Ok(NarrativeEntity {
        id: row.get(0)?,
        universe_id: row.get(1)?,
        kind: row.get(2)?,
        name: row.get(3)?,
        created_at_utc: row.get(4)?,
    })
}

fn alias_from_row(row: &Row<'_>) -> rusqlite::Result<EntityAlias> {
    Ok(EntityAlias {
        id: row.get(0)?,
        entity_id: row.get(1)?,
        universe_id: row.get(2)?,
        alias: row.get(3)?,
    })
}

fn universe_exists(db: &Connection, universe_id: &str) -> Result<bool, EntityError> {
    Ok(db.query_row(
        "SELECT EXISTS(SELECT 1 FROM universes WHERE id=?1)",
        params![universe_id],
        |row| row.get::<_, i64>(0),
    )? == 1)
}

pub fn get_entity(db: &Connection, id: &str) -> Result<NarrativeEntity, EntityError> {
    db.query_row(
        "SELECT id, universe_id, kind, name, created_at_utc
         FROM narrative_entities WHERE id=?1",
        params![id], entity_from_row,
    )
    .optional()?
    .ok_or(EntityError::NotFound("Entité narrative"))
}

pub fn get_alias(db: &Connection, id: &str) -> Result<EntityAlias, EntityError> {
    db.query_row(
        "SELECT id, entity_id, universe_id, alias FROM entity_aliases WHERE id=?1",
        params![id], alias_from_row,
    )
    .optional()?
    .ok_or(EntityError::NotFound("Alias"))
}

pub fn snapshot(db: &Connection, universe_id: &str) -> Result<EntitySnapshot, EntityError> {
    let universe_id = text(universe_id, "L'univers")?;
    if !universe_exists(db, &universe_id)? {
        return Err(EntityError::NotFound("Univers"));
    }
    let mut entity_stmt = db.prepare(
        "SELECT id, universe_id, kind, name, created_at_utc
         FROM narrative_entities WHERE universe_id=?1
         ORDER BY kind, name, id",
    )?;
    let entities = entity_stmt.query_map(params![universe_id], entity_from_row)?
        .collect::<rusqlite::Result<Vec<_>>>()?;
    let mut alias_stmt = db.prepare(
        "SELECT a.id, a.entity_id, a.universe_id, a.alias
         FROM entity_aliases a WHERE a.universe_id=?1
         ORDER BY a.entity_id, a.alias, a.id",
    )?;
    let aliases = alias_stmt.query_map(params![universe_id], alias_from_row)?
        .collect::<rusqlite::Result<Vec<_>>>()?;
    Ok(EntitySnapshot { entities, aliases })
}

pub fn create_entity(
    db: &mut Connection, input: CreateEntityInput,
) -> Result<NarrativeEntity, EntityError> {
    let id = text(&input.id, "L'identifiant")?;
    let universe_id = text(&input.universe_id, "L'univers")?;
    let kind = kind(&input.kind)?;
    let name = text(&input.name, "Le nom")?;
    if !universe_exists(db, &universe_id)? {
        return Err(EntityError::NotFound("Univers"));
    }
    if get_entity(db, &id).is_ok() {
        return Err(EntityError::Validation("Identifiant d'entité déjà utilisé.".to_string()));
    }
    db.execute(
        "INSERT INTO narrative_entities(id, universe_id, kind, name)
         VALUES (?1, ?2, ?3, ?4)",
        params![id, universe_id, kind, name],
    )?;
    get_entity(db, &id)
}

pub fn rename_entity(
    db: &mut Connection, input: RenameEntityInput,
) -> Result<NarrativeEntity, EntityError> {
    let id = text(&input.id, "L'identifiant")?;
    let name = text(&input.name, "Le nom")?;
    if !matches!(get_entity(db, &id), Ok(_)) {
        return Err(EntityError::NotFound("Entité narrative"));
    }
    db.execute(
        "UPDATE narrative_entities SET name=?2 WHERE id=?1",
        params![id, name],
    )?;
    get_entity(db, &id)
}

pub fn delete_entity(db: &mut Connection, id: &str) -> Result<(), EntityError> {
    let id = text(id, "L'identifiant")?;
    get_entity(db, &id)?;
    let count: i64 = db.query_row(
        "SELECT COUNT(*) FROM entity_aliases WHERE entity_id=?1",
        params![id],
        |row| row.get(0),
    )?;
    if count > 0 {
        return Err(EntityError::HasChildren { count });
    }
    let facts: i64 = db.query_row(
        "SELECT COUNT(*) FROM narrative_facts WHERE entity_id=?1",
        params![id], |r| r.get(0),
    )?;
    if facts > 0 { return Err(EntityError::HasFacts { count: facts }); }
    db.execute("DELETE FROM narrative_entities WHERE id=?1", params![id])?;
    Ok(())
}

pub fn create_alias(
    db: &mut Connection, input: CreateAliasInput,
) -> Result<EntityAlias, EntityError> {
    let id = text(&input.id, "L'identifiant")?;
    let entity_id = text(&input.entity_id, "L'entité")?;
    let alias = text(&input.alias, "L'alias")?;
    let parent = get_entity(db, &entity_id)?;
    if get_alias(db, &id).is_ok() {
        return Err(EntityError::Validation("Identifiant d'alias déjà utilisé.".to_string()));
    }
    let already_exists: i64 = db.query_row(
        "SELECT EXISTS(
             SELECT 1 FROM entity_aliases WHERE entity_id=?1 AND alias=?2
         )",
        params![entity_id, alias],
        |row| row.get(0),
    )?;
    if already_exists == 1 {
        return Err(EntityError::Validation("Cet alias existe déjà pour cette entité.".to_string()));
    }
    db.execute(
        "INSERT INTO entity_aliases(id, entity_id, universe_id, alias)
         VALUES (?1, ?2, ?3, ?4)",
        params![id, entity_id, parent.universe_id, alias],
    )?;
    get_alias(db, &id)
}

pub fn rename_alias(
    db: &mut Connection, input: RenameAliasInput,
) -> Result<EntityAlias, EntityError> {
    let id = text(&input.id, "L'identifiant")?;
    let alias = text(&input.alias, "L'alias")?;
    let existing = get_alias(db, &id)?;
    let collision: i64 = db.query_row(
        "SELECT EXISTS(
            SELECT 1 FROM entity_aliases
            WHERE entity_id=?1 AND alias=?2 AND id<>?3
         )",
        params![existing.entity_id, alias, id],
        |row| row.get(0),
    )?;
    if collision == 1 {
        return Err(EntityError::Validation("Cet alias existe déjà pour cette entité.".to_string()));
    }
    db.execute("UPDATE entity_aliases SET alias=?2 WHERE id=?1", params![id, alias])?;
    get_alias(db, &id)
}

pub fn delete_alias(db: &mut Connection, id: &str) -> Result<(), EntityError> {
    let id = text(id, "L'identifiant")?;
    get_alias(db, &id)?;
    db.execute("DELETE FROM entity_aliases WHERE id=?1", params![id])?;
    Ok(())
}

fn atomic<T, F>(db: &mut Connection, operation: F) -> Result<T, EntityError>
where
    F: FnOnce(&Transaction<'_>) -> Result<T, EntityError>,
{
    let tx = db.transaction()?;
    let result = operation(&tx)?;
    tx.commit()?;
    Ok(result)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::database;

    fn connection() -> Connection {
        let mut db = Connection::open_in_memory().expect("memory");
        database::configure_connection(&db).expect("FK enabled");
        database::run_migrations(&mut db).expect("schema v4");
        db
    }

    fn universe(db: &Connection, id: &str) {
        db.execute(
            "INSERT INTO universes (id, name) VALUES (?1, ?2)",
            params![id, format!("Universe {id}")],
        ).expect("universe");
    }

    fn entity(id: &str, universe_id: &str, kind: &str, name: &str) -> CreateEntityInput {
        CreateEntityInput {
            id: id.to_string(), universe_id: universe_id.to_string(),
            kind: kind.to_string(), name: name.to_string(),
        }
    }

    #[test]
    fn creates_lists_and_reads_all_six_kinds_with_duplicate_names() {
        let mut db = connection();
        universe(&db, "u1");
        universe(&db, "u2");
        for (n, kind) in ENTITY_KINDS.iter().enumerate() {
            let created = create_entity(&mut db, entity(&format!("e{n}"), "u1", kind, "Same"))
                .expect("create");
            assert_eq!(created.kind, *kind);
        }
        create_entity(&mut db, entity("other", "u2", "character", "Same")).expect("same name");
        let result = snapshot(&db, "u1").expect("snapshot");
        assert_eq!(result.entities.len(), 6);
        assert!(result.aliases.is_empty());
        assert_eq!(get_entity(&db, "e0").expect("get").name, "Same");
        assert_eq!(snapshot(&db, "u2").expect("other").entities.len(), 1);
    }

    #[test]
    fn rejects_unknown_kind_blank_name_and_invalid_universe() {
        let mut db = connection();
        universe(&db, "u1");
        assert!(matches!(
            create_entity(&mut db, entity("x", "u1", "monster", "Name")),
            Err(EntityError::Validation(_))
        ));
        assert!(matches!(
            create_entity(&mut db, entity("x", "u1", "place", "  ")),
            Err(EntityError::Validation(_))
        ));
        assert!(matches!(
            create_entity(&mut db, entity("x", "bad", "place", "Name")),
            Err(EntityError::NotFound("Univers"))
        ));
        assert!(matches!(snapshot(&db, "bad"), Err(EntityError::NotFound("Univers"))));
    }

    #[test]
    fn rename_preserves_entity_identity_kind_and_universe() {
        let mut db = connection();
        universe(&db, "u1");
        create_entity(&mut db, entity("e1", "u1", "character", "Before")).expect("create");
        let renamed = rename_entity(&mut db, RenameEntityInput {
            id: "e1".to_owned(), name: "After".to_owned(),
        }).expect("rename");
        assert_eq!(renamed.id, "e1");
        assert_eq!(renamed.kind, "character");
        assert_eq!(renamed.universe_id, "u1");
        for sql in [
            "UPDATE narrative_entities SET id='bad' WHERE id='e1'",
            "UPDATE narrative_entities SET kind='place' WHERE id='e1'",
            "UPDATE narrative_entities SET universe_id='other' WHERE id='e1'",
        ] {
            assert!(db.execute(sql, []).is_err());
        }
        assert!(matches!(get_entity(&db, "absent"), Err(EntityError::NotFound(_))));
    }

    #[test]
    fn alias_crud_guards_duplicate_and_cross_universe_ownership() {
        let mut db = connection();
        universe(&db, "u1");
        universe(&db, "u2");
        create_entity(&mut db, entity("e1", "u1", "character", "Ariane")).expect("first");
        create_entity(&mut db, entity("e2", "u2", "character", "Ariane")).expect("second");
        let a = create_alias(&mut db, CreateAliasInput {
            id: "a1".to_owned(), entity_id: "e1".to_owned(), alias: "Ari".to_owned(),
        }).expect("alias");
        assert_eq!(a.universe_id, "u1");
        assert!(matches!(
            create_alias(&mut db, CreateAliasInput {
                id: "a2".to_owned(), entity_id: "e1".to_owned(), alias: "Ari".to_owned(),
            }), Err(EntityError::Validation(_))
        ));
        assert_eq!(snapshot(&db, "u1").expect("u1").aliases.len(), 1);
        assert!(snapshot(&db, "u2").expect("u2").aliases.is_empty());
        assert!(db.execute(
            "UPDATE entity_aliases SET universe_id='u2' WHERE id='a1'", [],
        ).is_err());
        let updated = rename_alias(&mut db, RenameAliasInput {
            id: "a1".to_owned(), alias: "Aria".to_owned(),
        }).expect("rename");
        assert_eq!(updated.id, "a1");
        delete_alias(&mut db, "a1").expect("delete");
        assert!(matches!(get_alias(&db, "a1"), Err(EntityError::NotFound(_))));
    }

    #[test]
    fn refuses_entity_delete_while_aliases_exist_and_then_deletes() {
        let mut db = connection();
        universe(&db, "u1");
        create_entity(&mut db, entity("e1", "u1", "event", "Event")).expect("entity");
        create_alias(&mut db, CreateAliasInput {
            id: "a1".to_owned(), entity_id: "e1".to_owned(), alias: "Nickname".to_owned(),
        }).expect("alias");
        assert!(matches!(
            delete_entity(&mut db, "e1"),
            Err(EntityError::HasChildren { count: 1 })
        ));
        assert_eq!(get_entity(&db, "e1").expect("preserved").id, "e1");
        delete_alias(&mut db, "a1").expect("delete alias");
        delete_entity(&mut db, "e1").expect("delete leaf");
        assert!(matches!(get_entity(&db, "e1"), Err(EntityError::NotFound(_))));
    }

    #[test]
    fn failed_multi_row_operation_rolls_back_every_insert() {
        let mut db = connection();
        universe(&db, "u1");
        let failed = atomic(&mut db, |tx| {
            tx.execute(
                "INSERT INTO narrative_entities (id, universe_id, kind, name)
                 VALUES ('e1', 'u1', 'character', 'Name')", [],
            )?;
            tx.execute(
                "INSERT INTO entity_aliases (id, entity_id, universe_id, alias)
                 VALUES ('a1', 'e1', 'wrong-universe', 'Alias')", [],
            )?;
            Ok(())
        });
        assert!(failed.is_err());
        let total: i64 = db.query_row(
            "SELECT COUNT(*) FROM narrative_entities", [], |r| r.get(0),
        ).expect("count");
        assert_eq!(total, 0);
    }

    #[test]
    fn errors_serialize_to_stable_tauri_payloads() {
        let missing = serde_json::to_value(EntityError::NotFound("Alias").payload())
            .expect("serialization");
        assert_eq!(missing["code"], "not_found");
        let child = serde_json::to_value(EntityError::HasChildren { count: 2 }.payload())
            .expect("serialization");
        assert_eq!(child["code"], "has_children");
    }
}
