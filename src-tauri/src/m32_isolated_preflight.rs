//! Explicit DEVELOPMENT-ONLY M3.2 isolate gate, not a writer yet.
//! This phase registers exactly one metadata-only IPC command. It NEVER
//! opens SQLite or grants an editing command, even if the frontend requests it.
//! Target-Windows custody and an explicit fresh operator decision are required
//! before any separate future feature can become write capable.

use serde::Serialize;

const PREFIX: &str = "com.fabulaxiom.m32gate";
const OPERATOR_ACK: &str = "M32_READONLY_PREFLIGHT_NO_DATABASE_WRITES";

#[derive(Debug, Serialize)]
pub(crate) struct PreflightStatus {
    phase: &'static str,
    write_ipc_registered: bool,
    production_schema_migrated: bool,
    operator_data_opened: bool,
    isolated_identity_required: bool,
}

pub(crate) fn identity_valid(identity: &str) -> bool {
    identity.strip_prefix(PREFIX).is_some_and(|suffix| {
        suffix.len() == 32
            && suffix
                .bytes()
                .all(|c| c.is_ascii_hexdigit() && !c.is_ascii_uppercase())
    })
}

pub(crate) fn validate_launch(
    actual_id: &str,
    expected_id: &str,
    acknowledgement: &str,
) -> Result<(), &'static str> {
    if !identity_valid(actual_id) || actual_id != expected_id {
        return Err("m32_isolated_identity_not_approved");
    }
    if acknowledgement != OPERATOR_ACK {
        return Err("m32_readonly_preflight_not_acknowledged");
    }
    Ok(())
}

#[tauri::command]
pub(crate) fn m32_isolated_preflight_status() -> PreflightStatus {
    PreflightStatus {
        phase: "M3.2 isolated command registration preflight only",
        write_ipc_registered: false,
        production_schema_migrated: false,
        operator_data_opened: false,
        isolated_identity_required: true,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn isolated_id() -> String {
        format!("{PREFIX}0123456789abcdef0123456789abcdef")
    }

    #[test]
    fn only_explicit_isolated_m32_identity_is_accepted() {
        let approved = isolated_id();
        assert!(identity_valid(&approved));
        assert_eq!(validate_launch(&approved, &approved, OPERATOR_ACK), Ok(()));
        for invalid in [
            "com.fabulaxiom.desktop".to_string(),
            "com.fabulaxiom.m31launch0123456789abcdef0123456789abcdef".to_string(),
            format!("{PREFIX}0123456789abcdef0123456789abcdeF"),
            format!("{PREFIX}0123456789abcdef0123456789abcde"),
            format!("{PREFIX}0123456789abcdef0123456789abcdef0"),
            format!("{PREFIX}0123456789abcdef0123456789abcdeg"),
            format!("{PREFIX}../0123456789abcdef0123456789abcde"),
        ] {
            assert!(!identity_valid(&invalid));
            assert!(validate_launch(&invalid, &invalid, OPERATOR_ACK).is_err());
        }
    }

    #[test]
    fn identity_acknowledgement_and_exact_operator_expectation_are_mandatory() {
        let id = isolated_id();
        assert_eq!(
            validate_launch(&id, "com.fabulaxiom.desktop", OPERATOR_ACK),
            Err("m32_isolated_identity_not_approved")
        );
        assert_eq!(
            validate_launch(&id, &id, ""),
            Err("m32_readonly_preflight_not_acknowledged")
        );
        assert_eq!(
            validate_launch(&id, &id, "M32_WRITE_APPROVED"),
            Err("m32_readonly_preflight_not_acknowledged")
        );
    }

    #[test]
    fn current_preflight_never_claims_a_database_or_write_registration() {
        let s = m32_isolated_preflight_status();
        assert!(!s.write_ipc_registered);
        assert!(!s.production_schema_migrated);
        assert!(!s.operator_data_opened);
        assert!(s.isolated_identity_required);
    }
}
