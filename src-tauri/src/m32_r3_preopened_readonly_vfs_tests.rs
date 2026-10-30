//! R3 test-only Windows read-only sqlite3_file backed by a pre-held Win32 HANDLE.
//! Every fixture is freshly created under %TEMP%; no operator file, runtime
//! VFS registration, writer admission, WAL, or production locking semantics.
//! xLock/xCheckReservedLock deliberately assume ONE sealed fixture reader:
//! they are NOT a general cross-process SQLite locking implementation.

use rusqlite::{ffi, Connection, OpenFlags};
use std::{
    ffi::{c_int, c_void, CString},
    fs::{self, File, OpenOptions},
    os::windows::{fs::{OpenOptionsExt, FileExt}, io::{AsRawHandle, FromRawHandle}},
    path::{Path, PathBuf},
    process, ptr,
    sync::atomic::{AtomicUsize, Ordering},
    time::{SystemTime, UNIX_EPOCH},
};

type Identity = (u64, [u8; 16]);
const SHARE_ALL: u32 = 1 | 2 | 4;
const READ_ACCESS: u32 = 0x8000_0000;

#[repr(C)]
struct WinFileIdInfo { volume: u64, id: [u8; 16] }

#[link(name = "kernel32")]
unsafe extern "system" {
    fn GetFileInformationByHandleEx(handle: *mut c_void, class: i32,
        data: *mut c_void, size: u32) -> i32;
    fn ReOpenFile(original: *mut c_void, access: u32, share: u32, flags: u32) -> *mut c_void;
}

fn id_of(file: &File) -> Option<Identity> {
    let mut info = std::mem::MaybeUninit::<WinFileIdInfo>::uninit();
    let status = unsafe {
        GetFileInformationByHandleEx(file.as_raw_handle().cast(), 0x12,
            info.as_mut_ptr().cast(), std::mem::size_of::<WinFileIdInfo>() as u32)
    };
    if status == 0 { return None; }
    let info = unsafe { info.assume_init() };
    Some((info.volume, info.id))
}

fn reopen_readonly(held: &File) -> Option<File> {
    let handle = unsafe { ReOpenFile(held.as_raw_handle().cast(), READ_ACCESS, SHARE_ALL, 0) };
    if handle.is_null() || handle as isize == -1 { return None; }
    Some(unsafe { File::from_raw_handle(handle.cast()) })
}

// sqlite3_file is the first member, as required by SQLite's VFS ABI.
#[repr(C)]
struct ReadOnlySqliteFile {
    base: ffi::sqlite3_file,
    file: *mut File, // owned Box<File>, dropped exactly once by xClose
}

unsafe extern "C" fn ro_close(file: *mut ffi::sqlite3_file) -> c_int {
    let opened = unsafe { &mut *(file as *mut ReadOnlySqliteFile) };
    let owned = std::mem::replace(&mut opened.file, ptr::null_mut());
    opened.base.pMethods = ptr::null();
    if !owned.is_null() { unsafe { drop(Box::from_raw(owned)) }; }
    ffi::SQLITE_OK
}

unsafe extern "C" fn ro_read(
    file: *mut ffi::sqlite3_file, buf: *mut c_void, size: c_int, offset: ffi::sqlite3_int64,
) -> c_int {
    if file.is_null() || buf.is_null() || size < 0 || offset < 0 { return ffi::SQLITE_IOERR_READ; }
    if size == 0 { return ffi::SQLITE_OK; }
    let opened = unsafe { &*(file as *const ReadOnlySqliteFile) };
    if opened.file.is_null() { return ffi::SQLITE_IOERR_READ; }
    let data = unsafe { std::slice::from_raw_parts_mut(buf.cast::<u8>(), size as usize) };
    // SQLite requires zero-fill for the unread suffix on a short read.
    data.fill(0);
    let native = unsafe { &*opened.file };
    match native.seek_read(data, offset as u64) {
        Ok(n) if n == size as usize => ffi::SQLITE_OK,
        Ok(_) => ffi::SQLITE_IOERR_SHORT_READ,
        Err(_) => ffi::SQLITE_IOERR_READ,
    }
}

