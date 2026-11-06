//! R4: REGISTERED test-only SQLite VFS binding NORMAL WAL xShm* to held Win32
//! SHM native HANDLE. Fresh %TEMP% fixtures; default VFS xOpen only for the
//! invented database/WAL/journal. NEVER operator data or production IPC.
//! NOT atomic main/WAL/SHM custody, no production registration, no writer gate.
use rusqlite::{ffi,Connection,OpenFlags};
use std::{ffi::{c_int,c_void,CStr,CString},fs::{self,File,OpenOptions},
    os::windows::{fs::OpenOptionsExt,io::AsRawHandle},path::{Path,PathBuf},
    ptr,sync::atomic::{AtomicBool,AtomicUsize,Ordering,fence},time::{SystemTime,UNIX_EPOCH},process};

#[repr(C)]
#[derive(Clone,Copy,Debug,PartialEq,Eq)]
struct FileIdInfo{volume:u64,id:[u8;16]}
#[repr(C)]
struct Overlapped{internal:usize,internal_high:usize,offset:u32,offset_high:u32,event:*mut c_void}
#[link(name="kernel32")]
unsafe extern "system"{
    fn GetFileInformationByHandleEx(h:*mut c_void,class:i32,out:*mut c_void,size:u32)->i32;
    fn CreateFileMappingW(h:*mut c_void,attrs:*mut c_void,protection:u32,
        high:u32,low:u32,name:*const u16)->*mut c_void;
    fn MapViewOfFile(h:*mut c_void,access:u32,high:u32,low:u32,size:usize)->*mut c_void;
    fn UnmapViewOfFile(view:*const c_void)->i32;
    fn CloseHandle(h:*mut c_void)->i32;
    fn LockFileEx(h:*mut c_void,flags:u32,reserved:u32,low:u32,high:u32,ov:*mut Overlapped)->i32;
    fn UnlockFileEx(h:*mut c_void,reserved:u32,low:u32,high:u32,ov:*mut Overlapped)->i32;
}
fn id(file:&File)->Option<FileIdInfo>{
    let mut v=std::mem::MaybeUninit::<FileIdInfo>::uninit();
    let ok=unsafe{GetFileInformationByHandleEx(file.as_raw_handle().cast(),18,
        v.as_mut_ptr().cast(),std::mem::size_of::<FileIdInfo>() as u32)};
    (ok!=0).then(||unsafe{v.assume_init()})
}
fn raw_id(handle:*mut c_void)->Option<FileIdInfo>{
    if handle.is_null(){return None}
    let mut v=std::mem::MaybeUninit::<FileIdInfo>::uninit();
    let ok=unsafe{GetFileInformationByHandleEx(handle,18,
        v.as_mut_ptr().cast(),std::mem::size_of::<FileIdInfo>() as u32)};
    (ok!=0).then(||unsafe{v.assume_init()})
}
fn ov(byte:u32)->Overlapped{
    Overlapped{internal:0,internal_high:0,offset:byte,offset_high:0,event:ptr::null_mut()}
}
const PAGE_SIZE:usize=32768;
// CI-only bounded SHM mapping: exactly two 32-KiB pages, never unlimited or runtime.
const SHM_REGION_COUNT:usize=2;
const SHM_MAPPING_BYTES:usize=PAGE_SIZE*SHM_REGION_COUNT;
const SHM_LOCK:u32=2;
const SHM_UNLOCK:u32=1;
const SHM_SHARED:u32=4;
const SHM_EXCLUSIVE:u32=8;
const PREFIX:&str="fabulaxiom-r4-registered-owned-shm-";

