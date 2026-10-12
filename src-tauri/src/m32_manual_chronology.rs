//! M3.2 first-stage *test-only* manual chronology service contract.
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

#[cfg(test)]
mod tests {
    use super::*;
    use crate::database;

    const V7_SQL: &str = include_str!("../sql/m3_1_world_time_v7_candidate.sql");

    fn isolated_v7() -> Connection {
        let mut db = Connection::open_in_memory().expect("in-memory only");
        database::configure_connection(&db).expect("foreign keys on");
        assert_eq!(database::run_migrations(&mut db).expect("legacy v6"), 6);
        // Deliberately stage the candidate only inside a new in-memory fixture.
        let tx = db.transaction().expect("isolated transaction");
        tx.execute_batch(V7_SQL).expect("candidate");
        tx.execute(
            "INSERT INTO schema_migrations(version,name)
             VALUES (7,'007_create_world_time_foundation')", [],
        ).expect("explicit fixture lineage only");
        tx.commit().expect("isolated commit");
        assert_eq!(database::current_schema_version(&db).unwrap(), 7);
        db
    }

    fn universe(db: &Connection, id: &str) {
        db.execute(
            "INSERT INTO universes(id,name) VALUES (?1,?2)",
            params![id,format!("Universe {id}")],
        ).expect("universe");
    }

    fn unknown<'a>(id: &'a str, universe_id: &'a str) -> AnchorDraft<'a> {
        AnchorDraft {
            id, universe_id, time_kind: "unknown", calendar_id: None,
            event_entity_id: None, source_revision_id: None,
            exact_label: None, window_start_text: None, window_end_text: None,
            precision_text: None,
        }
    }

    #[test]
    fn four_time_kinds_remain_raw_and_unordered() {
        let db = isolated_v7();
        universe(&db, "u1");
        create_calendar(&db, "cal", "u1", "Tides", "One cycle is eleven moons").unwrap();
        create_anchor(&db, AnchorDraft {
            id: "a", universe_id: "u1", time_kind: "exact", calendar_id: Some("cal"),
            exact_label: Some("Tide XX, Moon VII"), precision_text: Some("moon"),
            ..unknown("a", "u1")
        }).unwrap();
        create_anchor(&db, AnchorDraft {
            id: "b", universe_id: "u1", time_kind: "approximate",
            calendar_id: Some("cal"), window_start_text: Some("First storm"),
            precision_text: Some("season"), ..unknown("b", "u1")
        }).unwrap();
        create_anchor(&db, AnchorDraft {
            id: "c", universe_id: "u1", time_kind: "relative",
            ..unknown("c","u1")
        }).unwrap();
        create_anchor(&db, unknown("d", "u1")).unwrap();

        let a = list_anchors(&db, "u1").unwrap();
        assert_eq!(a.len(), 4);
        assert_eq!(a[0].exact_label.as_deref(), Some("Tide XX, Moon VII"));
        assert_eq!(a[1].window_start_text.as_deref(), Some("First storm"));
        assert_eq!(a[2].time_kind, "relative");
        assert_eq!(a[3].time_kind, "unknown");
        assert!(list_precedences(&db, "u1").unwrap().is_empty());
        assert!(create_anchor(&db, AnchorDraft {
            id: "bad", universe_id: "u1", time_kind: "exact",
            exact_label: Some("2026-10-12"), ..unknown("bad","u1")
        }).is_err(), "exact requires explicit fictional calendar");
    }

    #[test]
    fn human_edges_are_partial_order_and_cycles_are_rejected() {
        let db = isolated_v7(); universe(&db,"u1");
        for id in ["z","a","b","orphan"] {
            create_anchor(&db, unknown(id,"u1")).unwrap();
        }
        create_precedence(&db,"ab","u1","a","b","Author decision",None).unwrap();
        create_precedence(&db,"bz","u1","b","z","Chapter note",None).unwrap();
        assert!(create_precedence(&db,"za","u1","z","a","would cycle",None).is_err());
        assert!(create_precedence(&db,"aa","u1","a","a","self",None).is_err());
        assert!(create_precedence(&db,"dupe","u1","a","b","repeated",None).is_err());
        assert_eq!(list_precedences(&db,"u1").unwrap().len(), 2);
        assert_eq!(list_anchors(&db,"u1").unwrap().len(), 4);
        assert!(list_precedences(&db,"u2").unwrap().is_empty());
    }

