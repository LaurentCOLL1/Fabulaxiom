//! TEST-ONLY / OPT-IN: non-migrating inspection of an ALREADY-OPEN fictional RAM source.
//!
//! No on-disk file paths, no Tauri state/IPC, no migrations, no backup output,
//! no private source, no operator authorization. Neither query_only nor total_changes
//! authenticates another process or proves absence of a real SQLite writer.

use rusqlite::{params, Connection, Error, Result};

const FICTIONAL_VERSIONS: [i64; 2] = [6, 7];

#[derive(Debug, PartialEq, Eq)]
struct FictionalReading {
    version: i64,
    invented_event_count: i64,
}

/// Holds ONLY a borrow. No source opener is reachable through this API.
struct PreopenedFictionalReader<'a> {
    source: &'a Connection,
    version: i64,
    change_count_before: i64,
}

fn total_changes(source: &Connection) -> Result<i64> {
    source.query_row("SELECT total_changes()", [], |r| r.get(0))
}

/// Every inspection rechecks query-only, all attached schemas, and the
/// fictional version lineage. No call to database::open_database/migrations.
fn inspect_fictional_ram_source(source: &Connection, version: i64) -> Result<FictionalReading> {
    if !FICTIONAL_VERSIONS.contains(&version) {
        return Err(Error::InvalidQuery);
    }
    let query_only: i64 = source.query_row("PRAGMA query_only", [], |r| r.get(0))?;
    if query_only != 1 {
        return Err(Error::InvalidQuery);
    }

    let databases = source
        .prepare("PRAGMA database_list")?
        .query_map([], |row| Ok((row.get::<_, String>(1)?, row.get::<_, String>(2)?)))?
        .collect::<Result<Vec<_>>>()?;
    let mut main_count = 0;
    let mut temp_count = 0;
    for (name, path) in databases {
        if !path.is_empty() {
            return Err(Error::InvalidQuery);
        }
        match name.as_str() {
            "main" => main_count += 1,
            "temp" => temp_count += 1,
            _ => return Err(Error::InvalidQuery),
        }
    }
    if main_count != 1 || temp_count > 1 {
        return Err(Error::InvalidQuery);
    }

    let versions = source
        .prepare("SELECT version FROM schema_migrations ORDER BY version")?
        .query_map([], |r| r.get::<_, i64>(0))?
        .collect::<Result<Vec<_>>>()?;
    if versions != (1..=version).collect::<Vec<_>>() {
        return Err(Error::InvalidQuery);
    }
    let integrity: String = source.query_row("PRAGMA integrity_check", [], |r| r.get(0))?;
    let bad_fk: i64 = source.query_row(
        "SELECT count(*) FROM pragma_foreign_key_check", [], |r| r.get(0)
    )?;
    if integrity != "ok" || bad_fk != 0 {
        return Err(Error::InvalidQuery);
    }

    let count: i64 = source.query_row("SELECT count(*) FROM imaginary_events", [], |r| r.get(0))?;
    if count != 1 {
        return Err(Error::InvalidQuery);
    }
    Ok(FictionalReading { version, invented_event_count: count })
}

impl<'a> PreopenedFictionalReader<'a> {
    fn new(source: &'a Connection, version: i64) -> Result<Self> {
        inspect_fictional_ram_source(source, version)?;
        Ok(Self { source, version, change_count_before: total_changes(source)? })
    }

    fn read_again(&self) -> Result<FictionalReading> {
        if total_changes(self.source)? != self.change_count_before {
            return Err(Error::InvalidQuery);
        }
        let reading = inspect_fictional_ram_source(self.source, self.version)?;
        if total_changes(self.source)? != self.change_count_before {
            return Err(Error::InvalidQuery);
        }
        Ok(reading)
    }
}

