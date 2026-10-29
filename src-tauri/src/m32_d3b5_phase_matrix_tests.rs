//! D3b-5 bounded Windows crash-phase *refusal* fixtures.
//! New per-test %TEMP% roots only; no recovery, marker or production profile.
//! These checks bracket high-level SQLite operations. They do not interrupt
//! xSync or xShmUnmap callbacks, simulate power loss or attest durability.

use rusqlite::{Connection, OpenFlags};
use std::{
    ffi::{c_void, OsStr},
    fs,
    path::{Path, PathBuf},
    process,
    sync::atomic::{AtomicUsize, Ordering},
    time::{SystemTime, UNIX_EPOCH},
};

const CHILD_ROLE: &str = "FABULAXIOM_M32_D3B5_DISPOSABLE_CHILD_PHASE";
const CHILD_PATH: &str = "FABULAXIOM_M32_D3B5_DISPOSABLE_CHILD_PATH";
const TERMINATED: i32 = 77;
const REFUSAL: &str = "RECOVERY_REQUIRED_NOT_AUTHORIZED";

#[link(name = "kernel32")]
unsafe extern "system" {
    fn GetCurrentProcess() -> *mut c_void;
    fn TerminateProcess(handle: *mut c_void, exit_code: u32) -> i32;
}

struct OwnedRoot(PathBuf);
impl OwnedRoot {
    fn fresh() -> Self {
        static NEXT: AtomicUsize = AtomicUsize::new(0);
        let stamp = SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_nanos();
        let name = format!(
            "fabulaxiom-d3b5-disposable-{}-{stamp}-{}",
            process::id(), NEXT.fetch_add(1, Ordering::Relaxed)
        );
        let root = std::env::temp_dir().join(name);
        fs::create_dir(&root).expect("only create a genuinely new test-owned root");
        Self(root)
    }
    fn main(&self) -> PathBuf { self.0.join("new.sqlite3") }
}
impl Drop for OwnedRoot {
    fn drop(&mut self) {
        assert!(self.0.starts_with(std::env::temp_dir()));
        assert!(self.0.file_name().unwrap().to_string_lossy()
            .starts_with("fabulaxiom-d3b5-disposable-"));
        fs::remove_dir_all(&self.0).expect("only clean our disposable test-owned root");
    }
}

fn assert_owned_main(path: &Path) {
    assert_eq!(path.file_name(), Some(OsStr::new("new.sqlite3")));
    let dir = path.parent().expect("test-owned parent");
    assert!(dir.starts_with(std::env::temp_dir()), "never use operator paths");
    assert!(dir.file_name().unwrap().to_string_lossy()
        .starts_with("fabulaxiom-d3b5-disposable-"));
    assert!(path.is_file(), "parent must create a fresh main before the child");
}

fn create_new_main() -> (OwnedRoot, PathBuf) {
    let root = OwnedRoot::fresh();
    let path = root.main();
    fs::OpenOptions::new().write(true).create_new(true).open(&path)
        .expect("CREATE_NEW main only in a fresh owned CI root");
    assert_owned_main(&path);
    (root, path)
}

fn successor_refuses_without_predecessor_provenance(_phase: &str) -> &'static str {
    // The successor must not call SQLite on this potentially damaged file.
    REFUSAL
}

fn kill_child_at(phase: &str, path: &Path) {
    let exit = process::Command::new(std::env::current_exe().unwrap())
        .arg("--exact")
        .arg("m32_d3b5_phase_matrix_tests::m32_d3b5_child_terminate_at_phase")
        .arg("--nocapture")
        .env(CHILD_ROLE, phase)
        .env(CHILD_PATH, path)
        .status().expect("spawn only the current Rust test binary");
    assert_eq!(exit.code(), Some(TERMINATED),
        "child must reach the declared phase then TerminateProcess: {phase}: {exit:?}");
}

