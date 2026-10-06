use serde::Serialize;

#[derive(Serialize)]
struct BootstrapStatus {
    app_name: &'static str,
    milestone: &'static str,
    rust_bridge: &'static str,
}

#[tauri::command]
fn bootstrap_status() -> BootstrapStatus {
    BootstrapStatus {
        app_name: "Fabulaxiom",
        milestone: "M0 desktop skeleton",
        rust_bridge: "React -> Tauri -> Rust operational",
    }
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![bootstrap_status])
        .run(tauri::generate_context!())
        .expect("error while running Fabulaxiom");
}
