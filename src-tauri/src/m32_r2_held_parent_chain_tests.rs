//! P1 R2 held-ancestor witness on disposable Windows CI file objects.
//! Complements #223's lexical/mutex/FileId prefix without changing its
//! five historical tests. Never opens SQLite or an existing operator profile.
//! A successful check stops at R4: WAL/SHM mapping and V7 admission remain
//! independently unproven. Held-directory IDs do NOT seal an arbitrary later
//! pathname-based SQLite xOpen or attest a predecessor after crash.

use std::{
    ffi::{c_void, OsStr},
    fs::{self, File, OpenOptions},
    io::{self, Write},
    os::windows::{ffi::OsStrExt, fs::{MetadataExt, OpenOptionsExt}, io::AsRawHandle},
    path::{Path, PathBuf},
    process,
    ptr,
    sync::atomic::{AtomicUsize, Ordering},
    time::{SystemTime, UNIX_EPOCH},
};

const ROOT_PREFIX: &str = "fabulaxiom-r2-held-chain-";
const PROFILE: &str = "fictional-profile";
const DB_DIR: &str = "database";
const DB_FILE: &str = "new.sqlite3";
const FILE_ATTRIBUTE_REPARSE_POINT: u32 = 0x400;
const FILE_FLAG_BACKUP_SEMANTICS: u32 = 0x0200_0000;
const FILE_FLAG_OPEN_REPARSE_POINT: u32 = 0x0020_0000;
const FILE_READ_ATTRIBUTES: u32 = 0x0000_0080;
const FILE_SHARE_READ: u32 = 1;
const FILE_SHARE_WRITE: u32 = 2;
const WAIT_OBJECT_0: u32 = 0;
const ERROR_ALREADY_EXISTS: u32 = 183;

#[link(name = "kernel32")]
unsafe extern "system" {
    fn GetFileInformationByHandleEx(handle: *mut c_void, class: i32, data: *mut c_void, size: u32) -> i32;
    fn CreateMutexW(attrs: *mut c_void, initial_owner: i32, name: *const u16) -> *mut c_void;
    fn WaitForSingleObject(handle: *mut c_void, timeout: u32) -> u32;
    fn ReleaseMutex(handle: *mut c_void) -> i32;
    fn CloseHandle(handle: *mut c_void) -> i32;
    fn GetLastError() -> u32;
}

#[repr(C)]
struct FileIdInfo { volume: u64, id: [u8; 16] }
type Identity = (u64, [u8; 16]);

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Refusal {
    NotCooperativelyOwned,
    UnsafeDirectory,
    DirectoryChanged,
    MainFileChanged,
    UnknownSidecar,
    R4ShmMappingUnproven,
}

fn file_id(file: &File) -> Result<Identity, Refusal> {
    let mut info = std::mem::MaybeUninit::<FileIdInfo>::uninit();
    let ok = unsafe {
        GetFileInformationByHandleEx(file.as_raw_handle().cast(), 0x12,
            info.as_mut_ptr().cast(), std::mem::size_of::<FileIdInfo>() as u32)
    };
    if ok == 0 { return Err(Refusal::UnsafeDirectory); }
    let info = unsafe { info.assume_init() };
    Ok((info.volume, info.id))
}

struct Root(PathBuf);
impl Root {
    fn fresh() -> Self {
        static SEQ: AtomicUsize = AtomicUsize::new(0);
        let tick = SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_nanos();
        let root = std::env::temp_dir().join(format!("{ROOT_PREFIX}{}-{tick}-{}",
            process::id(), SEQ.fetch_add(1, Ordering::Relaxed)));
        fs::create_dir(&root).expect("new unique test-owned root");
        fs::create_dir(root.join(PROFILE)).unwrap();
        fs::create_dir(root.join(PROFILE).join(DB_DIR)).unwrap();
        Self(root)
    }
    fn profile(&self) -> PathBuf { self.0.join(PROFILE) }
    fn db_dir(&self) -> PathBuf { self.profile().join(DB_DIR) }
    fn main(&self) -> PathBuf { self.db_dir().join(DB_FILE) }
    fn parents(&self) -> [PathBuf; 3] { [self.0.clone(), self.profile(), self.db_dir()] }
    fn new_main(&self) -> File {
        OpenOptions::new().read(true).write(true).create_new(true).open(self.main())
            .expect("new-only fictional main, not a SQLite profile")
    }
    fn claim_name(&self) -> String {
        format!("Local\\Fabulaxiom-R2-Held-{}", self.0.file_name().unwrap().to_string_lossy())
    }
}
impl Drop for Root {
    fn drop(&mut self) {
        assert!(self.0.starts_with(std::env::temp_dir()));
        assert!(self.0.file_name().unwrap().to_string_lossy().starts_with(ROOT_PREFIX));
        fs::remove_dir_all(&self.0).expect("delete fixture root after handles are dropped");
    }
}

