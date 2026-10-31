//! R4 stock Win32 SQLite VFS reference ONLY: a fresh disposable %TEMP% fixture.
//! NOT the preopened R3 VFS, xShm* admission, operator data or runtime writer.
use rusqlite::{Connection, OpenFlags};
use std::{
    ffi::c_void, fs::{self, File, OpenOptions},
    os::windows::{fs::OpenOptionsExt, io::AsRawHandle},
    path::{Path, PathBuf}, process,
    sync::atomic::{AtomicUsize, Ordering},
    time::{SystemTime, UNIX_EPOCH},
};
const PREFIX: &str = "fabulaxiom-r4-default-win32-fixture-";
type Identity = (u64, [u8; 16]);
#[repr(C)] struct FileIdInfo { volume: u64, id: [u8; 16] }
#[link(name="kernel32")]
unsafe extern "system" {
    fn GetFileInformationByHandleEx(file:*mut c_void,class:i32,info:*mut c_void,size:u32)->i32;
    fn CreateFileMappingW(file:*mut c_void, attr:*mut c_void, protect:u32, hi:u32, lo:u32, name:*const u16)->*mut c_void;
    fn MapViewOfFile(mapping:*mut c_void, access:u32, hi:u32, lo:u32, bytes:usize)->*mut c_void;
    fn UnmapViewOfFile(view:*const c_void)->i32;
    fn CloseHandle(h:*mut c_void)->i32;
}
struct OwnedFixture(PathBuf);
impl OwnedFixture {
    fn new()->Self {
        static SEQ:AtomicUsize=AtomicUsize::new(0);
        let tick=SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_nanos();
        let root=std::env::temp_dir().join(format!("{PREFIX}{}-{tick}-{}",
            process::id(),SEQ.fetch_add(1,Ordering::Relaxed)));
        fs::create_dir(&root).expect("create new fixture root");
        Self(root)
    }
    fn main(&self)->PathBuf {self.0.join("invented.sqlite3")}
    fn sidecar(&self,suffix:&str)->PathBuf {self.0.join(format!("invented.sqlite3{suffix}"))}
    fn create_fresh_main(&self) {
        let file=OpenOptions::new().read(true).write(true).create_new(true)
            .open(self.main()).expect("CREATE_NEW only in new fixture root");
        drop(file);
    }
}
impl Drop for OwnedFixture {
    fn drop(&mut self) {
        assert!(self.0.starts_with(std::env::temp_dir()));
        assert!(self.0.file_name().unwrap().to_string_lossy().starts_with(PREFIX));
        fs::remove_dir_all(&self.0).expect("remove only owned fixture");
    }
}
fn pinned_identity(path:&Path)->Identity {
    let file:File=OpenOptions::new().read(true).share_mode(1|2|4)
        .open(path).expect("CI-owned file only");
    let mut info=std::mem::MaybeUninit::<FileIdInfo>::uninit();
    let ok=unsafe{GetFileInformationByHandleEx(file.as_raw_handle().cast(),0x12,
        info.as_mut_ptr().cast(),std::mem::size_of::<FileIdInfo>() as u32)};
    assert_ne!(ok,0,"FileId128 must be observable");
    let info=unsafe{info.assume_init()};
    (info.volume,info.id)
}
// Only a live SQLite-created disposable SHM file; this is not the opaque
// handle internally mapped by sqlite3_io_methods.xShmMap.
fn observe_live_sqlite_shm_readonly_view(shm: &Path) {
    let held = OpenOptions::new().read(true).share_mode(1|2|4)
        .open(shm).expect("fresh SQLite-owned WAL-index only");
    assert!(held.metadata().unwrap().len() >= 136);
    let file_id = || {
        let mut info = std::mem::MaybeUninit::<FileIdInfo>::uninit();
        let ok = unsafe { GetFileInformationByHandleEx(
            held.as_raw_handle().cast(), 0x12, info.as_mut_ptr().cast(),
            std::mem::size_of::<FileIdInfo>() as u32) };
        assert_ne!(ok, 0);
        let info = unsafe { info.assume_init() };
        (info.volume, info.id)
    };
    let before = file_id();
    let mapping = unsafe { CreateFileMappingW(held.as_raw_handle().cast(),
        std::ptr::null_mut(), 0x02, 0, 0, std::ptr::null()) };
    assert!(!mapping.is_null(), "PAGE_READONLY mapping on held fixture SHM");
    let view = unsafe { MapViewOfFile(mapping, 0x0004, 0, 0, 136) };
    if view.is_null() {
        assert_ne!(unsafe { CloseHandle(mapping) }, 0);
        panic!("FILE_MAP_READ on live WAL-index");
    }
    let version = unsafe { std::ptr::read_unaligned(view.cast::<u32>()) };
    let copy_version = unsafe {
        std::ptr::read_unaligned(view.cast::<u8>().add(48).cast::<u32>())
    };
    let is_init = unsafe { std::ptr::read_volatile(view.cast::<u8>().add(12)) };
    assert_ne!(unsafe { UnmapViewOfFile(view) }, 0);
    assert_ne!(unsafe { CloseHandle(mapping) }, 0);
    assert_eq!(version, 3_007_000);
    assert_eq!(copy_version, 3_007_000);
    assert_eq!(is_init, 1);
    assert_eq!(before, file_id(), "held native FileId128 remains stable");
}

