mod backup;
mod backup_commands;
mod database;
#[cfg(feature = "m32-synthetic-preview")]
mod m32_synthetic_preview;
#[cfg(all(feature = "m31-isolated-preview", feature = "m32-synthetic-preview"))]
compile_error!("M3.1 read-only v7 preview and M3.2 fictional preview cannot coexist");
#[cfg(all(feature = "m32-synthetic-preview", not(debug_assertions)))]
compile_error!("M3.2 fictional Tauri preview is DEBUG-ONLY; release builds forbidden");
#[cfg(feature = "m31-isolated-preview")]
mod m31_readonly_preview;
#[cfg(all(feature = "m31-isolated-preview", not(debug_assertions)))]
compile_error!("M3.1 read-only isolated preview is debug-only; do not ship this build flavor");
mod entity;
mod entity_commands;
mod facts;
mod fact_commands;
mod review;
mod review_commands;
mod hierarchy;
mod hierarchy_commands;
mod revision_commands;
mod revisions;

// Route C: generated disposable CI runner files only; never operator storage.
#[cfg(test)]
mod greenfield_smoke_tests;

// PR #35 safe first-stage port: *only* compiled in Rust unit tests; never Tauri IPC.
#[cfg(test)]
mod m32_manual_chronology;

// Offline, in-memory-only M3.1 candidate: never run on operator database.
#[cfg(test)]
mod world_time_schema_tests;
// Candidate only: fail-closed v6 inspection with disposable in-memory fixtures.
#[cfg(test)]
mod world_time_preflight;
// Only disposable closed-file v6->v7 candidate copy rehearsals.
#[cfg(test)]
mod world_time_file_migration_tests;
// M3.2 single-user Windows Hello decision policy rehearsal only. No OS prompt,
// Tauri command, production consent token, SQLite opener or writer is exposed.
#[cfg(test)]
mod m32_sensitive_action_consent_tests;
// M3.2 desktop HWND eligibility rehearsal: plain synthetic values only.
// No WinRT activation, HWND lookup, Tauri command or operator I/O.
#[cfg(test)]
mod m32_desktop_hello_boundary_tests;

// Never compile this feature into a Tauri runtime, even debug builds.
#[cfg(all(feature = "m32-g3-owned-ram-toy", not(test)))]
compile_error!("M3.2 owner-to-RAM backup fixture must be compiled ONLY as Rust unit tests");
#[cfg(all(test, feature = "m32-g3-owned-ram-toy"))]
mod m32_owned_backup_toy;
#[cfg(all(test, feature = "m32-g3-owned-ram-toy"))]
mod m32_owner_lifecycle_toy;
// Pure-RAM thread handoff actor: ownership/teardown only, never source provenance.
#[cfg(all(test, feature = "m32-g3-owned-ram-toy"))]
mod m32_owner_handoff_actor_toy;
// TEST-ONLY: borrowed query-only connection to a completely fictitious RAM DB.
#[cfg(all(test, feature = "m32-g3-owned-ram-toy"))]
mod m32_preopened_query_only_toy;

use std::time::Duration;

use backup_commands::{backup_status, create_database_backup, restore_database_backup};

use fact_commands::{create_narrative_fact, facts_snapshot, fact_source_revision};
use review_commands::{fact_review_snapshot, review_fact_history, review_narrative_fact};
use entity_commands::{
    create_entity_alias, create_narrative_entity, delete_entity_alias,
    delete_narrative_entity, entity_snapshot, rename_entity_alias,
    rename_narrative_entity,
};
use hierarchy_commands::{
    create_chapter, create_novel, create_scene, create_series, create_universe, delete_chapter,
    delete_novel, delete_scene, delete_series, delete_universe, hierarchy_snapshot, rename_chapter,
    rename_novel, rename_scene, rename_series, rename_universe, reorder_chapter, reorder_novel,
    reorder_scene, reorder_series, set_novel_series,
};
use revision_commands::{
    create_scene_text_revision, greenfield_revision_archive_enabled, scene_archived_revision_ids,
    scene_revision_history, set_current_scene_revision, set_scene_revision_archived,
};
use reqwest::{redirect::Policy, Client};
use serde::{Deserialize, Serialize};

const OLLAMA_ENDPOINT: &str = "http://127.0.0.1:11434";
const OLLAMA_VERSION_URL: &str = "http://127.0.0.1:11434/api/version";