struct CooperativeClaim { handle: *mut c_void, held: bool }
impl CooperativeClaim {
    fn new(root: &Root) -> Self {
        let name = root.claim_name();
        assert!(name.starts_with("Local\\Fabulaxiom-R2-Held-"));
        let wide: Vec<u16> = OsStr::new(&name).encode_wide().chain(Some(0)).collect();
        let handle = unsafe { CreateMutexW(ptr::null_mut(), 0, wide.as_ptr()) };
        assert!(!handle.is_null(), "test-only Win32 mutex");
        assert_ne!(unsafe { GetLastError() }, ERROR_ALREADY_EXISTS, "unexpected preexisting fixture claim");
        let held = unsafe { WaitForSingleObject(handle, 0) } == WAIT_OBJECT_0;
        assert!(held, "fixture mutex claim must be uncontended");
        Self { handle, held }
    }
}
impl Drop for CooperativeClaim {
    fn drop(&mut self) {
        if self.held { assert_ne!(unsafe { ReleaseMutex(self.handle) }, 0); }
        assert_ne!(unsafe { CloseHandle(self.handle) }, 0);
    }
}

fn directory_handle(path: &Path) -> Result<File, Refusal> {
    let m = fs::symlink_metadata(path).map_err(|_| Refusal::UnsafeDirectory)?;
    if !m.is_dir() || m.file_attributes() & FILE_ATTRIBUTE_REPARSE_POINT != 0 {
        return Err(Refusal::UnsafeDirectory);
    }
    // Deny delete-sharing to make attempted rename observable. Names must
    // still be revalidated; this is NOT an atomic OS open proof for SQLite.
    OpenOptions::new()
        .access_mode(FILE_READ_ATTRIBUTES)
        .share_mode(FILE_SHARE_READ | FILE_SHARE_WRITE)
        .custom_flags(FILE_FLAG_BACKUP_SEMANTICS | FILE_FLAG_OPEN_REPARSE_POINT)
        .open(path).map_err(|_| Refusal::UnsafeDirectory)
}

struct PinnedChain(Vec<(PathBuf, File, Identity)>);
impl PinnedChain {
    fn acquire(root: &Root) -> Result<Self, Refusal> {
        let mut pins = Vec::with_capacity(3);
        for path in root.parents() {
            let handle = directory_handle(&path)?;
            let id = file_id(&handle)?;
            let reopened = directory_handle(&path)?;
            if file_id(&reopened)? != id { return Err(Refusal::DirectoryChanged); }
            drop(reopened);
            pins.push((path, handle, id));
        }
        Ok(Self(pins))
    }
    fn revalidate(&self, root: &Root) -> Result<(), Refusal> {
        if self.0.len() != 3 { return Err(Refusal::DirectoryChanged); }
        let expected_paths = root.parents();
        for ((path, held, id), expected) in self.0.iter().zip(expected_paths.iter()) {
            if path != expected || file_id(held)? != *id {
                return Err(Refusal::DirectoryChanged);
            }
            let reopened = directory_handle(path).map_err(|_| Refusal::DirectoryChanged)?;
            if file_id(&reopened)? != *id { return Err(Refusal::DirectoryChanged); }
        }
        Ok(())
    }
}

fn sidecars_absent(path: &Path) -> bool {
    ["-wal", "-shm", "-journal"].iter().all(|suffix| {
        path.with_file_name(format!("{DB_FILE}{suffix}")).symlink_metadata()
            .is_err_and(|e| e.kind() == io::ErrorKind::NotFound)
    })
}

