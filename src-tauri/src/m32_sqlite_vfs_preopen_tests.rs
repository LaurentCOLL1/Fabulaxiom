//! Disposable Windows SQLite VFS boundary experiment, compiled only as tests.
//! A refusal at xOpen precedes default-VFS delegation; a post-xOpen FileId
//! check does not. This does NOT authenticate any Windows operator profile.
//! A separate disposable xShmMap probe uses extra SQLite-allocated file bytes
//! and an IO-methods copy; it is NOT a production VFS or an atomic opener.

use rusqlite::{ffi, Connection, OpenFlags};
use std::{
    ffi::{c_char, c_int, c_void, CStr, CString},
    fs,
    path::PathBuf,
    process,
    ptr,
    sync::atomic::{AtomicBool, AtomicUsize, Ordering},
    time::{SystemTime, UNIX_EPOCH},
};

// Test-only FILE_ID_INFO (volume + full 128-bit ID) on the actual OS handle.
// Observing two matching IDs is never a lock on the intervening pathname.
fn win_file_id_128(file: &fs::File) -> Result<(u64, [u8; 16]), String> {
    use std::os::windows::io::AsRawHandle;
    win_raw_file_id_128(file.as_raw_handle())
}

fn win_raw_file_id_128(handle: *mut c_void) -> Result<(u64, [u8; 16]), String> {
    #[repr(C)]
    struct FileIdInfo { volume: u64, id: [u8; 16] }
    #[link(name = "kernel32")]
    unsafe extern "system" {
        fn GetFileInformationByHandleEx(
            handle: *mut c_void, class: i32, data: *mut c_void, size: u32,
        ) -> i32;
    }
    const FILE_ID_INFO_CLASS: i32 = 0x12;
    let mut info = std::mem::MaybeUninit::<FileIdInfo>::uninit();
    let result = unsafe {
        GetFileInformationByHandleEx(handle, FILE_ID_INFO_CLASS,
            info.as_mut_ptr().cast(), std::mem::size_of::<FileIdInfo>() as u32)
    };
    if result == 0 {
        return Err(format!("STOP: FileIdInfo unavailable: {}", std::io::Error::last_os_error()));
    }
    let info = unsafe { info.assume_init() };
    Ok((info.volume, info.id))
}

fn sqlite_opened_file_id_128(db: &Connection) -> Result<(u64, [u8; 16]), String> {
    let mut handle: *mut c_void = ptr::null_mut();
    // Borrow SQLite's actual Windows handle AFTER xOpen; never close it.
    let code = unsafe {
        ffi::sqlite3_file_control(db.handle(), b"main\0".as_ptr().cast::<c_char>(),
            ffi::SQLITE_FCNTL_WIN32_GET_HANDLE,
            (&mut handle as *mut *mut c_void).cast())
    };
    if code != ffi::SQLITE_OK || handle.is_null() {
        return Err(format!("STOP: SQLite native handle unavailable: {code}"));
    }
    win_raw_file_id_128(handle)
}

struct FileIdPrecheckPlan {
    path: PathBuf,
    expected: (u64, [u8; 16]),
    // Experimental in-xOpen *veto*: verify the delegated handle before this
    // callback returns to SQLite, never manufacture runtime writer admission.
    check_delegated_handle: bool,
    // A controlled fixture-only move between a successful precheck and the
    // default VFS xOpen, to make the TOCTOU gap deterministic.
    move_original_to: Option<PathBuf>,
}

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
    file_tail_offset: usize,
    wrap_main_shm: bool,
    deny_shm: AtomicBool,
    shm_map_refusals: AtomicUsize,
    shm_map_delegations: AtomicUsize,
    allow_main_db: AtomicBool,
    deny_journal: AtomicBool,
    deny_wal: AtomicBool,
    main_refusals: AtomicUsize,
    journal_refusals: AtomicUsize,
    wal_refusals: AtomicUsize,
    wal_delegations: AtomicUsize,
    // The default Windows xShmMap path does not pass through this xOpen hook.
    shm_named_xopens: AtomicUsize,
    main_delegations: AtomicUsize,
    precheck: Option<FileIdPrecheckPlan>,
    precheck_acceptances: AtomicUsize,
    precheck_refusals: AtomicUsize,
    swaps_after_precheck: AtomicUsize,
    delegated_handle_matches: AtomicUsize,
    delegated_handle_refusals: AtomicUsize,
}

