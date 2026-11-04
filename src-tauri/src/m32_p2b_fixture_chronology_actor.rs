//! P2b: single-owner chronology command actor for invented v7 fixtures ONLY.
//!
//! Compiled exclusively under #[cfg(test)] in lib.rs. Mirrors the bounded
//! single-owner queue/teardown pattern of m32_v7_writer_service without
//! changing PreparedV7Writer, V7WriterAdmission, or the production runtime.
//! Receives ONE caller-created RAM fixture Connection; no path opener, IPC,
//! profile resolution, migration registration, backup, or recovery.

use crate::{
    m32_manual_chronology as chronology,
    m32_p2_fixture_chronology_service::{
        FixtureChronologyService, FixtureError, FixtureSnapshot, RelationDraft,
    },
};
use rusqlite::Connection;
use std::{
    sync::mpsc::{self, Receiver, Sender, SyncSender, TrySendError},
    thread::{self, JoinHandle},
};

const QUEUE_CAPACITY: usize = 8;

#[derive(Debug)]
pub(crate) enum ActorError {
    Rejected(FixtureError),
    Domain(FixtureError),
    QueueFull,
    Disconnected,
    WorkerPanicked,
}

#[derive(Clone)]
pub(crate) struct AnchorInput {
    pub id: String,
    pub universe_id: String,
    pub time_kind: String,
    pub calendar_id: Option<String>,
    pub event_entity_id: Option<String>,
    pub source_revision_id: Option<String>,
    pub exact_label: Option<String>,
    pub window_start_text: Option<String>,
    pub window_end_text: Option<String>,
    pub precision_text: Option<String>,
}
impl AnchorInput {
    fn draft(&self) -> chronology::AnchorDraft<'_> {
        chronology::AnchorDraft {
            id: &self.id,
            universe_id: &self.universe_id,
            time_kind: &self.time_kind,
            calendar_id: self.calendar_id.as_deref(),
            event_entity_id: self.event_entity_id.as_deref(),
            source_revision_id: self.source_revision_id.as_deref(),
            exact_label: self.exact_label.as_deref(),
            window_start_text: self.window_start_text.as_deref(),
            window_end_text: self.window_end_text.as_deref(),
            precision_text: self.precision_text.as_deref(),
        }
    }
}

#[derive(Clone)]
pub(crate) struct RelationInput {
    pub id: String,
    pub universe_id: String,
    pub before_anchor_id: String,
    pub after_anchor_id: String,
    pub reason: String,
    pub source_revision_id: Option<String>,
}
impl RelationInput {
    fn draft(&self) -> RelationDraft<'_> {
        RelationDraft {
            id: &self.id,
            universe_id: &self.universe_id,
            before_anchor_id: &self.before_anchor_id,
            after_anchor_id: &self.after_anchor_id,
            reason: &self.reason,
            source_revision_id: self.source_revision_id.as_deref(),
        }
    }
}

type Reply<T> = Sender<Result<T, FixtureError>>;
enum Command {
    Calendar {
        id: String, universe: String, name: String, definition: String,
        reply: Reply<()>,
    },
    Anchor {
        anchor: AnchorInput, relation: Option<RelationInput>, reply: Reply<()>,
    },
    Precedence {
        relation: RelationInput, reply: Reply<()>,
    },
    Snapshot {
        universe: String, reply: Reply<FixtureSnapshot>,
    },
    RevokePrecedence {
        decision_id: String, universe: String, prior_id: String,
        reason: String, source_revision_id: Option<String>, reply: Reply<()>,
    },

    // P2d typed test-only restatement; stage-4 SQL overlay required.
    RestatePrecedence {
        id: String, universe: String, prior_id: String,
        before: String, after: String, reason: String,
        source_revision_id: Option<String>, reply: Reply<()>,
    },
    ActiveGraph {
        universe: String, reply: Reply<Vec<chronology::ActivePrecedence>>,
    },

    // P2e: one authored revocation + one restatement; single actor command
    // and a single SQLite IMMEDIATE transaction on the preopened test fixture.
    CorrectPrecedence {
        decision_id: String, restatement_id: String, universe: String,
        prior_id: String, before: String, after: String, reason: String,
        source_revision_id: Option<String>, reply: Reply<()>,
    },

