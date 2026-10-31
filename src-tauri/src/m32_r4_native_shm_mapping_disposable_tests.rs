//! R4: native Win32 HANDLE->file-mapping proof on newly created, disposable SHM-like files.
//! NOT SQLite xShmMap, NOT atomic main/WAL/SHM custody and NOT writer admission.
use std::{
    ffi::c_void,
    fs::{self, File, OpenOptions},
    os::windows::{fs::OpenOptionsExt, io::AsRawHandle},
    path::PathBuf, process, ptr::{self, NonNull},
    sync::atomic::{AtomicUsize, Ordering},
    time::{SystemTime, UNIX_EPOCH},
};

const PREFIX: &str = "fabulaxiom-r4-held-shm-mapping-";
const FILE_ID_INFO_CLASS: i32 = 0x12;
const PAGE_READWRITE: u32 = 0x04;
const FILE_MAP_WRITE: u32 = 0x0002;
const MAP_SIZE: usize = 4096;

#[repr(C)]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
struct FileIdInfo { volume: u64, file_id: [u8; 16] }

#[link(name = "kernel32")]
unsafe extern "system" {
    fn GetFileInformationByHandleEx(handle: *mut c_void, class: i32,
        info: *mut c_void, size: u32) -> i32;
    fn CreateFileMappingW(handle: *mut c_void, attributes: *mut c_void,
        protect: u32, maximum_high: u32, maximum_low: u32, name: *const u16) -> *mut c_void;
    fn MapViewOfFile(mapping: *mut c_void, access: u32,
        offset_high: u32, offset_low: u32, bytes: usize) -> *mut c_void;
    fn UnmapViewOfFile(address: *const c_void) -> i32;
    fn CloseHandle(handle: *mut c_void) -> i32;
}

fn file_id_from_held(file: &File) -> FileIdInfo {
    let mut info = std::mem::MaybeUninit::<FileIdInfo>::uninit();
    let ok = unsafe {
        GetFileInformationByHandleEx(file.as_raw_handle().cast(), FILE_ID_INFO_CLASS,
            info.as_mut_ptr().cast(), std::mem::size_of::<FileIdInfo>() as u32)
    };
    assert_ne!(ok, 0, "FileId128 must come from the same held native HANDLE");
    unsafe { info.assume_init() }
}

struct OwnedFixture(PathBuf);
impl OwnedFixture {
    fn new() -> Self {
        static SEQUENCE: AtomicUsize = AtomicUsize::new(0);
        let tick = SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_nanos();
        let path = std::env::temp_dir().join(format!("{PREFIX}{}-{tick}-{}",
            process::id(), SEQUENCE.fetch_add(1, Ordering::Relaxed)));
        fs::create_dir(&path).expect("new test-owned TEMP directory only");
        Self(path)
    }
    fn new_shm(&self, name: &str) -> File {
        assert!(name.ends_with("-shm"), "only invented SHM-like test files");
        let file = OpenOptions::new().read(true).write(true).create_new(true)
            .share_mode(1 | 2 | 4).open(self.0.join(name))
            .expect("CREATE_NEW test-owned file only");
        file.set_len(MAP_SIZE as u64).expect("size test-only SHM file");
        file
    }
}
impl Drop for OwnedFixture {
    fn drop(&mut self) {
        assert!(self.0.starts_with(std::env::temp_dir()));
        assert!(self.0.file_name().unwrap().to_string_lossy().starts_with(PREFIX));
        fs::remove_dir_all(&self.0).expect("only remove test-owned TEMP root");
    }
}

struct HeldFileMapping { mapping: NonNull<c_void>, view: NonNull<c_void> }
impl HeldFileMapping {
    fn create_using_same_handle(held: &File) -> Self {
        // No independent reopen-by-name: CreateFileMappingW receives this File's held HANDLE.
        let mapping = unsafe { CreateFileMappingW(
            held.as_raw_handle().cast(), ptr::null_mut(), PAGE_READWRITE,
            0, 0, ptr::null()
        ) };
        let mapping = NonNull::new(mapping).expect("native mapping from held HANDLE");
        let view = unsafe { MapViewOfFile(mapping.as_ptr(), FILE_MAP_WRITE, 0, 0, MAP_SIZE) };
        let Some(view) = NonNull::new(view) else {
            assert_ne!(unsafe { CloseHandle(mapping.as_ptr()) }, 0);
            panic!("MapViewOfFile failed for test-held HANDLE");
        };
        Self { mapping, view }
    }
    fn exercise(&self) {
        let ptr = self.view.as_ptr().cast::<u8>();
        unsafe {
            ptr::write_volatile(ptr, 0x6d);
            assert_eq!(ptr::read_volatile(ptr), 0x6d);
        }
    }
}
impl Drop for HeldFileMapping {
    fn drop(&mut self) {
        assert_ne!(unsafe { UnmapViewOfFile(self.view.as_ptr()) }, 0);
        assert_ne!(unsafe { CloseHandle(self.mapping.as_ptr()) }, 0);
    }
}

#[test]
fn r4_native_mapping_from_held_shm_has_stable_fileid128_through_mapping() {
    let fixture = OwnedFixture::new();
    let held = fixture.new_shm("invented.sqlite3-shm");
    let before = file_id_from_held(&held);
    let mapping = HeldFileMapping::create_using_same_handle(&held);
    mapping.exercise();
    assert_eq!(before, file_id_from_held(&held));
    drop(mapping);
    drop(held);
}

#[test]
fn r4_native_mapping_from_held_shm_does_not_confuse_another_fileid128() {
    let fixture = OwnedFixture::new();
    let held = fixture.new_shm("invented.sqlite3-shm");
    let other = fixture.new_shm("other.sqlite3-shm");
    let before = file_id_from_held(&held);
    let mapping = HeldFileMapping::create_using_same_handle(&held);
    mapping.exercise();
    assert_ne!(before, file_id_from_held(&other));
    assert_eq!(before, file_id_from_held(&held));
    drop(mapping);
    drop(other);
    drop(held);
}
