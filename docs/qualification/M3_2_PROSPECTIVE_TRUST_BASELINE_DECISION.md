# M3.2 — Decision proposal: prospective trust baseline (governance only)

**Status: PROPOSED / REVIEW REQUIRED / NOT OPERATOR-AUTHORIZED.** Date: 2026-10-15. This document selects a *path to propose*; neither merging the document nor accepting its CI creates evidence or grants permission to execute Windows operations.

## Verified starting authorities and separation of concerns

- `LaurentCOLL1/Fabulaxiom` protected `main=f7eabfea74480d307b52d4b053730021efc95352` (PR #34 M3.1 normalization merged). PR #33 M3.1 implementation merged; its read-only v7 preview was tested only in an isolated Windows environment. Production/restored-active SQLite still uses schema **v6**, with no automatic migration 007.
- Implementation PR [#35](https://github.com/LaurentCOLL1/Fabulaxiom/pull/35) is OPEN/DRAFT/unmerged at `41ce7b915e76d22785d53d7fffe288d113dd0bf5`. Its Stage33 documentation-only Windows `pull_request` run [#38672905255](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/38672905255) completed/success **44/44**; those results qualify that *source*, not custody or real M3.2 integration.
- Historical custody [issue #36](https://github.com/LaurentCOLL1/Fabulaxiom/issues/36) is OPEN and continues to track five independent-witness gaps. Strict operator decision criteria live in [the Stage33 matrix](https://github.com/LaurentCOLL1/Fabulaxiom/blob/41ce7b915e76d22785d53d7fffe288d113dd0bf5/docs/qualification/M3_2_EXTERNAL_ATTESTATION_RESOLUTION_MATRIX.md).
- Current historical status **`PENDING_EXTERNAL_ATTESTATION`**: 21 historical SHA pins, 3 observed-only SHA and 2 roles without an independent historical SHA anchor. A future baseline cannot rewrite these historical classifications.

## Chosen route and limit of authorization

**Adopt route B as the preferred *prospective recovery governance design*, alongside one bounded final search for original independent custody witnesses.** The user chose this approach to avoid indefinitely stalling M3.2; this is NOT approval to run a script, copy protected databases, move files, alter ACL, start the application, or migrate SQLite. The baseline only authenticates and controls a **new point in time**, if a separately authorized operator ceremony later succeeds. Never label it a historical M1.5/M2.5/M3.1 restoration, nor mark any of the five prior missing independent witnesses as found.

### Historical roles remain blocked (NO auto-promotion)

| Root | Role | What would independently prove former history |
| --- | --- | --- |
| `production` | `pre_m24_early_manifest` | Earlier independent authentic custody of original early-manifest bytes/role and digest |
| `acl` | `original_acls` | Contemporaneous independent ACL-export content/digest and recorded chain of custody |
| `acl` | `pre_repair_json` | Contemporaneous independent pre-repair JSON content/digest and role |
| `production` | `activation_marker` | Historically anchored **bytes**, not just an old report naming the marker |
| `m25` | `isolated_v6` | Historical independent digest of the actual M2.5 isolated-v6 copy, not some other v6 backup |

The three observed hashes and original path hints remain in issue #36 and the Stage33 resolution matrix; never reinterpret current observation as creation-time proof. All five roles remain unverified until separately evidenced and reviewed.

## Trust states: must not be conflated

1. **Historical custody state:** `PENDING_EXTERNAL_ATTESTATION (21/3/2)` until each old role is independently examined; may remain pending permanently even if a prospective baseline is sound.
2. **Prospective baseline state:** `NOT_STARTED` → `PREPARED` → `COLLECTED_UNDER_AUTHORIZATION` → `INDEPENDENTLY_REVIEWED` → `ACCEPTED_FOR_FUTURE_REFERENCE`. Initial status **NOT_STARTED**. Never set to accepted on a documentation or unit-test success alone.
3. **Real M3.2 product qualification:** `NOT_AUTHORIZED` pending a distinct decision that explicitly states which operations may rely on the new prospective baseline despite unresolved old provenance, plus operator Windows offline qualification. This is an explicit governance-policy change, **not** a silent substitution for original historical attestation.

## Separate decision gates (all fail closed)

**Gate 0 — documentary review (this PR):** Review source/existing operator evidence, exact main and PR #35 head, and protected SHA-attached CI. Approve or reject the **protocol only**. A merge of the protocol, if later authorized, still means **no local execution authority**.

**Gate 1 — bounded historical search:** Inventory independent contemporaneous witnesses in existing third-party archives and logs *without modifying originals*. Decide for each role: independently proven with source, or `HISTORICAL_UNVERIFIED`; do not silently drop outstanding items. Stop after defined scope and record negative limits, not a fictitious proof of nonexistence.

**Gate 2 — separate operator authorization:** Publish an explicit, SHA-pinned ceremony plan naming exact **local source roles**, read-only checks, designated *new* output directory, required free space, rights, reviewer/custodian roles, no-overwrite rules, app shutdown, rollback and abort triggers. Operator must approve the plan *before* any filesystem interaction. Consent to route B is not consent to run Gate 2.

**Gate 3 — protected, consistent prospective capture:** Operator verifies 7 worktrees (without cleaning/moving), stopped Tauri/Ollama only if the protocol requires it, medium-integrity Windows token, active M1.5 restored v6 pointer and separate M3.1 v7 identity, presence and ACLs of all originals. Take a new independent consistent SQLite snapshot using the SQLite Online Backup API (or a separately reviewed equivalent) into a **new, non-colliding destination**, not by raw copying a live WAL-mode `.sqlite3` file. Record source identity, schema `user_version`, journal mode, source association, snapshot creation time, byte lengths, SHA-256, WAL/SHM conditions and versioned manifest; only query source with an approved safe read-only connection. No output to GitHub, no secrets in public logs.

**Gate 4 — verification and preservation:** On the **new copy** run `PRAGMA integrity_check` (expect exactly `ok`) and `PRAGMA foreign_key_check` (expect zero rows); independently verify SQLite schema identity, required row counts, immutable scene revision/head and provenance checks and per-table logical digests under a frozen explicit canonicalization. A hash alone does not establish a consistent snapshot; SQLite foreign-key checks are separate from integrity checks. Protect original v6 and isolated v7 artifacts; record new output hashes and compare them after copying to independent storage. An immutable/written-once manifest with authenticated provenance is required; a self-authored SHA in the same mutable folder is not independent custody. Cryptographic signing keys and their protections must be authorized separately.

**Gate 5 — independent review + restore rehearsal:** A second reviewer/custodian distinct from the person preparing the capture confirms scope, backup usability, permissions, digest recomputation, identity of historical roles and the **limits** of the prospective baseline. Restore **only into an isolated fresh destination** and repeat integrity, foreign-key, row-level and application-free audit checks. Preserve the source and activation marker unchanged. If genuinely independent review is unavailable, do not relabel the ceremony independent: hold for an explicitly reviewed alternative assurance model.

**Gate 6 — new, explicit product permission (later PR):** Only after Gates 0–5, prepare a separate, narrowly scoped plan to test **read-only** React/Tauri/SQLite v7 in an operator-approved isolated copy. Distinguish valid historical uncertainty from future baseline acceptance. The timeline GUI, cycle/revision tests and operator UI acceptance from M3.2 remain required. An editor, normal production migration 007, IPC writer, activation swap, merging PR #35 or starting M3.3 **each requires a distinct authorization and exact-source qualification**.

### Abort / rollback semantics

Any mismatched SHA/identity, changed Git refs, non-clean protected sources, missing/unclear file, ACL surprise, running process, SQLite corruption, nonzero `foreign_key_check`, unreadable backup, collision, missing disk space, misleading credential/log exposure, mismatch of historical identity, or failure of independent review → **STOP**. Leave every protected source in place. Quarantine only newly created and clearly identified ceremony outputs; never delete or revert original operator history as a side effect.

### Security/privacy and scope

This repository is PUBLIC. Never commit/upload local SQLite bytes, manifests containing private absolute paths, secret keys/passwords, confidential ACL listings, novels or private archive content. Public PR stores only **sanitized role names, check results and policy**, not operational evidence with secrets. The custody ledger and signed prospective snapshot manifests belong in protected operator-approved storage. Nothing in this document permits taking custody of user data.

## Acceptance of this document is not acceptance of M3.2

A distinct DRAFT governance PR may be considered documentation-ready only after new SHA-exact Windows CI passes, independent review of wording and a negative audit that no workflow/runtime/migration/editor code changed. The historical 21/3/2 status, PR #35 DRAFT and issue #36 OPEN must remain unchanged. **Do not mark M3.2 COMPLETE, clear `PENDING_EXTERNAL_ATTESTATION`, authorize 007 or merge PR #35 from this action.**

Technical reference (not evidence of the user's files): [SQLite Online Backup API](https://www.sqlite.org/backup.html), [SQLite PRAGMA integrity/foreign_key checks](https://www.sqlite.org/pragma.html), [GitHub required exact-head CI](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks), [NIST backup and recovery controls](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final).
