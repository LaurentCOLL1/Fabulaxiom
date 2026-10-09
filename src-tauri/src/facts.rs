use rusqlite::{params, Connection, OptionalExtension, Row, Transaction};
use serde::{Deserialize, Serialize};
use std::fmt;

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct NarrativeFact {
    pub id: String,
    pub entity_id: String,
    pub universe_id: String,
    pub fact_key: String,
    pub fact_value: String,
    pub provenance_kind: String,
    pub validity_kind: Option<String>,
    pub validity_text: Option<String>,
    pub created_at_utc: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct FactSource {
    pub id: String,
    pub fact_id: String,
    pub universe_id: String,
    pub revision_id: String,
    pub start_byte: i64,
    pub end_byte: i64,
    pub quoted_text: String,
}

#[derive(Debug, Clone, Serialize, PartialEq, Eq)]
pub struct FactRecord {
    pub fact: NarrativeFact,
    pub source: Option<FactSource>,
}

#[derive(Debug, Clone, Serialize, PartialEq, Eq)]
pub struct FactSnapshot {
    pub universe_id: String,
    pub records: Vec<FactRecord>,
}

#[derive(Debug, Clone, Deserialize, PartialEq, Eq)]
pub struct FactUniverseInput {
    pub universe_id: String,
}

#[derive(Debug, Clone, Deserialize, PartialEq, Eq)]
pub struct CreateFactSourceInput {
    pub id: String,
    pub revision_id: String,
    pub start_byte: i64,
    pub end_byte: i64,
    pub quoted_text: String,
}

#[derive(Debug, Clone, Deserialize, PartialEq, Eq)]
pub struct CreateFactInput {
    pub id: String,
    pub entity_id: String,
    pub fact_key: String,
    pub fact_value: String,
    pub provenance_kind: String,
    pub validity_kind: Option<String>,
    pub validity_text: Option<String>,
    pub source: Option<CreateFactSourceInput>,
}

#[derive(Debug, Clone, Serialize, PartialEq, Eq)]
pub struct FactErrorPayload {
    pub code: &'static str,
    pub message: String,
}

#[derive(Debug)]
pub enum FactError {
    NotFound(&'static str),
    Validation(&'static str),
    CrossUniverse,
    InvalidSpan,
    SourceMismatch,
    Database(rusqlite::Error),
}

impl FactError {
    pub fn payload(&self) -> FactErrorPayload {
        match self {
            Self::NotFound(object) => FactErrorPayload {
                code: "not_found",
                message: format!("{object} introuvable."),
            },
            Self::Validation(message) => FactErrorPayload {
                code: "validation",
                message: (*message).to_owned(),
            },
            Self::CrossUniverse => FactErrorPayload {
                code: "cross_universe",
                message: "La source et l'entité ne sont pas dans le même univers.".to_owned(),
            },
            Self::InvalidSpan => FactErrorPayload {
                code: "invalid_utf8_span",
                message: "Les positions doivent désigner des limites UTF-8 valides et un passage non vide.".to_owned(),
            },
            Self::SourceMismatch => FactErrorPayload {
                code: "source_mismatch",
                message: "Le passage cité ne correspond pas au texte immuable de la révision.".to_owned(),
            },
            Self::Database(_) => FactErrorPayload {
                code: "database",
                message: "Échec de l'opération de faits dans la base locale.".to_owned(),
            },
        }
    }
}
impl fmt::Display for FactError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let payload = self.payload();
        write!(f, "{}: {}", payload.code, payload.message)
    }
}
impl std::error::Error for FactError {}
impl From<rusqlite::Error> for FactError {
    fn from(error: rusqlite::Error) -> Self { Self::Database(error) }
}

fn required(value: &str) -> Result<String, FactError> {
    let value = value.trim();
    if value.is_empty() { return Err(FactError::Validation("Un identifiant ou texte obligatoire est vide.")); }
    Ok(value.to_owned())
}

fn from_fact(row: &Row<'_>) -> rusqlite::Result<NarrativeFact> {
    Ok(NarrativeFact {
        id: row.get(0)?, entity_id: row.get(1)?, universe_id: row.get(2)?,
        fact_key: row.get(3)?, fact_value: row.get(4)?,
        provenance_kind: row.get(5)?, validity_kind: row.get(6)?,
        validity_text: row.get(7)?, created_at_utc: row.get(8)?,
    })
}
fn from_source(row: &Row<'_>) -> rusqlite::Result<FactSource> {
    Ok(FactSource {
        id: row.get(0)?, fact_id: row.get(1)?, universe_id: row.get(2)?,
        revision_id: row.get(3)?, start_byte: row.get(4)?,
        end_byte: row.get(5)?, quoted_text: row.get(6)?,
    })
}

fn load_source(db: &Connection, fact_id: &str) -> Result<Option<FactSource>, FactError> {
    Ok(db.query_row(
        "SELECT id, fact_id, universe_id, revision_id, start_byte, end_byte, quoted_text
         FROM fact_sources WHERE fact_id=?1",
        params![fact_id], from_source,
    ).optional()?)
}

pub fn get_fact(db: &Connection, id: &str) -> Result<FactRecord, FactError> {
    let id = required(id)?;
    let fact = db.query_row(
        "SELECT id, entity_id, universe_id, fact_key, fact_value, provenance_kind,
                validity_kind, validity_text, created_at_utc
         FROM narrative_facts WHERE id=?1",
        params![id], from_fact,
    ).optional()?.ok_or(FactError::NotFound("Fait"))?;
    let source = load_source(db, &id)?;
    if (fact.provenance_kind == "sourced") != source.is_some() {
        return Err(FactError::Validation("Fait sans provenance cohérente."));
    }
    Ok(FactRecord { fact, source })
}

pub fn snapshot(db: &Connection, universe_id: &str) -> Result<FactSnapshot, FactError> {
    let id = required(universe_id)?;
    let exists: i64 = db.query_row(
        "SELECT EXISTS(SELECT 1 FROM universes WHERE id=?1)",
        params![id], |r| r.get(0),
    )?;
    if exists == 0 { return Err(FactError::NotFound("Univers")); }
    let mut statement = db.prepare(
        "SELECT id, entity_id, universe_id, fact_key, fact_value, provenance_kind,
                validity_kind, validity_text, created_at_utc
         FROM narrative_facts WHERE universe_id=?1 ORDER BY entity_id, fact_key, id",
    )?;
    let facts = statement.query_map(params![id], from_fact)?
        .collect::<rusqlite::Result<Vec<_>>>()?;
    let records = facts.into_iter().map(|fact| {
        let source = load_source(db, &fact.id)?;
        if (fact.provenance_kind == "sourced") != source.is_some() {
            return Err(FactError::Validation("Fait sans provenance cohérente."));
        }
        Ok(FactRecord { fact, source })
    }).collect::<Result<Vec<_>, FactError>>()?;
    Ok(FactSnapshot { universe_id: id, records })
}

fn validate_time(
    kind: Option<String>, value: Option<String>,
) -> Result<(Option<String>, Option<String>), FactError> {
    match (kind, value) {
        (None, None) => Ok((None, None)),
        (Some(kind), Some(value)) => {
            let kind = required(&kind)?;
            if !["exact", "approximate", "relative", "unknown"].contains(&kind.as_str()) {
                return Err(FactError::Validation("Type de validité temporelle inconnu."));
            }
            Ok((Some(kind), Some(required(&value)?)))
        },
        _ => Err(FactError::Validation("La validité temporelle doit être entièrement renseignée ou absente.")),
    }
}

fn check_source(
    tx: &Transaction<'_>, source: CreateFactSourceInput, universe_id: &str,
) -> Result<(String, String, i64, i64, String), FactError> {
    let source_id = required(&source.id)?;
    let revision_id = required(&source.revision_id)?;
    let entry: Option<(String, String)> = tx.query_row(
        "SELECT r.content, n.universe_id
         FROM scene_text_revisions r
         JOIN scenes s ON s.id=r.scene_id
         JOIN chapters c ON c.id=s.chapter_id
         JOIN novels n ON n.id=c.novel_id
         WHERE r.id=?1",
        params![revision_id], |r| Ok((r.get(0)?, r.get(1)?)),
    ).optional()?;
    let (content, source_universe) = entry.ok_or(FactError::NotFound("Révision"))?;
    if source_universe != universe_id { return Err(FactError::CrossUniverse); }
    let start = usize::try_from(source.start_byte).map_err(|_| FactError::InvalidSpan)?;
    let end = usize::try_from(source.end_byte).map_err(|_| FactError::InvalidSpan)?;
    if start >= end || end > content.len()
        || !content.is_char_boundary(start) || !content.is_char_boundary(end) {
        return Err(FactError::InvalidSpan);
    }
    if content.get(start..end) != Some(source.quoted_text.as_str()) {
        return Err(FactError::SourceMismatch);
    }
    Ok((source_id, revision_id, source.start_byte, source.end_byte, source.quoted_text))
}

/// An entire sourced fact and its exact citation are written in one transaction.
/// No write to the current scene head and no AI/canon operation is performed.
pub fn create_fact(db: &mut Connection, input: CreateFactInput) -> Result<FactRecord, FactError> {
    let id = required(&input.id)?;
    let entity_id = required(&input.entity_id)?;
    let key = required(&input.fact_key)?;
    let value = required(&input.fact_value)?;
    let provenance = required(&input.provenance_kind)?;
    if !["sourced", "unsourced"].contains(&provenance.as_str()) {
        return Err(FactError::Validation("La provenance doit être sourced ou unsourced."));
    }
    if (provenance == "sourced") != input.source.is_some() {
        return Err(FactError::Validation("Une source est obligatoire pour sourced et interdite pour unsourced."));
    }
    let (validity_kind, validity_text) = validate_time(input.validity_kind, input.validity_text)?;
    let tx = db.transaction()?;
    let universe_id: String = tx.query_row(
        "SELECT universe_id FROM narrative_entities WHERE id=?1",
        params![entity_id], |r| r.get(0),
    ).optional()?.ok_or(FactError::NotFound("Entité narrative"))?;
    let existing: i64 = tx.query_row(
        "SELECT EXISTS(SELECT 1 FROM narrative_facts WHERE id=?1)",
        params![id], |r| r.get(0),
    )?;
    if existing != 0 { return Err(FactError::Validation("Identifiant de fait déjà utilisé.")); }
    tx.execute(
        "INSERT INTO narrative_facts
         (id, entity_id, universe_id, fact_key, fact_value, provenance_kind, validity_kind, validity_text)
         VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8)",
        params![id, entity_id, universe_id, key, value, provenance, validity_kind, validity_text],
    )?;
    if let Some(source) = input.source {
        let (sid, revision_id, start, end, quote) = check_source(&tx, source, &universe_id)?;
        tx.execute(
            "INSERT INTO fact_sources
             (id, fact_id, universe_id, revision_id, start_byte, end_byte, quoted_text)
             VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7)",
            params![sid, id, universe_id, revision_id, start, end, quote],
        )?;
    }
    let record = get_fact(&tx, &id)?;
    tx.commit()?;
    Ok(record)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::database;

    fn fixture() -> Connection {
        let mut db = Connection::open_in_memory().expect("memory");
        database::configure_connection(&db).expect("foreign keys");
        database::run_migrations(&mut db).expect("migration v5");
        db.execute_batch(
            "INSERT INTO universes(id,name) VALUES ('u1','One'),('u2','Two');
             INSERT INTO novels(id,universe_id,title,sort_order)
             VALUES ('n1','u1','First',0),('n2','u2','Second',0);
             INSERT INTO chapters(id,novel_id,title,sort_order)
             VALUES ('c1','n1','First',0),('c2','n2','Second',0);
             INSERT INTO scenes(id,chapter_id,title,sort_order)
             VALUES ('s1','c1','First',0),('s2','c2','Second',0);
             INSERT INTO scene_text_revisions(id,scene_id,revision_number,content)
             VALUES ('r1','s1',1,'Été 🐈 magique'),('r2','s2',1,'Other universe');
             INSERT INTO scene_revision_heads(scene_id,revision_id) VALUES('s1','r1');
             INSERT INTO narrative_entities(id,universe_id,kind,name)
             VALUES ('e1','u1','character','Ariane'),('e2','u2','character','Ariane');"
        ).expect("seed");
        db
    }
    fn unsourced(id: &str, eid: &str) -> CreateFactInput {
        CreateFactInput {
            id: id.to_owned(), entity_id: eid.to_owned(),
            fact_key: "signe".to_owned(), fact_value: "Un signe".to_owned(),
            provenance_kind: "unsourced".to_owned(),
            validity_kind: None, validity_text: None, source: None,
        }
    }
    fn sourced(id: &str) -> CreateFactInput {
        // The first "É" is 2 bytes, the cat emoji is 4 bytes.
        CreateFactInput {
            id: id.to_owned(), entity_id: "e1".to_owned(),
            fact_key: "lieu".to_owned(), fact_value: "Un jardin".to_owned(),
            provenance_kind: "sourced".to_owned(),
            validity_kind: Some("relative".to_owned()),
            validity_text: Some("après la fête".to_owned()),
            source: Some(CreateFactSourceInput {
                id: format!("source-{id}"), revision_id: "r1".to_owned(),
                start_byte: 0, end_byte: 10, quoted_text: "Été 🐈".to_owned(),
            }),
        }
    }
    #[test]
    fn unsourced_is_explicit_and_does_not_invent_citations() {
        let mut db = fixture();
        let result = create_fact(&mut db, unsourced("f1", "e1")).expect("unsourced");
        assert!(result.source.is_none());
        assert_eq!(result.fact.provenance_kind, "unsourced");
        assert_eq!(snapshot(&db, "u1").unwrap().records.len(), 1);
        assert_eq!(snapshot(&db, "u2").unwrap().records.len(), 0);
        assert!(matches!(snapshot(&db, "bad"), Err(FactError::NotFound("Univers"))));
        assert_eq!(serde_json::to_value(&result).unwrap()["fact"]["fact_key"], "signe");
    }
    #[test]
    fn exact_multibyte_anchor_survives_current_head_changes() {
        let mut db = fixture();
        let created = create_fact(&mut db, sourced("f1")).expect("sourced");
        let source = created.source.as_ref().unwrap();
        assert_eq!((source.start_byte, source.end_byte), (0, 10));
        assert_eq!(source.quoted_text, "Été 🐈");
        db.execute("INSERT INTO scene_text_revisions(id,scene_id,revision_number,content)
                    VALUES ('r3','s1',2,'A new revision')", []).unwrap();
        db.execute("UPDATE scene_revision_heads SET revision_id='r3' WHERE scene_id='s1'", []).unwrap();
        assert_eq!(get_fact(&db, "f1").unwrap(), created);
        assert_eq!(snapshot(&db, "u1").unwrap().records[0], created);
    }
    #[test]
    fn rejects_split_utf8_out_of_bounds_empty_and_mismatched_quote() {
        let mut db = fixture();
        for (start, end, quote) in [
            (1, 10, "té 🐈"), (0, 9, "Été "), (0, 800, "Été 🐈"),
            (-1, 10, "Été 🐈"), (10, 10, ""), (0, 10, "ÉtÉ 🐈"),
        ] {
            let mut input = sourced("bad");
            let src = input.source.as_mut().unwrap();
            src.start_byte=start; src.end_byte=end; src.quoted_text=quote.to_owned();
            assert!(create_fact(&mut db, input).is_err());
            assert_eq!(db.query_row("SELECT COUNT(*) FROM narrative_facts",[],|r|r.get::<_,i64>(0)).unwrap(),0);
        }
    }
    #[test]
    fn cross_universe_revisions_and_missing_entities_fail_without_rows() {
        let mut db=fixture();
        let mut cross=sourced("cross");
        cross.source.as_mut().unwrap().revision_id="r2".to_owned();
        assert!(matches!(create_fact(&mut db,cross),Err(FactError::CrossUniverse)));
        assert!(matches!(create_fact(&mut db,unsourced("x","absent")),Err(FactError::NotFound(_))));
        let mut invalid=sourced("missing");
        invalid.source.as_mut().unwrap().revision_id="absent".to_owned();
        assert!(matches!(create_fact(&mut db,invalid),Err(FactError::NotFound(_))));
        let count:i64=db.query_row("SELECT COUNT(*) FROM narrative_facts",[],|r|r.get(0)).unwrap();
        assert_eq!(count,0);
    }
    #[test]
    fn rejects_fabricated_provenance_and_bad_validity() {
        let mut db=fixture();
        let mut bad=unsourced("a","e1");
        bad.provenance_kind="canon".to_owned();
        assert!(create_fact(&mut db,bad).is_err());
        let mut bad=unsourced("b","e1");
        bad.provenance_kind="sourced".to_owned();
        assert!(create_fact(&mut db,bad).is_err());
        let mut bad=sourced("c");bad.provenance_kind="unsourced".to_owned();
        assert!(create_fact(&mut db,bad).is_err());
        let mut bad=unsourced("d","e1");bad.validity_text=Some("later".to_owned());
        assert!(create_fact(&mut db,bad).is_err());
        let mut bad=unsourced("e","e1");bad.validity_kind=Some("gregorian".to_owned());bad.validity_text=Some("5".to_owned());
        assert!(create_fact(&mut db,bad).is_err());
    }
    #[test]
    fn second_row_failure_rolls_back_fact_in_same_transaction() {
        let mut db=fixture();
        create_fact(&mut db,sourced("f1")).unwrap();
        let mut another=sourced("f2");
        another.source.as_mut().unwrap().id="source-f1".to_owned();
        assert!(create_fact(&mut db,another).is_err());
        assert!(matches!(get_fact(&db,"f2"),Err(FactError::NotFound(_))));
        let count:i64=db.query_row("SELECT COUNT(*) FROM fact_sources",[],|r|r.get(0)).unwrap();
        assert_eq!(count,1);
    }
    #[test]
    fn database_restricts_invalid_direct_sql_and_entity_delete() {
        let mut db=fixture();
        create_fact(&mut db,sourced("f1")).unwrap();
        for sql in [
            "DELETE FROM narrative_entities WHERE id='e1'",
            "UPDATE narrative_facts SET entity_id='e2' WHERE id='f1'",
            "DELETE FROM narrative_facts WHERE id='f1'",
            "UPDATE fact_sources SET start_byte=2 WHERE fact_id='f1'",
            "DELETE FROM fact_sources WHERE fact_id='f1'",
            "INSERT INTO fact_sources(id,fact_id,universe_id,revision_id,start_byte,end_byte,quoted_text)
             VALUES('wrong','f1','u1','r2',0,5,'Other')",
        ] {assert!(db.execute(sql,[]).is_err(),"{sql}");}
        let violations:Vec<_>=db.prepare("PRAGMA foreign_key_check").unwrap().query_map([],|_|Ok(())).unwrap()
            .collect::<rusqlite::Result<Vec<_>>>().unwrap();
        assert!(violations.is_empty());
        assert_eq!(db.query_row("PRAGMA integrity_check",[],|r|r.get::<_,String>(0)).unwrap(),"ok");
    }
    #[test]
    fn source_error_payload_is_deterministic() {
        let encoded=serde_json::to_value(FactError::InvalidSpan.payload()).unwrap();
        assert_eq!(encoded["code"],"invalid_utf8_span");
    }
}
