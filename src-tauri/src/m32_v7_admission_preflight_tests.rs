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
use std::os::windows::fs::MetadataExt;

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
enum AdmissionMode { NewOnly, ExistingProfile }

// S1 is a *decision model*, not a runtime admission state machine.  A clean
// shutdown can justify rechecking a disposable file, never mint a writer token.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
enum LifecycleObservation { Absent, CleanlyClosed, UncertainAfterCrash, Active, Foreign }

fn lifecycle_preflight_mode(observed: LifecycleObservation) -> Result<AdmissionMode, Refusal> {
    match observed {
        LifecycleObservation::Absent => Ok(AdmissionMode::NewOnly),
        LifecycleObservation::CleanlyClosed => Ok(AdmissionMode::ExistingProfile),
        LifecycleObservation::UncertainAfterCrash | LifecycleObservation::Active |
        LifecycleObservation::Foreign => Err(Refusal::LifecycleUnproven),
    }
}

// Only a successful explicit close of a disposable, already-open test
// connection can create this *in-process observation*. It is NOT persisted,
// transferable to a new process, or bound to a later delegated SQLite xOpen.
fn observe_disposable_explicit_close(connection: Connection) -> Result<LifecycleObservation, Refusal> {
    connection.close().map_err(|_| Refusal::LifecycleUnproven)?;
    Ok(LifecycleObservation::CleanlyClosed)
}

#[derive(Debug, Eq, PartialEq)]
enum Refusal {
    Missing, AlreadyExists, SidecarPresent, ForeignSchema,
    ForeignKeyViolation, HandoffNotAtomic,
    OutsideOwnedRoot, UnsafeOwnedAncestor,
    LifecycleUnproven,
}

const PROFILE: &str = "com.fabulaxiom.greenfield.v1";
const SIDECARS: [&str; 3] = ["-wal", "-shm", "-journal"];
const FILE_ATTRIBUTE_REPARSE_POINT: u32 = 0x400;

fn has_reparse_attribute(attributes: u32) -> bool {
    attributes & FILE_ATTRIBUTE_REPARSE_POINT != 0
}

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

