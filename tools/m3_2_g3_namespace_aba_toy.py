"""M3.2 G3: disposable toy Windows transient-namespace ABA counterexample.

This module DEMONSTRATES an unproven security property; it does not close
the gap or qualify a real SQLite source. CLI only accepts --self-test.
All runtime paths are created internally with TemporaryDirectory.
"""
from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import tempfile

from m3_2_g3_win_single_handle_toy import (
    TOY_PREFIX, TOY_FILE, ToyGateError, create_fictional_toy
)
from m3_2_g3_win_pinned_toy_directory import inspect_under_pinned_toy_root


class TransientToyVeto(RuntimeError):
    pass


@dataclass(frozen=True)
class EndpointEvidence:
    before_id: tuple[int, ...]
    after_id: tuple[int, ...]


def checkpoint_only_verdict(endpoints: EndpointEvidence) -> str:
    """Two identity readings CANNOT prove no intervening namespace changes."""
    if not endpoints.before_id or endpoints.before_id != endpoints.after_id:
        return "VETO_OBSERVED_IDENTITY_MISMATCH"
    return "ENDPOINT_EQUAL_TRANSIENT_UNPROVEN"


def require_real_g3_authority(*, toy_verdict: str, provenance: str = "toy") -> None:
    """Never authorize actual G3 from this laboratory; no override available."""
    raise TransientToyVeto(
        "REAL_G3_NOT_AUTHORIZED: endpoint snapshots and toy provenance insufficient"
    )


def toy_transient_rename(root: Path, source: Path) -> dict[str, object]:
    """Attempt RENAME->RESTORE while a disposable source+directory handle lives.

    If rename is blocked, that is one possible OS result. If allowed and
    restored, the endpoint identity checks may observe the original folder
    despite the transient namespace change. Either result is NOT a real G3 GO.
    """
    if os.name != "nt" or root.parent != Path(tempfile.gettempdir()):
        raise TransientToyVeto("only Windows generated temporary fixtures")
    if not root.name.startswith(TOY_PREFIX) or source != root / TOY_FILE:
        raise TransientToyVeto("unrecognized synthetic role")

    detour = root.with_name(root.name + "-aba-detour")
    if detour.exists() or detour.is_symlink():
        raise TransientToyVeto("detour already occupied")
    facts: dict[str, object] = {
        "attempted": False, "renamed": False, "restored": False,
        "kernel_denied": False, "audit_result": None,
        "real_g3_authorized": False,
    }

    def injection(path: Path, _: Path) -> None:
        facts["attempted"] = True
        try:
            os.rename(path, detour)
        except OSError:
            facts["kernel_denied"] = True
            return
        facts["renamed"] = True
        try:
            os.rename(detour, path)
        except OSError as exc:
            raise TransientToyVeto("toy directory could not be restored") from exc
        facts["restored"] = True

    # A matching result here is a COUNTEREXAMPLE when rename+restore occurred,
    # not an attestation that the source path has always been stable.
    try:
        result = inspect_under_pinned_toy_root(
            root, source, version=6, test_hook=injection
        )
    finally:
        # Every toy output is confined to its own TemporaryDirectory. In the
        # unlikely event an injected rename could not be undone while handles
        # were held, attempt restoration after handles close, without touching
        # any operator folder.
        if detour.exists() and not root.exists():
            os.rename(detour, root)
    facts["audit_result"] = result["status"]
    facts["endpoint_only_safety"] = "UNPROVEN"
    return facts


def toy_transient_sidecar(root: Path, source: Path) -> dict[str, object]:
    """Briefly create/delete a fictional -journal between sidecar checkpoints.

    No SQLite rollback recovery is triggered. This demonstrates an
    observational gap, not a valid test for hot journal recoverability.
    """
    if os.name != "nt" or root.parent != Path(tempfile.gettempdir()):
        raise TransientToyVeto("Windows temporary fixture only")
    journal = Path(str(source) + "-journal")
    if journal.exists() or journal.is_symlink():
        raise TransientToyVeto("preexisting journal")
    injected = False

    def injection(_: Path, __: Path) -> None:
        nonlocal injected
        with journal.open("xb") as stream:
            stream.write(b"DISPOSABLE-SENTINEL-NOT-A-SQLITE-JOURNAL")
        injected = True
        journal.unlink()

    try:
        audit = inspect_under_pinned_toy_root(
            root, source, version=6, test_hook=injection
        )
    except ToyGateError as exc:
        # The first Windows CI observed a directory last-write-time change
        # caused by the create/delete of the fictional journal. This is a
        # correct fail-closed veto, NOT a test to disable or work around.
        if str(exc) != "toy directory handle changed":
            raise
        return {
            "journal_transient": injected,
            "checkpoint_audit": "VETO_DIRECTORY_METADATA_CHANGED",
            "real_g3_authorized": False,
            "time_of_check_use_race": "UNPROVEN",
        }
    return {
        "journal_transient": injected,
        "checkpoint_audit": audit["status"],
        "real_g3_authorized": False,
        "time_of_check_use_race": "UNPROVEN",
    }


def self_test() -> None:
    if os.name != "nt":
        raise TransientToyVeto("Win32 tests only")
    with tempfile.TemporaryDirectory(prefix=TOY_PREFIX) as name:
        root = Path(name)
        src = create_fictional_toy(root, 6)
        outcome = toy_transient_rename(root, src)
        if outcome["real_g3_authorized"] or not outcome["attempted"]:
            raise TransientToyVeto("toy-only rename gate failed")
    print("G3 TRANSIENT NAMESPACE TOY: observation-only / real G3 blocked")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="G3 temporary toy namespace ABA experiment")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if not args.self_test:
        parser.error("ONLY --self-test; no operator paths or real outputs")
    self_test()
