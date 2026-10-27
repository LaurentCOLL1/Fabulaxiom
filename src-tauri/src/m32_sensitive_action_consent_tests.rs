//! M3.2 single-user Windows Hello *policy* rehearsal, exclusively #[cfg(test)].
//!
//! The real desktop verifier would have to use the trusted WinRT interop
//! IUserConsentVerifierInterop::RequestVerificationForWindowAsync(HWND, ...).
//! This fixture NEVER invokes Windows Hello and NEVER accepts a client-supplied
//! `verified` flag. Its fake OS outcome only tests policy logic. No operation
//! is wired to Tauri, an operator SQLite database, or the real M3.2 gate.

const CONSENT_WINDOW_MS: u64 = 30_000;

#[derive(Clone, Debug, Eq, PartialEq)]
enum SensitiveAction {
    ConfirmManualChronologyCorrection,
    RestoreBackup,
    ActivateNewV7,
    DeleteProject,
}

#[derive(Clone, Debug, Eq, PartialEq)]
struct ExactIntent {
    action: SensitiveAction,
    // Opaque synthetic fixture IDs, NEVER a filesystem path or a PIN.
    resource_id: String,
    // Must change whenever the selected content or revision changes.
    revision_fingerprint: String,
}

impl ExactIntent {
    fn fictional(action: SensitiveAction, resource: &str, fingerprint: &str) -> Self {
        Self { action, resource_id: resource.into(), revision_fingerprint: fingerprint.into() }
    }

