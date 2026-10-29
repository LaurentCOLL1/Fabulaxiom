//! R2->R3 Windows CI boundary: held disposable ancestor IDs and actual
//! SQLite-opened main HANDLE FileId128. This is test-only, never an admitted
//! profile or a pre-xOpen atomic guarantee. No SQL/migrations/WAL writes;
//! WAL/SHM identity remains R4 NOT_PROVEN and successor restart remains STOP.

use rusqlite::{ffi, Connection, OpenFlags};
use std::{
    ffi::{c_char, c_void},
    fs::{self, File, OpenOptions},
    io,
    os::windows::{fs::{MetadataExt, OpenOptionsExt}, io::AsRawHandle},
    path::{Path, PathBuf},
    process,
    ptr,
    sync::atomic::{AtomicUsize, Ordering},
    time::{SystemTime, UNIX_EPOCH},
};

const ROOT_PREFIX: &str = "fabulaxiom-r23-delegated-disposable-";
const READ_ATTRIBUTES: u32 = 0x80;
const SHARE_READ: u32 = 1;
const SHARE_WRITE: u32 = 2;
const BACKUP_SEMANTICS: u32 = 0x0200_0000;
const OPEN_REPARSE_POINT: u32 = 0x0020_0000;
const REPARSE_ATTRIBUTE: u32 = 0x400;
const MAIN: &str = "invented.sqlite3";
type Identity = (u64, [u8; 16]);

#[link(name = "kernel32")]
unsafe extern "system" {
    fn GetFileInformationByHandleEx(handle: *mut c_void, class: i32,
        data: *mut c_void, size: u32) -> i32;
}

#[repr(C)]
// Win32 FILE_ID_INFO layout: volume serial + 128-bit file identifier.
struct FileIdInfo { volume: u64, id: [u8; 16] }

#[derive(Debug, PartialEq, Eq)]
enum Refusal {
    AncestorUnsafe,
    AncestorChanged,
    MainChanged,
    UnknownSidecar,
    SqliteOpenFailed,
    SqliteHandleUnavailable,
    R4MappingUnproven,
}

fn id_raw(handle: *mut c_void) -> Result<Identity, Refusal> {
    let mut info = std::mem::MaybeUninit::<FileIdInfo>::uninit();
    let status = unsafe {
        GetFileInformationByHandleEx(handle, 0x12, info.as_mut_ptr().cast(),
            std::mem::size_of::<FileIdInfo>() as u32)
    };
    if status == 0 { return Err(Refusal::SqliteHandleUnavailable); }
    let value = unsafe { info.assume_init() };
    Ok((value.volume, value.id))
}
fn file_id(file: &File) -> Result<Identity, Refusal> {
    id_raw(file.as_raw_handle().cast())
}

fn sqlite_opened_id(db: &Connection) -> Result<Identity, Refusal> {
    let mut handle: *mut c_void = ptr::null_mut();
    // Borrow only while the SQLite connection is live; never close this HANDLE.
    let status = unsafe {
        ffi::sqlite3_file_control(db.handle(), b"main\0".as_ptr().cast::<c_char>(),
            ffi::SQLITE_FCNTL_WIN32_GET_HANDLE,
            (&mut handle as *mut *mut c_void).cast())
    };
    if status != ffi::SQLITE_OK || handle.is_null() {
        return Err(Refusal::SqliteHandleUnavailable);
    }
    id_raw(handle)
}

struct OwnedRoot(PathBuf);
impl OwnedRoot {
    fn fresh() -> Self {
        static COUNTER: AtomicUsize = AtomicUsize::new(0);
        let tick = SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_nanos();
        let root = std::env::temp_dir().join(format!("{ROOT_PREFIX}{}-{tick}-{}",
            process::id(), COUNTER.fetch_add(1, Ordering::Relaxed)));
        fs::create_dir(&root).expect("new disposable CI root");
        fs::create_dir(root.join("fictional-profile")).unwrap();
        fs::create_dir(root.join("fictional-profile").join("database")).unwrap();
        Self(root)
    }
    fn parent_paths(&self) -> [PathBuf; 3] {
        [self.0.clone(), self.0.join("fictional-profile"),
            self.0.join("fictional-profile").join("database")]
    }
    fn main(&self) -> PathBuf {
        self.0.join("fictional-profile").join("database").join(MAIN)
    }
    fn create_empty_main(&self) -> File {
        OpenOptions::new().read(true).write(true).create_new(true)
            .open(self.main()).expect("CREATE_NEW only in test-owned root")
    }
}
impl Drop for OwnedRoot {
    fn drop(&mut self) {
        assert!(self.0.starts_with(std::env::temp_dir()));
        assert!(self.0.file_name().unwrap().to_string_lossy().starts_with(ROOT_PREFIX));
        fs::remove_dir_all(&self.0).expect("cleanup CI fixture after handles close");
    }
}

