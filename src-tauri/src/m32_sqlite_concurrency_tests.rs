//! M3.2 stage 9: real two-connection SQLite transaction and rollback proofs.
//! Test-only; NO Tauri IPC and NO existing operator database/backup is opened.
//! Uses a unique scratch SQLite file in the CI runner's temporary directory.
//! Independent PRIVATE caches + WAL test committed isolation and writer locks.
//! The RAII guard removes scratch DB and its sidecars after closing connections.

use crate::{database, m32_manual_chronology as chronology};
use rusqlite::{Connection, ErrorCode, TransactionBehavior};
use std::{
    fs::{self, OpenOptions},
    path::PathBuf,
    sync::atomic::{AtomicU64, Ordering},
    time::{Duration, SystemTime, UNIX_EPOCH},
};

const V7: &str = include_str!("../sql/m3_1_world_time_v7_candidate.sql");
const DECISIONS: &str = include_str!("../sql/m3_2_chronology_decisions_candidate.sql");
const RESTATEMENTS: &str = include_str!("../sql/m3_2_active_precedence_candidate.sql");
const RESTATEMENT_WITHDRAWALS: &str =
    include_str!("../sql/m3_2_restatement_revocations_candidate.sql");
const SUCCESSORS: &str = include_str!("../sql/m3_2_restatement_successors_candidate.sql");
const SUCCESSOR_WITHDRAWALS: &str =
    include_str!("../sql/m3_2_successor_revocations_candidate.sql");
const CHAINS: &str = include_str!("../sql/m3_2_recursive_chain_candidate.sql");

static TEST_SERIAL: AtomicU64 = AtomicU64::new(0);

struct ScratchDatabase(PathBuf);
impl Drop for ScratchDatabase {
    fn drop(&mut self) {
        // Scratch-only cleanup: NEVER an existing database or a qualification
        // artifact. Connections must have been dropped before the guard.
        for suffix in ["", "-wal", "-shm", "-journal"] {
            let candidate = format!("{}{}", self.0.display(), suffix);
            if std::path::Path::new(&candidate).exists() {
                fs::remove_file(&candidate).expect("scratch DB clean-up");
            }
        }
    }
}

fn scratch_pair() -> (ScratchDatabase, Connection, Connection) {
    // Exclusive file creation prevents accidentally opening an existing file.
    // No managed operator paths, UUID fixture folders, or production app root.
    let tick = SystemTime::now().duration_since(UNIX_EPOCH)
        .expect("positive epoch").as_nanos();
    let sequence = TEST_SERIAL.fetch_add(1, Ordering::Relaxed);
    let path = std::env::temp_dir().join(format!(
        "fabulaxiom-m32-stage9-{}-{tick}-{sequence}.sqlite3",
        std::process::id(),
    ));
    let handle = OpenOptions::new().write(true).create_new(true)
        .open(&path).expect("new unique scratch SQLite file");
    drop(handle);
    let scratch = ScratchDatabase(path.clone());

    let mut writer = Connection::open(&path).expect("scratch writer");
    database::configure_connection(&writer).expect("writer foreign keys");
    assert_eq!(database::run_migrations(&mut writer).unwrap(), 6);
    // Normal deployment does not set this. WAL is chosen exclusively to
    // demonstrate read visibility and writer isolation with two real handles.
    let wal: String = writer.pragma_query_value(
        None, "journal_mode", |row| row.get(0),
    ).unwrap();
    assert_ne!(wal, "memory");
    let wal: String = writer.pragma_update_and_check(
        None, "journal_mode", "WAL", |row| row.get(0),
    ).unwrap();
    assert_eq!(wal.to_lowercase(), "wal");
    {
        let tx = writer.transaction().unwrap();
        for sql in [V7, DECISIONS, RESTATEMENTS, RESTATEMENT_WITHDRAWALS,
                    SUCCESSORS, SUCCESSOR_WITHDRAWALS, CHAINS] {
            tx.execute_batch(sql).expect("candidate SQL only on scratch DB");
        }
        tx.execute(
            "INSERT INTO schema_migrations(version,name)
             VALUES (7,'007_create_world_time_foundation')", [],
        ).unwrap();
        tx.commit().unwrap();
    }
    assert_eq!(database::current_schema_version(&writer).unwrap(), 7);
    let reader = Connection::open(&path).expect("second independent handle");
    database::configure_connection(&reader).expect("reader foreign keys");
    assert_eq!(database::current_schema_version(&reader).unwrap(), 7);
    assert_eq!(database::MAX_AUTOMATIC_MIGRATION_VERSION, 6);
    (scratch, writer, reader)
}

