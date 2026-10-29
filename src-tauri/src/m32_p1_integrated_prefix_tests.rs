//! P1 bounded R1–R4 *pre-admission* Windows CI test chain.
//! Every file is created under a new %TEMP% root by this Rust test binary.
//! There is no SQLite open, recovery, Tauri registration or writer token.
//! This integrates real Win32 mutex and FILE_ID_INFO checks, but deliberately
//! leaves R2 ancestor pinning and R4 WAL/SHM mapping NOT_PROVEN.
//! Passing a preflight never grants EXISTING_PROFILE or v7 writer admission.

use std::{
    ffi::{c_void, OsStr},
    fs::{self, File, OpenOptions},
    io::{self, Write},
    os::windows::{ffi::OsStrExt, fs::MetadataExt, io::AsRawHandle},
    path::{Path, PathBuf},
    process,
    ptr,
    sync::atomic::{AtomicUsize, Ordering},
    time::{SystemTime, UNIX_EPOCH},
};

const ROOT_PREFIX: &str = "fabulaxiom-p1-prefix-fixture-";
const WAIT_OBJECT_0: u32 = 0;
const WAIT_TIMEOUT: u32 = 0x102;
const ERROR_ALREADY_EXISTS: u32 = 183;
const FILE_ATTRIBUTE_REPARSE_POINT: u32 = 0x400;

#[link(name = "kernel32")]
unsafe extern "system" {
    fn CreateMutexW(attributes: *mut c_void, initial_owner: i32, name: *const u16) -> *mut c_void;
    fn WaitForSingleObject(handle: *mut c_void, milliseconds: u32) -> u32;
    fn ReleaseMutex(handle: *mut c_void) -> i32;
    fn CloseHandle(handle: *mut c_void) -> i32;
    fn GetLastError() -> u32;
    fn GetFileInformationByHandleEx(handle: *mut c_void, class: i32, data: *mut c_void, size: u32) -> i32;
}

#[repr(C)]
struct FileIdInfo { volume: u64, id: [u8; 16] }

type Identity = (u64, [u8; 16]);

fn file_id(file: &File) -> Result<Identity, &'static str> {
    let mut info = std::mem::MaybeUninit::<FileIdInfo>::uninit();
    let code = unsafe {
        GetFileInformationByHandleEx(file.as_raw_handle().cast(), 0x12,
            info.as_mut_ptr().cast(), std::mem::size_of::<FileIdInfo>() as u32)
    };
    if code == 0 { return Err("FILE_ID_INFO_UNAVAILABLE"); }
    let info = unsafe { info.assume_init() };
    Ok((info.volume, info.id))
}

struct Disposable(PathBuf);
impl Disposable {
    fn new() -> Self {
        static SEQ: AtomicUsize = AtomicUsize::new(0);
        let tick = SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_nanos();
        let root = std::env::temp_dir().join(format!("{ROOT_PREFIX}{}-{tick}-{}",
            process::id(), SEQ.fetch_add(1, Ordering::Relaxed)));
        fs::create_dir(&root).expect("create a new, fixture-owned %TEMP% directory");
        Self(root)
    }
    fn main(&self) -> PathBuf { self.0.join("new.sqlite3") }
    fn new_main(&self) -> File {
        OpenOptions::new().read(true).write(true).create_new(true)
            .open(self.main()).expect("CREATE_NEW only in a fresh fixture root")
    }
    fn mutex_name(&self) -> String {
        format!("Local\\Fabulaxiom-P1-Prefix-{}",
            self.0.file_name().unwrap().to_string_lossy())
    }
}
impl Drop for Disposable {
    fn drop(&mut self) {
        assert!(self.0.starts_with(std::env::temp_dir()));
        assert!(self.0.file_name().unwrap().to_string_lossy().starts_with(ROOT_PREFIX));
        fs::remove_dir_all(&self.0).expect("cleanup only own disposable fixture root");
    }
}

