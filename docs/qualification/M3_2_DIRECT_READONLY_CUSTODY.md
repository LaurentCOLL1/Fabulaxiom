# M3.2 Stage 16 — Manifest-free, source-pinned four-root read-only custody

**NEW SOURCE CANDIDATE. NOT qualified by any prior CI. NOT AUTHORIZED to run on the operator PC.**

## Accepted predecessor

Stage 15 exact source HEAD `11fa03d6c58dd5d7fb42a2f4c12b40850503dca8` obtained terminal [pull_request Windows CI #38408731334](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/38408731334), **completed/success, 28/28 steps**, and protected `main=f7eabfea74480d307b52d4b053730021efc95352` was unchanged. Stage 15 fixed exact legacy table-name and matching backup/restore/rollback count-and-byte semantic checks on synthetic JSON fixtures. No real production or ACL data was accessed by the CI.

## Why this stage is necessary

Stage 12 four-root custody and Stage 13 source-pinning expect an operator-provided protected SHA manifest and an independently pre-recorded SHA of that manifest. Creating a new manifest from current operator files and hashing it in the same sitting is NOT independent attestation. Such a self-referential bootstrap must not be described as historical qualification.

Stage 16 adds `tools/m3_2_direct_custody_readonly.py`, a distinct, **manifest-free** source-only SHA verifier: source-controlled role/path/SHA policy supplies 21 historical file SHA references and three separate observational SHA references. The other two roles (M1.5 activation marker and isolated M2.5 v6 database) remain explicitly UNANCHORED/OBSERVED, never inferred as historical. The direct validator requires four exact pre-existing root identities: production `com.fabulaxiom.desktop`, isolated `com.fabulaxiom.m25qual35fb842c`, isolated M3.1 `com.fabulaxiom.m31launchdb8d3278504c448084478a70ccb71cbd`, and external ACL proof `Fabulaxiom-M31-ACL-Evidence-4d520e18`. It never creates a root or reserves a proposed M3.2 identity.

## Safeguards

- `--dry-run` only; medium-integrity non-admin token, explicit app-stopped acknowledgement, exact live source commit SHA and `origin/main` SHA, clean source tree.
- Existing paths/ancestors checked for junctions, symlinks, reparse points; expected source path and precise filename required for every role. The pre-M2.3 v4 backup is discovered **only inside its historical custody folder** with the strict original filename pattern and exactly one candidate, with a correspondingly named manifest.
- All 26 file paths are hashed twice; source-pinned 21 and observed-only three are compared against distinct checked-in expected SHA-256 digests. The remaining two unanchored files are only observed for stable bytes, with no authority upgrade. Two different M2.4 v5 backup names with the same SHA are independently accepted.
- The actual M1.5 activation marker must continue to select the SHA-pinned restored-active v6 filename. Archived ACL JSON must identify the preserved isolated M3.1 identity and BUILTIN\Administrators original-owner SID, without applying that SDDL.
- Existing SQLite `-wal`, `-shm`, `-journal` sidecars on protected databases cause FAIL; the gate never removes them or opens a SQLite connection.
- No raw file data, archive SDDL, absolute protected filesystem paths or discovered sensitive row values are emitted in status output.

The only successful byte-inspection status is `PENDING_EXTERNAL_ATTESTATION`, with `m32_staging_authorized=false`, `operator_live_qualified=false`, `sqlite_opened=false`, and CLI exit **2**. An invalid source or file condition returns FAIL and also exit 2. There is NO READY/WRITE result, no --prepare, migration 007, new identity, restore action, Tauri launch or change to the normal application.

## Synthetic CI and distinct operator boundary

`tools/test_m3_2_direct_custody_readonly.py` adds 18 independent disposable synthetic unit tests to the Windows required job: role count, no manifest, duplicate-content backup names, marker selection, unexpected SHA, observational archive mismatch, unanchored isolation, hash-during-read race, missing/duplicate pre-M2.3 candidates, sidecars, ACL metadata, token, Git SHA, process ACK, occupied identity, wrong root, missing file, unsafe path and helper SHA correctness. File-digest mocking is confined to synthetic tests so they can simulate fixed historical SHA without access to the user's original bytes.

The operator must NOT execute this candidate until the **new exact-head Windows `pull_request` CI is terminal PASS**, after a separately reviewed explicit PowerShell 5.1 non-elevated preflight. This stage intentionally avoids the circular operator-manifest authority problem; it does **not** establish independent signed ACL history or qualify SQLite physical integrity, backups' restore fitness, automatic migration 007 or a writable M3.2 editor. Production restored v6, all historical M2/M3.1 copies, ACL evidence, old worktrees and `main` remain untouched; PR #35 DRAFT/unmerged, M3.3+ blocked.
