//! P2a: test-only typed chronology fixture adapter.
//!
//! The caller lends an already-opened, invented v7 Connection. This module
//! never opens a path, mints production admission, registers Tauri State/IPC,
//! or accesses an operator profile. P1 independently proves NEW_ONLY disk
//! persistence; these tests qualify only the bounded service contract.

use crate::{database, m32_manual_chronology as chronology};
use rusqlite::{Connection, TransactionBehavior};

#[derive(Debug)]
pub(crate) enum FixtureError {
    Stop(&'static str),
    Sql(rusqlite::Error),
}

impl From<rusqlite::Error> for FixtureError {
    fn from(error: rusqlite::Error) -> Self { Self::Sql(error) }
}

pub(crate) struct RelationDraft<'a> {
    pub id: &'a str,
    pub universe_id: &'a str,
    pub before_anchor_id: &'a str,
    pub after_anchor_id: &'a str,
    pub reason: &'a str,
    pub source_revision_id: Option<&'a str>,
}

/// A non-persistent P2f author review result; NOT a write admission token.
#[derive(Debug, PartialEq, Eq)]
pub(crate) struct CorrectionPreview {
    pub prior_precedence_id: String,
    pub proposed: chronology::ActivePrecedence,
    // Fictional active edges at preview start and after staged correction.
    // Both are copied values, NOT committed database snapshots or grants.
    pub active_before: Vec<chronology::ActivePrecedence>,
    pub active_after: Vec<chronology::ActivePrecedence>,
}

pub(crate) struct FixtureSnapshot {
    pub anchors: Vec<chronology::ManualAnchor>,
    pub precedences: Vec<chronology::ManualPrecedence>,
    pub current_anchor_ids: Vec<String>,
    pub current_precedence_ids: Vec<String>,
}

pub(crate) struct FixtureChronologyService<'a> {
    db: &'a mut Connection,
}

impl<'a> FixtureChronologyService<'a> {
    pub fn from_already_opened_disposable_v7(
        db: &'a mut Connection,
    ) -> Result<Self, FixtureError> {
        // This is a TEST gate, not a reusable admission decision for an
        // operator path, another process, or an untrusted on-disk identity.
        if !db.is_autocommit()
            || db.is_readonly("main").unwrap_or(true)
            || !database::foreign_keys_enabled(db).unwrap_or(false)
            || database::current_schema_version(db).ok() != Some(7)
        {
            return Err(FixtureError::Stop("not an isolated writable v7 fixture"));
        }
        let query_only: i64 = db.pragma_query_value(None, "query_only", |r| r.get(0))?;
        if query_only != 0 {
            return Err(FixtureError::Stop("query_only connection"));
        }
        let names = {
            let mut stmt = db.prepare("PRAGMA database_list")?;
            let result = stmt.query_map([], |r| r.get::<_, String>(1))?
                .collect::<rusqlite::Result<Vec<_>>>()?;
            result
        };
        if !names.iter().any(|n| n == "main")
            || names.iter().any(|n| n != "main" && n != "temp")
        {
            return Err(FixtureError::Stop("unexpected attached database"));
        }
        for table in [
            "fictional_calendars",
            "world_time_anchors",
            "world_time_precedences",
            "world_time_anchor_decisions",
            "world_time_precedence_decisions",
        ] {
            let count: i64 = db.query_row(
                "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name=?1",
                [table],
                |r| r.get(0),
            )?;
            if count != 1 {
                return Err(FixtureError::Stop("incomplete chronology fixture schema"));
            }
        }
        Ok(Self { db })
    }

    pub fn create_calendar(
        &mut self, id: &str, universe: &str, name: &str, definition: &str,
    ) -> Result<(), FixtureError> {
        chronology::create_calendar(self.db, id, universe, name, definition)?;
        Ok(())
    }

    // A failed precedence causes SQLite transaction rollback of the new anchor.
    pub fn create_anchor_with_optional_relation(
        &mut self,
        anchor: chronology::AnchorDraft<'_>,
        relation: Option<RelationDraft<'_>>,
    ) -> Result<(), FixtureError> {
        if let Some(ref relation) = relation {
            if relation.universe_id != anchor.universe_id
                || (relation.before_anchor_id != anchor.id
                    && relation.after_anchor_id != anchor.id)
            {
                return Err(FixtureError::Stop("relation must contain the new anchor in the same universe"));
            }
        }
        let tx = self.db.transaction_with_behavior(TransactionBehavior::Immediate)?;
        chronology::create_anchor(&tx, anchor)?;
        if let Some(relation) = relation {
            chronology::create_precedence(
                &tx, relation.id, relation.universe_id,
                relation.before_anchor_id, relation.after_anchor_id,
                relation.reason, relation.source_revision_id,
            )?;
        }
        tx.commit()?;
        Ok(())
    }