#[derive(Serialize)]
struct BootstrapStatus {
    app_name: &'static str,
    milestone: &'static str,
    rust_bridge: &'static str,
}

#[derive(Debug, Deserialize, PartialEq)]
struct OllamaVersionResponse {
    version: String,
}

#[derive(Debug, Serialize, PartialEq)]
struct OllamaStatus {
    available: bool,
    endpoint: &'static str,
    version: Option<String>,
    error: Option<String>,
}

#[derive(Debug, Serialize, PartialEq)]
struct DatabaseStatus {
    available: bool,
    path: Option<String>,
    schema_version: Option<i64>,
    foreign_keys: bool,
    error: Option<String>,
}

#[tauri::command]
fn bootstrap_status() -> BootstrapStatus {
    BootstrapStatus {
        app_name: "Fabulaxiom",
        milestone: "M2.2 no-AI entity and alias CRUD",
        rust_bridge: "React -> Tauri -> Rust operational",
    }
}

async fn read_ollama_status() -> OllamaStatus {
    let client = match Client::builder()
        .no_proxy()
        .redirect(Policy::none())
        .connect_timeout(Duration::from_secs(2))
        .timeout(Duration::from_secs(3))
        .build()
    {
        Ok(client) => client,
        Err(error) => {
            return OllamaStatus {
                available: false,
                endpoint: OLLAMA_ENDPOINT,
                version: None,
                error: Some(format!("impossible de préparer le client HTTP local : {error}")),
            };
        }
    };

    let response = match client.get(OLLAMA_VERSION_URL).send().await {
        Ok(response) => response,
        Err(error) => {
            return OllamaStatus {
                available: false,
                endpoint: OLLAMA_ENDPOINT,
                version: None,
                error: Some(format!("API Ollama locale inaccessible : {error}")),
            };
        }
    };

    let response = match response.error_for_status() {
        Ok(response) => response,
        Err(error) => {
            return OllamaStatus {
                available: false,
                endpoint: OLLAMA_ENDPOINT,
                version: None,
                error: Some(format!("API Ollama locale en erreur : {error}")),
            };
        }
    };

    match response.json::<OllamaVersionResponse>().await {
        Ok(payload) if !payload.version.trim().is_empty() => OllamaStatus {
            available: true,
            endpoint: OLLAMA_ENDPOINT,
            version: Some(payload.version),
            error: None,
        },
        Ok(_) => OllamaStatus {
            available: false,
            endpoint: OLLAMA_ENDPOINT,
            version: None,
            error: Some("réponse Ollama sans version".to_string()),
        },
        Err(error) => OllamaStatus {
            available: false,
            endpoint: OLLAMA_ENDPOINT,
            version: None,
            error: Some(format!("réponse Ollama invalide : {error}")),
        },
    }
}

#[tauri::command]
async fn ollama_status() -> OllamaStatus {
    read_ollama_status().await
}

#[tauri::command]
fn database_status(app: tauri::AppHandle) -> DatabaseStatus {
    let path = match database::database_path(&app) {
        Ok(path) => path,
        Err(error) => {
            return DatabaseStatus {
                available: false,
                path: None,
                schema_version: None,
                foreign_keys: false,
                error: Some(error.to_string()),
            };
        }
    };

    let display_path = path.to_string_lossy().into_owned();

    let connection = match database::open_database(&path) {
        Ok(connection) => connection,
        Err(error) => {
            return DatabaseStatus {
                available: false,
                path: Some(display_path),
                schema_version: None,
                foreign_keys: false,
                error: Some(error.to_string()),
            };
        }
    };

    let schema_version = match database::current_schema_version(&connection) {
        Ok(version) => version,
        Err(error) => {
            return DatabaseStatus {
                available: false,
                path: Some(display_path),
                schema_version: None,
                foreign_keys: false,
                error: Some(error.to_string()),
            };
        }
    };

    let foreign_keys = match database::foreign_keys_enabled(&connection) {
        Ok(enabled) => enabled,
        Err(error) => {
            return DatabaseStatus {
                available: false,
                path: Some(display_path),
                schema_version: Some(schema_version),
                foreign_keys: false,
                error: Some(error.to_string()),
            };
        }
    };

    DatabaseStatus {
        available: schema_version == database::CURRENT_SCHEMA_VERSION && foreign_keys,
        path: Some(display_path),
        schema_version: Some(schema_version),
        foreign_keys,
        error: if schema_version == database::CURRENT_SCHEMA_VERSION && foreign_keys {
            None
        } else {
            Some("qualification SQLite incomplète".to_string())
        },
    }
}