// The default Win32 sqlite3_file occupies the first default_vfs.szOsFile bytes.
// SQLite allocates our larger dispatch.szOsFile; this aligned tail belongs to
// the *same disposable file object*, not to a process-global map. Its copied
// method table changes ONLY xShmMap, all other Win32 methods stay delegated.
#[repr(C)]
struct FixtureMainFileTail {
    methods: ffi::sqlite3_io_methods,
    original_methods: *const ffi::sqlite3_io_methods,
    vfs: *const FixtureVfs,
}

unsafe extern "C" fn fixture_xshm_map(
    file: *mut ffi::sqlite3_file,
    page: c_int,
    page_size: c_int,
    extend: c_int,
    mapped: *mut *mut c_void,
) -> c_int {
    // The copied io_methods table is the FIRST field of our aligned file tail.
    let tail = unsafe { &*((*file).pMethods as *const FixtureMainFileTail) };
    let gate = unsafe { &*tail.vfs };
    if gate.deny_shm.load(Ordering::SeqCst) {
        gate.shm_map_refusals.fetch_add(1, Ordering::SeqCst);
        unsafe { *mapped = ptr::null_mut() };
        return ffi::SQLITE_IOERR_SHMMAP;
    }
    gate.shm_map_delegations.fetch_add(1, Ordering::SeqCst);
    let Some(original) = (unsafe { (*tail.original_methods).xShmMap }) else {
        unsafe { *mapped = ptr::null_mut() };
        return ffi::SQLITE_IOERR_SHMMAP;
    };
    unsafe { original(file, page, page_size, extend, mapped) }
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
    if !name.is_null() {
        let bytes = unsafe { CStr::from_ptr(name) }.to_bytes();
        if bytes.ends_with(b"-shm") {
            gate.shm_named_xopens.fetch_add(1, Ordering::SeqCst);
        }
    }
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
    if flags & ffi::SQLITE_OPEN_WAL != 0 && gate.deny_wal.load(Ordering::SeqCst) {
        gate.wal_refusals.fetch_add(1, Ordering::SeqCst);
        unsafe { (*file).pMethods = ptr::null() };
        return ffi::SQLITE_CANTOPEN;
    }
    if flags & ffi::SQLITE_OPEN_WAL != 0 {
        gate.wal_delegations.fetch_add(1, Ordering::SeqCst);
    }
    if flags & ffi::SQLITE_OPEN_MAIN_DB != 0 {
        if let Some(plan) = &gate.precheck {
            let observed = fs::File::open(&plan.path)
                .map_err(|e| e.to_string())
                .and_then(|file| win_file_id_128(&file));
            if observed != Ok(plan.expected) {
                gate.precheck_refusals.fetch_add(1, Ordering::SeqCst);
                unsafe { (*file).pMethods = ptr::null() };
                return ffi::SQLITE_CANTOPEN;
            }
            gate.precheck_acceptances.fetch_add(1, Ordering::SeqCst);
            if let Some(displaced) = &plan.move_original_to {
                // Deliberately release the temporary observation handle,
                // rename the owned original and install an owned replacement
                // BEFORE delegating to the Windows VFS. Never operator I/O.
                if fs::rename(&plan.path, displaced).is_err()
                    || fs::OpenOptions::new().write(true).create_new(true)
                        .open(&plan.path).is_err()
                {
                    unsafe { (*file).pMethods = ptr::null() };
                    return ffi::SQLITE_CANTOPEN;
                }
                gate.swaps_after_precheck.fetch_add(1, Ordering::SeqCst);
            }
        }
        gate.main_delegations.fetch_add(1, Ordering::SeqCst);
    }
    let Some(delegated_open) = (unsafe { (*gate.default_vfs).xOpen }) else {
        unsafe { (*file).pMethods = ptr::null() };
        return ffi::SQLITE_CANTOPEN;
    };
    let result = unsafe { delegated_open(gate.default_vfs, name, file, flags, out_flags) };
    if result == ffi::SQLITE_OK && flags & ffi::SQLITE_OPEN_MAIN_DB != 0 {
        if let Some(plan) = &gate.precheck {
            if plan.check_delegated_handle {
                // Exactly the file object returned by the *delegated* xOpen.
                // A separate post-Connection-open check would be too late.
                let methods = unsafe { (*file).pMethods };
                let mut handle: *mut c_void = ptr::null_mut();
                let control = if methods.is_null() {
                    ffi::SQLITE_CANTOPEN
                } else if let Some(file_control) = unsafe { (*methods).xFileControl } {
                    unsafe { file_control(file, ffi::SQLITE_FCNTL_WIN32_GET_HANDLE,
                        (&mut handle as *mut *mut c_void).cast()) }
                } else { ffi::SQLITE_CANTOPEN };
                let identity = if control == ffi::SQLITE_OK && !handle.is_null() {
                    win_raw_file_id_128(handle).ok()
                } else { None };
                if identity != Some(plan.expected) {
                    gate.delegated_handle_refusals.fetch_add(1, Ordering::SeqCst);
                    if !methods.is_null() {
                        if let Some(close) = unsafe { (*methods).xClose } {
                            let _ = unsafe { close(file) };
                        }
                    }
                    unsafe { (*file).pMethods = ptr::null() };
                    return ffi::SQLITE_CANTOPEN;
                }
                gate.delegated_handle_matches.fetch_add(1, Ordering::SeqCst);
            }
        }
    }
    if result == ffi::SQLITE_OK && flags & ffi::SQLITE_OPEN_MAIN_DB != 0 && gate.wrap_main_shm {
        let original = unsafe { (*file).pMethods };
        if original.is_null() || unsafe { (*original).iVersion } < 2
            || (unsafe { (*original).xShmMap }).is_none()
        {
            if !original.is_null() {
                if let Some(close) = unsafe { (*original).xClose } {
                    let _ = unsafe { close(file) };
                }
            }
            unsafe { (*file).pMethods = ptr::null() };
            return ffi::SQLITE_CANTOPEN;
        }
        let tail = unsafe { (file as *mut u8).add(gate.file_tail_offset) }
            as *mut FixtureMainFileTail;
        let mut methods = unsafe { ptr::read(original) };
        methods.xShmMap = Some(fixture_xshm_map);
        unsafe {
            ptr::write(tail, FixtureMainFileTail {
                methods, original_methods: original, vfs: gate,
            });
            (*file).pMethods = &(*tail).methods;
        }
    }
    result
}