    pub fn create_precedence(&mut self, relation: RelationDraft<'_>) -> Result<(), FixtureError> {
        let tx = self.db.transaction_with_behavior(TransactionBehavior::Immediate)?;
        chronology::create_precedence(
            &tx, relation.id, relation.universe_id,
            relation.before_anchor_id, relation.after_anchor_id,
            relation.reason, relation.source_revision_id,
        )?;
        tx.commit()?;
        Ok(())
    }

    /// Append-only retirement on an already borrowed v7 test fixture.
    /// The prior relation is preserved; the SQLite decision is not a delete.
    pub fn revoke_precedence(
        &mut self, decision_id: &str, universe: &str, prior_id: &str,
        reason: &str, source_revision_id: Option<&str>,
    ) -> Result<(), FixtureError> {
        let tx = self.db.transaction_with_behavior(TransactionBehavior::Immediate)?;
        chronology::decide_precedence(
            &tx, decision_id, universe, prior_id,
            "revoke", None, reason, source_revision_id,
        )?;
        tx.commit()?;
        Ok(())
    }


    // P2d: optional stage-4 SQL only on a disposable v7 fixture. Later
    // withdrawal/chain overlays have different semantics and fail closed.
    fn require_p2d_overlay(&self) -> Result<(), FixtureError> {
        for (kind, name) in [
            ("table", "world_time_precedence_restatements"),
            ("trigger", "m32_restatement_guard"),
            ("trigger", "m32_raw_precedence_active_graph_guard"),
        ] {
            let count: i64 = self.db.query_row(
                "SELECT COUNT(*) FROM sqlite_master WHERE type=?1 AND name=?2",
                rusqlite::params![kind, name],
                |row| row.get(0),
            )?;
            if count != 1 {
                return Err(FixtureError::Stop("P2d stage-4 RAM overlay not installed"));
            }
        }
        let later: i64 = self.db.query_row(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND
             name IN ('world_time_restatement_revocations',
                      'world_time_restatement_successors',
                      'world_time_successor_revocations')",
            [], |row| row.get(0),
        )?;
        if later != 0 {
            return Err(FixtureError::Stop("P2d refuses later correction layers"));
        }
        Ok(())
    }

    /// Re-author a previously revoked edge, never by reinserting into the
    /// immutable v7 raw-edge table whose historical cycle guard still applies.
    pub fn restate_revoked_precedence(
        &mut self, id: &str, universe: &str, prior_id: &str,
        before: &str, after: &str, reason: &str,
        source_revision_id: Option<&str>,
    ) -> Result<(), FixtureError> {
        self.require_p2d_overlay()?;
        let tx = self.db.transaction_with_behavior(TransactionBehavior::Immediate)?;
        chronology::restate_revoked_precedence(
            &tx, id, universe, prior_id, before, after, reason, source_revision_id,
        )?;
        tx.commit()?;
        Ok(())
    }


    /// P2e fixture-only authored correction: append revocation AND new
    /// stage-4 restatement in the same transaction. If either INSERT is
    /// rejected by STRICT scope/cycle/uniqueness guards, rollback both.

    // This exact pair of INSERTs is shared by preview and final confirmation.
    // No separate validation-only implementation is allowed to drift.
    fn stage_atomic_correction(
        db: &Connection, decision_id: &str, restatement_id: &str,
        universe: &str, prior_id: &str, before: &str, after: &str,
        reason: &str, source_revision_id: Option<&str>,
    ) -> Result<(), FixtureError> {
        chronology::decide_precedence(
            db, decision_id, universe, prior_id,
            "revoke", None, reason, source_revision_id,
        )?;
        chronology::restate_revoked_precedence(
            db, restatement_id, universe, prior_id,
            before, after, reason, source_revision_id,
        )?;
        Ok(())
    }

    /// P2e final action: one transaction, BOTH records commit or both rollback.
    pub fn correct_precedence_atomically(
        &mut self, decision_id: &str, restatement_id: &str,
        universe: &str, prior_id: &str, before: &str, after: &str,
        reason: &str, source_revision_id: Option<&str>,
    ) -> Result<(), FixtureError> {
        self.require_p2d_overlay()?;
        let tx = self.db.transaction_with_behavior(TransactionBehavior::Immediate)?;
        Self::stage_atomic_correction(
            &tx, decision_id, restatement_id, universe,
            prior_id, before, after, reason, source_revision_id,
        )?;
        tx.commit()?;
        Ok(())
    }

