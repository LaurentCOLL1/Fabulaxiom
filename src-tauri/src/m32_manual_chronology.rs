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



// Stage two: append-only author decisions on RAM-only candidate SQL (PR #35 lineage).
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



// Stage 3: explicit restatement of one revoked, immutable precedence; test-only.
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



// Stage four: test-only restatement withdrawal and immutable audit.
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



// Compilation is gated by #[cfg(test)] in lib.rs. Test databases exist only in RAM.

#[cfg(test)]
mod tests {
    use super::*;
    use crate::database;

    const V7_CANDIDATE: &str = include_str!("../sql/m3_1_world_time_v7_candidate.sql");
    const M32_DECISIONS: &str = include_str!("../sql/m3_2_chronology_decisions_candidate.sql");
    const M32_RESTATEMENTS: &str = include_str!("../sql/m3_2_active_precedence_candidate.sql");
    const M32_REVOCATIONS: &str = include_str!("../sql/m3_2_restatement_revocations_candidate.sql");

    fn fixture() -> Connection {
        let mut db = Connection::open_in_memory().expect("RAM only");
        database::configure_connection(&db).expect("foreign keys enabled");
        assert_eq!(database::run_migrations(&mut db).expect("v6 in RAM"), 6);
        db.execute(
            "INSERT INTO universes(id,name) VALUES ('u1','Imaginaire A'),('u2','Imaginaire B')", []
        ).expect("two invented universes");
        db.execute_batch(V7_CANDIDATE).expect("v7 candidate in disposable RAM");
        db.execute_batch(M32_DECISIONS).expect("decisions only in disposable RAM");
        db.execute_batch(M32_RESTATEMENTS).expect("restatement schema only in RAM");
        db.execute_batch(M32_REVOCATIONS).expect("withdrawal only in invented RAM");
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
        // The v6 universe name is outside M3.2 immutable-anchor contract.
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
    #[test]
    fn explicit_anchor_revocation_keeps_immutable_history() {
        let db=fixture();
        create_anchor(&db,draft("a","u1","unknown")).unwrap();
        create_anchor(&db,draft("b","u1","relative")).unwrap();
        decide_anchor(&db,"d1","u1","a","revoke",None,"L'auteur corrige",None).unwrap();
        assert_eq!(list_current_anchor_ids(&db,"u1").unwrap(),vec!["b".to_string()]);
        assert_eq!(list_anchors(&db,"u1").unwrap().len(),2);
        let decisions=list_anchor_decisions(&db,"u1").unwrap();
        assert_eq!(decisions.len(),1);
        assert_eq!(decisions[0].action,"revoke");
        assert!(decide_anchor(&db,"d2","u1","a","revoke",None,"double",None).is_err());
        assert!(db.execute("DELETE FROM world_time_anchor_decisions WHERE id='d1'",[]).is_err());
        assert!(db.execute("UPDATE world_time_anchor_decisions SET reason='new' WHERE id='d1'",[]).is_err());
    }

    #[test]
    fn atomic_anchor_supersession_updates_current_selection_not_original() {
        let mut db=fixture();
        create_anchor(&db,draft("old","u1","unknown")).unwrap();
        supersede_anchor_atomically(&mut db,draft("new","u1","relative"),
            "decision","old","Decision manuelle",None).unwrap();
        assert_eq!(list_current_anchor_ids(&db,"u1").unwrap(),vec!["new".to_string()]);
        assert_eq!(list_anchors(&db,"u1").unwrap().len(),2);
        let decision=&list_anchor_decisions(&db,"u1").unwrap()[0];
        assert_eq!(decision.replacement_id.as_deref(),Some("new"));
        assert_eq!(decision.prior_id,"old");
        assert_eq!(database::current_schema_version(&db).unwrap(),6);
    }

    #[test]
    fn failed_atomic_supersession_rolls_back_new_anchor_across_universes() {
        let mut db=fixture();
        create_anchor(&db,draft("prior","u1","unknown")).unwrap();
        assert!(supersede_anchor_atomically(&mut db,draft("foreign","u2","unknown"),
            "invalid","prior","Cross universe",None).is_err());
        assert!(list_anchors(&db,"u2").unwrap().is_empty());
        assert!(list_anchor_decisions(&db,"u1").unwrap().is_empty());
        assert_eq!(list_current_anchor_ids(&db,"u1").unwrap(),vec!["prior".to_string()]);
    }

    #[test]
    fn explicit_precedence_revocation_keeps_old_authored_edge() {
        let db=fixture();
        create_anchor(&db,draft("a","u1","unknown")).unwrap();
        create_anchor(&db,draft("b","u1","unknown")).unwrap();
        create_precedence(&db,"edge","u1","a","b","author before",None).unwrap();
        assert_eq!(list_current_precedence_ids(&db,"u1").unwrap(),vec!["edge".to_string()]);
        decide_precedence(&db,"d","u1","edge","revoke",None,"Author correction",None).unwrap();
        assert!(list_current_precedence_ids(&db,"u1").unwrap().is_empty());
        assert_eq!(list_precedences(&db,"u1").unwrap().len(),1);
        assert!(decide_precedence(&db,"twice","u1","edge","revoke",None,"double",None).is_err());
        assert!(db.execute("DELETE FROM world_time_precedence_decisions WHERE id='d'",[]).is_err());
    }

    #[test]
    fn retired_anchors_cannot_receive_new_edges() {
        let db=fixture();
        create_anchor(&db,draft("a","u1","unknown")).unwrap();
        create_anchor(&db,draft("b","u1","unknown")).unwrap();
        decide_anchor(&db,"retire","u1","a","revoke",None,"Retired",None).unwrap();
        assert!(create_precedence(&db,"edge","u1","a","b","invalid history",None).is_err());
        assert!(list_precedences(&db,"u1").unwrap().is_empty());
    }

    #[test]
    fn decision_validation_rejects_cross_world_missing_and_wrong_actions() {
        let db=fixture();
        create_anchor(&db,draft("u1a","u1","unknown")).unwrap();
        create_anchor(&db,draft("u2a","u2","unknown")).unwrap();
        assert!(decide_anchor(&db,"foreign","u2","u1a","revoke",None,"wrong",None).is_err());
        assert!(decide_anchor(&db,"missing","u1","unknown","revoke",None,"missing",None).is_err());
        assert!(decide_anchor(&db,"action","u1","u1a","approve",None,"invalid",None).is_err());
        assert!(decide_anchor(&db,"replacement","u1","u1a","supersede",Some("u2a"),"cross",None).is_err());
        create_precedence(&db,"p","u1","u1a","u1a","self",None).expect_err("self edge rejected");
        create_anchor(&db,draft("u1b","u1","unknown")).unwrap();
        create_precedence(&db,"p","u1","u1a","u1b","authored",None).unwrap();
        assert!(decide_precedence(&db,"wrong-owner","u2","p","revoke",None,"other",None).is_err());
        assert!(decide_precedence(&db,"wrong-action","u1","p","approve",None,"invalid",None).is_err());
    }

    #[test]
    fn restatement_requires_explicit_same_universe_revoked_edge() {
        let db=fixture();
        for id in ["a","b","c"] { create_anchor(&db,draft(id,"u1","unknown")).unwrap(); }
        create_anchor(&db,draft("foreign","u2","unknown")).unwrap();
        create_precedence(&db,"old","u1","a","b","Auteur: avant",None).unwrap();
        assert!(restate_revoked_precedence(&db,"attempt","u1","old","a","c","not revoked",None).is_err());
        decide_precedence(&db,"revoke","u1","old","revoke",None,"Auteur corrige",None).unwrap();
        restate_revoked_precedence(&db,"new","u1","old","a","c","A avant C",None).unwrap();
        let n:i64=db.query_row("SELECT COUNT(*) FROM world_time_precedence_restatements WHERE universe_id='u1'",[],|r|r.get(0)).unwrap();
        assert_eq!(n,1);
        assert_eq!(list_precedences(&db,"u1").unwrap().len(),1);
        assert!(list_current_precedence_ids(&db,"u1").unwrap().is_empty());
        assert!(restate_revoked_precedence(&db,"foreign","u2","old","foreign","foreign","cross",None).is_err());
    }

    #[test]
    fn restatement_rejects_reverse_cycle_against_current_human_edges() {
        let db=fixture();
        for id in ["a","b","c"] { create_anchor(&db,draft(id,"u1","unknown")).unwrap(); }
        create_precedence(&db,"ab","u1","a","b","first",None).unwrap();
        create_precedence(&db,"bc","u1","b","c","second",None).unwrap();
        decide_precedence(&db,"withdraw-ab","u1","ab","revoke",None,"revision",None).unwrap();
        assert!(restate_revoked_precedence(&db,"cycle","u1","ab","c","b","reverse cycle",None).is_err());
        assert!(restate_revoked_precedence(&db,"self","u1","ab","b","b","self",None).is_err());
        let n:i64=db.query_row("SELECT COUNT(*) FROM world_time_precedence_restatements",[],|r|r.get(0)).unwrap();
        assert_eq!(n,0);
    }

    #[test]
    fn restatement_is_immutable_and_original_can_only_be_rewritten_once() {
        let db=fixture();
        for id in ["a","b","c"] { create_anchor(&db,draft(id,"u1","unknown")).unwrap(); }
        create_precedence(&db,"original","u1","a","b","authored",None).unwrap();
        decide_precedence(&db,"revoke","u1","original","revoke",None,"withdraw",None).unwrap();
        restate_revoked_precedence(&db,"correction","u1","original","a","c","corrected",None).unwrap();
        assert!(restate_revoked_precedence(&db,"again","u1","original","c","a","fork",None).is_err());
        assert!(db.execute("UPDATE world_time_precedence_restatements SET reason='changed' WHERE id='correction'",[]).is_err());
        assert!(db.execute("DELETE FROM world_time_precedence_restatements WHERE id='correction'",[]).is_err());
        assert_eq!(list_precedences(&db,"u1").unwrap().len(),1);
    }

    #[test]
    fn retired_anchor_and_duplicate_live_relation_cannot_be_restatements() {
        let db=fixture();
        for id in ["a","b","c","d"] { create_anchor(&db,draft(id,"u1","unknown")).unwrap(); }
        create_precedence(&db,"original","u1","a","b","authored",None).unwrap();
        create_precedence(&db,"active","u1","c","d","authored",None).unwrap();
        decide_precedence(&db,"withdraw","u1","original","revoke",None,"withdraw",None).unwrap();
        assert!(restate_revoked_precedence(&db,"duplicate","u1","original","c","d","already live",None).is_err());
        decide_anchor(&db,"retired","u1","a","revoke",None,"retired anchor",None).unwrap();
        assert!(restate_revoked_precedence(&db,"historical","u1","original","a","d","retired",None).is_err());
    }

    #[test]
    fn raw_precedence_insert_cannot_bypass_restated_active_cycle() {
        let db=fixture();
        for id in ["a","b","c"] { create_anchor(&db,draft(id,"u1","unknown")).unwrap(); }
        create_precedence(&db,"original","u1","a","b","authored",None).unwrap();
        decide_precedence(&db,"withdraw","u1","original","revoke",None,"withdraw",None).unwrap();
        restate_revoked_precedence(&db,"corrected","u1","original","b","c","rephrase",None).unwrap();
        assert!(create_precedence(&db,"cycle","u1","c","b","must veto",None).is_err());
        let n:i64=db.query_row("SELECT COUNT(*) FROM world_time_precedences WHERE id='cycle'",[],|r|r.get(0)).unwrap();
        assert_eq!(n,0);
        assert_eq!(database::current_schema_version(&db).unwrap(),6);
    }

    fn sample_restatement(db: &Connection) {
        for id in ["a","b","c"] { create_anchor(db,draft(id,"u1","unknown")).unwrap(); }
        create_precedence(db,"old","u1","a","b","human",None).unwrap();
        decide_precedence(db,"wd-old","u1","old","revoke",None,"human",None).unwrap();
        restate_revoked_precedence(db,"corrected","u1","old","a","c","human",None).unwrap();
    }

    #[test]
    fn restatement_withdrawal_is_historical_and_never_reinstates_legacy_edge() {
        let db=fixture(); sample_restatement(&db);
        revoke_restatement(&db,"withdraw-correction","u1","corrected","human withdraw",None).unwrap();
        let history=list_restatement_history(&db,"u1").unwrap();
        assert_eq!(history.len(),1);
        assert_eq!(history[0].revocation_id.as_deref(),Some("withdraw-correction"));
        assert_eq!(history[0].revocation_reason.as_deref(),Some("human withdraw"));
        assert_eq!(history[0].revoked_precedence_id,"old");
        assert_eq!(list_precedences(&db,"u1").unwrap().len(),1);
        assert!(list_current_precedence_ids(&db,"u1").unwrap().is_empty());
    }

    #[test]
    fn restatement_withdrawal_refuses_foreign_unknown_and_duplicate_targets() {
        let db=fixture(); sample_restatement(&db);
        assert!(revoke_restatement(&db,"wrong","u2","corrected","wrong universe",None).is_err());
        assert!(revoke_restatement(&db,"missing","u1","no-such-id","missing",None).is_err());
        revoke_restatement(&db,"one","u1","corrected","withdraw",None).unwrap();
        assert!(revoke_restatement(&db,"two","u1","corrected","duplicate",None).is_err());
        assert!(list_restatement_history(&db,"u2").unwrap().is_empty());
    }

    #[test]
    fn restatement_withdrawal_records_are_immutable_and_do_not_migrate_disk() {
        let db=fixture(); sample_restatement(&db);
        revoke_restatement(&db,"withdraw","u1","corrected","immutable",None).unwrap();
        assert!(db.execute("UPDATE world_time_restatement_revocations SET reason='changed'",[]).is_err());
        assert!(db.execute("DELETE FROM world_time_restatement_revocations",[]).is_err());
        assert_eq!(list_restatement_history(&db,"u1").unwrap().len(),1);
        assert_eq!(database::current_schema_version(&db).unwrap(),6);
    }

    #[test]
    fn other_universe_remains_independent_after_fictional_restatement_withdrawal() {
        let db=fixture(); sample_restatement(&db);
        create_anchor(&db,draft("other","u2","unknown")).unwrap();
        revoke_restatement(&db,"withdraw","u1","corrected","human",None).unwrap();
        assert_eq!(list_anchors(&db,"u2").unwrap().len(),1);
        assert!(list_restatement_history(&db,"u2").unwrap().is_empty());
        assert!(list_current_precedence_ids(&db,"u1").unwrap().is_empty());
    }

}
