//! R4: REGISTERED test-only SQLite VFS binding NORMAL WAL xShm* to held Win32
//! SHM native HANDLE. Fresh %TEMP% fixtures; default VFS xOpen only for the
//! invented database/WAL/journal. NEVER operator data or production IPC.
//! NOT atomic main/WAL/SHM custody, no production registration, no writer gate.
use rusqlite::{ffi,Connection,OpenFlags};
use std::{ffi::{c_int,c_void,CStr,CString},fs::{self,File,OpenOptions},
    os::windows::{fs::OpenOptionsExt,io::AsRawHandle},path::{Path,PathBuf},
    ptr,sync::atomic::{AtomicUsize,Ordering,fence},time::{SystemTime,UNIX_EPOCH},process};

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
fn ov(byte:u32)->Overlapped{
    Overlapped{internal:0,internal_high:0,offset:byte,offset_high:0,event:ptr::null_mut()}
}
const PAGE_SIZE:usize=32768;
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
            if p==&shm {f.set_len(PAGE_SIZE as u64).unwrap();}
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
        let view=unsafe{MapViewOfFile(mapping,2|4,0,0,PAGE_SIZE)};
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
struct ShmState{held:File,expected:FileIdInfo,view:View,modes:[u32;8]}
impl ShmState{
    fn new(held:File,expected:FileIdInfo)->Option<Self>{
        if id(&held)!=Some(expected){return None}
        let view=View::from_held(&held)?;
        Some(Self{held,expected,view,modes:[0;8]})
    }
    fn valid(&self)->bool{id(&self.held)==Some(self.expected)}
}
#[repr(C)]
struct Vfs{
    dispatch:ffi::sqlite3_vfs,
    default:*mut ffi::sqlite3_vfs,
    root:PathBuf,
    shm:PathBuf,
    master:File,
    expected:FileIdInfo,
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
    if !held.valid()||page!=0||sz!=PAGE_SIZE as c_int||(extend!=0&&extend!=1){
        gate.denials.fetch_add(1,Ordering::SeqCst);
        return ffi::SQLITE_IOERR_SHMMAP;
    }
    gate.shm_maps.fetch_add(1,Ordering::SeqCst);
    unsafe{*out=held.view.view};
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
    let state=unsafe{&*t.shm_state};
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
    let Some(delegate)=(unsafe{(*gate.default).xOpen})else{return ffi::SQLITE_CANTOPEN};
    let result=unsafe{delegate(gate.default,name,file,flags,outflags)};
    if result!=ffi::SQLITE_OK{return result}
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
    let state=held.and_then(|f|ShmState::new(f,gate.expected));
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
        let mut state=Box::new(Vfs{
            dispatch:unsafe{ptr::read(default)},default,root:root.dir.clone(),
            shm:root.shm.clone(),master,expected,tail_offset,
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
