//! M3.2 G3: TEST-ONLY, IN-MEMORY SQLite owner lifecycle / lease rehearsal.
//!
//! This is NOT a Tauri state type, file opener or source authentication.
//! It creates its own invented database with Connection::open_in_memory().
//! No operator path, disk, runtime IPC, network, migration 007 or activation.

use rusqlite::{backup::Backup, params, Connection, Error, Result};
use std::sync::{
    atomic::{AtomicU64, Ordering},
    Arc, Mutex,
};
use std::time::Duration;

static NEXT_TOY_SESSION: AtomicU64 = AtomicU64::new(1);
const MAX_TOY_BYTES: i64 = 2 * 1024 * 1024;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
struct ToyLease {
    session: u64,
    revision: u64,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum ToyState {
    Ready,
    Capturing,
    Poisoned,
    Revoked,
}

/// Cannot be cloned; owns its pre-opened in-memory source for its full lifetime.
/// A Mutex<OwnerSlot> serializes toy access. This is not a real authentication token.
struct OwnerSlot {
    source: Option<Connection>,
    session: u64,
    revision: u64,
    version: i64,
    state: ToyState,
}

fn fictional_schema(conn: &Connection, version: i64) -> Result<()> {
    conn.execute_batch(
        "PRAGMA foreign_keys=ON;
         CREATE TABLE imaginary_books (id INTEGER PRIMARY KEY, title TEXT NOT NULL);
         CREATE TABLE invented_facts (id INTEGER PRIMARY KEY, book_id INTEGER NOT NULL
             REFERENCES imaginary_books(id), detail TEXT NOT NULL);
         CREATE TABLE schema_migrations (version INTEGER PRIMARY KEY);
         INSERT INTO imaginary_books VALUES (1, 'Imaginary book');
         INSERT INTO invented_facts VALUES (1, 1, 'Before');",
    )?;
    for i in 1..=version {
        conn.execute("INSERT INTO schema_migrations VALUES (?1)", params![i])?;
    }
    Ok(())
}

fn memory_only(conn: &Connection) -> Result<bool> {
    let mut stmt = conn.prepare("PRAGMA database_list")?;
    let list = stmt
        .query_map([], |row| Ok((row.get::<_, String>(1)?, row.get::<_, String>(2)?)))?
        .collect::<Result<Vec<_>>>()?;
    // SQLite can lazily materialize its implicit "temp" schema after
    // read-only PRAGMA validation. That is NOT an external ATTACH. We still
    // reject every other schema name and any on-disk database path.
    let mut main = 0;
    let mut temp = 0;
    for (name, path) in list {
        if !path.is_empty() {
            return Ok(false);
        }
        match name.as_str() {
            "main" => main += 1,
            "temp" => temp += 1,
            _ => return Ok(false),
        }
    }
    Ok(main == 1 && temp <= 1)
}

fn qualified_snapshot(conn: &Connection, version: i64) -> Result<()> {
    if !memory_only(conn)? {
        return Err(Error::InvalidQuery);
    }
    let result: String = conn.query_row("PRAGMA integrity_check", [], |r| r.get(0))?;
    let fk: i64 = conn.query_row(
        "SELECT count(*) FROM pragma_foreign_key_check", [], |r| r.get(0)
    )?;
    let lineage = conn
        .prepare("SELECT version FROM schema_migrations ORDER BY version")?
        .query_map([], |r| r.get::<_, i64>(0))?
        .collect::<Result<Vec<_>>>()?;
    let books: i64 = conn.query_row("SELECT count(*) FROM imaginary_books", [], |r| r.get(0))?;
    let facts: i64 = conn.query_row("SELECT count(*) FROM invented_facts", [], |r| r.get(0))?;
    if result != "ok" || fk != 0 || lineage != (1..=version).collect::<Vec<_>>()
        || books != 1 || facts != 1
    {
        return Err(Error::InvalidQuery);
    }
    Ok(())
}

fn memory_budget(conn: &Connection) -> Result<i64> {
    let pages: i64 = conn.query_row("PRAGMA page_count", [], |r| r.get(0))?;
    let size: i64 = conn.query_row("PRAGMA page_size", [], |r| r.get(0))?;
    pages.checked_mul(size).ok_or(Error::InvalidQuery)
}

impl OwnerSlot {
    fn new_invented(version: i64) -> Result<Self> {
        if version != 6 && version != 7 {
            return Err(Error::InvalidQuery);
        }
        let source = Connection::open_in_memory()?;
        fictional_schema(&source, version)?;
        Ok(Self {
            source: Some(source),
            session: NEXT_TOY_SESSION.fetch_add(1, Ordering::Relaxed),
            revision: 1,
            version,
            state: ToyState::Ready,
        })
    }