unsafe extern "C" fn ro_write(_: *mut ffi::sqlite3_file, _: *const c_void,
    _: c_int, _: ffi::sqlite3_int64) -> c_int { ffi::SQLITE_READONLY }
unsafe extern "C" fn ro_truncate(_: *mut ffi::sqlite3_file,
    _: ffi::sqlite3_int64) -> c_int { ffi::SQLITE_READONLY }
unsafe extern "C" fn ro_sync(_: *mut ffi::sqlite3_file, _: c_int) -> c_int {
    // No writes can occur through this adapter. Not a durability proof.
    ffi::SQLITE_OK
}
unsafe extern "C" fn ro_file_size(
    file: *mut ffi::sqlite3_file, out: *mut ffi::sqlite3_int64,
) -> c_int {
    if out.is_null() || file.is_null() { return ffi::SQLITE_IOERR_FSTAT; }
    let opened = unsafe { &*(file as *const ReadOnlySqliteFile) };
    if opened.file.is_null() { return ffi::SQLITE_IOERR_FSTAT; }
    let native = unsafe { &*opened.file };
    match native.metadata() {
        Ok(meta) if meta.len() <= i64::MAX as u64 => {
            unsafe { *out = meta.len() as ffi::sqlite3_int64 };
            ffi::SQLITE_OK
        }
        _ => ffi::SQLITE_IOERR_FSTAT,
    }
}

// TEST-ONLY single-reader lock convention. No Win32 file-range locks or
// interprocess safety is claimed. Production R4 remains STOP.
unsafe extern "C" fn ro_lock(_: *mut ffi::sqlite3_file, lock: c_int) -> c_int {
    if lock == ffi::SQLITE_LOCK_SHARED { ffi::SQLITE_OK } else { ffi::SQLITE_BUSY }
}
unsafe extern "C" fn ro_unlock(_: *mut ffi::sqlite3_file, lock: c_int) -> c_int {
    if lock == ffi::SQLITE_LOCK_NONE || lock == ffi::SQLITE_LOCK_SHARED {
        ffi::SQLITE_OK
    } else { ffi::SQLITE_IOERR_UNLOCK }
}
unsafe extern "C" fn ro_reserved(_: *mut ffi::sqlite3_file, out: *mut c_int) -> c_int {
    if out.is_null() { return ffi::SQLITE_IOERR_CHECKRESERVEDLOCK; }
    unsafe { *out = 0 };
    ffi::SQLITE_OK
}
unsafe extern "C" fn ro_control(_: *mut ffi::sqlite3_file, _: c_int,
    _: *mut c_void) -> c_int { ffi::SQLITE_NOTFOUND }
unsafe extern "C" fn ro_sector(_: *mut ffi::sqlite3_file) -> c_int { 4096 }
unsafe extern "C" fn ro_device(_: *mut ffi::sqlite3_file) -> c_int { 0 }

static READONLY_IO: ffi::sqlite3_io_methods = ffi::sqlite3_io_methods {
    iVersion: 1,
    xClose: Some(ro_close),
    xRead: Some(ro_read),
    xWrite: Some(ro_write),
    xTruncate: Some(ro_truncate),
    xSync: Some(ro_sync),
    xFileSize: Some(ro_file_size),
    xLock: Some(ro_lock),
    xUnlock: Some(ro_unlock),
    xCheckReservedLock: Some(ro_reserved),
    xFileControl: Some(ro_control),
    xSectorSize: Some(ro_sector),
    xDeviceCharacteristics: Some(ro_device),
    xShmMap: None,
    xShmLock: None,
    xShmBarrier: None,
    xShmUnmap: None,
    xFetch: None,
    xUnfetch: None,
};

#[repr(C)]
struct ReadOnlyVfs {
    dispatch: ffi::sqlite3_vfs,
    held: File,
    expected: Identity,
    accepted: AtomicUsize,
    refused: AtomicUsize,
    // No default-VFS xOpen delegation exists in this adapter.
}