    #[test]
    fn other_universe_and_non_event_sources_fail_without_writes() {
        let db = isolated_v7(); universe(&db,"u1"); universe(&db,"u2");
        create_calendar(&db,"cal1","u1","Calendar","Custom epoch").unwrap();
        db.execute_batch(
            "INSERT INTO narrative_entities(id,universe_id,kind,name)
             VALUES ('actor','u1','character','Same'),
                    ('event','u1','event','Same'),
                    ('event2','u2','event','Same')",
        ).unwrap();

        assert!(create_anchor(&db, AnchorDraft {
            id:"wrong-kind", event_entity_id:Some("actor"), ..unknown("wrong-kind","u1")
        }).is_err());
        assert!(create_anchor(&db, AnchorDraft {
            id:"wrong-universe", event_entity_id:Some("event2"),
            ..unknown("wrong-universe","u1")
        }).is_err());
        assert!(create_anchor(&db, AnchorDraft {
            id:"wrong-calendar",time_kind:"exact",calendar_id:Some("cal1"),
            exact_label:Some("Fictional day"), ..unknown("wrong-calendar","u2")
        }).is_err());
        create_anchor(&db, AnchorDraft {
            id:"good",event_entity_id:Some("event"), ..unknown("good","u1")
        }).unwrap();
        create_anchor(&db, unknown("other","u2")).unwrap();
        assert!(create_precedence(&db,"cross","u1","good","other","invalid",None).is_err());
        assert_eq!(list_anchors(&db,"u1").unwrap().len(),1);
        assert_eq!(list_anchors(&db,"u2").unwrap().len(),1);
    }

    #[test]
    fn historical_revision_is_not_rebased_to_current_scene_head() {
        let db=isolated_v7(); universe(&db,"u1"); universe(&db,"u2");
        db.execute_batch(
            "INSERT INTO novels(id,universe_id,title,sort_order) VALUES
                ('novel1','u1','First novel',0),('novel2','u2','Other novel',0);
             INSERT INTO chapters(id,novel_id,title,sort_order) VALUES
                ('chap1','novel1','Chapter',0),('chap2','novel2','Chapter',0);
             INSERT INTO scenes(id,chapter_id,title,sort_order) VALUES
                ('scene1','chap1','Scene',0),('scene2','chap2','Scene',0);
             INSERT INTO scene_text_revisions(id,scene_id,revision_number,content) VALUES
                ('old-rev','scene1',1,'First text'),
                ('other-rev','scene2',1,'Foreign text')",
        ).unwrap();
        create_anchor(&db, AnchorDraft {
            id:"linked",source_revision_id:Some("old-rev"), ..unknown("linked","u1")
        }).unwrap();
        assert!(create_anchor(&db, AnchorDraft {
            id:"cross",source_revision_id:Some("other-rev"), ..unknown("cross","u1")
        }).is_err());
        assert_eq!(
            list_anchors(&db,"u1").unwrap()[0].source_revision_id.as_deref(),
            Some("old-rev")
        );
    }

    #[test]
    fn existing_history_is_immutable_and_normal_runtime_stays_v6() {
        let db=isolated_v7(); universe(&db,"u1");
        create_anchor(&db, unknown("x","u1")).unwrap();
        create_anchor(&db, unknown("y","u1")).unwrap();
        create_precedence(&db,"xy","u1","x","y","authored",None).unwrap();
        assert!(db.execute(
            "UPDATE world_time_anchors SET time_kind='relative' WHERE id='x'",[]
        ).is_err());
        assert!(db.execute(
            "DELETE FROM world_time_precedences WHERE id='xy'",[]
        ).is_err());
        assert_eq!(list_anchors(&db,"u1").unwrap().len(),2);
        assert_eq!(list_precedences(&db,"u1").unwrap().len(),1);
        assert_eq!(database::CURRENT_SCHEMA_VERSION,6);
        assert_eq!(database::MAX_AUTOMATIC_MIGRATION_VERSION,6);
    }
}
