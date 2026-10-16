//! M3.2 G3: RUSQLITE OWNER-TO-RAM BACKUP LAB - IN MEMORY ONLY.
//!
//! Compiled only with cfg(test) + opt-in Cargo feature. No filesystem APIs,
//! paths to an actual database, Tauri runtime, migrations, or network.
//! This demonstrates snapshot semantics, NOT source identity/custody or G3.
//! Changing feature flags for a production binary is compile-time forbidden.

use rusqlite::{backup::Backup, params, Connection, Error, Result};
use std::time::Duration;

const MAX_TOY_BYTES: i64 = 2 * 1024 * 1024;

fn invented_owner(version: i64) -> Result<Connection> {
    assert!(version == 6 || version == 7, "fictional versions only");
    let owner = Connection::open_in_memory()?;
    owner.execute_batch(
        "PRAGMA foreign_keys=ON;
         CREATE TABLE imaginary_books (id INTEGER PRIMARY KEY, title TEXT NOT NULL);
         CREATE TABLE invented_facts (id INTEGER PRIMARY KEY,
            book_id INTEGER NOT NULL REFERENCES imaginary_books(id),
            detail TEXT NOT NULL);
         CREATE TABLE schema_migrations (version INTEGER PRIMARY KEY, name TEXT NOT NULL);
         INSERT INTO imaginary_books VALUES(1, 'Made up story');
         INSERT INTO invented_facts VALUES(1, 1, 'Fictional detail');",
    )?;
    for n in 1..=version {
        owner.execute(
            "INSERT INTO schema_migrations (version, name) VALUES (?1, ?2)",
            params![n, format!("toy-{n}")],
        )?;
    }
    Ok(owner)
}

fn only_one_in_memory_database(connection: &Connection) -> Result<bool> {
    let mut stmt = connection.prepare("PRAGMA database_list")?;
    let rows = stmt.query_map([], |row| {
        Ok((row.get::<_, String>(1)?, row.get::<_, String>(2)?))
    })?;
    let list = rows.collect::<Result<Vec<_>>>()?;
    Ok(list.len() == 1 && list[0].0 == "main" && list[0].1.is_empty())
}

fn toy_source_size(source: &Connection) -> Result<i64> {
    let pages: i64 = source.query_row("PRAGMA page_count", [], |r| r.get(0))?;
    let page_size: i64 = source.query_row("PRAGMA page_size", [], |r| r.get(0))?;
    pages.checked_mul(page_size).ok_or(Error::InvalidQuery)
}

fn assert_toy_snapshot(snapshot: &Connection, expected_version: i64) -> Result<()> {
    let integrity: String = snapshot.query_row("PRAGMA integrity_check", [], |r| r.get(0))?;
    if integrity != "ok" {
        return Err(Error::InvalidQuery);
    }
    let foreign_key_errors: i64 =
        snapshot.query_row("SELECT COUNT(*) FROM pragma_foreign_key_check", [], |r| r.get(0))?;
    if foreign_key_errors != 0 {
        return Err(Error::InvalidQuery);
    }
    let mut stmt = snapshot.prepare("SELECT version FROM schema_migrations ORDER BY version")?;
    let lineage = stmt
        .query_map([], |row| row.get::<_, i64>(0))?
        .collect::<Result<Vec<_>>>()?;
    if lineage != (1..=expected_version).collect::<Vec<_>>() {
        return Err(Error::InvalidQuery);
    }
    let books: i64 = snapshot.query_row("SELECT COUNT(*) FROM imaginary_books", [], |r| r.get(0))?;
    let facts: i64 = snapshot.query_row("SELECT COUNT(*) FROM invented_facts", [], |r| r.get(0))?;
    if books != 1 || facts != 1 {
        return Err(Error::InvalidQuery);
    }
    Ok(())
}

/// The caller supplies an ALREADY-OPEN source Connection. No source opening.
fn backup_preopened_ram_owner(
    source: &Connection,
    target: &mut Connection,
    version: i64,
    max_bytes: i64,
) -> Result<()> {
    if (version != 6 && version != 7)
        || max_bytes <= 0
        || max_bytes > MAX_TOY_BYTES
        || !source.is_autocommit()
        || !target.is_autocommit()
        || !only_one_in_memory_database(source)?
        || !only_one_in_memory_database(target)?
    {
        return Err(Error::InvalidQuery);
    }
    // The real backup API can OVERWRITE destination contents. The toy contract
    // requires an empty RAM destination and never accepts any file path.
    let existing: i64 = target.query_row(
        "SELECT COUNT(*) FROM sqlite_master", [], |r| r.get(0)
    )?;
    let size = toy_source_size(source)?;
    if existing != 0 || size <= 0 || size > max_bytes {
        return Err(Error::InvalidQuery);
    }
    let changes_before = source.total_changes();
    {
        let handle = Backup::new(source, target)?;
        handle.run_to_completion(16, Duration::from_millis(1), None)?;
    }
    // Reject changes made through this owner while backup executes. This does
    // NOT claim all external writers are excluded (SQLite supports them).
    if source.total_changes() != changes_before || toy_source_size(target)? > max_bytes {
        return Err(Error::InvalidQuery);
    }
    assert_toy_snapshot(target, version)
}

#[test]
fn m32_owned_backup_toy_v6_success() -> Result<()> {
    let source = invented_owner(6)?;
    let mut ram = Connection::open_in_memory()?;
    backup_preopened_ram_owner(&source, &mut ram, 6, MAX_TOY_BYTES)?;
    assert_toy_snapshot(&ram, 6)
}