    // P2f: speculative author review, always rolled back on the worker.
    PreviewCorrection {
        decision_id: String, restatement_id: String, universe: String,
        prior_id: String, before: String, after: String, reason: String,
        source_revision_id: Option<String>,
        reply: Reply<crate::m32_p2_fixture_chronology_service::CorrectionPreview>,
    },
    Stop(Sender<()>),
}

#[derive(Clone)]
pub(crate) struct FixtureChronologyClient {
    queue: SyncSender<Command>,
}
impl FixtureChronologyClient {
    fn call<T>(
        &self, make: impl FnOnce(Reply<T>) -> Command,
    ) -> Result<T, ActorError> {
        let (tx, rx) = mpsc::channel();
        self.queue.try_send(make(tx)).map_err(|error| match error {
            TrySendError::Full(_) => ActorError::QueueFull,
            TrySendError::Disconnected(_) => ActorError::Disconnected,
        })?;
        rx.recv().map_err(|_| ActorError::Disconnected)?
            .map_err(ActorError::Domain)
    }

    pub(crate) fn create_calendar(
        &self, id: String, universe: String, name: String, definition: String,
    ) -> Result<(), ActorError> {
        self.call(|reply| Command::Calendar { id, universe, name, definition, reply })
    }
    pub(crate) fn create_anchor(
        &self, anchor: AnchorInput, relation: Option<RelationInput>,
    ) -> Result<(), ActorError> {
        self.call(|reply| Command::Anchor { anchor, relation, reply })
    }
    pub(crate) fn create_precedence(&self, relation: RelationInput) -> Result<(), ActorError> {
        self.call(|reply| Command::Precedence { relation, reply })
    }
    pub(crate) fn snapshot(&self, universe: String) -> Result<FixtureSnapshot, ActorError> {
        self.call(|reply| Command::Snapshot { universe, reply })
    }
    pub(crate) fn revoke_precedence(
        &self, decision_id: String, universe: String, prior_id: String,
        reason: String, source_revision_id: Option<String>,
    ) -> Result<(), ActorError> {
        self.call(|reply| Command::RevokePrecedence {
            decision_id, universe, prior_id, reason, source_revision_id, reply,
        })
    }

    pub(crate) fn restate_precedence(
        &self, id: String, universe: String, prior_id: String,
        before: String, after: String, reason: String,
        source_revision_id: Option<String>,
    ) -> Result<(), ActorError> {
        self.call(|reply| Command::RestatePrecedence {
            id, universe, prior_id, before, after, reason, source_revision_id, reply,
        })
    }
    pub(crate) fn p2d_active_graph(
        &self, universe: String,
    ) -> Result<Vec<chronology::ActivePrecedence>, ActorError> {
        self.call(|reply| Command::ActiveGraph { universe, reply })
    }

    pub(crate) fn correct_precedence_atomically(
        &self, decision_id: String, restatement_id: String, universe: String,
        prior_id: String, before: String, after: String, reason: String,
        source_revision_id: Option<String>,
    ) -> Result<(), ActorError> {
        self.call(|reply| Command::CorrectPrecedence {
            decision_id, restatement_id, universe, prior_id, before, after,
            reason, source_revision_id, reply,
        })
    }

    pub(crate) fn preview_atomic_correction(
        &self, decision_id: String, restatement_id: String, universe: String,
        prior_id: String, before: String, after: String, reason: String,
        source_revision_id: Option<String>,
    ) -> Result<crate::m32_p2_fixture_chronology_service::CorrectionPreview, ActorError> {
        self.call(|reply| Command::PreviewCorrection {
            decision_id, restatement_id, universe, prior_id, before, after,
            reason, source_revision_id, reply,
        })
    }


}