#[cfg(test)]
fn imagined_connection(version: i64) -> Result<Connection> {
    if !FICTIONAL_VERSIONS.contains(&version) {
        return Err(Error::InvalidQuery);
    }
    let source = Connection::open_in_memory()?;
    source.execute_batch(
        "PRAGMA foreign_keys=ON;
         CREATE TABLE schema_migrations(version INTEGER PRIMARY KEY);
         CREATE TABLE imaginary_events(id INTEGER PRIMARY KEY, description TEXT NOT NULL);
         INSERT INTO imaginary_events VALUES (1, 'completely invented');",
    )?;
    for n in 1..=version {
        source.execute("INSERT INTO schema_migrations VALUES (?1)", params![n])?;
    }
    source.execute_batch("PRAGMA query_only=ON;")?;
    Ok(source)
}

#[test]
fn toy_01_preopened_v6_reads_without_migration() -> Result<()> {
    let c = imagined_connection(6)?;
    let before = total_changes(&c)?;
    let r = PreopenedFictionalReader::new(&c, 6)?;
    assert_eq!(r.read_again()?, FictionalReading { version: 6, invented_event_count: 1 });
    assert_eq!(total_changes(&c)?, before);
    Ok(())
}

#[test]
fn toy_02_preopened_v7_reads_without_migration() -> Result<()> {
    let c = imagined_connection(7)?;
    let r = PreopenedFictionalReader::new(&c, 7)?;
    assert_eq!(r.read_again()?.version, 7);
    Ok(())
}

#[test]
fn toy_03_wrong_expected_lineage_stops() -> Result<()> {
    let c = imagined_connection(6)?;
    assert!(PreopenedFictionalReader::new(&c, 7).is_err());
    Ok(())
}

#[test]
fn toy_04_unknown_version_stops() -> Result<()> {
    let c = imagined_connection(6)?;
    assert!(PreopenedFictionalReader::new(&c, 8).is_err());
    Ok(())
}

#[test]
fn toy_05_query_only_disabled_stops() -> Result<()> {
    let c = imagined_connection(6)?;
    c.execute_batch("PRAGMA query_only=OFF;")?;
    assert!(PreopenedFictionalReader::new(&c, 6).is_err());
    Ok(())
}

#[test]
fn toy_06_insert_rejected_by_query_only() -> Result<()> {
    let c = imagined_connection(6)?;
    let r = PreopenedFictionalReader::new(&c, 6)?;
    assert!(c.execute("INSERT INTO imaginary_events VALUES (2, 'wrong')", []).is_err());
    assert!(r.read_again().is_ok());
    Ok(())
}

#[test]
fn toy_07_update_and_drop_rejected_by_query_only() -> Result<()> {
    let c = imagined_connection(6)?;
    assert!(c.execute("UPDATE imaginary_events SET description='wrong'", []).is_err());
    assert!(c.execute_batch("DROP TABLE imaginary_events").is_err());
    Ok(())
}

#[test]
fn toy_08_unexpected_attached_ram_schema_stops() -> Result<()> {
    let c = imagined_connection(6)?;
    c.execute_batch("ATTACH DATABASE ':memory:' AS extra;")?;
    assert!(PreopenedFictionalReader::new(&c, 6).is_err());
    Ok(())
}

#[test]
fn toy_09_missing_version_row_stops() -> Result<()> {
    let c = imagined_connection(6)?;
    c.execute_batch("PRAGMA query_only=OFF; DELETE FROM schema_migrations WHERE version=6; PRAGMA query_only=ON;")?;
    assert!(PreopenedFictionalReader::new(&c, 6).is_err());
    Ok(())
}

