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


#[derive(Debug, PartialEq, Eq)]
pub struct ChronologyDecision {
    pub id: String,
    pub prior_id: String,
    pub action: String,
    pub replacement_id: Option<String>,
    pub reason: String,
    pub source_revision_id: Option<String>,
}

// Permanent append-only record, never an UPDATE or DELETE of source history.
pub fn decide_anchor(
    db: &Connection,
    id: &str,
    universe_id: &str,
    prior_anchor_id: &str,
    action: &str,
    replacement_anchor_id: Option<&str>,
    reason: &str,
    source_revision_id: Option<&str>,
) -> Result<()> {
    db.execute(
        "INSERT INTO world_time_anchor_decisions
          (id,universe_id,prior_anchor_id,action,replacement_anchor_id,reason,source_revision_id)
         VALUES (?1,?2,?3,?4,?5,?6,?7)",
        params![
            id, universe_id, prior_anchor_id, action, replacement_anchor_id, reason,
            source_revision_id
        ],
    )?;
    Ok(())
}

pub fn decide_precedence(
    db: &Connection,
    id: &str,
    universe_id: &str,
    prior_precedence_id: &str,
    action: &str,
    replacement_precedence_id: Option<&str>,
    reason: &str,
    source_revision_id: Option<&str>,
) -> Result<()> {
    db.execute(
        "INSERT INTO world_time_precedence_decisions
          (id,universe_id,prior_precedence_id,action,replacement_precedence_id,reason,source_revision_id)
         VALUES (?1,?2,?3,?4,?5,?6,?7)",
        params![
            id, universe_id, prior_precedence_id, action, replacement_precedence_id,
            reason, source_revision_id
        ],
    )?;
    Ok(())
}

// New anchor insertion and the superseding decision must commit together.
// The existing original anchor is never modified, even on failure.
pub fn supersede_anchor_atomically(
    db: &mut Connection,
    new_anchor: AnchorDraft<'_>,
    decision_id: &str,
    prior_anchor_id: &str,
    reason: &str,
    source_revision_id: Option<&str>,
) -> Result<()> {
    let tx = db.transaction()?;
    create_anchor(&tx, new_anchor)?;
    decide_anchor(
        &tx, decision_id, new_anchor.universe_id, prior_anchor_id,
        "supersede", Some(new_anchor.id), reason, source_revision_id,
    )?;
    tx.commit()
}

// Stable identifier ordering is display order only; never fictional time.
pub fn list_current_anchor_ids(db: &Connection, universe_id: &str) -> Result<Vec<String>> {
    let mut stmt = db.prepare(
        "SELECT a.id FROM world_time_anchors a
         WHERE a.universe_id=?1 AND NOT EXISTS(
             SELECT 1 FROM world_time_anchor_decisions d
             WHERE d.prior_anchor_id=a.id AND d.universe_id=a.universe_id
         ) ORDER BY a.id",
    )?;
    stmt.query_map([universe_id], |row| row.get(0))?.collect()
}

pub fn list_current_precedence_ids(db: &Connection, universe_id: &str) -> Result<Vec<String>> {
    let mut stmt = db.prepare(
        "SELECT p.id FROM world_time_precedences p
         WHERE p.universe_id=?1 AND NOT EXISTS(
             SELECT 1 FROM world_time_precedence_decisions d
             WHERE d.prior_precedence_id=p.id AND d.universe_id=p.universe_id
         ) ORDER BY p.id",
    )?;
    stmt.query_map([universe_id], |row| row.get(0))?.collect()
}

pub fn list_anchor_decisions(db: &Connection, universe_id: &str) -> Result<Vec<ChronologyDecision>> {
    let mut stmt = db.prepare(
        "SELECT id,prior_anchor_id,action,replacement_anchor_id,reason,source_revision_id
         FROM world_time_anchor_decisions WHERE universe_id=?1 ORDER BY id",
    )?;
    stmt.query_map([universe_id], |row| {
        Ok(ChronologyDecision {
            id: row.get(0)?,
            prior_id: row.get(1)?,
            action: row.get(2)?,
            replacement_id: row.get(3)?,
            reason: row.get(4)?,
            source_revision_id: row.get(5)?,
        })
    })?.collect()
}


#[derive(Debug, PartialEq, Eq)]
pub struct ActivePrecedence {
    pub id: String,
    pub before_anchor_id: String,
    pub after_anchor_id: String,
    pub origin: String,
}