#[cfg(not(any(feature = "m31-isolated-preview", feature = "m32-synthetic-preview")))]
#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            bootstrap_status,
            database_status,
            backup_status,
            create_database_backup,
            restore_database_backup,
            ollama_status,
            hierarchy_snapshot,
            create_universe,
            rename_universe,
            delete_universe,
            create_series,
            rename_series,
            reorder_series,
            delete_series,
            create_novel,
            rename_novel,
            set_novel_series,
            reorder_novel,
            delete_novel,
            create_chapter,
            rename_chapter,
            reorder_chapter,
            delete_chapter,
            create_scene,
            rename_scene,
            reorder_scene,
            delete_scene,
            scene_revision_history,
            create_scene_text_revision,
            set_current_scene_revision,
            greenfield_revision_archive_enabled,
            scene_archived_revision_ids,
            set_scene_revision_archived,
            entity_snapshot,
            create_narrative_entity,
            rename_narrative_entity,
            delete_narrative_entity,
            create_entity_alias,
            rename_entity_alias,
            delete_entity_alias,
            facts_snapshot,
            create_narrative_fact,
            fact_source_revision,
            fact_review_snapshot,
            review_fact_history,
            review_narrative_fact
        ])
        .run(tauri::generate_context!())
        .expect("error while running Fabulaxiom");
}

/// Only one read-only command is registered. All M2 mutation IPC is absent.
#[cfg(all(feature = "m31-isolated-preview", not(feature = "m32-synthetic-preview")))]
#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    let context = tauri::generate_context!();
    let actual_id = context.config().identifier.as_str();
    let expected_id = std::env::var("FABULAXIOM_M31_PREVIEW_ID")
        .expect("M3.1 isolated preview requires explicit operator identity acknowledgement");
    m31_readonly_preview::validate_launch(actual_id, &expected_id)
        .expect("M3.1 preview refuses a production/non-isolated Tauri identity");

    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            m31_readonly_preview::m31_readonly_preview_status
        ])
        .run(context)
        .expect("M3.1 isolated read-only preview failed");
}

/** Distinct DEVELOPMENT-ONLY fictional UI shell.
 * NO invoke_handler, plugins, registered SQLite commands, or fallback to the
 * normal application. The hardcoded lab has NO operator files or paths.
 */
#[cfg(all(feature = "m32-synthetic-preview", not(feature = "m31-isolated-preview")))]
#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    let context = tauri::generate_context!();
    let actual_id = context.config().identifier.as_str();
    let actual_url = context.config().build.dev_url.as_ref().map(|url| url.as_str());
    let windows: Vec<&str> = context.config().app.windows
        .iter().map(|window| window.label.as_str()).collect();
    let explicit_id = std::env::var("FABULAXIOM_M32_PREVIEW_ID")
        .expect("M3.2 fictional preview requires an explicit exact identity opt-in");
    m32_synthetic_preview::validate_launch(actual_id, &explicit_id, actual_url, &windows)
        .expect("M3.2 fictional preview refuses wrong identity, homepage or window");
    // A different startup path from the normal and M3.1 variants. By design
    // this builder has zero app invoke commands, state, or plugins.
    tauri::Builder::default().run(context)
        .expect("M3.2 fictional-only preview shell failed");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn ollama_endpoint_is_fixed_to_ipv4_loopback() {
        let endpoint = reqwest::Url::parse(OLLAMA_ENDPOINT).expect("valid endpoint");

        assert_eq!(endpoint.scheme(), "http");
        assert_eq!(endpoint.host_str(), Some("127.0.0.1"));
        assert_eq!(endpoint.port_or_known_default(), Some(11434));
    }

    #[test]
    fn ollama_version_response_deserializes() {
        let payload: OllamaVersionResponse =
            serde_json::from_str(r#"{"version":"0.40.0"}"#).expect("valid Ollama response");

        assert_eq!(
            payload,
            OllamaVersionResponse {
                version: "0.40.0".to_string()
            }
        );
    }
}
