//! M3.1 isolated v7-candidate checks. This module is only built during tests.
 //! The operator's v6 active database MUST NOT be migrated by these fixtures.
use crate::database;
use rusqlite::{params, Connection};

const CANDIDATE_SQL: &str = include_str!("../sql/m3_1_world_time_v7_candidate.sql");

fn v6() -> Connection {
    let mut db = Connection::open_in_memory().expect("memory");
    database::configure_connection(&db).expect("foreign keys");
    assert_eq!(database::run_migrations(&mut db).expect("v6 migrations"), 6);
    db
}

fn stage_isolated(db: &mut Connection) {
    let tx = db.transaction().expect("begin isolated schema transaction");
    tx.execute_batch(CANDIDATE_SQL).expect("candidate SQL");
    tx.commit().expect("commit isolated schema");
    // Deliberately no v7 row in schema_migrations, and no production migration.
    assert_eq!(database::current_schema_version(db).expect("version"), 6);
}

fn universe(db: &Connection, id: &str) {
    db.execute(
        "INSERT INTO universes(id,name) VALUES (?1,?2)",
        params![id, format!("Universe {id}")],
    ).expect("universe");
}

fn calendar(db: &Connection, id: &str, owner: &str) {
    db.execute(
        "INSERT INTO fictional_calendars(id,universe_id,name,definition_text)
         VALUES (?1,?2,'Solar cycles','Locally authored units; no real-world epoch')",
        params![id,owner],
    ).expect("calendar");
}

fn anchor(db: &Connection, id: &str, owner: &str) {
    db.execute(
        "INSERT INTO world_time_anchors(id,universe_id,time_kind) VALUES (?1,?2,'unknown')",
        params![id,owner],
    ).expect("unknown-time anchor");
}

fn precedence(db: &Connection, id: &str, before: &str, after: &str) -> rusqlite::Result<usize> {
    db.execute(
        "INSERT INTO world_time_precedences
         (id,universe_id,before_anchor_id,after_anchor_id,reason)
         VALUES (?1,'u1',?2,?3,'Human declared order')",
        params![id,before,after],
    )
}

#[test]
fn v6_runtime_remains_v6_until_explicit_operator_gate() {
    let db = v6();
    assert_eq!(database::CURRENT_SCHEMA_VERSION, 6);
    for name in ["fictional_calendars", "world_time_anchors", "world_time_precedences"] {
        let exists: i64 = db.query_row(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name=?1",
            [name], |r| r.get(0),
        ).expect("schema");
        assert_eq!(exists, 0, "candidate table must not appear on app launch");
    }
}

#[test]
fn isolated_candidate_adds_three_strict_tables_without_rewriting_v6() {
    let mut db = v6();
    universe(&db,"u1");
    db.execute(
        "INSERT INTO narrative_entities(id,universe_id,kind,name)
         VALUES ('actor','u1','character','Alpha')", [],
    ).expect("v6 entity");
    db.execute(
        "INSERT INTO narrative_facts(id,entity_id,universe_id,fact_key,fact_value,provenance_kind)
         VALUES ('fact1','actor','u1','status','present','unsourced')", [],
    ).expect("v6 fact");
    let before: String = db.query_row(
        "SELECT fact_value FROM narrative_facts WHERE id='fact1'",[],|r|r.get(0)
    ).expect("fact before");
    stage_isolated(&mut db);
    let strict: i64 = db.query_row(
        "SELECT COUNT(*) FROM pragma_table_list
         WHERE name IN ('fictional_calendars','world_time_anchors','world_time_precedences')
           AND strict=1", [], |r|r.get(0),
    ).expect("strict count");
    assert_eq!(strict,3);
    let after: String = db.query_row(
        "SELECT fact_value FROM narrative_facts WHERE id='fact1'",[],|r|r.get(0)
    ).expect("fact after");
    assert_eq!(before,after);
    assert_eq!(db.query_row("PRAGMA integrity_check",[],|r|r.get::<_,String>(0)).unwrap(),"ok");
    assert_eq!(db.query_row("SELECT COUNT(*) FROM pragma_foreign_key_check",[],|r|r.get::<_,i64>(0)).unwrap(),0);
}

