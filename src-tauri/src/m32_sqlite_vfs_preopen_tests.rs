//! Disposable Windows SQLite VFS boundary experiment, compiled only as tests.
//! A refusal at xOpen precedes default-VFS delegation; a post-xOpen FileId
//! check does not. This does NOT authenticate any Windows operator profile.
//! Disposable D2 xShmMap and D3a xShmLock/xShmBarrier/xShmUnmap/xClose
//! probes use SQLite-allocated extra bytes; D3b kills only a CI fixture child.
//! No production VFS, crash recovery, operator file or atomic opener.

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


// R3 next step: prove ReOpenFile reaches the actual SQLite xOpen callback.
// A cloned Win32 HANDLE is NOT a valid sqlite3_file until a complete audited
// io_methods adapter exists. Every attempt below MUST fail closed.
fn r3_clone_preopened_handle(held: &fs::File) -> Option<fs::File> {
    use std::os::windows::io::{AsRawHandle, FromRawHandle};
    #[link(name = "kernel32")]
    unsafe extern "system" {
        fn ReOpenFile(handle: *mut c_void, access: u32, share: u32, flags: u32) -> *mut c_void;
    }
    const GENERIC_READ: u32 = 0x8000_0000;
    const GENERIC_WRITE: u32 = 0x4000_0000;
    const FILE_SHARE_READ_WRITE_DELETE: u32 = 1 | 2 | 4;
    let handle = unsafe {
        ReOpenFile(held.as_raw_handle().cast(),
            GENERIC_READ | GENERIC_WRITE, FILE_SHARE_READ_WRITE_DELETE, 0)
    };
    if handle.is_null() || handle as isize == -1 { return None; }
    // The clone is a *new* HANDLE; File closes only this clone.
    Some(unsafe { fs::File::from_raw_handle(handle.cast()) })
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
    // R3 closed-world callback probe: no default VFS xOpen allowed.
    r3_preopened: Option<fs::File>,
    r3_expected: Option<(u64, [u8; 16])>,
    r3_callback_matches: AtomicUsize,
    r3_callback_refusals: AtomicUsize,
    precheck: Option<FileIdPrecheckPlan>,
    precheck_acceptances: AtomicUsize,
    precheck_refusals: AtomicUsize,
    swaps_after_precheck: AtomicUsize,
    delegated_handle_matches: AtomicUsize,
    delegated_handle_refusals: AtomicUsize,
    // D3a only: record the actual delegated Windows -wal handle and the
    // complete SHM/close callbacks on disposable SQLite files, never runtime.
    d3a_wal_path: Option<PathBuf>,
    d3a_wrong_expected_wal_id: Option<(u64, [u8; 16])>,
    d3a_require_complete_shm: bool,
    d3a_simulate_missing_shm_lock: bool,
    d3a_deny_shm_lock: AtomicBool,
    d3a_wal_identity_matches: AtomicUsize,
    d3a_wal_identity_refusals: AtomicUsize,
    d3a_wal_veto_close_calls: AtomicUsize,
    d3a_method_refusals: AtomicUsize,
    d3a_shm_lock_refusals: AtomicUsize,
    d3a_shm_lock_delegations: AtomicUsize,
    d3a_shm_barrier_delegations: AtomicUsize,
    d3a_shm_unmap_delegations: AtomicUsize,
    d3a_shm_unmap_failures: AtomicUsize,
    d3a_main_close_successes: AtomicUsize,
    d3a_wal_close_successes: AtomicUsize,
    d3a_close_failures: AtomicUsize,
    // R4: capture only the actual returned xShmMap region-0 view on a NEW fixture.
    r4_actual_xshm_region0: AtomicUsize,
    r4_actual_xshm_region0_size: AtomicUsize,
}

// The default Win32 sqlite3_file occupies the first default_vfs.szOsFile bytes.
// SQLite allocates our larger dispatch.szOsFile; this aligned tail belongs to
// the *same disposable file object*, not to a process-global map. D2 changes
// only xShmMap; D3a additionally WRAPS lock/barrier/unmap/close with real
// Win32 delegation. Neither mode changes an operator or default VFS.
#[repr(C)]
struct FixtureMainFileTail {
    methods: ffi::sqlite3_io_methods,
    original_methods: *const ffi::sqlite3_io_methods,
    vfs: *const FixtureVfs,
    is_wal: bool,
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
    let rc = unsafe { original(file, page, page_size, extend, mapped) };
    if rc == ffi::SQLITE_OK && page == 0 && !mapped.is_null() &&
        !(unsafe { *mapped }).is_null() && page_size >= 136 {
        gate.r4_actual_xshm_region0.store(unsafe { *mapped } as usize, Ordering::SeqCst);
        gate.r4_actual_xshm_region0_size.store(page_size as usize, Ordering::SeqCst);
    }
    rc
}


// D3a's copied main-file io_methods table retains the original Win32 methods.
// xShmLock is an error-returning callback; xShmBarrier is void and therefore
// cannot express a veto. A missing barrier is refused while installing the
// D3a wrapper, before any SQLite SQL and before any SHM mapping.
unsafe extern "C" fn fixture_d3a_xshm_lock(
    file: *mut ffi::sqlite3_file, offset: c_int, count: c_int, flags: c_int,
) -> c_int {
    let tail = unsafe { &*((*file).pMethods as *const FixtureMainFileTail) };
    let gate = unsafe { &*tail.vfs };
    if gate.d3a_deny_shm_lock.load(Ordering::SeqCst) {
        gate.d3a_shm_lock_refusals.fetch_add(1, Ordering::SeqCst);
        return ffi::SQLITE_IOERR;
    }
    let Some(original) = (unsafe { (*tail.original_methods).xShmLock }) else {
        gate.d3a_shm_lock_refusals.fetch_add(1, Ordering::SeqCst);
        return ffi::SQLITE_IOERR;
    };
    gate.d3a_shm_lock_delegations.fetch_add(1, Ordering::SeqCst);
    unsafe { original(file, offset, count, flags) }
}

unsafe extern "C" fn fixture_d3a_xshm_barrier(file: *mut ffi::sqlite3_file) {
    let tail = unsafe { &*((*file).pMethods as *const FixtureMainFileTail) };
    let gate = unsafe { &*tail.vfs };
    gate.d3a_shm_barrier_delegations.fetch_add(1, Ordering::SeqCst);
    if let Some(original) = unsafe { (*tail.original_methods).xShmBarrier } {
        unsafe { original(file) };
    }
}

unsafe extern "C" fn fixture_d3a_xshm_unmap(
    file: *mut ffi::sqlite3_file, delete_flag: c_int,
) -> c_int {
    let tail = unsafe { &*((*file).pMethods as *const FixtureMainFileTail) };
    let gate = unsafe { &*tail.vfs };
    gate.d3a_shm_unmap_delegations.fetch_add(1, Ordering::SeqCst);
    let Some(original) = (unsafe { (*tail.original_methods).xShmUnmap }) else {
        gate.d3a_shm_unmap_failures.fetch_add(1, Ordering::SeqCst);
        return ffi::SQLITE_IOERR;
    };
    let result = unsafe { original(file, delete_flag) };
    if result != ffi::SQLITE_OK {
        gate.d3a_shm_unmap_failures.fetch_add(1, Ordering::SeqCst);
    }
    result
}