fn boundary(root: &Root, claim: &CooperativeClaim, pins: &PinnedChain,
    expected_main_id: Identity) -> Result<(), Refusal>
{
    if !claim.held { return Err(Refusal::NotCooperativelyOwned); }
    pins.revalidate(root)?;
    if !sidecars_absent(&root.main()) { return Err(Refusal::UnknownSidecar); }
    // This is just a native FileId handle read, never an SQLite open.
    let main = File::open(root.main()).map_err(|_| Refusal::MainFileChanged)?;
    if file_id(&main)? != expected_main_id { return Err(Refusal::MainFileChanged); }
    pins.revalidate(root)?;
    Ok(())
}

fn stop_after_bound_fixture_prefix(root: &Root, claim: &CooperativeClaim,
    pins: &PinnedChain, expected: Identity) -> Refusal
{
    match boundary(root, claim, pins, expected) {
        Err(e) => e,
        Ok(()) => Refusal::R4ShmMappingUnproven,
    }
}

#[test]
fn m32_p1_r2_held_parent_handles_and_main_id_stop_at_unmapped_shm() {
    let root = Root::fresh();
    let main = root.new_main();
    let expected = file_id(&main).unwrap();
    let claim = CooperativeClaim::new(&root);
    let pins = PinnedChain::acquire(&root).unwrap();
    assert_eq!(boundary(&root, &claim, &pins, expected), Ok(()));
    assert_eq!(stop_after_bound_fixture_prefix(&root, &claim, &pins, expected),
        Refusal::R4ShmMappingUnproven);
    // The pins must outlive every revalidation and potential DB operation.
}

#[test]
fn m32_p1_r2_parent_rename_while_held_is_denied_or_detected() {
    let root = Root::fresh();
    let main = root.new_main();
    let expected = file_id(&main).unwrap();
    let claim = CooperativeClaim::new(&root);
    let pins = PinnedChain::acquire(&root).unwrap();
    let profile = root.profile();
    let moved = root.0.join("profile-displaced");
    match fs::rename(&profile, &moved) {
        Err(_) => {
            assert_eq!(boundary(&root, &claim, &pins, expected), Ok(()));
        }
        Ok(()) => {
            // A filesystem accepting a move must not be mistaken for an
            // authenticated old pathname. Close pins before restoring.
            assert!(boundary(&root, &claim, &pins, expected).is_err());
            drop(pins);
            drop(main);
            fs::rename(&moved, &profile).expect("restore only disposable fixture");
            return;
        }
    }
    assert_eq!(stop_after_bound_fixture_prefix(&root, &claim, &pins, expected),
        Refusal::R4ShmMappingUnproven);
}

#[test]
fn m32_p1_r2_parent_pins_do_not_authenticate_replaced_main_name() {
    let root = Root::fresh();
    let first = root.new_main();
    let old_id = file_id(&first).unwrap();
    drop(first);
    let displaced = root.db_dir().join("displaced-fiction.sqlite3");
    fs::rename(root.main(), &displaced).expect("move new empty fixture main");
    let mut replacement = root.new_main();
    replacement.write_all(b"fiction only").unwrap();
    assert_ne!(file_id(&replacement).unwrap(), old_id);
    let claim = CooperativeClaim::new(&root);
    let pins = PinnedChain::acquire(&root).unwrap();
    assert_eq!(boundary(&root, &claim, &pins, old_id),
        Err(Refusal::MainFileChanged));
    assert!(fs::read(&displaced).unwrap().is_empty());
}

#[test]
fn m32_p1_r2_pinned_chain_refuses_unexpected_sidecar_without_editing_it() {
    for suffix in ["-wal", "-shm", "-journal"] {
        let root = Root::fresh();
        let main = root.new_main();
        let expected = file_id(&main).unwrap();
        let claim = CooperativeClaim::new(&root);
        let pins = PinnedChain::acquire(&root).unwrap();
        let sentinel = root.db_dir().join(format!("{DB_FILE}{suffix}"));
        fs::write(&sentinel, b"untrusted-fixture-sentinel").unwrap();
        assert_eq!(boundary(&root, &claim, &pins, expected), Err(Refusal::UnknownSidecar));
        assert_eq!(fs::read(&sentinel).unwrap(), b"untrusted-fixture-sentinel");
    }
}