#[test]
fn fictitious_dates_are_never_converted_to_gregorian_or_total_order() {
    let mut db=v6();
    universe(&db,"u1");
    stage_isolated(&mut db);
    calendar(&db,"fiction1","u1");
    assert!(db.execute(
        "UPDATE fictional_calendars SET definition_text='rewritten rules'
         WHERE id='fiction1'", []
    ).is_err(), "no silent calendar reinterpretation");
    assert!(db.execute(
        "DELETE FROM fictional_calendars WHERE id='fiction1'", []
    ).is_err(), "calendar definition history must be preserved");
    db.execute(
        "INSERT INTO world_time_anchors
         (id,universe_id,calendar_id,time_kind,exact_label,precision_text)
         VALUES ('a','u1','fiction1','exact','Cycle XII, Bloom 3','day')",[]
    ).expect("raw fictional exact");
    db.execute(
        "INSERT INTO world_time_anchors
         (id,universe_id,calendar_id,time_kind,window_start_text,precision_text)
         VALUES ('b','u1','fiction1','approximate','Before second eclipse','season')",[]
    ).expect("open approximate window");
    anchor(&db,"c","u1");
    db.execute(
        "INSERT INTO world_time_anchors(id,universe_id,time_kind)
         VALUES ('d','u1','relative')",[]
    ).expect("relative");
    let count: i64=db.query_row("SELECT COUNT(*) FROM world_time_anchors",[],|r|r.get(0)).unwrap();
    assert_eq!(count,4);
    let comparisons:i64=db.query_row("SELECT COUNT(*) FROM world_time_precedences",[],|r|r.get(0)).unwrap();
    assert_eq!(comparisons,0);
    for sql in [
        "INSERT INTO world_time_anchors(id,universe_id,time_kind,exact_label) VALUES ('bad1','u1','exact','today')",
        "INSERT INTO world_time_anchors(id,universe_id,time_kind,calendar_id,exact_label) VALUES ('bad2','u1','unknown','fiction1','Cycle I')",
        "INSERT INTO world_time_anchors(id,universe_id,time_kind,calendar_id) VALUES ('bad3','u1','approximate','fiction1')",
    ] {
        assert!(db.execute(sql,[]).is_err(),"{sql}");
    }
}

#[test]
fn foreign_keys_reject_cross_universe_calendar_anchor_and_precedence() {
    let mut db=v6(); universe(&db,"u1"); universe(&db,"u2");
    stage_isolated(&mut db);
    calendar(&db,"one","u1"); calendar(&db,"two","u2");
    assert!(db.execute(
        "INSERT INTO world_time_anchors(id,universe_id,calendar_id,time_kind,exact_label)
         VALUES ('bad','u2','one','exact','Cycle X')", []
    ).is_err());
    anchor(&db,"a","u1"); anchor(&db,"b","u2");
    assert!(db.execute(
        "INSERT INTO world_time_precedences
         (id,universe_id,before_anchor_id,after_anchor_id,reason)
         VALUES ('cross','u1','a','b','invalid')", []
    ).is_err());
}

#[test]
fn event_links_require_event_kind_not_display_name() {
    let mut db=v6(); universe(&db,"u1"); universe(&db,"u2");
    db.execute(
        "INSERT INTO narrative_entities(id,universe_id,kind,name)
         VALUES ('event1','u1','event','Same name'),('actor1','u1','character','Same name'),
                ('event2','u2','event','Same name')", []
    ).expect("entities");
    stage_isolated(&mut db);
    assert!(db.execute(
        "INSERT INTO world_time_anchors(id,universe_id,time_kind,event_entity_id)
         VALUES ('bad-kind','u1','unknown','actor1')", []
    ).is_err());
    assert!(db.execute(
        "INSERT INTO world_time_anchors(id,universe_id,time_kind,event_entity_id)
         VALUES ('bad-world','u1','unknown','event2')", []
    ).is_err());
    db.execute(
        "INSERT INTO world_time_anchors(id,universe_id,time_kind,event_entity_id)
         VALUES ('good','u1','unknown','event1')", []
    ).expect("event is same universe");
}