struct Scratch{dir:PathBuf,db:PathBuf,shm:PathBuf}
impl Scratch{
    fn fresh()->Self{
        let tick=SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_nanos();
        let dir=std::env::temp_dir().join(format!("{PREFIX}{}-{tick}",process::id()));
        fs::create_dir(&dir).expect("fresh disposable TEMP root");
        let db=dir.join("invented.sqlite3");
        let shm=dir.join("invented.sqlite3-shm");
        for p in [&db,&shm]{
            let f=OpenOptions::new().read(true).write(true).share_mode(1|2|4)
                .create_new(true).open(p).expect("CREATE_NEW only");
            if p==&shm {f.set_len(SHM_MAPPING_BYTES as u64).unwrap();}
        }
        Self{dir,db,shm}
    }
}
impl Drop for Scratch{
    fn drop(&mut self){
        assert!(self.dir.starts_with(std::env::temp_dir()));
        assert!(self.dir.file_name().unwrap().to_string_lossy().starts_with(PREFIX));
        fs::remove_dir_all(&self.dir).expect("fresh TEMP cleanup only");
    }
}
struct View{mapping:*mut c_void,view:*mut c_void}
impl View{
    fn from_held(held:&File)->Option<Self>{
        let mapping=unsafe{CreateFileMappingW(held.as_raw_handle().cast(),
            ptr::null_mut(),4,0,0,ptr::null())};
        if mapping.is_null(){return None}
        let view=unsafe{MapViewOfFile(mapping,2|4,0,0,SHM_MAPPING_BYTES)};
        if view.is_null(){
            let _=unsafe{CloseHandle(mapping)};
            return None;
        }
        Some(Self{mapping,view})
    }
}
impl Drop for View{
    fn drop(&mut self){
        assert_ne!(unsafe{UnmapViewOfFile(self.view.cast_const())},0);
        assert_ne!(unsafe{CloseHandle(self.mapping)},0);
    }
}
struct ShmState{held:File,expected:FileIdInfo,path:PathBuf,view:View,modes:[u32;8],poisoned:bool}
impl ShmState{
    fn new(held:File,expected:FileIdInfo,path:PathBuf)->Option<Self>{
        if id(&held)!=Some(expected){return None}
        let view=View::from_held(&held)?;
        Some(Self{held,expected,path,view,modes:[0;8],poisoned:false})
    }
    fn valid(&mut self)->bool{
        // A mismatched or missing SHM pathname must poison this SQLite file
        // permanently: returning the old name later must NOT re-arm xShm*.
        // This still does not remove TOCTOU between successive callbacks.
        if self.poisoned{return false}
        let held_ok=id(&self.held)==Some(self.expected);
        let named_ok=OpenOptions::new().read(true).write(true).share_mode(1|2|4)
            .open(&self.path).ok().and_then(|fresh|id(&fresh))==Some(self.expected);
        if !(held_ok&&named_ok){self.poisoned=true;return false}
        true
    }
}
#[repr(C)]
struct Vfs{
    dispatch:ffi::sqlite3_vfs,
    default:*mut ffi::sqlite3_vfs,
    root:PathBuf,
    shm:PathBuf,
    master:File,
    expected:FileIdInfo,
    master_db:File,
    expected_db:FileIdInfo,
    // Test-only fault flags allow native xOpen HANDLE veto without name swaps.
    deny_main_native_id_for_test:AtomicBool,
    deny_wal_native_id_for_test:AtomicBool,
    // SQLite's WAL xOpen provides the associated live main sqlite3_file.
    deny_wal_main_owner_for_test:AtomicBool,
    wal_main_owner_matches:AtomicUsize,
    main_native_matches:AtomicUsize,
    wal_native_matches:AtomicUsize,
    native_refusals:AtomicUsize,
    tail_offset:usize,
    main_opens:AtomicUsize,
    shm_maps:AtomicUsize,
    shm_locks:AtomicUsize,
    shm_unmaps:AtomicUsize,
    deletes_requested:AtomicUsize,
    closes:AtomicUsize,
    denials:AtomicUsize,
}
#[repr(C)]
struct FileTail{
    methods:ffi::sqlite3_io_methods,
    original:*const ffi::sqlite3_io_methods,
    gate:*const Vfs,
    shm_state:*mut ShmState,
}
unsafe fn tail<'a>(file:*mut ffi::sqlite3_file)->Option<&'a mut FileTail>{
    if file.is_null(){return None}
    let methods=unsafe{(*file).pMethods};
    if methods.is_null(){return None}
    Some(unsafe{&mut *(methods as *mut FileTail)})
}
unsafe extern "C" fn xshm_map(
    file:*mut ffi::sqlite3_file,page:c_int,sz:c_int,extend:c_int,out:*mut *mut c_void
)->c_int{
    if out.is_null(){return ffi::SQLITE_IOERR_SHMMAP}
    unsafe{*out=ptr::null_mut()};
    let Some(t)=(unsafe{tail(file)})else{return ffi::SQLITE_IOERR_SHMMAP};
    if t.shm_state.is_null(){return ffi::SQLITE_IOERR_SHMMAP}
    let held=unsafe{&mut *t.shm_state};
    let gate=unsafe{&*t.gate};
    if !held.valid()||page<0||page as usize>=SHM_REGION_COUNT
        ||sz!=PAGE_SIZE as c_int||(extend!=0&&extend!=1){
        gate.denials.fetch_add(1,Ordering::SeqCst);
        return ffi::SQLITE_IOERR_SHMMAP;
    }
    gate.shm_maps.fetch_add(1,Ordering::SeqCst);
    // One held FileId128 backs both regions; pointer stays within the 64-KiB view.
    unsafe{*out=held.view.view.cast::<u8>().add(page as usize*PAGE_SIZE).cast()};
    ffi::SQLITE_OK
}
unsafe extern "C" fn xshm_lock(
    file:*mut ffi::sqlite3_file,index:c_int,n:c_int,flags:c_int
)->c_int{
    let Some(t)=(unsafe{tail(file)})else{return ffi::SQLITE_IOERR_SHMLOCK};
    if t.shm_state.is_null(){return ffi::SQLITE_IOERR_SHMLOCK}
    let s=unsafe{&mut *t.shm_state};
    let gate=unsafe{&*t.gate};
    let f=flags as u32;
    let supported=[SHM_LOCK|SHM_SHARED,SHM_LOCK|SHM_EXCLUSIVE,
        SHM_UNLOCK|SHM_SHARED,SHM_UNLOCK|SHM_EXCLUSIVE].contains(&f);
    if !s.valid()||index<0||n<1||index.checked_add(n).is_none_or(|end|end>8)
        ||!supported || (f&SHM_SHARED!=0 && n!=1){
        gate.denials.fetch_add(1,Ordering::SeqCst);
        return ffi::SQLITE_IOERR_SHMLOCK;
    }
    let low=index as usize;
    let high=(index+n) as usize;
    let mode=f&(SHM_SHARED|SHM_EXCLUSIVE);
    let mut overlap=ov(120+index as u32);
    if f&SHM_UNLOCK!=0{
        if s.modes[low..high].iter().any(|m|*m!=mode){
            gate.denials.fetch_add(1,Ordering::SeqCst);
            return ffi::SQLITE_IOERR_SHMLOCK;
        }
        let rc=unsafe{UnlockFileEx(s.held.as_raw_handle().cast(),0,n as u32,0,&mut overlap)};
        if rc==0{return ffi::SQLITE_IOERR_SHMLOCK}
        s.modes[low..high].fill(0);
        return ffi::SQLITE_OK;
    }
    if s.modes[low..high].iter().any(|m|*m!=0){
        gate.denials.fetch_add(1,Ordering::SeqCst);
        return ffi::SQLITE_IOERR_SHMLOCK;
    }
    let win_flags=1|if mode==SHM_EXCLUSIVE{2}else{0};
    let rc=unsafe{LockFileEx(s.held.as_raw_handle().cast(),win_flags,0,n as u32,0,&mut overlap)};
    if rc==0{
        return if std::io::Error::last_os_error().raw_os_error()==Some(33){
            ffi::SQLITE_BUSY
        } else {ffi::SQLITE_IOERR_SHMLOCK};
    }
    s.modes[low..high].fill(mode);
    gate.shm_locks.fetch_add(1,Ordering::SeqCst);
    ffi::SQLITE_OK
}
unsafe extern "C" fn xshm_barrier(_file:*mut ffi::sqlite3_file){fence(Ordering::SeqCst)}
unsafe extern "C" fn xshm_unmap(file:*mut ffi::sqlite3_file,delete_flag:c_int)->c_int{
    let Some(t)=(unsafe{tail(file)})else{return ffi::SQLITE_IOERR_SHMMAP};
    if t.shm_state.is_null(){return ffi::SQLITE_IOERR_SHMMAP}
    let state=unsafe{&mut *t.shm_state};
    let gate=unsafe{&*t.gate};
    if !state.valid()||!(delete_flag==0||delete_flag==1)||
        state.modes.iter().any(|mode|*mode!=0){
        gate.denials.fetch_add(1,Ordering::SeqCst);
        return ffi::SQLITE_IOERR_SHMMAP;
    }
    if delete_flag==1{
        // Lab only: do not unlink a shared native object while a second
        // fixture connection might still be attached. Scratch owns cleanup.
        gate.deletes_requested.fetch_add(1,Ordering::SeqCst);
    }
    let raw=t.shm_state;
    t.shm_state=ptr::null_mut();
    drop(unsafe{Box::from_raw(raw)});
    gate.shm_unmaps.fetch_add(1,Ordering::SeqCst);
    ffi::SQLITE_OK
}
unsafe extern "C" fn xclose(file:*mut ffi::sqlite3_file)->c_int{
    let Some(t)=(unsafe{tail(file)})else{return ffi::SQLITE_IOERR};
    let original=t.original;
    let gate=unsafe{&*t.gate};
    let mut leaked_lock=false;
    if !t.shm_state.is_null(){
        let raw=t.shm_state;
        t.shm_state=ptr::null_mut();
        leaked_lock=unsafe{(&*raw).modes.iter().any(|mode|*mode!=0)};
        drop(unsafe{Box::from_raw(raw)});
    }
    let rc=match unsafe{(*original).xClose}{
        Some(close)=>unsafe{close(file)},
        None=>ffi::SQLITE_IOERR,
    };
    gate.closes.fetch_add(1,Ordering::SeqCst);
    if leaked_lock||rc!=ffi::SQLITE_OK{ffi::SQLITE_IOERR}else{ffi::SQLITE_OK}
}
unsafe extern "C" fn xopen(
    vfs:*mut ffi::sqlite3_vfs,name:ffi::sqlite3_filename,
    file:*mut ffi::sqlite3_file,flags:c_int,outflags:*mut c_int
)->c_int{
    let gate=unsafe{&*(vfs as *const Vfs)};
    unsafe{(*file).pMethods=ptr::null()};
    // xOpen is limited to the test's fresh root, not only to a matching
    // basename, and never opens a NULL/temporary filename or operator file.
    let allowed=if name.is_null(){false}else{
        let name=unsafe{CStr::from_ptr(name)}.to_string_lossy();
        Path::new(name.as_ref()).starts_with(&gate.root)
    };
    if !allowed{
        gate.denials.fetch_add(1,Ordering::SeqCst);
        return ffi::SQLITE_CANTOPEN;
    }
    let main=flags&ffi::SQLITE_OPEN_MAIN_DB!=0;
    let wal=flags&ffi::SQLITE_OPEN_WAL!=0;
    if wal {
        // SQLite documents this API ONLY for the untouched filename pointer
        // supplied to WAL/MAIN_JOURNAL xOpen. Never call it for other flags.
        // It proves the WAL open was associated with the retained main
        // sqlite3_file, rather than guessing main identity from WAL pathname.
        // Delegated WAL xOpen remains by-name: this is NOT atomic custody.
        let owner=unsafe{ffi::sqlite3_database_file_object(name)};
        let methods=if owner.is_null(){ptr::null()}else{unsafe{(*owner).pMethods}};
        let mut native:*mut c_void=ptr::null_mut();
        let rc=if methods.is_null(){ffi::SQLITE_NOTFOUND}
            else if let Some(control)=unsafe{(*methods).xFileControl}{
                unsafe{control(owner,ffi::SQLITE_FCNTL_WIN32_GET_HANDLE,
                    (&mut native as *mut *mut c_void).cast())}
            }else{ffi::SQLITE_NOTFOUND};
        let observed=if rc==ffi::SQLITE_OK{raw_id(native)}else{None};
        if observed!=Some(gate.expected_db)||
            gate.deny_wal_main_owner_for_test.load(Ordering::SeqCst){
            gate.native_refusals.fetch_add(1,Ordering::SeqCst);
            gate.denials.fetch_add(1,Ordering::SeqCst);
            return ffi::SQLITE_CANTOPEN;
        }
        gate.wal_main_owner_matches.fetch_add(1,Ordering::SeqCst);
    }
    let Some(delegate)=(unsafe{(*gate.default).xOpen})else{return ffi::SQLITE_CANTOPEN};
    let result=unsafe{delegate(gate.default,name,file,flags,outflags)};
    if result!=ffi::SQLITE_OK{return result}
    // Verify the ACTUAL native Win32 HANDLE returned by the default xOpen.
    // SQLite's file-control opcode 29 reads that HANDLE from this sqlite3_file.
    // WAL path observation remains a non-atomic test-only comparison; this
    // does not bind the custody of main/-wal/-shm as an indivisible unit.
    if main||wal{
        let original=unsafe{(*file).pMethods};
        let mut native:*mut c_void=ptr::null_mut();
        let rc=if original.is_null(){ffi::SQLITE_NOTFOUND}
            else if let Some(control)=unsafe{(*original).xFileControl}{
                unsafe{control(file,ffi::SQLITE_FCNTL_WIN32_GET_HANDLE,
                    (&mut native as *mut *mut c_void).cast())}
            }else{ffi::SQLITE_NOTFOUND};
        let observed=if rc==ffi::SQLITE_OK{raw_id(native)}else{None};
        let expected=if main{Some(gate.expected_db)}else{
            // The WAL name is observed after the delegate opened it; this
            // is NOT a preowned, atomically pinned WAL identity.
            let named=unsafe{CStr::from_ptr(name)}.to_string_lossy();
            OpenOptions::new().read(true).write(true).share_mode(1|2|4)
                .open(Path::new(named.as_ref())).ok().and_then(|f|id(&f))
        };
        let deny=if main{
            gate.deny_main_native_id_for_test.load(Ordering::SeqCst)
        }else{
            gate.deny_wal_native_id_for_test.load(Ordering::SeqCst)
        };
        if observed.is_none()||observed!=expected||deny{
            gate.native_refusals.fetch_add(1,Ordering::SeqCst);
            gate.denials.fetch_add(1,Ordering::SeqCst);
            if !original.is_null(){
                if let Some(close)=unsafe{(*original).xClose}{
                    let _=unsafe{close(file)};
                }
            }
            unsafe{(*file).pMethods=ptr::null()};
            return ffi::SQLITE_CANTOPEN;
        }
        if main{gate.main_native_matches.fetch_add(1,Ordering::SeqCst);}
        if wal{gate.wal_native_matches.fetch_add(1,Ordering::SeqCst);}
    }
    if !main{return result}
    let original=unsafe{(*file).pMethods};
    if original.is_null()||(unsafe{(*original).iVersion}<2){
        if !original.is_null(){
            if let Some(close)=unsafe{(*original).xClose}{let _=unsafe{close(file)};}
        }
        unsafe{(*file).pMethods=ptr::null()};
        gate.denials.fetch_add(1,Ordering::SeqCst);
        return ffi::SQLITE_CANTOPEN;
    }
    let held=OpenOptions::new().read(true).write(true).share_mode(1|2|4)
        .open(&gate.shm).ok();
    let state=held.and_then(|f|ShmState::new(f,gate.expected,gate.shm.clone()));
    let Some(state)=state else{
        if let Some(close)=unsafe{(*original).xClose}{let _=unsafe{close(file)};}
        unsafe{(*file).pMethods=ptr::null()};
        gate.denials.fetch_add(1,Ordering::SeqCst);
        return ffi::SQLITE_CANTOPEN;
    };
    let tail=unsafe{(file as *mut u8).add(gate.tail_offset)} as *mut FileTail;
    let mut methods=unsafe{ptr::read(original)};
    methods.xClose=Some(xclose);
    methods.xShmMap=Some(xshm_map);
    methods.xShmLock=Some(xshm_lock);
    methods.xShmBarrier=Some(xshm_barrier);
    methods.xShmUnmap=Some(xshm_unmap);
    unsafe{
        ptr::write(tail,FileTail{
            methods,original,gate,shm_state:Box::into_raw(Box::new(state))
        });
        (*file).pMethods=&(*tail).methods;
    }
    gate.main_opens.fetch_add(1,Ordering::SeqCst);
    ffi::SQLITE_OK
}
struct Registered{
    state:Box<Vfs>,
    name:CString,
}
impl Registered{
    fn fresh(root:&Scratch)->Self{
        static SERIAL:AtomicUsize=AtomicUsize::new(0);
        let name=CString::new(format!("r4-owner-shm-vfs-{}-{}",
            process::id(),SERIAL.fetch_add(1,Ordering::Relaxed))).unwrap();
        let default=unsafe{ffi::sqlite3_vfs_find(ptr::null())};
        assert!(!default.is_null());
        let size=unsafe{(*default).szOsFile} as usize;
        let align=std::mem::align_of::<FileTail>();
        let tail_offset=size.div_ceil(align)*align;
        let wrapped=tail_offset+std::mem::size_of::<FileTail>();
        assert!(wrapped<=c_int::MAX as usize);
        let master=OpenOptions::new().read(true).write(true).share_mode(1|2|4)
            .open(&root.shm).expect("SHM fixture must be CREATE_NEW first");
        let expected=id(&master).expect("native FileId128 on fixture");
        let master_db=OpenOptions::new().read(true).write(true).share_mode(1|2|4)
            .open(&root.db).expect("main fixture was CREATE_NEW only");
        let expected_db=id(&master_db).expect("main fixture FileId128");
        let mut state=Box::new(Vfs{
            dispatch:unsafe{ptr::read(default)},default,root:root.dir.clone(),
            shm:root.shm.clone(),master,expected,master_db,expected_db,
            deny_main_native_id_for_test:AtomicBool::new(false),
            deny_wal_native_id_for_test:AtomicBool::new(false),
            deny_wal_main_owner_for_test:AtomicBool::new(false),
            wal_main_owner_matches:AtomicUsize::new(0),
            main_native_matches:AtomicUsize::new(0),
            wal_native_matches:AtomicUsize::new(0),
            native_refusals:AtomicUsize::new(0),
            tail_offset,
            main_opens:AtomicUsize::new(0),shm_maps:AtomicUsize::new(0),
            shm_locks:AtomicUsize::new(0),shm_unmaps:AtomicUsize::new(0),
            deletes_requested:AtomicUsize::new(0),closes:AtomicUsize::new(0),
            denials:AtomicUsize::new(0),
        });
        state.dispatch.szOsFile=wrapped as c_int;
        state.dispatch.pNext=ptr::null_mut();
        state.dispatch.zName=name.as_ptr();
        state.dispatch.xOpen=Some(xopen);
        assert_eq!(unsafe{ffi::sqlite3_vfs_register(&mut state.dispatch,0)},ffi::SQLITE_OK);
        Self{state,name}
    }
    fn name(&self)->&str{self.name.to_str().unwrap()}
}
impl Drop for Registered{
    fn drop(&mut self){
        assert_eq!(unsafe{ffi::sqlite3_vfs_unregister(&mut self.state.dispatch)},ffi::SQLITE_OK);
    }
}
#[test]
fn r4_registered_owner_shm_runs_normal_wal_sql_only_on_disposable_fixture(){
    let root=Scratch::fresh();
    let registered=Registered::fresh(&root);
    let db=Connection::open_with_flags_and_vfs(
        &root.db,OpenFlags::SQLITE_OPEN_READ_WRITE,registered.name()).unwrap();
    let lock_mode:String=db.query_row("PRAGMA locking_mode=NORMAL",[],|r|r.get(0)).unwrap();
    assert_eq!(lock_mode.to_ascii_lowercase(),"normal");
    let journal:String=db.query_row("PRAGMA journal_mode=WAL",[],|r|r.get(0)).unwrap();
    assert_eq!(journal.to_ascii_lowercase(),"wal");
    db.execute_batch("CREATE TABLE ephemeral (n INTEGER NOT NULL); INSERT INTO ephemeral VALUES (7);").unwrap();
    let n:i64=db.query_row("SELECT n FROM ephemeral",[],|r|r.get(0)).unwrap();
    assert_eq!(n,7);
    assert!(registered.state.main_opens.load(Ordering::SeqCst)>=1);
    assert!(registered.state.shm_maps.load(Ordering::SeqCst)>=1,
        "NORMAL WAL must exercise custom native SHM callback, not EXCLUSIVE fallback");
    assert!(registered.state.shm_locks.load(Ordering::SeqCst)>=1);
    drop(db);
    assert!(registered.state.shm_unmaps.load(Ordering::SeqCst)>=1);
    assert!(registered.state.closes.load(Ordering::SeqCst)>=1);
    // Native SHM file intentionally persists until the fresh Scratch drops.
}
#[test]
fn r4_registered_owner_shm_denies_replaced_shm_identity_before_main_xopen(){
    let root=Scratch::fresh();
    let gate=Registered::fresh(&root);
    let moved=root.dir.join("old-shm.fixture");
    fs::rename(&root.shm,&moved).expect("fresh TEST path rename only");
    let decoy=OpenOptions::new().read(true).write(true).share_mode(1|2|4)
        .create_new(true).open(&root.shm).unwrap();
    decoy.set_len(PAGE_SIZE as u64).unwrap();
    assert_ne!(id(&decoy),Some(gate.state.expected));
    let opened=Connection::open_with_flags_and_vfs(
        &root.db,OpenFlags::SQLITE_OPEN_READ_WRITE,gate.name());
    assert!(opened.is_err(),"FileId mismatch must FAIL CLOSED before SQLite SQL");
    assert_eq!(gate.state.main_opens.load(Ordering::SeqCst),0);
    assert!(gate.state.denials.load(Ordering::SeqCst)>=1);
    drop(decoy);
    // Unmodified native master remains held through the refusal.
    assert_eq!(id(&gate.state.master),Some(gate.state.expected));
}


