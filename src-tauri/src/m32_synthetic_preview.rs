//! M3.2 FICTIONAL WEBVIEW experiment: no operator source, no application IPC.
 //! Explicit debug-only Tauri flavor. This is not an M3.1 or real G3 launch.
pub(crate) const LAB_ID: &str = "com.fabulaxiom.m32synthetic.preview";
pub(crate) const LAB_URL: &str = "http://127.0.0.1:1420/m32-browser-lab.html";
pub(crate) const LAB_WINDOW: &str = "m32-fiction";

/// Admission is checked BEFORE constructing the Tauri runtime. Never accept
/// production identity, default localhost homepage, extra windows, or guessed
/// opt-ins. This does not open, verify, create or modify any SQLite source.
pub(crate) fn validate_launch(
    actual_id: &str,
    expected_env_id: &str,
    actual_dev_url: Option<&str>,
    windows: &[&str],
) -> Result<(), &'static str> {
    if actual_id != LAB_ID || expected_env_id != LAB_ID {
        return Err("m32_synthetic_identity_not_authorized");
    }
    if actual_dev_url != Some(LAB_URL) {
        return Err("m32_synthetic_fixture_url_not_authorized");
    }
    if windows != [LAB_WINDOW] {
        return Err("m32_synthetic_window_not_isolated");
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn admits_only_exact_fictional_dev_context() {
        assert_eq!(validate_launch(LAB_ID, LAB_ID, Some(LAB_URL), &[LAB_WINDOW]), Ok(()));
    }
    #[test]
    fn rejects_production_and_legacy_preview_identity() {
        for name in [
            "com.fabulaxiom.desktop", "com.fabulaxiom.m31launchdb8d3278504c448084478a70ccb71cbd",
            "com.fabulaxiom.m32synthetic.preview.extra", "",
        ] {
            assert!(validate_launch(name, LAB_ID, Some(LAB_URL), &[LAB_WINDOW]).is_err());
            assert!(validate_launch(LAB_ID, name, Some(LAB_URL), &[LAB_WINDOW]).is_err());
        }
    }
    #[test]
    fn refuses_default_homepage_external_url_and_missing_url() {
        for url in [
            None, Some("http://localhost:1420"), Some("http://127.0.0.1:1420/"),
            Some("http://127.0.0.1:1420/index.html"),
            Some("https://example.com/m32-browser-lab.html"),
            Some("http://127.0.0.1:11434/m32-browser-lab.html"),
        ] {
            assert!(validate_launch(LAB_ID, LAB_ID, url, &[LAB_WINDOW]).is_err());
        }
    }
    #[test]
    fn rejects_main_and_extra_windows() {
        for windows in [
            &[][..], &["main"][..], &["m32-fiction", "main"][..],
            &["m32-fiction", "m32-fiction"][..],
        ] {
            assert!(validate_launch(LAB_ID, LAB_ID, Some(LAB_URL), windows).is_err());
        }
    }
    /// Compiles the real Tauri context but never calls Builder::run/build.
    /// Intentionally ignored during normal Rust suites: the dedicated Windows
    /// CI command provides TAURI_CONFIG and an explicit fictional identity.
    /// This tests codegen against its *provided* merged config, not CLI merging
    /// and not Windows WebView2 runtime permission enforcement.
    #[test]
    #[ignore = "run only in isolated CI with explicit fictional TAURI_CONFIG"]
    fn compiled_fictional_context_no_runtime() {
        let context: tauri::Context = tauri::generate_context!(test = true);
        let config = context.config();
        let windows: Vec<&str> = config.app.windows.iter().map(|w| w.label.as_str()).collect();
        let actual_url = config.build.dev_url.as_ref().map(|u| u.as_str());
        let opt_in = std::env::var("FABULAXIOM_M32_PREVIEW_ID")
            .expect("CI must set only fictional preview identity");
        assert_eq!(validate_launch(&config.identifier, &opt_in, actual_url, &windows), Ok(()));
        assert_eq!(config.app.windows.len(), 1);
        assert!(!config.bundle.active);
        let caps = serde_json::to_value(&config.app.security.capabilities)
            .expect("serialize the compile-time capability references");
        assert_eq!(caps, serde_json::json!(["default"]));
        // A capability reference alone is not a native ACL grant. The separate
        // source-only audit checks default.json targets only window "main".
    }

    #[test]
    fn lab_constants_explicitly_refuse_real_source_assumptions() {
        assert_ne!(LAB_ID, "com.fabulaxiom.desktop");
        assert!(!LAB_WINDOW.eq("main"));
        assert!(LAB_URL.starts_with("http://127.0.0.1:1420/"));
        assert!(LAB_URL.ends_with("/m32-browser-lab.html"));
    }
}