struct ClaimedMutex { handle: *mut c_void, held: bool }
impl ClaimedMutex {
    fn fresh(name: &str) -> (Self, bool) {
        assert!(name.starts_with("Local\\Fabulaxiom-P1-Prefix-"));
        let name: Vec<u16> = OsStr::new(name).encode_wide().chain(Some(0)).collect();
        let handle = unsafe { CreateMutexW(ptr::null_mut(), 0, name.as_ptr()) };
        assert!(!handle.is_null(), "test-owned CreateMutexW");
        let preexisting = unsafe { GetLastError() == ERROR_ALREADY_EXISTS };
        (Self { handle, held: false }, preexisting)
    }
    fn claim(&mut self) -> u32 {
        let code = unsafe { WaitForSingleObject(self.handle, 0) };
        if code == WAIT_OBJECT_0 { self.held = true; }
        code
    }
}
impl Drop for ClaimedMutex {
    fn drop(&mut self) {
        if self.held {
            assert_ne!(unsafe { ReleaseMutex(self.handle) }, 0);
        }
        assert_ne!(unsafe { CloseHandle(self.handle) }, 0);
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Refusal {
    UntrustedNamespace, Sidecar, IdentityMismatch, MutexNotClaimed,
    R2AncestorsNotPinned, R4MappingNotProven, R5SchemaUnverified,
    R7PredecessorUnknown,
}

fn safe_path(root: &Disposable, path: &Path) -> bool {
    if path != root.main() || path.file_name() != Some(OsStr::new("new.sqlite3")) {
        return false;
    }
    if !root.0.starts_with(std::env::temp_dir()) ||
        !root.0.file_name().unwrap().to_string_lossy().starts_with(ROOT_PREFIX) {
        return false;
    }
    for p in [root.0.as_path(), path] {
        match p.symlink_metadata() {
            Ok(metadata) if metadata.file_attributes() & FILE_ATTRIBUTE_REPARSE_POINT == 0 => {}
            _ => return false,
        }
    }
    true
}

fn sidecars_absent(path: &Path) -> bool {
    // Missing means absent, any other I/O error or dangling link means STOP.
    ["-wal", "-shm", "-journal"].iter().all(|suffix| {
        path.with_file_name(format!("new.sqlite3{suffix}")).symlink_metadata()
            .is_err_and(|error| error.kind() == io::ErrorKind::NotFound)
    })
}

/// Observes R1/R3 real objects and a limited R2/R4 lexical preflight.
/// This is NOT pre-xOpen atomic identity and not a schema/actor proof.
fn observed_prefix(root: &Disposable, held: bool, file: &File,
    expected: Identity) -> Result<(), Refusal>
{
    if !held { return Err(Refusal::MutexNotClaimed); }
    if !safe_path(root, &root.main()) { return Err(Refusal::UntrustedNamespace); }
    if !sidecars_absent(&root.main()) { return Err(Refusal::Sidecar); }
    if file_id(file).ok() != Some(expected) { return Err(Refusal::IdentityMismatch); }
    Ok(())
}

fn next_gate_after_observation(root: &Disposable, held: bool, file: &File,
    expected: Identity) -> Refusal
{
    match observed_prefix(root, held, file, expected) {
        Err(reason) => reason,
        // A successful lexical preflight/handle observation is deliberately
        // NOT an R2 ancestor-handle pin and certainly not R5–R9 admission.
        Ok(()) => Refusal::R2AncestorsNotPinned,
    }
}

fn restart_without_durable_predecessor_evidence() -> Refusal {
    Refusal::R7PredecessorUnknown
}

#[test]
fn m32_p1_prefix_fresh_claim_fileid_still_stops_before_sqlite() {
    let root = Disposable::new();
    let file = root.new_main();
    let id = file_id(&file).expect("native FILE_ID_INFO on created fixture main");
    let (mut mutex, existed) = ClaimedMutex::fresh(&root.mutex_name());
    assert!(!existed);
    assert_eq!(mutex.claim(), WAIT_OBJECT_0);
    assert_eq!(observed_prefix(&root, mutex.held, &file, id), Ok(()));
    assert_eq!(next_gate_after_observation(&root, mutex.held, &file, id),
        Refusal::R2AncestorsNotPinned);
    assert_eq!(restart_without_durable_predecessor_evidence(), Refusal::R7PredecessorUnknown);
}

#[test]
fn m32_p1_prefix_file_identity_substitution_refuses_without_sqlite() {
    let root = Disposable::new();
    let original = root.new_main();
    let expected = file_id(&original).unwrap();
    drop(original);
    let moved = root.0.join("renamed-invented.sqlite3");
    fs::rename(root.main(), &moved).unwrap();
    let replacement = root.new_main();
    assert_ne!(file_id(&replacement).unwrap(), expected);
    let (mut mutex, existed) = ClaimedMutex::fresh(&root.mutex_name());
    assert!(!existed);
    assert_eq!(mutex.claim(), WAIT_OBJECT_0);
    assert_eq!(observed_prefix(&root, mutex.held, &replacement, expected),
        Err(Refusal::IdentityMismatch));
    assert_eq!(fs::read(&moved).unwrap(), Vec::<u8>::new());
}

#[test]
fn m32_p1_prefix_unknown_sidecars_refuse_and_preserve_sentinel() {
    for suffix in ["-wal", "-shm", "-journal"] {
        let root = Disposable::new();
        let file = root.new_main();
        let id = file_id(&file).unwrap();
        let sidecar = root.0.join(format!("new.sqlite3{suffix}"));
        File::create(&sidecar).unwrap().write_all(b"unknown-provenance").unwrap();
        let (mut mutex, existed) = ClaimedMutex::fresh(&root.mutex_name());
        assert!(!existed);
        assert_eq!(mutex.claim(), WAIT_OBJECT_0);
        assert_eq!(observed_prefix(&root, mutex.held, &file, id),
            Err(Refusal::Sidecar));
        assert_eq!(fs::read(&sidecar).unwrap(), b"unknown-provenance");
    }
}

#[test]
fn m32_p1_prefix_unclaimed_or_destroyed_mutex_never_attests_previous_owner() {
    let root = Disposable::new();
    let file = root.new_main();
    let id = file_id(&file).unwrap();
    let name = root.mutex_name();
    let (mut first, existed) = ClaimedMutex::fresh(&name);
    assert!(!existed);
    assert_eq!(observed_prefix(&root, first.held, &file, id),
        Err(Refusal::MutexNotClaimed));
    assert_eq!(first.claim(), WAIT_OBJECT_0);
    drop(first);
    let (mut successor, existed) = ClaimedMutex::fresh(&name);
    assert!(!existed, "a fresh free mutex cannot prove a predecessor cleanly closed SQLite");
    assert_eq!(successor.claim(), WAIT_OBJECT_0);
    assert_eq!(restart_without_durable_predecessor_evidence(),
        Refusal::R7PredecessorUnknown);
    assert_eq!(next_gate_after_observation(&root, successor.held, &file, id),
        Refusal::R2AncestorsNotPinned);
}

#[test]
fn m32_p1_prefix_rejects_path_escape_even_if_main_name_matches() {
    let root = Disposable::new();
    let file = root.new_main();
    let id = file_id(&file).unwrap();
    let (mut mutex, existed) = ClaimedMutex::fresh(&root.mutex_name());
    assert!(!existed);
    assert_eq!(mutex.claim(), WAIT_OBJECT_0);
    assert!(!safe_path(&root, &root.0.join("outside").join("new.sqlite3")));
    assert_eq!(observed_prefix(&root, mutex.held, &file, id), Ok(()));
    assert_eq!(next_gate_after_observation(&root, mutex.held, &file, id),
        Refusal::R2AncestorsNotPinned);
}
