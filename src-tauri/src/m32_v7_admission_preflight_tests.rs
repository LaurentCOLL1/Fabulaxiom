//! S1/S2 Windows-only disposable admission *preflight* witnesses.
//! Preflight is not admission: no V7WriterAdmission constructor is reachable,
//! no runtime opener/IPC, and no claim of atomic SQLite xOpen identity.

use std::{
    fs::{self, OpenOptions},
    io,
    path::{Path, PathBuf},
    process,
    sync::{atomic::{AtomicU64, Ordering}, Arc, Barrier},
    thread,
    time::{SystemTime, UNIX_EPOCH},
};

use rusqlite::{Connection, OpenFlags};

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
enum AdmissionMode { NewOnly, ExistingProfile }

#[derive(Debug, Eq, PartialEq)]
enum Refusal {
    Missing, AlreadyExists, SidecarPresent, ForeignSchema,
    ForeignKeyViolation, HandoffNotAtomic,
}

const PROFILE: &str = "com.fabulaxiom.greenfield.v1";
const SIDECARS: [&str; 3] = ["-wal", "-shm", "-journal"];

fn sidecars_absent(path: &Path) -> Result<(), Refusal> {
    let name = path.file_name().unwrap().to_string_lossy();
    for suffix in SIDECARS {
        match path.with_file_name(format!("{name}{suffix}")).symlink_metadata() {
            Err(e) if e.kind() == io::ErrorKind::NotFound => {},
            _ => return Err(Refusal::SidecarPresent),
        }
    }
    Ok(())
}

// No profile auto-discovery, no migration, and no actual connection opening.
// symlink_metadata detects dangling links too. Unknown errors fail closed.
fn preflight(path: &Path, mode: AdmissionMode) -> Result<(), Refusal> {
    sidecars_absent(path)?;
    match (mode, path.symlink_metadata()) {
        (AdmissionMode::NewOnly, Err(e)) if e.kind() == io::ErrorKind::NotFound => Ok(()),
        (AdmissionMode::NewOnly, _) => Err(Refusal::AlreadyExists),
        (AdmissionMode::ExistingProfile, Ok(m)) if m.file_type().is_file() => Ok(()),
        (AdmissionMode::ExistingProfile, _) => Err(Refusal::Missing),
    }
}

// A staged path check remains susceptible to substitution before SQLite xOpen.
// Even equal FileIds at two instants do not seal this handoff.
fn deny_unbound_handoff() -> Result<(), Refusal> { Err(Refusal::HandoffNotAtomic) }

// Evidence of a *negative* only: neither this check nor a clean FK result
// authenticates an expected Fabulaxiom migration lineage or the opened handle.
fn reject_foreign_fixture(connection: &Connection) -> Result<(), Refusal> {
    let foreign: i64 = connection
        .query_row("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='foreign_owner'", [], |r| r.get(0))
        .map_err(|_| Refusal::ForeignSchema)?;
    if foreign != 0 { return Err(Refusal::ForeignSchema); }
    let violations: i64 = connection
        .query_row("SELECT COUNT(*) FROM pragma_foreign_key_check", [], |r| r.get(0))
        .map_err(|_| Refusal::ForeignKeyViolation)?;
    if violations != 0 { return Err(Refusal::ForeignKeyViolation); }
    Ok(())
}

static NEXT_ROOT: AtomicU64 = AtomicU64::new(0);
struct Disposable(PathBuf);
impl Disposable {
    fn new() -> Self {
        let tick = SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_nanos();
        let n = NEXT_ROOT.fetch_add(1, Ordering::Relaxed);
        let root = std::env::temp_dir().join(format!("fabulaxiom-s1s2-{}-{tick}-{n}", process::id()));
        fs::create_dir(&root).expect("private fresh fixture root");
        Self(root)
    }
    fn db(&self) -> PathBuf { self.0.join(PROFILE).join("database").join("fabulaxiom.sqlite3") }
    fn prepare(&self) {
        fs::create_dir_all(self.db().parent().unwrap()).unwrap();
    }
}
impl Drop for Disposable {
    fn drop(&mut self) { fs::remove_dir_all(&self.0).expect("remove only fixture-owned root"); }
}

#[test]
fn m32_s1_new_only_and_existing_profile_are_mutually_exclusive() {
    let root = Disposable::new(); root.prepare(); let db = root.db();
    assert_eq!(preflight(&db, AdmissionMode::NewOnly), Ok(()));
    assert_eq!(preflight(&db, AdmissionMode::ExistingProfile), Err(Refusal::Missing));
    let claim = OpenOptions::new().write(true).create_new(true).open(&db).unwrap();
    assert_eq!(preflight(&db, AdmissionMode::NewOnly), Err(Refusal::AlreadyExists));
    assert_eq!(preflight(&db, AdmissionMode::ExistingProfile), Ok(()));
    assert!(OpenOptions::new().write(true).create_new(true).open(&db).is_err());
    drop(claim);
    assert_eq!(deny_unbound_handoff(), Err(Refusal::HandoffNotAtomic));
}

#[test]
fn m32_s2_all_sidecars_veto_both_modes_without_mutation() {
    for suffix in SIDECARS {
        let root = Disposable::new(); root.prepare(); let db = root.db();
        let sidecar = db.with_file_name(format!("{}{}", db.file_name().unwrap().to_string_lossy(), suffix));
        fs::write(&sidecar, b"invented sentinel").unwrap();
        assert_eq!(preflight(&db, AdmissionMode::NewOnly), Err(Refusal::SidecarPresent));
        fs::write(&db, b"invented main").unwrap();
        assert_eq!(preflight(&db, AdmissionMode::ExistingProfile), Err(Refusal::SidecarPresent));
        assert_eq!(fs::read(&sidecar).unwrap(), b"invented sentinel");
    }
}

