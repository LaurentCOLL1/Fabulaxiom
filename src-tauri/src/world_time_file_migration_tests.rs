//! M3.1 controlled-copy migration rehearsal, exclusively disposable test files.
//! We copy ONLY a closed fixture DB, never a live active operator database.
//! No production runtime entry point or v7 registry change is exposed here.
use crate::{database, m32_manual_chronology as chronology};
use crate::world_time_preflight::{inspect_v6, PreflightFailure};
use rusqlite::{params, types::ValueRef, Connection, OpenFlags};
use std::{
    collections::BTreeMap,
    fs,
    io::ErrorKind,
    path::{Component, Path, PathBuf},
    process,
    sync::{Arc, Barrier},
    thread,
    time::{SystemTime, UNIX_EPOCH},
};

const CANDIDATE_SQL: &str = include_str!("../sql/m3_1_world_time_v7_candidate.sql");
const M32_DECISIONS_SQL: &str = include_str!("../sql/m3_2_chronology_decisions_candidate.sql");

struct DisposableRoot(PathBuf);
impl DisposableRoot {
    fn new(name: &str) -> Self {
        let unique = SystemTime::now().duration_since(UNIX_EPOCH)
            .expect("time").as_nanos();
        let root = std::env::temp_dir().join(format!(
            "fabulaxiom-m31-{name}-{}-{unique}", process::id()
        ));
        fs::create_dir(&root).expect("new owned disposable test directory");
        Self(root)
    }
    fn file(&self, name: &str) -> PathBuf { self.0.join(name) }
}
impl Drop for DisposableRoot {
    fn drop(&mut self) {
        // Only the disposable directory created by this test is removed.
        fs::remove_dir_all(&self.0).expect("cleanup test fixture");
    }
}

// Next Gate C test-only building block. SQLite's CREATE flag may reopen an
// existing database; OS create_new is the exclusive namespace claim instead.
// This is NOT a production v7 opener: no operator root/activation proof, no
// durable ownership of ancestors, and no Tauri IPC is exposed.
// The caller supplies only a name within its freshly owned disposable root.
fn claim_new_only_disposable_file(path: &Path) -> Result<fs::File, String> {
    if !path.parent().is_some_and(Path::is_dir) {
        return Err("STOP: no pre-existing owned fixture parent".to_owned());
    }
    // SQLite may inspect a sibling WAL, SHM or rollback journal as soon as it
    // opens the file. Reject all such occupied names before claiming the DB.
    // Any error other than NotFound also stops: unknown is not absent.
    for suffix in ["-wal", "-shm", "-journal"] {
        let mut name = path.as_os_str().to_os_string();
        name.push(suffix);
        match fs::symlink_metadata(Path::new(&name)) {
            Ok(_) => return Err(format!("STOP: occupied SQLite sidecar {suffix}")),
            Err(error) if error.kind() == ErrorKind::NotFound => {},
            Err(error) => return Err(format!("STOP: cannot verify sidecar {suffix}: {error}")),
        }
    }
    let mut options = fs::OpenOptions::new();
    options.write(true).create_new(true);
    #[cfg(windows)] {
        use std::os::windows::fs::OpenOptionsExt;
        // FILE_SHARE_READ | FILE_SHARE_WRITE, deliberately WITHOUT
        // FILE_SHARE_DELETE: SQLite may open RW while a rename of this
        // newly created file is denied until its claim handle is released.
        options.share_mode(0x0000_0001 | 0x0000_0002);
    }
    options.open(path)
        .map_err(|error| format!("STOP: destination is not exclusively new: {error}"))
}

// Pin the *immediate* fixture parent across the test-only SQLite handoff.
// This does not pin all ancestor directory identities or validate ACL/reparse
// traversal; neither protection may be assumed for a real Greenfield profile.
#[cfg(windows)]
fn pin_disposable_parent(path: &Path) -> Result<fs::File, String> {
    use std::os::windows::fs::OpenOptionsExt;
    let parent = path.parent().ok_or("STOP: missing parent")?;
    // FILE_FLAG_BACKUP_SEMANTICS opens a directory handle. No DELETE share.
    fs::OpenOptions::new()
        .access_mode(0)
        .share_mode(0x0000_0001 | 0x0000_0002)
        .custom_flags(0x0200_0000)
        .open(parent)
        .map_err(|error| format!("STOP: cannot pin fixture parent: {error}"))
}

fn connect_claimed_disposable_file(path: &Path, claim: fs::File) -> Result<Connection, String> {
    // Keep the OS claim live WHILE SQLite opens the same path. On Windows its
    // no-delete share is an observable barrier for this *file*, not a proof
    // of full rooted identity, hostile ancestors, sidecars or app lifetime.
    let connection = Connection::open_with_flags(path, OpenFlags::SQLITE_OPEN_READ_WRITE)
        .map_err(|error| format!("STOP: newly claimed file cannot open: {error}"))?;
    drop(claim);
    database::configure_connection(&connection)
        .map_err(|error| format!("STOP: foreign keys unavailable: {error}"))?;
    Ok(connection)
}

fn open_new_only_disposable_file(path: &Path) -> Result<Connection, String> {
    #[cfg(windows)]
    let _parent_pin = pin_disposable_parent(path)?;
    let claim = claim_new_only_disposable_file(path)?;
    connect_claimed_disposable_file(path, claim)
}

// Experimental *fixture* boundary: relative components must stay lexically
// beneath the exact disposable root created by this test. This says nothing
// about the ownership of the OS temp directory or an operator profile root.
fn checked_fixture_parent_chain(root: &Path, destination: &Path)
    -> Result<Vec<PathBuf>, String>
{
    fn forbidden_device_name(name: &str) -> bool {
        let upper = name.to_ascii_uppercase();
        matches!(upper.as_str(), "CON" | "PRN" | "AUX" | "NUL")
            || (upper.len() == 4
                && (upper.starts_with("COM") || upper.starts_with("LPT"))
                && matches!(upper.as_bytes()[3], b'1'..=b'9'))
    }
    if !root.is_absolute() || !destination.is_absolute() {
        return Err("STOP: fixture paths must be absolute".to_owned());
    }
    let relative = destination.strip_prefix(root)
        .map_err(|_| "STOP: destination is outside the disposable fixture root")?;
    let mut names = Vec::new();
    for component in relative.components() {
        let Component::Normal(name) = component else {
            return Err("STOP: non-normal destination component".to_owned());
        };
        let text = name.to_str().ok_or("STOP: non-UTF8 fixture component")?;
        if text.is_empty() {
            return Err("STOP: empty fixture component".to_owned());
        }
        names.push(text.to_owned());
    }
    if names.len() < 2 {
        return Err("STOP: destination needs a fixture-owned subdirectory".to_owned());
    }
    let filename = names.pop().expect("at least two validated components");
    let stem = filename.strip_suffix(".sqlite3")
        .ok_or("STOP: only SQLite fixture filenames allowed")?;
    if stem.is_empty() || forbidden_device_name(stem)
        || !stem.bytes().all(|byte| byte.is_ascii_alphanumeric() || byte == b'-' || byte == b'_')
        || names.iter().any(|part| {
            forbidden_device_name(part)
                || !part.bytes().all(|byte| byte.is_ascii_alphanumeric() || byte == b'-' || byte == b'_')
        })
    {
        return Err("STOP: unsafe fixture component".to_owned());
    }
    let mut chain = vec![root.to_path_buf()];
    let mut cursor = root.to_path_buf();
    for name in names {
        cursor.push(name);
        chain.push(cursor.clone());
    }
    Ok(chain)
}

// Windows fixture identity helpers use only stable Rust + test-only Win32 FFI.
// A retained handle is NOT assumed to prevent directory renaming: Windows
// Server 2025 CI twice renamed an empty leaf despite omitted DELETE sharing.
#[cfg(windows)]
fn windows_fixture_handle_identity(handle: &fs::File) -> Result<(u32, u64), String> {
    use std::os::windows::io::AsRawHandle;
    windows_fixture_raw_handle_identity(handle.as_raw_handle())
}

#[cfg(windows)]
fn windows_fixture_raw_handle_identity(handle: *mut std::ffi::c_void) -> Result<(u32, u64), String> {
    use std::ffi::c_void;

    // Stable-Rust test-only Win32 ABI: MetadataExt::file_index and
    // volume_serial_number currently require unstable `windows_by_handle`.
    // BY_HANDLE_FILE_INFORMATION preserves their legacy 64-bit FileIndex
    // boundary without nightly features or an added production dependency.
    #[repr(C)]
    struct WinFileTime { low: u32, high: u32 }
    #[repr(C)]
    struct WinHandleFileInfo {
        attributes: u32,
        created: WinFileTime,
        accessed: WinFileTime,
        modified: WinFileTime,
        volume: u32,
        size_high: u32,
        size_low: u32,
        links: u32,
        index_high: u32,
        index_low: u32,
    }
    #[link(name = "kernel32")]
    unsafe extern "system" {
        fn GetFileInformationByHandle(handle: *mut c_void, info: *mut WinHandleFileInfo) -> i32;
    }
    let mut info = std::mem::MaybeUninit::<WinHandleFileInfo>::uninit();
    let result = unsafe { GetFileInformationByHandle(handle, info.as_mut_ptr()) };
    if result == 0 {
        return Err(format!("STOP: GetFileInformationByHandle failed: {}", std::io::Error::last_os_error()));
    }
    let info = unsafe { info.assume_init() };
    Ok((info.volume, (u64::from(info.index_high) << 32) | u64::from(info.index_low)))
}