#[test]
fn original_revision_ownership_is_independent_of_current_head() {
    let mut db=v6(); universe(&db,"u1"); universe(&db,"u2");
    db.execute_batch(
        "INSERT INTO novels(id,universe_id,title,sort_order)
         VALUES ('n2','u2','Other novel',0);
         INSERT INTO chapters(id,novel_id,title,sort_order) VALUES ('c2','n2','C',0);
         INSERT INTO scenes(id,chapter_id,title,sort_order) VALUES ('s2','c2','Scene',0);
         INSERT INTO scene_text_revisions(id,scene_id,revision_number,content)
         VALUES ('r2','s2',1,'Original text');"
    ).expect("existing historical revision");
    stage_isolated(&mut db);
    assert!(db.execute(
        "INSERT INTO world_time_anchors
         (id,universe_id,time_kind,source_revision_id)
         VALUES ('wrong','u1','unknown','r2')",[]
    ).is_err());
    db.execute(
        "INSERT INTO world_time_anchors
         (id,universe_id,time_kind,source_revision_id)
         VALUES ('right','u2','unknown','r2')",[]
    ).expect("same-universe historical revision");
}

#[test]
fn before_after_cycles_and_self_edges_fail_without_changing_history() {
    let mut db=v6(); universe(&db,"u1"); stage_isolated(&mut db);
    for id in ["a","b","c","orphan"] { anchor(&db,id,"u1"); }
    precedence(&db,"ab","a","b").expect("a before b");
    precedence(&db,"bc","b","c").expect("b before c");
    assert!(precedence(&db,"ca","c","a").is_err(),"cycle across path");
    assert!(precedence(&db,"aa","a","a").is_err(),"self-loop");
    assert!(precedence(&db,"dup","a","b").is_err(),"duplicate precedence");
    let edges:i64=db.query_row("SELECT COUNT(*) FROM world_time_precedences",[],|r|r.get(0)).unwrap();
    assert_eq!(edges,2);
    precedence(&db,"oc","orphan","c").expect("separate acyclic component");
    assert!(db.execute(
        "UPDATE world_time_precedences SET reason='silent rewrite' WHERE id='ab'",[]
    ).is_err());
    assert!(db.execute(
        "DELETE FROM world_time_anchors WHERE id='a'",[]
    ).is_err());
}

#[test]
fn schema_transaction_rolls_back_fully_on_invalid_candidate_reapply() {
    let mut db=v6(); stage_isolated(&mut db);
    let tx=db.transaction().expect("transaction");
    assert!(tx.execute_batch(CANDIDATE_SQL).is_err(),"no accidental second application");
    drop(tx); // rollback
    assert_eq!(database::current_schema_version(&db).unwrap(),6);
    let count:i64=db.query_row(
        "SELECT COUNT(*) FROM sqlite_master WHERE type='table'
         AND name='fictional_calendars'",[],|r|r.get(0)
    ).unwrap();
    assert_eq!(count,1);
}


