//! M3.1 controlled-copy migration rehearsal, exclusively disposable test files.
//! We copy ONLY a closed fixture DB, never a live active operator database.
//! No production runtime entry point or v7 registry change is exposed here.
use crate::database;
use crate::world_time_preflight::{inspect_v6, PreflightFailure};
use rusqlite::{Connection, OpenFlags};
use std::{
    fs,
    path::{Path, PathBuf},
    process,
    time::{SystemTime, UNIX_EPOCH},
};

const CANDIDATE_SQL: &str = include_str!("../sql/m3_1_world_time_v7_candidate.sql");

struct DisposableRoot(PathBuf);
impl DisposableRoot {
    fn new(name: &str) -> Self {
        let unique = SystemTime::now().duration_since(UNIX_EPOCH)
            .expect("time").as_nanos();
        let root = std::env::temp_dir().join(format!(
            "fabulaxiom-m31-{name}-{}-{unique}", process::id()
        ));
        fs::create_dir(&root).expect("new owned disposable test directory");
        Self(root)
    }
    fn file(&self, name: &str) -> PathBuf { self.0.join(name) }
}
impl Drop for DisposableRoot {
    fn drop(&mut self) {
        // Only the disposable directory created by this test is removed.
        fs::remove_dir_all(&self.0).expect("cleanup test fixture");
    }
}

