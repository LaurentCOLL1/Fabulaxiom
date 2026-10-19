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

    // Test-only synthetic resolved command, NOT generated application ACL.
    // Uses Tauri's own native RuntimeAuthority::resolve_access matcher with
    // deliberately invented permissions, no Builder, WebView or operator files.
    fn native_acl_fixture(windows: &[&str], webviews: &[&str]) -> tauri::ipc::RuntimeAuthority {
        use tauri::utils::acl::{resolved::{Resolved, ResolvedCommand}, ExecutionContext};
        let command = ResolvedCommand {
            context: ExecutionContext::Local,
            windows: windows.iter().map(|pattern| pattern.parse().expect("valid toy window glob")).collect(),
            webviews: webviews.iter().map(|pattern| pattern.parse().expect("valid toy webview glob")).collect(),
            ..Default::default()
        };
        let mut resolved = Resolved::default();
        resolved.allowed_commands.insert("plugin:app|version".into(), vec![command]);
        // A Rust unit-test constructor. NOT Tauri's generated or live authority.
        tauri::ipc::RuntimeAuthority::new(Default::default(), resolved)
    }

    #[test]
    fn native_acl_source_selected_main_does_not_match_fictional_window() {
        use tauri::ipc::Origin;
        // Exact public repository capability file. The command remains TOY.
        let capability: serde_json::Value =
            serde_json::from_str(include_str!("../capabilities/default.json"))
                .expect("source capability JSON");
        assert_eq!(capability["identifier"], "default");
        assert_eq!(capability["permissions"], serde_json::json!(["core:default"]));
        assert_eq!(capability["windows"], serde_json::json!(["main"]));
        assert!(capability.get("webviews").is_none());
        let only_window = capability["windows"][0].as_str().expect("main label");
        let authority = native_acl_fixture(&[only_window], &[]);
        assert!(authority.resolve_access("plugin:app|version", "main", "main", &Origin::Local).is_some());
        assert!(authority.resolve_access("plugin:app|version", LAB_WINDOW, LAB_WINDOW, &Origin::Local).is_none());
        assert!(authority.resolve_access("plugin:app|version", "other", "other", &Origin::Local).is_none());
        println!("M32_NATIVE_ACL_TOY_MAIN_WINDOW_VETO_PASS: actual source selector + synthetic native matcher; no runtime");
    }

    #[test]
    fn native_acl_glob_mutations_reveal_possible_fictional_window_access() {
        use tauri::ipc::Origin;
        for selector in ["m32-fiction", "m32-*", "*"] {
            let authority = native_acl_fixture(&[selector], &[]);
            assert!(authority.resolve_access("plugin:app|version", LAB_WINDOW, "arbitrary-webview", &Origin::Local).is_some(),
                "native matcher must detect unsafe toy selector {selector}");
        }
        let exact = native_acl_fixture(&["main"], &[]);
        assert!(exact.resolve_access("plugin:app|version", LAB_WINDOW, "main", &Origin::Local).is_none());
    }

    #[test]
    fn native_acl_webview_match_can_grant_when_window_does_not_match() {
        use tauri::ipc::Origin;
        let authority = native_acl_fixture(&["main"], &[LAB_WINDOW]);
        assert!(authority.resolve_access("plugin:app|version", "unrelated", LAB_WINDOW, &Origin::Local).is_some());
        assert!(authority.resolve_access("plugin:app|version", "unrelated", "unrelated", &Origin::Local).is_none());
        let empty = native_acl_fixture(&[], &[]);
        assert!(empty.resolve_access("plugin:app|version", LAB_WINDOW, LAB_WINDOW, &Origin::Local).is_none());
    }

    #[test]
    fn native_acl_unknown_command_is_not_granted_by_fictional_matcher() {
        use tauri::ipc::Origin;
        let authority = native_acl_fixture(&["*"], &[]);
        assert!(authority.resolve_access("plugin:app|version", LAB_WINDOW, LAB_WINDOW, &Origin::Local).is_some());
        assert!(authority.resolve_access("plugin:fs|read_file", LAB_WINDOW, LAB_WINDOW, &Origin::Local).is_none());
    }


    // Real Tauri capability->manifest resolution, but only on an INVENTED
    // permission/manifest. It is not the actual generated core:default ACL.
    // No App, Context access, process, WebView or SQLite is created.
    fn native_resolution_manifest(deny: bool) -> std::collections::BTreeMap<
        String, tauri::utils::acl::manifest::Manifest
    > {
        use tauri::utils::acl::{manifest::Manifest, Permission};
        let allow: Permission = serde_json::from_value(serde_json::json!({
            "identifier": "allow-consult",
            "commands": { "allow": ["consult"] }
        })).expect("valid fabricated test permission");
        let mut manifest = Manifest::default();
        manifest.permissions.insert("allow-consult".into(), allow);
        if deny {
            let denied: Permission = serde_json::from_value(serde_json::json!({
                "identifier": "deny-consult",
                "commands": { "deny": ["consult"] }
            })).expect("valid fabricated deny permission");
            manifest.permissions.insert("deny-consult".into(), denied);
        }
        [("m32fixture".into(), manifest)].into()
    }

    fn native_resolution_source_capability() -> serde_json::Value {
        let mut cap: serde_json::Value = serde_json::from_str(
            include_str!("../capabilities/default.json")
        ).expect("checked-in public default capability");
        assert_eq!(cap["identifier"], "default");
        assert_eq!(cap["windows"], serde_json::json!(["main"]));
        assert_eq!(cap["permissions"], serde_json::json!(["core:default"]));
        assert!(cap.get("remote").is_none());
        assert!(cap.get("webviews").is_none());
        // Replace only the TEST INPUT permission, NOT the real capability file.
        cap["permissions"] = serde_json::json!(["m32fixture:allow-consult"]);
        cap
    }

    fn native_resolution_run(
        toy_capabilities: Vec<serde_json::Value>,
        include_manifest: bool,
        deny: bool,
    ) -> Result<tauri::utils::acl::resolved::Resolved, tauri::utils::acl::Error> {
        use tauri::utils::acl::{capability::Capability, resolved::Resolved};
        let caps: std::collections::BTreeMap<String, Capability> =
            toy_capabilities.into_iter().map(|data| {
                let c: Capability = serde_json::from_value(data)
                    .expect("valid invented Tauri capability");
                (c.identifier.clone(), c)
            }).collect();
        let manifests = if include_manifest {
            native_resolution_manifest(deny)
        } else {
            Default::default()
        };
        Resolved::resolve(&manifests, caps, tauri::utils::platform::Target::current())
    }

    #[test]
    fn native_resolve_source_main_to_fictional_manifest_and_denies_lab() {
        use tauri::ipc::{Origin, RuntimeAuthority};
        let resolved = native_resolution_run(
            vec![native_resolution_source_capability()], true, false,
        ).expect("real native Tauri resolver on fictional manifest");
        assert!(resolved.allowed_commands.contains_key("plugin:m32fixture|consult"));
        assert!(resolved.denied_commands.is_empty());
        let authority = RuntimeAuthority::new(Default::default(), resolved);
        assert!(authority.resolve_access(
            "plugin:m32fixture|consult", "main", "main", &Origin::Local
        ).is_some());
        assert!(authority.resolve_access(
            "plugin:m32fixture|consult", LAB_WINDOW, LAB_WINDOW, &Origin::Local
        ).is_none());
        assert!(authority.resolve_access(
            "plugin:m32fixture|consult", "main", LAB_WINDOW,
            &Origin::Remote { url: "https://example.invalid/".parse().unwrap() }
        ).is_none());
        println!("M32_NATIVE_ACL_MANIFEST_RESOLVE_TOY_PASS: Tauri native resolve + source main selector; fictional only");
    }

    #[test]
    fn native_resolve_wildcard_and_union_can_expose_fictional_window() {
        use tauri::ipc::{Origin, RuntimeAuthority};
        for window_selector in ["m32-*", "*"] {
            let mut cap = native_resolution_source_capability();
            cap["windows"] = serde_json::json!([window_selector]);
            let resolved = native_resolution_run(vec![cap], true, false)
                .expect("valid toy wildcard capability");
            let authority = RuntimeAuthority::new(Default::default(), resolved);
            assert!(authority.resolve_access(
                "plugin:m32fixture|consult", LAB_WINDOW, LAB_WINDOW, &Origin::Local
            ).is_some(), "native resolution failed to expose wildcard {window_selector}");
        }
        let source = native_resolution_source_capability();
        let mut second = source.clone();
        second["identifier"] = serde_json::json!("another-toy-capability");
        second["windows"] = serde_json::json!([LAB_WINDOW]);
        let resolved = native_resolution_run(vec![source, second], true, false)
            .expect("native resolution unions multiple invented capabilities");
        assert_eq!(resolved.allowed_commands["plugin:m32fixture|consult"].len(), 2);
        let authority = RuntimeAuthority::new(Default::default(), resolved);
        assert!(authority.resolve_access(
            "plugin:m32fixture|consult", LAB_WINDOW, LAB_WINDOW, &Origin::Local
        ).is_some());
    }

    #[test]
    fn native_resolve_deny_overrides_allow_even_for_other_window() {
        use tauri::ipc::{Origin, RuntimeAuthority};
        let source = native_resolution_source_capability();
        let mut deny = source.clone();
        deny["identifier"] = serde_json::json!("fictional-deny-only");
        deny["windows"] = serde_json::json!(["unrelated"]);
        deny["permissions"] = serde_json::json!(["m32fixture:deny-consult"]);
        let resolved = native_resolution_run(vec![source, deny], true, true)
            .expect("native resolution of fictional deny command");
        assert!(resolved.allowed_commands.contains_key("plugin:m32fixture|consult"));
        assert!(resolved.denied_commands.contains_key("plugin:m32fixture|consult"));
        let authority = RuntimeAuthority::new(Default::default(), resolved);
        // Tauri denies the matching command for this origin irrespective
        // of window/webview labels on the denying capability.
        assert!(authority.resolve_access(
            "plugin:m32fixture|consult", "main", "main", &Origin::Local
        ).is_none());
    }

    #[test]
    fn native_resolve_fails_on_missing_manifest_or_permission() {
        let source = native_resolution_source_capability();
        assert!(native_resolution_run(vec![source.clone()], false, false).is_err(),
            "missing manifest must not silently grant a fabricated permission");
        let mut unknown = source;
        unknown["permissions"] = serde_json::json!(["m32fixture:missing"]);
        assert!(native_resolution_run(vec![unknown], true, false).is_err(),
            "unknown permission must not silently become an allow");
    }

}