    fn is_complete(&self) -> bool {
        !self.resource_id.trim().is_empty() && !self.revision_fingerprint.trim().is_empty()
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
enum TrustedOsOutcome {
    Verified,
    Canceled,
    DeviceNotPresent,
    NotConfiguredForUser,
    DisabledByPolicy,
    DeviceBusy,
    RetriesExhausted,
    ApiFailure,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
enum Refusal {
    GateNotAuthorized,
    IntentIncomplete,
    ConsentAlreadyPending,
    NoPendingConsent,
    ClockInvalid,
    ConsentExpired,
    ConsentNotVerified,
    IntentChanged,
    RevalidationFailed,
}

#[derive(Clone, Debug)]
struct PendingConsent {
    intent: ExactIntent,
    requested_at_ms: u64,
    expires_at_ms: u64,
}

#[derive(Default)]
struct FixtureSensitiveActionBoundary {
    pending: Option<PendingConsent>,
    committed_fixture_intents: Vec<ExactIntent>,
}

impl FixtureSensitiveActionBoundary {
    fn request(&mut self, intent: ExactIntent, now_ms: u64,
               separately_authorized_gate: bool) -> Result<(), Refusal> {
        if !separately_authorized_gate { return Err(Refusal::GateNotAuthorized); }
        if !intent.is_complete() { return Err(Refusal::IntentIncomplete); }
        if self.pending.is_some() { return Err(Refusal::ConsentAlreadyPending); }
        let expiry = now_ms.checked_add(CONSENT_WINDOW_MS).ok_or(Refusal::ClockInvalid)?;
        self.pending = Some(PendingConsent {
            intent, requested_at_ms: now_ms, expires_at_ms: expiry,
        });
        Ok(())
    }

    // One-shot atomic policy *fixture*: take() invalidates even on denial.
    // A production command must additionally revalidate preflight/SQLite
    // identity and enforce gates INSIDE its backend before any real mutation.
    fn apply_fixture(&mut self, current_intent: &ExactIntent,
                     trusted_os_outcome: TrustedOsOutcome, now_ms: u64,
                     separately_authorized_gate: bool, fresh_preflight_ok: bool)
                     -> Result<(), Refusal> {
        let ticket = self.pending.take().ok_or(Refusal::NoPendingConsent)?;
        if !separately_authorized_gate { return Err(Refusal::GateNotAuthorized); }
        if now_ms < ticket.requested_at_ms { return Err(Refusal::ClockInvalid); }
        if now_ms > ticket.expires_at_ms { return Err(Refusal::ConsentExpired); }
        if trusted_os_outcome != TrustedOsOutcome::Verified {
            return Err(Refusal::ConsentNotVerified);
        }
        if *current_intent != ticket.intent { return Err(Refusal::IntentChanged); }
        if !fresh_preflight_ok { return Err(Refusal::RevalidationFailed); }
        // Never write SQLite: the only effect is a disposable in-RAM vector.
        self.committed_fixture_intents.push(ticket.intent);
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn decision() -> ExactIntent {
        ExactIntent::fictional(SensitiveAction::ConfirmManualChronologyCorrection,
                              "fixture-universe-1", "revision-a")
    }

    #[test]
    fn m32_hello_fixture_exact_verified_decision_is_one_shot() {
        let mut boundary = FixtureSensitiveActionBoundary::default();
        let intent = decision();
        boundary.request(intent.clone(), 100, true).unwrap();
        boundary.apply_fixture(&intent, TrustedOsOutcome::Verified, 101, true, true).unwrap();
        assert_eq!(boundary.committed_fixture_intents, vec![intent.clone()]);
        assert_eq!(boundary.apply_fixture(&intent, TrustedOsOutcome::Verified, 102, true, true),
                   Err(Refusal::NoPendingConsent));
        assert_eq!(boundary.committed_fixture_intents.len(), 1);
    }

    #[test]
    fn m32_hello_fixture_never_accepts_missing_ticket_or_gate() {
        let mut boundary = FixtureSensitiveActionBoundary::default();
        let intent = decision();
        assert_eq!(boundary.apply_fixture(&intent, TrustedOsOutcome::Verified, 50, true, true),
                   Err(Refusal::NoPendingConsent));
        assert_eq!(boundary.request(intent.clone(), 50, false),
                   Err(Refusal::GateNotAuthorized));
        boundary.request(intent.clone(), 50, true).unwrap();
        assert_eq!(boundary.apply_fixture(&intent, TrustedOsOutcome::Verified, 51, false, true),
                   Err(Refusal::GateNotAuthorized));
        assert!(boundary.committed_fixture_intents.is_empty());
        assert!(boundary.pending.is_none());
    }

    #[test]
    fn m32_hello_fixture_every_nonverified_os_outcome_stops_and_consumes() {
        for failure in [TrustedOsOutcome::Canceled, TrustedOsOutcome::DeviceNotPresent,
                        TrustedOsOutcome::NotConfiguredForUser,
                        TrustedOsOutcome::DisabledByPolicy, TrustedOsOutcome::DeviceBusy,
                        TrustedOsOutcome::RetriesExhausted, TrustedOsOutcome::ApiFailure] {
            let mut boundary = FixtureSensitiveActionBoundary::default();
            let intent = decision();
            boundary.request(intent.clone(), 100, true).unwrap();
            assert_eq!(boundary.apply_fixture(&intent, failure, 110, true, true),
                       Err(Refusal::ConsentNotVerified), "{failure:?}");
            assert!(boundary.pending.is_none());
            assert!(boundary.committed_fixture_intents.is_empty());
        }
    }

    #[test]
    fn m32_hello_fixture_action_substitution_fails_closed() {
        for different_action in [SensitiveAction::RestoreBackup,
                                 SensitiveAction::ActivateNewV7,
                                 SensitiveAction::DeleteProject] {
            let mut boundary = FixtureSensitiveActionBoundary::default();
            boundary.request(decision(), 1, true).unwrap();
            let changed = ExactIntent::fictional(different_action, "fixture-universe-1", "revision-a");
            assert_eq!(boundary.apply_fixture(&changed, TrustedOsOutcome::Verified, 2, true, true),
                       Err(Refusal::IntentChanged));
            assert!(boundary.committed_fixture_intents.is_empty());
        }
    }

    #[test]
    fn m32_hello_fixture_target_substitution_fails_closed() {
        let mut boundary = FixtureSensitiveActionBoundary::default();
        boundary.request(decision(), 1, true).unwrap();
        let other = ExactIntent::fictional(SensitiveAction::ConfirmManualChronologyCorrection,
                                         "fixture-universe-2", "revision-a");
        assert_eq!(boundary.apply_fixture(&other, TrustedOsOutcome::Verified, 2, true, true),
                   Err(Refusal::IntentChanged));
        assert!(boundary.committed_fixture_intents.is_empty());
    }

    #[test]
    fn m32_hello_fixture_revision_change_fails_closed() {
        let mut boundary = FixtureSensitiveActionBoundary::default();
        boundary.request(decision(), 1, true).unwrap();
        let changed = ExactIntent::fictional(SensitiveAction::ConfirmManualChronologyCorrection,
                                           "fixture-universe-1", "revision-b");
        assert_eq!(boundary.apply_fixture(&changed, TrustedOsOutcome::Verified, 2, true, true),
                   Err(Refusal::IntentChanged));
        assert!(boundary.committed_fixture_intents.is_empty());
    }

    #[test]
    fn m32_hello_fixture_expiry_and_backward_clock_stop() {
        let mut boundary = FixtureSensitiveActionBoundary::default();
        let intent = decision();
        boundary.request(intent.clone(), 100, true).unwrap();
        assert_eq!(boundary.apply_fixture(&intent, TrustedOsOutcome::Verified, 30_101, true, true),
                   Err(Refusal::ConsentExpired));
        boundary.request(intent.clone(), 100, true).unwrap();
        assert_eq!(boundary.apply_fixture(&intent, TrustedOsOutcome::Verified, 99, true, true),
                   Err(Refusal::ClockInvalid));
        assert!(boundary.committed_fixture_intents.is_empty());
    }

    #[test]
    fn m32_hello_fixture_clock_overflow_rejected_before_prompt() {
        let mut boundary = FixtureSensitiveActionBoundary::default();
        assert_eq!(boundary.request(decision(), u64::MAX, true), Err(Refusal::ClockInvalid));
        assert!(boundary.pending.is_none());
    }

    #[test]
    fn m32_hello_fixture_disallows_two_parallel_consent_requests() {
        let mut boundary = FixtureSensitiveActionBoundary::default();
        boundary.request(decision(), 1, true).unwrap();
        assert_eq!(boundary.request(decision(), 2, true), Err(Refusal::ConsentAlreadyPending));
        assert!(boundary.committed_fixture_intents.is_empty());
    }

    #[test]
    fn m32_hello_fixture_empty_identity_or_revision_denied() {
        let mut boundary = FixtureSensitiveActionBoundary::default();
        let empty_target = ExactIntent::fictional(SensitiveAction::DeleteProject, " ", "revision-a");
        let empty_revision = ExactIntent::fictional(SensitiveAction::DeleteProject, "fixture", " ");
        assert_eq!(boundary.request(empty_target, 1, true), Err(Refusal::IntentIncomplete));
        assert_eq!(boundary.request(empty_revision, 1, true), Err(Refusal::IntentIncomplete));
    }

    #[test]
    fn m32_hello_fixture_backend_revalidation_still_required_after_hello() {
        let mut boundary = FixtureSensitiveActionBoundary::default();
        let intent = decision();
        boundary.request(intent.clone(), 100, true).unwrap();
        assert_eq!(boundary.apply_fixture(&intent, TrustedOsOutcome::Verified, 101, true, false),
                   Err(Refusal::RevalidationFailed));
        assert!(boundary.pending.is_none());
        assert!(boundary.committed_fixture_intents.is_empty());
    }
}