unsafe extern "C" fn ro_xopen(
    vfs: *mut ffi::sqlite3_vfs, name: ffi::sqlite3_filename,
    file: *mut ffi::sqlite3_file, flags: c_int, out_flags: *mut c_int,
) -> c_int {
    unsafe { (*file).pMethods = ptr::null() };
    let gate = unsafe { &*(vfs as *const ReadOnlyVfs) };
    if name.is_null() || flags & ffi::SQLITE_OPEN_MAIN_DB == 0
        || flags & ffi::SQLITE_OPEN_READONLY == 0
        || flags & (ffi::SQLITE_OPEN_READWRITE | ffi::SQLITE_OPEN_CREATE) != 0
    {
        gate.refused.fetch_add(1, Ordering::SeqCst);
        return ffi::SQLITE_CANTOPEN;
    }
    let Some(native) = reopen_readonly(&gate.held) else {
        gate.refused.fetch_add(1, Ordering::SeqCst);
        return ffi::SQLITE_CANTOPEN;
    };
    if id_of(&native) != Some(gate.expected) {
        gate.refused.fetch_add(1, Ordering::SeqCst);
        return ffi::SQLITE_CANTOPEN;
    }
    // This successful xOpen owns the cloned File via its sqlite3_file.
    // The original held File stays with the registered test-only VFS.
    unsafe {
        ptr::write(file.cast::<ReadOnlySqliteFile>(), ReadOnlySqliteFile {
            base: ffi::sqlite3_file { pMethods: &READONLY_IO },
            file: Box::into_raw(Box::new(native)),
        });
        if !out_flags.is_null() { *out_flags = ffi::SQLITE_OPEN_READONLY; }
    }
    gate.accepted.fetch_add(1, Ordering::SeqCst);
    ffi::SQLITE_OK
}

struct RegisteredReadOnlyVfs {
    state: Box<ReadOnlyVfs>,
    _name: CString,
}
impl RegisteredReadOnlyVfs {
    fn new(held: File) -> Self {
        static NEXT: AtomicUsize = AtomicUsize::new(0);
        let expected = id_of(&held).expect("new CI-owned FileIdInfo");
        let name = CString::new(format!("fabulaxiom-r3-readonly-test-{}-{}",
            process::id(), NEXT.fetch_add(1, Ordering::Relaxed))).unwrap();
        let default = unsafe { ffi::sqlite3_vfs_find(ptr::null()) };
        assert!(!default.is_null());
        let mut state = Box::new(ReadOnlyVfs {
            dispatch: unsafe { ptr::read(default) },
            held,
            expected,
            accepted: AtomicUsize::new(0),
            refused: AtomicUsize::new(0),
        });
        state.dispatch.pNext = ptr::null_mut();
        state.dispatch.zName = name.as_ptr();
        state.dispatch.szOsFile = state.dispatch.szOsFile.max(
            std::mem::size_of::<ReadOnlySqliteFile>() as c_int
        );
        state.dispatch.xOpen = Some(ro_xopen);
        assert_eq!(unsafe { ffi::sqlite3_vfs_register(&mut state.dispatch, 0) }, ffi::SQLITE_OK);
        Self { state, _name: name }
    }
    fn name(&self) -> &str { self._name.to_str().unwrap() }
}
impl Drop for RegisteredReadOnlyVfs {
    fn drop(&mut self) {
        assert_eq!(unsafe { ffi::sqlite3_vfs_unregister(&mut self.state.dispatch) }, ffi::SQLITE_OK);
    }
}

struct OwnedRoot(PathBuf);
impl OwnedRoot {
    fn new() -> Self {
        static NEXT: AtomicUsize = AtomicUsize::new(0);
        let tick = SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_nanos();
        let path = std::env::temp_dir().join(format!("fabulaxiom-r3-ro-test-{}-{tick}-{}",
            process::id(), NEXT.fetch_add(1, Ordering::Relaxed)));
        fs::create_dir(&path).expect("unique CI scratch directory");
        Self(path)
    }
    fn database(&self) -> PathBuf { self.0.join("invented.sqlite3") }
}
impl Drop for OwnedRoot {
    fn drop(&mut self) {
        assert!(self.0.starts_with(std::env::temp_dir()));
        assert!(self.0.file_name().unwrap().to_string_lossy().starts_with("fabulaxiom-r3-ro-test-"));
        fs::remove_dir_all(&self.0).expect("only CI-owned disposable scratch");
    }
}

