use super::*;
use crate::database;

fn seeded() -> Connection {
    let mut db = Connection::open_in_memory().expect("memory DB");
    database::configure_connection(&db).expect("configure FK");
    database::run_migrations(&mut db).expect("migrate v6");
    db.execute_batch(
        "INSERT INTO universes(id,name) VALUES('u1','Universe One'),('u2','Universe Two');
         INSERT INTO narrative_entities(id,universe_id,kind,name)
         VALUES ('e1','u1','character','Before'),
                ('e2','u2','character','Other');
         INSERT INTO narrative_facts(id,entity_id,universe_id,fact_key,fact_value,provenance_kind)
         VALUES('f1','e1','u1','trait','Careful','unsourced'),
               ('f2','e2','u2','trait','Bold','unsourced');"
    ).expect("fixtures");
    db
}
fn input(id: &str, fact: &str, rev: i64, status: &str) -> ReviewFactInput {
    ReviewFactInput {
        id:id.to_owned(), fact_id:fact.to_owned(),
        universe_id:"u1".to_owned(), expected_revision:rev,
        next_status:status.to_owned(), action_kind:"set_status".to_owned(),
        reviewer_label:"Operator-entered label".to_owned(),
        reason:"Operator review context".to_owned(),
        confirmation_phrase:None,
    }
}
fn approve(id:&str,rev:i64)->ReviewFactInput {
    let mut data=input(id,"f1",rev,"canon");
    data.action_kind="approve_canon".to_owned();
    data.confirmation_phrase=Some("APPROVE_CANON".to_owned());
    data
}
#[test]
fn facts_default_to_draft_with_zero_review_events() {
    let db=seeded();
    let current=state(&db,"f1","u1").unwrap();
    assert_eq!(current.status,"draft");
    assert_eq!(current.revision_number,0);
    let h=history(&db,"f1","u1").unwrap();
    assert!(h.events.is_empty());
    assert_eq!(snapshot(&db,"u1").unwrap().reviews.len(),1);
    assert_eq!(snapshot(&db,"u2").unwrap().reviews[0].status,"draft");
}
#[test]
fn suggestion_never_automatically_becomes_canon() {
    let mut db=seeded();
    let h=review(&mut db,input("event1","f1",0,"suggestion")).unwrap();
    assert_eq!(h.state.status,"suggestion");
    assert_eq!(h.events.len(),1);
    assert_eq!(h.events[0].previous_status,"draft");
    assert_eq!(h.events[0].revision_number,1);
    let denied=review(&mut db,input("event2","f1",1,"canon"));
    assert!(matches!(denied,Err(ReviewError::HumanConfirmationRequired)));
    let h=history(&db,"f1","u1").unwrap();
    assert_eq!(h.events.len(),1);
    assert_eq!(h.state.status,"suggestion");
    assert_eq!(snapshot(&db,"u2").unwrap().reviews[0].status,"draft");
}
#[test]
fn explicit_operator_approval_and_revocation_append_history() {
    let mut db=seeded();
    review(&mut db,input("suggest","f1",0,"suggestion")).unwrap();
    let h=review(&mut db,approve("approval",1)).unwrap();
    assert_eq!(h.state.status,"canon");
    assert_eq!(h.state.revision_number,2);
    let forbidden=review(&mut db,input("withdraw","f1",2,"draft"));
    assert!(matches!(forbidden,Err(ReviewError::HumanConfirmationRequired)));
    let mut revoke=input("withdraw","f1",2,"unknown");
    revoke.action_kind="revoke_canon".to_owned();
    revoke.confirmation_phrase=Some("REVOKE_CANON".to_owned());
    let h=review(&mut db,revoke).unwrap();
    assert_eq!(h.state.status,"unknown");
    assert_eq!(h.events.len(),3);
    assert_eq!(h.events[2].previous_status,"canon");
    assert_eq!(h.events[2].action_kind,"revoke_canon");
}
#[test]
fn different_uncertain_or_alternate_states_keep_separate_lineage() {
    let mut db=seeded();
    let statuses=["unknown","ambiguous","contradictory","variant","draft","suggestion"];
    for (i,status) in statuses.iter().enumerate() {
        let event=input(&format!("event{i}"),"f1",i as i64,status);
        review(&mut db,event).unwrap();
    }
    let record=history(&db,"f1","u1").unwrap();
    assert_eq!(record.events.len(),statuses.len());
    assert_eq!(record.state.status,"suggestion");
    for (idx,e) in record.events.iter().enumerate() {
        assert_eq!(&e.next_status,&statuses[idx]);
    }
}
#[test]
fn status_guards_reject_duplicate_stale_unknown_and_cross_universe() {
    let mut db=seeded();
    assert!(matches!(review(&mut db,input("a","f1",0,"wizard")),
        Err(ReviewError::InvalidStatus)));
    assert!(matches!(review(&mut db,input("a","f1",0,"draft")),
        Err(ReviewError::InvalidTransition)));
    let mut cross=input("a","f2",0,"variant");
    cross.universe_id="u1".to_owned();
    assert!(matches!(review(&mut db,cross),Err(ReviewError::CrossUniverse)));
    review(&mut db,input("a","f1",0,"unknown")).unwrap();
    assert!(matches!(review(&mut db,input("b","f1",0,"variant")),
        Err(ReviewError::StaleRevision)));
    assert!(review(&mut db,input("a","f1",1,"variant")).is_err());
    assert!(matches!(state(&db,"missing","u1"),Err(ReviewError::NotFound)));
    assert_eq!(history(&db,"f1","u1").unwrap().events.len(),1);
}
#[test]
fn cannot_forge_canon_with_sql_or_modify_audit() {
    let mut db=seeded();
    review(&mut db,input("draft2suggest","f1",0,"suggestion")).unwrap();
    for sql in [
        "INSERT INTO fact_review_events
         (id,fact_id,universe_id,revision_number,previous_status,next_status,
          action_kind,actor_kind,reviewer_label,human_confirmation,reason)
         VALUES('bad','f1','u1',2,'suggestion','canon','set_status','human','Me',0,'reason')",
        "INSERT INTO fact_review_events
         (id,fact_id,universe_id,revision_number,previous_status,next_status,
          action_kind,actor_kind,reviewer_label,human_confirmation,reason)
         VALUES('bad2','f1','u1',3,'suggestion','canon','approve_canon','human','Me',1,'reason')",
        "INSERT INTO fact_review_events
         (id,fact_id,universe_id,revision_number,previous_status,next_status,
          action_kind,actor_kind,reviewer_label,human_confirmation,reason)
         VALUES('bad3','f2','u1',1,'draft','variant','set_status','human','Me',0,'reason')",
        "UPDATE fact_review_events SET next_status='canon' WHERE id='draft2suggest'",
        "DELETE FROM fact_review_events WHERE id='draft2suggest'",
    ] {
        assert!(db.execute(sql,[]).is_err(),"{sql}");
    }
    let h=history(&db,"f1","u1").unwrap();
    assert_eq!(h.events.len(),1);
    assert_eq!(h.state.status,"suggestion");
    assert_eq!(db.query_row("PRAGMA integrity_check",[],|r|r.get::<_,String>(0)).unwrap(),"ok");
    let issue_count:i64=db.query_row(
        "SELECT COUNT(*) FROM pragma_foreign_key_check",[],|r|r.get(0)
    ).unwrap();
    assert_eq!(issue_count,0);
}
#[test]
fn unchanged_fact_source_and_review_survives_entity_rename() {
    let mut db=seeded();
    let original:String=db.query_row(
        "SELECT fact_value FROM narrative_facts WHERE id='f1'",[],|r|r.get(0)
    ).unwrap();
    review(&mut db,approve("approve",0)).unwrap();
    db.execute("UPDATE narrative_entities SET name='After' WHERE id='e1'",[]).unwrap();
    assert_eq!(history(&db,"f1","u1").unwrap().state.status,"canon");
    let value:String=db.query_row(
        "SELECT fact_value FROM narrative_facts WHERE id='f1'",[],|r|r.get(0)
    ).unwrap();
    assert_eq!(original,value);
    assert!(db.execute("DELETE FROM narrative_facts WHERE id='f1'",[]).is_err());
}
#[test]
fn operator_label_and_confirmation_are_required_not_assumed() {
    let mut db=seeded();
    let mut bad=approve("a",0);
    bad.reviewer_label="  ".to_owned();
    assert!(matches!(review(&mut db,bad),Err(ReviewError::Validation(_))));
    let mut bad=approve("b",0);
    bad.confirmation_phrase=Some("yes".to_owned());
    assert!(matches!(review(&mut db,bad),Err(ReviewError::HumanConfirmationRequired)));
    let mut bad=input("c","f1",0,"variant");
    bad.action_kind="approve_canon".to_owned();
    assert!(matches!(review(&mut db,bad),Err(ReviewError::InvalidTransition)));
    assert!(history(&db,"f1","u1").unwrap().events.is_empty());
    assert_eq!(serde_json::to_value(ReviewError::StaleRevision.payload()).unwrap()["code"],
        "stale_revision");
}