struct RegisteredFixtureVfs {
    state: Box<FixtureVfs>,
    _name: CString,
}
impl RegisteredFixtureVfs {
    fn new(allow_main_db: bool, deny_journal: bool) -> Self {
        Self::with_precheck_and_wal(allow_main_db, deny_journal, false, None)
    }

    fn with_wal_policy(deny_wal: bool) -> Self {
        Self::with_precheck_and_wal(true, false, deny_wal, None)
    }

    fn with_precheck(
        allow_main_db: bool, deny_journal: bool, precheck: Option<FileIdPrecheckPlan>,
    ) -> Self {
        Self::with_precheck_and_wal(allow_main_db, deny_journal, false, precheck)
    }

    fn with_precheck_and_wal(
        allow_main_db: bool, deny_journal: bool, deny_wal: bool,
        precheck: Option<FileIdPrecheckPlan>,
    ) -> Self {
        Self::with_policy(allow_main_db, deny_journal, deny_wal, precheck, None)
    }

    fn with_shm_policy(deny_shm: bool) -> Self {
        Self::with_policy(true, false, false, None, Some(deny_shm))
    }

    fn with_policy(
        allow_main_db: bool, deny_journal: bool, deny_wal: bool,
        precheck: Option<FileIdPrecheckPlan>, shm_policy: Option<bool>,
    ) -> Self {
        // Distinct registered names avoid interfering with other parallel
        // SQLite tests, and makeDflt=0 never changes the process default.
        static NEXT: AtomicUsize = AtomicUsize::new(0);
        let name = CString::new(format!("fabulaxiom-vfs-test-{}-{}",
            process::id(), NEXT.fetch_add(1, Ordering::Relaxed))).unwrap();
        let default_vfs = unsafe { ffi::sqlite3_vfs_find(ptr::null()) };
        assert!(!default_vfs.is_null(), "SQLite default VFS unavailable");
        let default_file_size = unsafe { (*default_vfs).szOsFile } as usize;
        let tail_align = std::mem::align_of::<FixtureMainFileTail>();
        let file_tail_offset = default_file_size.div_ceil(tail_align) * tail_align;
        let wrapped_file_size = file_tail_offset + std::mem::size_of::<FixtureMainFileTail>();
        assert!(wrapped_file_size <= c_int::MAX as usize);
        let mut state = Box::new(FixtureVfs {
            dispatch: unsafe { ptr::read(default_vfs) },
            default_vfs,
            file_tail_offset,
            wrap_main_shm: shm_policy.is_some(),
            deny_shm: AtomicBool::new(shm_policy.unwrap_or(false)),
            shm_map_refusals: AtomicUsize::new(0),
            shm_map_delegations: AtomicUsize::new(0),
            allow_main_db: AtomicBool::new(allow_main_db),
            deny_journal: AtomicBool::new(deny_journal),
            deny_wal: AtomicBool::new(deny_wal),
            main_refusals: AtomicUsize::new(0),
            journal_refusals: AtomicUsize::new(0),
            wal_refusals: AtomicUsize::new(0),
            wal_delegations: AtomicUsize::new(0),
            shm_named_xopens: AtomicUsize::new(0),
            main_delegations: AtomicUsize::new(0),
            precheck,
            precheck_acceptances: AtomicUsize::new(0),
            precheck_refusals: AtomicUsize::new(0),
            swaps_after_precheck: AtomicUsize::new(0),
            delegated_handle_matches: AtomicUsize::new(0),
            delegated_handle_refusals: AtomicUsize::new(0),
        });
        state.dispatch.pNext = ptr::null_mut();
        state.dispatch.zName = name.as_ptr();
        if shm_policy.is_some() {
            state.dispatch.szOsFile = wrapped_file_size as c_int;
        }
        state.dispatch.xOpen = Some(fixture_xopen);
        assert_eq!(unsafe { ffi::sqlite3_vfs_register(&mut state.dispatch, 0) }, ffi::SQLITE_OK);
        Self { state, _name: name }
    }
    fn name(&self) -> &str { self._name.to_str().unwrap() }
}