// Capture close outcome on main and WAL separately. The delegated xClose
// must really run; a Rust Drop or a mutex release is not close attestation.
unsafe extern "C" fn fixture_d3a_xclose(file: *mut ffi::sqlite3_file) -> c_int {
    let tail = unsafe { &*((*file).pMethods as *const FixtureMainFileTail) };
    let gate = unsafe { &*tail.vfs };
    let result = match unsafe { (*tail.original_methods).xClose } {
        Some(original) => unsafe { original(file) },
        None => ffi::SQLITE_IOERR,
    };
    if result == ffi::SQLITE_OK {
        if tail.is_wal {
            gate.d3a_wal_close_successes.fetch_add(1, Ordering::SeqCst);
        } else {
            gate.d3a_main_close_successes.fetch_add(1, Ordering::SeqCst);
        }
    } else {
        gate.d3a_close_failures.fetch_add(1, Ordering::SeqCst);
    }
    result
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
    // Never delegate a pathname to Win32 SQLite when a preopened HANDLE
    // is handed to this test-only VFS. Prove callback ownership, then STOP.
    if let Some(held) = &gate.r3_preopened {
        if flags & ffi::SQLITE_OPEN_MAIN_DB != 0 {
            let reopened_id = r3_clone_preopened_handle(held)
                .and_then(|clone| win_file_id_128(&clone).ok());
            if reopened_id.is_some() && reopened_id == gate.r3_expected {
                gate.r3_callback_matches.fetch_add(1, Ordering::SeqCst);
            } else {
                gate.r3_callback_refusals.fetch_add(1, Ordering::SeqCst);
            }
        } else {
            gate.r3_callback_refusals.fetch_add(1, Ordering::SeqCst);
        }
        unsafe { (*file).pMethods = ptr::null() };
        return ffi::SQLITE_CANTOPEN; // io_methods NOT implemented; no fallback!
    }
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
    // D3a WAL identity is checked on the ACTUAL delegated sqlite3_file,
    // never only on a pre-xOpen pathname. A second path observation is still
    // non-atomic; this test cannot establish hostile same-SID exclusion.
    if result == ffi::SQLITE_OK && flags & ffi::SQLITE_OPEN_WAL != 0 {
        if let Some(path) = &gate.d3a_wal_path {
            let original = unsafe { (*file).pMethods };
            let mut handle: *mut c_void = ptr::null_mut();
            let control = if original.is_null() {
                ffi::SQLITE_CANTOPEN
            } else if let Some(file_control) = unsafe { (*original).xFileControl } {
                unsafe { file_control(file, ffi::SQLITE_FCNTL_WIN32_GET_HANDLE,
                    (&mut handle as *mut *mut c_void).cast()) }
            } else { ffi::SQLITE_CANTOPEN };
            let actual = if control == ffi::SQLITE_OK && !handle.is_null() {
                win_raw_file_id_128(handle).ok()
            } else { None };
            let observed_owned_name = fs::File::open(path)
                .ok().and_then(|owned| win_file_id_128(&owned).ok());
            let named_wal = !name.is_null() && unsafe { CStr::from_ptr(name) }
                .to_bytes().ends_with(b"new.sqlite3-wal");
            let expected = gate.d3a_wrong_expected_wal_id.or(observed_owned_name);
            if !named_wal || actual.is_none() || actual != expected {
                gate.d3a_wal_identity_refusals.fetch_add(1, Ordering::SeqCst);
                if !original.is_null() {
                    if let Some(close) = unsafe { (*original).xClose } {
                        gate.d3a_wal_veto_close_calls.fetch_add(1, Ordering::SeqCst);
                        let _ = unsafe { close(file) };
                    }
                }
                unsafe { (*file).pMethods = ptr::null() };
                return ffi::SQLITE_CANTOPEN;
            }
            // The WAL file's own copied xClose is observed separately from
            // the main handle and is installed only after identity match.
            if original.is_null() || (unsafe { (*original).xClose }).is_none() {
                gate.d3a_wal_identity_refusals.fetch_add(1, Ordering::SeqCst);
                unsafe { (*file).pMethods = ptr::null() };
                return ffi::SQLITE_CANTOPEN;
            }
            let tail = unsafe { (file as *mut u8).add(gate.file_tail_offset) }
                as *mut FixtureMainFileTail;
            let mut methods = unsafe { ptr::read(original) };
            methods.xClose = Some(fixture_d3a_xclose);
            unsafe {
                ptr::write(tail, FixtureMainFileTail {
                    methods, original_methods: original, vfs: gate, is_wal: true,
                });
                (*file).pMethods = &(*tail).methods;
            }
            gate.d3a_wal_identity_matches.fetch_add(1, Ordering::SeqCst);
        }
    }
    if result == ffi::SQLITE_OK && flags & ffi::SQLITE_OPEN_MAIN_DB != 0 && gate.wrap_main_shm {
        let original = unsafe { (*file).pMethods };
        let d3a_missing = gate.d3a_require_complete_shm && (
            gate.d3a_simulate_missing_shm_lock
            || original.is_null()
            || (unsafe { (*original).xShmLock }).is_none()
            || (unsafe { (*original).xShmBarrier }).is_none()
            || (unsafe { (*original).xShmUnmap }).is_none()
            || (unsafe { (*original).xClose }).is_none()
        );
        if original.is_null() || unsafe { (*original).iVersion } < 2
            || (unsafe { (*original).xShmMap }).is_none() || d3a_missing
        {
            if gate.d3a_require_complete_shm {
                gate.d3a_method_refusals.fetch_add(1, Ordering::SeqCst);
            }
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
        if gate.d3a_require_complete_shm {
            methods.xShmLock = Some(fixture_d3a_xshm_lock);
            methods.xShmBarrier = Some(fixture_d3a_xshm_barrier);
            methods.xShmUnmap = Some(fixture_d3a_xshm_unmap);
            methods.xClose = Some(fixture_d3a_xclose);
        }
        unsafe {
            ptr::write(tail, FixtureMainFileTail {
                methods, original_methods: original, vfs: gate, is_wal: false,
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

    // Main HANDLE must be created by the test fixture; never a path opener.
    fn with_preopened_r3(held: fs::File) -> Self {
        let id = win_file_id_128(&held).expect("R3 disposable Win32 FileId128");
        let mut gate = Self::with_policy(true, false, false, None, None);
        gate.state.r3_expected = Some(id);
        gate.state.r3_preopened = Some(held);
        gate
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

    // Only D3a disposable Windows fixtures can enable the stronger WAL/SHM
    // observation. No production opener, actor, D3b or operator path.
    fn with_d3a(
        main_path: PathBuf, expected_main: (u64, [u8; 16]),
        wrong_wal_id: Option<(u64, [u8; 16])>,
        deny_shm_lock: bool, simulate_missing_shm_lock: bool,
    ) -> Self {
        let mut gate = Self::with_policy(true, false, false,
            Some(FileIdPrecheckPlan {
                path: main_path.clone(), expected: expected_main,
                check_delegated_handle: true, move_original_to: None,
            }), Some(false));
        gate.state.d3a_wal_path = Some(main_path.with_file_name("new.sqlite3-wal"));
        gate.state.d3a_wrong_expected_wal_id = wrong_wal_id;
        gate.state.d3a_require_complete_shm = true;
        gate.state.d3a_simulate_missing_shm_lock = simulate_missing_shm_lock;
        gate.state.d3a_deny_shm_lock.store(deny_shm_lock, Ordering::SeqCst);
        gate
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
            r3_preopened: None,
            r3_expected: None,
            r3_callback_matches: AtomicUsize::new(0),
            r3_callback_refusals: AtomicUsize::new(0),
            precheck,
            precheck_acceptances: AtomicUsize::new(0),
            precheck_refusals: AtomicUsize::new(0),
            swaps_after_precheck: AtomicUsize::new(0),
            delegated_handle_matches: AtomicUsize::new(0),
            delegated_handle_refusals: AtomicUsize::new(0),
            d3a_wal_path: None,
            d3a_wrong_expected_wal_id: None,
            d3a_require_complete_shm: false,
            d3a_simulate_missing_shm_lock: false,
            d3a_deny_shm_lock: AtomicBool::new(false),
            d3a_wal_identity_matches: AtomicUsize::new(0),
            d3a_wal_identity_refusals: AtomicUsize::new(0),
            d3a_wal_veto_close_calls: AtomicUsize::new(0),
            d3a_method_refusals: AtomicUsize::new(0),
            d3a_shm_lock_refusals: AtomicUsize::new(0),
            d3a_shm_lock_delegations: AtomicUsize::new(0),
            d3a_shm_barrier_delegations: AtomicUsize::new(0),
            d3a_shm_unmap_delegations: AtomicUsize::new(0),
            d3a_shm_unmap_failures: AtomicUsize::new(0),
            d3a_main_close_successes: AtomicUsize::new(0),
            d3a_wal_close_successes: AtomicUsize::new(0),
            d3a_close_failures: AtomicUsize::new(0),
            r4_actual_xshm_region0: AtomicUsize::new(0),
            r4_actual_xshm_region0_size: AtomicUsize::new(0),
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


// D2 P1-0: an INTEGRATED, Windows test-only witness. It deliberately reuses
// the disposable VFS xOpen/FileId128 and wrapped xShmMap fixture above.
// Win32 same-SID mutexes coordinate cooperative peers; they cannot exclude
// an uncooperative same-SID process. No V7WriterAdmission, operator paths,
// Tauri IPC, production DACL or durable recovery proof is involved.
mod d2_p1_disposable_session {
    use super::*;
    use std::{ffi::{c_void, OsStr}, os::windows::ffi::OsStrExt, path::PathBuf};

    const WAIT_OBJECT_0: u32 = 0;
    const WAIT_ABANDONED: u32 = 0x80;
    const WAIT_TIMEOUT: u32 = 0x102;
    const ERROR_ALREADY_EXISTS: u32 = 183;

    #[link(name = "kernel32")]
    unsafe extern "system" {
        fn CreateMutexW(attributes: *mut c_void, initial_owner: i32, name: *const u16) -> *mut c_void;
        fn WaitForSingleObject(handle: *mut c_void, milliseconds: u32) -> u32;
        fn ReleaseMutex(handle: *mut c_void) -> i32;
        fn CloseHandle(handle: *mut c_void) -> i32;
        fn GetLastError() -> u32;
    }

    #[derive(Debug, Clone, Copy, PartialEq, Eq)]
    enum D2Claim { Claimed, Contended, Abandoned }

    struct D2Mutex { handle: *mut c_void, held: bool }
    impl D2Mutex {
        fn open(name: &str) -> (Self, bool) {
            let wide: Vec<u16> = OsStr::new(name).encode_wide().chain(Some(0)).collect();
            let handle = unsafe { CreateMutexW(ptr::null_mut(), 0, wide.as_ptr()) };
            assert!(!handle.is_null(), "disposable D2 mutex creation failed");
            let already_exists = unsafe { GetLastError() } == ERROR_ALREADY_EXISTS;
            (Self { handle, held: false }, already_exists)
        }
        fn try_claim(&mut self) -> D2Claim {
            match unsafe { WaitForSingleObject(self.handle, 0) } {
                WAIT_OBJECT_0 => { self.held = true; D2Claim::Claimed }
                WAIT_ABANDONED => { self.held = true; D2Claim::Abandoned }
                WAIT_TIMEOUT => D2Claim::Contended,
                other => panic!("unexpected D2 fixture mutex wait: {other}"),
            }
        }
        fn release(&mut self) {
            assert!(self.held);
            assert_ne!(unsafe { ReleaseMutex(self.handle) }, 0);
            self.held = false;
        }
    }
    impl Drop for D2Mutex {
        fn drop(&mut self) {
            if self.held { self.release(); }
            assert_ne!(unsafe { CloseHandle(self.handle) }, 0);
        }
    }

    fn name() -> String {
        static NEXT: AtomicUsize = AtomicUsize::new(0);
        let tick = SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_nanos();
        format!("Local\\Fabulaxiom-D2-Disposable-{}-{tick}-{}",
            process::id(), NEXT.fetch_add(1, Ordering::Relaxed))
    }
    fn child(mode: &str, mutex_name: &str) -> bool {
        std::process::Command::new(std::env::current_exe().unwrap())
            .arg("--exact")
            .arg("m32_sqlite_vfs_preopen_tests::d2_p1_disposable_session::m32_d2_child_probe")
            .arg("--nocapture")
            .env("FABULAXIOM_D2_CHILD_MODE", mode)
            .env("FABULAXIOM_D2_CHILD_MUTEX", mutex_name)
            .status().unwrap().success()
    }

    // The child never opens SQLite. This is a cooperative second process using
    // the same Windows user as the parent and a random Local fixture-only name.
    #[test]
    fn m32_d2_child_probe() {
        let Ok(mode) = std::env::var("FABULAXIOM_D2_CHILD_MODE") else { return };
        let mutex_name = std::env::var("FABULAXIOM_D2_CHILD_MUTEX").unwrap();
        let (mut claim, preexisting) = D2Mutex::open(&mutex_name);
        assert!(preexisting, "child must see the parent's exact live mutex");
        match mode.as_str() {
            "contended" => assert_eq!(claim.try_claim(), D2Claim::Contended),
            "free" => {
                assert_eq!(claim.try_claim(), D2Claim::Claimed);
                claim.release();
            }
            "abandon" => {
                assert_eq!(claim.try_claim(), D2Claim::Claimed);
                // Exit this disposable child only. Parent must refuse recovery.
                process::exit(0);
            }
            _ => panic!("unknown D2 child mode"),
        }
    }

    fn owned_main() -> (DisposableRoot, PathBuf, (u64, [u8; 16])) {
        let owned = DisposableRoot::new();
        let path = owned.db();
        fs::OpenOptions::new().write(true).create_new(true).open(&path).unwrap();
        let id = win_file_id_128(&fs::File::open(&path).unwrap()).unwrap();
        (owned, path, id)
    }

    fn bound_gate(
        path: PathBuf, expected: (u64, [u8; 16]),
        deny_wal: bool, deny_shm: bool, move_original_to: Option<PathBuf>,
    ) -> RegisteredFixtureVfs {
        RegisteredFixtureVfs::with_policy(true, false, deny_wal,
            Some(FileIdPrecheckPlan {
                path, expected, check_delegated_handle: true, move_original_to,
            }), Some(deny_shm))
    }

    #[test]
    fn m32_d2_p1_cooperative_owner_delegated_fileid_wal_shm_positive_is_not_admission() {
        let (_owned, path, expected) = owned_main();
        let mutex_name = name();
        let (mut mutex, existed) = D2Mutex::open(&mutex_name);
        assert!(!existed, "unexpected fixture name collision must STOP");
        assert_eq!(mutex.try_claim(), D2Claim::Claimed);
        assert!(child("contended", &mutex_name), "cooperative peer must STOP before SQLite");
        let gate = bound_gate(path.clone(), expected, false, false, None);
        let connection = Connection::open_with_flags_and_vfs(
            &path, OpenFlags::SQLITE_OPEN_READ_WRITE, gate.name()).unwrap();
        assert_eq!(sqlite_opened_file_id_128(&connection).unwrap(), expected);
        assert_eq!(gate.state.delegated_handle_matches.load(Ordering::SeqCst), 1);
        let mode: String = connection.query_row("PRAGMA journal_mode=WAL", [], |row| row.get(0)).unwrap();
        assert_eq!(mode.to_ascii_lowercase(), "wal");
        connection.execute_batch("CREATE TABLE invented_d2(id INTEGER PRIMARY KEY);").unwrap();
        assert!(gate.state.wal_delegations.load(Ordering::SeqCst) >= 1);
        assert!(gate.state.shm_map_delegations.load(Ordering::SeqCst) >= 1);
        assert_eq!(gate.state.shm_map_refusals.load(Ordering::SeqCst), 0);
        assert_eq!(gate.state.shm_named_xopens.load(Ordering::SeqCst), 0);
        assert!(connection.close().is_ok(), "explicit fixture close");
        drop(gate);
        mutex.release();
        assert!(child("free", &mutex_name), "after close only a cooperative peer may claim");
        // Even successful cooperation + delegated handle + SHM is NOT a runtime
        // cross-process EXISTING_PROFILE proof or writer admission.
    }

    #[test]
    fn m32_d2_p1_identity_swap_after_cooperative_claim_vetoes_xopen() {
        let (owned, path, expected) = owned_main();
        let displaced = owned.0.join("d2-original.sqlite3");
        let mutex_name = name();
        let (mut mutex, existed) = D2Mutex::open(&mutex_name);
        assert!(!existed);
        assert_eq!(mutex.try_claim(), D2Claim::Claimed);
        let gate = bound_gate(path.clone(), expected, false, false, Some(displaced.clone()));
        let attempted = Connection::open_with_flags_and_vfs(
            &path, OpenFlags::SQLITE_OPEN_READ_WRITE, gate.name());
        assert!(attempted.is_err(), "delegated xOpen handle mismatch must STOP");
        assert_eq!(gate.state.swaps_after_precheck.load(Ordering::SeqCst), 1);
        assert_eq!(gate.state.delegated_handle_refusals.load(Ordering::SeqCst), 1);
        assert_eq!(gate.state.shm_map_delegations.load(Ordering::SeqCst), 0);
        assert_eq!(gate.state.wal_delegations.load(Ordering::SeqCst), 0);
        assert_eq!(win_file_id_128(&fs::File::open(&displaced).unwrap()).unwrap(), expected);
        assert_ne!(win_file_id_128(&fs::File::open(&path).unwrap()).unwrap(), expected);
        drop(gate);
        mutex.release();
    }

    #[test]
    fn m32_d2_p1_wal_veto_after_bound_main_handle_stops_before_wal_open() {
        let (owned, path, expected) = owned_main();
        let (mut mutex, existed) = D2Mutex::open(&name());
        assert!(!existed);
        assert_eq!(mutex.try_claim(), D2Claim::Claimed);
        let gate = bound_gate(path.clone(), expected, true, false, None);
        let db = Connection::open_with_flags_and_vfs(
            &path, OpenFlags::SQLITE_OPEN_READ_WRITE, gate.name()).unwrap();
        assert_eq!(gate.state.delegated_handle_matches.load(Ordering::SeqCst), 1);
        let switch = db.execute_batch("PRAGMA journal_mode=WAL;");
        if switch.is_ok() {
            assert!(db.execute_batch("CREATE TABLE invented_d2(id INTEGER PRIMARY KEY);").is_err());
        }
        assert!(gate.state.wal_refusals.load(Ordering::SeqCst) >= 1);
        assert_eq!(gate.state.wal_delegations.load(Ordering::SeqCst), 0);
        assert!(!owned.0.join("new.sqlite3-wal").exists());
        drop(db);
        drop(gate);
        mutex.release();
    }

    #[test]
    fn m32_d2_p1_shm_veto_after_bound_main_handle_stops_before_mapping() {
        let (owned, path, expected) = owned_main();
        let (mut mutex, existed) = D2Mutex::open(&name());
        assert!(!existed);
        assert_eq!(mutex.try_claim(), D2Claim::Claimed);
        let gate = bound_gate(path.clone(), expected, false, true, None);
        let db = Connection::open_with_flags_and_vfs(
            &path, OpenFlags::SQLITE_OPEN_READ_WRITE, gate.name()).unwrap();
        assert_eq!(gate.state.delegated_handle_matches.load(Ordering::SeqCst), 1);
        let switch = db.execute_batch("PRAGMA journal_mode=WAL;");
        if switch.is_ok() {
            assert!(db.execute_batch("CREATE TABLE invented_d2(id INTEGER PRIMARY KEY);").is_err());
        }
        assert!(gate.state.shm_map_refusals.load(Ordering::SeqCst) >= 1);
        assert_eq!(gate.state.shm_map_delegations.load(Ordering::SeqCst), 0);
        assert!(!owned.0.join("new.sqlite3-shm").exists());
        drop(db);
        drop(gate);
        mutex.release();
    }

    #[test]
    fn m32_d2_p1_abandoned_mutex_refuses_before_sqlite_xopen() {
        let owned = DisposableRoot::new();
        let path = owned.db();
        assert!(!path.exists());
        let mutex_name = name();
        let (mut mutex, existed) = D2Mutex::open(&mutex_name);
        assert!(!existed);
        assert!(child("abandon", &mutex_name), "child abandoned its fixture-only mutex");
        assert_eq!(mutex.try_claim(), D2Claim::Abandoned);
        // WAIT_ABANDONED grants ownership to the waiter but NOT a clean-close
        // attestation. Never try an xOpen, SQL, repair or automatic reopen.
        let gate = RegisteredFixtureVfs::new(true, false);
        assert_eq!(gate.state.main_delegations.load(Ordering::SeqCst), 0);
        assert!(!path.exists(), "uncertain lifecycle never created the fixture database");
        drop(gate);
        mutex.release();
    }
}


// D3a: explicit owner-authorized Windows CI-only WAL/SHM handle custody.
// These four fixtures never access an operator SQLite database or recover a
// crashed process. They reuse a fresh DisposableRoot and real default Win32
// VFS dispatch, but no runtime V7WriterAdmission, IPC, P2 or D3b is involved.
mod d3a_p1_disposable_wal_shm {
    use super::*;

    fn fresh_main() -> (DisposableRoot, PathBuf, (u64, [u8; 16])) {
        let owned = DisposableRoot::new();
        let path = owned.db();
        fs::OpenOptions::new().write(true).create_new(true)
            .open(&path).expect("D3a test-only fresh main file");
        let expected = win_file_id_128(&fs::File::open(&path).unwrap()).unwrap();
        (owned, path, expected)
    }

    #[test]
    fn m32_d3a_wal_real_delegated_fileid_all_shm_callbacks_and_close_positive_not_admission() {
        let (_owned, path, main_id) = fresh_main();
        let gate = RegisteredFixtureVfs::with_d3a(
            path.clone(), main_id, None, false, false);
        let db = Connection::open_with_flags_and_vfs(
            &path, OpenFlags::SQLITE_OPEN_READ_WRITE, gate.name())
            .expect("D3a owned main handle must be bound before WAL");
        assert_eq!(gate.state.delegated_handle_matches.load(Ordering::SeqCst), 1);
        let mode: String = db.query_row("PRAGMA journal_mode=WAL", [], |r| r.get(0)).unwrap();
        assert_eq!(mode.to_ascii_lowercase(), "wal");
        db.execute_batch(
            "CREATE TABLE invented_d3a(id INTEGER PRIMARY KEY, note TEXT);
             INSERT INTO invented_d3a(note) VALUES ('fiction-only');
             UPDATE invented_d3a SET note='fixture' WHERE id=1;",
        ).unwrap();
        assert_eq!(db.query_row("SELECT COUNT(*) FROM invented_d3a", [],
            |r| r.get::<_, i64>(0)).unwrap(), 1);
        assert!(gate.state.d3a_wal_identity_matches.load(Ordering::SeqCst) >= 1,
            "the real delegated WAL HANDLE must match the observed owned -wal FileId128");
        assert_eq!(gate.state.d3a_wal_identity_refusals.load(Ordering::SeqCst), 0);
        assert!(gate.state.shm_map_delegations.load(Ordering::SeqCst) >= 1);
        assert!(gate.state.d3a_shm_lock_delegations.load(Ordering::SeqCst) >= 1);
        assert!(gate.state.d3a_shm_barrier_delegations.load(Ordering::SeqCst) >= 1);
        assert_eq!(gate.state.d3a_shm_lock_refusals.load(Ordering::SeqCst), 0);
        assert!(db.close().is_ok(), "D3a fixture must explicitly close SQLite");
        assert!(gate.state.d3a_shm_unmap_delegations.load(Ordering::SeqCst) >= 1);
        assert_eq!(gate.state.d3a_shm_unmap_failures.load(Ordering::SeqCst), 0);
        assert!(gate.state.d3a_wal_close_successes.load(Ordering::SeqCst) >= 1);
        assert_eq!(gate.state.d3a_main_close_successes.load(Ordering::SeqCst), 1);
        assert_eq!(gate.state.d3a_close_failures.load(Ordering::SeqCst), 0);
        // Exact fixture close proves neither durable successor attestation nor
        // any cross-process EXISTING_PROFILE authorization.
    }

    #[test]
    fn m32_d3a_wrong_expected_wal_fileid_vetoes_after_delegation_and_closes() {
        let (owned, path, main_id) = fresh_main();
        let decoy = owned.0.join("wrong-d3a-wal-id.fixture");
        fs::OpenOptions::new().write(true).create_new(true).open(&decoy).unwrap();
        let wrong_wal_id = win_file_id_128(&fs::File::open(&decoy).unwrap()).unwrap();
        let gate = RegisteredFixtureVfs::with_d3a(
            path.clone(), main_id, Some(wrong_wal_id), false, false);
        let db = Connection::open_with_flags_and_vfs(
            &path, OpenFlags::SQLITE_OPEN_READ_WRITE, gate.name())
            .expect("D3a main only may open; WAL identity is deliberately foreign");
        let attempt = db.execute_batch("PRAGMA journal_mode=WAL;");
        if attempt.is_ok() {
            assert!(db.execute_batch("CREATE TABLE never_admitted_d3a(id INTEGER);").is_err(),
                "no successful user SQL after the WAL FileId128 mismatch");
        }
        assert!(gate.state.d3a_wal_identity_refusals.load(Ordering::SeqCst) >= 1);
        assert_eq!(gate.state.d3a_wal_identity_matches.load(Ordering::SeqCst), 0);
        assert!(gate.state.d3a_wal_veto_close_calls.load(Ordering::SeqCst) >= 1,
            "after delegated xOpen veto must call the original WAL xClose");
        assert!(gate.state.wal_delegations.load(Ordering::SeqCst) >= 1);
        assert_eq!(gate.state.shm_map_delegations.load(Ordering::SeqCst), 0);
        drop(db);
        assert_eq!(win_file_id_128(&fs::File::open(&decoy).unwrap()).unwrap(),
            wrong_wal_id);
        // SQLite may have created a WAL before this veto. Never assert that
        // rejection is an atomic OS open or manually delete a live sidecar.
    }

    #[test]
    fn m32_d3a_shm_lock_veto_after_wal_handle_binding_refuses_sql() {
        let (_owned, path, main_id) = fresh_main();
        let gate = RegisteredFixtureVfs::with_d3a(
            path.clone(), main_id, None, true, false);
        let db = Connection::open_with_flags_and_vfs(
            &path, OpenFlags::SQLITE_OPEN_READ_WRITE, gate.name()).unwrap();
        let attempt = db.execute_batch("PRAGMA journal_mode=WAL;");
        if attempt.is_ok() {
            assert!(db.execute_batch("CREATE TABLE never_admitted_d3a(id INTEGER);").is_err());
        }
        assert!(gate.state.d3a_wal_identity_matches.load(Ordering::SeqCst) >= 1);
        assert!(gate.state.d3a_shm_lock_refusals.load(Ordering::SeqCst) >= 1);
        assert_eq!(gate.state.d3a_shm_lock_delegations.load(Ordering::SeqCst), 0,
            "the injected veto is before default xShmLock");
        // Permit only best-effort SQLite fixture teardown after observed STOP,
        // not any subsequent SQL, WAL repair or process-restart experiment.
        gate.state.d3a_deny_shm_lock.store(false, Ordering::SeqCst);
        drop(db);
    }

    #[test]
    fn m32_d3a_missing_shm_lock_method_refuses_at_main_xopen_without_wal() {
        let (_owned, path, main_id) = fresh_main();
        let gate = RegisteredFixtureVfs::with_d3a(
            path.clone(), main_id, None, false, true);
        let attempt = Connection::open_with_flags_and_vfs(
            &path, OpenFlags::SQLITE_OPEN_READ_WRITE, gate.name());
        assert!(attempt.is_err(), "missing xShmLock in synthetic method table must STOP");
        assert_eq!(gate.state.d3a_method_refusals.load(Ordering::SeqCst), 1);
        assert_eq!(gate.state.main_delegations.load(Ordering::SeqCst), 1);
        assert_eq!(gate.state.d3a_wal_identity_matches.load(Ordering::SeqCst), 0);
        assert_eq!(gate.state.shm_map_delegations.load(Ordering::SeqCst), 0);
        assert!(!path.with_file_name("new.sqlite3-wal").exists());
    }
}

// D3b: separately owner-authorized *Windows CI disposable fixtures* only.
// A terminated child intentionally leaves fixture-owned WAL state behind. The
// surviving process inspects only filesystem metadata and a cooperative mutex:
// it MUST NOT call SQLite on that existing database, since even opening it may
// begin a recovery or checkpoint. This is a refusal witness, NOT recovery.
mod d3b_p1_disposable_crash_refusal {
    use super::*;
    use std::{ffi::{c_void, OsStr}, os::windows::ffi::OsStrExt};

    const WAIT_OBJECT_0: u32 = 0;
    const WAIT_ABANDONED: u32 = 0x80;
    const ERROR_ALREADY_EXISTS: u32 = 183;
    const CHILD_TERMINATED: i32 = 77;
    const CHILD_ROLE: &str = "FABULAXIOM_M32_D3B_CHILD_ROLE";
    const CHILD_DB: &str = "FABULAXIOM_M32_D3B_CHILD_DB";
    const CHILD_MUTEX: &str = "FABULAXIOM_M32_D3B_CHILD_MUTEX";

    #[link(name = "kernel32")]
    unsafe extern "system" {
        fn CreateMutexW(attributes: *mut c_void, initial_owner: i32, name: *const u16) -> *mut c_void;
        fn WaitForSingleObject(handle: *mut c_void, milliseconds: u32) -> u32;
        fn ReleaseMutex(handle: *mut c_void) -> i32;
        fn CloseHandle(handle: *mut c_void) -> i32;
        fn GetLastError() -> u32;
        fn GetCurrentProcess() -> *mut c_void;
        fn TerminateProcess(handle: *mut c_void, exit_code: u32) -> i32;
    }

    struct D3bMutex { handle: *mut c_void, held: bool }
    impl D3bMutex {
        fn open(name: &str) -> (Self, bool) {
            assert!(name.starts_with("Local\\Fabulaxiom-D3b-Disposable-"));
            let wide: Vec<u16> = OsStr::new(name).encode_wide().chain(Some(0)).collect();
            let handle = unsafe { CreateMutexW(ptr::null_mut(), 0, wide.as_ptr()) };
            assert!(!handle.is_null(), "D3b fixture-only mutex CreateMutexW");
            (Self { handle, held: false }, unsafe { GetLastError() } == ERROR_ALREADY_EXISTS)
        }
        fn claim(&mut self) -> u32 {
            let outcome = unsafe { WaitForSingleObject(self.handle, 0) };
            assert!(matches!(outcome, WAIT_OBJECT_0 | WAIT_ABANDONED),
                "D3b fixture mutex must be immediately claimable after child termination: {outcome}");
            self.held = true;
            outcome
        }
        fn release(&mut self) {
            assert!(self.held);
            assert_ne!(unsafe { ReleaseMutex(self.handle) }, 0);
            self.held = false;
        }
    }
    impl Drop for D3bMutex {
        fn drop(&mut self) {
            if self.held { self.release(); }
            assert_ne!(unsafe { CloseHandle(self.handle) }, 0);
        }
    }

    #[derive(Debug, PartialEq, Eq)]
    enum RestartDecision { RecoveryRequiredNotAuthorized }

    // Never use the outcome of a volatile mutex as durable predecessor proof.
    // No synthetic marker is manufactured or installed by D3b.
    fn reject_unattested_restart(_mutex_outcome: u32) -> RestartDecision {
        RestartDecision::RecoveryRequiredNotAuthorized
    }

    fn fresh_owned() -> (DisposableRoot, PathBuf, (u64, [u8; 16])) {
        let root = DisposableRoot::new();
        let path = root.db();
        fs::OpenOptions::new().write(true).create_new(true)
            .open(&path).expect("D3b fresh CI-only database, no existing profile");
        let id = win_file_id_128(&fs::File::open(&path).unwrap()).unwrap();
        (root, path, id)
    }

    fn mutex_name() -> String {
        static NEXT: AtomicUsize = AtomicUsize::new(0);
        let tick = SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_nanos();
        format!("Local\\Fabulaxiom-D3b-Disposable-{}-{tick}-{}",
            process::id(), NEXT.fetch_add(1, Ordering::Relaxed))
    }

    fn crash_child(role: &str, path: &PathBuf, name: &str) {
        let result = process::Command::new(std::env::current_exe().unwrap())
            .arg("--exact")
            .arg("m32_sqlite_vfs_preopen_tests::d3b_p1_disposable_crash_refusal::m32_d3b_child_fixture_terminate_before_sqlite_close")
            .arg("--nocapture")
            .env(CHILD_ROLE, role)
            .env(CHILD_DB, path)
            .env(CHILD_MUTEX, name)
            .status().expect("spawn only the same CI Rust test binary");
        assert_eq!(result.code(), Some(CHILD_TERMINATED),
            "D3b child must be forcibly terminated, not normally closed: {result:?}");
    }

    fn assert_disposable_path(path: &PathBuf) {
        assert_eq!(path.file_name(), Some(OsStr::new("new.sqlite3")));
        let parent = path.parent().expect("owned fixture parent");
        assert!(parent.starts_with(std::env::temp_dir()), "CI temp root only");
        assert!(parent.file_name().unwrap().to_string_lossy()
            .starts_with("fabulaxiom-vfs-fixture-"), "reject any operator directory");
        assert!(path.is_file(), "D3b fresh main must already exist");
    }

    #[test]
    fn m32_d3b_child_fixture_terminate_before_sqlite_close() {
        let Ok(role) = std::env::var(CHILD_ROLE) else { return };
        assert!(matches!(role.as_str(), "committed" | "pending"));
        let path = PathBuf::from(std::env::var_os(CHILD_DB).unwrap());
        assert_disposable_path(&path);
        let name = std::env::var(CHILD_MUTEX).unwrap();
        let (mut mutex, _) = D3bMutex::open(&name);
        assert_eq!(mutex.claim(), WAIT_OBJECT_0);
        let actual = win_file_id_128(&fs::File::open(&path).unwrap()).unwrap();
        let gate = RegisteredFixtureVfs::with_d3a(path.clone(), actual, None, false, false);
        let db = Connection::open_with_flags_and_vfs(
            &path, OpenFlags::SQLITE_OPEN_READ_WRITE, gate.name()).unwrap();
        assert_eq!(sqlite_opened_file_id_128(&db).unwrap(), actual);
        let mode: String = db.query_row("PRAGMA journal_mode=WAL", [], |row| row.get(0)).unwrap();
        assert_eq!(mode.to_ascii_lowercase(), "wal");
        db.execute_batch("CREATE TABLE invented_d3b(id INTEGER PRIMARY KEY, note TEXT);")
            .expect("only fixture-owned synthetic SQL");
        if role == "committed" {
            db.execute_batch("INSERT INTO invented_d3b(note) VALUES ('committed-fiction');")
                .unwrap();
        } else {
            db.execute_batch("BEGIN IMMEDIATE;
                INSERT INTO invented_d3b(note) VALUES ('never-committed-fiction');")
                .unwrap();
        }
        assert!(path.with_file_name("new.sqlite3-wal").exists());
        assert!(gate.state.d3a_wal_identity_matches.load(Ordering::SeqCst) >= 1);
        // Explicit Windows process termination skips Rust destructors, SQLite
        // close, SHM unmap, mutex release and last-close checkpoint. Never use
        // process::abort (which could invoke crash dialog/reporting on CI).
        let terminated = unsafe { TerminateProcess(GetCurrentProcess(), CHILD_TERMINATED as u32) };
        panic!("D3b TerminateProcess unexpectedly returned {terminated}");
    }

    fn inspect_only_owned_files(path: &PathBuf, expected: (u64, [u8; 16])) {
        assert_disposable_path(path);
        assert_eq!(win_file_id_128(&fs::File::open(path).unwrap()).unwrap(), expected);
        let wal = path.with_file_name("new.sqlite3-wal");
        assert!(fs::metadata(&wal).unwrap().len() > 0,
            "the fixture's post-crash WAL is a persistent state witness");
        // No Connection::open, PRAGMA, checkpoint, WAL delete, rename or repair.
        // A real -shm path may be present; its presence is not authenticated.
    }

    #[test]
    fn m32_d3b_committed_wal_abandoned_mutex_refuses_unattested_reopen() {
        let (_root, path, main_id) = fresh_owned();
        let name = mutex_name();
        let (mut parent, existed) = D3bMutex::open(&name);
        assert!(!existed);
        // Retained parent handle makes the child's abandoned mutex observable.
        crash_child("committed", &path, &name);
        assert_eq!(parent.claim(), WAIT_ABANDONED);
        inspect_only_owned_files(&path, main_id);
        assert_eq!(reject_unattested_restart(WAIT_ABANDONED),
            RestartDecision::RecoveryRequiredNotAuthorized);
        parent.release();
    }

    #[test]
    fn m32_d3b_pending_wal_vanished_mutex_still_refuses_unattested_reopen() {
        let (_root, path, main_id) = fresh_owned();
        let name = mutex_name();
        // The child owns the only named mutex handle. After its termination,
        // the parent creates a NEW free mutex -- never a clean-close witness.
        crash_child("pending", &path, &name);
        let (mut successor, existed) = D3bMutex::open(&name);
        assert!(!existed, "last handle closed, named mutex must be destroyed");
        assert_eq!(successor.claim(), WAIT_OBJECT_0);
        inspect_only_owned_files(&path, main_id);
        assert_eq!(reject_unattested_restart(WAIT_OBJECT_0),
            RestartDecision::RecoveryRequiredNotAuthorized);
        successor.release();
    }

    #[test]
    fn m32_d3b_busy_close_does_not_attest_restart_even_after_final_close() {
        let (_root, path, main_id) = fresh_owned();
        let name = mutex_name();
        let (mut mutex, existed) = D3bMutex::open(&name);
        assert!(!existed);
        assert_eq!(mutex.claim(), WAIT_OBJECT_0);
        let gate = RegisteredFixtureVfs::with_d3a(path.clone(), main_id, None, false, false);
        let db = Connection::open_with_flags_and_vfs(
            &path, OpenFlags::SQLITE_OPEN_READ_WRITE, gate.name()).unwrap();
        db.execute_batch("PRAGMA journal_mode=WAL;
            CREATE TABLE invented_d3b_busy(id INTEGER PRIMARY KEY);")
            .unwrap();
        let mut statement = db.prepare("SELECT * FROM invented_d3b_busy").unwrap();
        assert!(statement.exists([]).is_ok());
        // sqlite3_close, unlike sqlite3_close_v2, returns BUSY when statement
        // handles remain live. A failed close MUST NOT release the claim.
        let first_close = unsafe { ffi::sqlite3_close(db.handle()) };
        assert_eq!(first_close, ffi::SQLITE_BUSY);
        assert_eq!(gate.state.d3a_main_close_successes.load(Ordering::SeqCst), 0);
        assert_eq!(reject_unattested_restart(WAIT_OBJECT_0),
            RestartDecision::RecoveryRequiredNotAuthorized);
        drop(statement);
        assert!(db.close().is_ok(), "fixture cleanup only, not durable attestation");
        assert_eq!(gate.state.d3a_main_close_successes.load(Ordering::SeqCst), 1);
        mutex.release();
        // Even this completed local close cannot authenticate another process.
    }
}


// R4 / P1 decision probe, Windows CI-only on a NEW disposable SQLite file.
// SQLite documents that locking_mode=EXCLUSIVE before the FIRST WAL access
// suppresses xShmMap/xShmLock/xShmBarrier/xShmUnmap. The distinct "too late"
// control retains ordinary WAL shared-memory behavior. No runtime writer,
// existing-profile open, restart, marker, or VFS-handle handoff is implied.
mod r4_p1_exclusive_wal_disposable {
    use super::*;

    fn fresh_fixture(
        exclusive_before_wal: bool, veto_all_shm_map: bool,
    ) -> (DisposableRoot, RegisteredFixtureVfs, Connection) {
        let root = DisposableRoot::new();
        let path = root.db();
        fs::OpenOptions::new().write(true).create_new(true)
            .open(&path).expect("only a new, CI-owned main is created");
        let id = win_file_id_128(&fs::File::open(&path).unwrap()).unwrap();
        let gate = if veto_all_shm_map {
            RegisteredFixtureVfs::with_shm_policy(true)
        } else {
            RegisteredFixtureVfs::with_d3a(path.clone(), id, None, false, false)
        };
        // Exactly one new reviewed SQLite opening site in this helper;
        // never turn it into a runtime opener or use a historical profile.
        let db = Connection::open_with_flags_and_vfs(
            &path, OpenFlags::SQLITE_OPEN_READ_WRITE, gate.name()
        ).expect("test-owned SQLite main, no CREATE flag");
        if exclusive_before_wal {
            let lock: String = db.query_row(
                "PRAGMA locking_mode=EXCLUSIVE", [], |row| row.get(0)
            ).unwrap();
            assert_eq!(lock.to_ascii_lowercase(), "exclusive");
        }
        let mode: String = db.query_row(
            "PRAGMA journal_mode=WAL", [], |row| row.get(0)
        ).expect("fresh test-owned WAL");
        assert_eq!(mode.to_ascii_lowercase(), "wal");
        db.execute_batch(
            "CREATE TABLE invented_r4(id INTEGER PRIMARY KEY, content TEXT);
             INSERT INTO invented_r4(content) VALUES ('fictional');"
        ).expect("SQLite writes only into this newly created CI fixture");
        assert_eq!(db.query_row("SELECT COUNT(*) FROM invented_r4", [],
            |row| row.get::<_, i64>(0)).unwrap(), 1);
        if !exclusive_before_wal {
            let lock: String = db.query_row(
                "PRAGMA locking_mode=EXCLUSIVE", [], |row| row.get(0)
            ).unwrap();
            assert_eq!(lock.to_ascii_lowercase(), "exclusive");
        }
        (root, gate, db)
    }

    #[test]
    fn m32_r4_exclusive_before_wal_avoids_every_wrapped_shm_callback() {
        let (root, gate, db) = fresh_fixture(true, false);
        assert!(root.db().with_file_name("new.sqlite3-wal").exists());
        assert!(!root.db().with_file_name("new.sqlite3-shm").exists());
        assert!(gate.state.d3a_wal_identity_matches.load(Ordering::SeqCst) >= 1);
        assert_eq!(gate.state.shm_map_delegations.load(Ordering::SeqCst), 0);
        assert_eq!(gate.state.d3a_shm_lock_delegations.load(Ordering::SeqCst), 0);
        assert_eq!(gate.state.d3a_shm_barrier_delegations.load(Ordering::SeqCst), 0);
        assert_eq!(gate.state.d3a_shm_unmap_delegations.load(Ordering::SeqCst), 0);
        assert!(db.close().is_ok(), "explicit clean close only, NOT R7 restart");
        assert_eq!(gate.state.d3a_main_close_successes.load(Ordering::SeqCst), 1);
        assert_eq!(gate.state.d3a_close_failures.load(Ordering::SeqCst), 0);
        // Closing the test-only WAL session is not durable successor admission.
    }

    #[test]
    fn m32_r4_exclusive_before_wal_succeeds_with_shm_map_veto_armed() {
        let (root, gate, db) = fresh_fixture(true, true);
        assert!(root.db().with_file_name("new.sqlite3-wal").exists());
        assert!(!root.db().with_file_name("new.sqlite3-shm").exists());
        assert_eq!(gate.state.shm_map_refusals.load(Ordering::SeqCst), 0);
        assert_eq!(gate.state.shm_map_delegations.load(Ordering::SeqCst), 0);
        assert!(db.close().is_ok(), "test-only SQLite close");
    }

    #[test]
    fn m32_r4_exclusive_after_wal_does_not_undo_existing_shm_mapping() {
        let (root, gate, db) = fresh_fixture(false, false);
        assert!(root.db().with_file_name("new.sqlite3-wal").exists());
        assert!(root.db().with_file_name("new.sqlite3-shm").exists(),
            "normal WAL first must create the ordinary shared-memory index");
        assert!(gate.state.shm_map_delegations.load(Ordering::SeqCst) >= 1);
        assert!(gate.state.d3a_shm_lock_delegations.load(Ordering::SeqCst) >= 1);
        assert!(gate.state.d3a_shm_barrier_delegations.load(Ordering::SeqCst) >= 1);
        assert!(db.close().is_ok(), "no restart, no recovery");
        assert!(gate.state.d3a_shm_unmap_delegations.load(Ordering::SeqCst) >= 1);
    }

    // A second SQLite connection is not a second authorized P1 reader merely
    // because it runs under the same Windows SID or process. Never route UI
    // consultation through an independently opened SQLite connection while
    // a single owner holds EXCLUSIVE WAL.
    #[test]
    fn m32_r4_exclusive_owner_refuses_second_sqlite_reader_without_ipc() {
        let (root, gate, owner) = fresh_fixture(true, false);
        let reader = Connection::open_with_flags_and_vfs(
            &root.db(), OpenFlags::SQLITE_OPEN_READ_ONLY, gate.name()
        ).expect("test-only second connection constructor, NOT a P1 reader");
        reader.busy_timeout(std::time::Duration::from_millis(100)).unwrap();
        let failure = reader.query_row(
            "SELECT COUNT(*) FROM invented_r4", [],
            |row| row.get::<_, i64>(0)
        ).expect_err("EXCLUSIVE owner must prevent a separately opened reader");
        match failure {
            rusqlite::Error::SqliteFailure(native, _) =>
                assert_eq!(native.code, rusqlite::ErrorCode::DatabaseBusy),
            other => panic!("second reader must fail with SQLite BUSY: {other:?}"),
        }
        assert_eq!(owner.query_row("SELECT COUNT(*) FROM invented_r4", [],
            |row| row.get::<_, i64>(0)).unwrap(), 1,
            "the single owner remains the only admitted reader");
        assert_eq!(gate.state.shm_map_delegations.load(Ordering::SeqCst), 0);
        drop(reader);
        assert!(owner.close().is_ok(), "clean test-only close, not R7 restart proof");
    }

    // The initial raw-PRAGMA test FAILED at exact-head Windows CI
    // #40948171560: SQLite returned "normal" even though the fixture entered
    // WAL under EXCLUSIVE, while its second-reader refusal test passed.
    // Do not make file custody depend on a PRAGMA response. Model typed P1
    // requests with an explicit fail-closed owner boundary instead.
    #[derive(Debug, Clone, Copy)]
    enum R4OwnerRequest { ReadInventedCount, DowngradeLockingToNormal }

    fn r4_fixture_owner_execute(
        db: &Connection, request: R4OwnerRequest,
    ) -> Result<i64, &'static str> {
        match request {
            R4OwnerRequest::ReadInventedCount =>
                db.query_row("SELECT COUNT(*) FROM invented_r4", [],
                    |row| row.get::<_, i64>(0))
                    .map_err(|_| "STOP: fictional owner read failed"),
            R4OwnerRequest::DowngradeLockingToNormal =>
                Err("STOP: P1 EXCLUSIVE WAL locking downgrade not an allowed owner operation"),
        }
    }

    #[test]
    fn m32_r4_exclusive_wal_owner_policy_refuses_normal_downgrade() {
        let (_root, gate, owner) = fresh_fixture(true, false);
        let before: String = owner.query_row(
            "PRAGMA locking_mode", [], |row| row.get(0)
        ).unwrap();
        assert_eq!(before.to_ascii_lowercase(), "exclusive");
        assert_eq!(r4_fixture_owner_execute(&owner, R4OwnerRequest::ReadInventedCount),
            Ok(1));
        assert!(r4_fixture_owner_execute(
            &owner, R4OwnerRequest::DowngradeLockingToNormal
        ).unwrap_err().starts_with("STOP:"));
        // The rejected operation never invokes the unsafe SQLite PRAGMA.
        // This is NOT a production dispatcher or a proof of SQLite internals.
        let after: String = owner.query_row(
            "PRAGMA locking_mode", [], |row| row.get(0)
        ).unwrap();
        assert_eq!(after.to_ascii_lowercase(), "exclusive");
        assert_eq!(r4_fixture_owner_execute(&owner, R4OwnerRequest::ReadInventedCount),
            Ok(1));
        assert_eq!(gate.state.shm_map_delegations.load(Ordering::SeqCst), 0);
        assert!(owner.close().is_ok(), "test-only close; no reopening or recovery");
    }

}


// R3 preopened HANDLE xOpen veto: separate from the historical 26 VFS and
// five R4 witnesses. Both tests are Windows CI-only fresh %TEMP% fixtures.
fn r3_sqlite_callback_probe(path: &std::path::Path, gate: &RegisteredFixtureVfs) {
    // Exactly one new reviewed SQLite opener site; our xOpen always vetoes.
    let result = Connection::open_with_flags_and_vfs(
        path, OpenFlags::SQLITE_OPEN_READ_WRITE, gate.name()
    );
    assert!(result.is_err(), "R3 has no sqlite3_file io_methods adapter; STOP");
}

#[test]
fn m32_r3_sqlite_xopen_reopens_preheld_handle_without_path_delegation() {
    let owned = DisposableRoot::new();
    let path = owned.db();
    let held = fs::OpenOptions::new().read(true).write(true).create_new(true)
        .open(&path).expect("new disposable file only");
    let expected = win_file_id_128(&held).unwrap();
    let gate = RegisteredFixtureVfs::with_preopened_r3(held);
    r3_sqlite_callback_probe(&path, &gate);
    assert_eq!(gate.state.r3_callback_matches.load(Ordering::SeqCst), 1);
    assert_eq!(gate.state.r3_callback_refusals.load(Ordering::SeqCst), 0);
    assert_eq!(gate.state.main_delegations.load(Ordering::SeqCst), 0);
    assert_eq!(win_file_id_128(&fs::File::open(&path).unwrap()).unwrap(), expected);
    assert_eq!(fs::metadata(&path).unwrap().len(), 0);
    assert!(!path.with_file_name("new.sqlite3-wal").exists());
    assert!(!path.with_file_name("new.sqlite3-shm").exists());
}

#[test]
fn m32_r3_sqlite_xopen_held_handle_survives_replaced_name_but_vetoes() {
    use std::os::windows::fs::OpenOptionsExt;
    let owned = DisposableRoot::new();
    let path = owned.db();
    let displaced = owned.0.join("displaced-r3-original.sqlite3");
    let held = fs::OpenOptions::new().read(true).write(true).create_new(true)
        .share_mode(1 | 2 | 4).open(&path).expect("new disposable original");
    let original = win_file_id_128(&held).unwrap();
    fs::rename(&path, &displaced).expect("owned controlled name replacement");
    let replacement = fs::OpenOptions::new().read(true).write(true).create_new(true)
        .share_mode(1 | 2 | 4).open(&path).expect("different disposable replacement");
    let different = win_file_id_128(&replacement).unwrap();
    assert_ne!(original, different);
    let gate = RegisteredFixtureVfs::with_preopened_r3(held);
    r3_sqlite_callback_probe(&path, &gate);
    assert_eq!(gate.state.r3_callback_matches.load(Ordering::SeqCst), 1,
        "xOpen must clone the held original object, not replacement name");
    assert_eq!(gate.state.main_delegations.load(Ordering::SeqCst), 0);
    assert_eq!(win_file_id_128(&fs::File::open(&displaced).unwrap()).unwrap(), original);
    assert_eq!(win_file_id_128(&fs::File::open(&path).unwrap()).unwrap(), different);
    assert_eq!(fs::metadata(&path).unwrap().len(), 0);
    assert!(!path.with_file_name("new.sqlite3-wal").exists());
    assert!(!path.with_file_name("new.sqlite3-shm").exists());
    drop(replacement);
}


// R4 / D3a live -shm FileId128: NEW standalone test module deliberately
// OUTSIDE the immutable 26-test D2/D3ab historical fixture section and the
// existing five R4 P1 witnesses. Windows CI only, disposable %TEMP% namespace.
mod r4_d3a_live_shm_fileid_disposable {
    use super::*;

    #[test]
    fn m32_r4_d3a_shm_fileid_stable_during_live_wrapped_wal_disposable() {
        use std::os::windows::fs::OpenOptionsExt;
        // The default Win32 xShm* implementation remains the source of the
        // mapped WAL index. This independently observes the live -shm file
        // through two owned Windows handles; it does not pin xShmMap's HANDLE
        // or authenticate any entire main/WAL/SHM open as one atomic action.
        let owned = DisposableRoot::new();
        let path = owned.db();
        fs::OpenOptions::new().write(true).create_new(true).open(&path)
            .expect("new, CI-owned main only");
        let main_id = win_file_id_128(&fs::File::open(&path).unwrap()).unwrap();
        let wal = path.with_file_name("new.sqlite3-wal");
        let shm = path.with_file_name("new.sqlite3-shm");
        let gate = RegisteredFixtureVfs::with_d3a(
            path.clone(), main_id, None, false, false);
        let db = Connection::open_with_flags_and_vfs(
            &path, OpenFlags::SQLITE_OPEN_READ_WRITE, gate.name())
            .expect("new fixture only, never existing operator database");
        assert_eq!(sqlite_opened_file_id_128(&db).unwrap(), main_id);
        let mode: String = db.query_row("PRAGMA journal_mode=WAL", [], |r| r.get(0)).unwrap();
        assert_eq!(mode.to_ascii_lowercase(), "wal");
        db.execute_batch(
            "CREATE TABLE invented_r4_shm(value INTEGER NOT NULL);
             INSERT INTO invented_r4_shm(value) VALUES (1);"
        ).unwrap();
        assert!(fs::metadata(&wal).unwrap().len() > 0);
        assert!(fs::metadata(&shm).unwrap().len() > 0);
        const SHARE_READ_WRITE: u32 = 1 | 2;
        let wal_held = fs::OpenOptions::new().read(true).share_mode(SHARE_READ_WRITE)
            .open(&wal).expect("fixture's live WAL sidecar only");
        let shm_held = fs::OpenOptions::new().read(true).share_mode(SHARE_READ_WRITE)
            .open(&shm).expect("fixture's live SHM sidecar only");
        let wal_id = win_file_id_128(&wal_held).unwrap();
        let shm_id = win_file_id_128(&shm_held).unwrap();
        assert_ne!(main_id, wal_id);
        assert_ne!(main_id, shm_id);
        assert_ne!(wal_id, shm_id);
        db.execute("INSERT INTO invented_r4_shm(value) VALUES (2)", []).unwrap();
        assert_eq!(db.query_row("SELECT COUNT(*) FROM invented_r4_shm", [],
            |r| r.get::<_, i64>(0)).unwrap(), 2);
        assert_eq!(win_file_id_128(&wal_held).unwrap(), wal_id);
        assert_eq!(win_file_id_128(&shm_held).unwrap(), shm_id);
        // The second name-based observation is explicitly NON-ATOMIC;
        // only each held handle's identity is stable by construction.
        assert_eq!(win_file_id_128(&fs::OpenOptions::new().read(true)
            .share_mode(SHARE_READ_WRITE).open(&wal).unwrap()).unwrap(), wal_id);
        assert_eq!(win_file_id_128(&fs::OpenOptions::new().read(true)
            .share_mode(SHARE_READ_WRITE).open(&shm).unwrap()).unwrap(), shm_id);
        assert!(gate.state.d3a_wal_identity_matches.load(Ordering::SeqCst) >= 1);
        assert_eq!(gate.state.d3a_wal_identity_refusals.load(Ordering::SeqCst), 0);
        assert!(gate.state.shm_map_delegations.load(Ordering::SeqCst) >= 1);
        assert!(gate.state.d3a_shm_lock_delegations.load(Ordering::SeqCst) >= 1);
        assert!(gate.state.d3a_shm_barrier_delegations.load(Ordering::SeqCst) >= 1);
        // Release our extra sidecar handles before SQLite's last-close
        // checkpoint/delete lifecycle; this is still a disposable fixture.
        drop(shm_held);
        drop(wal_held);
        assert!(db.close().is_ok());
        assert!(gate.state.d3a_shm_unmap_delegations.load(Ordering::SeqCst) >= 1);
        assert_eq!(gate.state.d3a_shm_unmap_failures.load(Ordering::SeqCst), 0);
        assert!(gate.state.d3a_wal_close_successes.load(Ordering::SeqCst) >= 1);
        assert_eq!(gate.state.d3a_main_close_successes.load(Ordering::SeqCst), 1);
        // NO atomic custody of three handles; NO writer production admission.
    }

}


// R4, AFTER the historical D3a and R4 fixture groups. This compares bytes
// returned by the ACTUAL stock SQLite xShmMap callback through our test-only
// wrapper with a separately held FileId128-verified SHM file. It DOES NOT
// authenticate the opaque OS HANDLE that winShmNode used for its mapping.
mod r4_actual_xshm_region0_crosscheck_disposable {
    use super::*;
    use std::os::windows::{fs::{FileExt, OpenOptionsExt}, io::AsRawHandle};

    #[test]
    fn r4_actual_xshm_region0_matches_live_held_shm_file_not_native_handle_proof() {
        let owned = DisposableRoot::new();
        let path = owned.db();
        fs::OpenOptions::new().write(true).create_new(true)
            .open(&path).expect("CREATE_NEW in new fixture %TEMP% only");
        let main_id = win_file_id_128(&fs::File::open(&path).unwrap()).unwrap();
        let gate = RegisteredFixtureVfs::with_d3a(
            path.clone(), main_id, None, false, false);
        // Exactly one new reviewed SQLite opening site; a new disposable path.
        let db = Connection::open_with_flags_and_vfs(
            &path, OpenFlags::SQLITE_OPEN_READ_WRITE, gate.name()
        ).expect("test-only SQLite handle");
        let mode: String = db.query_row("PRAGMA journal_mode=WAL", [],
            |row| row.get(0)).unwrap();
        assert_eq!(mode.to_ascii_lowercase(), "wal");
        db.execute_batch(
            "CREATE TABLE invented_r4_crosscheck(v INTEGER NOT NULL);
             INSERT INTO invented_r4_crosscheck(v) VALUES(1);
             INSERT INTO invented_r4_crosscheck(v) VALUES(2);"
        ).unwrap();
        assert_eq!(db.query_row("SELECT COUNT(*) FROM invented_r4_crosscheck", [],
            |row| row.get::<_, i64>(0)).unwrap(), 2);

        let address = gate.state.r4_actual_xshm_region0.load(Ordering::SeqCst);
        let size = gate.state.r4_actual_xshm_region0_size.load(Ordering::SeqCst);
        assert_ne!(address, 0, "SQLite returned a real region-0 xShmMap address");
        assert!(size >= 136, "mapped WAL-index header must fit region zero");
        assert!(gate.state.shm_map_delegations.load(Ordering::SeqCst) >= 1);
        assert!(gate.state.d3a_shm_lock_delegations.load(Ordering::SeqCst) >= 1);
        assert!(gate.state.d3a_shm_barrier_delegations.load(Ordering::SeqCst) >= 1);

        let shm = path.with_file_name("new.sqlite3-shm");
        let held = fs::OpenOptions::new().read(true).share_mode(1|2|4)
            .open(&shm).expect("only SQLite-created live SHM in new fixture");
        let held_id_before = win_file_id_128(&held).unwrap();
        assert_ne!(main_id, held_id_before);
        // No further SQLite operations until this live view has been read.
        // SQLite owns this pointer; reading it after db.close would be UAF.
        let mut actual_callback_region = [0_u8; 136];
        unsafe {
            ptr::copy_nonoverlapping(address as *const u8,
                actual_callback_region.as_mut_ptr(), actual_callback_region.len());
        }
        let mut held_file_bytes = [0_u8; 136];
        assert_eq!(held.seek_read(&mut held_file_bytes, 0).unwrap(), 136);
        assert_eq!(actual_callback_region, held_file_bytes,
            "real xShmMap region-0 bytes must match same live named file bytes");
        assert_eq!(u32::from_ne_bytes(actual_callback_region[0..4].try_into().unwrap()),
            3_007_000);
        assert_eq!(u32::from_ne_bytes(actual_callback_region[48..52].try_into().unwrap()),
            3_007_000);
        assert_eq!(actual_callback_region[12], 1);
        assert_eq!(win_file_id_128(&held).unwrap(), held_id_before);
        drop(held);
        assert!(db.close().is_ok(), "unmap and close test-only SQLite before cleanup");
        assert!(gate.state.d3a_shm_unmap_delegations.load(Ordering::SeqCst) >= 1);
        assert_eq!(gate.state.d3a_shm_unmap_failures.load(Ordering::SeqCst), 0);
        assert_eq!(gate.state.d3a_close_failures.load(Ordering::SeqCst), 0);
        // Never dereference the region pointer after close; never production.
    }
}