#[test]
fn m32_s2_rename_between_preflight_and_open_is_not_an_admission() {
    let root = Disposable::new(); root.prepare(); let db = root.db();
    fs::write(&db, b"original").unwrap();
    assert_eq!(preflight(&db, AdmissionMode::ExistingProfile), Ok(()));
    let moved = db.with_extension("moved");
    fs::rename(&db, &moved).unwrap();
    fs::write(&db, b"substituted").unwrap();
    assert_eq!(deny_unbound_handoff(), Err(Refusal::HandoffNotAtomic));
    assert_eq!(fs::read(&moved).unwrap(), b"original");
    assert_eq!(fs::read(&db).unwrap(), b"substituted");
}

#[test]
fn m32_s2_foreign_schema_and_broken_fk_are_not_reopenable() {
    let root = Disposable::new(); root.prepare(); let db = root.db();
    let foreign = Connection::open_with_flags(&db, OpenFlags::SQLITE_OPEN_READ_WRITE | OpenFlags::SQLITE_OPEN_CREATE).unwrap();
    foreign.execute_batch("CREATE TABLE foreign_owner(x INTEGER); PRAGMA user_version=7;").unwrap();
    drop(foreign);
    assert_eq!(preflight(&db, AdmissionMode::ExistingProfile), Ok(()));
    // A filesystem preflight alone must never claim schema/lineage provenance.
    let read = Connection::open_with_flags(&db, OpenFlags::SQLITE_OPEN_READ_ONLY).unwrap();
    assert_eq!(reject_foreign_fixture(&read), Err(Refusal::ForeignSchema));
    assert_eq!(deny_unbound_handoff(), Err(Refusal::HandoffNotAtomic));
}

#[test]
fn m32_s2_broken_foreign_key_refused_on_disposable_sqlite() {
    let root = Disposable::new(); root.prepare(); let db = root.db();
    let connection = Connection::open(&db).unwrap();
    connection.execute_batch("PRAGMA foreign_keys=OFF;
        CREATE TABLE parent(id INTEGER PRIMARY KEY);
        CREATE TABLE child(parent_id INTEGER REFERENCES parent(id));
        INSERT INTO child(parent_id) VALUES(99);").unwrap();
    assert_eq!(reject_foreign_fixture(&connection), Err(Refusal::ForeignKeyViolation));
    assert_eq!(deny_unbound_handoff(), Err(Refusal::HandoffNotAtomic));
}

#[test]
fn m32_s2_two_simultaneous_new_only_claims_admit_only_one_name_reservation() {
    let root = Disposable::new(); root.prepare(); let db = root.db();
    let barrier = Arc::new(Barrier::new(3));
    let mut workers = Vec::new();
    for _ in 0..2 {
        let path = db.clone(); let start = barrier.clone();
        workers.push(thread::spawn(move || {
            start.wait();
            OpenOptions::new().write(true).create_new(true).open(&path).is_ok()
        }));
    }
    barrier.wait();
    let wins = workers.into_iter().map(|worker| worker.join().unwrap()).filter(|won| *won).count();
    assert_eq!(wins, 1);
    assert_eq!(preflight(&db, AdmissionMode::NewOnly), Err(Refusal::AlreadyExists));
    assert_eq!(deny_unbound_handoff(), Err(Refusal::HandoffNotAtomic));
}

#[test]
fn m32_s2_parent_namespace_replacement_after_preflight_is_a_stop() {
    let root = Disposable::new(); root.prepare(); let db = root.db();
    fs::write(&db, b"first namespace").unwrap();
    assert_eq!(preflight(&db, AdmissionMode::ExistingProfile), Ok(()));
    let parent = db.parent().unwrap();
    let renamed = root.0.join("database-moved");
    fs::rename(parent, &renamed).unwrap();
    fs::create_dir(parent).unwrap();
    fs::write(&db, b"replacement namespace").unwrap();
    assert_eq!(fs::read(renamed.join("fabulaxiom.sqlite3")).unwrap(), b"first namespace");
    assert_eq!(fs::read(&db).unwrap(), b"replacement namespace");
    // Two path checks can both pass; neither binds a subsequent SQLite xOpen.
    assert_eq!(preflight(&db, AdmissionMode::ExistingProfile), Ok(()));
    assert_eq!(deny_unbound_handoff(), Err(Refusal::HandoffNotAtomic));
}

#[test]
fn m32_s2_live_wal_and_external_connection_lock_are_not_writer_proof() {
    let root = Disposable::new(); root.prepare(); let db = root.db();
    let first = Connection::open(&db).unwrap();
    let journal: String = first.query_row("PRAGMA journal_mode=WAL", [], |r| r.get(0)).unwrap();
    assert_eq!(journal.to_lowercase(), "wal");
    first.execute_batch("CREATE TABLE invented(id INTEGER PRIMARY KEY); BEGIN IMMEDIATE;
        INSERT INTO invented(id) VALUES(1);").unwrap();
    assert_eq!(preflight(&db, AdmissionMode::ExistingProfile), Err(Refusal::SidecarPresent));
    let second = Connection::open(&db).unwrap();
    second.busy_timeout(std::time::Duration::ZERO).unwrap();
    assert!(second.execute_batch("BEGIN IMMEDIATE; INSERT INTO invented(id) VALUES(2); COMMIT;").is_err());
    first.execute_batch("ROLLBACK").unwrap();
    second.execute_batch("BEGIN IMMEDIATE; INSERT INTO invented(id) VALUES(2); COMMIT;").unwrap();
    // A prior BUSY does not establish absence of a writer later.
    assert_eq!(deny_unbound_handoff(), Err(Refusal::HandoffNotAtomic));
    drop(second); drop(first);
}
