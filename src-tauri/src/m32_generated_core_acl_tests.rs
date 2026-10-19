//! CI-only read-only tests for real Tauri-build Core manifest output.
//! Loaded solely from #[cfg(test)] under the non-default M3.2 feature.
//! No Tauri Builder, WebView2 runtime, SQLite or original operator data.
use super::LAB_WINDOW;

    // Reads only Tauri-build-generated ACL files from THIS GitHub CI checkout.
    // This evaluates actual generated CORE permission manifests without invoking
    // a CLI, Tauri Builder or WebView. It is not the private Context authority.
    fn native_generated_core_inputs() -> (
        std::collections::BTreeMap<String, tauri::utils::acl::manifest::Manifest>,
        std::collections::BTreeMap<String, tauri::utils::acl::capability::Capability>,
    ) {
        use std::{collections::BTreeMap, fs, path::PathBuf};
        use tauri::utils::acl::{capability::Capability, manifest::Manifest};
        assert_eq!(std::env::var("CI").as_deref(), Ok("true"), "STOP: CI only");
        assert_eq!(std::env::var("RUNNER_OS").as_deref(), Ok("Windows"), "STOP: Windows runner only");
        assert!(std::env::var_os("TAURI_CONFIG").is_none(), "STOP: no external config overlay");
        assert!(std::env::var_os("TAURI_DEV_HOST").is_none(), "STOP: no wildcard dev host");
        let root = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
            .canonicalize().expect("CI source directory exists");
        let generated = root.join("gen").join("schemas");
        for sub in [root.join("gen"), generated.clone()] {
            assert!(!fs::symlink_metadata(&sub).expect("Tauri build generated schemas").file_type().is_symlink(),
                "STOP: generated directory is a symlink");
        }
        let read = |name: &str| {
            let file = generated.join(name);
            assert!(!fs::symlink_metadata(&file).expect("Tauri build generated ACL file").file_type().is_symlink(),
                "STOP: generated ACL file is a symlink");
            let exact = file.canonicalize().expect("canonical CI generated file");
            assert!(exact.starts_with(&root), "STOP: generated ACL escaped checkout");
            fs::read_to_string(&exact).expect("Tauri-build must produce JSON inside CI checkout")
        };
        let manifests: BTreeMap<String, Manifest> =
            serde_json::from_str(&read("acl-manifests.json")).expect("real generated Tauri manifests");
        let capabilities: BTreeMap<String, Capability> =
            serde_json::from_str(&read("capabilities.json")).expect("real generated Tauri capabilities");
        (manifests, capabilities)
    }

    #[test]
    fn native_generated_core_real_manifest_and_capability_source_agree() {
        let (manifests, capabilities) = native_generated_core_inputs();
        let original: serde_json::Value = serde_json::from_str(
            include_str!("../capabilities/default.json")
        ).expect("tracked public capability");
        assert_eq!(capabilities.keys().map(String::as_str).collect::<Vec<_>>(), vec!["default"]);
        assert_eq!(original["identifier"], "default");
        assert_eq!(original["permissions"], serde_json::json!(["core:default"]));
        assert_eq!(original["windows"], serde_json::json!(["main"]));
        let generated: serde_json::Value =
            serde_json::to_value(&capabilities["default"]).expect("serialize generated capability");
        assert_eq!(generated["identifier"], original["identifier"]);
        assert_eq!(generated["permissions"], original["permissions"]);
        assert_eq!(generated["windows"], original["windows"]);
        assert!(manifests.contains_key("core"), "Tauri build output missing core manifest");
        for group in ["app", "event", "image", "menu", "path", "resources", "tray", "webview", "window"] {
            assert!(manifests.contains_key(&format!("core:{group}")),
                "Tauri build output missing core plugin family {group}");
        }
        println!("M32_NATIVE_GENERATED_CORE_SOURCE_BINDING_PASS: core ACL manifests from isolated Windows CI; no runtime");
    }

    #[test]
    fn native_generated_core_resolves_real_default_to_main_but_not_lab() {
        use tauri::{ipc::{Origin, RuntimeAuthority},
            utils::{acl::resolved::Resolved, platform::Target}};
        let (manifests, capabilities) = native_generated_core_inputs();
        let resolved = Resolved::resolve(&manifests, capabilities, Target::current())
            .expect("real Core default permission resolution from generated Tauri manifests");
        assert!(resolved.allowed_commands.len() > 10, "core:default unexpectedly resolves too few commands");
        assert!(resolved.allowed_commands.contains_key("plugin:app|version"),
            "actual generated core:app default must contain app version");
        let names: Vec<String> = resolved.allowed_commands.keys().cloned().collect();
        let authority = RuntimeAuthority::new(manifests, resolved);
        assert!(authority.resolve_access(
            "plugin:app|version", "main", "main", &Origin::Local
        ).is_some(), "normal main selector must match generated core permission");
        for command in &names {
            assert!(authority.resolve_access(command, LAB_WINDOW, LAB_WINDOW, &Origin::Local).is_none(),
                "STOP: generated real Core default leaked command {command} to fiction window");
        }
        assert!(authority.resolve_access(
            "plugin:app|version", "main", "main",
            &Origin::Remote { url: "https://example.invalid/".parse().unwrap() }
        ).is_none());
        println!("M32_NATIVE_GENERATED_CORE_LAB_DENIAL_PASS: generated Core command inventory denied for fiction; compile-time only");
    }

    #[test]
    fn native_generated_core_mutant_wildcard_exposes_lab_as_expected() {
        use tauri::{ipc::{Origin, RuntimeAuthority},
            utils::{acl::resolved::Resolved, platform::Target}};
        let (manifests, mut capabilities) = native_generated_core_inputs();
        capabilities.get_mut("default").expect("generated exact source")
            .windows = vec!["*".into()]; // IN-MEMORY NEGATIVE CONTROL ONLY
        let resolved = Resolved::resolve(&manifests, capabilities, Target::current())
            .expect("native Core manifest wildcard mutation");
        let authority = RuntimeAuthority::new(manifests, resolved);
        assert!(authority.resolve_access(
            "plugin:app|version", LAB_WINDOW, LAB_WINDOW, &Origin::Local
        ).is_some(), "test must detect an intentionally widened capability selector");
    }

    #[test]
    fn native_generated_core_unknown_permission_fails_closed() {
        use tauri::utils::{acl::{capability::Capability, resolved::Resolved}, platform::Target};
        let (manifests, mut capabilities) = native_generated_core_inputs();
        let mut cap = serde_json::to_value(&capabilities["default"])
            .expect("generated capability serialized for test mutation");
        cap["permissions"] = serde_json::json!(["core:permission-does-not-exist"]);
        capabilities.insert("default".to_string(),
            serde_json::from_value::<Capability>(cap).expect("valid mutated capability"));
        assert!(Resolved::resolve(&manifests, capabilities, Target::current()).is_err());
    }