#[test]
fn toy_10_same_version_content_rewrite_invalidates_existing_borrow() -> Result<()> {
    let c = imagined_connection(6)?;
    let r = PreopenedFictionalReader::new(&c, 6)?;
    c.execute_batch("PRAGMA query_only=OFF;
      UPDATE imaginary_events SET description='mutated invented data' WHERE id=1;
      PRAGMA query_only=ON;")?;
    assert!(r.read_again().is_err());
    Ok(())
}

#[test]
fn toy_11_disabling_query_only_invalidates_existing_borrow() -> Result<()> {
    let c = imagined_connection(6)?;
    let r = PreopenedFictionalReader::new(&c, 6)?;
    c.execute_batch("PRAGMA query_only=OFF;")?;
    assert!(r.read_again().is_err());
    Ok(())
}

#[test]
fn toy_12_no_invented_source_version_zero() {
    assert!(imagined_connection(0).is_err());
}

#[test]
fn toy_13_late_attached_ram_schema_invalidates_existing_borrow() -> Result<()> {
    let c = imagined_connection(7)?;
    let r = PreopenedFictionalReader::new(&c, 7)?;
    c.execute_batch("ATTACH DATABASE ':memory:' AS extra;")?;
    assert!(r.read_again().is_err());
    Ok(())
}

#[cfg(test)]
fn invented_shared_ram_pair(version: i64) -> Result<(Connection, Connection)> {
    use std::sync::atomic::{AtomicU64, Ordering};
    static NEXT_INVENTED_RAM: AtomicU64 = AtomicU64::new(1);
    let id = NEXT_INVENTED_RAM.fetch_add(1, Ordering::Relaxed);
    // SQLite URI mode=memory keeps both connections OFF DISK. Distinct ID for
    // parallel tests. Never substitute a protected original path or Tauri opener.
    let uri = format!("file:m32-invented-foreign-writer-{id}?mode=memory&cache=shared");
    let flags = rusqlite::OpenFlags::SQLITE_OPEN_READ_WRITE
        | rusqlite::OpenFlags::SQLITE_OPEN_CREATE
        | rusqlite::OpenFlags::SQLITE_OPEN_URI;
    let reader = Connection::open_with_flags(&uri, flags)?;
    reader.execute_batch(
        "CREATE TABLE schema_migrations(version INTEGER PRIMARY KEY);
         CREATE TABLE imaginary_events(id INTEGER PRIMARY KEY, description TEXT NOT NULL);
         INSERT INTO imaginary_events VALUES (1, 'fictitious initial event');",
    )?;
    for n in 1..=version {
        reader.execute("INSERT INTO schema_migrations VALUES (?1)", params![n])?;
    }
    let other_writer = Connection::open_with_flags(&uri, flags)?;
    reader.execute_batch("PRAGMA query_only=ON;")?;
    Ok((reader, other_writer))
}

#[test]
fn toy_14_query_only_and_total_changes_do_not_exclude_independent_writer() -> Result<()> {
    let (reader, other_writer) = invented_shared_ram_pair(6)?;
    let lease = PreopenedFictionalReader::new(&reader, 6)?;
    let initial_changes = total_changes(&reader)?;
    let initial_value: String = reader.query_row(
        "SELECT description FROM imaginary_events WHERE id=1", [], |row| row.get(0),
    )?;
    assert_eq!(initial_value, "fictitious initial event");

    // This independently opened connection updates the same invented RAM DB.
    // query_only is connection-scoped; total_changes is also connection-local.
    other_writer.execute(
        "UPDATE imaginary_events SET description='fictitious external rewrite' WHERE id=1", [],
    )?;
    assert_eq!(total_changes(&reader)?, initial_changes);
    assert_eq!(
        lease.read_again()?,
        FictionalReading { version: 6, invented_event_count: 1 },
    );
    let after: String = reader.query_row(
        "SELECT description FROM imaginary_events WHERE id=1", [], |row| row.get(0),
    )?;
    assert_eq!(after, "fictitious external rewrite");
    assert_ne!(after, initial_value);
    // TEST PASSES by reproducing a SECURITY GAP. This is NOT a real owner,
    // writer absence certificate, protected SQLite inspection or G3 permit.
    Ok(())
}

#[test]
fn toy_15_query_only_guard_can_detect_count_drift_but_not_all_foreign_writes() -> Result<()> {
    let (reader, other_writer) = invented_shared_ram_pair(7)?;
    let lease = PreopenedFictionalReader::new(&reader, 7)?;
    other_writer.execute("DELETE FROM imaginary_events WHERE id=1", [])?;
    assert_eq!(total_changes(&reader)?, 8); // 1 invented event + 7 migration rows
    assert!(lease.read_again().is_err()); // Detects this count drift, not all writes.
    assert_eq!(reader.query_row("PRAGMA query_only", [], |r| r.get::<_, i64>(0))?, 1);
    Ok(())
}