#[test]
fn r4_two_sqlite_connections_share_owned_native_shm_and_serialize_wal_writers(){
    let root=Scratch::fresh();
    let gate=Registered::fresh(&root);
    let first=Connection::open_with_flags_and_vfs(
        &root.db,OpenFlags::SQLITE_OPEN_READ_WRITE,gate.name()).unwrap();
    let mode:String=first.query_row("PRAGMA locking_mode=NORMAL",[],|r|r.get(0)).unwrap();
    assert_eq!(mode.to_ascii_lowercase(),"normal");
    let journal:String=first.query_row("PRAGMA journal_mode=WAL",[],|r|r.get(0)).unwrap();
    assert_eq!(journal.to_ascii_lowercase(),"wal");
    first.execute_batch("CREATE TABLE concurrent_fixture (n INTEGER NOT NULL);").unwrap();
    let second=Connection::open_with_flags_and_vfs(
        &root.db,OpenFlags::SQLITE_OPEN_READ_WRITE,gate.name()).unwrap();
    let second_mode:String=second.query_row("PRAGMA locking_mode=NORMAL",[],|r|r.get(0)).unwrap();
    assert_eq!(second_mode.to_ascii_lowercase(),"normal");
    first.execute_batch("BEGIN IMMEDIATE; INSERT INTO concurrent_fixture VALUES(11);").unwrap();
    assert!(second.execute_batch("BEGIN IMMEDIATE;").is_err(),
        "independent second SQLite connection cannot acquire WAL writer byte");
    first.execute_batch("COMMIT;").unwrap();
    second.execute_batch("BEGIN IMMEDIATE; INSERT INTO concurrent_fixture VALUES(13); COMMIT;").unwrap();
    let total:i64=first.query_row("SELECT SUM(n) FROM concurrent_fixture",[],|r|r.get(0)).unwrap();
    assert_eq!(total,24);
    assert_eq!(gate.state.main_opens.load(Ordering::SeqCst),2);
    assert!(gate.state.shm_maps.load(Ordering::SeqCst)>=2);
    assert!(gate.state.shm_locks.load(Ordering::SeqCst)>=2);
    drop(second);
    drop(first);
    assert_eq!(gate.state.closes.load(Ordering::SeqCst),2);
}
#[test]
fn r4_postopen_shm_path_substitution_fails_closed_at_next_wal_lock(){
    let root=Scratch::fresh();
    let gate=Registered::fresh(&root);
    let db=Connection::open_with_flags_and_vfs(
        &root.db,OpenFlags::SQLITE_OPEN_READ_WRITE,gate.name()).unwrap();
    let journal:String=db.query_row("PRAGMA journal_mode=WAL",[],|r|r.get(0)).unwrap();
    assert_eq!(journal.to_ascii_lowercase(),"wal");
    db.execute_batch("CREATE TABLE before_substitution (n INTEGER);").unwrap();
    let original=root.dir.join("original-held-shm.fixture");
    fs::rename(&root.shm,&original).expect("rename owned scratch SHM only");
    let decoy=OpenOptions::new().read(true).write(true).share_mode(1|2|4)
        .create_new(true).open(&root.shm).unwrap();
    decoy.set_len(PAGE_SIZE as u64).unwrap();
    assert_ne!(id(&decoy),Some(gate.state.expected));
    assert!(db.execute_batch("BEGIN IMMEDIATE; INSERT INTO before_substitution VALUES(1); COMMIT;").is_err(),
        "new SHM pathname FileId differs: next native lock must reject");
    assert!(gate.state.denials.load(Ordering::SeqCst)>=1);
    assert_eq!(id(&gate.state.master),Some(gate.state.expected));
    drop(db);
    drop(decoy);
    // This non-atomic post-name read cannot prove absence of a racing swap.
}