#[test]
fn m32_r4_default_win32_wal_shm_sidecar_identity_and_reader_snapshot_disposable() {
    let owned=OwnedFixture::new();
    owned.create_fresh_main();
    let main=owned.main();
    let wal=owned.sidecar("-wal");
    let shm=owned.sidecar("-shm");
    // All test-only SQLite reads and writes use the stock Win32 VFS.
    let writer=Connection::open(&main).expect("fresh test-only SQLite writer");
    let mode:String=writer.query_row("PRAGMA journal_mode=WAL",[],|r|r.get(0)).unwrap();
    assert_eq!(mode.to_ascii_lowercase(),"wal");
    writer.execute_batch("PRAGMA wal_autocheckpoint=0;
        CREATE TABLE invented_r4 (value INTEGER NOT NULL);
        INSERT INTO invented_r4(value) VALUES (1);").unwrap();
    let reader=Connection::open_with_flags(&main,OpenFlags::SQLITE_OPEN_READ_ONLY)
        .expect("test-only WAL reader");
    reader.execute_batch("BEGIN").unwrap();
    let first:i64=reader.query_row("SELECT COUNT(*) FROM invented_r4",[],|r|r.get(0)).unwrap();
    assert_eq!(first,1);
    writer.execute("INSERT INTO invented_r4(value) VALUES (2)",[]).unwrap();
    let old:i64=reader.query_row("SELECT COUNT(*) FROM invented_r4",[],|r|r.get(0)).unwrap();
    assert_eq!(old,1,"reader end-mark must remain unchanged after writer commit");
    let writer_count:i64=writer.query_row("SELECT COUNT(*) FROM invented_r4",[],|r|r.get(0)).unwrap();
    assert_eq!(writer_count,2);
    assert!(fs::metadata(&wal).unwrap().len()>0);
    assert!(fs::metadata(&shm).unwrap().len()>0);
    let main_id=pinned_identity(&main);
    let wal_id=pinned_identity(&wal);
    let shm_id=pinned_identity(&shm);
    assert_eq!(pinned_identity(&main),main_id);
    assert_eq!(pinned_identity(&wal),wal_id);
    assert_eq!(pinned_identity(&shm),shm_id);
    assert_ne!(main_id,wal_id);
    assert_ne!(main_id,shm_id);
    assert_ne!(wal_id,shm_id);
    observe_live_sqlite_shm_readonly_view(&shm);
    reader.execute_batch("COMMIT").unwrap();
    let new:i64=reader.query_row("SELECT COUNT(*) FROM invented_r4",[],|r|r.get(0)).unwrap();
    assert_eq!(new,2);
    drop(reader);
    drop(writer);
    // These observations are NOT custom xShm*, atomic custody, R4, or recovery admission.
}
