//! Route C smoke: real M1/M2 services on freshly generated CI-only SQLite files.
//! Compiled exclusively by #[cfg(test)] in lib.rs. Never starts Tauri, uses an
//! operator profile, or accesses historical databases / Windows user locations.

use crate::{backup, database, entity, facts, hierarchy, review, revisions};
use std::{
    fs,
    path::PathBuf,
    time::{SystemTime, UNIX_EPOCH},
};

fn new_ci_only_root(label: &str) -> PathBuf {
    let nonce = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .expect("runner clock")
        .as_nanos();
    let root = std::env::temp_dir().join(format!(
        "fabulaxiom-ci-greenfield-{label}-{}-{nonce}",
        std::process::id()
    ));
    // Never silently reuse a prior directory (including one created by a user).
    fs::create_dir(&root).expect("exclusive fresh CI-only root");
    root
}

#[test]
fn greenfield_ci_m1_m2_lifecycle_and_separate_destination_restore() {
    let source = new_ci_only_root("new-authoring");
    let restored_root = new_ci_only_root("new-restore");
    let source_db = backup::resolve_active_database_path(&source).expect("fresh default path");
    assert_eq!(source_db, source.join("database").join(database::DATABASE_FILENAME));
    assert!(!source_db.exists(), "first launch must start from a missing file");
    assert!(!restored_root.join("database").exists(), "restore must start in another new root");

    {
        // Only the runner-created fixture is allowed to be created/migrated.
        let mut db = database::open_database(&source_db).expect("create greenfield v6");
        assert_eq!(database::current_schema_version(&db).unwrap(), 6);
        hierarchy::create_universe(
            &mut db,
            hierarchy::CreateUniverseInput { id: "u-new".into(), name: "Mon univers".into() },
        ).unwrap();
        hierarchy::create_series(
            &mut db,
            hierarchy::CreateSeriesInput { id: "series-new".into(), universe_id: "u-new".into(), name: "Saga".into() },
        ).unwrap();
        hierarchy::create_novel(
            &mut db,
            hierarchy::CreateNovelInput {
                id: "novel-new".into(), universe_id: "u-new".into(),
                series_id: Some("series-new".into()), title: "Premier roman".into(),
            },
        ).unwrap();
        hierarchy::create_chapter(
            &mut db,
            hierarchy::CreateChapterInput { id: "chapter-new".into(), novel_id: "novel-new".into(), title: "Ouverture".into() },
        ).unwrap();
        hierarchy::create_scene(
            &mut db,
            hierarchy::CreateSceneInput { id: "scene-new".into(), chapter_id: "chapter-new".into(), title: "Départ".into() },
        ).unwrap();

        let first = revisions::create_scene_revision(
            &mut db,
            revisions::CreateSceneRevisionInput { id: "rev-1".into(), scene_id: "scene-new".into(), content: "Une porte.".into() },
        ).unwrap();
        let second = revisions::create_scene_revision(
            &mut db,
            revisions::CreateSceneRevisionInput {
                id: "rev-2".into(), scene_id: "scene-new".into(),
                content: "Ariane traverse la porte.".into(),
            },
        ).unwrap();
        assert_eq!((first.revision_number, second.revision_number), (1, 2));
        assert_eq!(second.parent_revision_id.as_deref(), Some("rev-1"));

        entity::create_entity(
            &mut db,
            entity::CreateEntityInput {
                id: "entity-new".into(), universe_id: "u-new".into(),
                kind: "character".into(), name: "Ariane".into(),
            },
        ).unwrap();
        let fact = facts::create_fact(
            &mut db,
            facts::CreateFactInput {
                id: "fact-new".into(), entity_id: "entity-new".into(),
                fact_key: "action".into(), fact_value: "traverse la porte".into(),
                provenance_kind: "sourced".into(), validity_kind: None, validity_text: None,
                source: Some(facts::CreateFactSourceInput {
                    id: "source-new".into(), revision_id: "rev-2".into(),
                    start_byte: 0, end_byte: 6, quoted_text: "Ariane".into(),
                }),
            },
        ).unwrap();
        assert_eq!(fact.source.unwrap().revision_id, "rev-2");
        let history = review::review(
            &mut db,
            review::ReviewFactInput {
                id: "review-new".into(), fact_id: "fact-new".into(), universe_id: "u-new".into(),
                expected_revision: 0, next_status: "canon".into(),
                action_kind: "approve_canon".into(), reviewer_label: "CI-fictif".into(),
                reason: "Acceptation fictive de test".into(),
                confirmation_phrase: Some("APPROVE_CANON".into()),
            },
        ).unwrap();
        assert_eq!(history.state.status, "canon");
        assert_eq!(history.events.len(), 1);
    }

    // Simulate a closed application and a new connection to the actual runner file.
    let reopened = database::open_database(&source_db).expect("reopen greenfield after exit");
    assert_eq!(database::current_schema_version(&reopened).unwrap(), 6);
    let current = revisions::scene_revision_history(&reopened, "scene-new").unwrap();
    assert_eq!(current.current_revision_id.as_deref(), Some("rev-2"));
    assert_eq!(current.revisions.len(), 2);
    assert_eq!(hierarchy::snapshot(&reopened).unwrap().novels.len(), 1);
    assert_eq!(review::state(&reopened, "fact-new", "u-new").unwrap().status, "canon");
    drop(reopened);

    let saved = backup::create_backup(&source).expect("create new-data-only backup");
    assert_eq!(saved.schema_version, 6);
    assert_eq!(saved.counts.universes, 1);
    assert_eq!(saved.counts.series, 1);
    assert_eq!(saved.counts.novels, 1);
    assert_eq!(saved.counts.chapters, 1);
    assert_eq!(saved.counts.scenes, 1);
    assert_eq!(saved.counts.revisions, 2);
    assert_eq!(saved.counts.current_heads, 1);
    assert_eq!(saved.counts.entities, 1);
    assert_eq!(saved.counts.facts, 1);
    assert_eq!(saved.counts.fact_sources, 1);
    assert_eq!(saved.counts.review_events, 1);

    let source_bytes_before_restore = fs::read(&source_db).expect("source bytes");
    let backup_bytes = fs::read(&saved.backup.path).expect("backup bytes");
    fs::create_dir(restored_root.join("backups")).expect("new restore inbox");
    let destination_backup = restored_root.join("backups").join(&saved.backup.file_name);
    assert!(!destination_backup.exists());
    fs::copy(&saved.backup.path, &destination_backup).expect("copy new fixture backup only");
    let restored = backup::restore_backup(&restored_root, &saved.backup.file_name)
        .expect("restore into separate fresh CI-only destination");

    assert_eq!(restored.counts, saved.counts);
    assert_ne!(restored.active_database_path, saved.backup.path);
    assert!(!restored_root.join("database").join(database::DATABASE_FILENAME).exists());
    assert_eq!(
        backup::resolve_active_database_path(&restored_root).unwrap(),
        PathBuf::from(restored.active_database_path.as_str())
    );
    let isolated = database::open_database(&PathBuf::from(restored.active_database_path.as_str()))
        .expect("open activated copy under fresh destination");
    assert_eq!(revisions::scene_revision_history(&isolated, "scene-new").unwrap().revisions.len(), 2);
    assert_eq!(review::state(&isolated, "fact-new", "u-new").unwrap().status, "canon");
    drop(isolated);

    assert_eq!(fs::read(&source_db).unwrap(), source_bytes_before_restore);
    assert_eq!(fs::read(&saved.backup.path).unwrap(), backup_bytes);
    assert_eq!(fs::read(&destination_backup).unwrap(), backup_bytes);
    assert_eq!(backup::resolve_active_database_path(&source).unwrap(), source_db);

    // These exact two roots were created exclusively by this test invocation.
    fs::remove_dir_all(&restored_root).expect("remove only owned restore fixture");
    fs::remove_dir_all(&source).expect("remove only owned authoring fixture");
}