#[test]
fn m32_vfs_fixture_fileid128_precheck_accepts_stable_disposable_identity() {
    let owned = DisposableRoot::new();
    let path = owned.db();
    fs::OpenOptions::new().write(true).create_new(true).open(&path).unwrap();
    let expected = win_file_id_128(&fs::File::open(&path).unwrap()).unwrap();
    let gate = RegisteredFixtureVfs::with_precheck(true, false, Some(FileIdPrecheckPlan {
        path: path.clone(), expected, check_delegated_handle: false, move_original_to: None,
    }));
    let db = Connection::open_with_flags_and_vfs(&path, OpenFlags::SQLITE_OPEN_READ_WRITE, gate.name())
        .expect("stable owned test path should delegate");
    assert_eq!(sqlite_opened_file_id_128(&db).unwrap(), expected);
    assert_eq!(gate.state.precheck_acceptances.load(Ordering::SeqCst), 1);
    assert_eq!(gate.state.main_delegations.load(Ordering::SeqCst), 1);
    drop(db);
}

#[test]
fn m32_vfs_fixture_fileid128_precheck_refuses_already_replaced_name() {
    let owned = DisposableRoot::new();
    let path = owned.db();
    let displaced = owned.0.join("prior.sqlite3");
    fs::OpenOptions::new().write(true).create_new(true).open(&path).unwrap();
    let expected = win_file_id_128(&fs::File::open(&path).unwrap()).unwrap();
    fs::rename(&path, &displaced).unwrap();
    fs::OpenOptions::new().write(true).create_new(true).open(&path).unwrap();
    let gate = RegisteredFixtureVfs::with_precheck(true, false, Some(FileIdPrecheckPlan {
        path: path.clone(), expected, check_delegated_handle: false, move_original_to: None,
    }));
    let result = Connection::open_with_flags_and_vfs(&path, OpenFlags::SQLITE_OPEN_READ_WRITE, gate.name());
    assert!(result.is_err(), "already replaced owned name must refuse before delegate");
    assert_eq!(gate.state.precheck_refusals.load(Ordering::SeqCst), 1);
    assert_eq!(gate.state.main_delegations.load(Ordering::SeqCst), 0);
    assert_eq!(win_file_id_128(&fs::File::open(&displaced).unwrap()).unwrap(), expected);
}