fn run(mut connection: Connection, rx: Receiver<Command>) {
    // The exclusive fixture was validated BEFORE thread transfer; no reopening.
    let Ok(mut service) = FixtureChronologyService::from_already_opened_disposable_v7(&mut connection) else {
        return;
    };
    while let Ok(command) = rx.recv() {
        match command {
            Command::Calendar { id, universe, name, definition, reply } => {
                let _ = reply.send(service.create_calendar(&id, &universe, &name, &definition));
            }
            Command::Anchor { anchor, relation, reply } => {
                let _ = reply.send(service.create_anchor_with_optional_relation(
                    anchor.draft(), relation.as_ref().map(RelationInput::draft),
                ));
            }
            Command::Precedence { relation, reply } => {
                let _ = reply.send(service.create_precedence(relation.draft()));
            }
            Command::Snapshot { universe, reply } => {
                let _ = reply.send(service.snapshot(&universe));
            }
            Command::RevokePrecedence {
                decision_id, universe, prior_id, reason, source_revision_id, reply,
            } => {
                let _ = reply.send(service.revoke_precedence(
                    &decision_id, &universe, &prior_id, &reason,
                    source_revision_id.as_deref(),
                ));
            }

            Command::RestatePrecedence {
                id, universe, prior_id, before, after, reason,
                source_revision_id, reply,
            } => {
                let _ = reply.send(service.restate_revoked_precedence(
                    &id, &universe, &prior_id, &before, &after, &reason,
                    source_revision_id.as_deref(),
                ));
            }
            Command::ActiveGraph { universe, reply } => {
                let _ = reply.send(service.p2d_active_graph(&universe));
            }

            Command::CorrectPrecedence {
                decision_id, restatement_id, universe, prior_id, before,
                after, reason, source_revision_id, reply,
            } => {
                let _ = reply.send(service.correct_precedence_atomically(
                    &decision_id, &restatement_id, &universe, &prior_id,
                    &before, &after, &reason, source_revision_id.as_deref(),
                ));
            }


            Command::PreviewCorrection {
                decision_id, restatement_id, universe, prior_id,
                before, after, reason, source_revision_id, reply,
            } => {
                let _ = reply.send(service.preview_atomic_correction(
                    &decision_id, &restatement_id, &universe, &prior_id,
                    &before, &after, &reason, source_revision_id.as_deref(),
                ));
            }
            Command::Stop(ack) => {
                let _ = ack.send(());
                break;
            }
        }
    }
    // SQLite connection dropped on worker, never exported or reopened.
}

pub(crate) struct FixtureChronologyActor {
    client: FixtureChronologyClient,
    worker: Option<JoinHandle<()>>,
}
impl FixtureChronologyActor {
    /// Caller-created fixture only. This is not a source-identity gate.
    pub(crate) fn from_preopened_invented_v7(mut connection: Connection)
        -> Result<Self, ActorError>
    {
        FixtureChronologyService::from_already_opened_disposable_v7(&mut connection)
            .map_err(ActorError::Rejected)?;
        // P2b is RAM-only even in tests: never accept a fixture backed by a
        // pathname. This is intentionally stricter than the P2a disk contract.
        let backing: String = connection.query_row(
            "SELECT file FROM pragma_database_list WHERE name='main'",
            [], |row| row.get(0),
        ).map_err(|_| ActorError::Rejected(FixtureError::Stop("cannot verify RAM-only main")))?;
        if !backing.is_empty() {
            return Err(ActorError::Rejected(FixtureError::Stop("disk-backed database refused")));
        }
        let (queue, rx) = mpsc::sync_channel(QUEUE_CAPACITY);
        let worker = thread::spawn(move || run(connection, rx));
        Ok(Self {
            client: FixtureChronologyClient { queue },
            worker: Some(worker),
        })
    }

    pub(crate) fn client(&self) -> FixtureChronologyClient {
        self.client.clone()
    }

    fn stop(&mut self) -> Result<(), ActorError> {
        let Some(worker) = self.worker.take() else { return Ok(()); };
        let (tx, rx) = mpsc::channel();
        let ok = self.client.queue.send(Command::Stop(tx)).is_ok() && rx.recv().is_ok();
        let joined = worker.join().is_ok();
        if ok && joined { Ok(()) } else { Err(ActorError::WorkerPanicked) }
    }

    pub(crate) fn shutdown(mut self) -> Result<(), ActorError> { self.stop() }
}
impl Drop for FixtureChronologyActor {
    fn drop(&mut self) { let _ = self.stop(); }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::database;

