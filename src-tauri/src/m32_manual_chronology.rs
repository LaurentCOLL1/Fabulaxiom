//! M3.2 first-stage *test-only* manual chronology service contract, cleanly ported from PR #35.
//! Never exported through Tauri IPC or compiled into the normal production app.
//! Works on fresh isolated v7 SQLite fixtures; no implicit date conversion.
//! The v7 schema is append-only: amendments/deletions require future governed
//! supersession, and are not silently implemented as SQL UPDATE/DELETE.

use rusqlite::{params, Connection, Result};

#[derive(Debug, PartialEq, Eq)]
pub struct ManualAnchor {
    pub id: String,
    pub universe_id: String,
    pub time_kind: String,
    pub calendar_id: Option<String>,
    pub event_entity_id: Option<String>,
    pub source_revision_id: Option<String>,
    pub exact_label: Option<String>,
    pub window_start_text: Option<String>,
    pub window_end_text: Option<String>,
    pub precision_text: Option<String>,
}

#[derive(Debug, PartialEq, Eq)]
pub struct ManualPrecedence {
    pub id: String,
    pub before_anchor_id: String,
    pub after_anchor_id: String,
    pub reason: String,
    pub source_revision_id: Option<String>,
}

#[derive(Debug, Clone, Copy)]
pub struct AnchorDraft<'a> {
    pub id: &'a str,
    pub universe_id: &'a str,
    pub time_kind: &'a str,
    pub calendar_id: Option<&'a str>,
    pub event_entity_id: Option<&'a str>,
    pub source_revision_id: Option<&'a str>,
    pub exact_label: Option<&'a str>,
    pub window_start_text: Option<&'a str>,
    pub window_end_text: Option<&'a str>,
    pub precision_text: Option<&'a str>,
}

// Each statement is single-record, parameterized and controlled by the
// candidate SQL's STRICT CHECK, ownership, immutable revision and cycle guards.
pub fn create_calendar(
    db: &Connection,
    id: &str,
    universe_id: &str,
    name: &str,
    definition_text: &str,
) -> Result<()> {
    db.execute(
        "INSERT INTO fictional_calendars(id,universe_id,name,definition_text)
         VALUES (?1,?2,?3,?4)",
        params![id, universe_id, name, definition_text],
    )?;
    Ok(())
}

pub fn create_anchor(db: &Connection, draft: AnchorDraft<'_>) -> Result<()> {
    db.execute(
        "INSERT INTO world_time_anchors
         (id,universe_id,time_kind,calendar_id,event_entity_id,source_revision_id,
          exact_label,window_start_text,window_end_text,precision_text)
         VALUES (?1,?2,?3,?4,?5,?6,?7,?8,?9,?10)",
        params![
            draft.id, draft.universe_id, draft.time_kind, draft.calendar_id,
            draft.event_entity_id, draft.source_revision_id, draft.exact_label,
            draft.window_start_text, draft.window_end_text, draft.precision_text
        ],
    )?;
    Ok(())
}

pub fn create_precedence(
    db: &Connection,
    id: &str,
    universe_id: &str,
    before_anchor_id: &str,
    after_anchor_id: &str,
    reason: &str,
    source_revision_id: Option<&str>,
) -> Result<()> {
    db.execute(
        "INSERT INTO world_time_precedences
         (id,universe_id,before_anchor_id,after_anchor_id,reason,source_revision_id)
         VALUES (?1,?2,?3,?4,?5,?6)",
        params![
            id, universe_id, before_anchor_id, after_anchor_id, reason, source_revision_id
        ],
    )?;
    Ok(())
}

// Sorting by immutable ID gives a stable *presentation list*. It does NOT
// infer a world-time, narration, or reader-reveal chronology.
pub fn list_anchors(db: &Connection, universe_id: &str) -> Result<Vec<ManualAnchor>> {
    let mut stmt = db.prepare(
        "SELECT id,universe_id,time_kind,calendar_id,event_entity_id,source_revision_id,
                exact_label,window_start_text,window_end_text,precision_text
         FROM world_time_anchors WHERE universe_id=?1 ORDER BY id",
    )?;
    stmt.query_map([universe_id], |row| {
        Ok(ManualAnchor {
            id: row.get(0)?,
            universe_id: row.get(1)?,
            time_kind: row.get(2)?,
            calendar_id: row.get(3)?,
            event_entity_id: row.get(4)?,
            source_revision_id: row.get(5)?,
            exact_label: row.get(6)?,
            window_start_text: row.get(7)?,
            window_end_text: row.get(8)?,
            precision_text: row.get(9)?,
        })
    })?.collect()
}