fn anchor(db: &Connection, id: &str) {
    chronology::create_anchor(db, chronology::AnchorDraft {
        id, universe_id: "u1", time_kind: "unknown", calendar_id: None,
        event_entity_id: None, source_revision_id: None, exact_label: None,
        window_start_text: None, window_end_text: None, precision_text: None,
    }).unwrap();
}

fn setup_history(db: &Connection) {
    db.execute("INSERT INTO universes(id,name) VALUES ('u1','Fixture only')",[]).unwrap();
    for id in ["a","b","c","d","e","f"] { anchor(db,id); }
    chronology::create_precedence(db,"ab","u1","a","b","old",None).unwrap();
    chronology::decide_precedence(
        db,"d0","u1","ab","revoke",None,"corrected",None,
    ).unwrap();
    chronology::restate_revoked_precedence(
        db,"ba","u1","ab","b","a","first correction",None,
    ).unwrap();
    chronology::revoke_restatement(db,"d1","u1","ba","withdrawn",None).unwrap();
    chronology::succeed_withdrawn_restatement(
        db,"ac","u1","ba","a","c","second correction",None,
    ).unwrap();
    chronology::revoke_successor(db,"d2","u1","ac","withdrawn again",None).unwrap();
}

fn active_count(db: &Connection) -> usize {
    chronology::list_active_precedence_graph(db,"u1").unwrap().len()
}

fn count(db: &Connection, table: &str) -> i64 {
    // Explicit allowlist: never construct queries against an unknown table.
    let query = match table {
        "chain" => "SELECT COUNT(*) FROM world_time_chain_links",
        "withdrawal" => "SELECT COUNT(*) FROM world_time_chain_revocations",
        _ => panic!("unapproved table"),
    };
    db.query_row(query,[],|row|row.get(0)).unwrap()
}

fn assert_integrity(db: &Connection) {
    assert_eq!(
        db.query_row("PRAGMA integrity_check",[],|r|r.get::<_,String>(0)).unwrap(),
        "ok",
    );
    assert_eq!(db.query_row(
        "SELECT COUNT(*) FROM pragma_foreign_key_check",[],|r|r.get::<_,i64>(0),
    ).unwrap(),0);
    assert_eq!(database::MAX_AUTOMATIC_MIGRATION_VERSION, 6);
}

#[test]
fn two_connections_hide_uncommitted_chain_and_serialize_writers() {
    let (scratch, mut writer, reader) = scratch_pair();
    setup_history(&writer);
    assert_eq!(active_count(&reader),0);

    let tx = writer.transaction_with_behavior(TransactionBehavior::Immediate).unwrap();
    chronology::append_chain_correction(
        &tx,"cd","u1",Some("ac"),None,"c","d","tentative",None,
    ).unwrap();
    assert_eq!(active_count(&tx),1);
    // WAL snapshot reader cannot observe a dirty inserted correction.
    assert_eq!(active_count(&reader),0);

    reader.busy_timeout(Duration::ZERO).unwrap();
    let blocked = chronology::append_chain_correction(
        &reader,"alternate","u1",Some("ac"),None,"c","e","contending writer",None,
    ).expect_err("second writer must not succeed before first transaction ends");
    assert!(matches!(blocked, rusqlite::Error::SqliteFailure(ref e, _)
        if e.code == ErrorCode::DatabaseBusy || e.code == ErrorCode::DatabaseLocked));
    tx.rollback().unwrap();
    assert_eq!(count(&reader,"chain"),0);
    // Successful retry proves rollback released parent-uniqueness and lock.
    chronology::append_chain_correction(
        &reader,"alternate","u1",Some("ac"),None,"c","e","committed",None,
    ).unwrap();
    assert_eq!(active_count(&writer),1);
    assert!(chronology::append_chain_correction(
        &writer,"fork","u1",Some("ac"),None,"d","f","raced fork",None,
    ).is_err());
    assert_eq!(count(&writer,"chain"),1);
    assert_integrity(&writer);
    drop(reader);
    drop(writer);
    drop(scratch);
}

