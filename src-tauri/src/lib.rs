use std::time::Duration;

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

#[tauri::command]
fn bootstrap_status() -> BootstrapStatus {
    BootstrapStatus {
        app_name: "Fabulaxiom",
        milestone: "M0 desktop skeleton",
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

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![bootstrap_status, ollama_status])
        .run(tauri::generate_context!())
        .expect("error while running Fabulaxiom");
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
