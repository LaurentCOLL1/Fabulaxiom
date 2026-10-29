//! Prepared, **unwired** single-owner writer for a future admitted Greenfield
//! v7 profile. This module is built with the backend but is not registered as
//! Tauri State, IPC, a database opener, or an operator-facing command.
//!
//! It deliberately cannot construct its `V7WriterAdmission` token in normal
//! builds. A separately authorized source-identity and sidecar gate must
//! eventually supply that proof. Unit tests alone can mint a fictional token.

#![allow(dead_code)] // Prepared API: no runtime call site is authorized yet.

use std::{
    sync::mpsc::{self, Receiver, Sender, SyncSender, TrySendError},
    thread::{self, JoinHandle},
    time::Duration,
};

use rusqlite::{Connection, TransactionBehavior};

use crate::{
    database::{self, CURRENT_SCHEMA_VERSION},
    revisions::{
        self, CreateSceneRevisionInput, RevisionErrorPayload, SceneRevisionHistory,
        SceneTextRevision, SetCurrentSceneRevisionInput, SetSceneRevisionArchivedInput,
    },
};

const QUEUE_CAPACITY: usize = 8;
const BUSY_TIMEOUT: Duration = Duration::from_secs(3);

/// No constructor outside this module. It is *not* an authorization to open a
/// pathname, accept an existing profile, or bypass the M3.2 writer gate.
pub(crate) struct V7WriterAdmission {
    _sealed: (),
}

#[cfg(test)]
impl V7WriterAdmission {
    fn fictional_ram_only() -> Self {
        Self { _sealed: () }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) enum WriterError {
    AdmissionRejected,
    QueueFull,
    Disconnected,
    Domain(RevisionErrorPayload),
    WorkerPanicked,
}

type Reply<T> = Sender<Result<T, WriterError>>;

enum Command {
    Create(CreateSceneRevisionInput, Reply<SceneTextRevision>),
    SetCurrent(SetCurrentSceneRevisionInput, Reply<SceneTextRevision>),
    SetArchived(SetSceneRevisionArchivedInput, Reply<Vec<String>>),
    History(String, Reply<SceneRevisionHistory>),
    Stop(Sender<()>),
}

#[derive(Clone)]
pub(crate) struct V7WriterClient {
    queue: SyncSender<Command>,
}

impl V7WriterClient {
    fn call<T>(&self, construct: impl FnOnce(Reply<T>) -> Command) -> Result<T, WriterError> {
        let (reply_tx, reply_rx) = mpsc::channel();
        self.queue.try_send(construct(reply_tx)).map_err(|error| match error {
            TrySendError::Full(_) => WriterError::QueueFull,
            TrySendError::Disconnected(_) => WriterError::Disconnected,
        })?;
        reply_rx.recv().map_err(|_| WriterError::Disconnected)?
    }

    pub(crate) fn create_revision(
        &self, input: CreateSceneRevisionInput,
    ) -> Result<SceneTextRevision, WriterError> {
        self.call(|reply| Command::Create(input, reply))
    }

    pub(crate) fn set_current_revision(
        &self, input: SetCurrentSceneRevisionInput,
    ) -> Result<SceneTextRevision, WriterError> {
        self.call(|reply| Command::SetCurrent(input, reply))
    }

    pub(crate) fn set_revision_archived(
        &self, input: SetSceneRevisionArchivedInput,
    ) -> Result<Vec<String>, WriterError> {
        self.call(|reply| Command::SetArchived(input, reply))
    }

