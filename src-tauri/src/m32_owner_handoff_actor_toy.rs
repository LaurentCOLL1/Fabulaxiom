//! M3.2/G3: test-only Rust thread handoff of an ALREADY-OPEN INVENTED RAM source.
//! This is a toy actor, NOT source authentication, production Tauri state or IPC.
//! Only Connection::open_in_memory creates source/destination. Never operator I/O.
//! No path, file, migration runner, production marker, SQLite sidecar or network.

use rusqlite::{backup::Backup, params, Connection};
use std::{
    sync::{
        atomic::{AtomicU64, Ordering},
        mpsc::{self, Receiver, Sender, SyncSender},
    },
    thread::{self, JoinHandle},
    time::Duration,
};

static NEXT_TOY_LEASE: AtomicU64 = AtomicU64::new(1);
const TOY_LIMIT_BYTES: i64 = 2 * 1024 * 1024;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum ToyError {
    InvalidFixture,
    BadLease,
    Revoked,
    Poisoned,
    Disconnected,
    Sqlite,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
struct ToyLease(u64);

/// A deliberately uncloneable RAM-only fixture. Its sole constructor opens RAM.
/// This type CANNOT attest to a Windows source identity or historic provenance.
struct InventedSource {
    conn: Connection,
    version: i64,
}

impl InventedSource {
    fn new(version: i64) -> Result<Self, ToyError> {
        if version != 6 && version != 7 {
            return Err(ToyError::InvalidFixture);
        }
        let conn = Connection::open_in_memory().map_err(|_| ToyError::Sqlite)?;
        conn.execute_batch(
            "PRAGMA foreign_keys=ON;
             CREATE TABLE imaginary_items (id INTEGER PRIMARY KEY, detail TEXT NOT NULL);
             CREATE TABLE schema_migrations (version INTEGER PRIMARY KEY);
             INSERT INTO imaginary_items VALUES (1, 'Invented RAM-only content');",
        )
        .map_err(|_| ToyError::Sqlite)?;
        for step in 1..=version {
            conn.execute("INSERT INTO schema_migrations VALUES (?1)", params![step])
                .map_err(|_| ToyError::Sqlite)?;
        }
        Ok(Self { conn, version })
    }
}

fn memory_only(conn: &Connection) -> Result<bool, ToyError> {
    let mut stmt = conn.prepare("PRAGMA database_list").map_err(|_| ToyError::Sqlite)?;
    let rows = stmt
        .query_map([], |row| Ok((row.get::<_, String>(1)?, row.get::<_, String>(2)?)))
        .map_err(|_| ToyError::Sqlite)?
        .collect::<rusqlite::Result<Vec<_>>>()
        .map_err(|_| ToyError::Sqlite)?;
    let mut main = 0;
    let mut temp = 0;
    for (name, path) in rows {
        if !path.is_empty() {
            return Ok(false);
        }
        match name.as_str() {
            "main" => main += 1,
            "temp" => temp += 1, // SQLite may lazily create a harmless RAM temp schema.
            _ => return Ok(false),
        }
    }
    Ok(main == 1 && temp <= 1)
}

fn valid_fixture(conn: &Connection, version: i64) -> Result<bool, ToyError> {
    if !conn.is_autocommit() || !memory_only(conn)? {
        return Ok(false);
    }
    let pages: i64 = conn.query_row("PRAGMA page_count", [], |row| row.get(0))
        .map_err(|_| ToyError::Sqlite)?;
    let page_size: i64 = conn.query_row("PRAGMA page_size", [], |row| row.get(0))
        .map_err(|_| ToyError::Sqlite)?;
    let bytes = pages.checked_mul(page_size).ok_or(ToyError::InvalidFixture)?;
    if bytes < 1 || bytes > TOY_LIMIT_BYTES {
        return Ok(false);
    }
    let integrity: String = conn
        .query_row("PRAGMA integrity_check", [], |row| row.get(0))
        .map_err(|_| ToyError::Sqlite)?;
    let fk_errors: i64 = conn
        .query_row("SELECT COUNT(*) FROM pragma_foreign_key_check", [], |row| row.get(0))
        .map_err(|_| ToyError::Sqlite)?;
    let lineage = conn
        .prepare("SELECT version FROM schema_migrations ORDER BY version")
        .map_err(|_| ToyError::Sqlite)?
        .query_map([], |row| row.get::<_, i64>(0))
        .map_err(|_| ToyError::Sqlite)?
        .collect::<rusqlite::Result<Vec<_>>>()
        .map_err(|_| ToyError::Sqlite)?;
    let total: i64 = conn
        .query_row("SELECT COUNT(*) FROM imaginary_items", [], |row| row.get(0))
        .map_err(|_| ToyError::Sqlite)?;
    Ok(integrity == "ok" && fk_errors == 0 && total == 1
        && lineage == (1..=version).collect::<Vec<_>>())
}

fn ram_snapshot(source: &Connection, version: i64) -> Result<String, ToyError> {
    if !valid_fixture(source, version)? {
        return Err(ToyError::InvalidFixture);
    }
    let mut destination = Connection::open_in_memory().map_err(|_| ToyError::Sqlite)?;
    {
        let backup = Backup::new(source, &mut destination).map_err(|_| ToyError::Sqlite)?;
        backup.run_to_completion(16, Duration::from_millis(1), None)
            .map_err(|_| ToyError::Sqlite)?;
    }
    if !valid_fixture(&destination, version)? {
        return Err(ToyError::InvalidFixture);
    }
    destination.query_row("SELECT detail FROM imaginary_items WHERE id=1", [], |row| row.get(0))
        .map_err(|_| ToyError::Sqlite)
}

enum Command {
    Capture(ToyLease, Sender<Result<String, ToyError>>),
    Revoke(Sender<()>),
    PoisonForTest(Sender<()>),
    Stop(Sender<()>),
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum ActorState {
    Ready,
    Revoked,
    Poisoned,
}

fn worker_loop(
    connection: Connection,
    version: i64,
    lease: ToyLease,
    inbox: Receiver<Command>,
) {
    // The raw Connection is moved here exactly once. No other thread owns it.
    let mut source = Some(connection);
    let mut state = ActorState::Ready;
    while let Ok(command) = inbox.recv() {
        match command {
            Command::Capture(presented, response) => {
                let result = match state {
                    ActorState::Revoked => Err(ToyError::Revoked),
                    ActorState::Poisoned => Err(ToyError::Poisoned),
                    ActorState::Ready if presented != lease => Err(ToyError::BadLease),
                    ActorState::Ready => {
                        let outcome = source.as_ref()
                            .ok_or(ToyError::Poisoned)
                            .and_then(|conn| ram_snapshot(conn, version));
                        if outcome.is_err() {
                            source.take();
                            state = ActorState::Poisoned; // fail closed, never reopen
                        }
                        outcome
                    }
                };
                let _ = response.send(result);
            }
            Command::Revoke(ack) => {
                source.take();
                state = ActorState::Revoked;
                let _ = ack.send(());
            }
            Command::PoisonForTest(ack) => {
                source.take();
                state = ActorState::Poisoned;
                let _ = ack.send(());
            }
            Command::Stop(ack) => {
                source.take();
                let _ = ack.send(());
                break;
            }
        }
    }
    // Dropping the channel also drops source. No path-based recovery.
}

#[derive(Clone)]
struct ToyClient {
    queue: SyncSender<Command>,
}

impl ToyClient {
    fn capture(&self, ticket: ToyLease) -> Result<String, ToyError> {
        let (reply_tx, reply_rx) = mpsc::channel();
        self.queue.send(Command::Capture(ticket, reply_tx))
            .map_err(|_| ToyError::Disconnected)?;
        reply_rx.recv().map_err(|_| ToyError::Disconnected)?
    }

    fn revoke(&self) -> Result<(), ToyError> {
        let (reply_tx, reply_rx) = mpsc::channel();
        self.queue.send(Command::Revoke(reply_tx))
            .map_err(|_| ToyError::Disconnected)?;
        reply_rx.recv().map_err(|_| ToyError::Disconnected)
    }

    fn poison_for_test(&self) -> Result<(), ToyError> {
        let (reply_tx, reply_rx) = mpsc::channel();
        self.queue.send(Command::PoisonForTest(reply_tx))
            .map_err(|_| ToyError::Disconnected)?;
        reply_rx.recv().map_err(|_| ToyError::Disconnected)
    }
}

/// Owns the worker thread but never exposes a raw rusqlite::Connection.
/// This is NOT a Tauri State; admission can only consume InventedSource.
struct ToyActor {
    client: ToyClient,
    worker: Option<JoinHandle<()>>,
    lease: ToyLease,
}

impl ToyActor {
    fn admit(fixture: InventedSource) -> Result<Self, ToyError> {
        if !valid_fixture(&fixture.conn, fixture.version)? {
            return Err(ToyError::InvalidFixture);
        }
        let lease = ToyLease(NEXT_TOY_LEASE.fetch_add(1, Ordering::Relaxed));
        let (queue, inbox) = mpsc::sync_channel(8);
        let version = fixture.version;
        // A move of the connection, not a reopening of its pathname.
        let worker = thread::spawn(move || worker_loop(fixture.conn, version, lease, inbox));
        Ok(Self { client: ToyClient { queue }, worker: Some(worker), lease })
    }

    fn client(&self) -> ToyClient {
        self.client.clone() // Clones only a message sender, never the SQLite handle.
    }

    fn shutdown(mut self) -> Result<(), ToyError> {
        let (reply_tx, reply_rx) = mpsc::channel();
        let sent = self.client.queue.send(Command::Stop(reply_tx)).is_ok();
        let acknowledged = sent && reply_rx.recv().is_ok();
        let joined = match self.worker.take() {
            Some(worker) => worker.join().is_ok(),
            None => false,
        };
        if acknowledged && joined {
            Ok(())
        } else {
            Err(ToyError::Disconnected)
        }
    }
}

#[test]
fn m32_owner_handoff_actor_toy_move_preopened_ram_to_worker() -> Result<(), ToyError> {
    let actor = ToyActor::admit(InventedSource::new(7)?)?;
    assert_eq!(actor.client().capture(actor.lease)?, "Invented RAM-only content");
    actor.shutdown()
}

#[test]
fn m32_owner_handoff_actor_toy_reject_invalid_version() {
    assert!(matches!(InventedSource::new(8), Err(ToyError::InvalidFixture)));
}

#[test]
fn m32_owner_handoff_actor_toy_reject_pending_transaction() -> Result<(), ToyError> {
    let fixture = InventedSource::new(6)?;
    fixture.conn.execute_batch("BEGIN; UPDATE imaginary_items SET detail='pending';")
        .map_err(|_| ToyError::Sqlite)?;
    assert!(matches!(ToyActor::admit(fixture), Err(ToyError::InvalidFixture)));
    Ok(())
}

#[test]
fn m32_owner_handoff_actor_toy_reject_attached_memory_database() -> Result<(), ToyError> {
    let fixture = InventedSource::new(6)?;
    fixture.conn.execute_batch("ATTACH DATABASE ':memory:' AS unauthorized_extra")
        .map_err(|_| ToyError::Sqlite)?;
    assert!(matches!(ToyActor::admit(fixture), Err(ToyError::InvalidFixture)));
    Ok(())
}

#[test]
fn m32_owner_handoff_actor_toy_reject_migration_gap() -> Result<(), ToyError> {
    let fixture = InventedSource::new(6)?;
    fixture.conn.execute("DELETE FROM schema_migrations WHERE version=4", [])
        .map_err(|_| ToyError::Sqlite)?;
    assert!(matches!(ToyActor::admit(fixture), Err(ToyError::InvalidFixture)));
    Ok(())
}

#[test]
fn m32_owner_handoff_actor_toy_wrong_lease_does_not_revoke_good_one() -> Result<(), ToyError> {
    let actor = ToyActor::admit(InventedSource::new(6)?)?;
    let client = actor.client();
    assert_eq!(client.capture(ToyLease(0)), Err(ToyError::BadLease));
    assert!(client.capture(actor.lease).is_ok());
    actor.shutdown()
}

#[test]
fn m32_owner_handoff_actor_toy_two_clients_one_worker() -> Result<(), ToyError> {
    let actor = ToyActor::admit(InventedSource::new(6)?)?;
    let first = actor.client();
    let second = actor.client();
    let lease = actor.lease;
    let a = thread::spawn(move || first.capture(lease));
    let b = thread::spawn(move || second.capture(lease));
    assert_eq!(a.join().map_err(|_| ToyError::Disconnected)??, "Invented RAM-only content");
    assert_eq!(b.join().map_err(|_| ToyError::Disconnected)??, "Invented RAM-only content");
    actor.shutdown()
}

#[test]
fn m32_owner_handoff_actor_toy_revoke_closes_source_irreversibly() -> Result<(), ToyError> {
    let actor = ToyActor::admit(InventedSource::new(6)?)?;
    let client = actor.client();
    let ticket = actor.lease;
    assert!(client.capture(ticket).is_ok());
    client.revoke()?;
    assert_eq!(client.capture(ticket), Err(ToyError::Revoked));
    client.revoke()?;
    assert_eq!(client.capture(ticket), Err(ToyError::Revoked));
    actor.shutdown()
}

#[test]
fn m32_owner_handoff_actor_toy_poison_fails_closed_without_reopen() -> Result<(), ToyError> {
    let actor = ToyActor::admit(InventedSource::new(7)?)?;
    let client = actor.client();
    client.poison_for_test()?;
    assert_eq!(client.capture(actor.lease), Err(ToyError::Poisoned));
    assert_eq!(client.capture(actor.lease), Err(ToyError::Poisoned));
    actor.shutdown()
}

#[test]
fn m32_owner_handoff_actor_toy_shutdown_rejects_queued_future_use() -> Result<(), ToyError> {
    let actor = ToyActor::admit(InventedSource::new(6)?)?;
    let client = actor.client();
    let ticket = actor.lease;
    actor.shutdown()?;
    assert_eq!(client.capture(ticket), Err(ToyError::Disconnected));
    Ok(())
}
