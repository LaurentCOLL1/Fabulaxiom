# M3.2 Stage 13 — Source-pinned independent SHA reference gate

**SOURCE CANDIDATE; new exact-head Windows CI required. NOT authorized for operator use.**

Stage 12 PR #35 exact head `f839987c5b2a9c9581fd65aa4eb11bc575abc720` passed [Windows CI #38318391796](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/38318391796) completed/success **26/26 steps**, including Stage 12 multi-root synthetic tests. Protected `main=f7eabfea74480d307b52d4b053730021efc95352` unchanged. M3.2 PR remains OPEN/DRAFT/unmerged.

## Why a new gate is needed

The Stage-12 external manifest accepts a record field `authority=historical`. Its presence does NOT prove historical origin: if an operator replaces an already observed SHA in a manifest and supplies a freshly derived manifest checksum, that manifest still only attests to itself. A future writer-preparation decision MUST NEVER follow such a self-attested label. The new Stage-13 `tools/m3_2_independent_authority_gate.py` adds a source-controlled pinning rule and preserves fail-closed pending status.

## Independent source anchors and observed-only roles

- For 21 historically documented roles, SHA-256 values are pinned in the checked-in source from earlier project GitHub qualification records (PR #33 and M2/M3.1 qualification documents). The operator-provided digest must match the source pin **and** declare `historical`. SHA matching is independent of the supplied manifest hash.
- Three roles (early M2.4 manifest, archived M3.1 original ACL and pre-repair JSON) must match their recently observed SHA-256 but remain `observed`: no independent historic witness is documented. Relabeling to `historical` is rejected.
- Two roles (M1.5 active marker and existing isolated M2.5 v6 file) have no independently recorded source SHA in the current documents. They must remain `observed` and are still byte-verified by the Stage-12 multi-root manifest. An attacker-controlled or recently regenerated manifest is not sufficient to upgrade them.
- Identity/path policy fixes each known role to an exact historical relative filename (including both separately named identical-SHA M2.4 v5 backups), except pre-M2.3 where only a historical directory and paired filename pattern were recoverable; the pair must share the same basename. This is fail-closed until confirmed against the real operator filename.

## Runtime behavior

`tools/m3_2_independent_authority_gate.py` is an opt-in `--dry-run` program with NO `--prepare` or `--write` option. It first checks medium non-admin Windows token and operator app-stopped acknowledgement, verifies supplied independent manifest SHA, checks source anchors/role-path policy, and delegates source Git, filesystem path, 4-root file SHA, sidecar and active marker checks to Stage 12. No protected SQLite connection, Tauri run, backup creation, ACL modification or source/production mutation.

The **only non-failure disposition** possible with the presently known evidence is `PENDING_EXTERNAL_ATTESTATION`, always `m32_staging_authorized=false`, `operator_live_qualified=false` and a nonzero CLI exit code 2. It must never be mistaken for `READY`. On invalid or unknown facts the status is FAIL. There is currently **NO** transition to write approval in this source.

Synthetic Windows tests cover complete 26-role pinning, same-SHA distinct names, the 3 observed-label promotion attacks, unanchored marker, forged pinned SHA, wrong backup filenames, mismatched M2.3 backup+manifest pair, missing/duplicate/unapproved roles, incorrect external manifest SHA, medium-token refusal, and preservation of all source fixture bytes. They use only disposable test manifests, never operator files. The only CI change is a dedicated step to the existing required Windows workflow. Dependency lockfiles, normal SQLite schema ceiling and Tauri runtime are unchanged.

## Real machine authorization boundary

The new exact-head CI must first be terminal PASS. The operator has **not** run this program; never construct a 'historic' ACL digest from current files. The existing immutable M1.5 restored-active v6, isolated M2.5/M3.1 stores, original operator backup history, ACL archives and default Tauri runtime are untouched. Preserve exact owner, ACL, no unexpected WAL and no production migration 007. A separate, future independent witness/governance ceremony is necessary before considering any M3.2 new-identity copy/rollback preparation. PR #35 stays DRAFT, M3.3 unauthorized.