// Route A is a TEST-ONLY, bounded threat model: the fresh fixture root is
// controlled by its creator, not an arbitrary path supplied by a caller.
// Checking reparse attributes does NOT pin ancestors, defeat privileged
// namespace replacement, or authorize a SQLite xOpen/actor token.
fn owned_namespace_preflight(root: &Disposable, candidate: &Path, mode: AdmissionMode)
    -> Result<(), Refusal>
{
    if candidate != root.db() { return Err(Refusal::OutsideOwnedRoot); }
    let profile = root.0.join(PROFILE);
    let database = profile.join("database");
    for ancestor in [&root.0, &profile, &database] {
        let metadata = ancestor.symlink_metadata().map_err(|_| Refusal::UnsafeOwnedAncestor)?;
        if !metadata.is_dir() || has_reparse_attribute(metadata.file_attributes()) {
            return Err(Refusal::UnsafeOwnedAncestor);
        }
    }
    match candidate.symlink_metadata() {
        Ok(metadata) if has_reparse_attribute(metadata.file_attributes()) =>
            return Err(Refusal::UnsafeOwnedAncestor),
        Err(error) if error.kind() != io::ErrorKind::NotFound =>
            return Err(Refusal::UnsafeOwnedAncestor),
        _ => {}
    }
    preflight(candidate, mode)
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

#[test]
fn m32_s2_route_a_owned_namespace_exact_path_and_reparse_refusal() {
    let owned = Disposable::new(); owned.prepare();
    let foreign = Disposable::new(); foreign.prepare();
    assert_eq!(owned_namespace_preflight(&owned, &owned.db(), AdmissionMode::NewOnly), Ok(()));
    assert_eq!(owned_namespace_preflight(&owned, &foreign.db(), AdmissionMode::NewOnly),
        Err(Refusal::OutsideOwnedRoot));
    let escape = owned.0.join("..").join("arbitrary.sqlite3");
    assert_eq!(owned_namespace_preflight(&owned, &escape, AdmissionMode::NewOnly),
        Err(Refusal::OutsideOwnedRoot));
    assert!(!has_reparse_attribute(0));
    assert!(has_reparse_attribute(FILE_ATTRIBUTE_REPARSE_POINT));
    assert!(has_reparse_attribute(FILE_ATTRIBUTE_REPARSE_POINT | 0x10));
    assert_eq!(deny_unbound_handoff(), Err(Refusal::HandoffNotAtomic));
}

#[test]
fn m32_s2_route_a_parent_missing_or_replaced_remains_unbound() {
    let owned = Disposable::new(); owned.prepare(); let db = owned.db();
    fs::write(&db, b"controlled placeholder").unwrap();
    assert_eq!(owned_namespace_preflight(&owned, &db, AdmissionMode::ExistingProfile), Ok(()));
    let parent = db.parent().unwrap();
    let moved = owned.0.join("owned-database-moved");
    fs::rename(parent, &moved).unwrap();
    assert_eq!(owned_namespace_preflight(&owned, &db, AdmissionMode::ExistingProfile),
        Err(Refusal::UnsafeOwnedAncestor));
    fs::create_dir(parent).unwrap();
    fs::write(&db, b"replacement placeholder").unwrap();
    assert_eq!(owned_namespace_preflight(&owned, &db, AdmissionMode::ExistingProfile), Ok(()));
    assert_ne!(fs::read(moved.join("fabulaxiom.sqlite3")).unwrap(), fs::read(&db).unwrap());
    assert_eq!(deny_unbound_handoff(), Err(Refusal::HandoffNotAtomic));
}

#[test]
fn m32_s1_route_a_clean_close_is_only_a_reopen_candidate() {
    let owned = Disposable::new(); owned.prepare(); let db = owned.db();
    assert_eq!(lifecycle_preflight_mode(LifecycleObservation::Absent), Ok(AdmissionMode::NewOnly));
    assert_eq!(owned_namespace_preflight(&owned, &db, AdmissionMode::NewOnly), Ok(()));
    {
        let connection = Connection::open(&db).unwrap();
        connection.execute_batch("CREATE TABLE disposable_revision(id INTEGER PRIMARY KEY);").unwrap();
    }
    assert_eq!(lifecycle_preflight_mode(LifecycleObservation::CleanlyClosed),
        Ok(AdmissionMode::ExistingProfile));
    assert_eq!(owned_namespace_preflight(&owned, &db, AdmissionMode::ExistingProfile), Ok(()));
    assert_eq!(owned_namespace_preflight(&owned, &db, AdmissionMode::NewOnly), Err(Refusal::AlreadyExists));
    assert_eq!(deny_unbound_handoff(), Err(Refusal::HandoffNotAtomic));
}

#[test]
fn m32_s1_route_a_uncertain_or_foreign_lifecycle_never_grants_a_mode() {
    for observed in [LifecycleObservation::UncertainAfterCrash, LifecycleObservation::Active,
                     LifecycleObservation::Foreign] {
        assert_eq!(lifecycle_preflight_mode(observed), Err(Refusal::LifecycleUnproven));
        assert_eq!(deny_unbound_handoff(), Err(Refusal::HandoffNotAtomic));
    }
    // A path can still pass a lexical/filesystem check while its provenance
    // or clean shutdown evidence is unknown: it MUST NOT become admission.
    let owned = Disposable::new(); owned.prepare(); let db = owned.db();
    fs::write(&db, b"unknown lifecycle").unwrap();
    assert_eq!(owned_namespace_preflight(&owned, &db, AdmissionMode::ExistingProfile), Ok(()));
    assert_eq!(lifecycle_preflight_mode(LifecycleObservation::UncertainAfterCrash),
        Err(Refusal::LifecycleUnproven));
}

#[test]
fn m32_s1_route_a_explicit_close_witness_is_inprocess_only() {
    let owned = Disposable::new(); owned.prepare(); let db = owned.db();
    let connection = Connection::open(&db).unwrap();
    connection.execute_batch("CREATE TABLE one_session(id INTEGER PRIMARY KEY);").unwrap();
    assert_eq!(lifecycle_preflight_mode(LifecycleObservation::Active),
        Err(Refusal::LifecycleUnproven));
    let within_process = observe_disposable_explicit_close(connection).unwrap();
    assert_eq!(within_process, LifecycleObservation::CleanlyClosed);
    assert_eq!(lifecycle_preflight_mode(within_process), Ok(AdmissionMode::ExistingProfile));
    assert_eq!(owned_namespace_preflight(&owned, &db, AdmissionMode::ExistingProfile), Ok(()));
    assert_eq!(deny_unbound_handoff(), Err(Refusal::HandoffNotAtomic));
}

#[test]
fn m32_s1_route_a_implicit_drop_cannot_mint_reopen_evidence() {
    let owned = Disposable::new(); owned.prepare(); let db = owned.db();
    {
        let connection = Connection::open(&db).unwrap();
        connection.execute_batch("CREATE TABLE implicit_close(id INTEGER PRIMARY KEY);").unwrap();
        // Drop cannot be observed as a successful explicit close by the
        // decision gate. This test does not simulate a process crash.
    }
    assert_eq!(owned_namespace_preflight(&owned, &db, AdmissionMode::ExistingProfile), Ok(()));
    assert_eq!(lifecycle_preflight_mode(LifecycleObservation::UncertainAfterCrash),
        Err(Refusal::LifecycleUnproven));
    assert_eq!(deny_unbound_handoff(), Err(Refusal::HandoffNotAtomic));
}