fn seed_invented_database(path: &Path, value: i64) {
    // Only after newly creating the test-owned %TEMP% directory, never an
    // existing operator profile. Seed with the ordinary SQLite VFS and CLOSE.
    let db = Connection::open(path).expect("fresh test-only database");
    db.execute("CREATE TABLE invented_r3 (value INTEGER NOT NULL)", []).unwrap();
    db.execute("INSERT INTO invented_r3(value) VALUES (?1)", [value]).unwrap();
    drop(db); // no concurrent writer when the read-only adapter runs
}

fn readonly_count(path: &Path, gate: &RegisteredReadOnlyVfs) -> i64 {
    let db = Connection::open_with_flags_and_vfs(
        path, OpenFlags::SQLITE_OPEN_READ_ONLY, gate.name()
    ).expect("read-only custom sqlite3_file must open a disposable SQLite image");
    db.query_row("SELECT value FROM invented_r3", [], |row| row.get(0)).unwrap()
}

#[test]
fn m32_r3_preopened_readonly_file_adapter_reads_invented_sqlite_content() {
    let root = OwnedRoot::new();
    let path = root.database();
    seed_invented_database(&path, 17);
    let held = OpenOptions::new().read(true).share_mode(SHARE_ALL)
        .open(&path).expect("held CI-owned database file");
    let expected = id_of(&held).unwrap();
    let gate = RegisteredReadOnlyVfs::new(held);
    assert_eq!(readonly_count(&path, &gate), 17);
    assert_eq!(gate.state.accepted.load(Ordering::SeqCst), 1);
    assert_eq!(gate.state.refused.load(Ordering::SeqCst), 0);
    assert_eq!(id_of(&File::open(&path).unwrap()), Some(expected));
    assert!(!path.with_file_name("invented.sqlite3-wal").exists());
    assert!(!path.with_file_name("invented.sqlite3-shm").exists());
}

#[test]
fn m32_r3_preopened_readonly_file_adapter_reads_original_after_name_substitution() {
    let root = OwnedRoot::new();
    let path = root.database();
    seed_invented_database(&path, 23);
    let held = OpenOptions::new().read(true).share_mode(SHARE_ALL)
        .open(&path).expect("held preapproved CI fixture");
    let original = id_of(&held).unwrap();
    let displaced = root.0.join("original-after-controlled-rename.sqlite3");
    fs::rename(&path, &displaced).expect("controlled rename of CI-owned file");
    seed_invented_database(&path, 99);
    let replacement = File::open(&path).unwrap();
    assert_ne!(id_of(&replacement), Some(original));
    let gate = RegisteredReadOnlyVfs::new(held);
    assert_eq!(readonly_count(&path, &gate), 23, "read original held File, never substituted path");
    assert_eq!(gate.state.accepted.load(Ordering::SeqCst), 1);
    assert_eq!(gate.state.refused.load(Ordering::SeqCst), 0);
    assert_eq!(id_of(&File::open(&displaced).unwrap()), Some(original));
    drop(replacement);
}

#[test]
fn m32_r3_preopened_readonly_file_adapter_refuses_write_open_before_dispatch() {
    let root = OwnedRoot::new();
    let path = root.database();
    seed_invented_database(&path, 31);
    let held = OpenOptions::new().read(true).share_mode(SHARE_ALL)
        .open(&path).expect("new disposable fixture");
    let gate = RegisteredReadOnlyVfs::new(held);
    let attempt = Connection::open_with_flags_and_vfs(
        &path, OpenFlags::SQLITE_OPEN_READ_WRITE, gate.name()
    );
    assert!(attempt.is_err(), "writeable SQLite xOpen must fail before any delegation");
    assert_eq!(gate.state.accepted.load(Ordering::SeqCst), 0);
    assert!(gate.state.refused.load(Ordering::SeqCst) >= 1);
    assert!(!path.with_file_name("invented.sqlite3-wal").exists());
    assert!(!path.with_file_name("invented.sqlite3-shm").exists());
}