    /// P2f test-only speculative preview. Execute the SAME SQL triggers and
    /// explicitly rollback even when all guards pass. The returned value is a
    /// draft description, never a confirmation token or reserved write.
    pub fn preview_atomic_correction(
        &mut self, decision_id: &str, restatement_id: &str,
        universe: &str, prior_id: &str, before: &str, after: &str,
        reason: &str, source_revision_id: Option<&str>,
    ) -> Result<CorrectionPreview, FixtureError> {
        self.require_p2d_overlay()?;
        let tx = self.db.transaction_with_behavior(TransactionBehavior::Immediate)?;
        let active_before = Self::query_active_graph(&tx, universe)?;
        Self::stage_atomic_correction(
            &tx, decision_id, restatement_id, universe,
            prior_id, before, after, reason, source_revision_id,
        )?;
        let active_after = Self::query_active_graph(&tx, universe)?;
        tx.rollback()?; // Never commits any author claim, on success or failure.
        Ok(CorrectionPreview {
            prior_precedence_id: prior_id.to_owned(),
            proposed: chronology::ActivePrecedence {
                id: restatement_id.to_owned(),
                before_anchor_id: before.to_owned(),
                after_anchor_id: after.to_owned(),
                origin: "restatement".to_owned(),
            },
            active_before,
            active_after,
        })
    }

    /// Active partial order is not the historical raw-v7 edge inventory.
    /// This deliberately models only the stage-4 overlay, not later generations.
    fn query_active_graph(
        db: &Connection, universe: &str,
    ) -> Result<Vec<chronology::ActivePrecedence>, FixtureError> {
        let mut stmt = db.prepare(
            "SELECT p.id,p.before_anchor_id,p.after_anchor_id,'original' AS origin
             FROM world_time_precedences p
             WHERE p.universe_id=?1
               AND NOT EXISTS (
                 SELECT 1 FROM world_time_precedence_decisions d
                 WHERE d.prior_precedence_id=p.id AND d.universe_id=p.universe_id
               )
               AND NOT EXISTS (
                 SELECT 1 FROM world_time_anchor_decisions d
                 WHERE d.universe_id=p.universe_id
                   AND d.prior_anchor_id IN (p.before_anchor_id,p.after_anchor_id)
               )
             UNION ALL
             SELECT t.id,t.before_anchor_id,t.after_anchor_id,'restatement' AS origin
             FROM world_time_precedence_restatements t
             WHERE t.universe_id=?1
               AND NOT EXISTS (
                 SELECT 1 FROM world_time_anchor_decisions d
                 WHERE d.universe_id=t.universe_id
                   AND d.prior_anchor_id IN (t.before_anchor_id,t.after_anchor_id)
               )
             ORDER BY id,origin",
        )?;
        let entries = stmt.query_map([universe], |row| {
            Ok(chronology::ActivePrecedence {
                id: row.get(0)?,
                before_anchor_id: row.get(1)?,
                after_anchor_id: row.get(2)?,
                origin: row.get(3)?,
            })
        })?.collect::<rusqlite::Result<Vec<_>>>()?;
        Ok(entries)
    }

    pub fn p2d_active_graph(
        &self, universe: &str,
    ) -> Result<Vec<chronology::ActivePrecedence>, FixtureError> {
        self.require_p2d_overlay()?;
        Self::query_active_graph(self.db, universe)
    }

