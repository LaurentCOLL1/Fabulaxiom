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
    calendar(&db,"fiction1","u1");
    stage_isolated(&mut db);
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
    calendar(&db,"one","u1"); calendar(&db,"two","u2");
    stage_isolated(&mut db);
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
    db.execute(
        "INSERT INTO novels(id,universe_id,title,sort_order)
         VALUES ('n2','u2','Other novel',0);
         INSERT INTO chapters(id,novel_id,title,sort_order) VALUES ('c2','n2','C',0);
         INSERT INTO scenes(id,chapter_id,title,sort_order) VALUES ('s2','c2','Scene',0);
         INSERT INTO scene_text_revisions(id,scene_id,revision_number,content)
         VALUES ('r2','s2',1,'Original text')",[]
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