    fn invented_v7() -> Connection {
        let mut db = crate::world_time_schema_tests::v6();
        db.execute_batch(
            "INSERT INTO universes(id,name) VALUES ('u1','Invented'),('u2','Other');
             INSERT INTO novels(id,universe_id,series_id,title,sort_order)
               VALUES ('n1','u1',NULL,'Novel',0);
             INSERT INTO chapters(id,novel_id,title,sort_order)
               VALUES ('c1','n1','Chapter',0);
             INSERT INTO scenes(id,chapter_id,title,sort_order)
               VALUES ('s1','c1','Scene',0);
             INSERT INTO scene_text_revisions(id,scene_id,revision_number,content)
               VALUES ('r2','s1',1,'old'),('r3','s1',2,'current');
             INSERT INTO scene_revision_heads(scene_id,revision_id) VALUES ('s1','r3');"
        ).unwrap();
        let tx = db.transaction().unwrap();
        tx.execute_batch(include_str!("../sql/m3_1_world_time_v7_candidate.sql")).unwrap();
        tx.execute_batch(include_str!("../sql/m3_2_chronology_decisions_candidate.sql")).unwrap();
        tx.execute("INSERT INTO schema_migrations(version,name)
                    VALUES (7,'007_create_world_time_foundation')", []).unwrap();
        tx.commit().unwrap();
        assert_eq!(database::current_schema_version(&db).unwrap(), 7);
        db
    }

    fn anchor(id: &str, universe: &str) -> AnchorInput {
        AnchorInput {
            id: id.into(), universe_id: universe.into(), time_kind: "relative".into(),
            calendar_id: None, event_entity_id: None,
            source_revision_id: if universe == "u1" { Some("r2".into()) } else { None },
            exact_label: None, window_start_text: None, window_end_text: None,
            precision_text: None,
        }
    }
    fn before(id: &str, a: &str, b: &str) -> RelationInput {
        RelationInput {
            id: id.into(), universe_id: "u1".into(),
            before_anchor_id: a.into(), after_anchor_id: b.into(),
            reason: "Explicit author order".into(), source_revision_id: Some("r2".into()),
        }
    }

    #[test]
    fn p2b_two_clients_serialize_v7_fixture_without_total_order() {
        let owner = FixtureChronologyActor::from_preopened_invented_v7(invented_v7()).unwrap();
        let first = owner.client();
        let second = owner.client();
        first.create_calendar("cal".into(),"u1".into(),"Cycles".into(),"Fiction".into()).unwrap();
        let a = thread::spawn(move || first.create_anchor(anchor("a1","u1"), None));
        let b = thread::spawn(move || second.create_anchor(anchor("a2","u1"), None));
        a.join().unwrap().unwrap();
        b.join().unwrap().unwrap();
        let client=owner.client();
        client.create_precedence(before("edge", "a1", "a2")).unwrap();
        let view=client.snapshot("u1".into()).unwrap();
        assert_eq!(view.current_anchor_ids, vec!["a1","a2"]);
        assert_eq!(view.precedences.len(), 1);
        assert!(view.anchors.iter().all(|a| a.source_revision_id.as_deref()==Some("r2")));
        assert!(client.snapshot("u2".into()).unwrap().anchors.is_empty());
        owner.shutdown().unwrap();
    }




    #[test]
    fn p2f_actor_preview_is_not_a_confirmation_token_and_detects_intervening_edges() {
        let db = {
            let db = invented_v7();
            db.execute_batch(include_str!("../sql/m3_2_active_precedence_candidate.sql"))
                .expect("Invented v7 RAM only");
            db
        };
        let owner = FixtureChronologyActor::from_preopened_invented_v7(db).unwrap();
        let preview_client = owner.client();
        let other_client = owner.client();
        for id in ["a1","a2","a3"] {
            preview_client.create_anchor(anchor(id,"u1"),None).unwrap();
        }
        preview_client.create_precedence(before("old12","a1","a2")).unwrap();
        let dry_run=preview_client.preview_atomic_correction(
            "decision12".into(),"new21".into(),"u1".into(),"old12".into(),
            "a2".into(),"a1".into(),"Author must confirm separately".into(),Some("r2".into()),
        ).unwrap();
        assert_eq!(dry_run.prior_precedence_id,"old12");
        assert_eq!(dry_run.proposed.id,"new21");
        assert_eq!(preview_client.snapshot("u1".into()).unwrap().current_precedence_ids,
                   vec!["old12"]);
        // A second serialized client changes the candidate graph AFTER preview.
        // The dry-run is not a token authorizing a stale write.
        other_client.create_precedence(before("edge13","a1","a3")).unwrap();
        other_client.create_precedence(before("edge32","a3","a2")).unwrap();
        assert!(matches!(preview_client.correct_precedence_atomically(
            "decision12".into(),"new21".into(),"u1".into(),"old12".into(),
            "a2".into(),"a1".into(),"Would now form an active cycle".into(),Some("r2".into()),
        ), Err(ActorError::Domain(_))));
        assert_eq!(preview_client.snapshot("u1".into()).unwrap().current_precedence_ids,
                   vec!["edge13","edge32","old12"]);
        assert_eq!(preview_client.p2d_active_graph("u1".into()).unwrap().len(),3);
        assert!(preview_client.snapshot("u2".into()).unwrap().anchors.is_empty());
        owner.shutdown().unwrap();
        assert!(matches!(preview_client.snapshot("u1".into()), Err(ActorError::Disconnected)));
    }

    #[test]
    fn p2e_actor_atomic_correction_is_single_command_and_failure_is_non_destructive() {
        let db = {
            let db = invented_v7();
            db.execute_batch(include_str!("../sql/m3_2_active_precedence_candidate.sql"))
                .expect("P2e inventoried overlay in RAM only");
            db
        };
        let owner = FixtureChronologyActor::from_preopened_invented_v7(db).unwrap();
        let client = owner.client();
        client.create_anchor(anchor("a1", "u1"), None).unwrap();
        client.create_anchor(anchor("a2", "u1"), None).unwrap();
        client.create_anchor(anchor("a3", "u1"), None).unwrap();
        client.create_precedence(before("old12", "a1", "a2")).unwrap();
        client.create_precedence(before("edge23", "a2", "a3")).unwrap();
        assert!(matches!(client.correct_precedence_atomically(
            "bad-decision".into(), "bad-cycle".into(), "u1".into(),
            "old12".into(), "a3".into(), "a2".into(),
            "Author tried cyclic rewrite".into(), Some("r2".into()),
        ), Err(ActorError::Domain(_))));
        assert_eq!(client.snapshot("u1".into()).unwrap().current_precedence_ids,
                   vec!["edge23", "old12"]);
        client.correct_precedence_atomically(
            "decision12".into(), "new21".into(), "u1".into(),
            "old12".into(), "a2".into(), "a1".into(),
            "Author revised history ordering".into(), Some("r2".into()),
        ).unwrap();
        let current = client.p2d_active_graph("u1".into()).unwrap();
        assert_eq!(current.len(), 2);
        let reverse = current.iter().find(|edge| edge.id == "new21").unwrap();
        assert_eq!((reverse.before_anchor_id.as_str(), reverse.after_anchor_id.as_str(),
                    reverse.origin.as_str()), ("a2", "a1", "restatement"));
        assert_eq!(client.snapshot("u1".into()).unwrap().precedences.len(), 2);
        assert_eq!(client.snapshot("u1".into()).unwrap().current_precedence_ids,
                   vec!["edge23"]);
        assert!(client.p2d_active_graph("u2".into()).unwrap().is_empty());
        owner.shutdown().unwrap();
        assert!(matches!(client.p2d_active_graph("u1".into()), Err(ActorError::Disconnected)));
    }

    #[test]
    fn p2d_actor_serialized_restatement_preserves_original_and_refuses_duplicates() {
        let db = {
            let db = invented_v7();
            db.execute_batch(include_str!("../sql/m3_2_active_precedence_candidate.sql"))
                .expect("P2d overlay on invented RAM only");
            db
        };
        let owner = FixtureChronologyActor::from_preopened_invented_v7(db).unwrap();
        let client = owner.client();
        client.create_anchor(anchor("a1", "u1"), None).unwrap();
        client.create_anchor(anchor("a2", "u1"), None).unwrap();
        client.create_precedence(before("old12", "a1", "a2")).unwrap();
        client.revoke_precedence(
            "rev12".into(), "u1".into(), "old12".into(),
            "Explicit author retirement".into(), Some("r2".into()),
        ).unwrap();
        client.restate_precedence(
            "correct21".into(), "u1".into(), "old12".into(),
            "a2".into(), "a1".into(), "Explicit author reversal".into(),
            Some("r2".into()),
        ).unwrap();
        let current = client.p2d_active_graph("u1".into()).unwrap();
        assert_eq!(current.len(), 1);
        assert_eq!(current[0].id, "correct21");
        assert_eq!(current[0].origin, "restatement");
        assert_eq!(current[0].before_anchor_id, "a2");
        assert_eq!(current[0].after_anchor_id, "a1");
        assert_eq!(client.snapshot("u1".into()).unwrap().precedences.len(), 1);
        assert!(matches!(client.restate_precedence(
            "duplicate".into(), "u1".into(), "old12".into(),
            "a2".into(), "a1".into(), "Duplicate not admitted".into(), None,
        ), Err(ActorError::Domain(_))));
        assert!(matches!(client.restate_precedence(
            "foreign".into(), "u2".into(), "old12".into(),
            "a2".into(), "a1".into(), "Wrong universe".into(), None,
        ), Err(ActorError::Domain(_))));
        assert!(client.p2d_active_graph("u2".into()).unwrap().is_empty());
        owner.shutdown().unwrap();
    }

    #[test]
    fn p2c_actor_revoke_is_serialized_and_retains_historical_relation() {
        let owner = FixtureChronologyActor::from_preopened_invented_v7(invented_v7()).unwrap();
        let client = owner.client();
        client.create_anchor(anchor("a1","u1"), None).unwrap();
        client.create_anchor(anchor("a2","u1"), None).unwrap();
        client.create_precedence(before("edge12","a1","a2")).unwrap();
        assert_eq!(client.snapshot("u1".into()).unwrap().current_precedence_ids, vec!["edge12"]);
        client.revoke_precedence(
            "decision1".into(),"u1".into(),"edge12".into(),
            "Author changed the chronology".into(),Some("r2".into()),
        ).unwrap();
        let state = client.snapshot("u1".into()).unwrap();
        assert_eq!(state.current_precedence_ids, Vec::<String>::new());
        assert_eq!(state.precedences.len(), 1);
        assert_eq!(state.current_anchor_ids, vec!["a1","a2"]);
        assert!(matches!(client.revoke_precedence(
            "decision2".into(),"u1".into(),"edge12".into(),
            "No duplicate retirements".into(),None,
        ), Err(ActorError::Domain(_))));
        assert!(matches!(client.revoke_precedence(
            "foreign".into(),"u2".into(),"edge12".into(),
            "Foreign universe".into(),None,
        ), Err(ActorError::Domain(_))));
        assert!(client.snapshot("u2".into()).unwrap().precedences.is_empty());
        owner.shutdown().unwrap();
    }

    #[test]
    fn p2b_actor_failed_relation_rolls_back_and_refuses_cycle_and_foreign_world() {
        let owner=FixtureChronologyActor::from_preopened_invented_v7(invented_v7()).unwrap();
        let client=owner.client();
        client.create_anchor(anchor("a1","u1"),None).unwrap();
        client.create_anchor(anchor("a2","u1"),Some(before("edge12","a1","a2"))).unwrap();
        assert!(matches!(
            client.create_anchor(anchor("ghost","u1"),Some(before("bad","missing","ghost"))),
            Err(ActorError::Domain(_))
        ));
        assert!(matches!(
            client.create_precedence(before("reverse","a2","a1")),
            Err(ActorError::Domain(_))
        ));
        assert!(matches!(
            client.create_anchor(anchor("foreign","u2"),Some(before("foreignedge","a1","foreign"))),
            Err(ActorError::Domain(_))
        ));
        let view=client.snapshot("u1".into()).unwrap();
        assert_eq!(view.current_anchor_ids,vec!["a1","a2"]);
        assert_eq!(view.precedences.len(),1);
        assert!(client.snapshot("u2".into()).unwrap().anchors.is_empty());
        owner.shutdown().unwrap();
    }

    #[test]
    fn p2b_actor_rejects_unqualified_v6_and_query_only() {
        let v6=crate::world_time_schema_tests::v6();
        assert!(matches!(
            FixtureChronologyActor::from_preopened_invented_v7(v6),
            Err(ActorError::Rejected(_))
        ));
        let db=invented_v7();
        db.pragma_update(None,"query_only",true).unwrap();
        assert!(matches!(
            FixtureChronologyActor::from_preopened_invented_v7(db),
            Err(ActorError::Rejected(_))
        ));
    }

    #[test]
    fn p2b_actor_shutdown_and_drop_revoke_cloned_clients() {
        let owner=FixtureChronologyActor::from_preopened_invented_v7(invented_v7()).unwrap();
        let client=owner.client();
        assert!(client.snapshot("u1".into()).is_ok());
        owner.shutdown().unwrap();
        assert!(matches!(client.snapshot("u1".into()),Err(ActorError::Disconnected)));
        let next=FixtureChronologyActor::from_preopened_invented_v7(invented_v7()).unwrap();
        let another=next.client();
        drop(next);
        assert!(matches!(another.snapshot("u1".into()),Err(ActorError::Disconnected)));
    }
    /// P3b consumes the SAME source-controlled fictional golden JSON as the
    /// TypeScript Vitest test. There is no network, wire transport or IPC.
    #[test]
    fn p3b_shared_golden_rust_actor_preserves_exact_historical_provenance() {
        let spec: serde_json::Value = serde_json::from_str(include_str!(
            "../../fixtures/m32_p3b_typed_chronology_contract_v1.json"
        )).unwrap();
        assert_eq!(spec["contract_version"].as_u64(), Some(1));
        assert_eq!(spec["data_origin"].as_str(), Some("fictional_cross_language_test_only"));
        assert_eq!(spec["fixture_name"].as_str(), Some("invented_isolated_chronology_v1"));
        for key in ["production_ipc_authorized", "operator_data_authorized", "writer_admitted"] {
            assert_eq!(spec[key].as_bool(), Some(false), "{key}");
        }
        let universe = spec["universe_id"].as_str().unwrap();
        let scene = spec["scene_id"].as_str().unwrap();
        let historical = spec["historical_revision_id"].as_str().unwrap();
        let head = spec["current_head_revision_id"].as_str().unwrap();
        assert_eq!(universe, "fiction-one");
        assert_eq!(scene, "fiction-s1");
        assert_eq!(historical, "fiction-r2");
        assert_eq!(head, "fiction-r3");
        assert_ne!(historical, head);

        let db = invented_v7();
        db.execute_batch(
            "INSERT INTO universes(id,name) VALUES ('fiction-one','Invented P3b world');
             INSERT INTO novels(id,universe_id,series_id,title,sort_order)
               VALUES ('fiction-n1','fiction-one',NULL,'Invented novel',0);
             INSERT INTO chapters(id,novel_id,title,sort_order)
               VALUES ('fiction-c1','fiction-n1','Invented chapter',0);
             INSERT INTO scenes(id,chapter_id,title,sort_order)
               VALUES ('fiction-s1','fiction-c1','Invented scene',0);
             INSERT INTO scene_text_revisions(id,scene_id,revision_number,content)
               VALUES ('fiction-r2','fiction-s1',1,'Earlier fiction'),
                      ('fiction-r3','fiction-s1',2,'Current fiction');
             INSERT INTO scene_revision_heads(scene_id,revision_id)
               VALUES ('fiction-s1','fiction-r3');"
        ).unwrap();
        let owner = FixtureChronologyActor::from_preopened_invented_v7(db).unwrap();
        let client = owner.client();
        let commands = spec["anchor_commands"].as_array().unwrap();
        assert_eq!(commands.len(), 3);
        for cmd in commands {
            assert_eq!(cmd["kind"].as_str(), Some("create_anchor_with_optional_relation"));
            assert_eq!(cmd["time_kind"].as_str(), Some("relative"));
            let anchor_id = cmd["anchor_id"].as_str().unwrap();
            let source = cmd["source_revision_id"].as_str().unwrap();
            assert_eq!(source, historical);
            let input = AnchorInput {
                id: anchor_id.to_owned(), universe_id: universe.to_owned(),
                time_kind: "relative".into(),
                calendar_id: None, event_entity_id: None,
                source_revision_id: Some(source.to_owned()),
                exact_label: None, window_start_text: None, window_end_text: None,
                precision_text: None,
            };
            let relation = cmd["relation"].as_object().map(|edge| {
                let after = edge["after_anchor_id"].as_str().unwrap();
                assert_eq!(after, "$new");
                RelationInput {
                    id: edge["id"].as_str().unwrap().into(),
                    universe_id: universe.into(),
                    before_anchor_id: edge["before_anchor_id"].as_str().unwrap().into(),
                    after_anchor_id: anchor_id.into(),
                    reason: edge["reason"].as_str().unwrap().into(),
                    source_revision_id: Some(source.into()),
                }
            });
            client.create_anchor(input, relation).unwrap();
        }
        let actual = client.snapshot(universe.into()).unwrap();
        let expected_ids: Vec<String> = spec["expected_current_anchor_ids"]
            .as_array().unwrap().iter().map(|v| v.as_str().unwrap().to_owned()).collect();
        assert_eq!(actual.current_anchor_ids, expected_ids);
        assert!(actual.anchors.iter().all(|a| a.source_revision_id.as_deref() == Some(historical)));
        let expected_edges = spec["expected_precedences"].as_array().unwrap();
        assert_eq!(actual.precedences.len(), expected_edges.len());
        let edge = &actual.precedences[0];
        assert_eq!(edge.id, expected_edges[0]["id"].as_str().unwrap());
        assert_eq!(edge.before_anchor_id, expected_edges[0]["before_anchor_id"].as_str().unwrap());
        assert_eq!(edge.after_anchor_id, expected_edges[0]["after_anchor_id"].as_str().unwrap());
        let incomparable = spec["expected_incomparable_anchor_id"].as_str().unwrap();
        assert!(!actual.precedences.iter().any(|e|
            e.before_anchor_id == incomparable || e.after_anchor_id == incomparable
        ));
        assert!(client.snapshot("u2".into()).unwrap().anchors.is_empty());

        // Negative witnesses: relation failure rolls back anchor; no
        // inferred cycle, foreign-Universe edge or wrong revision source.
        let invalid_relation = RelationInput {
            id: "fiction-invalid-edge".into(), universe_id: universe.into(),
            before_anchor_id: "missing".into(),
            after_anchor_id: "fiction-ghost".into(),
            reason: "Explicit invented error".into(),
            source_revision_id: Some(historical.into()),
        };
        let mut ghost = AnchorInput {
            id: "fiction-ghost".into(), universe_id: universe.into(),
            time_kind: "relative".into(), calendar_id: None, event_entity_id: None,
            source_revision_id: Some(historical.into()), exact_label: None,
            window_start_text: None, window_end_text: None, precision_text: None,
        };
        assert!(matches!(
            client.create_anchor(ghost.clone(), Some(invalid_relation)),
            Err(ActorError::Domain(_))
        ));
        assert!(matches!(
            client.create_precedence(RelationInput {
                id: "fiction-reverse-cycle".into(), universe_id: universe.into(),
                before_anchor_id: expected_ids[1].clone(),
                after_anchor_id: expected_ids[0].clone(),
                reason: "Invented cycle".into(), source_revision_id: Some(historical.into()),
            }),
            Err(ActorError::Domain(_))
        ));
        ghost.universe_id = "u2".into();
        ghost.source_revision_id = None;
        assert!(matches!(
            client.create_anchor(ghost, Some(RelationInput {
                id: "fiction-cross-world".into(), universe_id: "u2".into(),
                before_anchor_id: expected_ids[0].clone(), after_anchor_id: "fiction-ghost".into(),
                reason: "Cross world rejected".into(), source_revision_id: None,
            })),
            Err(ActorError::Domain(_))
        ));
        let mut wrong_revision = AnchorInput {
            id: "fiction-bad-revision".into(), universe_id: universe.into(),
            time_kind: "relative".into(), calendar_id: None, event_entity_id: None,
            source_revision_id: Some("r2".into()), exact_label: None,
            window_start_text: None, window_end_text: None, precision_text: None,
        };
        assert!(matches!(
            client.create_anchor(wrong_revision.clone(), None), Err(ActorError::Domain(_))
        ));
        wrong_revision.source_revision_id = Some("absent-rev".into());
        assert!(matches!(
            client.create_anchor(wrong_revision, None), Err(ActorError::Domain(_))
        ));
        assert_eq!(client.snapshot(universe.into()).unwrap().current_anchor_ids, expected_ids);
        owner.shutdown().unwrap();
    }

}