    pub(crate) fn revision_history(&self, scene_id: String) -> Result<SceneRevisionHistory, WriterError> {
        self.call(|reply| Command::History(scene_id, reply))
    }
}

fn preadmission_checks(connection: &Connection) -> Result<(), WriterError> {
    if !connection.is_autocommit()
        || connection.is_readonly("main").unwrap_or(true)
        || !database::foreign_keys_enabled(connection).unwrap_or(false)
        || database::current_schema_version(connection).ok() != Some(CURRENT_SCHEMA_VERSION)
    {
        return Err(WriterError::AdmissionRejected);
    }
    let query_only: i64 = connection
        .pragma_query_value(None, "query_only", |row| row.get(0))
        .map_err(|_| WriterError::AdmissionRejected)?;
    if query_only != 0 {
        return Err(WriterError::AdmissionRejected);
    }
    let mut names = connection
        .prepare("PRAGMA database_list")
        .map_err(|_| WriterError::AdmissionRejected)?;
    let attached = names
        .query_map([], |row| row.get::<_, String>(1))
        .map_err(|_| WriterError::AdmissionRejected)?
        .collect::<rusqlite::Result<Vec<_>>>()
        .map_err(|_| WriterError::AdmissionRejected)?;
    if attached.iter().any(|name| name != "main" && name != "temp") || !attached.iter().any(|name| name == "main") {
        return Err(WriterError::AdmissionRejected);
    }
    Ok(())
}

fn worker_loop(mut connection: Connection, inbox: Receiver<Command>) {
    // Existing domain revision operations use Connection::transaction(),
    // which respects this per-connection default: BEGIN IMMEDIATE, not DEFERRED.
    connection.set_transaction_behavior(TransactionBehavior::Immediate);
    while let Ok(command) = inbox.recv() {
        match command {
            Command::Create(input, reply) => {
                let result = revisions::create_scene_revision(&mut connection, input)
                    .map_err(|error| WriterError::Domain(error.payload()));
                let _ = reply.send(result);
            }
            Command::SetCurrent(input, reply) => {
                let result = revisions::set_current_scene_revision(&mut connection, input)
                    .map_err(|error| WriterError::Domain(error.payload()));
                let _ = reply.send(result);
            }
            Command::SetArchived(input, reply) => {
                let result = revisions::set_scene_revision_archived(&mut connection, input)
                    .map_err(|error| WriterError::Domain(error.payload()));
                let _ = reply.send(result);
            }
            Command::History(scene_id, reply) => {
                let result = revisions::scene_revision_history(&connection, &scene_id)
                    .map_err(|error| WriterError::Domain(error.payload()));
                let _ = reply.send(result);
            }
            Command::Stop(ack) => {
                let _ = ack.send(());
                break;
            }
        }
    }
    // The same connection is dropped here. No pathname reopening, fallback
    // backup, migration, checkpoint or implicit new connection is attempted.
}

/// Has no path-based constructor, and no registration in lib.rs's Tauri builder.
pub(crate) struct PreparedV7Writer {
    client: V7WriterClient,
    worker: Option<JoinHandle<()>>,
}

impl PreparedV7Writer {
    pub(crate) fn admit(
        connection: Connection, _proof: V7WriterAdmission,
    ) -> Result<Self, WriterError> {
        preadmission_checks(&connection)?;
        connection.busy_timeout(BUSY_TIMEOUT).map_err(|_| WriterError::AdmissionRejected)?;
        let (queue, inbox) = mpsc::sync_channel(QUEUE_CAPACITY);
        let worker = thread::spawn(move || worker_loop(connection, inbox));
        Ok(Self { client: V7WriterClient { queue }, worker: Some(worker) })
    }

    pub(crate) fn client(&self) -> V7WriterClient {
        self.client.clone()
    }

    fn stop_worker(&mut self) -> Result<(), WriterError> {
        let Some(worker) = self.worker.take() else { return Ok(()); };
        let (ack_tx, ack_rx) = mpsc::channel();
        let acknowledged = self.client.queue.send(Command::Stop(ack_tx)).is_ok()
            && ack_rx.recv().is_ok();
        let joined = worker.join().is_ok();
        if acknowledged && joined { Ok(()) } else { Err(WriterError::WorkerPanicked) }
    }