// 128-bit FILE_ID_INFO is the Win32 replacement for the legacy 64-bit
// FileIndex when ReFS can be involved. This remains an observation of a
// live fixture HANDLE, not a durable name claim or an atomic SQLite opener.
#[cfg(windows)]
fn windows_fixture_raw_file_id_128(handle: *mut std::ffi::c_void)
    -> Result<(u64, [u8; 16]), String>
{
    use std::ffi::c_void;
    const FILE_ID_INFO_CLASS: i32 = 0x12;
    #[repr(C)]
    struct WinFileIdInfo {
        volume_serial_number: u64,
        file_id: [u8; 16],
    }
    #[link(name = "kernel32")]
    unsafe extern "system" {
        fn GetFileInformationByHandleEx(
            handle: *mut c_void,
            info_class: i32,
            info: *mut c_void,
            size: u32,
        ) -> i32;
    }
    let mut info = std::mem::MaybeUninit::<WinFileIdInfo>::uninit();
    // SAFETY: FileIdInfo (0x12) expects a writable FILE_ID_INFO layout of
    // 8-byte volume serial + 16-byte identifier; no ownership of HANDLE.
    let result = unsafe {
        GetFileInformationByHandleEx(
            handle,
            FILE_ID_INFO_CLASS,
            info.as_mut_ptr().cast::<c_void>(),
            std::mem::size_of::<WinFileIdInfo>() as u32,
        )
    };
    if result == 0 {
        return Err(format!("STOP: FileIdInfo 128 unavailable: {}", std::io::Error::last_os_error()));
    }
    let info = unsafe { info.assume_init() };
    Ok((info.volume_serial_number, info.file_id))
}

#[cfg(windows)]
fn windows_fixture_file_id_128(handle: &fs::File) -> Result<(u64, [u8; 16]), String> {
    use std::os::windows::io::AsRawHandle;
    windows_fixture_raw_file_id_128(handle.as_raw_handle())
}

// Observe SQLite's *actual* Windows VFS file handle after xOpen. This is a
// test-only diagnostic, not a pre-open authorization and not a defense against
// changes to the surrounding namespace or SQLite journal/sidecar paths.
#[cfg(windows)]
fn sqlite_windows_fixture_opened_identity(db: &Connection) -> Result<(u32, u64), String> {
    windows_fixture_raw_handle_identity(sqlite_windows_fixture_native_handle(db)?)
}

#[cfg(windows)]
fn sqlite_windows_fixture_native_handle(db: &Connection) -> Result<*mut std::ffi::c_void, String> {
    use std::ffi::{c_char, c_void};
    let mut native_handle: *mut c_void = std::ptr::null_mut();
    // SAFETY: db remains alive during the call; "main" is NUL terminated;
    // the Windows VFS fills our pointer-sized native HANDLE, which is borrowed
    // only for GetFileInformationByHandle before db is dropped. Never close it.
    let code = unsafe {
        rusqlite::ffi::sqlite3_file_control(
            db.handle(),
            b"main\0".as_ptr().cast::<c_char>(),
            rusqlite::ffi::SQLITE_FCNTL_WIN32_GET_HANDLE,
            (&mut native_handle as *mut *mut c_void).cast::<c_void>(),
        )
    };
    if code != rusqlite::ffi::SQLITE_OK || native_handle.is_null() {
        return Err(format!("STOP: SQLite Windows VFS native handle unavailable: {code}"));
    }
    Ok(native_handle)
}

#[cfg(windows)]
fn sqlite_windows_fixture_opened_file_id_128(db: &Connection)
    -> Result<(u64, [u8; 16]), String>
{
    windows_fixture_raw_file_id_128(sqlite_windows_fixture_native_handle(db)?)
}

// The caller cannot perform application SQL before this identity comparison.
// However, SQLite xOpen HAS ALREADY happened; it may have opened a substituted
// file. This helper deliberately makes no pre-xOpen or atomicity claim.
#[cfg(windows)]
fn open_windows_fixture_with_post_xopen_identity_check(
    path: &Path, expected: (u32, u64),
) -> Result<Connection, String> {
    let db = Connection::open_with_flags(path, OpenFlags::SQLITE_OPEN_READ_WRITE)
        .map_err(|e| format!("STOP: SQLite could not open test-only file: {e}"))?;
    if sqlite_windows_fixture_opened_identity(&db)? != expected {
        return Err("STOP: SQLite VFS opened a different fixture file identity".to_owned());
    }
    Ok(db)
}

#[cfg(windows)]
fn open_windows_fixture_directory(path: &Path) -> Result<fs::File, String> {
    use std::os::windows::fs::OpenOptionsExt;
    const FILE_FLAG_BACKUP_SEMANTICS: u32 = 0x0200_0000;
    const FILE_FLAG_OPEN_REPARSE_POINT: u32 = 0x0020_0000;
    const FILE_READ_ATTRIBUTES: u32 = 0x0000_0080;
    fs::OpenOptions::new()
        .access_mode(FILE_READ_ATTRIBUTES)
        .share_mode(0x0000_0001 | 0x0000_0002)
        .custom_flags(FILE_FLAG_BACKUP_SEMANTICS | FILE_FLAG_OPEN_REPARSE_POINT)
        .open(path)
        .map_err(|e| format!("STOP: cannot inspect fixture ancestor: {e}"))
}

// Pin only test-owned root-to-parent handles, with no claim that handles freeze
// the directory *name*. Every later admission must revalidate against them.
#[cfg(windows)]
fn pin_checked_fixture_chain(root: &Path, destination: &Path)
    -> Result<Vec<fs::File>, String>
{
    use std::os::windows::fs::MetadataExt;
    const FILE_ATTRIBUTE_REPARSE_POINT: u32 = 0x0000_0400;
    let paths = checked_fixture_parent_chain(root, destination)?;
    let mut pins = Vec::with_capacity(paths.len());
    for parent in paths {
        let before = fs::symlink_metadata(&parent)
            .map_err(|e| format!("STOP: cannot inspect fixture ancestor: {e}"))?;
        if !before.is_dir() || before.file_attributes() & FILE_ATTRIBUTE_REPARSE_POINT != 0 {
            return Err("STOP: non-directory or reparse fixture ancestor".to_owned());
        }
        let before_handle = open_windows_fixture_directory(&parent)?;
        let before_id = windows_fixture_handle_identity(&before_handle)?;
        drop(before_handle);
        let pin = open_windows_fixture_directory(&parent)?;
        let held_id = windows_fixture_handle_identity(&pin)?;
        let held = pin.metadata()
            .map_err(|e| format!("STOP: held ancestor metadata unavailable: {e}"))?;
        let after_handle = open_windows_fixture_directory(&parent)?;
        let after_id = windows_fixture_handle_identity(&after_handle)?;
        drop(after_handle);
        let after = fs::symlink_metadata(&parent)
            .map_err(|e| format!("STOP: ancestor changed after pin: {e}"))?;
        if !held.is_dir()
            || held.file_attributes() & FILE_ATTRIBUTE_REPARSE_POINT != 0
            || before.file_attributes() & FILE_ATTRIBUTE_REPARSE_POINT != 0
            || after.file_attributes() & FILE_ATTRIBUTE_REPARSE_POINT != 0
            || before_id != held_id
            || after_id != held_id
        {
            return Err("STOP: fixture ancestor identity or reparse mismatch".to_owned());
        }
        pins.push(pin);
    }
    Ok(pins)
}

// Fail closed on a *controlled prior* rename/replacement even if Win32 allowed
// the name to move while our directory handle stayed valid. NOT an atomic
// guarantee between this check and SQLite's separate path-based VFS xOpen.
#[cfg(windows)]
fn revalidate_checked_fixture_chain(root: &Path, destination: &Path, pins: &[fs::File])
    -> Result<(), String>
{
    use std::os::windows::fs::MetadataExt;
    const FILE_ATTRIBUTE_REPARSE_POINT: u32 = 0x0000_0400;
    let paths = checked_fixture_parent_chain(root, destination)?;
    if paths.len() != pins.len() {
        return Err("STOP: fixture ancestor handle count changed".to_owned());
    }
    for (parent, held_handle) in paths.iter().zip(pins.iter()) {
        let metadata = fs::symlink_metadata(parent)
            .map_err(|e| format!("STOP: held ancestor path vanished: {e}"))?;
        if !metadata.is_dir() || metadata.file_attributes() & FILE_ATTRIBUTE_REPARSE_POINT != 0 {
            return Err("STOP: replaced or reparse fixture ancestor".to_owned());
        }
        let reopened = open_windows_fixture_directory(parent)?;
        if windows_fixture_handle_identity(&reopened)? != windows_fixture_handle_identity(held_handle)? {
            return Err("STOP: fixture ancestor name now resolves to another FileIndex".to_owned());
        }
    }
    Ok(())
}