#[test]
fn populated_v6_m2_citations_and_human_review_are_preserved_byte_for_byte() {
    let mut db = v6();
    // These are immutable, existing M2 records, not new M3 interpretations.
    db.execute_batch(r#"
        INSERT INTO universes(id,name) VALUES ('u1','Moonlands');
        INSERT INTO novels(id,universe_id,title,sort_order)
            VALUES ('n1','u1','Archive',0);
        INSERT INTO chapters(id,novel_id,title,sort_order)
            VALUES ('c1','n1','Chapter',0);
        INSERT INTO scenes(id,chapter_id,title,sort_order)
            VALUES ('s1','c1','Scene',0);
        INSERT INTO scene_text_revisions(id,scene_id,revision_number,content)
            VALUES ('r1','s1',1,'Éclipse 🌕 au lac');
        INSERT INTO scene_revision_heads(scene_id,revision_id) VALUES ('s1','r1');
        INSERT INTO narrative_entities(id,universe_id,kind,name)
            VALUES ('e1','u1','event','Éclipse');
        INSERT INTO narrative_facts(id,entity_id,universe_id,fact_key,fact_value,provenance_kind)
            VALUES ('f1','e1','u1','signal','Éclipse','sourced');
        INSERT INTO fact_sources(id,fact_id,universe_id,revision_id,start_byte,end_byte,quoted_text)
            VALUES ('source1','f1','u1','r1',0,8,'Éclipse');
        INSERT INTO fact_review_events
            (id,fact_id,universe_id,revision_number,previous_status,next_status,
             action_kind,actor_kind,reviewer_label,human_confirmation,reason)
            VALUES
            ('review1','f1','u1',1,'draft','suggestion','set_status','human',
             'operator',0,'Human suggestion'),
            ('review2','f1','u1',2,'suggestion','canon','approve_canon','human',
             'operator',1,'Reviewed exact source');
    "#).expect("populated M2 v6 baseline");

    let original: (String,String,String,i64,i64,i64) = db.query_row(
        "SELECT r.content, s.quoted_text, h.revision_id, s.end_byte,
                (SELECT COUNT(*) FROM fact_review_events),
                (SELECT COUNT(*) FROM schema_migrations)
         FROM scene_text_revisions r
         JOIN fact_sources s ON s.revision_id=r.id
         JOIN scene_revision_heads h ON h.scene_id=r.scene_id
         WHERE r.id='r1'",
        [], |row| Ok((row.get(0)?,row.get(1)?,row.get(2)?,
                     row.get(3)?,row.get(4)?,row.get(5)?))
    ).expect("before candidate");
    assert_eq!(original.1.as_bytes(), "Éclipse".as_bytes());
    assert_eq!(original.3, 8);
    assert_eq!(original.4, 2);
    assert_eq!(original.5, 6);

    stage_isolated(&mut db);
    let retained: (String,String,String,i64,i64,i64) = db.query_row(
        "SELECT r.content, s.quoted_text, h.revision_id, s.end_byte,
                (SELECT COUNT(*) FROM fact_review_events),
                (SELECT COUNT(*) FROM schema_migrations)
         FROM scene_text_revisions r
         JOIN fact_sources s ON s.revision_id=r.id
         JOIN scene_revision_heads h ON h.scene_id=r.scene_id
         WHERE r.id='r1'",
        [], |row| Ok((row.get(0)?,row.get(1)?,row.get(2)?,
                     row.get(3)?,row.get(4)?,row.get(5)?))
    ).expect("after candidate");
    assert_eq!(retained, original, "old M2 rows must be preserved exactly");
    let canon_status: String = db.query_row(
        "SELECT next_status FROM fact_review_events
         WHERE fact_id='f1' ORDER BY revision_number DESC LIMIT 1",
        [], |row| row.get(0)
    ).expect("human canon review retained");
    assert_eq!(canon_status, "canon");
    assert_eq!(db.query_row(
        "SELECT COUNT(*) FROM pragma_foreign_key_check",
        [], |row| row.get::<_, i64>(0)
    ).expect("FK integrity"), 0);
    assert_eq!(db.query_row(
        "PRAGMA integrity_check", [], |row| row.get::<_, String>(0)
    ).expect("SQLite integrity"), "ok");
}

#[test]
fn precedence_evidence_must_refer_to_historical_revision_in_same_universe() {
    let mut db = v6();
    db.execute_batch(r#"
        INSERT INTO universes(id,name) VALUES ('u1','One'),('u2','Two');
        INSERT INTO novels(id,universe_id,title,sort_order)
            VALUES ('n1','u1','One',0),('n2','u2','Two',0);
        INSERT INTO chapters(id,novel_id,title,sort_order)
            VALUES ('c1','n1','C1',0),('c2','n2','C2',0);
        INSERT INTO scenes(id,chapter_id,title,sort_order)
            VALUES ('s1','c1','S1',0),('s2','c2','S2',0);
        INSERT INTO scene_text_revisions(id,scene_id,revision_number,content)
            VALUES ('r1','s1',1,'Earlier'),
                   ('r2','s2',1,'Elsewhere');
    "#).expect("two distinct source universes");
    stage_isolated(&mut db);
    anchor(&db,"a","u1");
    anchor(&db,"b","u1");

    let wrong = db.execute(
        "INSERT INTO world_time_precedences
         (id,universe_id,before_anchor_id,after_anchor_id,reason,source_revision_id)
         VALUES ('bad','u1','a','b','Cross-universe source','r2')", []
    );
    assert!(wrong.is_err(), "foreign-world historical evidence must be rejected");
    let after_failure: i64 = db.query_row(
        "SELECT COUNT(*) FROM world_time_precedences",
        [], |row| row.get(0)
    ).expect("no partial write");
    assert_eq!(after_failure, 0);

    db.execute(
        "INSERT INTO world_time_precedences
         (id,universe_id,before_anchor_id,after_anchor_id,reason,source_revision_id)
         VALUES ('good','u1','a','b','Cited assertion','r1')", []
    ).expect("in-universe immutable source accepted");
    assert_eq!(db.query_row(
        "SELECT COUNT(*) FROM world_time_precedences",
        [], |row| row.get::<_,i64>(0)
    ).expect("one valid assertion"), 1);
    assert_eq!(db.query_row(
        "SELECT COUNT(*) FROM pragma_foreign_key_check",
        [], |row| row.get::<_,i64>(0)
    ).expect("foreign keys"), 0);
}