fn directory_handle(path: &Path) -> Result<File, Refusal> {
    let metadata = fs::symlink_metadata(path).map_err(|_| Refusal::AncestorUnsafe)?;
    if !metadata.is_dir() || metadata.file_attributes() & REPARSE_ATTRIBUTE != 0 {
        return Err(Refusal::AncestorUnsafe);
    }
    OpenOptions::new().access_mode(READ_ATTRIBUTES)
        .share_mode(SHARE_READ | SHARE_WRITE)
        .custom_flags(BACKUP_SEMANTICS | OPEN_REPARSE_POINT)
        .open(path).map_err(|_| Refusal::AncestorUnsafe)
}

struct Pins(Vec<(PathBuf, File, Identity)>);
impl Pins {
    fn acquire(root: &OwnedRoot) -> Result<Self, Refusal> {
        let mut pins = Vec::new();
        for path in root.parent_paths() {
            let handle = directory_handle(&path)?;
            let expected = file_id(&handle)?;
            let reopened = directory_handle(&path)?;
            if file_id(&reopened)? != expected { return Err(Refusal::AncestorChanged); }
            pins.push((path, handle, expected));
        }
        Ok(Self(pins))
    }
    fn revalidate(&self, root: &OwnedRoot) -> Result<(), Refusal> {
        for ((path, held, id), expected_path) in self.0.iter().zip(root.parent_paths()) {
            if path != &expected_path || file_id(held)? != *id {
                return Err(Refusal::AncestorChanged);
            }
            let reopened = directory_handle(path).map_err(|_| Refusal::AncestorChanged)?;
            if file_id(&reopened)? != *id { return Err(Refusal::AncestorChanged); }
        }
        Ok(())
    }
}

fn sidecars_absent(path: &Path) -> bool {
    ["-wal", "-shm", "-journal"].iter().all(|suffix| {
        path.with_file_name(format!("{MAIN}{suffix}")).symlink_metadata()
            .is_err_and(|err| err.kind() == io::ErrorKind::NotFound)
    })
}

// One reviewed SQLite constructor, called only after test-only preflight.
// It can have SQLite open-time effects, therefore this is NOT a real profile
// admission path. No SQL is issued even when the identity matches.
fn open_after_fixture_preflight<'a>(
    root: &OwnedRoot, pins: &'a Pins, expected_main: Identity, swap_after_precheck: bool,
) -> Result<Connection, Refusal> {
    pins.revalidate(root)?;
    if !sidecars_absent(&root.main()) { return Err(Refusal::UnknownSidecar); }
    let before = File::open(root.main()).map_err(|_| Refusal::MainChanged)?;
    if file_id(&before)? != expected_main { return Err(Refusal::MainChanged); }
    drop(before);
    // Controlled TOCTOU *only* inside the newly-owned disposable fixture.
    // The observed main name can now lead to a different SQLite-opened HANDLE.
    if swap_after_precheck {
        let displaced = root.main().with_file_name("displaced-after-preflight");
        fs::rename(root.main(), displaced).map_err(|_| Refusal::MainChanged)?;
        OpenOptions::new().write(true).create_new(true).open(root.main())
            .map_err(|_| Refusal::MainChanged)?;
    }
    let db = Connection::open_with_flags(&root.main(), OpenFlags::SQLITE_OPEN_READ_WRITE)
        .map_err(|_| Refusal::SqliteOpenFailed)?;
    let opened = sqlite_opened_id(&db)?;
    if opened != expected_main { return Err(Refusal::MainChanged); }
    pins.revalidate(root)?;
    Ok(db)
}

// An observed match may advance only to R4 testing; it never mints a
// production V7WriterAdmission token, even when the handles are identical.
fn refuse_unverified_r4(root: &OwnedRoot, pins: &Pins, db: &Connection,
    expected: Identity) -> Refusal {
    if pins.revalidate(root).is_err() || sqlite_opened_id(db).ok() != Some(expected) {
        Refusal::MainChanged
    } else {
        Refusal::R4MappingUnproven
    }
}