fn create_closed_populated_v6(path: &Path) {
    let db = database::open_database(path).expect("create isolated v6 test fixture");
    db.execute_batch(r#"
        INSERT INTO universes(id,name) VALUES ('u1','Aurora');
        INSERT INTO series(id,universe_id,name,sort_order)
            VALUES ('series1','u1','Eclipse arc',0);
        INSERT INTO novels(id,universe_id,series_id,title,sort_order)
            VALUES ('n1','u1','series1','Ancient Tales',0);
        INSERT INTO chapters(id,novel_id,title,sort_order)
            VALUES ('c1','n1','Dawn',0);
        INSERT INTO scenes(id,chapter_id,title,sort_order)
            VALUES ('s1','c1','Old scene',0);
        INSERT INTO scene_text_revisions(id,scene_id,revision_number,content)
            VALUES ('r1','s1',1,'Éclipse 🌕 dans la forêt');
        INSERT INTO scene_revision_heads(scene_id,revision_id)
            VALUES ('s1','r1');
        INSERT INTO narrative_entities(id,universe_id,kind,name)
            VALUES ('e1','u1','event','Éclipse');
        INSERT INTO entity_aliases(id,entity_id,universe_id,alias)
            VALUES ('a1','e1','u1','The lunar eclipse');
        INSERT INTO narrative_facts(id,entity_id,universe_id,fact_key,fact_value,provenance_kind)
            VALUES ('f1','e1','u1','state','confirmed','sourced');
        INSERT INTO fact_sources(id,fact_id,universe_id,revision_id,start_byte,end_byte,quoted_text)
            VALUES ('src1','f1','u1','r1',0,8,'Éclipse');
        INSERT INTO fact_review_events
            (id,fact_id,universe_id,revision_number,previous_status,next_status,
             action_kind,actor_kind,reviewer_label,human_confirmation,reason)
            VALUES
            ('rev1','f1','u1',1,'draft','suggestion','set_status','human','writer',0,'First review'),
            ('rev2','f1','u1',2,'suggestion','canon','approve_canon','human','writer',1,'Approved');
    "#).expect("legacy hierarchy, revisions, human review");
    assert_eq!(database::current_schema_version(&db).unwrap(), 6);
    drop(db); // Deliberately close before file copy: NEVER copy a live SQLite file.
}

fn opened_read_only_v6(path: &Path) -> Connection {
    let db = Connection::open_with_flags(path, OpenFlags::SQLITE_OPEN_READ_ONLY)
        .expect("read-only closed fixture");
    database::configure_connection(&db).expect("foreign keys on the connection");
    inspect_v6(&db).expect("six accepted migrations, integrity and table counts");
    db
}

fn checked_m2_snapshot(db: &Connection) -> (String, String, String, i64) {
    db.query_row(
        "SELECT r.content, h.revision_id,
                (SELECT next_status FROM fact_review_events
                 WHERE fact_id='f1' ORDER BY revision_number DESC LIMIT 1),
                (SELECT COUNT(*) FROM fact_review_events)
         FROM scene_text_revisions r
         JOIN scene_revision_heads h ON h.revision_id=r.id
         WHERE r.id='r1'",
        [], |row| Ok((row.get(0)?, row.get(1)?, row.get(2)?, row.get(3)?)),
    ).expect("M2 source, current revision and human canon history")
}

// Complete, type-tagged, order-independent snapshots of all *existing* v6 data.
// The extra v7 migration ledger row is deliberately excluded, never old ones.
fn legacy_rows(db: &Connection) -> BTreeMap<&'static str, Vec<Vec<String>>> {
    const TABLES: [&str; 14] = [
        "app_metadata", "schema_migrations", "universes", "series",
        "novels", "chapters", "scenes", "scene_text_revisions",
        "scene_revision_heads", "narrative_entities", "entity_aliases",
        "narrative_facts", "fact_sources", "fact_review_events",
    ];
    fn hex(bytes: &[u8]) -> String {
        bytes.iter().map(|byte| format!("{byte:02x}")).collect()
    }
    let mut output = BTreeMap::new();
    for table in TABLES {
        // Identifier is from the compile-time constant array above; no SQL injection.
        let clause = if table == "schema_migrations" {
            " WHERE version <= 6"
        } else {
            ""
        };
        let sql = format!("SELECT * FROM \"{table}\"{clause}");
        let mut stmt = db.prepare(&sql).expect("read legacy table");
        let width = stmt.column_count();
        let mut rows = stmt.query_map([], |row| {
            let mut cells = Vec::with_capacity(width);
            for index in 0..width {
                let cell = match row.get_ref(index)? {
                    ValueRef::Null => "N".to_string(),
                    ValueRef::Integer(value) => format!("I:{value}"),
                    ValueRef::Real(value) => format!("F:{:016x}", value.to_bits()),
                    ValueRef::Text(value) => format!("T:{}", hex(value)),
                    ValueRef::Blob(value) => format!("B:{}", hex(value)),
                };
                cells.push(cell);
            }
            Ok(cells)
        }).expect("query legacy rows")
        .collect::<rusqlite::Result<Vec<_>>>()
        .expect("collect legacy rows");
        rows.sort_unstable(); // Row order is not semantic in a relational table.
        output.insert(table, rows);
    }
    output
}

fn integrity(db: &Connection) {
    let result: String = db.query_row(
        "PRAGMA integrity_check", [], |row| row.get(0)
    ).expect("integrity");
    assert_eq!(result, "ok");
    let failed: i64 = db.query_row(
        "SELECT COUNT(*) FROM pragma_foreign_key_check",
        [], |row| row.get(0),
    ).expect("foreign key issues");
    assert_eq!(failed, 0);
}

#[test]
fn offline_copy_rehearsal_retains_original_v6_and_human_review() {
    let root = DisposableRoot::new("populated");
    let active_simulation = root.file("closed-source-v6.sqlite3");
    let sealed_simulation = root.file("sealed-before-v7.sqlite3");
    let copy = root.file("migration-candidate-v7.sqlite3");

    create_closed_populated_v6(&active_simulation);
    let before_bytes = fs::read(&active_simulation).expect("source bytes");
    fs::copy(&active_simulation, &sealed_simulation).expect("closed fixture sealed");
    fs::copy(&active_simulation, &copy).expect("disposable migration copy");

    let original_db = opened_read_only_v6(&active_simulation);
    let original_snapshot = checked_m2_snapshot(&original_db);
    let all_original_rows = legacy_rows(&original_db);
    assert_eq!(all_original_rows.len(), 14);
    assert!(all_original_rows.values().all(|rows| !rows.is_empty()),
        "populated fixture must exercise all 14 legacy v6 tables");
    drop(original_db);

    let mut candidate = Connection::open(&copy).expect("new copy only");
    database::configure_connection(&candidate).expect("FKs");
    {
        let tx = candidate.transaction().expect("migration atomic transaction");
        tx.execute_batch(CANDIDATE_SQL).expect("candidate schema in COPY ONLY");
        tx.execute(
            "INSERT INTO schema_migrations(version,name)
             VALUES (7,'007_create_world_time_foundation')", [],
        ).expect("simulated v7 row in COPY ONLY");
        tx.commit().expect("commit new copy");
    }
    assert_eq!(database::current_schema_version(&candidate).unwrap(), 7);
    assert_eq!(checked_m2_snapshot(&candidate), original_snapshot);
    assert_eq!(legacy_rows(&candidate), all_original_rows,
        "every original v6 row and typed value must be preserved");
    integrity(&candidate);
    let strict_count: i64 = candidate.query_row(
        "SELECT COUNT(*) FROM pragma_table_list
         WHERE name IN ('fictional_calendars','world_time_anchors','world_time_precedences')
           AND strict=1",
        [], |row| row.get(0),
    ).expect("three strict tables");
    assert_eq!(strict_count, 3);
    // An active v6 preflight must REFUSE a candidate schema/v7 database.
    assert_eq!(inspect_v6(&candidate), Err(PreflightFailure::UnexpectedVersion(7)));
    drop(candidate);

    let untouched = opened_read_only_v6(&active_simulation);
    assert_eq!(checked_m2_snapshot(&untouched), original_snapshot);
    assert_eq!(legacy_rows(&untouched), all_original_rows);
    drop(untouched);
    assert_eq!(fs::read(&active_simulation).unwrap(), before_bytes);
    assert_eq!(fs::read(&sealed_simulation).unwrap(), before_bytes);
}

#[test]
fn failed_copy_migration_rollback_keeps_v6_and_original_unchanged() {
    let root = DisposableRoot::new("rollback");
    let source = root.file("source-v6.sqlite3");
    let candidate_path = root.file("candidate.sqlite3");
    create_closed_populated_v6(&source);
    let original_bytes = fs::read(&source).expect("source before");
    fs::copy(&source, &candidate_path).expect("closed v6 disposable copy");

    let mut candidate = Connection::open(&candidate_path).expect("copy");
    database::configure_connection(&candidate).expect("FKs");
    let old = checked_m2_snapshot(&candidate);
    let before_rows = legacy_rows(&candidate);
    {
        let tx = candidate.transaction().expect("atomic migration");
        tx.execute_batch(CANDIDATE_SQL).expect("create new tables transactionally");
        // Intentional FK violation simulates an unacceptable migration step;
        // dropping tx must rollback all schema changes and the v7 marker.
        assert!(tx.execute(
            "INSERT INTO world_time_precedences
             (id,universe_id,before_anchor_id,after_anchor_id,reason)
             VALUES ('invalid','u1','missing-before','missing-after','fixture')",
            [],
        ).is_err());
    }
    assert_eq!(database::current_schema_version(&candidate).unwrap(), 6);
    inspect_v6(&candidate).expect("failed migration left v6 untouched");
    assert_eq!(checked_m2_snapshot(&candidate), old);
    assert_eq!(legacy_rows(&candidate), before_rows);
    integrity(&candidate);
    drop(candidate);

    assert_eq!(fs::read(&source).unwrap(), original_bytes);
    let untouched = opened_read_only_v6(&source);
    assert_eq!(checked_m2_snapshot(&untouched), old);
}