#[test]
fn m32_vfs_fixture_fileid128_precheck_then_internal_name_swap_is_not_atomic() {
    let owned = DisposableRoot::new();
    let path = owned.db();
    let displaced = owned.0.join("prior.sqlite3");
    fs::OpenOptions::new().write(true).create_new(true).open(&path).unwrap();
    let expected = win_file_id_128(&fs::File::open(&path).unwrap()).unwrap();
    let gate = RegisteredFixtureVfs::with_precheck(true, false, Some(FileIdPrecheckPlan {
        path: path.clone(), expected, check_delegated_handle: false,
        move_original_to: Some(displaced.clone()),
    }));
    let db = Connection::open_with_flags_and_vfs(&path, OpenFlags::SQLITE_OPEN_READ_WRITE, gate.name())
        .expect("SQLite default VFS follows the substituted fixture name");
    // Do NOT issue SQL to the substituted file; the post-open mismatch alone
    // demonstrates why a positive precheck is NOT an atomic authorization.
    let actual = sqlite_opened_file_id_128(&db).unwrap();
    assert_eq!(gate.state.precheck_acceptances.load(Ordering::SeqCst), 1);
    assert_eq!(gate.state.swaps_after_precheck.load(Ordering::SeqCst), 1);
    assert_eq!(gate.state.main_delegations.load(Ordering::SeqCst), 1);
    assert_ne!(actual, expected, "pre-xOpen FileId equality did not bind delegated xOpen");
    assert_eq!(actual, win_file_id_128(&fs::File::open(&path).unwrap()).unwrap());
    assert_eq!(expected, win_file_id_128(&fs::File::open(&displaced).unwrap()).unwrap());
    drop(db);
}

#[test]
fn m32_vfs_fixture_xopen_delegated_handle_matches_before_sqlite_accepts() {
    let owned = DisposableRoot::new();
    let path = owned.db();
    fs::OpenOptions::new().write(true).create_new(true).open(&path).unwrap();
    let expected = win_file_id_128(&fs::File::open(&path).unwrap()).unwrap();
    let gate = RegisteredFixtureVfs::with_precheck(true, false, Some(FileIdPrecheckPlan {
        path: path.clone(), expected, check_delegated_handle: true, move_original_to: None,
    }));
    let db = Connection::open_with_flags_and_vfs(&path, OpenFlags::SQLITE_OPEN_READ_WRITE, gate.name())
        .expect("only the unchanged disposable delegated handle may return to SQLite");
    assert_eq!(sqlite_opened_file_id_128(&db).unwrap(), expected);
    assert_eq!(gate.state.delegated_handle_matches.load(Ordering::SeqCst), 1);
    assert_eq!(gate.state.delegated_handle_refusals.load(Ordering::SeqCst), 0);
    drop(db);
}