#[test]
fn m32_r23_pinned_ancestors_and_actual_sqlite_handle_match_on_fresh_fixture() {
    let root = OwnedRoot::fresh();
    let first = root.create_empty_main();
    let expected = file_id(&first).unwrap();
    let pins = Pins::acquire(&root).unwrap();
    let db = open_after_fixture_preflight(&root, &pins, expected, false).unwrap();
    assert_eq!(sqlite_opened_id(&db), Ok(expected));
    assert_eq!(pins.revalidate(&root), Ok(()));
    // SQLite xOpen already ran, so positive equality cannot mint R3 admission.
    assert_eq!(refuse_unverified_r4(&root, &pins, &db, expected),
        Refusal::R4MappingUnproven);
    assert!(db.close().is_ok(), "test-only close, no SQL");
    drop(pins);
    drop(first);
}

#[test]
fn m32_r23_replaced_main_name_refuses_before_sqlite_open() {
    let root = OwnedRoot::fresh();
    let first = root.create_empty_main();
    let expected = file_id(&first).unwrap();
    drop(first);
    let moved = root.0.join("fictional-profile").join("database").join("old-file");
    fs::rename(root.main(), &moved).unwrap();
    let replacement = root.create_empty_main();
    assert_ne!(file_id(&replacement).unwrap(), expected);
    let pins = Pins::acquire(&root).unwrap();
    let result = open_after_fixture_preflight(&root, &pins, expected, false);
    assert!(matches!(result, Err(Refusal::MainChanged)));
    assert_eq!(fs::read(&moved).unwrap(), Vec::<u8>::new());
}

#[test]
fn m32_r23_unknown_sidecar_refuses_without_changing_sentinel() {
    for suffix in ["-wal", "-shm", "-journal"] {
        let root = OwnedRoot::fresh();
        let first = root.create_empty_main();
        let expected = file_id(&first).unwrap();
        let pins = Pins::acquire(&root).unwrap();
        let sidecar = root.main().with_file_name(format!("{MAIN}{suffix}"));
        fs::write(&sidecar, b"foreign-fixture").unwrap();
        assert!(matches!(open_after_fixture_preflight(&root, &pins, expected, false),
            Err(Refusal::UnknownSidecar)));
        assert_eq!(fs::read(&sidecar).unwrap(), b"foreign-fixture");
    }
}


#[test]
fn m32_r23_controlled_swap_after_precheck_vetoes_real_sqlite_handle() {
    let root = OwnedRoot::fresh();
    let first = root.create_empty_main();
    let expected = file_id(&first).unwrap();
    drop(first); // permit controlled rename on test-owned Windows file.
    let pins = Pins::acquire(&root).unwrap();
    assert!(matches!(open_after_fixture_preflight(&root, &pins, expected, true),
        Err(Refusal::MainChanged)));
    // The original name moved; no SQL or recovery was attempted on either.
    assert!(root.main().with_file_name("displaced-after-preflight").is_file());
    assert_eq!(pins.revalidate(&root), Ok(()));
}


// R3 probe: retain a Win32 MAIN handle without FILE_SHARE_DELETE throughout
// the separate pathname-based SQLite xOpen. This tests cooperative Win32 rename
// exclusion on a NEW, disposable file; it does not prove atomic VFS admission,
// hard-link immunity, or the WAL/SHM/callback side of the same session.
#[test]
fn m32_r3_held_main_without_delete_share_refuses_rename_before_sqlite_open() {
    let root = OwnedRoot::fresh();
    let first = root.create_empty_main();
    drop(first);
    let held = OpenOptions::new().read(true).write(true)
        .share_mode(SHARE_READ | SHARE_WRITE).open(root.main()).unwrap();
    let expected = file_id(&held).unwrap();
    let pins = Pins::acquire(&root).unwrap();
    let displaced = root.main().with_file_name("renamed-under-held-main");
    assert!(fs::rename(root.main(), &displaced).is_err(),
        "Win32 main handle without FILE_SHARE_DELETE must prevent rename");
    assert_eq!(file_id(&File::open(root.main()).unwrap()), Ok(expected));
    assert!(!displaced.exists(), "failed rename cannot install another identity");
    assert_eq!(pins.revalidate(&root), Ok(()));
    drop(held);
    // Negative control: rename becomes possible after releasing the main claim.
    fs::rename(root.main(), &displaced).unwrap();
    assert!(displaced.is_file());
    assert!(!root.main().exists());
    drop(pins);
}

