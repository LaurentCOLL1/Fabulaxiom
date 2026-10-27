//! Desktop Windows Hello HWND *preflight rehearsal* on invented values only.
//!
//! No actual Win32 handle, WinRT call, Tauri command, SQLite connection or IPC
//! is created here. `owned_by_process` and `active_window` are deliberately
//! supplied by the test, NOT trustworthy statements from React. A future native
//! backend would have to measure these itself, handle races, and be separately
//! authorized. A successful test is not proof of native compatibility.

const DESKTOP_INTEROP_MIN_BUILD: u32 = 22_000;

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
enum DeviceAvailability {
    Available,
    DeviceNotPresent,
    NotConfiguredForUser,
    DisabledByPolicy,
    DeviceBusy,
    ApiFailure,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
enum DesktopRefusal {
    GateClosed,
    UnsupportedDesktopBuild,
    MissingAppWindow,
    ForeignAppWindow,
    InactiveAppWindow,
    DeviceUnavailable,
    SnapshotChanged,
    VerificationNotApproved,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
struct InventedDesktopSnapshot {
    windows_build: u32,
    // Opaque integers of a made-up window, never actual HWND/PID values.
    window_id: u64,
    process_id: u32,
    window_owner_process_id: u32,
    active_app_window_id: u64,
    availability: DeviceAvailability,
    separately_authorized_gate: bool,
}

impl InventedDesktopSnapshot {
    fn fixture() -> Self {
        Self {
            windows_build: DESKTOP_INTEROP_MIN_BUILD,
            window_id: 0x1234,
            process_id: 100,
            window_owner_process_id: 100,
            active_app_window_id: 0x1234,
            availability: DeviceAvailability::Available,
            separately_authorized_gate: true,
        }
    }
}

// A mock call plan is NOT a bearer capability, verified consent, or IPC value.
// It may only be consumed by the simulated completion below.
fn plan_fixture_desktop_call(
    state: InventedDesktopSnapshot,
) -> Result<InventedDesktopSnapshot, DesktopRefusal> {
    if !state.separately_authorized_gate {
        return Err(DesktopRefusal::GateClosed);
    }
    if state.windows_build < DESKTOP_INTEROP_MIN_BUILD {
        return Err(DesktopRefusal::UnsupportedDesktopBuild);
    }
    if state.window_id == 0 || state.process_id == 0 {
        return Err(DesktopRefusal::MissingAppWindow);
    }
    if state.window_owner_process_id != state.process_id {
        return Err(DesktopRefusal::ForeignAppWindow);
    }
    if state.active_app_window_id != state.window_id {
        return Err(DesktopRefusal::InactiveAppWindow);
    }
    if state.availability != DeviceAvailability::Available {
        return Err(DesktopRefusal::DeviceUnavailable);
    }
    Ok(state)
}

// `os_verified` is test injection, never a React/IPC boolean. A real native
// result is checked only inside an authorized backend and is insufficient on
// its own: exact action/revision, storage identity and writer gates remain.
fn finish_fixture_desktop_call(
    planned: InventedDesktopSnapshot,
    fresh: InventedDesktopSnapshot,
    os_verified: bool,
) -> Result<(), DesktopRefusal> {
    if !os_verified {
        return Err(DesktopRefusal::VerificationNotApproved);
    }
    if planned != fresh {
        return Err(DesktopRefusal::SnapshotChanged);
    }
    plan_fixture_desktop_call(fresh).map(|_| ())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn m32_desktop_hello_fixture_windows_10_never_falls_back_to_uwp() {
        let mut state = InventedDesktopSnapshot::fixture();
        state.windows_build = 19_045;
        assert_eq!(plan_fixture_desktop_call(state),
                   Err(DesktopRefusal::UnsupportedDesktopBuild));
        state.windows_build = 21_999;
        assert_eq!(plan_fixture_desktop_call(state),
                   Err(DesktopRefusal::UnsupportedDesktopBuild));
    }

    #[test]
    fn m32_desktop_hello_fixture_22000_is_only_a_call_candidate() {
        let state = InventedDesktopSnapshot::fixture();
        assert_eq!(plan_fixture_desktop_call(state), Ok(state));
        // A candidate plan alone never asserts any successful verification.
        assert_eq!(finish_fixture_desktop_call(state, state, false),
                   Err(DesktopRefusal::VerificationNotApproved));
    }

    #[test]
    fn m32_desktop_hello_fixture_gate_must_precede_even_eligibility() {
        let mut state = InventedDesktopSnapshot::fixture();
        state.separately_authorized_gate = false;
        assert_eq!(plan_fixture_desktop_call(state), Err(DesktopRefusal::GateClosed));
        assert_eq!(finish_fixture_desktop_call(InventedDesktopSnapshot::fixture(), state, true),
                   Err(DesktopRefusal::SnapshotChanged));
    }

    #[test]
    fn m32_desktop_hello_fixture_missing_foreign_or_inactive_window_refused() {
        let mut state = InventedDesktopSnapshot::fixture();
        state.window_id = 0;
        assert_eq!(plan_fixture_desktop_call(state), Err(DesktopRefusal::MissingAppWindow));
        state = InventedDesktopSnapshot::fixture();
        state.window_owner_process_id = 999;
        assert_eq!(plan_fixture_desktop_call(state), Err(DesktopRefusal::ForeignAppWindow));
        state = InventedDesktopSnapshot::fixture();
        state.active_app_window_id = 0x5678;
        assert_eq!(plan_fixture_desktop_call(state), Err(DesktopRefusal::InactiveAppWindow));
    }

    #[test]
    fn m32_desktop_hello_fixture_all_unavailable_states_refused() {
        for availability in [DeviceAvailability::DeviceNotPresent,
                             DeviceAvailability::NotConfiguredForUser,
                             DeviceAvailability::DisabledByPolicy,
                             DeviceAvailability::DeviceBusy,
                             DeviceAvailability::ApiFailure] {
            let mut state = InventedDesktopSnapshot::fixture();
            state.availability = availability;
            assert_eq!(plan_fixture_desktop_call(state), Err(DesktopRefusal::DeviceUnavailable));
        }
    }

    #[test]
    fn m32_desktop_hello_fixture_snapshot_swap_and_stale_completion_refused() {
        let state = InventedDesktopSnapshot::fixture();
        for changed in [
            InventedDesktopSnapshot { window_id: 0x9876, ..state },
            InventedDesktopSnapshot { active_app_window_id: 0x9876, ..state },
            InventedDesktopSnapshot { window_owner_process_id: 101, ..state },
            InventedDesktopSnapshot { separately_authorized_gate: false, ..state },
            InventedDesktopSnapshot { availability: DeviceAvailability::DeviceBusy, ..state },
            InventedDesktopSnapshot { windows_build: 19_045, ..state },
        ] {
            assert_eq!(finish_fixture_desktop_call(state, changed, true),
                       Err(DesktopRefusal::SnapshotChanged));
        }
        assert_eq!(finish_fixture_desktop_call(state, state, true), Ok(()));
        // Ok means only that invented predicates were true; no action is run.
    }
}
