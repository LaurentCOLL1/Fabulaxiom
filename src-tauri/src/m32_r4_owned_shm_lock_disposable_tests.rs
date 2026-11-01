//! Windows-only test: one test-owned SHM HANDLE backs both mmap and lock domain.
//! NOT a SQLite xShm* VFS, not SQLite's private handle, not production admission.
use std::{ffi::c_void, fs::{self, File, OpenOptions}, ptr,
    os::windows::{fs::{FileExt,OpenOptionsExt},io::AsRawHandle},
    path::{Path,PathBuf},process,time::{SystemTime,UNIX_EPOCH}};
#[repr(C)]
struct FileIdInfo {volume:u64,id:[u8;16]}
#[repr(C)]
struct Overlapped {internal:usize,internal_high:usize,offset:u32,offset_high:u32,event:*mut c_void}
#[link(name="kernel32")]
unsafe extern "system" {
    fn GetFileInformationByHandleEx(h:*mut c_void,class:i32,out:*mut c_void,size:u32)->i32;
    fn LockFileEx(h:*mut c_void,flags:u32,reserved:u32,low:u32,high:u32,ov:*mut Overlapped)->i32;
    fn UnlockFileEx(h:*mut c_void,reserved:u32,low:u32,high:u32,ov:*mut Overlapped)->i32;
    fn CreateFileMappingW(h:*mut c_void,attrs:*mut c_void,protection:u32,
        high:u32,low:u32,name:*const u16)->*mut c_void;
    fn MapViewOfFile(h:*mut c_void,access:u32,high:u32,low:u32,size:usize)->*mut c_void;
    fn UnmapViewOfFile(view:*const c_void)->i32;
    fn CloseHandle(h:*mut c_void)->i32;
}
fn file_id(f:&File)->(u64,[u8;16]){
    let mut info=std::mem::MaybeUninit::<FileIdInfo>::uninit();
    let ok=unsafe{GetFileInformationByHandleEx(f.as_raw_handle().cast(),18,
        info.as_mut_ptr().cast(),std::mem::size_of::<FileIdInfo>() as u32)};
    assert_ne!(ok,0,"complete FileIdInfo must be available for fixture");
    let i=unsafe{info.assume_init()};
    (i.volume,i.id)
}
fn offset(b:u32)->Overlapped{
    Overlapped{internal:0,internal_high:0,offset:b,offset_high:0,event:ptr::null_mut()}
}
fn lock(f:&File,b:u32)->bool{
    assert!((120..=127).contains(&b),"WAL-index lock bytes only");
    let mut ov=offset(b);
    // EXCLUSIVE|FAIL_IMMEDIATELY, never an async wait / hidden recovery.
    unsafe{LockFileEx(f.as_raw_handle().cast(),0x02|0x01,0,1,0,&mut ov)!=0}
}
fn unlock(f:&File,b:u32){
    let mut ov=offset(b);
    assert_ne!(unsafe{UnlockFileEx(f.as_raw_handle().cast(),0,1,0,&mut ov)},0);
}
struct ScratchDir(PathBuf);
impl ScratchDir {
    fn new()->Self{
        let n=SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_nanos();
        let p=std::env::temp_dir().join(format!("fabulaxiom-owned-shm-test-{}-{n}",process::id()));
        fs::create_dir(&p).expect("new disposable per-test %TEMP% only");
        Self(p)
    }
}
impl Drop for ScratchDir{fn drop(&mut self){fs::remove_dir_all(&self.0).expect("scratch cleanup");}}
struct HeldShm{file:File,id:(u64,[u8;16]),mapping:*mut c_void,view:*mut c_void}
impl HeldShm{
    fn new(path:&Path)->Self{
        let file=OpenOptions::new().read(true).write(true).share_mode(1|2|4)
            .create_new(true).open(path).expect("fresh fixture CREATE_NEW");
        file.set_len(32768).unwrap();
        let id=file_id(&file);
        let mapping=unsafe{CreateFileMappingW(file.as_raw_handle().cast(),
            ptr::null_mut(),0x04,0,0,ptr::null())};
        assert!(!mapping.is_null(),"PAGE_READWRITE from held native HANDLE");
        let view=unsafe{MapViewOfFile(mapping,0x0002|0x0004,0,0,32768)};
        if view.is_null(){
            assert_ne!(unsafe{CloseHandle(mapping)},0);
            panic!("FAIL CLOSED: held SHM mapping unavailable");
        }
        Self{file,id,mapping,view}
    }
    fn stable(&self)->bool{file_id(&self.file)==self.id}
}
impl Drop for HeldShm{
    fn drop(&mut self){
        assert_ne!(unsafe{UnmapViewOfFile(self.view.cast_const())},0);
        assert_ne!(unsafe{CloseHandle(self.mapping)},0);
        // File drop then releases the one owned HANDLE.
    }
}
#[test]
fn r4_owned_shm_same_handle_maps_and_contends_on_wal_lock_byte(){
    let dir=ScratchDir::new();
    let p=dir.0.join("synthetic-shm");
    let owner=HeldShm::new(&p);
    assert!(owner.stable());
    unsafe{ptr::write_volatile(owner.view.cast::<u8>(),0x5a)};
    let mut byte=[0u8];
    assert_eq!(owner.file.seek_read(&mut byte,0).unwrap(),1);
    assert_eq!(byte,[0x5a]);
    let competitor=OpenOptions::new().read(true).write(true).share_mode(1|2|4).open(&p).unwrap();
    assert_eq!(file_id(&competitor),owner.id);
    assert!(lock(&owner.file,120));
    assert!(!lock(&competitor,120),"second HANDLE cannot acquire exclusive same-file byte");
    assert!(lock(&competitor,121),"different WAL index byte remains independent");
    unlock(&competitor,121);
    unlock(&owner.file,120);
    assert!(lock(&competitor,120));
    unlock(&competitor,120);
    assert!(owner.stable());
    drop(competitor);
    drop(owner);
}
#[test]
fn r4_equal_bytes_different_fileid_shm_decoy_has_separate_lock_domain(){
    let dir=ScratchDir::new();
    let owner=HeldShm::new(&dir.0.join("real-fixture-shm"));
    let decoy=HeldShm::new(&dir.0.join("same-bytes-decoy"));
    let header=[0x35u8;136];
    unsafe{
        ptr::copy_nonoverlapping(header.as_ptr(),owner.view.cast(),136);
        ptr::copy_nonoverlapping(header.as_ptr(),decoy.view.cast(),136);
    }
    let mut a=[0u8;136];let mut b=[0u8;136];
    assert_eq!(owner.file.seek_read(&mut a,0).unwrap(),136);
    assert_eq!(decoy.file.seek_read(&mut b,0).unwrap(),136);
    assert_eq!(a,b);
    assert_ne!(owner.id,decoy.id);
    assert!(lock(&owner.file,120));
    assert!(lock(&decoy.file,120),"equal bytes do NOT share lock domain");
    unlock(&decoy.file,120);
    unlock(&owner.file,120);
    assert!(owner.stable()&&decoy.stable());
    // No SQLite xShmMap callback, native Hello, operator profile or writer.
}