#[test]
fn m32_r3_held_main_without_delete_share_survives_sqlite_xopen_but_stops_at_r4() {
    let root = OwnedRoot::fresh();
    let first = root.create_empty_main();
    drop(first);
    let held = OpenOptions::new().read(true).write(true)
        .share_mode(SHARE_READ | SHARE_WRITE).open(root.main()).unwrap();
    let expected = file_id(&held).unwrap();
    let pins = Pins::acquire(&root).unwrap();
    // Uses the SINGLE already-inventoried SQLite open site; no new SQL site.
    let db = open_after_fixture_preflight(&root, &pins, expected, false).unwrap();
    assert_eq!(sqlite_opened_id(&db), Ok(expected));
    assert_eq!(file_id(&held), Ok(expected));
    assert_eq!(pins.revalidate(&root), Ok(()));
    assert_eq!(refuse_unverified_r4(&root, &pins, &db, expected),
        Refusal::R4MappingUnproven, "a held main is NOT a WAL/SHM admission");
    assert!(db.close().is_ok(), "fixture-only close without SQL");
    drop(held);
    drop(pins);
}


// Separate Windows process holds no pre-existing database privileges. The child
// receives only an explicitly invented per-test path under fresh %TEMP%.
// This is a CI experiment, not a Windows operator profile or a writer IPC.
const R3_CHILD_FILE: &str = "FABULAXIOM_R3_DISPOSABLE_CHILD_FILE";
const R3_CHILD_DENIED: i32 = 71;
const R3_CHILD_RENAMED: i32 = 72;

#[test]
fn m32_r3_child_rename_probe_only_fresh_disposable_main() {
    let Some(raw) = std::env::var_os(R3_CHILD_FILE) else { return };
    let path = PathBuf::from(raw);
    assert_eq!(path.file_name(), Some(std::ffi::OsStr::new(MAIN)));
    let database = path.parent().unwrap();
    assert_eq!(database.file_name(), Some(std::ffi::OsStr::new("database")));
    let profile = database.parent().unwrap();
    assert_eq!(profile.file_name(), Some(std::ffi::OsStr::new("fictional-profile")));
    let root = profile.parent().unwrap();
    assert!(root.starts_with(std::env::temp_dir()));
    assert!(root.file_name().unwrap().to_string_lossy().starts_with(ROOT_PREFIX));
    assert!(fs::symlink_metadata(&path).unwrap().is_file());
    let moved = path.with_file_name("moved-by-disposable-child");
    assert!(!moved.exists());
    let code = if fs::rename(&path, &moved).is_ok() {
        R3_CHILD_RENAMED
    } else {
        R3_CHILD_DENIED
    };
    process::exit(code);
}

fn r3_disposable_child_rename(path: &Path) -> i32 {
    assert_eq!(path.file_name(), Some(std::ffi::OsStr::new(MAIN)));
    let status = process::Command::new(std::env::current_exe().unwrap())
        .arg("--exact")
        .arg("m32_r23_sqlite_handle_boundary_tests::m32_r3_child_rename_probe_only_fresh_disposable_main")
        .arg("--nocapture")
        .env(R3_CHILD_FILE, path)
        .status().expect("only CI Rust test executable may run");
    status.code().expect("child must report an explicit rename result")
}

#[test]
fn m32_r3_other_process_rename_is_refused_before_and_during_sqlite_xopen() {
    let root = OwnedRoot::fresh();
    let first = root.create_empty_main();
    let expected = file_id(&first).unwrap();
    drop(first);
    let claim = OpenOptions::new().read(true).write(true)
        .share_mode(SHARE_READ | SHARE_WRITE).open(root.main()).unwrap();
    assert_eq!(file_id(&claim), Ok(expected));
    let pins = Pins::acquire(&root).unwrap();
    assert_eq!(r3_disposable_child_rename(&root.main()), R3_CHILD_DENIED);
    assert_eq!(file_id(&File::open(root.main()).unwrap()), Ok(expected));
    let db = open_after_fixture_preflight(&root, &pins, expected, false).unwrap();
    assert_eq!(sqlite_opened_id(&db), Ok(expected));
    assert_eq!(r3_disposable_child_rename(&root.main()), R3_CHILD_DENIED);
    assert_eq!(sqlite_opened_id(&db), Ok(expected));
    assert_eq!(refuse_unverified_r4(&root, &pins, &db, expected),
        Refusal::R4MappingUnproven);
    assert!(db.close().is_ok(), "disposable main close without SQL");
    drop(claim);
    // A true negative control: child succeeds with the very same owned path
    // after the claim is dropped, even while ancestor handles are retained.
    assert_eq!(r3_disposable_child_rename(&root.main()), R3_CHILD_RENAMED);
    assert!(!root.main().exists());
    assert_eq!(file_id(&File::open(root.main().with_file_name("moved-by-disposable-child")).unwrap()),
        Ok(expected));
    drop(pins);
}