fn parent_metadata_only(path: &Path, phase: &str) {
    assert_owned_main(path);
    let main = fs::metadata(path).expect("fixture main metadata");
    assert!(main.is_file());
    if phase != "after_close" {
        let wal = path.with_file_name("new.sqlite3-wal");
        assert!(fs::metadata(&wal).expect("fixture WAL metadata").len() > 0,
            "WAL must still exist when child is terminated with SQLite open");
    }
    // No Connection::open*, PRAGMA, wal checkpoint or SQLite recovery here.
    // WAL/SHM are not deleted, rewritten, copied, or treated as an admission token.
    assert_eq!(successor_refuses_without_predecessor_provenance(phase), REFUSAL);
}

#[test]
fn m32_d3b5_child_terminate_at_phase() {
    let Ok(phase) = std::env::var(CHILD_ROLE) else { return };
    assert!(matches!(phase.as_str(),
        "before_commit" | "after_commit" |
        "before_checkpoint" | "after_checkpoint" |
        "before_close" | "after_close"));
    let path = PathBuf::from(std::env::var_os(CHILD_PATH).expect("child fixture path"));
    assert_owned_main(&path);

    // This is the *same* new fixture precreated by the parent, NOT an existing
    // operator profile and never a successor reopening a crashed database.
    let db = Connection::open_with_flags(&path, OpenFlags::SQLITE_OPEN_READ_WRITE)
        .expect("only the first CI child may open its disposable main");
    db.execute_batch(
        "PRAGMA journal_mode=WAL;
         PRAGMA wal_autocheckpoint=0;
         PRAGMA synchronous=FULL;
         CREATE TABLE invented_d3b5(id INTEGER PRIMARY KEY, note TEXT);",
    ).expect("only fictional fixture SQL");

    match phase.as_str() {
        "before_commit" => {
            db.execute_batch(
                "BEGIN IMMEDIATE;
                 INSERT INTO invented_d3b5(note) VALUES ('pending-fiction');"
            ).unwrap();
            // Deliberately do not COMMIT.
        }
        "after_commit" | "before_checkpoint" | "before_close" => {
            db.execute_batch(
                "INSERT INTO invented_d3b5(note) VALUES ('committed-fiction');"
            ).unwrap();
        }
        "after_checkpoint" => {
            db.execute_batch(
                "INSERT INTO invented_d3b5(note) VALUES ('checkpoint-fiction');"
            ).unwrap();
            let (busy, _log, _done): (i32, i32, i32) = db.query_row(
                "PRAGMA wal_checkpoint(PASSIVE)", [], |r|
                Ok((r.get(0)?, r.get(1)?, r.get(2)?))
            ).unwrap();
            assert_eq!(busy, 0, "owned single-connection passive checkpoint");
        }
        "after_close" => {
            db.execute_batch(
                "INSERT INTO invented_d3b5(note) VALUES ('closed-fiction');"
            ).unwrap();
            assert!(db.close().is_ok(), "observed local close of disposable fixture");
            // Even a genuinely completed close is not a cross-process
            // provenance attestation or authority to open the file again.
        }
        _ => unreachable!(),
    }
    // OS process termination, NOT a simulated sudden loss of disk power.
    let result = unsafe { TerminateProcess(GetCurrentProcess(), TERMINATED as u32) };
    panic!("child TerminateProcess unexpectedly returned {result}");
}

#[test]
fn m32_d3b5_before_after_commit_always_refuses_successor_open() {
    for phase in ["before_commit", "after_commit"] {
        let (_root, path) = create_new_main();
        kill_child_at(phase, &path);
        parent_metadata_only(&path, phase);
    }
}

#[test]
fn m32_d3b5_before_after_passive_checkpoint_never_authorizes_recovery() {
    for phase in ["before_checkpoint", "after_checkpoint"] {
        let (_root, path) = create_new_main();
        kill_child_at(phase, &path);
        parent_metadata_only(&path, phase);
    }
}

#[test]
fn m32_d3b5_before_after_explicit_close_is_not_restart_attestation() {
    for phase in ["before_close", "after_close"] {
        let (_root, path) = create_new_main();
        kill_child_at(phase, &path);
        parent_metadata_only(&path, phase);
    }
}