pub fn list_precedences(db: &Connection, universe_id: &str) -> Result<Vec<ManualPrecedence>> {
    let mut stmt = db.prepare(
        "SELECT id,before_anchor_id,after_anchor_id,reason,source_revision_id
         FROM world_time_precedences WHERE universe_id=?1 ORDER BY id",
    )?;
    stmt.query_map([universe_id], |row| {
        Ok(ManualPrecedence {
            id: row.get(0)?,
            before_anchor_id: row.get(1)?,
            after_anchor_id: row.get(2)?,
            reason: row.get(3)?,
            source_revision_id: row.get(4)?,
        })
    })?.collect()
}



// Compilation is gated by #[cfg(test)] in lib.rs. Test databases exist only in RAM.

#[cfg(test)]
mod tests {
    use super::*;
    use crate::database;

    const V7_CANDIDATE: &str = include_str!("../sql/m3_1_world_time_v7_candidate.sql");

    fn fixture() -> Connection {
        let mut db = Connection::open_in_memory().expect("RAM only");
        database::configure_connection(&db).expect("foreign keys enabled");
        assert_eq!(database::run_migrations(&mut db).expect("v6 in RAM"), 6);
        db.execute(
            "INSERT INTO universes(id,name) VALUES ('u1','Imaginaire A'),('u2','Imaginaire B')", []
        ).expect("two invented universes");
        db.execute_batch(V7_CANDIDATE).expect("v7 candidate in disposable RAM");
        assert_eq!(database::current_schema_version(&db).expect("schema version"), 6);
        db
    }