#[test]
fn r4_delegated_native_main_and_wal_handles_match_fresh_fixture_identities(){
    let root=Scratch::fresh();
    let gate=Registered::fresh(&root);
    let db=Connection::open_with_flags_and_vfs(
        &root.db,OpenFlags::SQLITE_OPEN_READ_WRITE,gate.name()).unwrap();
    assert_eq!(gate.state.main_native_matches.load(Ordering::SeqCst),1);
    assert_eq!(id(&gate.state.master_db),Some(gate.state.expected_db));
    let journal:String=db.query_row("PRAGMA journal_mode=WAL",[],|r|r.get(0)).unwrap();
    assert_eq!(journal.to_ascii_lowercase(),"wal");
    db.execute_batch("CREATE TABLE xopen_fixture(n INTEGER); INSERT INTO xopen_fixture VALUES(9);").unwrap();
    assert!(gate.state.wal_native_matches.load(Ordering::SeqCst)>=1,
        "real delegated WAL xOpen HANDLE must be inspected, not guessed from name");
    assert!(gate.state.wal_main_owner_matches.load(Ordering::SeqCst)>=1,
        "actual WAL xOpen filename must resolve to the retained main SQLite native FileId");
    assert_eq!(gate.state.native_refusals.load(Ordering::SeqCst),0);
    drop(db);
}
#[test]
fn r4_delegated_main_and_wal_native_handle_faults_close_and_veto(){
    {
        let root=Scratch::fresh();
        let gate=Registered::fresh(&root);
        gate.state.deny_main_native_id_for_test.store(true,Ordering::SeqCst);
        let result=Connection::open_with_flags_and_vfs(
            &root.db,OpenFlags::SQLITE_OPEN_READ_WRITE,gate.name());
        assert!(result.is_err(),"actual native main xOpen must fail closed");
        assert_eq!(gate.state.main_opens.load(Ordering::SeqCst),0);
        assert!(gate.state.native_refusals.load(Ordering::SeqCst)>=1);
        assert_eq!(gate.state.main_native_matches.load(Ordering::SeqCst),0);
        assert_eq!(id(&gate.state.master_db),Some(gate.state.expected_db));
    }
    {
        let root=Scratch::fresh();
        let gate=Registered::fresh(&root);
        let db=Connection::open_with_flags_and_vfs(
            &root.db,OpenFlags::SQLITE_OPEN_READ_WRITE,gate.name()).unwrap();
        gate.state.deny_wal_native_id_for_test.store(true,Ordering::SeqCst);
        // Even if PRAGMA falls back to another journal, no WAL write may
        // proceed when the ACTUAL delegated WAL xOpen HANDLE is vetoed.
        let attempt=db.execute_batch(
            "PRAGMA journal_mode=WAL; CREATE TABLE blocked_wal(n INTEGER); INSERT INTO blocked_wal VALUES(5);");
        assert!(attempt.is_err(),"disposable WAL native-handle veto must fail closed");
        assert!(gate.state.native_refusals.load(Ordering::SeqCst)>=1);
        assert_eq!(gate.state.wal_native_matches.load(Ordering::SeqCst),0);
        drop(db);
    }
}


