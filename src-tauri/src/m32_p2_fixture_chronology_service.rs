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

pub(crate) struct FixtureSnapshot {
    pub anchors: Vec<chronology::ManualAnchor>,
    pub precedences: Vec<chronology::ManualPrecedence>,
    pub current_anchor_ids: Vec<String>,
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

    pub fn snapshot(&self, universe: &str) -> Result<FixtureSnapshot, FixtureError> {
        Ok(FixtureSnapshot {
            anchors: chronology::list_anchors(&*self.db, universe)?,
            precedences: chronology::list_precedences(&*self.db, universe)?,
            current_anchor_ids: chronology::list_current_anchor_ids(&*self.db, universe)?,
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
