//! Disposable Windows SQLite VFS boundary experiment, compiled only as tests.
//! A refusal at xOpen precedes default-VFS delegation; a post-xOpen FileId
//! check does not. This does NOT authenticate any Windows operator profile.

use rusqlite::{ffi, Connection, OpenFlags};
use std::{
    ffi::{c_int, CString},
    fs,
    path::PathBuf,
    process,
    ptr,
    sync::atomic::{AtomicBool, AtomicUsize, Ordering},
    time::{SystemTime, UNIX_EPOCH},
};

struct DisposableRoot(PathBuf);
impl DisposableRoot {
    fn new() -> Self {
        let id = SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_nanos();
        let root = std::env::temp_dir().join(format!("fabulaxiom-vfs-fixture-{}-{id}", process::id()));
        fs::create_dir(&root).expect("fresh disposable directory");
        Self(root)
    }
    fn db(&self) -> PathBuf { self.0.join("new.sqlite3") }
}
impl Drop for DisposableRoot {
    fn drop(&mut self) { fs::remove_dir_all(&self.0).expect("fixture-only cleanup"); }
}

// sqlite3_vfs is the first field so xOpen can recover our state. The copied
// default dispatch retains the default VFS's original pAppData; only xOpen is
// intercepted. This is a laboratory proxy, NOT a hardened production VFS.
#[repr(C)]
struct FixtureVfs {
    dispatch: ffi::sqlite3_vfs,
    default_vfs: *mut ffi::sqlite3_vfs,
    allow_main_db: AtomicBool,
    deny_journal: AtomicBool,
    main_refusals: AtomicUsize,
    journal_refusals: AtomicUsize,
    main_delegations: AtomicUsize,
}

// SAFETY: SQLite invokes xOpen through this C ABI. The pointer was registered
// from a live boxed FixtureVfs; SQLite supplies writable sqlite3_file memory.
// Refusal initializes pMethods to NULL, as required by the VFS contract.
unsafe extern "C" fn fixture_xopen(
    vfs: *mut ffi::sqlite3_vfs,
    name: ffi::sqlite3_filename,
    file: *mut ffi::sqlite3_file,
    flags: c_int,
    out_flags: *mut c_int,
) -> c_int {
    let gate = unsafe { &*(vfs as *const FixtureVfs) };
    if flags & ffi::SQLITE_OPEN_MAIN_DB != 0 && !gate.allow_main_db.load(Ordering::SeqCst) {
        gate.main_refusals.fetch_add(1, Ordering::SeqCst);
        unsafe { (*file).pMethods = ptr::null() };
        return ffi::SQLITE_CANTOPEN;
    }
    if flags & ffi::SQLITE_OPEN_MAIN_JOURNAL != 0 && gate.deny_journal.load(Ordering::SeqCst) {
        gate.journal_refusals.fetch_add(1, Ordering::SeqCst);
        unsafe { (*file).pMethods = ptr::null() };
        return ffi::SQLITE_CANTOPEN;
    }
    if flags & ffi::SQLITE_OPEN_MAIN_DB != 0 {
        gate.main_delegations.fetch_add(1, Ordering::SeqCst);
    }
    let Some(delegated_open) = (unsafe { (*gate.default_vfs).xOpen }) else {
        unsafe { (*file).pMethods = ptr::null() };
        return ffi::SQLITE_CANTOPEN;
    };
    unsafe { delegated_open(gate.default_vfs, name, file, flags, out_flags) }
}