// R4 CI-only successor: two *different Windows OS processes* contend over
// the same fresh SQLite WAL NORMAL fixture. This is NOT a hostile writer
// absence proof, NOT atomic main/WAL/SHM custody, and NOT production access.
const R4_CHILD_ROOT_ENV:&str="FABULAXIOM_R4_TEST_ONLY_CHILD_ROOT";
const R4_CHILD_NAME:&str=
    "m32_r4_registered_owned_shm_vfs_disposable_tests::r4_multiprocess_wal_child_helper";
const R4_PROOF_STAMP:&str="FABULAXIOM_R4_NEW_TEMP_ONLY_V1";

struct StopChildOnDrop(std::process::Child);
impl Drop for StopChildOnDrop {
    fn drop(&mut self){
        if self.0.try_wait().ok().flatten().is_none(){
            let _=self.0.kill();
            let _=self.0.wait();
        }
    }
}
fn r4_new_only_signal(root:&Path,name:&str){
    use std::io::Write;
    let mut f=OpenOptions::new().write(true).create_new(true)
        .open(root.join(name)).expect("signal CREATE_NEW in invented test dir");
    f.write_all(R4_PROOF_STAMP.as_bytes()).unwrap();
    f.sync_all().unwrap();
}
fn r4_wait_signal(root:&Path,name:&str,mut child:Option<&mut std::process::Child>){
    let end=std::time::Instant::now()+std::time::Duration::from_secs(20);
    loop{
        let signal=root.join(name);
        if signal.exists(){
            assert_eq!(fs::read_to_string(signal).unwrap(),R4_PROOF_STAMP);
            return;
        }
        if let Some(ref mut c)=child{
            if let Some(status)=c.try_wait().expect("child status"){
                panic!("R4 disposable child exited before {name}: {status}");
            }
        }
        assert!(std::time::Instant::now()<end,
            "bounded R4 child handshake timed out at {name}");
        std::thread::sleep(std::time::Duration::from_millis(20));
    }
}
#[test]
fn r4_multiprocess_wal_child_helper(){
    // Ordinary cargo test invokes this test but is a strict no-op.
    // Only a controlled parent sets the per-child root environment.
    let Some(dir)=std::env::var_os(R4_CHILD_ROOT_ENV).map(PathBuf::from)else{return};
    let temp=fs::canonicalize(std::env::temp_dir()).unwrap();
    assert_eq!(fs::canonicalize(&dir).unwrap().parent(),Some(temp.as_path()),
        "only a direct new %TEMP% test directory is accepted");
    assert!(dir.file_name().unwrap().to_string_lossy().starts_with(PREFIX));
    assert!(fs::symlink_metadata(&dir).unwrap().file_type().is_dir());
    assert_eq!(fs::read_to_string(dir.join("child-proof-stamp")).unwrap(),
        R4_PROOF_STAMP);
    // Child must not remove its parent's scratch root on exit.
    let root=std::mem::ManuallyDrop::new(Scratch{
        db:dir.join("invented.sqlite3"),
        shm:dir.join("invented.sqlite3-shm"),
        dir,
    });
    let gate=Registered::fresh(&root);
    let db=Connection::open_with_flags_and_vfs(
        &root.db,OpenFlags::SQLITE_OPEN_READ_WRITE,gate.name()).unwrap();
    let mode:String=db.query_row("PRAGMA journal_mode",[],|r|r.get(0)).unwrap();
    assert_eq!(mode.to_ascii_lowercase(),"wal");
    let busy=db.execute_batch("BEGIN IMMEDIATE;");
    assert!(matches!(busy.as_ref().err().and_then(|e|e.sqlite_error_code()),
        Some(rusqlite::ErrorCode::DatabaseBusy | rusqlite::ErrorCode::DatabaseLocked)),
        "the parent must exclusively hold the WAL writer byte: {busy:?}");
    r4_new_only_signal(&root.dir,"child-observed-wal-busy");
    r4_wait_signal(&root.dir,"parent-committed",None);
    db.execute_batch("BEGIN IMMEDIATE; INSERT INTO multi_process_fixture VALUES(13); COMMIT;")
        .expect("child writes only after parent released WAL writer lock");
    let sum:i64=db.query_row(
        "SELECT SUM(n) FROM multi_process_fixture",[],|r|r.get(0)).unwrap();
    assert_eq!(sum,24);
    assert_eq!(gate.state.main_native_matches.load(Ordering::SeqCst),1);
    assert!(gate.state.wal_native_matches.load(Ordering::SeqCst)>=1);
    assert!(gate.state.shm_maps.load(Ordering::SeqCst)>=1);
    assert!(gate.state.shm_locks.load(Ordering::SeqCst)>=1);
    drop(db);
}
#[test]
fn r4_two_windows_processes_serialize_wal_writes_on_fresh_owned_shm(){
    use std::io::Write;
    let root=Scratch::fresh();
    let mut stamp=OpenOptions::new().write(true).create_new(true)
        .open(root.dir.join("child-proof-stamp")).unwrap();
    stamp.write_all(R4_PROOF_STAMP.as_bytes()).unwrap();
    stamp.sync_all().unwrap();
    drop(stamp);
    let gate=Registered::fresh(&root);
    let db=Connection::open_with_flags_and_vfs(
        &root.db,OpenFlags::SQLITE_OPEN_READ_WRITE,gate.name()).unwrap();
    let mode:String=db.query_row("PRAGMA locking_mode=NORMAL",[],|r|r.get(0)).unwrap();
    assert_eq!(mode.to_ascii_lowercase(),"normal");
    let journal:String=db.query_row("PRAGMA journal_mode=WAL",[],|r|r.get(0)).unwrap();
    assert_eq!(journal.to_ascii_lowercase(),"wal");
    db.execute_batch("CREATE TABLE multi_process_fixture(n INTEGER NOT NULL);").unwrap();
    db.execute_batch("BEGIN IMMEDIATE; INSERT INTO multi_process_fixture VALUES(11);").unwrap();
    let process=std::process::Command::new(std::env::current_exe().unwrap())
        .arg("--exact").arg(R4_CHILD_NAME).arg("--nocapture")
        .env(R4_CHILD_ROOT_ENV,&root.dir).spawn()
        .expect("spawn only the current Rust test executable on disposable paths");
    let mut child=StopChildOnDrop(process);
    r4_wait_signal(&root.dir,"child-observed-wal-busy",Some(&mut child.0));
    db.execute_batch("COMMIT;").unwrap();
    r4_new_only_signal(&root.dir,"parent-committed");
    let deadline=std::time::Instant::now()+std::time::Duration::from_secs(20);
    let status=loop{
        if let Some(status)=child.0.try_wait().unwrap(){break status;}
        assert!(std::time::Instant::now()<deadline,"R4 child bounded completion");
        std::thread::sleep(std::time::Duration::from_millis(20));
    };
    assert!(status.success(),"separate Windows OS child test must PASS");
    let sum:i64=db.query_row("SELECT SUM(n) FROM multi_process_fixture",[],|r|r.get(0)).unwrap();
    assert_eq!(sum,24);
    assert_eq!(gate.state.main_native_matches.load(Ordering::SeqCst),1);
    assert!(gate.state.wal_native_matches.load(Ordering::SeqCst)>=1);
    assert!(gate.state.shm_maps.load(Ordering::SeqCst)>=1);
    assert!(gate.state.shm_locks.load(Ordering::SeqCst)>=1);
    drop(db);
}