#[test]
fn empty_v6_copy_upgrades_to_three_strict_candidate_tables() {
    let root = DisposableRoot::new("empty");
    let source = root.file("empty-v6.sqlite3");
    let copy = root.file("empty-copy.sqlite3");
    let db = database::open_database(&source).expect("new v6 disposable database");
    assert_eq!(database::current_schema_version(&db).unwrap(), 6);
    drop(db);
    fs::copy(&source, &copy).expect("closed empty fixture copy");

    let mut db = Connection::open(&copy).expect("independent new copy");
    database::configure_connection(&db).expect("FKs");
    let tx = db.transaction().expect("atomic transaction");
    tx.execute_batch(CANDIDATE_SQL).expect("create schema");
    tx.execute(
        "INSERT INTO schema_migrations(version,name)
         VALUES (7,'007_create_world_time_foundation')", [],
    ).expect("simulated copy-only registry");
    tx.commit().expect("commit");
    assert_eq!(database::current_schema_version(&db).unwrap(), 7);
    integrity(&db);
    drop(db);
    let original = opened_read_only_v6(&source);
    assert_eq!(database::current_schema_version(&original).unwrap(), 6);
}

// First real-file M3.2 authoring persistence witness, still *only* on two
// disposable databases freshly created by this Rust test. No Tauri command,
// no operator/Greenfield profile, no activation and no production migration registration.
// This does NOT qualify an application v7 opener or writer IPC.
#[test]
fn m32_new_only_disposable_v7_chronology_survives_reopen_without_touching_prior_v6() {
    let root = DisposableRoot::new("m32-new-only-persistence");
    let prior_v6 = root.file("prior-fresh-v6-untouched.sqlite3");
    let new_v7 = root.file("m32-new-project-v7-candidate.sqlite3");
    assert!(!new_v7.exists(), "the chronology candidate requires a new file");

    create_closed_populated_v6(&prior_v6);
    let prior_bytes = fs::read(&prior_v6).expect("sealed previous new-project fixture");

    // Independently create an entirely NEW store, never copy or migrate the
    // prior file; v1..v6 first, explicit v7 candidate only in this owned file.
    create_closed_populated_v6(&new_v7);
    let mut db = Connection::open_with_flags(&new_v7, OpenFlags::SQLITE_OPEN_READ_WRITE)
        .expect("open newly owned candidate only");
    database::configure_connection(&db).expect("foreign keys for new candidate");
    let original_m2 = checked_m2_snapshot(&db);
    {
        let tx = db.transaction().expect("candidate transaction");
        tx.execute_batch(CANDIDATE_SQL).expect("M3.1 tables only in new disposable file");
        tx.execute_batch(M32_DECISIONS_SQL)
            .expect("M3.2 immutable decisions only in new disposable file");
        tx.execute("INSERT INTO schema_migrations(version,name)
                    VALUES (7,'007_create_world_time_foundation')", [])
            .expect("record test-only v7 candidate version in new file");
        tx.commit().expect("candidate stage commits atomically");
    }
    assert_eq!(database::current_schema_version(&db).unwrap(), 7);
    db.execute("INSERT INTO universes(id,name) VALUES('u2','Second fictional universe')", [])
        .expect("another brand-new universe");
    // Baseline the newly authored u2 row too: no subsequent chronology decision
    // may rewrite even this fixture's established v6-shaped tables.
    let original_rows = legacy_rows(&db);
    chronology::create_calendar(&db, "m32-cycle", "u1", "Cycles", "Fiction only")
        .expect("manual calendar");
    let exact = chronology::AnchorDraft {
        id: "m32-exact", universe_id: "u1", time_kind: "exact",
        calendar_id: Some("m32-cycle"), event_entity_id: Some("e1"),
        source_revision_id: Some("r1"), exact_label: Some("Cycle XII"),
        window_start_text: None, window_end_text: None, precision_text: Some("day"),
    };
    chronology::create_anchor(&db, exact).expect("manual historical-revision binding");
    let unknown = chronology::AnchorDraft {
        id: "m32-unknown", universe_id: "u1", time_kind: "unknown",
        calendar_id: None, event_entity_id: None, source_revision_id: None,
        exact_label: None, window_start_text: None, window_end_text: None,
        precision_text: None,
    };
    chronology::create_anchor(&db, unknown).expect("undated event");
    chronology::create_precedence(
        &db, "m32-before", "u1", "m32-exact", "m32-unknown",
        "Author explicitly placed the event before", Some("r1"),
    ).expect("human before/after constraint");
    assert!(chronology::create_precedence(
        &db, "m32-cycle-refused", "u1", "m32-unknown", "m32-exact",
        "Invalid cycle", Some("r1"),
    ).is_err(), "a temporal cycle must be rejected in the file, not only RAM");
    let foreign = chronology::AnchorDraft {
        id: "m32-u2", universe_id: "u2", time_kind: "relative", ..unknown
    };
    chronology::create_anchor(&db, foreign).expect("second universe independent");
    assert!(chronology::create_precedence(
        &db, "m32-cross-refused", "u1", "m32-exact", "m32-u2",
        "Wrong universe", None,
    ).is_err(), "no cross-universe ordering");

    let replacement = chronology::AnchorDraft {
        id: "m32-corrected", exact_label: Some("Cycle XIII"), ..exact
    };
    chronology::supersede_anchor_atomically(
        &mut db, replacement, "m32-decision", "m32-exact",
        "Human correction without editing history", Some("r1"),
    ).expect("atomic human correction in new file");
    assert_eq!(chronology::list_current_anchor_ids(&db, "u1").unwrap(),
               vec!["m32-corrected", "m32-unknown"]);
    assert_eq!(chronology::list_anchors(&db, "u1").unwrap().len(), 3);
    assert_eq!(checked_m2_snapshot(&db), original_m2);
    assert_eq!(legacy_rows(&db), original_rows);
    integrity(&db);
    drop(db);

    // Simulated app exit and a new, explicit connection to this known-owned
    // test file. NEVER call the normal migration-capable app opener on v7.
    let reopened = Connection::open_with_flags(&new_v7, OpenFlags::SQLITE_OPEN_READ_WRITE)
        .expect("reopen same candidate path after closing");
    database::configure_connection(&reopened).expect("new connection FK guard");
    assert_eq!(database::current_schema_version(&reopened).unwrap(), 7);
    assert_eq!(chronology::list_precedences(&reopened, "u1").unwrap().len(), 1);
    assert_eq!(chronology::list_anchor_decisions(&reopened, "u1").unwrap().len(), 1);
    assert_eq!(chronology::list_current_anchor_ids(&reopened, "u1").unwrap(),
               vec!["m32-corrected", "m32-unknown"]);
    assert_eq!(checked_m2_snapshot(&reopened), original_m2);
    assert_eq!(legacy_rows(&reopened), original_rows);
    integrity(&reopened);
    drop(reopened);
    assert_eq!(fs::read(&prior_v6).unwrap(), prior_bytes,
               "separate earlier v6 fixture bytes must never change");
    assert!(!root.file("activation").exists(), "no activation marker switched");
}

#[test]
fn m32_new_only_claim_refuses_existing_file_directory_and_orphan_sidecars() {
    let root = DisposableRoot::new("m32-exclusive-refusals");
    let earlier = root.file("preexisting-v6.sqlite3");
    create_closed_populated_v6(&earlier);
    let earlier_bytes = fs::read(&earlier).unwrap();
    let marker = root.file("activation");
    fs::write(&marker, b"do-not-change-existing-activation").unwrap();
    let marker_bytes = fs::read(&marker).unwrap();

    assert!(open_new_only_disposable_file(&earlier).is_err(),
            "a healthy existing v6 project is still an occupied destination");
    let arbitrary = root.file("occupied-unspecified.sqlite3");
    fs::write(&arbitrary, b"not SQLite and not ours to replace").unwrap();
    let arbitrary_bytes = fs::read(&arbitrary).unwrap();
    assert!(open_new_only_disposable_file(&arbitrary).is_err(),
            "a non-SQLite file must also refuse exclusive creation");
    let directory = root.file("directory.sqlite3");
    fs::create_dir(&directory).unwrap();
    assert!(open_new_only_disposable_file(&directory).is_err());
    assert!(directory.is_dir());
    let absent_parent = root.file("uncreated-parent").join("new.sqlite3");
    assert!(open_new_only_disposable_file(&absent_parent).is_err(),
            "never silently construct a caller-selected parent directory");
    assert!(!absent_parent.parent().unwrap().exists());

    for suffix in ["-wal", "-shm", "-journal"] {
        let destination = root.file(&format!("separate-{suffix}.sqlite3"));
        let mut sidecar_name = destination.as_os_str().to_os_string();
        sidecar_name.push(suffix);
        let sidecar = PathBuf::from(sidecar_name);
        fs::write(&sidecar, b"existing sidecar must never be replayed").unwrap();
        let sidecar_bytes = fs::read(&sidecar).unwrap();
        assert!(open_new_only_disposable_file(&destination).is_err(),
                "orphan WAL/SHM/journal must block new-file ownership claim");
        assert!(!destination.exists(), "refusal must not even create a DB placeholder");
        assert_eq!(fs::read(&sidecar).unwrap(), sidecar_bytes);
    }
    assert_eq!(fs::read(&earlier).unwrap(), earlier_bytes);
    assert_eq!(fs::read(&arbitrary).unwrap(), arbitrary_bytes);
    assert_eq!(fs::read(&marker).unwrap(), marker_bytes);
}

#[test]
fn m32_exclusive_new_file_claim_builds_test_only_v7_and_reopen_cannot_reclaim_it() {
    let root = DisposableRoot::new("m32-exclusive-v7-initialization");
    let previous = root.file("other-prior-v6.sqlite3");
    create_closed_populated_v6(&previous);
    let previous_bytes = fs::read(&previous).unwrap();
    let destination = root.file("never-before-used.sqlite3");

    let mut db = open_new_only_disposable_file(&destination)
        .expect("claim a genuinely absent test-only filename");
    assert_eq!(database::run_migrations(&mut db).unwrap(), 6,
               "normal migrations stop at v6, on this newly owned file only");
    {
        let tx = db.transaction().unwrap();
        tx.execute_batch(CANDIDATE_SQL).unwrap();
        tx.execute_batch(M32_DECISIONS_SQL).unwrap();
        tx.execute("INSERT INTO schema_migrations(version,name)
                    VALUES(7,'007_create_world_time_foundation')", []).unwrap();
        tx.commit().unwrap();
    }
    db.execute("INSERT INTO universes(id,name) VALUES('new-only-u','Owned fiction')", [])
        .unwrap();
    chronology::create_anchor(&db, chronology::AnchorDraft {
        id: "owned-unknown", universe_id: "new-only-u", time_kind: "unknown",
        calendar_id: None, event_entity_id: None, source_revision_id: None,
        exact_label: None, window_start_text: None, window_end_text: None,
        precision_text: None,
    }).unwrap();
    integrity(&db);
    drop(db);

    let new_bytes = fs::read(&destination).unwrap();
    assert!(open_new_only_disposable_file(&destination).is_err(),
            "the exclusive *creation* gate must never double as an existing-v7 opener");
    assert_eq!(fs::read(&destination).unwrap(), new_bytes);
    let reopened = Connection::open_with_flags(&destination, OpenFlags::SQLITE_OPEN_READ_WRITE)
        .expect("explicit known-owned test fixture readback, not exclusive create");
    database::configure_connection(&reopened).unwrap();
    assert_eq!(database::current_schema_version(&reopened).unwrap(), 7);
    assert_eq!(chronology::list_current_anchor_ids(&reopened, "new-only-u").unwrap(),
               vec!["owned-unknown"]);
    integrity(&reopened);
    drop(reopened);
    assert_eq!(fs::read(&previous).unwrap(), previous_bytes,
               "previous independent v6 fixture must remain byte-identical");
    assert!(!root.file("activation").exists());
}

#[test]
fn m32_exclusive_claim_two_concurrent_creators_only_one_wins() {
    let root = DisposableRoot::new("m32-exclusive-creator-race");
    let destination = root.file("atomic-claim.sqlite3");
    let start = Arc::new(Barrier::new(3));
    let contenders: Vec<_> = (0..2).map(|_| {
        let barrier = Arc::clone(&start);
        let path = destination.clone();
        thread::spawn(move || {
            barrier.wait();
            open_new_only_disposable_file(&path).is_ok()
        })
    }).collect();
    start.wait();
    let accepted = contenders.into_iter()
        .map(|worker| worker.join().expect("no panic in owned race"))
        .filter(|won| *won)
        .count();
    assert_eq!(accepted, 1, "OS create_new must reject one of two simultaneous claims");
    assert!(destination.exists());
    assert!(!root.file("activation").exists());
}

#[test]
fn m32_unpinned_parent_name_can_be_replaced_before_new_only_claim() {
    let root = DisposableRoot::new("m32-parent-namespace-counterexample");
    let parent = root.file("claimed-parent");
    let displaced_parent = root.file("displaced-parent");
    fs::create_dir(&parent).unwrap();
    let original_token = parent.join("identity-token");
    fs::write(&original_token, b"original fixture parent").unwrap();
    let destination = parent.join("new-only-v7.sqlite3");
    assert!(destination.parent().unwrap().is_dir());

    // Simulate a rename between a caller's parent check and an eventual open.
    // Both directories remain under this one disposable test root. A path
    // string is not an authenticated directory identity.
    fs::rename(&parent, &displaced_parent).unwrap();
    fs::create_dir(&parent).unwrap();
    let db = open_new_only_disposable_file(&destination)
        .expect("the current fixture gate cannot authenticate an earlier parent");
    drop(db);
    assert!(destination.exists(), "the different parent received the new file");
    assert!(!displaced_parent.join("new-only-v7.sqlite3").exists());
    assert_eq!(fs::read(displaced_parent.join("identity-token")).unwrap(),
               b"original fixture parent");
    assert!(!parent.join("identity-token").exists());
    // NEGATIVE witness: future production admission MUST veto root replacement.
}

#[cfg(windows)]
#[test]
fn m32_windows_pinned_fixture_parent_and_claim_refuse_rename_during_open() {
    let root = DisposableRoot::new("m32-pinned-windows-handoff");
    let parent = root.file("owned-test-parent");
    fs::create_dir(&parent).unwrap();
    let destination = parent.join("exclusive.sqlite3");
    let pinned_parent = pin_disposable_parent(&destination).unwrap();
    let claim = claim_new_only_disposable_file(&destination).unwrap();
    assert!(fs::rename(&parent, root.file("redirected-parent")).is_err(),
            "an open no-delete-share parent handle should block its rename");
    assert!(fs::rename(&destination, parent.join("substituted.sqlite3")).is_err(),
            "an open no-delete-share file handle should block its rename");
    let db = connect_claimed_disposable_file(&destination, claim)
        .expect("SQLite RW must coexist with the no-delete-share claim");
    assert_eq!(database::current_schema_version(&db).unwrap_or(0), 0);
    drop(db);
    drop(pinned_parent);
    assert!(destination.exists());
    assert!(!parent.join("substituted.sqlite3").exists());
    assert!(!root.file("redirected-parent").exists());
}

#[test]
fn m32_owned_fixture_path_guard_refuses_escape_and_unsafe_components() {
    let root = DisposableRoot::new("m32-owned-path-lexical-guard");
    let nested = root.file("project_new");
    fs::create_dir(&nested).unwrap();
    let destination = nested.join("new_v7.sqlite3");
    assert_eq!(checked_fixture_parent_chain(&root.0, &destination).unwrap(),
               vec![root.0.clone(), nested.clone()]);
    let parent_escape = nested.join("..").join("outside.sqlite3");
    assert!(checked_fixture_parent_chain(&root.0, &parent_escape).is_err(),
            "an internal .. segment must veto before OS creation");
    assert!(checked_fixture_parent_chain(&root.0, &root.file("root-only.sqlite3")).is_err());
    assert!(checked_fixture_parent_chain(&root.0, &nested.join("stream:ads.sqlite3")).is_err());
    assert!(checked_fixture_parent_chain(&root.0, &nested.join("CON.sqlite3")).is_err());
    assert!(checked_fixture_parent_chain(&root.0, &nested.join("wrong.db")).is_err());
    assert!(checked_fixture_parent_chain(
        &root.0, &std::env::temp_dir().join("outside-fixture.sqlite3")
    ).is_err());
    assert!(!destination.exists());
    assert!(!root.file("outside.sqlite3").exists());
}

#[cfg(windows)]
#[test]
fn m32_windows_owned_fixture_chain_rechecks_substitution_before_sqlite() {
    let root = DisposableRoot::new("m32-owned-chain-fileid");
    let first = root.file("project_new");
    let second = first.join("nested");
    fs::create_dir(&first).unwrap();
    fs::create_dir(&second).unwrap();
    let destination = second.join("new_v7.sqlite3");
    let pins = pin_checked_fixture_chain(&root.0, &destination)
        .expect("all fixture-owned ancestors expose stable Windows FileIndex");
    assert_eq!(pins.len(), 3);
    revalidate_checked_fixture_chain(&root.0, &destination, &pins)
        .expect("clean fixture still resolves to its held ancestors");
    let renamed_leaf = first.join("replaced_nested");
    // The empty leaf was actually movable despite a held no-DELETE-share
    // handle on Windows Server 2025 (#40499869627, #40501278786). If this
    // runner permits it, restore the SAME NAME with a DIFFERENT directory and
    // demand a STOP rather than claiming the handles prevented substitution.
    let was_renamed = fs::rename(&second, &renamed_leaf).is_ok();
    if was_renamed {
        fs::create_dir(&second).expect("disposable replacement leaf only");
        assert_ne!(
            windows_fixture_handle_identity(&pins[2]).unwrap(),
            windows_fixture_handle_identity(&open_windows_fixture_directory(&second).unwrap()).unwrap(),
            "a newly created directory must not inherit the held leaf identity"
        );
        assert!(revalidate_checked_fixture_chain(&root.0, &destination, &pins).is_err(),
                "rename plus replacement MUST cause refusal before SQLite xOpen");
        assert!(!destination.exists());
        assert!(!renamed_leaf.join("new_v7.sqlite3").exists());
    } else {
        assert!(revalidate_checked_fixture_chain(&root.0, &destination, &pins).is_ok(),
                "if the OS vetoes rename, the original chain must remain intact");
    }
    drop(pins);

    // Independent positive witness, with a pristine new-only disposable root:
    // revalidation is a separate check, NOT an atomic SQLite VFS admission.
    let clean = DisposableRoot::new("m32-owned-chain-pristine-v7");
    let clean_first = clean.file("project_new");
    let clean_second = clean_first.join("nested");
    fs::create_dir(&clean_first).unwrap();
    fs::create_dir(&clean_second).unwrap();
    let clean_destination = clean_second.join("new_v7.sqlite3");
    let clean_pins = pin_checked_fixture_chain(&clean.0, &clean_destination).unwrap();
    revalidate_checked_fixture_chain(&clean.0, &clean_destination, &clean_pins).unwrap();
    let claim = claim_new_only_disposable_file(&clean_destination).unwrap();
    let db = connect_claimed_disposable_file(&clean_destination, claim)
        .expect("SQLite may open a separate pristine disposable fixture");
    assert_eq!(database::current_schema_version(&db).unwrap_or(0), 0);
    revalidate_checked_fixture_chain(&clean.0, &clean_destination, &clean_pins).unwrap();
    drop(db);
    drop(clean_pins);
    assert!(clean_destination.exists());
    assert!(!destination.exists());
}

#[cfg(windows)]
#[test]
fn m32_windows_sqlite_vfs_handle_matches_live_exclusive_fixture_claim() {
    let root = DisposableRoot::new("m32-sqlite-native-handle-pristine");
    let parent = root.file("project_new");
    fs::create_dir(&parent).unwrap();
    let destination = parent.join("new_v7.sqlite3");
    let pins = pin_checked_fixture_chain(&root.0, &destination).unwrap();
    revalidate_checked_fixture_chain(&root.0, &destination, &pins).unwrap();
    let claim = claim_new_only_disposable_file(&destination).unwrap();
    let claim_id = windows_fixture_handle_identity(&claim).unwrap();
    let db = open_windows_fixture_with_post_xopen_identity_check(&destination, claim_id)
        .expect("native SQLite VFS handle must refer to the claimed fixture file");
    assert_eq!(sqlite_windows_fixture_opened_identity(&db).unwrap(), claim_id);
    assert_eq!(db.query_row("SELECT 1", [], |row| row.get::<_, i64>(0)).unwrap(), 1);
    revalidate_checked_fixture_chain(&root.0, &destination, &pins).unwrap();
    drop(db);
    drop(claim);
    drop(pins);
    assert!(!root.file("activation").exists());
    assert!(!parent.join("new_v7.sqlite3-wal").exists());
    assert!(!parent.join("new_v7.sqlite3-shm").exists());
}

#[cfg(windows)]
#[test]
fn m32_windows_sqlite_vfs_native_handle_detects_post_check_name_substitution() {
    let root = DisposableRoot::new("m32-sqlite-native-handle-swap");
    let parent = root.file("project_new");
    fs::create_dir(&parent).unwrap();
    let destination = parent.join("new_v7.sqlite3");
    let displaced = parent.join("old_claimed_file.sqlite3");
    let pins = pin_checked_fixture_chain(&root.0, &destination).unwrap();
    let claim = claim_new_only_disposable_file(&destination).unwrap();
    let original_id = windows_fixture_handle_identity(&claim).unwrap();
    revalidate_checked_fixture_chain(&root.0, &destination, &pins).unwrap();

    // A controlled synthetic counterexample to the unchecked gap: release
    // our file-name claim, then move its name and put ANOTHER new file there,
    // *after* the earlier successful chain revalidation but BEFORE xOpen.
    // Both files and the replacement are exclusively fixture-owned.
    drop(claim);
    fs::rename(&destination, &displaced).unwrap();
    let substitute = claim_new_only_disposable_file(&destination).unwrap();
    let substitute_id = windows_fixture_handle_identity(&substitute).unwrap();
    assert_ne!(original_id, substitute_id, "substitution must be a distinct OS file");
    assert!(revalidate_checked_fixture_chain(&root.0, &destination, &pins).is_ok(),
            "unchanged parents alone cannot detect a swapped *file* name");
    assert!(open_windows_fixture_with_post_xopen_identity_check(&destination, original_id).is_err(),
            "SQLite xOpen follows the substituted name; native handle comparison must STOP");
    assert_eq!(windows_fixture_handle_identity(&substitute).unwrap(), substitute_id);
    assert_eq!(fs::read(&displaced).unwrap(), Vec::<u8>::new());
    assert_eq!(fs::read(&destination).unwrap(), Vec::<u8>::new());
    assert!(!root.file("activation").exists());
    drop(substitute);
    drop(pins);
}

#[cfg(windows)]
#[test]
fn m32_windows_sqlite_fileid_128_matches_claim_but_cannot_prevent_prior_swap() {
    let root = DisposableRoot::new("m32-win32-128-fileid-pristine");
    let parent = root.file("project_new");
    fs::create_dir(&parent).unwrap();
    let destination = parent.join("new_v7.sqlite3");
    let claim = claim_new_only_disposable_file(&destination).unwrap();
    let id_64 = windows_fixture_handle_identity(&claim).unwrap();
    let id_128 = windows_fixture_file_id_128(&claim).unwrap();
    let db = open_windows_fixture_with_post_xopen_identity_check(&destination, id_64).unwrap();
    assert_eq!(sqlite_windows_fixture_opened_file_id_128(&db).unwrap(), id_128,
               "held new-only OS claim and native SQLite VFS HANDLE must agree at 128 bits");
    assert_eq!(db.query_row("SELECT 1", [], |row| row.get::<_, i64>(0)).unwrap(), 1);
    drop(db);
    drop(claim);

    // Separate fixture: a successful PRE-xOpen parent check is not an
    // authenticated file binding. Relinquish the file claim intentionally,
    // then substitute a distinct same-name file before SQLite xOpen.
    let swapped = DisposableRoot::new("m32-win32-128-fileid-swapped");
    let swapped_parent = swapped.file("project_new");
    fs::create_dir(&swapped_parent).unwrap();
    let path = swapped_parent.join("new_v7.sqlite3");
    let moved = swapped_parent.join("old_claimed_file.sqlite3");
    let pins = pin_checked_fixture_chain(&swapped.0, &path).unwrap();
    let original = claim_new_only_disposable_file(&path).unwrap();
    let original_id = windows_fixture_file_id_128(&original).unwrap();
    revalidate_checked_fixture_chain(&swapped.0, &path, &pins).unwrap();
    drop(original);
    fs::rename(&path, &moved).unwrap();
    let replacement = claim_new_only_disposable_file(&path).unwrap();
    let replacement_id = windows_fixture_file_id_128(&replacement).unwrap();
    assert_ne!(original_id, replacement_id);
    revalidate_checked_fixture_chain(&swapped.0, &path, &pins).unwrap();
    let followed = Connection::open_with_flags(&path, OpenFlags::SQLITE_OPEN_READ_WRITE).unwrap();
    assert_eq!(sqlite_windows_fixture_opened_file_id_128(&followed).unwrap(), replacement_id);
    assert_ne!(sqlite_windows_fixture_opened_file_id_128(&followed).unwrap(), original_id,
               "128-bit FileId detects the ALREADY OPENED substitution, not a prevented xOpen");
    drop(followed);
    assert_eq!(fs::read(&moved).unwrap(), Vec::<u8>::new());
    assert_eq!(fs::read(&path).unwrap(), Vec::<u8>::new());
    assert!(!swapped.file("activation").exists());
    drop(replacement);
    drop(pins);
}


#[test]
fn wal_live_fixture_vacuum_into_produces_consistent_v6_backup_without_raw_file_copy() {
    let root = DisposableRoot::new("wal-online-backup");
    let live = root.file("wal-live-source-v6.sqlite3");
    let consistent = root.file("wal-vacuum-into-backup.sqlite3");

    let db = database::open_database(&live).expect("owned disposable v6 DB");
    let journal_mode: String = db.query_row(
        "PRAGMA journal_mode=WAL", [], |row| row.get(0)
    ).expect("enable WAL only on owned fixture");
    assert_eq!(journal_mode.to_ascii_lowercase(), "wal");

    db.execute(
        "INSERT INTO universes(id,name) VALUES ('wal-u1','WAL 🌙 timeline')",
        [],
    ).expect("committed WAL universe");
    db.execute(
        "INSERT INTO narrative_entities(id,universe_id,kind,name)
         VALUES ('wal-event','wal-u1','event','Éclipse 🌙')",
        [],
    ).expect("committed WAL event");
    inspect_v6(&db).expect("v6 is valid while WAL source is open");
    let rows_before = legacy_rows(&db);

    // sqlite.org/lang_vacuum.html: VACUUM INTO creates a consistent snapshot
    // even when the source database is live and using WAL.
    assert!(!consistent.exists(), "new uniquely owned destination only");
    db.execute(
        "VACUUM INTO ?1",
        params![consistent.to_string_lossy().to_string()],
    ).expect("SQLite-consistent copy; NO fs::copy of open/live SQLite");

    // Inspect the backup while the source WAL connection is STILL open.
    let backup = opened_read_only_v6(&consistent);
    assert_eq!(legacy_rows(&backup), rows_before);
    integrity(&backup);
    drop(backup);

    let source_after = legacy_rows(&db);
    assert_eq!(source_after, rows_before, "snapshot creation must not mutate source");
    db.execute(
        "INSERT INTO narrative_entities(id,universe_id,kind,name)
         VALUES ('wal-later-event','wal-u1','event','Added after snapshot')",
        [],
    ).expect("commit another independent WAL record after backup");
    let changed_source_rows = legacy_rows(&db);
    assert_ne!(changed_source_rows, rows_before, "post-backup change must be observable");
    let stable_backup = opened_read_only_v6(&consistent);
    assert_eq!(legacy_rows(&stable_backup), rows_before,
        "sealed WAL backup must NOT include post-snapshot writes");
    drop(stable_backup);
    drop(db);
    let original = opened_read_only_v6(&live);
    assert_eq!(legacy_rows(&original), changed_source_rows);
}


// TEST-ONLY proof of semantics for a future explicitly authorized v7 entry point.
// No runtime automatic migration or production path invokes this function.
// Retrying a completed upgrade must be a validated no-op; forged registry rows
// and partially installed schemas must NOT be mistaken for completed migrations.
// Complete expected SQLite DDL inventory for the three candidate tables,
// including every index, trigger and internally generated UNIQUE autoindex.
// A v7 marker and three superficially STRICT tables alone are not trustworthy.
fn candidate_ddl_inventory(db: &Connection) -> Result<Vec<(String,String,String,String)>, String> {
    let mut statement = db.prepare(
        "SELECT type, name, tbl_name, COALESCE(sql,'')
         FROM sqlite_schema
         WHERE tbl_name IN (
           'fictional_calendars','world_time_anchors','world_time_precedences'
         ) ORDER BY type,name"
    ).map_err(|e| e.to_string())?;
    statement.query_map([], |row| {
        Ok((row.get(0)?,row.get(1)?,row.get(2)?,row.get(3)?))
    }).map_err(|e| e.to_string())?
        .collect::<rusqlite::Result<Vec<_>>>()
        .map_err(|e| e.to_string())
}

fn expected_candidate_ddl_inventory() -> Result<Vec<(String,String,String,String)>, String> {
    let mut reference = Connection::open_in_memory().map_err(|e| e.to_string())?;
    database::configure_connection(&reference).map_err(|e| e.to_string())?;
    database::run_migrations(&mut reference).map_err(|e| e.to_string())?;
    reference.execute_batch(CANDIDATE_SQL).map_err(|e| e.to_string())?;
    candidate_ddl_inventory(&reference)
}

// Retrying v7 must not silently accept a changed old v6 schema.
// Compare every legacy table, index, UNIQUE autoindex and trigger against
// fresh in-memory migrations 1..6, excluding only internal ANALYZE stats.
fn legacy_ddl_inventory(db: &Connection) -> Result<Vec<(String,String,String,String)>, String> {
    let mut statement = db.prepare(
        "SELECT type,name,tbl_name,COALESCE(sql,'')
         FROM sqlite_schema
         WHERE tbl_name NOT IN (
           'fictional_calendars','world_time_anchors','world_time_precedences'
         ) AND name NOT LIKE 'sqlite_stat%'
         ORDER BY type,name"
    ).map_err(|e| e.to_string())?;
    statement.query_map([], |row| {
        Ok((row.get(0)?,row.get(1)?,row.get(2)?,row.get(3)?))
    }).map_err(|e| e.to_string())?
        .collect::<rusqlite::Result<Vec<_>>>()
        .map_err(|e| e.to_string())
}

fn expected_legacy_ddl_inventory() -> Result<Vec<(String,String,String,String)>, String> {
    let mut reference = Connection::open_in_memory().map_err(|e| e.to_string())?;
    database::configure_connection(&reference).map_err(|e| e.to_string())?;
    database::run_migrations(&mut reference).map_err(|e| e.to_string())?;
    legacy_ddl_inventory(&reference)
}

fn apply_candidate_explicitly_once(db: &mut Connection) -> Result<bool, String> {
    let foreign_keys: i64 = db.query_row(
        "PRAGMA foreign_keys", [], |row| row.get(0)
    ).map_err(|e| e.to_string())?;
    if foreign_keys != 1 {
        return Err("foreign keys not enforced".to_string());
    }
    let version = database::current_schema_version(db).map_err(|e| e.to_string())?;
    match version {
        6 => {
            inspect_v6(db).map_err(|e| format!("v6 preflight blocked: {e:?}"))?;
            let tx = db.transaction().map_err(|e| e.to_string())?;
            tx.execute_batch(CANDIDATE_SQL).map_err(|e| e.to_string())?;
            tx.execute(
                "INSERT INTO schema_migrations(version,name)
                 VALUES (7,'007_create_world_time_foundation')", []
            ).map_err(|e| e.to_string())?;
            tx.commit().map_err(|e| e.to_string())?;
            Ok(true)
        }
        7 => {
            let entries: Vec<(i64, String)> = db.prepare(
                "SELECT version,name FROM schema_migrations ORDER BY version"
            ).map_err(|e| e.to_string())?
                .query_map([], |row| Ok((row.get(0)?,row.get(1)?)))
                .map_err(|e| e.to_string())?
                .collect::<rusqlite::Result<Vec<_>>>()
                .map_err(|e| e.to_string())?;
            const NAMES: [&str; 7] = [
                "001_create_app_metadata",
                "002_create_project_hierarchy",
                "003_create_scene_text_revisions",
                "004_create_narrative_entity_registry",
                "005_create_narrative_fact_provenance",
                "006_create_human_fact_review_log",
                "007_create_world_time_foundation",
            ];
            if entries.len() != NAMES.len()
                || entries.iter().enumerate().any(|(i, (version, name))| {
                    *version != i as i64 + 1 || name != NAMES[i]
                })
            {
                return Err("migration ledger mismatch".to_string());
            }
            let count: i64 = db.query_row(
                "SELECT COUNT(*) FROM pragma_table_list
                 WHERE name IN ('fictional_calendars',
                                'world_time_anchors',
                                'world_time_precedences') AND strict=1",
                [], |row| row.get(0)
            ).map_err(|e| e.to_string())?;
            if count != 3 {
                return Err("candidate v7 tables missing or non-STRICT".to_string());
            }
            if candidate_ddl_inventory(db)? != expected_candidate_ddl_inventory()? {
                return Err("candidate v7 schema DDL drift (table/index/trigger)".to_string());
            }
            if legacy_ddl_inventory(db)? != expected_legacy_ddl_inventory()? {
                return Err("legacy v6 schema DDL drift (table/index/trigger)".to_string());
            }
            let integrity: String = db.query_row(
                "PRAGMA integrity_check", [], |row| row.get(0)
            ).map_err(|e| e.to_string())?;
            let fk_broken: i64 = db.query_row(
                "SELECT COUNT(*) FROM pragma_foreign_key_check",
                [], |row| row.get(0)
            ).map_err(|e| e.to_string())?;
            if integrity != "ok" || fk_broken != 0 {
                return Err("candidate database integrity failed".to_string());
            }
            Ok(false)
        }
        _ => Err(format!("explicit candidate cannot handle schema {version}")),
    }
}

#[test]
fn explicit_candidate_is_idempotent_on_populated_disposable_copy() {
    let root = DisposableRoot::new("idempotence");
    let source = root.file("closed-original-v6.sqlite3");
    let copy = root.file("isolated-candidate.sqlite3");
    create_closed_populated_v6(&source);
    let original_bytes = fs::read(&source).expect("sealed original");
    fs::copy(&source, &copy).expect("closed fixture copy");

    let mut db = Connection::open(&copy).expect("disposable copy");
    database::configure_connection(&db).expect("FKs");
    let all_original = legacy_rows(&db);
    assert!(apply_candidate_explicitly_once(&mut db).expect("explicit first upgrade"));
    assert_eq!(database::current_schema_version(&db).unwrap(), 7);
    db.execute(
        "INSERT INTO world_time_anchors(id,universe_id,time_kind)
         VALUES ('fixture-anchor','u1','unknown')", []
    ).expect("new authored world-time assertion");

    let anchor_count: i64 = db.query_row(
        "SELECT COUNT(*) FROM world_time_anchors", [], |row| row.get(0)
    ).expect("anchor count");
    let before_changes: i64 = db.query_row(
        "SELECT total_changes()", [], |row| row.get(0)
    ).expect("change count");
    assert!(!apply_candidate_explicitly_once(&mut db).expect("validated second no-op"));
    let after_changes: i64 = db.query_row(
        "SELECT total_changes()", [], |row| row.get(0)
    ).expect("change count");
    assert_eq!(before_changes, after_changes);
    assert_eq!(db.query_row(
        "SELECT COUNT(*) FROM world_time_anchors", [], |row| row.get::<_, i64>(0)
    ).unwrap(), anchor_count);
    assert_eq!(db.query_row(
        "SELECT COUNT(*) FROM schema_migrations", [], |row| row.get::<_, i64>(0)
    ).unwrap(), 7);
    assert_eq!(legacy_rows(&db), all_original);
    integrity(&db);
    drop(db);

    assert_eq!(fs::read(&source).unwrap(), original_bytes);
    opened_read_only_v6(&source);
}

#[test]
fn explicit_candidate_rejects_forged_v7_and_unknown_versions() {
    let root = DisposableRoot::new("forged-ledger");
    let source = root.file("synthetic-v6.sqlite3");
    create_closed_populated_v6(&source);
    let mut db = Connection::open(&source).expect("disposable fixture");
    database::configure_connection(&db).expect("FKs");
    let before = legacy_rows(&db);
    db.execute(
        "INSERT INTO schema_migrations(version,name)
         VALUES (7,'007_create_world_time_foundation')", []
    ).expect("fake v7 marker with NO v7 SQL installed");
    let after_forgery = legacy_rows(&db);
    assert!(apply_candidate_explicitly_once(&mut db).is_err(),
        "v7 marker without 3 installed STRICT tables must fail closed");
    assert_eq!(legacy_rows(&db), after_forgery);
    assert_eq!(db.query_row(
        "SELECT COUNT(*) FROM world_time_anchors", [], |row| row.get::<_, i64>(0)
    ).is_err(), true, "no v7 table created by retry");
    db.execute(
        "INSERT INTO schema_migrations(version,name)
         VALUES (8,'008_unapproved')", []
    ).expect("synthetic future version");
    assert!(apply_candidate_explicitly_once(&mut db).is_err());
    assert_eq!(db.query_row(
        "SELECT COUNT(*) FROM schema_migrations", [], |row| row.get::<_, i64>(0)
    ).unwrap(), 8);
    // The forged fixture modified its migration ledger only; original business
    // tables remain identical.
    for (name, rows) in before {
        if name != "schema_migrations" {
            assert_eq!(after_forgery.get(name), Some(&rows));
        }
    }
}


#[test]
fn explicit_candidate_second_call_rejects_missing_trigger_without_repair() {
    let root = DisposableRoot::new("missing-trigger");
    let source = root.file("closed-v6.sqlite3");
    create_closed_populated_v6(&source);
    let old_source_bytes = fs::read(&source).expect("source baseline");
    let copy = root.file("candidate-copy.sqlite3");
    fs::copy(&source, &copy).expect("closed fixture source copied only");
    let mut db = Connection::open(&copy).expect("owned disposable copy");
    database::configure_connection(&db).expect("FK enabled");
    assert!(apply_candidate_explicitly_once(&mut db).expect("first explicit copy migration"));
    let rows = legacy_rows(&db);
    db.execute_batch("DROP TRIGGER world_time_precedences_guard;")
        .expect("simulate damaged constraint in disposable copy");
    let objects_before = candidate_ddl_inventory(&db).expect("inventory before retry");
    let reason = apply_candidate_explicitly_once(&mut db)
        .expect_err("missing cycle trigger must stop idempotent retry");
    assert!(reason.contains("DDL drift"), "unexpected failure: {reason}");
    assert_eq!(candidate_ddl_inventory(&db).unwrap(), objects_before,
        "failed retry must not secretly repair schema");
    assert_eq!(legacy_rows(&db), rows, "all old v6 history remains untouched");
    assert_eq!(database::current_schema_version(&db).unwrap(), 7);
    drop(db);
    assert_eq!(fs::read(&source).unwrap(), old_source_bytes,
        "source v6 file must be byte-identical");
}

#[test]
fn explicit_candidate_second_call_rejects_extra_unreviewed_index() {
    let root = DisposableRoot::new("extra-index");
    let copy = root.file("owned-v6.sqlite3");
    create_closed_populated_v6(&copy);
    let mut db = Connection::open(&copy).expect("isolated fixture");
    database::configure_connection(&db).expect("FK enabled");
    assert!(apply_candidate_explicitly_once(&mut db).expect("first upgrade"));
    let legacy_before = legacy_rows(&db);
    db.execute_batch(
        "CREATE INDEX unreviewed_extra_time_index
         ON world_time_anchors(time_kind);"
    ).expect("simulate unapproved v7 index");
    let ddl_before = candidate_ddl_inventory(&db).unwrap();
    assert!(apply_candidate_explicitly_once(&mut db).is_err(),
        "extra DDL object must not be silently accepted on rerun");
    assert_eq!(candidate_ddl_inventory(&db).unwrap(), ddl_before);
    assert_eq!(legacy_rows(&db), legacy_before);
}


#[test]
fn idempotent_v7_retry_rejects_missing_legacy_v6_revision_trigger() {
    let root = DisposableRoot::new("missing-v6-trigger");
    let source = root.file("closed-original-v6.sqlite3");
    create_closed_populated_v6(&source);
    let unchanged_original = fs::read(&source).expect("source bytes");
    let copy = root.file("isolated-v7.sqlite3");
    fs::copy(&source, &copy).expect("closed fixture copy only");

    let mut db = Connection::open(&copy).expect("disposable copy");
    database::configure_connection(&db).expect("FK enabled");
    assert!(apply_candidate_explicitly_once(&mut db).expect("first migration"));
    let before_rows = legacy_rows(&db);
    db.execute_batch("DROP TRIGGER scene_text_revisions_no_delete;")
        .expect("simulate removed historic append-only guard");
    let observed_schema = legacy_ddl_inventory(&db).expect("snapshot altered DDL");
    let reason = apply_candidate_explicitly_once(&mut db)
        .expect_err("missing old revision trigger must fail closed");
    assert!(reason.contains("legacy v6 schema DDL drift"), "{reason}");
    assert_eq!(legacy_ddl_inventory(&db).unwrap(), observed_schema,
        "failed check must not silently repair historical schema");
    assert_eq!(legacy_rows(&db), before_rows,
        "all original v6 rows must be preserved");
    drop(db);
    assert_eq!(fs::read(&source).unwrap(), unchanged_original);
}

#[test]
fn idempotent_v7_retry_rejects_unapproved_legacy_index() {
    let root = DisposableRoot::new("rogue-v6-index");
    let copy = root.file("disposable.sqlite3");
    create_closed_populated_v6(&copy);
    let mut db = Connection::open(&copy).expect("isolated fixture");
    database::configure_connection(&db).expect("FK enabled");
    assert!(apply_candidate_explicitly_once(&mut db).expect("first migration"));
    let before_rows = legacy_rows(&db);
    db.execute_batch("CREATE INDEX unapproved_universe_index ON universes(name);")
        .expect("simulate unapproved legacy DDL");
    let schema_before = legacy_ddl_inventory(&db).unwrap();
    let reason = apply_candidate_explicitly_once(&mut db)
        .expect_err("unapproved old-table index must block retry");
    assert!(reason.contains("legacy v6 schema DDL drift"), "{reason}");
    assert_eq!(legacy_ddl_inventory(&db).unwrap(), schema_before);
    assert_eq!(legacy_rows(&db), before_rows);
}


// M3.1 controlled-launch BOUNDARY ONLY: does not launch Tauri or activate v7.
// The two files below belong exclusively to this temporary test root. This
// test deliberately uses the normal application database opener as a negative
// gate and records byte-for-byte preservation before/after refusal.
#[test]
fn controlled_readonly_launch_refuses_auto_v7_without_changing_disposable_files() {
    let root = DisposableRoot::new("v7-normal-launch-refusal");
    let source = root.file("closed-original-v6.sqlite3");
    let third = root.file("isolated-copy-v7.sqlite3");
    create_closed_populated_v6(&source);
    let source_bytes = fs::read(&source).expect("closed v6 source bytes");
    fs::copy(&source, &third).expect("copy ONLY closed disposable fixture");

    let mut isolated = Connection::open(&third).expect("writable disposable target");
    database::configure_connection(&isolated).expect("FK on");
    let old_rows = legacy_rows(&isolated);
    assert!(apply_candidate_explicitly_once(&mut isolated).expect("stage copy v7"));
    assert_eq!(database::current_schema_version(&isolated).unwrap(), 7);
    assert_eq!(legacy_rows(&isolated), old_rows);
    drop(isolated);

    let third_bytes_before = fs::read(&third).expect("closed v7 before runtime opener");
    let result = database::open_database(&third);
    assert!(matches!(
        result,
        Err(database::DatabaseError::ExplicitMigrationRequired(7))
    ), "normal v6 application open must refuse v7");
    assert_eq!(
        fs::read(&third).expect("v7 bytes after refusal"),
        third_bytes_before,
        "normal app startup must not mutate unsupported v7"
    );
    assert_eq!(fs::read(&source).unwrap(), source_bytes, "original v6 unchanged");

    // The separate explicit READ_ONLY connection is inspect-only and cannot
    // be mistaken for the shipped application's writable open_database().
    let inspector = Connection::open_with_flags(&third, OpenFlags::SQLITE_OPEN_READ_ONLY)
        .expect("explicit v7 inspector");
    database::configure_connection(&inspector).expect("FK checks");
    inspector.pragma_update(None, "query_only", true).expect("query only");
    assert_eq!(database::current_schema_version(&inspector).unwrap(), 7);
    assert_eq!(legacy_rows(&inspector), old_rows, "all M2 history intact");
    assert_eq!(inspector.query_row(
        "SELECT COUNT(*) FROM world_time_anchors",
        [], |row| row.get::<_, i64>(0)
    ).unwrap(), 0);
    assert_eq!(
        inspector.query_row("PRAGMA integrity_check", [], |row| row.get::<_, String>(0))
            .unwrap(), "ok"
    );
    assert_eq!(
        inspector.query_row(
            "SELECT COUNT(*) FROM pragma_foreign_key_check",
            [], |row| row.get::<_, i64>(0)
        ).unwrap(), 0
    );
    assert!(inspector.execute(
        "INSERT INTO world_time_anchors(id,universe_id,time_kind)
         VALUES ('unapproved-write','u1','unknown')", []
    ).is_err(), "read-only v7 inspector must refuse direct writes");
    drop(inspector);
    assert_eq!(fs::read(&third).unwrap(), third_bytes_before);
    assert_eq!(fs::read(&source).unwrap(), source_bytes);
}