    pub(crate) fn shutdown(mut self) -> Result<(), WriterError> {
        self.stop_worker()
    }
}

impl Drop for PreparedV7Writer {
    fn drop(&mut self) {
        let _ = self.stop_worker();
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn fictive_connection() -> Connection {
        let mut db = Connection::open_in_memory().expect("invented RAM, never an operator path");
        database::configure_connection(&db).unwrap();
        database::run_migrations(&mut db).unwrap();
        db.execute_batch("INSERT INTO universes (id, name) VALUES ('u1','Invented');
            INSERT INTO novels (id, universe_id, series_id, title, sort_order) VALUES ('n1','u1',NULL,'Invented',0);
            INSERT INTO chapters (id, novel_id, title, sort_order) VALUES ('c1','n1','Invented',0);
            INSERT INTO scenes (id, chapter_id, title, sort_order) VALUES ('sc1','c1','Invented',0);")
            .unwrap();
        db
    }

    fn new_actor() -> PreparedV7Writer {
        PreparedV7Writer::admit(fictive_connection(), V7WriterAdmission::fictional_ram_only())
            .unwrap()
    }

    fn revision(id: &str, scene: &str) -> CreateSceneRevisionInput {
        CreateSceneRevisionInput {
            id: id.into(), scene_id: scene.into(), content: format!("Invented text {id}"),
        }
    }

    #[test]
    fn m32_v7_writer_prepared_serializes_typed_revision_and_read() {
        let owner = new_actor();
        let client = owner.client();
        let created = client.create_revision(revision("r1", "sc1")).unwrap();
        assert_eq!(created.revision_number, 1);
        let history = client.revision_history("sc1".into()).unwrap();
        assert_eq!(history.current_revision_id.as_deref(), Some("r1"));
        assert_eq!(history.revisions, vec![created]);
        client.create_revision(revision("r2", "sc1")).unwrap();
        assert_eq!(client.set_revision_archived(SetSceneRevisionArchivedInput {
            scene_id: "sc1".into(), revision_id: "r1".into(), archived: true,
        }).unwrap(), vec!["r1".to_string()]);
        assert_eq!(client.set_current_revision(SetCurrentSceneRevisionInput {
            scene_id: "sc1".into(), revision_id: "r1".into(),
        }).unwrap().revision_number, 1);
        assert_eq!(client.set_revision_archived(SetSceneRevisionArchivedInput {
            scene_id: "sc1".into(), revision_id: "r1".into(), archived: false,
        }).unwrap(), Vec::<String>::new());
        assert_eq!(client.revision_history("sc1".into()).unwrap().current_revision_id.as_deref(), Some("r1"));
        owner.shutdown().unwrap();
    }

    #[test]
    fn m32_v7_writer_prepared_two_clients_one_connection_ordered() {
        let owner = new_actor();
        let first = owner.client();
        let second = owner.client();
        let a = thread::spawn(move || first.create_revision(revision("r1", "sc1")));
        let b = thread::spawn(move || second.create_revision(revision("r2", "sc1")));
        let mut numbers = [a.join().unwrap().unwrap().revision_number,
                           b.join().unwrap().unwrap().revision_number];
        numbers.sort_unstable();
        assert_eq!(numbers, [1, 2]);
        assert_eq!(owner.client().revision_history("sc1".into()).unwrap().revisions.len(), 2);
        owner.shutdown().unwrap();
    }

    #[test]
    fn m32_v7_writer_prepared_rejects_unmigrated_connection_without_mutation() {
        let db = Connection::open_in_memory().unwrap();
        assert!(matches!(PreparedV7Writer::admit(db, V7WriterAdmission::fictional_ram_only()),
            Err(WriterError::AdmissionRejected)));
    }

    #[test]
    fn m32_v7_writer_prepared_rejects_active_transaction() {
        let db = fictive_connection();
        db.execute_batch("BEGIN IMMEDIATE").unwrap();
        assert!(matches!(PreparedV7Writer::admit(db, V7WriterAdmission::fictional_ram_only()),
            Err(WriterError::AdmissionRejected)));
    }

    #[test]
    fn m32_v7_writer_prepared_rejects_query_only() {
        let db = fictive_connection();
        db.pragma_update(None, "query_only", true).unwrap();
        assert!(matches!(PreparedV7Writer::admit(db, V7WriterAdmission::fictional_ram_only()),
            Err(WriterError::AdmissionRejected)));
    }

    #[test]
    fn m32_v7_writer_prepared_rejects_attached_ram_database() {
        let db = fictive_connection();
        db.execute_batch("ATTACH DATABASE ':memory:' AS unexpected").unwrap();
        assert!(matches!(PreparedV7Writer::admit(db, V7WriterAdmission::fictional_ram_only()),
            Err(WriterError::AdmissionRejected)));
    }

    #[test]
    fn m32_v7_writer_prepared_domain_refusal_preserves_prior_state() {
        let owner = new_actor();
        let client = owner.client();
        assert!(matches!(client.create_revision(revision("bad", "missing")),
            Err(WriterError::Domain(_))));
        assert!(client.revision_history("sc1".into()).unwrap().revisions.is_empty());
        assert_eq!(client.create_revision(revision("r1", "sc1")).unwrap().revision_number, 1);
        owner.shutdown().unwrap();
    }

    #[test]
    fn m32_v7_writer_prepared_shutdown_revokes_cloned_clients() {
        let owner = new_actor();
        let client = owner.client();
        owner.shutdown().unwrap();
        assert_eq!(client.create_revision(revision("later", "sc1")),
            Err(WriterError::Disconnected));
    }

    // Fictional RAM-only owner tests. They cannot authorize a real v7 file.
    #[test]
    fn m32_v7_writer_prepared_r5_rejects_incomplete_migration_lineage() {
        let db = fictive_connection();
        db.execute("DELETE FROM schema_migrations WHERE version = ?1", [CURRENT_SCHEMA_VERSION]).unwrap();
        assert!(matches!(
            PreparedV7Writer::admit(db, V7WriterAdmission::fictional_ram_only()),
            Err(WriterError::AdmissionRejected)
        ));
    }

    #[test]
    fn m32_v7_writer_prepared_r5_rejects_foreign_keys_off() {
        let db = fictive_connection();
        db.pragma_update(None, "foreign_keys", false).unwrap();
        assert!(!database::foreign_keys_enabled(&db).unwrap());
        assert!(matches!(
            PreparedV7Writer::admit(db, V7WriterAdmission::fictional_ram_only()),
            Err(WriterError::AdmissionRejected)
        ));
    }

    #[test]
    fn m32_v7_writer_prepared_r8_drop_revokes_multiple_clients() {
        let owner = new_actor();
        let first = owner.client();
        let second = owner.client();
        assert!(first.revision_history("sc1".into()).is_ok());
        drop(owner);
        assert_eq!(first.revision_history("sc1".into()), Err(WriterError::Disconnected));
        assert_eq!(second.create_revision(revision("after-drop", "sc1")),
            Err(WriterError::Disconnected));
    }

}