#[test]
fn rollback_of_withdrawal_and_replacement_is_atomic_across_connections() {
    let (scratch, mut writer, reader) = scratch_pair();
    setup_history(&writer);
    chronology::append_chain_correction(
        &writer,"cd","u1",Some("ac"),None,"c","d","committed parent",None,
    ).unwrap();
    assert_eq!(active_count(&reader),1);

    let tx = writer.transaction_with_behavior(TransactionBehavior::Immediate).unwrap();
    chronology::revoke_chain_correction(
        &tx,"withdraw-cd","u1","cd","tentative withdrawal",None,
    ).unwrap();
    chronology::append_chain_correction(
        &tx,"de","u1",None,Some("cd"),"d","e","tentative replacement",None,
    ).unwrap();
    assert_eq!(active_count(&tx),1);
    // Reader sees old complete committed assertion, not half a correction.
    let view = chronology::list_active_precedence_graph(&reader,"u1").unwrap();
    assert_eq!(view.len(),1);
    assert_eq!(view[0].id,"cd");
    assert_eq!(count(&reader,"withdrawal"),0);
    tx.rollback().unwrap();

    assert_eq!(count(&reader,"withdrawal"),0);
    assert_eq!(count(&reader,"chain"),1);
    assert_eq!(chronology::list_active_precedence_graph(&reader,"u1").unwrap()[0].id,"cd");
    // Same operations are then safely committed as a single transaction.
    let tx = writer.transaction_with_behavior(TransactionBehavior::Immediate).unwrap();
    chronology::revoke_chain_correction(
        &tx,"withdraw-cd","u1","cd","approved withdrawal",None,
    ).unwrap();
    chronology::append_chain_correction(
        &tx,"de","u1",None,Some("cd"),"d","e","approved replacement",None,
    ).unwrap();
    tx.commit().unwrap();
    assert_eq!(count(&reader,"withdrawal"),1);
    assert_eq!(count(&reader,"chain"),2);
    let committed = chronology::list_active_precedence_graph(&reader,"u1").unwrap();
    assert_eq!(committed.len(),1);
    assert_eq!(committed[0].id,"de");
    assert_integrity(&reader);
    drop(reader);
    drop(writer);
    drop(scratch);
}

#[test]
fn two_connection_readonly_and_cycle_guards_reject_cross_handle_bypass() {
    let (scratch, writer, reader) = scratch_pair();
    setup_history(&writer);
    chronology::append_chain_correction(
        &writer,"cd","u1",Some("ac"),None,"c","d","final",None,
    ).unwrap();
    assert_eq!(active_count(&reader),1);
    // Cross-connection raw insert that would close a cycle must fail.
    assert!(chronology::create_precedence(
        &reader,"raw-dc","u1","d","c","active only cycle",None,
    ).is_err());
    assert_eq!(active_count(&writer),1);
    reader.pragma_update(None,"query_only",true).unwrap();
    assert!(chronology::append_chain_correction(
        &reader,"forbidden","u1",None,Some("cd"),"d","f","read-only refused",None,
    ).is_err());
    assert_eq!(count(&writer,"chain"),1);
    assert_eq!(count(&writer,"withdrawal"),0);
    assert_integrity(&writer);
    drop(reader);
    drop(writer);
    drop(scratch);
}