// Authored replacement must reference an explicitly revoked old assertion;
// new factual graph edges are persisted in a separate immutable table.
pub fn restate_revoked_precedence(
    db: &Connection,
    id: &str,
    universe_id: &str,
    revoked_precedence_id: &str,
    before_anchor_id: &str,
    after_anchor_id: &str,
    reason: &str,
    source_revision_id: Option<&str>,
) -> Result<()> {
    db.execute(
        "INSERT INTO world_time_precedence_restatements
         (id,universe_id,revoked_precedence_id,before_anchor_id,after_anchor_id,reason,source_revision_id)
         VALUES (?1,?2,?3,?4,?5,?6,?7)",
        params![
            id, universe_id, revoked_precedence_id, before_anchor_id,
            after_anchor_id, reason, source_revision_id
        ],
    )?;
    Ok(())
}


#[derive(Debug, PartialEq, Eq)]
pub struct RestatementHistory {
    pub id: String,
    pub revoked_precedence_id: String,
    pub before_anchor_id: String,
    pub after_anchor_id: String,
    pub reason: String,
    pub revocation_id: Option<String>,
    pub revocation_reason: Option<String>,
}

// A correction is never silently deleted; one append-only decision retires it.
pub fn revoke_restatement(
    db: &Connection,
    id: &str,
    universe_id: &str,
    restatement_id: &str,
    reason: &str,
    source_revision_id: Option<&str>,
) -> Result<()> {
    db.execute(
        "INSERT INTO world_time_restatement_revocations
         (id,universe_id,restatement_id,reason,source_revision_id)
         VALUES (?1,?2,?3,?4,?5)",
        params![id, universe_id, restatement_id, reason, source_revision_id],
    )?;
    Ok(())
}

// Full audit log includes retired restatements. It is NOT sorted by time.
pub fn list_restatement_history(
    db: &Connection,
    universe_id: &str,
) -> Result<Vec<RestatementHistory>> {
    let mut stmt = db.prepare(
        "SELECT t.id,t.revoked_precedence_id,t.before_anchor_id,t.after_anchor_id,
                t.reason,d.id,d.reason
         FROM world_time_precedence_restatements t
         LEFT JOIN world_time_restatement_revocations d
                ON d.restatement_id=t.id AND d.universe_id=t.universe_id
         WHERE t.universe_id=?1 ORDER BY t.id",
    )?;
    stmt.query_map([universe_id], |row| {
        Ok(RestatementHistory {
            id: row.get(0)?,
            revoked_precedence_id: row.get(1)?,
            before_anchor_id: row.get(2)?,
            after_anchor_id: row.get(3)?,
            reason: row.get(4)?,
            revocation_id: row.get(5)?,
            revocation_reason: row.get(6)?,
        })
    })?.collect()
}