struct RegisteredFixtureVfs {
    state: Box<FixtureVfs>,
    _name: CString,
}
impl RegisteredFixtureVfs {
    fn new(allow_main_db: bool, deny_journal: bool) -> Self {
        // Distinct registered names avoid interfering with other parallel
        // SQLite tests, and makeDflt=0 never changes the process default.
        static NEXT: AtomicUsize = AtomicUsize::new(0);
        let name = CString::new(format!("fabulaxiom-vfs-test-{}-{}",
            process::id(), NEXT.fetch_add(1, Ordering::Relaxed))).unwrap();
        let default_vfs = unsafe { ffi::sqlite3_vfs_find(ptr::null()) };
        assert!(!default_vfs.is_null(), "SQLite default VFS unavailable");
        let mut state = Box::new(FixtureVfs {
            dispatch: unsafe { ptr::read(default_vfs) },
            default_vfs,
            allow_main_db: AtomicBool::new(allow_main_db),
            deny_journal: AtomicBool::new(deny_journal),
            main_refusals: AtomicUsize::new(0),
            journal_refusals: AtomicUsize::new(0),
            main_delegations: AtomicUsize::new(0),
        });
        state.dispatch.pNext = ptr::null_mut();
        state.dispatch.zName = name.as_ptr();
        state.dispatch.xOpen = Some(fixture_xopen);
        assert_eq!(unsafe { ffi::sqlite3_vfs_register(&mut state.dispatch, 0) }, ffi::SQLITE_OK);
        Self { state, _name: name }
    }
    fn name(&self) -> &str { self._name.to_str().unwrap() }
}
impl Drop for RegisteredFixtureVfs {
    fn drop(&mut self) {
        assert_eq!(unsafe { ffi::sqlite3_vfs_unregister(&mut self.state.dispatch) }, ffi::SQLITE_OK);
    }
}

#[test]
fn m32_vfs_fixture_refuses_main_before_default_xopen_and_file_creation() {
    let owned = DisposableRoot::new();
    let gate = RegisteredFixtureVfs::new(false, false);
    let path = owned.db();
    assert!(!path.exists());
    let attempt = Connection::open_with_flags_and_vfs(
        &path, OpenFlags::SQLITE_OPEN_READ_WRITE | OpenFlags::SQLITE_OPEN_CREATE, gate.name());
    assert!(attempt.is_err(), "pre-delegation VFS refusal expected");
    assert_eq!(gate.state.main_refusals.load(Ordering::SeqCst), 1);
    assert_eq!(gate.state.main_delegations.load(Ordering::SeqCst), 0);
    assert!(!path.exists(), "default xOpen never created the fixture database");
}

#[test]
fn m32_vfs_fixture_allowed_claim_delegates_real_sqlite_xopen() {
    let owned = DisposableRoot::new();
    let path = owned.db();
    let claim = fs::OpenOptions::new().write(true).create_new(true).open(&path).unwrap();
    let gate = RegisteredFixtureVfs::new(true, false);
    let db = Connection::open_with_flags_and_vfs(&path, OpenFlags::SQLITE_OPEN_READ_WRITE, gate.name())
        .expect("explicitly claimed disposable fixture");
    assert_eq!(db.query_row("SELECT 1", [], |row| row.get::<_, i64>(0)).unwrap(), 1);
    assert_eq!(gate.state.main_delegations.load(Ordering::SeqCst), 1);
    assert_eq!(gate.state.main_refusals.load(Ordering::SeqCst), 0);
    drop(db);
    drop(claim);
}

#[test]
fn m32_vfs_fixture_journal_refusal_blocks_fixture_transaction() {
    let owned = DisposableRoot::new();
    let path = owned.db();
    fs::OpenOptions::new().write(true).create_new(true).open(&path).unwrap();
    let gate = RegisteredFixtureVfs::new(true, true);
    let db = Connection::open_with_flags_and_vfs(&path, OpenFlags::SQLITE_OPEN_READ_WRITE, gate.name())
        .expect("disposable preclaimed SQLite file");
    db.execute_batch("PRAGMA journal_mode=DELETE;").unwrap();
    let result = db.execute_batch("CREATE TABLE invented(id INTEGER PRIMARY KEY, note TEXT);");
    assert!(result.is_err(), "journaling must refuse before default xOpen");
    assert!(gate.state.journal_refusals.load(Ordering::SeqCst) >= 1);
    assert!(!path.with_file_name("new.sqlite3-journal").exists());
    drop(db);
}
