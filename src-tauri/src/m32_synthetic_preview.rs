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
        // The actual TAURI_CONFIG contains a RAW RFC7396 override.
        // Its nulls must survive until Tauri merges it against base config.
        // Tauri codegen itself always writes None for hooks regardless of
        // source; never claim that inspecting codegen hooks proves safety.
        let supplied = std::env::var("TAURI_CONFIG")
            .expect("only synthetic CI may provide the raw fictional overlay");
        let patch: serde_json::Value = serde_json::from_str(&supplied)
            .expect("valid RFC7396 overlay JSON");
        for key in ["beforeDevCommand", "beforeBuildCommand", "frontendDist"] {
            assert!(patch["build"][key].is_null(), "RFC7396 deletion marker missing for {key}");
        }
        assert_eq!(patch["identifier"], LAB_ID);
        // frontend_dist survives codegen as Option, unlike command hooks.
        // This tests the Tauri codegen merge, NOT the CLI --config command.
        assert!(config.build.frontend_dist.is_none(), "production dist inherited by Tauri context");
        let caps = serde_json::to_value(&config.app.security.capabilities)
            .expect("serialize the compile-time capability references");
        assert_eq!(caps, serde_json::json!(["default"]));
        // A capability reference alone is not a native ACL grant. The separate
        // source-only audit checks default.json targets only window "main".
    }

    /// Tests a TOOLS-ONLY static candidate, not the active launch overlay.
    /// Generated context is compiled but NO Builder or native window is started.
    #[test]
    #[ignore = "CI-only candidate config; deliberately forbidden by current launcher"]
    fn compiled_static_candidate_csp_no_runtime() {
        let context: tauri::Context = tauri::generate_context!(test = true);
        let config = context.config();
        let candidate_url = "http://127.0.0.1:14279/m32-browser-lab.html";
        let actual_url = config.build.dev_url.as_ref().map(|u| u.as_str());
        assert_eq!(actual_url, Some(candidate_url));
        assert_eq!(config.identifier, LAB_ID);
        assert_eq!(config.app.windows.len(), 1);
        assert_eq!(config.app.windows[0].label, LAB_WINDOW);
        assert!(!config.bundle.active);
        assert!(config.build.frontend_dist.is_none());
        let supplied = std::env::var("TAURI_CONFIG")
            .expect("CI must provide only raw inert candidate JSON");
        let patch: serde_json::Value = serde_json::from_str(&supplied)
            .expect("candidate must be valid JSON");
        assert_eq!(patch["build"]["devUrl"], candidate_url);
        for key in ["beforeDevCommand", "beforeBuildCommand", "frontendDist"] {
            assert!(patch["build"][key].is_null());
        }
        let expected_csp = patch["app"]["security"]["devCsp"]
            .as_str().expect("string CSP candidate required");
        assert!(!expected_csp.contains("unsafe-inline"));
        assert!(!expected_csp.contains("unsafe-eval"));
        assert!(expected_csp.contains("connect-src 'none'"));
        let parsed = serde_json::to_value(
            config.app.security.dev_csp.as_ref().expect("native devCsp missing")
        ).expect("serialize native devCsp for comparison");
        assert_eq!(parsed, serde_json::json!(expected_csp));
        assert_eq!(
            serde_json::to_value(&config.app.security.capabilities).unwrap(),
            serde_json::json!(["default"])
        );
        // The production runtime admission remains deliberately closed.
        assert!(validate_launch(LAB_ID, LAB_ID, actual_url, &[LAB_WINDOW]).is_err());
    }

    #[test]
    fn lab_constants_explicitly_refuse_real_source_assumptions() {
        assert_ne!(LAB_ID, "com.fabulaxiom.desktop");
        assert!(!LAB_WINDOW.eq("main"));
        assert!(LAB_URL.starts_with("http://127.0.0.1:1420/"));
        assert!(LAB_URL.ends_with("/m32-browser-lab.html"));
    }
}
