fn main() {
    // Tauri defaults to permitting all registered application commands.
    // This separate BUILD-TIME allowlist closes that default for M3.2's
    // debug-only gate; frontend window capabilities alone are not sufficient.
    if std::env::var_os("CARGO_FEATURE_M32_ISOLATED_PREFLIGHT").is_some() {
        tauri_build::try_build(
            tauri_build::Attributes::new().app_manifest(
                tauri_build::AppManifest::new()
                    .commands(&["m32_isolated_preflight_status"]),
            ),
        )
        .expect("M3.2 preflight application IPC manifest must compile");
    } else {
        tauri_build::build();
    }
}
