# M3.2 — Stage 15: strict M3.1 legacy custody cross-links

**SOURCE CANDIDATE. Separate exact-HEAD Windows CI must pass before acceptance. Real operator data access is NOT authorized.**

## Accepted predecessor

Stage 14 at PR #35 source HEAD `612f0e40df4fcb2d4ea697205da82a0c0c39dbc0` passed required [Windows `pull_request` CI #38340992280](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/38340992280), terminal `completed/success`, **28/28 job steps**. Protected `main=f7eabfea74480d307b52d4b053730021efc95352` remained unchanged. Source-only Stage 14 validated cross-references of five historical M3.1 JSON claims against source-pinned SHA-256; it did NOT freshly open SQLite, prove physical integrity or authenticate the independent ACL archive.

## Gap closed

Old Stage-14 validator accepted any fourteen string table names if row counts were nonnegative. Such a manifest could omit the actual `narrative_entities` or `fact_review_events` table while declaring arbitrary table names. It also did not require backup-v6 and restored-v6 table counts/byte sizes to match, or bind the forced-rollback-v6 file size to the recorded backup bytes. Those are real consistency gaps even if protected SHA-256 normally rejects unexpected on-disk changes.

Stage 15 modifies the **existing** read-only `tools/m3_2_m31_semantic_readonly.py` validator to use `m3_1_v6_audit.LEGACY_TABLES` as the exact source-controlled fourteen-name set. Its internal backups and restoration must declare the same per-table counts, and their positive integral byte sizes must be identical. The `rolled_back_file_bytes` claim must match the original v6 backup size. Booleans cannot masquerade as integers. Distinct-digest archives stay under source-pinned hash checks before and after the JSON read.

## Adversarial synthetic acceptance

The existing `tools/test_m3_2_m31_semantic_readonly.py` suite now contains **21 tests** (up from 16), entirely synthetic/disposable. Five new tests reject: an invented table replacing a real table while retaining count 14; disagreement on an existing per-table row count; differing backup/restore byte sizes; different rollback/backup sizes; and boolean-as-row-count/byte-size tricks. Existing 16 semantic/pending-source tests remain. The already-required Windows `M3.2 M3.1 archived manifests semantic Windows fixtures` step executes the expanded suite; no workflow, lockfile, production migration, Tauri runtime or plugin changes are required.

## Trust and production boundaries

These checks validate claims inside immutable historically SHA-matched JSONs; they are **not a new SQLite file integrity check, restore drill, signed historical authority, or local Windows acceptance**. `PRAGMA integrity_check` and `PRAGMA foreign_key_check` would be necessary in any separately authorized real SQLite audit; merely reading a saved manifest's `integrity` field is not equivalent. The previous source-anchored Stage 13 gate still has observed/unattested evidence and returns `PENDING_EXTERNAL_ATTESTATION`; Stage 15 never returns READY or approves staging. A valid record remains pending, with `m32_staging_authorized=false` and CLI exit code 2.

Do not reopen or mutate the M1.5 restored-active production v6, prior M2.1/M2.3/M2.4 files (including two distinct names with identical v5 content SHA), isolated M2.5 and M3.1 environments, original ACL evidence or any SQLite sidecars. Do not prepare a new M3.2 writer identity, enable schema 007, merge PR #35 or authorize M3.3. Require a NEW exact-HEAD terminal `pull_request completed/success` CI and review all steps before calling Stage 15 qualified.
