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
    assert_eq!(current.revisions[0].content, "Ariane traverse la porte.");
    assert_eq!(current.revisions[1].content, "Une porte.");
    assert_eq!(hierarchy::snapshot(&reopened).unwrap().novels.len(), 1);
    assert_eq!(review::state(&reopened, "fact-new", "u-new").unwrap().status, "canon");
    drop(reopened);

    // The Greenfield UI archives visibility preferences, not revision texts.
    // Prove these preferences survive the actual v6 file backup and restore.
    {
        let mut db = database::open_database(&source_db).unwrap();
        assert_eq!(
            revisions::set_scene_revision_archived(
                &mut db,
                revisions::SetSceneRevisionArchivedInput {
                    scene_id: "scene-new".into(),
                    revision_id: "rev-1".into(),
                    archived: true,
                },
            ).unwrap(),
            vec!["rev-1"]
        );
        assert_eq!(database::current_schema_version(&db).unwrap(), 6);
    }

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
    let restored_history = revisions::scene_revision_history(&isolated, "scene-new").unwrap();
    assert_eq!(restored_history.revisions.len(), 2);
    assert_eq!(restored_history.current_revision_id.as_deref(), Some("rev-2"));
    assert_eq!(restored_history.revisions[0].content, "Ariane traverse la porte.");
    assert_eq!(restored_history.revisions[1].content, "Une porte.");
    assert_eq!(revisions::scene_archived_revision_ids(&isolated, "scene-new").unwrap(), vec!["rev-1"]);
    assert_eq!(database::current_schema_version(&isolated).unwrap(), 6);
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

#[test]
fn greenfield_ci_corrupt_backup_cannot_activate_a_fresh_restore_root() {
    let source = new_ci_only_root("corrupt-source");
    let destination = new_ci_only_root("corrupt-destination");
    let source_db = backup::resolve_active_database_path(&source).unwrap();
    {
        let mut db = database::open_database(&source_db).unwrap();
        hierarchy::create_universe(
            &mut db,
            hierarchy::CreateUniverseInput { id: "u-corrupt".into(), name: "Fiction".into() },
        ).unwrap();
    }
    let saved = backup::create_backup(&source).unwrap();
    let source_before = fs::read(&source_db).unwrap();
    let backup_before = fs::read(&saved.backup.path).unwrap();

    fs::create_dir(destination.join("backups")).unwrap();
    let copied = destination.join("backups").join(&saved.backup.file_name);
    fs::write(&copied, b"not a SQLite database - runner fixture only").unwrap();
    assert!(backup::restore_backup(&destination, &saved.backup.file_name).is_err());
    assert!(!destination.join("database").exists());
    assert_eq!(backup::resolve_active_database_path(&destination).unwrap(),
               destination.join("database").join(database::DATABASE_FILENAME));
    assert_eq!(fs::read(&copied).unwrap(), b"not a SQLite database - runner fixture only");
    assert_eq!(fs::read(&source_db).unwrap(), source_before);
    assert_eq!(fs::read(&saved.backup.path).unwrap(), backup_before);

    fs::remove_dir_all(destination).unwrap();
    fs::remove_dir_all(source).unwrap();
}

#[test]
fn greenfield_ci_occupied_restore_root_switches_selection_so_operator_use_is_blocked() {
    // Negative qualification evidence: the existing M1.5 restore API does NOT
    // require an empty root. It preserves bytes, but switches the active marker.
    // Never use it as an operator Greenfield restore procedure without a new guard.
    let source = new_ci_only_root("occupied-source");
    let destination = new_ci_only_root("occupied-destination");
    let source_db = backup::resolve_active_database_path(&source).unwrap();
    let old_destination_db = backup::resolve_active_database_path(&destination).unwrap();
    {
        let mut db = database::open_database(&source_db).unwrap();
        hierarchy::create_universe(
            &mut db,
            hierarchy::CreateUniverseInput { id: "imported".into(), name: "Import".into() },
        ).unwrap();
    }
    {
        let mut db = database::open_database(&old_destination_db).unwrap();
        hierarchy::create_universe(
            &mut db,
            hierarchy::CreateUniverseInput { id: "existing".into(), name: "Existing".into() },
        ).unwrap();
    }
    let existing_bytes = fs::read(&old_destination_db).unwrap();
    let saved = backup::create_backup(&source).unwrap();
    let backup_bytes = fs::read(&saved.backup.path).unwrap();
    fs::create_dir(destination.join("backups")).unwrap();
    let copied = destination.join("backups").join(&saved.backup.file_name);
    fs::copy(&saved.backup.path, &copied).unwrap();

    let result = backup::restore_backup(&destination, &saved.backup.file_name).unwrap();
    assert_eq!(result.previous_database_path, old_destination_db.to_string_lossy());
    assert_ne!(result.active_database_path, result.previous_database_path);
    assert_eq!(backup::resolve_active_database_path(&destination).unwrap(),
               PathBuf::from(&result.active_database_path));
    assert_eq!(fs::read(&old_destination_db).unwrap(), existing_bytes);
    assert_eq!(fs::read(&copied).unwrap(), backup_bytes);
    assert_eq!(fs::read(&saved.backup.path).unwrap(), backup_bytes);
    let new_active = database::open_database(&PathBuf::from(&result.active_database_path)).unwrap();
    let snapshot = hierarchy::snapshot(&new_active).unwrap();
    assert_eq!(snapshot.universes.len(), 1);
    assert_eq!(snapshot.universes[0].id, "imported");
    drop(new_active);

    fs::remove_dir_all(destination).unwrap();
    fs::remove_dir_all(source).unwrap();
}