    fn lease(&self) -> Result<ToyLease> {
        if self.state != ToyState::Ready || self.source.is_none() {
            return Err(Error::InvalidQuery);
        }
        Ok(ToyLease { session: self.session, revision: self.revision })
    }

    fn check(&self, ticket: ToyLease) -> Result<()> {
        if self.state != ToyState::Ready
            || self.source.is_none()
            || ticket.session != self.session
            || ticket.revision != self.revision
        {
            return Err(Error::InvalidQuery);
        }
        Ok(())
    }

    /// Captures to an independent RAM connection, without opening a source path.
    /// An unexpected failed capture permanently poisons this *toy* owner.
    fn capture(&mut self, ticket: ToyLease, max_bytes: i64) -> Result<Connection> {
        self.check(ticket)?;
        if max_bytes < 1 || max_bytes > MAX_TOY_BYTES {
            return Err(Error::InvalidQuery);
        }
        self.state = ToyState::Capturing;
        let result = (|| {
            let source = self.source.as_ref().ok_or(Error::InvalidQuery)?;
            if !source.is_autocommit() || !memory_only(source)? {
                return Err(Error::InvalidQuery);
            }
            if memory_budget(source)? > max_bytes {
                return Err(Error::InvalidQuery);
            }
            let mut dest = Connection::open_in_memory()?;
            {
                let backup = Backup::new(source, &mut dest)?;
                backup.run_to_completion(16, Duration::from_millis(1), None)?;
            }
            if memory_budget(&dest)? > max_bytes {
                return Err(Error::InvalidQuery);
            }
            qualified_snapshot(&dest, self.version)?;
            Ok(dest)
        })();
        match result {
            Ok(snapshot) => {
                self.state = ToyState::Ready;
                Ok(snapshot)
            }
            Err(error) => {
                self.state = ToyState::Poisoned;
                Err(error)
            }
        }
    }

    /// A toy owner write invalidates all previously issued lease tokens.
    fn edit_fixture(&mut self, ticket: ToyLease, value: &str) -> Result<ToyLease> {
        self.check(ticket)?;
        let source = self.source.as_ref().ok_or(Error::InvalidQuery)?;
        if !source.is_autocommit() {
            self.state = ToyState::Poisoned;
            return Err(Error::InvalidQuery);
        }
        source.execute("UPDATE invented_facts SET detail=?1 WHERE id=1", [value])?;
        self.revision = self.revision.checked_add(1).ok_or(Error::InvalidQuery)?;
        self.lease()
    }