// Reflects active partial-order assertions, not a chronological total order.
// The original legacy and corrected assertions remain separately inspectable.
pub fn list_active_precedence_graph(
    db: &Connection,
    universe_id: &str,
) -> Result<Vec<ActivePrecedence>> {
    let mut stmt = db.prepare(
        "SELECT p.id,p.before_anchor_id,p.after_anchor_id,'legacy'
         FROM world_time_precedences p
         WHERE p.universe_id=?1
           AND NOT EXISTS (
               SELECT 1 FROM world_time_precedence_decisions d
               WHERE d.prior_precedence_id=p.id
           )
           AND NOT EXISTS (
               SELECT 1 FROM world_time_anchor_decisions d
               WHERE d.universe_id=p.universe_id AND
                     d.prior_anchor_id IN (p.before_anchor_id,p.after_anchor_id)
           )
         UNION ALL
         SELECT t.id,t.before_anchor_id,t.after_anchor_id,'restatement'
         FROM world_time_precedence_restatements t
         WHERE t.universe_id=?1
           AND NOT EXISTS (
               SELECT 1 FROM world_time_restatement_revocations d
               WHERE d.restatement_id=t.id AND d.universe_id=t.universe_id
           )
           AND NOT EXISTS (
               SELECT 1 FROM world_time_anchor_decisions d
               WHERE d.universe_id=t.universe_id AND
                     d.prior_anchor_id IN (t.before_anchor_id,t.after_anchor_id)
           )
         ORDER BY 1",
    )?;
    stmt.query_map([universe_id], |row| {
        Ok(ActivePrecedence {
            id: row.get(0)?,
            before_anchor_id: row.get(1)?,
            after_anchor_id: row.get(2)?,
            origin: row.get(3)?,
        })
    })?.collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::database;

    const V7_SQL: &str = include_str!("../sql/m3_1_world_time_v7_candidate.sql");
    const DECISION_SQL: &str = include_str!("../sql/m3_2_chronology_decisions_candidate.sql");
    const RESTATEMENT_SQL: &str = include_str!("../sql/m3_2_active_precedence_candidate.sql");
    const RESTATEMENT_REVOCATION_SQL: &str = include_str!("../sql/m3_2_restatement_revocations_candidate.sql");

    fn isolated_v7() -> Connection {
        let mut db = Connection::open_in_memory().expect("in-memory only");
        database::configure_connection(&db).expect("foreign keys on");
        assert_eq!(database::run_migrations(&mut db).expect("legacy v6"), 6);
        // Deliberately stage the candidate only inside a new in-memory fixture.
        let tx = db.transaction().expect("isolated transaction");
        tx.execute_batch(V7_SQL).expect("candidate");
        tx.execute_batch(DECISION_SQL).expect("isolated M3.2 decision candidate");
        tx.execute_batch(RESTATEMENT_SQL).expect("isolated active-edge candidate");
        tx.execute_batch(RESTATEMENT_REVOCATION_SQL).expect("isolated correction retirement");
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

    #[test]
    fn revocation_is_append_only_and_historical_rows_remain() {
        let db=isolated_v7(); universe(&db,"u1"); universe(&db,"u2");
        create_anchor(&db,unknown("a","u1")).unwrap();
        create_anchor(&db,unknown("b","u1")).unwrap();
        create_precedence(&db,"ab","u1","a","b","old assertion",None).unwrap();
        decide_anchor(&db,"d1","u1","a","revoke",None,"Human correction",None).unwrap();
        assert_eq!(list_anchors(&db,"u1").unwrap().len(),2);
        assert_eq!(list_current_anchor_ids(&db,"u1").unwrap(),vec!["b"]);
        assert_eq!(list_precedences(&db,"u1").unwrap().len(),1);
        assert_eq!(list_anchor_decisions(&db,"u1").unwrap()[0].action,"revoke");
        assert!(decide_anchor(&db,"d2","u1","a","revoke",None,"duplicate",None).is_err());
        assert!(decide_anchor(&db,"d3","u2","b","revoke",None,"wrong world",None).is_err());
        assert!(create_precedence(&db,"bad","u1","a","b","retired anchor",None).is_err());
        assert!(db.execute("UPDATE world_time_anchor_decisions SET reason='rewritten' WHERE id='d1'",[]).is_err());
        assert!(db.execute("DELETE FROM world_time_anchor_decisions WHERE id='d1'",[]).is_err());
        assert_eq!(list_current_anchor_ids(&db,"u2").unwrap(),Vec::<String>::new());
    }

    #[test]
    fn supersession_replaces_identity_without_changing_old_history() {
        let mut db=isolated_v7(); universe(&db,"u1"); universe(&db,"u2");
        create_anchor(&db,unknown("old","u1")).unwrap();
        supersede_anchor_atomically(
            &mut db,unknown("fresh","u1"),"decision1","old","Explicit replacement",None,
        ).unwrap();
        assert_eq!(list_current_anchor_ids(&db,"u1").unwrap(),vec!["fresh"]);
        assert_eq!(list_anchors(&db,"u1").unwrap().len(),2);
        assert_eq!(list_anchor_decisions(&db,"u1").unwrap()[0].replacement_id.as_deref(),Some("fresh"));
        assert!(decide_anchor(&db,"wrong","u2","old","revoke",None,"wrong world",None).is_err());
        // Atomic rollback: the replacement anchor must not linger after an
        // invalid second decision on an already retired anchor.
        let before=list_anchors(&db,"u1").unwrap().len();
        assert!(supersede_anchor_atomically(
            &mut db,unknown("uncommitted","u1"),"decision2","old","duplicate",None,
        ).is_err());
        assert_eq!(list_anchors(&db,"u1").unwrap().len(),before);
        assert!(decide_anchor(&db,"cycle","u1","fresh","supersede",Some("old"),"cycle",None).is_err());
        assert_eq!(list_current_anchor_ids(&db,"u1").unwrap(),vec!["fresh"]);
    }

    #[test]
    fn precedence_decisions_preserve_retracted_edges_without_cascade() {
        let db=isolated_v7(); universe(&db,"u1"); universe(&db,"u2");
        for id in ["a","b","c"] { create_anchor(&db,unknown(id,"u1")).unwrap(); }
        create_anchor(&db,unknown("foreign","u2")).unwrap();
        create_precedence(&db,"ab","u1","a","b","old",None).unwrap();
        create_precedence(&db,"bc","u1","b","c","new",None).unwrap();
        decide_precedence(&db,"r1","u1","ab","revoke",None,"Incorrect order",None).unwrap();
        assert_eq!(list_precedences(&db,"u1").unwrap().len(),2);
        assert_eq!(list_current_precedence_ids(&db,"u1").unwrap(),vec!["bc"]);
        assert!(decide_precedence(&db,"foreign","u2","bc","revoke",None,"wrong universe",None).is_err());
        assert!(decide_precedence(&db,"repeat","u1","ab","revoke",None,"duplicate",None).is_err());
        assert!(db.execute("DELETE FROM world_time_precedence_decisions WHERE id='r1'",[]).is_err());
        assert!(db.execute("DELETE FROM world_time_precedences WHERE id='ab'",[]).is_err());
        assert_eq!(list_precedences(&db,"u1").unwrap().len(),2);
        // Limitation of v7: raw cycle guard still includes retired edges.
        // A reverse edge may not be inserted, even after a decision.
        assert!(create_precedence(&db,"ba","u1","b","a","historical veto",None).is_err());
    }

    #[test]
    fn correction_revision_must_belong_to_original_universe() {
        let db=isolated_v7(); universe(&db,"u1"); universe(&db,"u2");
        db.execute_batch(
            "INSERT INTO novels(id,universe_id,title,sort_order) VALUES
                ('novel1','u1','First novel',0),('novel2','u2','Other novel',0);
             INSERT INTO chapters(id,novel_id,title,sort_order) VALUES
                ('chap1','novel1','Chapter',0),('chap2','novel2','Chapter',0);
             INSERT INTO scenes(id,chapter_id,title,sort_order) VALUES
                ('scene1','chap1','Scene',0),('scene2','chap2','Scene',0);
             INSERT INTO scene_text_revisions(id,scene_id,revision_number,content) VALUES
                ('u1r','scene1',1,'Original'),('u2r','scene2',1,'Other')"
        ).unwrap();
        create_anchor(&db,unknown("a","u1")).unwrap();
        create_anchor(&db,unknown("b","u1")).unwrap();
        create_precedence(&db,"ab","u1","a","b","old",None).unwrap();
        assert!(decide_anchor(&db,"wrong","u1","a","revoke",None,"reason",Some("u2r")).is_err());
        decide_anchor(&db,"good","u1","a","revoke",None,"reason",Some("u1r")).unwrap();
        assert!(decide_precedence(&db,"foreign","u1","ab","revoke",None,"reason",Some("u2r")).is_err());
        decide_precedence(&db,"local","u1","ab","revoke",None,"reason",Some("u1r")).unwrap();
    }


    #[test]
    fn reversed_edge_after_revocation_is_current_without_erasing_history() {
        let db=isolated_v7(); universe(&db,"u1"); universe(&db,"u2");
        for id in ["a","b","c"] { create_anchor(&db,unknown(id,"u1")).unwrap(); }
        create_anchor(&db,unknown("foreign","u2")).unwrap();
        create_precedence(&db,"ab","u1","a","b","original",None).unwrap();
        decide_precedence(&db,"revoke-ab","u1","ab","revoke",None,"human correction",None).unwrap();
        // The M3.1 table still rejects reverse history; the corrected graph
        // keeps the legacy row immutable and permits a separate new assertion.
        assert!(create_precedence(&db,"ba-legacy","u1","b","a","v7 veto",None).is_err());
        restate_revoked_precedence(
            &db,"ba-new","u1","ab","b","a","Explicit reverse",None,
        ).unwrap();
        assert_eq!(list_precedences(&db,"u1").unwrap().len(),1);
        assert!(list_current_precedence_ids(&db,"u1").unwrap().is_empty());
        let live=list_active_precedence_graph(&db,"u1").unwrap();
        assert_eq!(live,vec![ActivePrecedence{
            id:"ba-new".into(),before_anchor_id:"b".into(),
            after_anchor_id:"a".into(),origin:"restatement".into(),
        }]);
        assert!(list_active_precedence_graph(&db,"u2").unwrap().is_empty());
        assert!(db.execute("DELETE FROM world_time_precedence_restatements WHERE id='ba-new'",[]).is_err());
        assert!(db.execute("UPDATE world_time_precedence_restatements SET reason='change' WHERE id='ba-new'",[]).is_err());
    }

    #[test]
    fn restatement_is_scoped_and_must_reference_revoked_original() {
        let db=isolated_v7(); universe(&db,"u1"); universe(&db,"u2");
        for id in ["a","b","c"] { create_anchor(&db,unknown(id,"u1")).unwrap(); }
        create_anchor(&db,unknown("foreign","u2")).unwrap();
        create_precedence(&db,"ab","u1","a","b","original",None).unwrap();
        assert!(restate_revoked_precedence(
            &db,"r0","u1","ab","b","a","not yet revoked",None,
        ).is_err());
        decide_precedence(&db,"d","u1","ab","revoke",None,"correction",None).unwrap();
        assert!(restate_revoked_precedence(
            &db,"r1","u2","ab","foreign","foreign","wrong world",None,
        ).is_err());
        assert!(restate_revoked_precedence(
            &db,"r2","u1","ab","b","foreign","cross-world",None,
        ).is_err());
        assert!(restate_revoked_precedence(
            &db,"r3","u1","ab","b","b","self cycle",None,
        ).is_err());
        restate_revoked_precedence(&db,"r4","u1","ab","b","a","valid",None).unwrap();
        assert!(restate_revoked_precedence(
            &db,"r5","u1","ab","a","c","second correction",None,
        ).is_err());
        assert_eq!(list_active_precedence_graph(&db,"u1").unwrap().len(),1);
    }

    #[test]
    fn active_graph_cycle_rejects_restatement_and_legacy_backdoor() {
        let db=isolated_v7(); universe(&db,"u1");
        for id in ["a","b","c","d"] { create_anchor(&db,unknown(id,"u1")).unwrap(); }
        create_precedence(&db,"ab","u1","a","b","old",None).unwrap();
        create_precedence(&db,"ac","u1","a","c","another relation",None).unwrap();
        create_precedence(&db,"cb","u1","c","b","another relation",None).unwrap();
        decide_precedence(&db,"d","u1","ab","revoke",None,"wrong edge",None).unwrap();
        assert!(restate_revoked_precedence(
            &db,"bad-cycle","u1","ab","b","a","would create b-a-c-b",None,
        ).is_err());
        assert_eq!(list_active_precedence_graph(&db,"u1").unwrap().len(),2);
        // Newly authored raw v7 edges must also be checked against already
        // committed corrected-graph assertions.
        decide_precedence(&db,"ac-d","u1","ac","revoke",None,"remove path",None).unwrap();
        restate_revoked_precedence(&db,"ba","u1","ab","b","a","reverse is now safe",None).unwrap();
        // The old M3.1 guard ALLOWS this pair: its historical graph
        // has no path c -> d. The active graph DOES have c -> b -> a -> d,
        // so the new M3.2 trigger must veto d -> c to avoid a cycle.
        create_precedence(&db,"ad","u1","a","d","safe extension",None).unwrap();
        assert!(create_precedence(&db,"dc","u1","d","c","active-only cycle",None).is_err());
        assert_eq!(list_active_precedence_graph(&db,"u1").unwrap().len(),3);
    }

    #[test]
    fn retired_anchor_excludes_corrected_edge_from_active_projection() {
        let db=isolated_v7(); universe(&db,"u1");
        for id in ["a","b"] { create_anchor(&db,unknown(id,"u1")).unwrap(); }
        create_precedence(&db,"ab","u1","a","b","first",None).unwrap();
        decide_precedence(&db,"d","u1","ab","revoke",None,"reversed",None).unwrap();
        decide_anchor(&db,"anchor-retired","u1","b","revoke",None,"removed",None).unwrap();
        assert!(restate_revoked_precedence(
            &db,"no","u1","ab","b","a","retired endpoint",None,
        ).is_err());
        assert!(list_active_precedence_graph(&db,"u1").unwrap().is_empty());
    }


    #[test]
    fn second_order_restatement_revocation_is_append_only_and_hidden_from_current_graph() {
        let db = isolated_v7();
        universe(&db, "u1");
        universe(&db, "u2");
        for id in ["a", "b"] { create_anchor(&db, unknown(id, "u1")).unwrap(); }
        create_precedence(&db, "original", "u1", "a", "b", "Initial before", None).unwrap();
        decide_precedence(
            &db, "d0", "u1", "original", "revoke", None, "Author disagrees", None,
        ).unwrap();
        restate_revoked_precedence(
            &db, "correction", "u1", "original", "b", "a", "Reverse order", None,
        ).unwrap();
        assert_eq!(list_active_precedence_graph(&db, "u1").unwrap().len(), 1);
        assert_eq!(list_restatement_history(&db, "u1").unwrap().len(), 1);

        revoke_restatement(
            &db, "d1", "u1", "correction", "Author withdraws correction", None,
        ).unwrap();
        assert!(list_active_precedence_graph(&db, "u1").unwrap().is_empty());
        assert_eq!(list_precedences(&db, "u1").unwrap().len(), 1);
        let history = list_restatement_history(&db, "u1").unwrap();
        assert_eq!(history.len(), 1);
        assert_eq!(history[0].id, "correction");
        assert_eq!(history[0].revoked_precedence_id, "original");
        assert_eq!(history[0].revocation_id.as_deref(), Some("d1"));
        assert_eq!(
            history[0].revocation_reason.as_deref(),
            Some("Author withdraws correction"),
        );
        assert!(list_restatement_history(&db, "u2").unwrap().is_empty());
        assert!(revoke_restatement(&db, "d2", "u1", "correction", "Repeated", None).is_err());
        assert!(revoke_restatement(&db, "d3", "u2", "correction", "Wrong world", None).is_err());
        assert!(revoke_restatement(&db, "d4", "u1", "absent", "Missing", None).is_err());
        assert!(revoke_restatement(&db, "d5", "u1", "correction", "  ", None).is_err());
        assert!(db.execute(
            "UPDATE world_time_restatement_revocations SET reason='edited' WHERE id='d1'", [],
        ).is_err());
        assert!(db.execute(
            "DELETE FROM world_time_restatement_revocations WHERE id='d1'", [],
        ).is_err());
        // Unique original->restatement lineage still forbids silently
        // authoring another revision through the stage-4 table.
        assert!(restate_revoked_precedence(
            &db, "unsanctioned", "u1", "original", "a", "b",
            "No new lineage contract", None,
        ).is_err());
        assert_eq!(
            db.query_row("PRAGMA integrity_check", [], |row| row.get::<_, String>(0)).unwrap(),
            "ok",
        );
        let foreign_key_errors: i64 = db.query_row(
            "SELECT COUNT(*) FROM pragma_foreign_key_check", [], |row| row.get(0),
        ).unwrap();
        assert_eq!(foreign_key_errors, 0);
        assert_eq!(database::MAX_AUTOMATIC_MIGRATION_VERSION, 6);
    }

    #[test]
    fn second_order_decision_revision_must_be_same_universe_and_immutable() {
        let db = isolated_v7();
        universe(&db, "u1");
        universe(&db, "u2");
        db.execute_batch(
            "INSERT INTO novels(id,universe_id,title,sort_order) VALUES
                ('novel1','u1','One',0),('novel2','u2','Two',0);
             INSERT INTO chapters(id,novel_id,title,sort_order) VALUES
                ('chap1','novel1','First',0),('chap2','novel2','Second',0);
             INSERT INTO scenes(id,chapter_id,title,sort_order) VALUES
                ('scene1','chap1','First',0),('scene2','chap2','Second',0);
             INSERT INTO scene_text_revisions(id,scene_id,revision_number,content) VALUES
                ('local','scene1',1,'Original'),('foreign','scene2',1,'Foreign')",
        ).unwrap();
        create_anchor(&db, unknown("a", "u1")).unwrap();
        create_anchor(&db, unknown("b", "u1")).unwrap();
        create_precedence(&db, "ab", "u1", "a", "b", "Before", None).unwrap();
        decide_precedence(&db, "d0", "u1", "ab", "revoke", None, "Correction", None).unwrap();
        restate_revoked_precedence(&db, "ba", "u1", "ab", "b", "a", "Reversed", None).unwrap();
        assert!(revoke_restatement(
            &db, "foreign-decision", "u1", "ba", "Illegal source", Some("foreign"),
        ).is_err());
        assert!(list_restatement_history(&db, "u1").unwrap()[0].revocation_id.is_none());
        revoke_restatement(
            &db, "local-decision", "u1", "ba", "Same-Universe reason", Some("local"),
        ).unwrap();
        assert!(list_active_precedence_graph(&db, "u1").unwrap().is_empty());
    }


}