// R4 region>0 CI-only qualification: the exact same held native SHM file
// supplies two independent SQLite connections with the same page-1 bytes.
// It does NOT implement dynamic growth or atomically bind main/WAL/SHM.
#[test]
fn r4_owned_xshm_region_one_shared_native_mapping_and_bounded_veto_disposable(){
    fn map_region(db:&Connection,page:c_int,size:c_int,extend:c_int)->(c_int,*mut c_void){
        let mut file:*mut ffi::sqlite3_file=ptr::null_mut();
        // SQLite returns its actual sqlite3_file, not an unrelated pathname re-open.
        let rc=unsafe{ffi::sqlite3_file_control(db.handle(),ptr::null(),
            ffi::SQLITE_FCNTL_FILE_POINTER,(&mut file as *mut *mut ffi::sqlite3_file).cast())};
        assert_eq!(rc,ffi::SQLITE_OK);
        assert!(!file.is_null());
        let methods=unsafe{(*file).pMethods};
        assert!(!methods.is_null());
        let callback=unsafe{(*methods).xShmMap}.expect("owned test VFS xShmMap");
        let mut out:*mut c_void=ptr::null_mut();
        let code=unsafe{callback(file,page,size,extend,&mut out)};
        (code,out)
    }
    let root=Scratch::fresh();
    assert_eq!(fs::metadata(&root.shm).unwrap().len(),SHM_MAPPING_BYTES as u64);
    let gate=Registered::fresh(&root);
    let first=Connection::open_with_flags_and_vfs(
        &root.db,OpenFlags::SQLITE_OPEN_READ_WRITE,gate.name()).unwrap();
    let lock_mode:String=first.query_row("PRAGMA locking_mode=NORMAL",[],|r|r.get(0)).unwrap();
    assert_eq!(lock_mode.to_ascii_lowercase(),"normal");
    let journal:String=first.query_row("PRAGMA journal_mode=WAL",[],|r|r.get(0)).unwrap();
    assert_eq!(journal.to_ascii_lowercase(),"wal");
    first.execute_batch("CREATE TABLE region_one_fixture(n INTEGER NOT NULL);
        INSERT INTO region_one_fixture VALUES (3);").unwrap();
    let second=Connection::open_with_flags_and_vfs(
        &root.db,OpenFlags::SQLITE_OPEN_READ_WRITE,gate.name()).unwrap();
    let observed:i64=second.query_row("SELECT SUM(n) FROM region_one_fixture",[],|r|r.get(0)).unwrap();
    assert_eq!(observed,3);
    let pinned=id(&gate.state.master).unwrap();
    let (rc0,page0)=map_region(&first,0,PAGE_SIZE as c_int,0);
    let (rc1,page1)=map_region(&first,1,PAGE_SIZE as c_int,0);
    assert_eq!((rc0,rc1),(ffi::SQLITE_OK,ffi::SQLITE_OK));
    assert!(!page0.is_null()&&!page1.is_null());
    assert_eq!(page1 as usize-page0 as usize,PAGE_SIZE);
    let (rc_peer,peer_region1)=map_region(&second,1,PAGE_SIZE as c_int,0);
    assert_eq!(rc_peer,ffi::SQLITE_OK);
    assert!(!peer_region1.is_null());
    const PROBE_OFFSET:usize=127; // within region 1; not the WAL-index region-0 header
    let before=unsafe{*page1.cast::<u8>().add(PROBE_OFFSET)};
    unsafe{*page1.cast::<u8>().add(PROBE_OFFSET)=0xA7};
    assert_eq!(unsafe{*peer_region1.cast::<u8>().add(PROBE_OFFSET)},0xA7,
        "two SQLite VFS clients must see the same held native SHM page-1 bytes");
    unsafe{*page1.cast::<u8>().add(PROBE_OFFSET)=before};
    assert_eq!(id(&gate.state.master),Some(pinned));
    assert_eq!(id(&gate.state.master_db),Some(gate.state.expected_db));
    let accepted=gate.state.shm_maps.load(Ordering::SeqCst);
    let denied=gate.state.denials.load(Ordering::SeqCst);
    for (region,size,extend) in [
        (2,PAGE_SIZE as c_int,0),
        (-1,PAGE_SIZE as c_int,0),
        (c_int::MAX,PAGE_SIZE as c_int,1),
        (1,(PAGE_SIZE/2) as c_int,0),
        (1,PAGE_SIZE as c_int,2),
    ] {
        let (code,output)=map_region(&first,region,size,extend);
        assert_eq!(code,ffi::SQLITE_IOERR_SHMMAP);
        assert!(output.is_null(),"rejected mapping cannot leak an unbounded pointer");
    }
    assert_eq!(gate.state.shm_maps.load(Ordering::SeqCst),accepted);
    assert!(gate.state.denials.load(Ordering::SeqCst)>=denied+5);
    let final_count:i64=first.query_row(
        "SELECT COUNT(*) FROM region_one_fixture",[],|r|r.get(0)).unwrap();
    assert_eq!(final_count,1,"out-of-bounds probes cannot damage WAL page zero");
    drop(second);
    drop(first);
    assert!(gate.state.shm_unmaps.load(Ordering::SeqCst)>=2);
    // This is only a two-page borrowed test mapping, NOT all WAL-index regions.
}


// R4 disposable ABA witness: seeing a SHM FileId/path substitution poisons a
// connection for good, even if the original pathname is later restored.
// This never establishes atomic main/WAL/SHM custody or writer admission.
#[test]
fn r4_observed_shm_path_aba_restoration_never_rearms_native_callbacks(){
    let root=Scratch::fresh();
    let gate=Registered::fresh(&root);
    let db=Connection::open_with_flags_and_vfs(
        &root.db,OpenFlags::SQLITE_OPEN_READ_WRITE,gate.name()).unwrap();
    let locking:String=db.query_row("PRAGMA locking_mode=NORMAL",[],|row|row.get(0)).unwrap();
    assert_eq!(locking.to_ascii_lowercase(),"normal");
    let journal:String=db.query_row("PRAGMA journal_mode=WAL",[],|row|row.get(0)).unwrap();
    assert_eq!(journal.to_ascii_lowercase(),"wal");
    db.execute_batch("CREATE TABLE shm_aba_fixture(n INTEGER NOT NULL);
        INSERT INTO shm_aba_fixture VALUES (7);").unwrap();
    let expected=gate.state.expected;
    let mut file:*mut ffi::sqlite3_file=ptr::null_mut();
    let file_control=unsafe{ffi::sqlite3_file_control(db.handle(),ptr::null(),
        ffi::SQLITE_FCNTL_FILE_POINTER,
        (&mut file as *mut *mut ffi::sqlite3_file).cast())};
    assert_eq!(file_control,ffi::SQLITE_OK);
    assert!(!file.is_null());
    let methods=unsafe{(*file).pMethods};
    assert!(!methods.is_null());
    let xlock=unsafe{(*methods).xShmLock}.expect("real test VFS native SHM lock callback");
    let xmap=unsafe{(*methods).xShmMap}.expect("real test VFS native SHM map callback");

    let original=root.dir.join("original-owned-shm-aba.fixture");
    fs::rename(&root.shm,&original).expect("rename disposable SHM only");
    let decoy=OpenOptions::new().read(true).write(true).share_mode(1|2|4)
        .create_new(true).open(&root.shm).unwrap();
    decoy.set_len(SHM_MAPPING_BYTES as u64).unwrap();
    assert_ne!(id(&decoy),Some(expected));
    assert_eq!(unsafe{xlock(file,0,1,(SHM_LOCK|SHM_SHARED) as c_int)},
        ffi::SQLITE_IOERR_SHMLOCK,"observed SHM substitution must poison the connection");

    drop(decoy);
    fs::remove_file(&root.shm).expect("remove test-only decoy");
    fs::rename(&original,&root.shm).expect("restore original test-only SHM name");
    assert_eq!(id(&gate.state.master),Some(expected));
    let named=OpenOptions::new().read(true).write(true).share_mode(1|2|4)
        .open(&root.shm).unwrap();
    assert_eq!(id(&named),Some(expected),"native held and named SHM IDs match again");
    drop(named);

    assert_eq!(unsafe{xlock(file,0,1,(SHM_LOCK|SHM_SHARED) as c_int)},
        ffi::SQLITE_IOERR_SHMLOCK,"ABA restoration cannot revoke observed poison");
    let mut output:*mut c_void=ptr::null_mut();
    assert_eq!(unsafe{xmap(file,1,PAGE_SIZE as c_int,0,&mut output)},
        ffi::SQLITE_IOERR_SHMMAP,"poisoned connection must not expose mapped SHM");
    assert!(output.is_null());
    assert!(gate.state.denials.load(Ordering::SeqCst)>=3);
    drop(db);
    // Default SQLite writer, other VFSes and all operator locations unchanged.
}


// R4 CI-only negative: WAL xOpen is associated with SQLite's actual main
// sqlite3_file, not a by-name main re-open. A forced owner veto must occur
// before the WAL delegate xOpen. Still not a three-file atomic custody proof.
#[test]
fn r4_wal_xopen_sqlite_main_file_object_native_owner_veto_disposable(){
    let root=Scratch::fresh();
    let gate=Registered::fresh(&root);
    let db=Connection::open_with_flags_and_vfs(
        &root.db,OpenFlags::SQLITE_OPEN_READ_WRITE,gate.name()).unwrap();
    assert_eq!(id(&gate.state.master_db),Some(gate.state.expected_db));
    gate.state.deny_wal_main_owner_for_test.store(true,Ordering::SeqCst);
    let attempt=db.execute_batch(
        "PRAGMA journal_mode=WAL;
         CREATE TABLE blocked_wal_owner(n INTEGER);
         INSERT INTO blocked_wal_owner VALUES (9);");
    assert!(attempt.is_err(),"native SQLite WAL->main owner veto must fail closed");
    assert_eq!(gate.state.wal_main_owner_matches.load(Ordering::SeqCst),0);
    assert_eq!(gate.state.wal_native_matches.load(Ordering::SeqCst),0,
        "veto must precede delegated WAL xOpen");
    assert!(gate.state.native_refusals.load(Ordering::SeqCst)>=1);
    assert!(gate.state.denials.load(Ordering::SeqCst)>=1);
    drop(db);
}


// R4 disposable design witness: independently held, newly invented native
// main/WAL/SHM file identities; an observed WAL name swap latches a refusal.
// This is NOT yet integrated into SQLite xOpen, is NOT atomic, and cannot
// authorize any production writer or access operator data.
#[test]
fn r4_preheld_wal_main_shm_native_identity_triad_aba_poison_disposable(){
    fn path_id(path:&Path)->Option<FileIdInfo>{
        OpenOptions::new().read(true).write(true).share_mode(1|2|4)
            .open(path).ok().and_then(|file|id(&file))
    }
    let root=Scratch::fresh();
    let wal=root.dir.join("invented.sqlite3-wal");
    let held_wal=OpenOptions::new().read(true).write(true).share_mode(1|2|4)
        .create_new(true).open(&wal).expect("CREATE_NEW WAL only in disposable TEMP");
    let held_main=OpenOptions::new().read(true).write(true).share_mode(1|2|4)
        .open(&root.db).expect("fresh main fixture only");
    let held_shm=OpenOptions::new().read(true).write(true).share_mode(1|2|4)
        .open(&root.shm).expect("fresh SHM fixture only");
    let expected_main=id(&held_main).expect("native FileId128 main");
    let expected_wal=id(&held_wal).expect("native FileId128 WAL");
    let expected_shm=id(&held_shm).expect("native FileId128 SHM");
    let mut poisoned=false;
    let mut check=||{
        if poisoned{return false}
        let same=id(&held_main)==Some(expected_main)
            &&id(&held_wal)==Some(expected_wal)
            &&id(&held_shm)==Some(expected_shm)
            &&path_id(&root.db)==Some(expected_main)
            &&path_id(&wal)==Some(expected_wal)
            &&path_id(&root.shm)==Some(expected_shm);
        if !same{poisoned=true}
        same
    };
    assert!(check(),"three fresh native handles and names initially agree");
    let previous=root.dir.join("original-held-wal.fixture");
    fs::rename(&wal,&previous).expect("rename only own WAL fixture");
    let decoy=OpenOptions::new().read(true).write(true).share_mode(1|2|4)
        .create_new(true).open(&wal).expect("CREATE_NEW decoy");
    assert_ne!(id(&decoy),Some(expected_wal));
    assert!(!check(),"substituted WAL pathname must poison the triad");
    assert_eq!(id(&held_wal),Some(expected_wal),"held WAL identity survives rename");
    assert_eq!(id(&held_main),Some(expected_main));
    assert_eq!(id(&held_shm),Some(expected_shm));
    drop(decoy);
    fs::remove_file(&wal).expect("remove disposable decoy");
    fs::rename(&previous,&wal).expect("restore original disposable WAL");
    assert_eq!(path_id(&wal),Some(expected_wal));
    assert!(!check(),"restoration cannot undo previously observed refusal");
    drop(held_wal);
    drop(held_main);
    drop(held_shm);
    // The only cleanup is Scratch::drop on our new TEMP directory.
}