    /// Explicit revocation releases this toy connection and never reopens it.
    fn revoke(&mut self) {
        self.source = None;
        self.state = ToyState::Revoked;
        self.revision = self.revision.saturating_add(1);
    }
}

fn toy_detail(conn: &Connection) -> Result<String> {
    conn.query_row("SELECT detail FROM invented_facts WHERE id=1", [], |r| r.get(0))
}

#[test]
fn m32_owner_lifecycle_implicit_temp_schema_remains_memory_only() -> Result<()> {
    let conn = Connection::open_in_memory()?;
    conn.execute_batch("CREATE TEMP TABLE harmless_fixture (n INTEGER);")?;
    assert!(memory_only(&conn)?);
    Ok(())
}

#[test]
fn m32_owner_lifecycle_second_validation_is_idempotent() -> Result<()> {
    let mut owner = OwnerSlot::new_invented(7)?;
    let ticket = owner.lease()?;
    let copy = owner.capture(ticket, MAX_TOY_BYTES)?;
    qualified_snapshot(&copy, 7)?;
    qualified_snapshot(&copy, 7)?;
    assert!(memory_only(&copy)?);
    Ok(())
}

#[test]
fn m32_owner_lifecycle_v6_reusable_before_revocation() -> Result<()> {
    let mut owner = OwnerSlot::new_invented(6)?;
    let token = owner.lease()?;
    let copy1 = owner.capture(token, MAX_TOY_BYTES)?;
    let copy2 = owner.capture(token, MAX_TOY_BYTES)?;
    assert_eq!(toy_detail(&copy1)?, "Before");
    assert_eq!(toy_detail(&copy2)?, "Before");
    assert_eq!(owner.state, ToyState::Ready);
    Ok(())
}

#[test]
fn m32_owner_lifecycle_v7_lineage() -> Result<()> {
    let mut owner = OwnerSlot::new_invented(7)?;
    let lease = owner.lease()?;
    let snapshot = owner.capture(lease, MAX_TOY_BYTES)?;
    qualified_snapshot(&snapshot, 7)
}

#[test]
fn m32_owner_lifecycle_distinct_owner_lease_rejected() -> Result<()> {
    let one = OwnerSlot::new_invented(6)?;
    let mut two = OwnerSlot::new_invented(6)?;
    assert!(two.capture(one.lease()?, MAX_TOY_BYTES).is_err());
    assert_eq!(two.state, ToyState::Ready);
    Ok(())
}

#[test]
fn m32_owner_lifecycle_write_invalidates_old_lease() -> Result<()> {
    let mut owner = OwnerSlot::new_invented(6)?;
    let old = owner.lease()?;
    let fresh = owner.edit_fixture(old, "Now")?;
    assert!(owner.capture(old, MAX_TOY_BYTES).is_err());
    let snapshot = owner.capture(fresh, MAX_TOY_BYTES)?;
    assert_eq!(toy_detail(&snapshot)?, "Now");
    Ok(())
}

#[test]
fn m32_owner_lifecycle_old_snapshot_unchanged_by_later_edit() -> Result<()> {
    let mut owner = OwnerSlot::new_invented(6)?;
    let old = owner.lease()?;
    let snapshot = owner.capture(old, MAX_TOY_BYTES)?;
    let new = owner.edit_fixture(old, "After")?;
    assert_eq!(toy_detail(&snapshot)?, "Before");
    let newer = owner.capture(new, MAX_TOY_BYTES)?;
    assert_eq!(toy_detail(&newer)?, "After");
    Ok(())
}

#[test]
fn m32_owner_lifecycle_revoked_owner_never_reopens() -> Result<()> {
    let mut owner = OwnerSlot::new_invented(6)?;
    let ticket = owner.lease()?;
    owner.revoke();
    assert!(owner.capture(ticket, MAX_TOY_BYTES).is_err());
    assert!(owner.lease().is_err());
    assert!(owner.source.is_none());
    assert_eq!(owner.state, ToyState::Revoked);
    Ok(())
}

#[test]
fn m32_owner_lifecycle_invalid_version_rejected() {
    assert!(OwnerSlot::new_invented(8).is_err());
}

#[test]
fn m32_owner_lifecycle_uncommitted_source_causes_poison() -> Result<()> {
    let mut owner = OwnerSlot::new_invented(6)?;
    let ticket = owner.lease()?;
    owner.source.as_ref().ok_or(Error::InvalidQuery)?
        .execute_batch("BEGIN; UPDATE invented_facts SET detail='uncommitted' WHERE id=1;")?;
    assert!(owner.capture(ticket, MAX_TOY_BYTES).is_err());
    assert_eq!(owner.state, ToyState::Poisoned);
    assert!(owner.lease().is_err());
    Ok(())
}

#[test]
fn m32_owner_lifecycle_corrupt_migrations_poison() -> Result<()> {
    let mut owner = OwnerSlot::new_invented(6)?;
    let ticket = owner.lease()?;
    owner.source.as_ref().ok_or(Error::InvalidQuery)?
        .execute("DELETE FROM schema_migrations WHERE version=6", [])?;
    assert!(owner.capture(ticket, MAX_TOY_BYTES).is_err());
    assert_eq!(owner.state, ToyState::Poisoned);
    assert!(owner.capture(ticket, MAX_TOY_BYTES).is_err());
    Ok(())
}

#[test]
fn m32_owner_lifecycle_foreign_key_orphan_poison() -> Result<()> {
    let mut owner = OwnerSlot::new_invented(6)?;
    let ticket = owner.lease()?;
    let source = owner.source.as_ref().ok_or(Error::InvalidQuery)?;
    source.execute_batch("PRAGMA foreign_keys=OFF;")?;
    source.execute("UPDATE invented_facts SET book_id=999 WHERE id=1", [])?;
    assert!(owner.capture(ticket, MAX_TOY_BYTES).is_err());
    assert_eq!(owner.state, ToyState::Poisoned);
    Ok(())
}

#[test]
fn m32_owner_lifecycle_memory_limit_veto_without_read() -> Result<()> {
    let mut owner = OwnerSlot::new_invented(6)?;
    let ticket = owner.lease()?;
    assert!(owner.capture(ticket, 0).is_err());
    assert!(owner.capture(ticket, MAX_TOY_BYTES + 1).is_err());
    assert_eq!(owner.state, ToyState::Ready);
    Ok(())
}

#[test]
fn m32_owner_lifecycle_budget_exhaustion_poison() -> Result<()> {
    let mut owner = OwnerSlot::new_invented(6)?;
    let ticket = owner.lease()?;
    assert!(owner.capture(ticket, 512).is_err());
    assert_eq!(owner.state, ToyState::Poisoned);
    Ok(())
}

#[test]
fn m32_owner_lifecycle_attached_source_poison() -> Result<()> {
    let mut owner = OwnerSlot::new_invented(6)?;
    let ticket = owner.lease()?;
    owner.source.as_ref().ok_or(Error::InvalidQuery)?
        .execute_batch("ATTACH DATABASE ':memory:' AS extra_toy")?;
    assert!(owner.capture(ticket, MAX_TOY_BYTES).is_err());
    assert_eq!(owner.state, ToyState::Poisoned);
    Ok(())
}

#[test]
fn m32_owner_lifecycle_mutex_serializes_test_threads() -> Result<()> {
    let shared = Arc::new(Mutex::new(OwnerSlot::new_invented(6)?));
    let ticket = shared.lock().map_err(|_| Error::InvalidQuery)?.lease()?;
    let first = Arc::clone(&shared);
    let second = Arc::clone(&shared);
    let a = std::thread::spawn(move || -> Result<String> {
        let mut guard = first.lock().map_err(|_| Error::InvalidQuery)?;
        let copy = guard.capture(ticket, MAX_TOY_BYTES)?;
        toy_detail(&copy)
    });
    let b = std::thread::spawn(move || -> Result<String> {
        let mut guard = second.lock().map_err(|_| Error::InvalidQuery)?;
        let copy = guard.capture(ticket, MAX_TOY_BYTES)?;
        toy_detail(&copy)
    });
    assert_eq!(a.join().map_err(|_| Error::InvalidQuery)??, "Before");
    assert_eq!(b.join().map_err(|_| Error::InvalidQuery)??, "Before");
    Ok(())
}

#[test]
fn m32_owner_lifecycle_mutex_poison_does_not_silently_recover() -> Result<()> {
    let shared = Arc::new(Mutex::new(OwnerSlot::new_invented(6)?));
    let poisoner = Arc::clone(&shared);
    let task = std::thread::spawn(move || {
        let _held = poisoner.lock().expect("fixture lock");
        panic!("intentional toy mutex poison");
    });
    assert!(task.join().is_err());
    assert!(shared.lock().is_err());
    Ok(())
}

#[test]
fn m32_owner_lifecycle_explicit_revocation_preserves_snapshot() -> Result<()> {
    let mut owner = OwnerSlot::new_invented(7)?;
    let ticket = owner.lease()?;
    let copy = owner.capture(ticket, MAX_TOY_BYTES)?;
    owner.revoke();
    qualified_snapshot(&copy, 7)?;
    assert!(owner.capture(ticket, MAX_TOY_BYTES).is_err());
    Ok(())
}
