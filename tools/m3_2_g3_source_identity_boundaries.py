"""M3.2 G3 source-identity acquisition design screen, with NO runtime I/O.

Every outcome is a design review disposition, never real source authorization.
Do not add operator paths, SQLite openers, credentials or Win32 handles here.
"""
from dataclasses import dataclass, field
from enum import Enum


class SourceCandidate(str, Enum):
    CURRENT_MIGRATING_APP_OPEN = "current_migrating_app_open"
    SQLITE_PATH_READONLY_REOPEN = "sqlite_path_readonly_reopen"
    SQLITE_IMMUTABLE_URI = "sqlite_immutable_uri"
    SQLITE_DB_FILENAME = "sqlite_db_filename"
    SQLITE_FILE_POINTER = "sqlite_file_pointer"
    RUSQLITE_RAW_HANDLE = "rusqlite_raw_handle"
    WIN32_FILE_ID_ONLY = "win32_file_id_only"
    HISTORICAL_HASH_ONLY = "historical_hash_only"
    RAM_ONLY_OWNER_ACTOR = "ram_only_owner_actor"
    CUSTOM_SQLITE_VFS_PROPOSAL = "custom_sqlite_vfs_proposal"
    AUTHENTICATED_PREOPENED_OWNER_PROPOSAL = "authenticated_preopened_owner_proposal"


class Disposition(str, Enum):
    VETO_UNSAFE_SHORTCUT = "VETO_UNSAFE_SHORTCUT"
    NOT_SOURCE_PROVENANCE = "NOT_SOURCE_PROVENANCE"
    ARCHITECTURE_REVIEW_ONLY = "ARCHITECTURE_REVIEW_ONLY"


@dataclass(frozen=True)
class ScreenResult:
    candidate: SourceCandidate
    disposition: Disposition
    rationale: str
    missing_boundary: tuple[str, ...]
    real_g3_authorized: bool = field(init=False, default=False)


# This is deliberately exhaustive: adding a candidate requires a code change,
# a new threat model and fresh exact-head CI. No fallback route can silently pass.
_DESIGN_SCREEN: dict[SourceCandidate, tuple[Disposition, str, tuple[str, ...]]] = {
    SourceCandidate.CURRENT_MIGRATING_APP_OPEN: (
        Disposition.VETO_UNSAFE_SHORTCUT,
        "Existing application open creates directories and runs migrations.",
        ("non_migrating_source", "independent_original_identity"),
    ),
    SourceCandidate.SQLITE_PATH_READONLY_REOPEN: (
        Disposition.VETO_UNSAFE_SHORTCUT,
        "A new read-only SQLite open is still a distinct source acquisition, potentially involving recovery/journals.",
        ("operator_authorized_acquisition", "no_original_side_effects", "independent_original_identity"),
    ),
    SourceCandidate.SQLITE_IMMUTABLE_URI: (
        Disposition.VETO_UNSAFE_SHORTCUT,
        "immutable=1 disables locking and change detection; it cannot prove the file never changes.",
        ("immutable_original_attestation", "journal_consistency", "continuous_source_identity"),
    ),
    SourceCandidate.SQLITE_DB_FILENAME: (
        Disposition.NOT_SOURCE_PROVENANCE,
        "SQLite returns a VFS-full pathname, not an authenticated Windows file object.",
        ("sqlite_connection_to_win32_object_binding", "ancestor_identity_continuity"),
    ),
    SourceCandidate.SQLITE_FILE_POINTER: (
        Disposition.NOT_SOURCE_PROVENANCE,
        "SQLITE_FCNTL_FILE_POINTER returns sqlite3_file*, not a portable verified Win32 HANDLE.",
        ("vfs_specific_owned_handle_proof", "journal_sidecar_provenance"),
    ),
    SourceCandidate.RUSQLITE_RAW_HANDLE: (
        Disposition.VETO_UNSAFE_SHORTCUT,
        "Unsafe raw sqlite3 pointer adapters do not authenticate the underlying original or establish ownership.",
        ("raw_handle_lifetime_audit", "independent_original_identity"),
    ),
    SourceCandidate.WIN32_FILE_ID_ONLY: (
        Disposition.NOT_SOURCE_PROVENANCE,
        "A Windows identity belongs to the inspected handle, not automatically to the handle owned by SQLite.",
        ("sqlite_connection_to_win32_object_binding", "namespace_and_ancestor_continuity"),
    ),
    SourceCandidate.HISTORICAL_HASH_ONLY: (
        Disposition.NOT_SOURCE_PROVENANCE,
        "An operator-observed hash cannot retroactively authenticate missing historical custody anchors.",
        ("independently_anchored_historical_custody", "exact_original_binding"),
    ),
    SourceCandidate.RAM_ONLY_OWNER_ACTOR: (
        Disposition.NOT_SOURCE_PROVENANCE,
        "Synthetic RAM owner proves move, serialize and revoke behavior, not original-file identity.",
        ("independent_original_identity", "original_preopened_owner"),
    ),
    SourceCandidate.CUSTOM_SQLITE_VFS_PROPOSAL: (
        Disposition.ARCHITECTURE_REVIEW_ONLY,
        "A dedicated VFS might support handle binding, but requires a separate implementation and OS/SQLite safety review.",
        ("audited_vfs_and_sidecars", "operator_authorized_acquisition", "continuous_original_identity"),
    ),
    SourceCandidate.AUTHENTICATED_PREOPENED_OWNER_PROPOSAL: (
        Disposition.ARCHITECTURE_REVIEW_ONLY,
        "No authenticated non-migrating preopened source-owner exists in the inspected production runtime.",
        ("real_authenticated_preopened_owner", "source_lifetime_and_journal_assurance", "operator_specific_consent"),
    ),
}


def screen(candidate: SourceCandidate) -> ScreenResult:
    if not isinstance(candidate, SourceCandidate):
        raise TypeError("Only a typed SourceCandidate may be screened")
    disposition, rationale, requirements = _DESIGN_SCREEN[candidate]
    return ScreenResult(candidate, disposition, rationale, requirements)


def all_screened() -> tuple[ScreenResult, ...]:
    return tuple(screen(candidate) for candidate in SourceCandidate)