    fn draft<'a>(id: &'a str, universe: &'a str, kind: &'a str) -> AnchorDraft<'a> {
        AnchorDraft {
            id, universe_id: universe, time_kind: kind,
            calendar_id: None, event_entity_id: None, source_revision_id: None,
            exact_label: None, window_start_text: None, window_end_text: None,
            precision_text: None,
        }
    }

    #[test]
    fn service_creates_and_lists_two_universes_without_real_sqlite() {
        let db=fixture();
        create_anchor(&db, draft("u1-a", "u1", "unknown")).unwrap();
        create_anchor(&db, draft("u2-a", "u2", "relative")).unwrap();
        assert_eq!(list_anchors(&db, "u1").unwrap()[0].id, "u1-a");
        assert_eq!(list_anchors(&db, "u2").unwrap()[0].id, "u2-a");
        assert_eq!(list_precedences(&db, "u1").unwrap().len(), 0);
        assert_eq!(database::CURRENT_SCHEMA_VERSION, 6);
    }

    #[test]
    fn author_explicitly_creates_all_four_time_kinds_without_conversion() {
        let db=fixture();
        create_calendar(&db, "sol", "u1", "Cycle solaire", "Aucune conversion grégorienne").unwrap();
        let mut exact = draft("a-exact", "u1", "exact");
        exact.calendar_id=Some("sol");
        exact.exact_label=Some("Cycle XII, saison 3");
        create_anchor(&db, exact).unwrap();
        let mut approximate = draft("a-approx", "u1", "approximate");
        approximate.calendar_id=Some("sol");
        approximate.window_start_text=Some("avant l'éclipse");
        approximate.precision_text=Some("saison");
        create_anchor(&db, approximate).unwrap();
        create_anchor(&db, draft("a-relative", "u1", "relative")).unwrap();
        create_anchor(&db, draft("a-unknown", "u1", "unknown")).unwrap();
        let all = list_anchors(&db, "u1").unwrap();
        assert_eq!(all.len(), 4);
        assert_eq!(all.iter().find(|a|a.id=="a-exact").unwrap().exact_label.as_deref(),
                   Some("Cycle XII, saison 3"));
        assert_eq!(all.iter().find(|a|a.id=="a-approx").unwrap().precision_text.as_deref(),
                   Some("saison"));
        assert!(list_precedences(&db,"u1").unwrap().is_empty());
    }

    #[test]
    fn only_human_precedence_orders_events_and_cycles_are_rejected() {
        let db=fixture();
        for id in ["a", "b", "c"] {
            create_anchor(&db, draft(id, "u1", "unknown")).unwrap();
        }
        create_precedence(&db,"edge-ab","u1","a","b","Auteur : A avant B",None).unwrap();
        create_precedence(&db,"edge-bc","u1","b","c","Auteur : B avant C",None).unwrap();
        assert!(create_precedence(&db,"edge-ca","u1","c","a","cycle interdit",None).is_err());
        assert!(create_precedence(&db,"edge-aa","u1","a","a","self",None).is_err());
        assert!(create_precedence(&db,"edge-dup","u1","a","b","duplicate",None).is_err());
        let edges=list_precedences(&db,"u1").unwrap();
        assert_eq!(edges.len(),2);
        assert_eq!(edges[0].before_anchor_id, "a");
        assert_eq!(edges[1].after_anchor_id, "c");
    }

    #[test]
    fn strict_guards_refuse_foreign_universe_and_ambiguous_dates() {
        let db=fixture();
        create_calendar(&db,"cal-u1","u1","Auteur A","Temps local").unwrap();
        let mut cross=draft("cross","u2","exact");
        cross.calendar_id=Some("cal-u1");
        cross.exact_label=Some("cycle");
        assert!(create_anchor(&db,cross).is_err());
        let mut incomplete=draft("incomplete","u1","exact");
        incomplete.calendar_id=Some("cal-u1");
        assert!(create_anchor(&db,incomplete).is_err());
        create_anchor(&db,draft("anchor-u1","u1","unknown")).unwrap();
        create_anchor(&db,draft("anchor-u2","u2","unknown")).unwrap();
        assert!(create_precedence(&db,"cross-edge","u1","anchor-u1","anchor-u2","wrong",None).is_err());
        assert!(create_calendar(&db, "cal-u1", "u1", "Again", "Duplicate").is_err());
        assert_eq!(list_anchors(&db,"u2").unwrap().len(),1);
    }

    #[test]
    fn immutable_authored_assertions_are_never_destructively_updated() {
        let db=fixture();
        create_anchor(&db,draft("a","u1","unknown")).unwrap();
        assert!(db.execute("UPDATE world_time_anchors SET time_kind='relative' WHERE id='a'",[]).is_err());
        assert!(db.execute("DELETE FROM world_time_anchors WHERE id='a'",[]).is_err());
        assert!(db.execute("UPDATE universes SET name='Changed' WHERE id='u1'",[]).is_err());
        assert_eq!(list_anchors(&db,"u1").unwrap()[0].time_kind,"unknown");
    }

    #[test]
    fn historical_revision_reference_is_not_current_head_and_obeys_scope() {
        let db=fixture();
        db.execute_batch("
            INSERT INTO novels(id,universe_id,title,sort_order) VALUES
                ('n1','u1','Roman premier',0),
                ('n2','u2','Roman second',0);
            INSERT INTO chapters(id,novel_id,title,sort_order)
                VALUES ('c1','n1','Chapitre',0),('c2','n2','Chapitre',0);
            INSERT INTO scenes(id,chapter_id,title,sort_order)
                VALUES ('s1','c1','Scene',0),('s2','c2','Scene',0);
            INSERT INTO scene_text_revisions(id,scene_id,revision_number,content)
                VALUES ('old-r1','s1',1,'Ancien texte'),
                       ('new-r1','s1',2,'Texte revise'),
                       ('old-r2','s2',1,'Autre roman');").unwrap();
        let mut preserved=draft("historic","u1","unknown");
        preserved.source_revision_id=Some("old-r1");
        create_anchor(&db,preserved).unwrap();
        let mut alien=draft("alien","u1","unknown");
        alien.source_revision_id=Some("old-r2");
        assert!(create_anchor(&db,alien).is_err());
        assert_eq!(list_anchors(&db,"u1").unwrap()[0].source_revision_id.as_deref(),
                   Some("old-r1"));
    }
}