    pub fn snapshot(&self, universe: &str) -> Result<FixtureSnapshot, FixtureError> {
        Ok(FixtureSnapshot {
            anchors: chronology::list_anchors(&*self.db, universe)?,
            precedences: chronology::list_precedences(&*self.db, universe)?,
            current_anchor_ids: chronology::list_current_anchor_ids(&*self.db, universe)?,
            current_precedence_ids: chronology::list_current_precedence_ids(&*self.db, universe)?,
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    const V7: &str = include_str!("../sql/m3_1_world_time_v7_candidate.sql");
    const DECISIONS: &str = include_str!("../sql/m3_2_chronology_decisions_candidate.sql");

    fn invented_connection() -> Connection {
        // Reuse the existing RAM-only fixture helper: zero new SQLite open sites.
        let mut db = crate::world_time_schema_tests::v6();
        db.execute_batch(
            "INSERT INTO universes(id,name) VALUES('u1','Invented'),('u2','Other');
             INSERT INTO novels(id,universe_id,series_id,title,sort_order)
                 VALUES('n1','u1',NULL,'Invented novel',0);
             INSERT INTO chapters(id,novel_id,title,sort_order)
                 VALUES('c1','n1','Invented chapter',0);
             INSERT INTO scenes(id,chapter_id,title,sort_order)
                 VALUES('s2','c1','Invented scene',0);
             INSERT INTO scene_text_revisions(id,scene_id,revision_number,content)
                 VALUES('r2','s2',1,'Earlier fictional draft'),
                       ('r3','s2',2,'Current fictional draft');
             INSERT INTO scene_revision_heads(scene_id,revision_id) VALUES('s2','r3');"
        ).unwrap();
        let tx = db.transaction().unwrap();
        tx.execute_batch(V7).unwrap();
        tx.execute_batch(DECISIONS).unwrap();
        tx.execute(
            "INSERT INTO schema_migrations(version,name)
             VALUES(7,'007_create_world_time_foundation')", [],
        ).unwrap();
        tx.commit().unwrap();
        assert_eq!(database::current_schema_version(&db).unwrap(), 7);
        db
    }

    fn draft<'a>(id: &'a str, universe: &'a str) -> chronology::AnchorDraft<'a> {
        chronology::AnchorDraft {
            id, universe_id: universe, time_kind: "relative", calendar_id: None,
            event_entity_id: None, source_revision_id: Some("r2"),
            exact_label: None, window_start_text: None, window_end_text: None,
            precision_text: None,
        }
    }

    fn relation<'a>(id: &'a str, before: &'a str, after: &'a str) -> RelationDraft<'a> {
        RelationDraft {
            id, universe_id: "u1", before_anchor_id: before,
            after_anchor_id: after, reason: "Author-declared before/after",
            source_revision_id: Some("r2"),
        }
    }

    #[test]
    fn p2_preopened_fixture_service_preserves_historical_source_and_partial_order() {
        let mut db = invented_connection();
        {
            let mut service = FixtureChronologyService::from_already_opened_disposable_v7(&mut db).unwrap();
            service.create_calendar("cal1", "u1", "Fictional cycles", "No Gregorian conversion").unwrap();
            service.create_anchor_with_optional_relation(draft("a1", "u1"), None).unwrap();
            service.create_anchor_with_optional_relation(
                draft("a2", "u1"), Some(relation("edge12", "a1", "a2")),
            ).unwrap();
            let own = service.snapshot("u1").unwrap();
            assert_eq!(own.current_anchor_ids, vec!["a1", "a2"]);
            assert_eq!(own.precedences.len(), 1);
            assert_eq!(own.precedences[0].before_anchor_id, "a1");
            assert_eq!(own.precedences[0].after_anchor_id, "a2");
            assert!(own.anchors.iter().all(|a| a.source_revision_id.as_deref() == Some("r2")));
            assert!(service.snapshot("u2").unwrap().anchors.is_empty());
        }
        let head: String = db.query_row(
            "SELECT revision_id FROM scene_revision_heads WHERE scene_id='s2'",
            [], |r| r.get(0),
        ).unwrap();
        assert_eq!(head, "r3", "old source r2 cannot replace current head r3");
        assert_eq!(db.query_row("PRAGMA integrity_check", [], |r| r.get::<_, String>(0)).unwrap(), "ok");
    }

    #[test]
    fn p2_preopened_fixture_service_rolls_back_failed_batch_and_refuses_cycle() {
        let mut db = invented_connection();
        let mut service = FixtureChronologyService::from_already_opened_disposable_v7(&mut db).unwrap();
        service.create_anchor_with_optional_relation(draft("a1", "u1"), None).unwrap();
        service.create_anchor_with_optional_relation(
            draft("a2", "u1"), Some(relation("edge12", "a1", "a2")),
        ).unwrap();
        assert!(matches!(
            service.create_anchor_with_optional_relation(
                draft("ghost", "u1"), Some(relation("bad-edge", "missing", "ghost")),
            ),
            Err(FixtureError::Sql(_))
        ));
        assert!(matches!(
            service.create_precedence(relation("cycle", "a2", "a1")),
            Err(FixtureError::Sql(_))
        ));
        assert!(matches!(
            service.create_anchor_with_optional_relation(
                draft("foreign", "u2"), Some(relation("bad-universe", "a1", "foreign")),
            ),
            Err(FixtureError::Stop(_))
        ));
        let snapshot = service.snapshot("u1").unwrap();
        assert_eq!(snapshot.current_anchor_ids, vec!["a1", "a2"]);
        assert_eq!(snapshot.precedences.len(), 1);
        assert!(service.snapshot("u2").unwrap().anchors.is_empty());
    }





    #[test]
    fn p2g_preview_shows_before_after_partial_order_without_persisting() {
        let mut db = invented_connection();
        db.execute_batch(include_str!("../sql/m3_2_active_precedence_candidate.sql")).unwrap();
        {
            let mut service = FixtureChronologyService::from_already_opened_disposable_v7(&mut db).unwrap();
            for id in ["a1","a2","a3"] {
                service.create_anchor_with_optional_relation(draft(id, "u1"), None).unwrap();
            }
            service.create_precedence(relation("old12", "a1", "a2")).unwrap();
            service.create_precedence(relation("edge13", "a1", "a3")).unwrap();
            let comparison = service.preview_atomic_correction(
                "decision12", "new21", "u1", "old12", "a2", "a1",
                "Human review of fictional order", Some("r2"),
            ).unwrap();
            assert_eq!(comparison.active_before.len(), 2);
            assert_eq!(comparison.active_before.iter().map(|e|e.id.as_str()).collect::<Vec<_>>(),
                       vec!["edge13", "old12"]);
            assert_eq!(comparison.active_after.len(), 2);
            assert_eq!(comparison.active_after.iter().map(|e|e.id.as_str()).collect::<Vec<_>>(),
                       vec!["edge13", "new21"]);
            assert_eq!(comparison.proposed.id, "new21");
            assert_eq!(comparison.active_after.iter().find(|e|e.id=="new21").unwrap().origin,
                       "restatement");
            assert_eq!(service.p2d_active_graph("u1").unwrap(), comparison.active_before,
                       "preview is a comparison, never a write");
            assert!(service.p2d_active_graph("u2").unwrap().is_empty());
        }
        let counts: (i64,i64) = (
            db.query_row("SELECT count(*) FROM world_time_precedence_decisions",[],|r|r.get(0)).unwrap(),
            db.query_row("SELECT count(*) FROM world_time_precedence_restatements",[],|r|r.get(0)).unwrap()
        );
        assert_eq!(counts,(0,0));
        assert_eq!(db.query_row("SELECT revision_id FROM scene_revision_heads WHERE scene_id='s2'",[],|r|r.get::<_,String>(0)).unwrap(),"r3");
        assert_eq!(db.query_row("PRAGMA integrity_check",[],|r|r.get::<_,String>(0)).unwrap(),"ok");
    }

    #[test]
    fn p2g_failed_preview_preserves_graph_and_refuses_foreign_universe() {
        let mut db = invented_connection();
        db.execute_batch(include_str!("../sql/m3_2_active_precedence_candidate.sql")).unwrap();
        {
            let mut service = FixtureChronologyService::from_already_opened_disposable_v7(&mut db).unwrap();
            for id in ["a1","a2","a3"] {
                service.create_anchor_with_optional_relation(draft(id,"u1"),None).unwrap();
            }
            service.create_precedence(relation("old12","a1","a2")).unwrap();
            service.create_precedence(relation("edge23","a2","a3")).unwrap();
            let before=service.p2d_active_graph("u1").unwrap();
            assert!(matches!(service.preview_atomic_correction(
                "cycle-decision","cycle-restate","u1","old12",
                "a3","a2","Human proposed cycle",Some("r2"),
            ),Err(FixtureError::Sql(_))));
            assert!(matches!(service.preview_atomic_correction(
                "foreign-decision","foreign-restate","u2","old12",
                "a2","a1","Wrong universe",None,
            ),Err(FixtureError::Sql(_))));
            assert_eq!(service.p2d_active_graph("u1").unwrap(),before);
            assert!(service.p2d_active_graph("u2").unwrap().is_empty());
        }
        let count: i64=db.query_row("SELECT count(*) FROM world_time_precedence_decisions",[],|r|r.get(0)).unwrap();
        assert_eq!(count,0);
    }

    #[test]
    fn p2f_success_preview_is_write_free_and_does_not_authorize_commit() {
        let mut db = invented_connection();
        db.execute_batch(include_str!("../sql/m3_2_active_precedence_candidate.sql")).unwrap();
        {
            let mut service = FixtureChronologyService::from_already_opened_disposable_v7(&mut db).unwrap();
            service.create_anchor_with_optional_relation(draft("a1", "u1"), None).unwrap();
            service.create_anchor_with_optional_relation(draft("a2", "u1"), None).unwrap();
            service.create_precedence(relation("old12", "a1", "a2")).unwrap();
            let preview = service.preview_atomic_correction(
                "decision12", "new21", "u1", "old12", "a2", "a1",
                "Author preview only", Some("r2"),
            ).unwrap();
            assert_eq!(preview.prior_precedence_id, "old12");
            assert_eq!((preview.proposed.id.as_str(),
                        preview.proposed.before_anchor_id.as_str(),
                        preview.proposed.after_anchor_id.as_str(),
                        preview.proposed.origin.as_str()),
                       ("new21", "a2", "a1", "restatement"));
            assert_eq!(service.snapshot("u1").unwrap().current_precedence_ids, vec!["old12"]);
            assert_eq!(service.p2d_active_graph("u1").unwrap().len(), 1);
            assert!(service.p2d_active_graph("u2").unwrap().is_empty());
        }
        let (decisions,restatements): (i64,i64) = (
            db.query_row("SELECT COUNT(*) FROM world_time_precedence_decisions",[],
                         |row| row.get(0)).unwrap(),
            db.query_row("SELECT COUNT(*) FROM world_time_precedence_restatements",[],
                         |row| row.get(0)).unwrap(),
        );
        assert_eq!((decisions,restatements), (0,0), "preview must leave zero writes");
        assert_eq!(db.query_row("SELECT revision_id FROM scene_revision_heads
                                 WHERE scene_id='s2'",[],|row| row.get::<_,String>(0)).unwrap(),"r3");
        {
            let mut service = FixtureChronologyService::from_already_opened_disposable_v7(&mut db).unwrap();
            service.correct_precedence_atomically(
                "decision12", "new21", "u1", "old12", "a2", "a1",
                "Author confirmed separately", Some("r2"),
            ).unwrap();
            assert_eq!(service.p2d_active_graph("u1").unwrap()[0].id,"new21");
        }
        assert_eq!(db.query_row("PRAGMA integrity_check",[],|row|row.get::<_,String>(0)).unwrap(),"ok");
    }

    #[test]
    fn p2f_invalid_preview_rolls_back_and_needs_stage4_overlay() {
        let mut db = invented_connection();
        {
            let mut service = FixtureChronologyService::from_already_opened_disposable_v7(&mut db).unwrap();
            assert!(matches!(service.preview_atomic_correction(
                "missing", "missing-restate", "u1", "old12", "a2", "a1", "No overlay", None,
            ), Err(FixtureError::Stop(_))));
        }
        db.execute_batch(include_str!("../sql/m3_2_active_precedence_candidate.sql")).unwrap();
        {
            let mut service = FixtureChronologyService::from_already_opened_disposable_v7(&mut db).unwrap();
            for id in ["a1","a2","a3"] {
                service.create_anchor_with_optional_relation(draft(id,"u1"),None).unwrap();
            }
            service.create_precedence(relation("old12","a1","a2")).unwrap();
            service.create_precedence(relation("edge23","a2","a3")).unwrap();
            assert!(matches!(service.preview_atomic_correction(
                "bad-cycle","bad32","u1","old12","a3","a2",
                "Would create an active cycle",Some("r2"),
            ),Err(FixtureError::Sql(_))));
            assert!(matches!(service.preview_atomic_correction(
                "bad-foreign","foreign21","u2","old12","a2","a1",
                "Wrong universe",None,
            ),Err(FixtureError::Sql(_))));
            assert!(matches!(service.preview_atomic_correction(
                "bad-source","bad-source21","u1","old12","a2","a1",
                "Wrong source revision",Some("absent-revision"),
            ),Err(FixtureError::Sql(_))));
            assert_eq!(service.snapshot("u1").unwrap().current_precedence_ids,
                       vec!["edge23","old12"]);
        }
        let decisions: i64 = db.query_row("SELECT COUNT(*) FROM world_time_precedence_decisions",
                        [],|row|row.get(0)).unwrap();
        let restatements: i64 = db.query_row("SELECT COUNT(*) FROM world_time_precedence_restatements",
                        [],|row|row.get(0)).unwrap();
        assert_eq!((decisions,restatements),(0,0));
        assert_eq!(db.query_row("PRAGMA integrity_check",[],|row|row.get::<_,String>(0)).unwrap(),"ok");
    }

    #[test]
    fn p2e_atomic_correction_commits_both_assertions_once_with_history() {
        let mut db = invented_connection();
        db.execute_batch(include_str!("../sql/m3_2_active_precedence_candidate.sql")).unwrap();
        {
            let mut service = FixtureChronologyService::from_already_opened_disposable_v7(&mut db).unwrap();
            service.create_anchor_with_optional_relation(draft("a1", "u1"), None).unwrap();
            service.create_anchor_with_optional_relation(draft("a2", "u1"), None).unwrap();
            service.create_precedence(relation("old12", "a1", "a2")).unwrap();
            service.correct_precedence_atomically(
                "decision12", "new21", "u1", "old12", "a2", "a1",
                "Writer corrected event ordering", Some("r2"),
            ).unwrap();
            let active = service.p2d_active_graph("u1").unwrap();
            assert_eq!(active.len(), 1);
            assert_eq!((active[0].id.as_str(), active[0].before_anchor_id.as_str(),
                        active[0].after_anchor_id.as_str(), active[0].origin.as_str()),
                       ("new21", "a2", "a1", "restatement"));
            assert_eq!(service.snapshot("u1").unwrap().precedences.len(), 1);
            assert!(service.snapshot("u1").unwrap().current_precedence_ids.is_empty());
            assert!(service.p2d_active_graph("u2").unwrap().is_empty());
        }
        let decision: (String, String, String) = db.query_row(
            "SELECT action,reason,source_revision_id
             FROM world_time_precedence_decisions WHERE id='decision12'",
            [], |row| Ok((row.get(0)?, row.get(1)?, row.get(2)?)),
        ).unwrap();
        assert_eq!(decision, (
            "revoke".into(), "Writer corrected event ordering".into(), "r2".into(),
        ));
        let historic: i64 = db.query_row(
            "SELECT COUNT(*) FROM world_time_precedences WHERE id='old12'",
            [], |row| row.get(0),
        ).unwrap();
        let head: String = db.query_row(
            "SELECT revision_id FROM scene_revision_heads WHERE scene_id='s2'",
            [], |row| row.get(0),
        ).unwrap();
        assert_eq!((historic, head.as_str()), (1, "r3"));
        assert_eq!(db.query_row("PRAGMA integrity_check", [], |row| row.get::<_,String>(0)).unwrap(), "ok");
    }

    #[test]
    fn p2e_atomic_correction_rolls_back_decision_on_cycle_or_wrong_scope() {
        let mut db = invented_connection();
        db.execute_batch(include_str!("../sql/m3_2_active_precedence_candidate.sql")).unwrap();
        {
            let mut service = FixtureChronologyService::from_already_opened_disposable_v7(&mut db).unwrap();
            for id in ["a1", "a2", "a3"] {
                service.create_anchor_with_optional_relation(draft(id, "u1"), None).unwrap();
            }
            service.create_precedence(relation("old12", "a1", "a2")).unwrap();
            service.create_precedence(relation("edge23", "a2", "a3")).unwrap();
            assert!(matches!(service.correct_precedence_atomically(
                "decision-cycle", "bad32", "u1", "old12", "a3", "a2",
                "Would cycle with A2 before A3", Some("r2"),
            ), Err(FixtureError::Sql(_))));
            assert_eq!(service.snapshot("u1").unwrap().current_precedence_ids,
                       vec!["edge23", "old12"]);
            assert_eq!(service.p2d_active_graph("u1").unwrap().len(), 2);
            assert!(matches!(service.correct_precedence_atomically(
                "decision-cross", "bad-cross", "u2", "old12", "a2", "a1",
                "Different invented universe", None,
            ), Err(FixtureError::Sql(_))));
            assert!(matches!(service.correct_precedence_atomically(
                "decision-invalid-source", "bad-source", "u1", "old12",
                "a2", "a1", "Bad historical provenance", Some("r3-bogus"),
            ), Err(FixtureError::Sql(_))));
        }
        let decisions: i64 = db.query_row(
            "SELECT COUNT(*) FROM world_time_precedence_decisions",
            [], |row| row.get(0),
        ).unwrap();
        let restatements: i64 = db.query_row(
            "SELECT COUNT(*) FROM world_time_precedence_restatements",
            [], |row| row.get(0),
        ).unwrap();
        assert_eq!((decisions, restatements), (0, 0), "both inserts rolled back");
        assert_eq!(db.query_row("PRAGMA integrity_check", [], |row| row.get::<_,String>(0)).unwrap(), "ok");
    }

    #[test]
    fn p2d_preopened_stage4_restatement_reverses_only_active_order() {
        let mut db = invented_connection();
        db.execute_batch(include_str!("../sql/m3_2_active_precedence_candidate.sql"))
            .expect("disposable RAM stage-4 overlay only");
        {
            let mut service = FixtureChronologyService::from_already_opened_disposable_v7(&mut db).unwrap();
            for id in ["a1", "a2", "a3"] {
                service.create_anchor_with_optional_relation(draft(id, "u1"), None).unwrap();
            }
            service.create_precedence(relation("old12", "a1", "a2")).unwrap();
            service.revoke_precedence("rev12", "u1", "old12", "Author corrected order", Some("r2")).unwrap();
            assert!(service.p2d_active_graph("u1").unwrap().is_empty());
            service.restate_revoked_precedence(
                "new21", "u1", "old12", "a2", "a1", "Author: B before A", Some("r2"),
            ).unwrap();
            let active = service.p2d_active_graph("u1").unwrap();
            assert_eq!(active.len(), 1);
            assert_eq!((active[0].id.as_str(), active[0].before_anchor_id.as_str(),
                        active[0].after_anchor_id.as_str(), active[0].origin.as_str()),
                       ("new21", "a2", "a1", "restatement"));
            assert_eq!(service.snapshot("u1").unwrap().precedences.len(), 1,
                       "immutable revoked original retained");
            assert!(service.snapshot("u1").unwrap().current_precedence_ids.is_empty());
            assert!(service.p2d_active_graph("u2").unwrap().is_empty());
            assert!(matches!(service.restate_revoked_precedence(
                "duplicate", "u1", "old12", "a2", "a1", "No second restatement", Some("r2"),
            ), Err(FixtureError::Sql(_))));
            assert!(matches!(service.restate_revoked_precedence(
                "foreign", "u2", "old12", "a2", "a1", "Wrong universe", None,
            ), Err(FixtureError::Sql(_))));
            service.create_precedence(relation("ac", "a1", "a3")).unwrap();
            assert!(matches!(service.create_precedence(relation("cb", "a3", "a2")),
                             Err(FixtureError::Sql(_))),
                    "new raw edge must not form cycle via active B->A->C graph");
            assert_eq!(service.p2d_active_graph("u1").unwrap().len(), 2);
        }
        let intact: i64 = db.query_row(
            "SELECT COUNT(*) FROM world_time_precedences WHERE id='old12'",
            [], |row| row.get(0),
        ).unwrap();
        let restatements: i64 = db.query_row(
            "SELECT COUNT(*) FROM world_time_precedence_restatements WHERE universe_id='u1'",
            [], |row| row.get(0),
        ).unwrap();
        let head: String = db.query_row(
            "SELECT revision_id FROM scene_revision_heads WHERE scene_id='s2'",
            [], |row| row.get(0),
        ).unwrap();
        assert_eq!((intact, restatements, head.as_str()), (1, 1, "r3"));
        assert_eq!(db.query_row("PRAGMA integrity_check", [], |row| row.get::<_, String>(0)).unwrap(), "ok");
    }

    #[test]
    fn p2d_restatement_requires_independent_stage4_overlay() {
        let mut db = invented_connection();
        let mut service = FixtureChronologyService::from_already_opened_disposable_v7(&mut db).unwrap();
        assert!(matches!(service.restate_revoked_precedence(
            "no-overlay", "u1", "missing", "a", "b", "refused", None,
        ), Err(FixtureError::Stop(_))));
        assert!(matches!(service.p2d_active_graph("u1"), Err(FixtureError::Stop(_))));
    }

    #[test]
    fn p2c_preopened_fixture_revoke_is_append_only_scoped_and_idempotently_refused() {
        let mut db = invented_connection();
        {
            let mut service = FixtureChronologyService::from_already_opened_disposable_v7(&mut db).unwrap();
            service.create_anchor_with_optional_relation(draft("a1","u1"), None).unwrap();
            service.create_anchor_with_optional_relation(
                draft("a2","u1"), Some(relation("edge12","a1","a2")),
            ).unwrap();
            assert_eq!(service.snapshot("u1").unwrap().current_precedence_ids, vec!["edge12"]);
            service.revoke_precedence(
                "rev-edge12", "u1", "edge12", "Author withdrew this order", Some("r2"),
            ).unwrap();
            let after = service.snapshot("u1").unwrap();
            assert_eq!(after.current_precedence_ids, Vec::<String>::new());
            assert_eq!(after.precedences.len(), 1, "original immutable relation retained");
            assert_eq!(after.current_anchor_ids, vec!["a1","a2"]);
            assert!(matches!(
                service.revoke_precedence("rev-again","u1","edge12","duplicate",Some("r2")),
                Err(FixtureError::Sql(_)),
            ));
            assert!(matches!(
                service.revoke_precedence("foreign","u2","edge12","foreign",None),
                Err(FixtureError::Sql(_)),
            ));
            assert!(matches!(
                service.revoke_precedence("missing","u1","absent","missing",None),
                Err(FixtureError::Sql(_)),
            ));
            assert!(service.snapshot("u2").unwrap().precedences.is_empty());
        }
        let (action, reason, source): (String,String,Option<String>) = db.query_row(
            "SELECT action,reason,source_revision_id
             FROM world_time_precedence_decisions WHERE id='rev-edge12'",
            [], |row| Ok((row.get(0)?,row.get(1)?,row.get(2)?)),
        ).unwrap();
        assert_eq!(action, "revoke");
        assert_eq!(reason, "Author withdrew this order");
        assert_eq!(source.as_deref(), Some("r2"));
        let historic: i64 = db.query_row(
            "SELECT COUNT(*) FROM world_time_precedences WHERE id='edge12'",
            [], |row| row.get(0),
        ).unwrap();
        assert_eq!(historic, 1);
        assert_eq!(db.query_row("PRAGMA integrity_check", [], |row| row.get::<_,String>(0)).unwrap(), "ok");
    }

    #[test]
    fn p2_preopened_fixture_service_refuses_unqualified_connections() {
        // Existing test-only v6 helper, without an extra SQLite opening site.
        let mut v6 = crate::world_time_schema_tests::v6();
        assert!(matches!(
            FixtureChronologyService::from_already_opened_disposable_v7(&mut v6),
            Err(FixtureError::Stop(_))
        ));
        let mut db = invented_connection();
        db.pragma_update(None, "query_only", true).unwrap();
        assert!(matches!(
            FixtureChronologyService::from_already_opened_disposable_v7(&mut db),
            Err(FixtureError::Stop(_))
        ));
        db.pragma_update(None, "query_only", false).unwrap();
        db.pragma_update(None, "foreign_keys", false).unwrap();
        assert!(matches!(
            FixtureChronologyService::from_already_opened_disposable_v7(&mut db),
            Err(FixtureError::Stop(_))
        ));
        db.pragma_update(None, "foreign_keys", true).unwrap();
        db.execute_batch("ATTACH DATABASE ':memory:' AS foreign_store").unwrap();
        assert!(matches!(
            FixtureChronologyService::from_already_opened_disposable_v7(&mut db),
            Err(FixtureError::Stop(_))
        ));
    }
}