// R3 follow-up: Win32 ReOpenFile works from an already selected HANDLE, not
// the pathname. This is a *non-SQLite* CI-only experiment; the existing SQLite
// default VFS still opens by name and MUST NOT be called atomic by these tests.
#[link(name = "kernel32")]
unsafe extern "system" {
    fn ReOpenFile(original: *mut c_void, access: u32, share: u32, flags: u32) -> *mut c_void;
}
const R3_SHARE_DELETE: u32 = 4;
const R3_GENERIC_READ: u32 = 0x8000_0000;
const R3_GENERIC_WRITE: u32 = 0x4000_0000;

fn r3_reopen_existing_win32_file(file: &File, share: u32) -> io::Result<File> {
    use std::os::windows::io::FromRawHandle;
    let reopened = unsafe {
        ReOpenFile(file.as_raw_handle().cast(), R3_GENERIC_READ | R3_GENERIC_WRITE, share, 0)
    };
    if reopened as isize == -1 {
        return Err(io::Error::last_os_error());
    }
    // ReOpenFile creates a NEW HANDLE. Ownership transfers to the Rust File;
    // the borrowed original handle is never closed or consumed.
    Ok(unsafe { File::from_raw_handle(reopened.cast()) })
}

#[test]
fn m32_r3_reopenfile_preserves_live_disposable_main_identity_without_path_lookup() {
    let root = OwnedRoot::fresh();
    root.create_empty_main();
    let held = OpenOptions::new().read(true).write(true)
        .share_mode(SHARE_READ | SHARE_WRITE).open(root.main()).unwrap();
    let original = file_id(&held).unwrap();
    let reopened = r3_reopen_existing_win32_file(&held, SHARE_READ | SHARE_WRITE)
        .expect("ReOpenFile should reopen the already held fixture object");
    assert_eq!(file_id(&reopened), Ok(original));
    assert_eq!(file_id(&File::open(root.main()).unwrap()), Ok(original));
    assert!(fs::rename(root.main(), root.main().with_file_name("cannot-rename-held-main")).is_err());
    drop(reopened);
    drop(held);
    assert!(!root.main().with_file_name("cannot-rename-held-main").exists());
}

#[test]
fn m32_r3_reopenfile_binds_original_file_even_after_name_replacement() {
    let root = OwnedRoot::fresh();
    let held = OpenOptions::new().read(true).write(true).create_new(true)
        .share_mode(SHARE_READ | SHARE_WRITE | R3_SHARE_DELETE)
        .open(root.main()).unwrap();
    let original = file_id(&held).unwrap();
    let displaced = root.main().with_file_name("displaced-before-handle-reopen");
    fs::rename(root.main(), &displaced).unwrap();
    let replacement = OpenOptions::new().read(true).write(true).create_new(true)
        .share_mode(SHARE_READ | SHARE_WRITE | R3_SHARE_DELETE)
        .open(root.main()).unwrap();
    let foreign_identity = file_id(&replacement).unwrap();
    assert_ne!(foreign_identity, original, "controlled CI-only name replacement");
    let reopened = r3_reopen_existing_win32_file(
        &held, SHARE_READ | SHARE_WRITE | R3_SHARE_DELETE
    ).expect("ReOpenFile MUST follow original handle, not the substituted name");
    assert_eq!(file_id(&reopened), Ok(original));
    assert_eq!(file_id(&held), Ok(original));
    assert_eq!(file_id(&File::open(&displaced).unwrap()), Ok(original));
    assert_eq!(file_id(&File::open(root.main()).unwrap()), Ok(foreign_identity));
    drop(reopened);
    drop(replacement);
    drop(held);
}