#[test]
fn m32_vfs_fixture_xopen_delegated_substitution_closes_and_vetoes() {
    let owned = DisposableRoot::new();
    let path = owned.db();
    let displaced = owned.0.join("prior.sqlite3");
    fs::OpenOptions::new().write(true).create_new(true).open(&path).unwrap();
    let expected = win_file_id_128(&fs::File::open(&path).unwrap()).unwrap();
    let gate = RegisteredFixtureVfs::with_precheck(true, false, Some(FileIdPrecheckPlan {
        path: path.clone(), expected, check_delegated_handle: true,
        move_original_to: Some(displaced.clone()),
    }));
    let attempt = Connection::open_with_flags_and_vfs(&path, OpenFlags::SQLITE_OPEN_READ_WRITE, gate.name());
    assert!(attempt.is_err(), "substitution between precheck and delegated xOpen must refuse");
    assert_eq!(gate.state.precheck_acceptances.load(Ordering::SeqCst), 1);
    assert_eq!(gate.state.swaps_after_precheck.load(Ordering::SeqCst), 1);
    assert_eq!(gate.state.main_delegations.load(Ordering::SeqCst), 1);
    assert_eq!(gate.state.delegated_handle_refusals.load(Ordering::SeqCst), 1);
    assert_eq!(gate.state.delegated_handle_matches.load(Ordering::SeqCst), 0);
    assert_eq!(win_file_id_128(&fs::File::open(&displaced).unwrap()).unwrap(), expected);
    assert_ne!(win_file_id_128(&fs::File::open(&path).unwrap()).unwrap(), expected);
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

#[test]
fn m32_vfs_fixture_wal_refusal_precedes_named_default_open() {
    let owned = DisposableRoot::new();
    let path = owned.db();
    fs::OpenOptions::new().write(true).create_new(true).open(&path).unwrap();
    let gate = RegisteredFixtureVfs::with_wal_policy(true);
    let db = Connection::open_with_flags_and_vfs(&path, OpenFlags::SQLITE_OPEN_READ_WRITE, gate.name())
        .expect("only a new owned fixture may be opened");
    // WAL selection or the first transaction must try to open the -wal file.
    // No live profile, sidecar or migration participates in this exercise.
    let switch = db.execute_batch("PRAGMA journal_mode=WAL;");
    if switch.is_ok() {
        assert!(db.execute_batch("CREATE TABLE invented(id INTEGER PRIMARY KEY);").is_err());
    }
    assert!(gate.state.wal_refusals.load(Ordering::SeqCst) >= 1);
    assert_eq!(gate.state.wal_delegations.load(Ordering::SeqCst), 0);
    assert!(!owned.0.join("new.sqlite3-wal").exists());
    drop(db);
}

#[test]
fn m32_vfs_fixture_wal_xopen_does_not_cover_shm_mapping() {
    let owned = DisposableRoot::new();
    let path = owned.db();
    fs::OpenOptions::new().write(true).create_new(true).open(&path).unwrap();
    let gate = RegisteredFixtureVfs::with_wal_policy(false);
    let db = Connection::open_with_flags_and_vfs(&path, OpenFlags::SQLITE_OPEN_READ_WRITE, gate.name())
        .expect("only a new owned fixture may be opened");
    let journal_mode: String = db.query_row("PRAGMA journal_mode=WAL", [], |row| row.get(0)).unwrap();
    assert_eq!(journal_mode.to_ascii_lowercase(), "wal");
    db.execute_batch("CREATE TABLE invented(id INTEGER PRIMARY KEY);").unwrap();
    assert!(gate.state.wal_delegations.load(Ordering::SeqCst) >= 1);
    assert!(owned.0.join("new.sqlite3-shm").exists(),
        "default Windows xShmMap creates the owned WAL index while the connection lives");
    assert_eq!(gate.state.shm_named_xopens.load(Ordering::SeqCst), 0,
        "a name-only xOpen policy did not authorize or intercept -shm");
    drop(db);
}

#[test]
fn m32_vfs_fixture_wrapped_shm_map_refuses_before_default_mapping() {
    let owned = DisposableRoot::new();
    let path = owned.db();
    fs::OpenOptions::new().write(true).create_new(true).open(&path).unwrap();
    let gate = RegisteredFixtureVfs::with_shm_policy(true);
    let db = Connection::open_with_flags_and_vfs(&path, OpenFlags::SQLITE_OPEN_READ_WRITE, gate.name())
        .expect("owned fixture, wrapped main-file methods");
    let switch = db.execute_batch("PRAGMA journal_mode=WAL;");
    if switch.is_ok() {
        assert!(db.execute_batch("CREATE TABLE invented(id INTEGER PRIMARY KEY);").is_err());
    }
    assert!(gate.state.shm_map_refusals.load(Ordering::SeqCst) >= 1);
    assert_eq!(gate.state.shm_map_delegations.load(Ordering::SeqCst), 0);
    assert!(!owned.0.join("new.sqlite3-shm").exists(),
        "the default Windows xShmMap was not reached to create the WAL index");
    drop(db);
}

#[test]
fn m32_vfs_fixture_wrapped_shm_map_delegates_disposable_wal() {
    let owned = DisposableRoot::new();
    let path = owned.db();
    fs::OpenOptions::new().write(true).create_new(true).open(&path).unwrap();
    let gate = RegisteredFixtureVfs::with_shm_policy(false);
    let db = Connection::open_with_flags_and_vfs(&path, OpenFlags::SQLITE_OPEN_READ_WRITE, gate.name())
        .expect("owned fixture, wrapped main-file methods");
    let mode: String = db.query_row("PRAGMA journal_mode=WAL", [], |r| r.get(0)).unwrap();
    assert_eq!(mode.to_ascii_lowercase(), "wal");
    db.execute_batch("CREATE TABLE invented(id INTEGER PRIMARY KEY);").unwrap();
    assert!(gate.state.shm_map_delegations.load(Ordering::SeqCst) >= 1);
    assert_eq!(gate.state.shm_map_refusals.load(Ordering::SeqCst), 0);
    assert!(owned.0.join("new.sqlite3-shm").exists());
    assert_eq!(gate.state.shm_named_xopens.load(Ordering::SeqCst), 0,
        "the io_methods hook, not the xOpen filename hook, mediated WAL mapping");
    drop(db);
}
