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


// R4: FIRST actual sqlite3_io_methods v2 callback ABI test against a
// test-OWNED Win32 HANDLE. NEVER registered with sqlite3_vfs_register and
// NEVER passed to SQLite for SQL. This is NOT a working SQLite WAL VFS.
mod owned_shm_abi_refusal {
    use super::*;
    use rusqlite::ffi;
    use std::sync::atomic::{fence, Ordering};

    const LOCK:u32=2;
    const UNLOCK:u32=1;
    const SHARED:u32=4;
    const EXCLUSIVE:u32=8;

    struct CallbackOwner {
        held:Option<HeldShm>,
        held_modes:[u32;8],
        revoked:bool,
    }
    impl CallbackOwner {
        fn new(shm:HeldShm)->Self {
            Self{held:Some(shm),held_modes:[0;8],revoked:false}
        }
        fn valid(&self)->bool {
            !self.revoked && self.held.as_ref().is_some_and(|h|h.stable())
        }
    }
    #[repr(C)]
    struct CallbackFile {
        file:ffi::sqlite3_file,
        owner:*mut CallbackOwner,
    }
    unsafe fn owner<'a>(f:*mut ffi::sqlite3_file)->Option<&'a mut CallbackOwner> {
        if f.is_null(){return None}
        let ptr=unsafe{(*(f as *mut CallbackFile)).owner};
        if ptr.is_null(){return None}
        Some(unsafe{&mut *ptr})
    }
    unsafe extern "C" fn xshm_map(
        f:*mut ffi::sqlite3_file, page:i32,size:i32,extend:i32,out:*mut *mut c_void
    )->i32 {
        if out.is_null(){return ffi::SQLITE_IOERR_SHMMAP}
        unsafe{*out=ptr::null_mut()};
        let Some(o)=(unsafe{owner(f)})else{return ffi::SQLITE_IOERR_SHMMAP};
        if !o.valid() || page!=0 || size!=32768 || (extend!=0&&extend!=1) {
            return ffi::SQLITE_IOERR_SHMMAP;
        }
        unsafe{*out=o.held.as_ref().unwrap().view};
        ffi::SQLITE_OK
    }
    unsafe extern "C" fn xshm_lock(
        f:*mut ffi::sqlite3_file,index:i32,n:i32,flags:i32
    )->i32 {
        let Some(o)=(unsafe{owner(f)})else{return ffi::SQLITE_IOERR_SHMLOCK};
        // Range locking, cross-process coordination and multiple SQLite
        // connections are NOT qualified. Refuse n!=1 without stock fallback.
        if !o.valid() || !(0..=7).contains(&index) || n!=1 {
            return ffi::SQLITE_IOERR_SHMLOCK;
        }
        let flags=flags as u32;
        if ![LOCK|SHARED,LOCK|EXCLUSIVE,UNLOCK|SHARED,UNLOCK|EXCLUSIVE].contains(&flags){
            return ffi::SQLITE_IOERR_SHMLOCK;
        }
        let slot=index as usize;
        let mode=flags&(SHARED|EXCLUSIVE);
        let mut ov=offset(120+index as u32);
        let file=&o.held.as_ref().unwrap().file;
        if flags&UNLOCK!=0 {
            if o.held_modes[slot]!=mode {return ffi::SQLITE_IOERR_SHMLOCK}
            if unsafe{UnlockFileEx(file.as_raw_handle().cast(),0,1,0,&mut ov)}==0 {
                return ffi::SQLITE_IOERR_SHMLOCK;
            }
            o.held_modes[slot]=0;
            return ffi::SQLITE_OK;
        }
        if o.held_modes[slot]!=0 {return ffi::SQLITE_IOERR_SHMLOCK}
        let winflags=1|if mode==EXCLUSIVE {2}else{0};
        if unsafe{LockFileEx(file.as_raw_handle().cast(),winflags,0,1,0,&mut ov)}==0 {
            return if std::io::Error::last_os_error().raw_os_error()==Some(33) {
                ffi::SQLITE_BUSY
            }else{ffi::SQLITE_IOERR_SHMLOCK};
        }
        o.held_modes[slot]=mode;
        ffi::SQLITE_OK
    }
    unsafe extern "C" fn xshm_barrier(_f:*mut ffi::sqlite3_file){
        // Void ABI: no async veto. Owner admission must precede invocation.
        fence(Ordering::SeqCst);
    }
    unsafe extern "C" fn xshm_unmap(f:*mut ffi::sqlite3_file,delete_flag:i32)->i32 {
        let Some(o)=(unsafe{owner(f)})else{return ffi::SQLITE_IOERR_SHMMAP};
        if !o.valid()||delete_flag!=0 {return ffi::SQLITE_IOERR_SHMMAP}
        if o.held_modes.iter().any(|mode|*mode!=0){return ffi::SQLITE_BUSY}
        // Drop the exact native map and HANDLE only after last valid lock.
        o.held.take();
        o.revoked=true;
        ffi::SQLITE_OK
    }
    struct AbiTable {
        _methods:Box<ffi::sqlite3_io_methods>,
        file:CallbackFile,
    }
    impl AbiTable {
        fn new(state:&mut CallbackOwner)->Self {
            // Never given to SQLite core! xClose/xRead/etc remain NULL.
            // Only v2 SHM callbacks are directly exercised by tests.
            let mut m=Box::new(unsafe{std::mem::zeroed::<ffi::sqlite3_io_methods>()});
            m.iVersion=2;
            m.xShmMap=Some(xshm_map);
            m.xShmLock=Some(xshm_lock);
            m.xShmBarrier=Some(xshm_barrier);
            m.xShmUnmap=Some(xshm_unmap);
            let file=CallbackFile{
                file:ffi::sqlite3_file{pMethods:m.as_ref()},
                owner:state as *mut CallbackOwner,
            };
            Self{_methods:m,file}
        }
        fn ptr(&mut self)->*mut ffi::sqlite3_file{&mut self.file.file}
    }