#[test]
fn m32_owned_backup_toy_v7_success() -> Result<()> {
    let source = invented_owner(7)?;
    let mut ram = Connection::open_in_memory()?;
    backup_preopened_ram_owner(&source, &mut ram, 7, MAX_TOY_BYTES)?;
    assert_toy_snapshot(&ram, 7)
}

#[test]
fn m32_owned_backup_toy_source_is_still_open_and_unchanged() -> Result<()> {
    let source = invented_owner(6)?;
    let before = source.total_changes();
    let mut ram = Connection::open_in_memory()?;
    backup_preopened_ram_owner(&source, &mut ram, 6, MAX_TOY_BYTES)?;
    let books: i64 = source.query_row("SELECT COUNT(*) FROM imaginary_books", [], |r| r.get(0))?;
    assert_eq!(books, 1);
    assert_eq!(source.total_changes(), before);
    Ok(())
}

#[test]
fn m32_owned_backup_toy_later_source_write_does_not_mutate_snapshot() -> Result<()> {
    let source = invented_owner(6)?;
    let mut ram = Connection::open_in_memory()?;
    backup_preopened_ram_owner(&source, &mut ram, 6, MAX_TOY_BYTES)?;
    source.execute("UPDATE invented_facts SET detail='later' WHERE id=1", [])?;
    let captured: String = ram.query_row(
        "SELECT detail FROM invented_facts WHERE id=1", [], |r| r.get(0)
    )?;
    assert_eq!(captured, "Fictional detail");
    Ok(())
}

#[test]
fn m32_owned_backup_toy_rejects_uncommitted_owner_transaction() -> Result<()> {
    let source = invented_owner(6)?;
    source.execute_batch("BEGIN; UPDATE invented_facts SET detail='pending' WHERE id=1;")?;
    let mut ram = Connection::open_in_memory()?;
    assert!(backup_preopened_ram_owner(&source, &mut ram, 6, MAX_TOY_BYTES).is_err());
    source.execute_batch("ROLLBACK")?;
    Ok(())
}

#[test]
fn m32_owned_backup_toy_rejects_wrong_migrations() -> Result<()> {
    let source = invented_owner(6)?;
    source.execute("DELETE FROM schema_migrations WHERE version=6", [])?;
    let mut ram = Connection::open_in_memory()?;
    assert!(backup_preopened_ram_owner(&source, &mut ram, 6, MAX_TOY_BYTES).is_err());
    Ok(())
}

#[test]
fn m32_owned_backup_toy_rejects_orphan_foreign_key() -> Result<()> {
    let source = invented_owner(6)?;
    source.execute_batch("PRAGMA foreign_keys=OFF")?;
    source.execute("UPDATE invented_facts SET book_id=404 WHERE id=1", [])?;
    let mut ram = Connection::open_in_memory()?;
    assert!(backup_preopened_ram_owner(&source, &mut ram, 6, MAX_TOY_BYTES).is_err());
    Ok(())
}

#[test]
fn m32_owned_backup_toy_refuses_nonempty_destination_without_overwrite() -> Result<()> {
    let source = invented_owner(6)?;
    let mut ram = Connection::open_in_memory()?;
    ram.execute_batch("CREATE TABLE keep_me (value TEXT); INSERT INTO keep_me VALUES ('sentinel');")?;
    assert!(backup_preopened_ram_owner(&source, &mut ram, 6, MAX_TOY_BYTES).is_err());
    let sentinel: String = ram.query_row("SELECT value FROM keep_me", [], |r| r.get(0))?;
    assert_eq!(sentinel, "sentinel");
    Ok(())
}

#[test]
fn m32_owned_backup_toy_refuses_attached_memory_source() -> Result<()> {
    let source = invented_owner(6)?;
    source.execute_batch("ATTACH DATABASE ':memory:' AS extra_toy")?;
    let mut ram = Connection::open_in_memory()?;
    assert!(backup_preopened_ram_owner(&source, &mut ram, 6, MAX_TOY_BYTES).is_err());
    source.execute_batch("DETACH DATABASE extra_toy")?;
    Ok(())
}

#[test]
fn m32_owned_backup_toy_refuses_attached_memory_destination() -> Result<()> {
    let source = invented_owner(6)?;
    let mut ram = Connection::open_in_memory()?;
    ram.execute_batch("ATTACH DATABASE ':memory:' AS extra_ram")?;
    assert!(backup_preopened_ram_owner(&source, &mut ram, 6, MAX_TOY_BYTES).is_err());
    Ok(())
}

#[test]
fn m32_owned_backup_toy_refuses_unknown_version() -> Result<()> {
    let source = invented_owner(6)?;
    let mut ram = Connection::open_in_memory()?;
    assert!(backup_preopened_ram_owner(&source, &mut ram, 8, MAX_TOY_BYTES).is_err());
    Ok(())
}

#[test]
fn m32_owned_backup_toy_refuses_too_small_memory_budget() -> Result<()> {
    let source = invented_owner(6)?;
    let mut ram = Connection::open_in_memory()?;
    assert!(backup_preopened_ram_owner(&source, &mut ram, 6, 1024).is_err());
    Ok(())
}

#[test]
fn m32_owned_backup_toy_refuses_invalid_memory_limit() -> Result<()> {
    let source = invented_owner(6)?;
    let mut ram = Connection::open_in_memory()?;
    assert!(backup_preopened_ram_owner(&source, &mut ram, 6, MAX_TOY_BYTES + 1).is_err());
    Ok(())
}