fn create_closed_populated_v6(path: &Path) {
    let db = database::open_database(path).expect("create isolated v6 test fixture");
    db.execute_batch(r#"
        INSERT INTO universes(id,name) VALUES ('u1','Aurora');
        INSERT INTO novels(id,universe_id,title,sort_order)
            VALUES ('n1','u1','Ancient Tales',0);
        INSERT INTO chapters(id,novel_id,title,sort_order)
            VALUES ('c1','n1','Dawn',0);
        INSERT INTO scenes(id,chapter_id,title,sort_order)
            VALUES ('s1','c1','Old scene',0);
        INSERT INTO scene_text_revisions(id,scene_id,revision_number,content)
            VALUES ('r1','s1',1,'Éclipse 🌕 dans la forêt');
        INSERT INTO scene_revision_heads(scene_id,revision_id)
            VALUES ('s1','r1');
        INSERT INTO narrative_entities(id,universe_id,kind,name)
            VALUES ('e1','u1','event','Éclipse');
        INSERT INTO narrative_facts(id,entity_id,universe_id,fact_key,fact_value,provenance_kind)
            VALUES ('f1','e1','u1','state','confirmed','unsourced');
        INSERT INTO fact_review_events
            (id,fact_id,universe_id,revision_number,previous_status,next_status,
             action_kind,actor_kind,reviewer_label,human_confirmation,reason)
            VALUES
            ('rev1','f1','u1',1,'draft','suggestion','set_status','human','writer',0,'First review'),
            ('rev2','f1','u1',2,'suggestion','canon','approve_canon','human','writer',1,'Approved');
    "#).expect("legacy hierarchy, revisions, human review");
    assert_eq!(database::current_schema_version(&db).unwrap(), 6);
    drop(db); // Deliberately close before file copy: NEVER copy a live SQLite file.
}

fn opened_read_only_v6(path: &Path) -> Connection {
    let db = Connection::open_with_flags(path, OpenFlags::SQLITE_OPEN_READ_ONLY)
        .expect("read-only closed fixture");
    database::configure_connection(&db).expect("foreign keys on the connection");
    inspect_v6(&db).expect("six accepted migrations, integrity and table counts");
    db
}

fn checked_m2_snapshot(db: &Connection) -> (String, String, String, i64) {
    db.query_row(
        "SELECT r.content, h.revision_id,
                (SELECT next_status FROM fact_review_events
                 WHERE fact_id='f1' ORDER BY revision_number DESC LIMIT 1),
                (SELECT COUNT(*) FROM fact_review_events)
         FROM scene_text_revisions r
         JOIN scene_revision_heads h ON h.revision_id=r.id
         WHERE r.id='r1'",
        [], |row| Ok((row.get(0)?, row.get(1)?, row.get(2)?, row.get(3)?)),
    ).expect("M2 source, current revision and human canon history")
}

fn integrity(db: &Connection) {
    let result: String = db.query_row(
        "PRAGMA integrity_check", [], |row| row.get(0)
    ).expect("integrity");
    assert_eq!(result, "ok");
    let failed: i64 = db.query_row(
        "SELECT COUNT(*) FROM pragma_foreign_key_check",
        [], |row| row.get(0),
    ).expect("foreign key issues");
    assert_eq!(failed, 0);
}

#[test]
fn offline_copy_rehearsal_retains_original_v6_and_human_review() {
    let root = DisposableRoot::new("populated");
    let active_simulation = root.file("closed-source-v6.sqlite3");
    let sealed_simulation = root.file("sealed-before-v7.sqlite3");
    let copy = root.file("migration-candidate-v7.sqlite3");

    create_closed_populated_v6(&active_simulation);
    let before_bytes = fs::read(&active_simulation).expect("source bytes");
    fs::copy(&active_simulation, &sealed_simulation).expect("closed fixture sealed");
    fs::copy(&active_simulation, &copy).expect("disposable migration copy");

    let original_db = opened_read_only_v6(&active_simulation);
    let original_snapshot = checked_m2_snapshot(&original_db);
    drop(original_db);

    let mut candidate = Connection::open(&copy).expect("new copy only");
    database::configure_connection(&candidate).expect("FKs");
    {
        let tx = candidate.transaction().expect("migration atomic transaction");
        tx.execute_batch(CANDIDATE_SQL).expect("candidate schema in COPY ONLY");
        tx.execute(
            "INSERT INTO schema_migrations(version,name)
             VALUES (7,'007_create_world_time_foundation')", [],
        ).expect("simulated v7 row in COPY ONLY");
        tx.commit().expect("commit new copy");
    }
    assert_eq!(database::current_schema_version(&candidate).unwrap(), 7);
    assert_eq!(checked_m2_snapshot(&candidate), original_snapshot);
    integrity(&candidate);
    let strict_count: i64 = candidate.query_row(
        "SELECT COUNT(*) FROM pragma_table_list
         WHERE name IN ('fictional_calendars','world_time_anchors','world_time_precedences')
           AND strict=1",
        [], |row| row.get(0),
    ).expect("three strict tables");
    assert_eq!(strict_count, 3);
    // An active v6 preflight must REFUSE a candidate schema/v7 database.
    assert_eq!(inspect_v6(&candidate), Err(PreflightFailure::UnexpectedVersion(7)));
    drop(candidate);

    let untouched = opened_read_only_v6(&active_simulation);
    assert_eq!(checked_m2_snapshot(&untouched), original_snapshot);
    drop(untouched);
    assert_eq!(fs::read(&active_simulation).unwrap(), before_bytes);
    assert_eq!(fs::read(&sealed_simulation).unwrap(), before_bytes);
}

#[test]
fn failed_copy_migration_rollback_keeps_v6_and_original_unchanged() {
    let root = DisposableRoot::new("rollback");
    let source = root.file("source-v6.sqlite3");
    let candidate_path = root.file("candidate.sqlite3");
    create_closed_populated_v6(&source);
    let original_bytes = fs::read(&source).expect("source before");
    fs::copy(&source, &candidate_path).expect("closed v6 disposable copy");

    let mut candidate = Connection::open(&candidate_path).expect("copy");
    database::configure_connection(&candidate).expect("FKs");
    let old = checked_m2_snapshot(&candidate);
    {
        let tx = candidate.transaction().expect("atomic migration");
        tx.execute_batch(CANDIDATE_SQL).expect("create new tables transactionally");
        // Intentional FK violation simulates an unacceptable migration step;
        // dropping tx must rollback all schema changes and the v7 marker.
        assert!(tx.execute(
            "INSERT INTO world_time_precedences
             (id,universe_id,before_anchor_id,after_anchor_id,reason)
             VALUES ('invalid','u1','missing-before','missing-after','fixture')",
            [],
        ).is_err());
    }
    assert_eq!(database::current_schema_version(&candidate).unwrap(), 6);
    inspect_v6(&candidate).expect("failed migration left v6 untouched");
    assert_eq!(checked_m2_snapshot(&candidate), old);
    integrity(&candidate);
    drop(candidate);

    assert_eq!(fs::read(&source).unwrap(), original_bytes);
    let untouched = opened_read_only_v6(&source);
    assert_eq!(checked_m2_snapshot(&untouched), old);
}

#[test]
fn empty_v6_copy_upgrades_to_three_strict_candidate_tables() {
    let root = DisposableRoot::new("empty");
    let source = root.file("empty-v6.sqlite3");
    let copy = root.file("empty-copy.sqlite3");
    let db = database::open_database(&source).expect("new v6 disposable database");
    assert_eq!(database::current_schema_version(&db).unwrap(), 6);
    drop(db);
    fs::copy(&source, &copy).expect("closed empty fixture copy");

    let mut db = Connection::open(&copy).expect("independent new copy");
    database::configure_connection(&db).expect("FKs");
    let tx = db.transaction().expect("atomic transaction");
    tx.execute_batch(CANDIDATE_SQL).expect("create schema");
    tx.execute(
        "INSERT INTO schema_migrations(version,name)
         VALUES (7,'007_create_world_time_foundation')", [],
    ).expect("simulated copy-only registry");
    tx.commit().expect("commit");
    assert_eq!(database::current_schema_version(&db).unwrap(), 7);
    integrity(&db);
    drop(db);
    let original = opened_read_only_v6(&source);
    assert_eq!(database::current_schema_version(&original).unwrap(), 6);
}