    #[test]
    fn r4_xshm_abi_held_handle_shared_exclusive_contention_and_map_refusal() {
        let root=ScratchDir::new();
        let path=root.0.join("scratch-shm");
        let mut o=CallbackOwner::new(HeldShm::new(&path));
        let competitor=OpenOptions::new().read(true).write(true).share_mode(1|2|4)
            .open(&path).expect("same disposable SHM, no operator");
        let mut api=AbiTable::new(&mut o);
        let p=api.ptr();
        let mut output:*mut c_void=ptr::null_mut();
        assert_eq!(unsafe{xshm_map(p,0,32768,1,&mut output)},ffi::SQLITE_OK);
        assert!(!output.is_null());
        assert_eq!(unsafe{xshm_map(p,1,32768,1,&mut output)},ffi::SQLITE_IOERR_SHMMAP);
        assert!(output.is_null());
        assert_eq!(unsafe{xshm_lock(p,0,1,(LOCK|SHARED) as i32)},ffi::SQLITE_OK);
        assert!(!try_exclusive(&competitor,120),"shared lock prevents competitor exclusive");
        assert_eq!(unsafe{xshm_lock(p,0,1,(UNLOCK|SHARED) as i32)},ffi::SQLITE_OK);
        assert!(try_exclusive(&competitor,120));
        unlock(&competitor,120);
        assert_eq!(unsafe{xshm_lock(p,7,1,(LOCK|EXCLUSIVE) as i32)},ffi::SQLITE_OK);
        unsafe{xshm_barrier(p)};
        assert_eq!(unsafe{xshm_lock(p,7,1,(UNLOCK|EXCLUSIVE) as i32)},ffi::SQLITE_OK);
        assert_eq!(unsafe{xshm_unmap(p,0)},ffi::SQLITE_OK);
        drop(competitor);
    }

    #[test]
    fn r4_xshm_abi_invalid_flags_locked_unmap_delete_and_stale_epoch_refusal() {
        let root=ScratchDir::new();
        let mut o=CallbackOwner::new(HeldShm::new(&root.0.join("only-scratch-shm")));
        let mut api=AbiTable::new(&mut o);
        let p=api.ptr();
        let mut output=1usize as *mut c_void;
        assert_eq!(unsafe{xshm_map(p,0,1024,1,&mut output)},ffi::SQLITE_IOERR_SHMMAP);
        assert!(output.is_null());
        assert_eq!(unsafe{xshm_lock(p,8,1,(LOCK|SHARED) as i32)},ffi::SQLITE_IOERR_SHMLOCK);
        assert_eq!(unsafe{xshm_lock(p,0,2,(LOCK|SHARED) as i32)},ffi::SQLITE_IOERR_SHMLOCK);
        assert_eq!(unsafe{xshm_lock(p,0,1,(LOCK|SHARED|EXCLUSIVE) as i32)},ffi::SQLITE_IOERR_SHMLOCK);
        assert_eq!(unsafe{xshm_lock(p,0,1,(UNLOCK|SHARED) as i32)},ffi::SQLITE_IOERR_SHMLOCK);
        assert_eq!(unsafe{xshm_lock(p,0,1,(LOCK|EXCLUSIVE) as i32)},ffi::SQLITE_OK);
        assert_eq!(unsafe{xshm_unmap(p,0)},ffi::SQLITE_BUSY);
        assert_eq!(unsafe{xshm_lock(p,0,1,(UNLOCK|SHARED) as i32)},ffi::SQLITE_IOERR_SHMLOCK);
        assert_eq!(unsafe{xshm_lock(p,0,1,(UNLOCK|EXCLUSIVE) as i32)},ffi::SQLITE_OK);
        assert_eq!(unsafe{xshm_unmap(p,1)},ffi::SQLITE_IOERR_SHMMAP);
        assert_eq!(unsafe{xshm_unmap(p,0)},ffi::SQLITE_OK);
        assert_eq!(unsafe{xshm_map(p,0,32768,1,&mut output)},ffi::SQLITE_IOERR_SHMMAP);
        assert!(output.is_null());
        assert_eq!(unsafe{xshm_lock(p,0,1,(LOCK|SHARED) as i32)},ffi::SQLITE_IOERR_SHMLOCK);
    }
}
