# Fabulaxiom — Current State

## 2026-10-14 Stage 24 — synthetic read-only chronology filter/navigation SOURCE CANDIDATE; NEW CI pending

Stage23 exact source `3cb8a334098633cea321b1f76a6b58001260bd1d` passed Windows pull_request CI #38605084315 **completed/success 35/35**, including 28 Stage23, 25 Stage22, 25 Stage21, 25 Stage20a and 33 provenance fixtures; protected `main=f7eabfea74480d307b52d4b053730021efc95352` remained unchanged. Stage24 adds pure in-memory `tools/m3_2_chronology_navigation_reference.py`, 35 synthetic tests, Windows CI step, `docs/qualification/M3_2_READONLY_CHRONOLOGY_NAVIGATION.md` and continuity docs. Filtering by historical status, time kind, exact fictional calendar/revision, or literal case-insensitive label/window text is scoped to exactly one Universe and applied before paging. Cursors detect stale snapshot/filter/Universe and permit previous/next pages; they are NOT authentication. Source insertion order is display-only; edit controls false. No Rust/Tauri/React/SQLite runtime changes or operator file access. Real Stage18.1 isolated-v7 physical read-only audit PASS in its scope; global `PENDING_EXTERNAL_ATTESTATION` remains 21 historical SHA / 3 recent / 2 unanchored. Seven Windows worktrees, active restored M1.5 v6, M3.1 isolated v7 and ACL historic archives preserved. PR #35 DRAFT, no writer, normal migration 007, merge or M3.3.

## 2026-10-14 Stage 23 — synthetic read-only chronology pagination SOURCE CANDIDATE; exact-head CI pending

Stage22 exact source `4f291197adc9017310342e6af38000f6d5a920c7` obtained Windows PR CI #38599527966 terminal completed/success **34/34**, including 25 presentation, 25 projection, 25 correction and 33 provenance fixtures. Protected main remains `f7eabfea74480d307b52d4b053730021efc95352`, PR #35 OPEN/DRAFT/UNMERGED. Stage23 adds pure in-memory `tools/m3_2_chronology_pagination_reference.py`, 28 tests, CI, `docs/qualification/M3_2_READONLY_CHRONOLOGY_PAGINATION.md` and updates continuity. It pages by source insertion order (never world-time) 1..64 anchors per page, supports 513+ synthetic anchors without Stage22 512-count veto, preserves immutable IDs and correction lineage, rejects malformed/cross-Universe/stale cursors and never authorizes editing. Cursor is a consistency hint, NOT signature or access control. No UI, Rust, SQLite, network or operator execution. Real Stage18.1 isolated-v7 physical audit PASS only; overall PENDING_EXTERNAL_ATTESTATION (21 historic SHA / 3 observed / 2 unanchored) remains. Seven local worktrees, production restored v6, isolated v7 and ACL/backup history preserved. PR #35 DRAFT; no migration 007 normal startup, writer, merge or M3.3.

## 2026-10-14 Stage 22 — bounded synthetic chronology presentation DTO, CI pending

Stage 21 PR #35 exact HEAD `3bd899cc5876042ff57c3b8ab63fb91a6a40a2c9` passed Windows PR CI #38595478362 completed/success 33/33, including 25 Stage21 synthetic read-only projection tests, 25 Stage20a correction tests, 33 provenance tests and Rust/React. `main=f7eabfea74480d307b52d4b053730021efc95352` unchanged. This new Stage22 SOURCE CANDIDATE adds only `tools/m3_2_chronology_presentation_reference.py`, 25 synthetic tests, a single Windows CI step, `docs/qualification/M3_2_READONLY_CHRONOLOGY_PRESENTATION.md` and continuity updates. Frozen DTOs convey 1-Universe, immutable history/status, explicit human before/after/incomparable, and unavailable narration/reveal/editing, refusing more than 512 anchors/128 comparisons, malformed/duplicate/cross-Universe pairs. No Rust/React/UI/SQLite runtime operation, no operator commands. Real Stage18.1 isolated M3.1 v7 read-only physical audit PASS but overall PENDING_EXTERNAL_ATTESTATION (21 historical/3 recent/2 unanchored). Seven Windows worktrees, production v6, isolated v7, ACL/backups untouched. PR #35 remains DRAFT, no writer, production migration 007, merge or M3.3.

## 2026-10-14 Stage 21 — pure in-memory read-only world chronology projection SOURCE CANDIDATE

Stage 20a `a1c27c36fa5f48557ec1475fccf13577979d8d07` passed required exact-head Windows pull_request CI #38579592096 **32/32 terminal success**, including 25 synthetic append-only correction tests and 33 provenance fixtures. Protected main remained f7eabfea74480d307b52d4b053730021efc95352. Stage 21 adds only `tools/m3_2_chronology_projection_reference.py` and 25 new synthetic tests, CI step, and `docs/qualification/M3_2_READONLY_CHRONOLOGY_PROJECTION.md`. This model reads immutable Python tuples, scopes inspection to one Universe, exposes active/replaced/withdrawn and complete correction lineage, and computes before/after/same/incomparable ONLY from explicit source precedence links. No Gregorian comparison or implicit narration/reveal order; all editing flags remain false. It does NOT read SQLite/operator files or create runtime UI/IPC. New exact-head CI mandatory. Real Stage18.1 isolated-v7 physical PASS does not upgrade overall `PENDING_EXTERNAL_ATTESTATION` (21 historical, 3 recent observed, 2 unanchored). Seven operator worktrees, active restored-v6, isolated-v7, ACL/backups preserved; PR #35 DRAFT, no M3.2 writer, production 007, merge or M3.3.

## 2026-10-14 Stage 20a — synthetic test parser correction, NEW SHA CI PENDING

First Stage 20 candidate c75dd2c3842378be50aa17eeb8b85d212f743d84 failed exact-head Windows CI #38578661460 at its new pure-Python supersession suite. Logs show Python SyntaxError on test_m3_2_supersession_reference.py line 178: one missing closing parenthesis in the duplicate-anchor synthetic case. Twenty-four preceding Windows steps, including original provenance tests, succeeded; none of the 25 new supersession tests ran because import failed. This is a test-source typo, not SQLite corruption or a production operator failure. Stage 20a fixes only the missing closing parenthesis; a source-level bracket check returned balanced and all 25 tests remain. New exact-head Windows CI is mandatory. Stage 20 pure in-memory-only and documentary; seven operator worktrees, active v6, isolated v7 and ACL historic evidence untouched. PR #35 DRAFT, 21/3/2 historical classifications PENDING; no writer, migration 007, merge or M3.3.


## 2026-10-14 Stage 20 — append-only chronology correction SYNTHETIC SOURCE CANDIDATE (new CI pending)

Predecessor PR #35 e7e20e08f761b9f9d572b3580714ac9cdfe401c2 obtained required exact-head Windows CI #38570448347 terminal completed/success 31/31. Protected main remains f7eabfea74480d307b52d4b053730021efc95352. Operator Stage 18.1 real isolated v7 physical and custody read-only audit was successful only within its scope; M3.2 overall remains PENDING_EXTERNAL_ATTESTATION (21 historic SHA/3 recent observations/2 unanchored). Stage 20 adds ONLY tools/m3_2_supersession_reference.py (pure in-memory tuple model), 25 disposable synthetic Windows cases, and docs/qualification/M3_2_APPEND_ONLY_SUPERSESSION_DESIGN.md. Existing v7 triggers prohibit UPDATE/DELETE and check cycles across historical precedence rows; therefore proposed anchor rectification is append-only, conservative, forbidden for anchors with historical precedences, and no precedence/calendar corrections are claimed. New exact-head Windows pull_request CI required; no production or isolated SQLite/Tauri/React changes. Seven original local worktrees/ACL and historic backups preserved; PR #35 remains DRAFT, no migration 007 normal startup, M3.2 writer, merge or M3.3.

## 2026-10-14 Stage 19.1b ACCEPTED; M3.2 manual chronology UX planning contract SOURCE CANDIDATE

Protected main remains f7eabfea74480d307b52d4b053730021efc95352. PR #35 Stage 19.1b exact SHA 5839d3d23d04ee8bab8a7af1a7f50bb45582cf1a obtained terminal Windows pull_request CI #38506803238 completed/success 31/31 including 33 synthetic provenance input tests. The two earlier Stage 19.1 CI attempts remain FAILED. The operator previously passed the real isolated M3.1 v7 read-only physical audit (26/26 custody; 21 historic, 3 recent observed, 2 unanchored; integrity/FK/typed-v6 checksum and before/after v7 SHA). Overall M3.2 remains PENDING_EXTERNAL_ATTESTATION. A predecessor M3.1 PR #33 comment from October 11 documents that ACL archives were saved before scoped repair but DOES NOT independently pin their file SHA; no retrospective promotion is allowed. This candidate adds only docs/qualification/M3_2_MANUAL_CHRONOLOGY_UX_CONTRACT.md: prospective manual chronology world/narration/reveal separation, immutable v7 schema and correction limitations, 12 synthetic acceptance scenarios. No React/Rust/SQLite changes; new exact-head CI mandatory for documentary source. Existing seven operator worktrees, production v6, isolated v7 and ACL backups untouched. PR #35 remains DRAFT, no writer/migration/merge/M3.3.


## 2026-10-14 Stage 19.1b — narrowed worktree name guard (new CI PENDING)

Previous Stage 19.1a SHA `4ca1458c4b25473dc2e338656cdbabf3faf1db03` failed Windows CI #38506420793 because protected source prefix `fabulaxiom-m32-` also matched CI synthetic folder `fabulaxiom-m32-provenance-synthetic-*`. Stage 19.1b narrows veto to known worktree roles plus hex SHA, retaining app/ACL root and exact operator main protections, with 33 synthetic provenance tests. New exact-head CI mandatory. Seven local worktrees, SQLite and archived ACL evidence untouched; PR #35 remains DRAFT. No write authority.


## 2026-10-14 Stage 19.1a — correct Windows CI checkout basename false positive (NEW CI PENDING)

Stage-19.1 first candidate b72e2ebf78db80aaabaf921dd5b79455c53bfa46 FAILED Windows PR CI #38506053405 in provenance fixtures. Its blanket Fabulaxiom ancestor-name veto matched GitHub runner D:\\a\\Fabulaxiom\\Fabulaxiom, aborting synthetic file claims before parsing. Stage 19.1a limits the base-repo veto to exact operator M:\\Fabulaxiom, preserving named production/isolated/ACL roots and special M25/M31/M32 source prefixes. Synthetic suite expands 29→31 tests, including explicit GitHub checkout-name and operator main-root regression cases. No source-file authority promotion, no local operator execution, no v6/v7/ACL mutation. New exact-head CI required; PR #35 DRAFT and M3.3 blocked.

## 2026-10-14 Stage 19.1 — provenance JSON read-only intake hardening SOURCE CANDIDATE (CI PENDING)

Stage 19 exact GitHub source `3c237179396bafafd5c4733a5f6f3ae7a7355ac7` passed Windows CI #38503049446 **31/31**. Stage 18.1 real isolated-v7 physical audit already PASS in byte, integrity/FK, 7-ledger and corrected inherited v6 logical scope; overall still PENDING_EXTERNAL_ATTESTATION. Stage 19.1 protects external JSON claim intake by rejecting symlink/junction/reparse ancestors and known protected roots, using bounded double-read+file-metadata checks, strict duplicate-key/UTF-8/nonfinite JSON vetoes. Expands synthetic Windows claim tests **16→29**; no promotion of 3 recent or 2 unanchored roles and no signature/timestamp checks. NEW exact-head CI required. Seven local worktrees and all SQLite/ACL archives preserved. PR #35 DRAFT; production remains restored-active v6; no M3.2 writer or M3.3.

## 2026-10-14 Stage 19 — evidence provenance claim triage SOURCE CANDIDATE (CI pending)

Stage 18.1 fixed source exact SHA `f89d31fb69ba37378fb2b8eaeab806ca2d55029c` qualified Windows pull_request CI #38498919187 30/30. Operator's actual isolated M3.1 v7 physical read-only audit PASS: protected custody 26/26, historical pinned 21/21, observed 3/3, 2 unanchored; historical isolated V7 file SHA before/after MATCH, integrity_check+foreign_key_check PASS, 14 inherited strict and 3 empty candidate strict tables, 7 ledger migrations, projected 6-row V6 logical hash MATCH, no sidecars or local Git changes. Report STILL PENDING_EXTERNAL_ATTESTATION / exit 2, no production v6 SQLite connection or write. Documented in PR #35. Stage 19 introduces a separate synthetic-only CLI provenance CLAIM triage schema and 16 adversarial Windows tests. It cannot auto-upgrade 3 recent observations or 2 unanchored roles using self-supplied URLs, timestamps, custodian names or SHA hashes; output remains PENDING/FAIL only. NEW exact-head CI required; no local operator run. Original 7 worktrees and v6/v7 protected archives untouched, PR #35 DRAFT, no M3.3. See docs/qualification/M3_2_PROVENANCE_CLAIM_TRIAGE.md.


## 2026-10-14 Stage 18.1 — real isolated-v7 digest mismatch: source algorithm FIX CANDIDATE (new CI pending)

Operator actual stage-18 gate on HEAD de42f847003509ce19edee8ae68b0a77420b7be1 returned FAIL `isolated_v7_legacy_logical_digest_mismatch` / exit 2 **after** original v7 physical integrity/FK/strict-table checks, with original isolated file SHA same before/after, no SQLite sidecars, clean Git. Exact source defect: Stage-18 includes v7 ledger row 007 when rehashing historic v6 `schema_migrations` 6-row reference. Original M3.1 copier verifies first six rows separately and allows seventh. Stage 18.1 source correction hashes only first six migration rows by historical typed-v1 algorithm while keeping 7-row lineage; retains historic source SHA pins and all vetoes, +2 independent-oracle synthetic tests (18 total). New exact-head CI mandatory, no operator command yet, no local data repair, PR #35 DRAFT and M3.3 blocked. See docs/qualification/M3_2_ISOLATED_V7_PHYSICAL_READONLY.md.


## 2026-10-13 M3.2 Stage 18 — isolated M3.1 v7 physical read-only SOURCE CANDIDATE (new CI PENDING)

Stage 17 exact HEAD `281d6667b5d08ca0ab3217d24e650574bc70f2ca` passed required Windows CI #38421108816 29/29. Operator subsequently ran genuine source-anchored four-root custody: 26/26 roles, 21/21 historic pinned and 3/3 recent observed SHAs MATCH, 2 unanchored, Git source clean. Status remained PENDING_EXTERNAL_ATTESTATION, CLI exit 2. Stage 18 adds a **new source-only / synthetic CI** verifier for physical integrity of the **existing isolated M3.1 v7** SQLite copy: require previous 26-role live-custody gate before read-only mode=ro connection; SQLite header and no WAL/sidecar, separate integrity/FK, seven exact migration rows, 17 STRICT tables, v7 tables empty, old typed legacy logical SHA and file SHA/id before-after. Never opens production v6. New head CI mandatory; no operator command authorized. PR #35 DRAFT, M3.3 blocked. See `docs/qualification/M3_2_ISOLATED_V7_PHYSICAL_READONLY.md`.


## 2026-10-13 M3.2 Stage 17 — M1.5 activation inventory hardening (CI PENDING)

Stage 16 exact HEAD `fc1a25e411a0a22a337a5a2eb995f58a70ffff52` passed required Windows `pull_request` CI #38411230384, 29/29 SUCCESS. Stage 17 source candidate closes a gap where a second/newer M1.5 activation marker could change runtime selection while the old marker still passes SHA custody. It requires the exact sole expected activation marker both before and after the four-root scan. Synthetic tests expand 18 → 24, including actual SHA hashing of disposable fixture bytes. No change to production, Tauri, migrations or historical files. New exact-head CI required; real operator invocation remains unauthorized, output remains PENDING_EXTERNAL_ATTESTATION, PR #35 DRAFT and M3.3 blocked. See docs/qualification/M3_2_ACTIVATION_MARKER_INVENTORY.md.

## 2026-10-13 Stage 16 — manifest-free source-anchored four-root auditor (NEW CI PENDING)

Stage 15 exact HEAD `11fa03d6c58dd5d7fb42a2f4c12b40850503dca8` obtained required Windows `pull_request` CI #38408731334 completed/success, 28/28. Stage 16 source candidate adds a distinct read-only, manifest-free 26-role custody auditor with 18 disposable synthetic Windows tests. It uses 21 source-pinned historical digests, three recent-observation digests, two unanchored roles, and exact original M1.5/M2.5/M3.1/external ACL root identities; it never treats a newly generated operator SHA manifest as independent authority. Result can only be PENDING_EXTERNAL_ATTESTATION or FAIL, never READY/staging. New exact-head Windows CI required, and **no operator command yet authorized**. Production v6/ACL/backups unmodified; PR #35 DRAFT; M3.3 prohibited. See `docs/qualification/M3_2_DIRECT_READONLY_CUSTODY.md`.

## 2026-10-13 M3.2 Stage 15 — exact legacy-table and backup/restore cross-links (CI PENDING)

Stage 14 exact HEAD `612f0e40df4fcb2d4ea697205da82a0c0c39dbc0` passed required Windows `pull_request` CI #38340992280, 28/28 SUCCESS. Stage 15 source candidate tightens SHA-pinned M3.1 archival JSON claims: exact 14 v6 legacy table names from the existing audit authority, per-table backup/restore count equality, positive exact-integer byte-size equality for backup/restore/forced rollback, and boolean-as-integer veto. 21 synthetic tests in the existing CI step. No operator invocation, SQLite connection, runtime migration or staging. New exact-HEAD CI required. PR #35 OPEN/DRAFT, M3.3 blocked. See `docs/qualification/M3_2_M31_SEMANTIC_HARDENING.md`.

## 2026-10-13 M3.2 Stage 14 — archival M3.1 manifest semantics SOURCE CANDIDATE

Stage 13 HEAD 5e5d76141cbf7fbb69954beefe0acbfb822da6d0 passed required Windows pull_request CI #38339487476 completed/success 27/27. Stage 14 source adds SHA-pinned *semantic* checks of M3.1 v6 backup/restore, third v7, fourth rollback, isolated preparation and Tauri overlay, with 16 synthetic adversarial cases. This verifies JSON assertions and cross-hash lineage, **not fresh SQLite integrity or authoritative external ACL history**. New own-HEAD CI required. No operator command or write, status remains PENDING_EXTERNAL_ATTESTATION, PR #35 DRAFT and M3.3 blocked. See docs/qualification/M3_2_M31_SEMANTIC_READONLY_GATE.md.

## 2026-10-13 — M3.2 Stage 13 source-anchored custody policy (NEW CI PENDING)

Stage 12 at HEAD f839987c5b2a9c9581fd65aa4eb11bc575abc720 received required exact-head Windows pull_request CI #38318391796 completed/success, 26/26 steps. Stage 13 source candidate independently pins 21 historical reference SHA values, keeps 3 recent observations and 2 unanchored roles as OBSERVED, and refuses relabeling or path substitution. Output is strictly PENDING_EXTERNAL_ATTESTATION and never write authorization; no operator Windows command proposed. New SHA's CI must be accepted separately. Production M1.5 v6, M3.1 read-only, PR #35 DRAFT, M3.3 blocked. See docs/qualification/M3_2_INDEPENDENT_AUTHORITY_GATE.md.

## 2026-10-13 M3.2 stage 12 — multi-root read-only custody SOURCE CANDIDATE

Stage 11 exact SHA 2ed947f2d2c13c74e150054a7dfbeb5153186134 Windows CI #38294992362 completed/success 25/25. Operator subsequently confirmed 11/11 M3.1 file SHA, named M2.4 duplicate-content backups, M2.5 and app snapshots, and current isolated M3.1 root+descendant ACLs. Archived ACL digests and early M2.4 manifest are recent-observation-only. Stage 12 adds separate four-root fail-closed read-only custody source and synthetic Windows tests; NO operator call, staging, SQLite, IPC or production mutation. New exact-HEAD CI required. PR #35 DRAFT, M3.3 blocked. See docs/qualification/M3_2_MULTIROOT_READONLY_GATE.md.

## 2026-10-12 M3.2 stage 11 — Windows post-restart read-only custody gate (candidate)

Stage-10 exact HEAD `4d3f571443ed31105b351ee0e0427efc20bf569e` passed Windows required CI #38293132998, 24/24 SUCCESS. New stage-11 `tools/m3_2_operator_readonly_gate.py` supports **--dry-run ONLY** with standard/medium Windows token, exact Git head/origin-main, clean worktree, protected pre-recorded SHA manifest, safe paths/no junctions, and unused M3.2 identity; creates zero files and never opens SQLite. Synthetic Windows fixture tests + CI step added. New exact-head CI must pass. PR #35 remains DRAFT/unmerged, M1.5 production v6 and backups untouched; no M3.2 write IPC or M3.3. See `docs/qualification/M3_2_POST_RESTART_GATE.md`.

## 2026-10-12 — M3.2 stage 10 debug-only isolated preflight; NEW CI pending

Stage 9 exact head `d1a14aeb0703a9eb0c225ecd89be2a56d4b8b7c8` passed [Windows CI #38269738499](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/38269738499) **completed/success, 23/23 steps**. M3.2 stage 10 proposes a **separate, opt-in, debug-only** preflight-only Tauri feature, unique M3.2 identity with explicit ACK, and exactly one status IPC registered via both invoke_handler and feature-specific build-time AppManifest. It performs **ZERO writes, ZERO SQLite/production reads** and is not mounted or operator launched. No existing normal or M3.1 preview IPC changes. Exact-head CI required. PR #35 still OPEN/DRAFT; M1.5 production v6 and protected backups untouched. M3.3 unauthorized. See `docs/qualification/M3_2_ISOLATED_IPC_PREFLIGHT.md`.

## 2026-10-12 — M3.2 stage 9 independent SQLite connections, pending exact-head CI

Stage-8 `eb9f6486567fdcb65ba5556b2861593c7b18bca0` has **terminal required Windows CI #38263839166 23/23 PASS**. New stage-9 test-only scratch SQLite file (NOT operator data) verifies two separate WAL connections, committed-only read visibility, serialized writers, atomic correction withdrawal/replacement rollback and commit, UNIQUE fork veto, raw-v7 cycle-bypass veto and read-only `query_only` refusal. Exact-head CI is not yet accepted. Normal runtime remains v6, M1.5 restored-active activation untouched, no new Tauri IPC. PR #35 OPEN/DRAFT, M3.3 unauthorized.

## 2026-10-12 — M3.2 stage 8 generic immutable correction chain, new CI pending

Stage-7 exact source `31e2078cfeedf5f0d755fc0fc0c940685d3cb4f0` obtained terminal required Windows CI #38262070398 23/23 PASS. New stage-8 candidate adds test-only unlimited-depth linear correction-chain lineage (STRICT immutable nodes and withdrawals), current active-graph projection and cycle guards; no production IPC, data access or migrations. Exact-head CI still required. PR #35 remains OPEN/DRAFT/UNMERGED, M3.3 unauthorized. M1.5 restored production v6 and backup custody untouched. Detailed gate: `docs/qualification/M3_2_MANUAL_CHRONOLOGY_STAGE1.md`.

## 2026-10-12 — M3.2 stage 7: successor withdrawal candidate, exact-head CI pending

Stage-6 `4119fc5b5a49a84fc05a3770cc57216e7638c603` is qualified by Windows #38259258644, 23/23 SUCCESS. New test-only STRICT append-only successor-withdrawal decision, refreshed active-graph view, Rust auditable listing and same-Universe/custody tests are proposed at current PR #35 HEAD; qualify with its own CI. No arbitrary edit chain, operator writable app or migration 007. M3.2 remains OPEN/DRAFT; normal application remains restored-active v6 and M1.5 unchanged. See stage 7 in `docs/qualification/M3_2_MANUAL_CHRONOLOGY_STAGE1.md`.

## 2026-10-12 M3.2 stage 6 — one-generation correction successor, pending CI

Previous M3.2 stage-5 exact HEAD `7cd198493b32645025d7a34ca30735d2ef99579e` passed Windows PR CI #38200842678 23/23 SUCCESS. New test-only SQLite candidate and Rust service add one immutable successor after explicitly withdrawn initial restatement, plus shared active-graph view and incoming raw/initial-restatement graph guards. One successor per withdrawn first correction, **no recursive authoring**, production IPC or schema activation. New HEAD CI is required. M3.2 PR #35 DRAFT; M3.3 blocked. Production M1.5 restored-active v6 unchanged.

## 2026-10-12 M3.2 stage 5: second-order restatement withdrawal, candidate

Stage-4 guarded active graph at HEAD `dc2fa5b2cbcb4d91b8c3d3e26a30e27093534cdd` passed exact-head PR CI #38199955357 **completed/success** (23 Windows steps). New stage-5 `#[cfg(test)]` SQLite/Rust-only restatement revocation design retains legacy and corrected assertions but removes a withdrawn correction from the active projection; immutable per-Universe provenance, duplicate veto and audit history included. The new HEAD requires its own CI and remains DRAFT. Re-authoring after restatement withdrawal is intentionally unavailable until a governed version-chain/active-graph redesign; **do not claim complete M3.2 CRUD**. Normal Windows application remains v6 and M1.5 unchanged, with no new Tauri IPC or operator data writes. M3.3 unauthorized.

## 2026-10-12 — M3.2 stage 4 active precedence restatements (candidate)

Stage-3 preview HEAD `ecdf04627bdb40fc948b1b7c7f2d3abec57952b0` obtained exact-head CI #38199285576 SUCCESS. New stage-4 source models **test-only** current partial-order corrections in a separate append-only restatement table after explicit human revocation of original legacy edge, while preserving the original v7 immutable historical row. SQL cycle/backdoor/Universe guards act on combined active graph. Rust tests in memory; no new normal/M3.1 IPC, production v7 migration, or local operator mutation. This head is **not** qualified until fresh CI success. Full restatement lifecycle, isolated writable M3.2 Tauri UX and Windows operator gate remain pending. See `docs/qualification/M3_2_MANUAL_CHRONOLOGY_STAGE1.md`. M3.2 PR #35 remains DRAFT; M3.3 unauthorized.

## 2026-10-12 M3.2 stage 3: separate coordinate UI prototype, no runtime mount

Stage-2 isolated append-only decision schema/Rust contract HEAD `27b4c60b8c304dd29bdf7c1f03efa2cd3c6b7551` was **CI #38198727275 completed/success, 23/23 Windows steps**. New stage-3 React read-only projection is **not mounted** in the application; three separate panels represent fictional world-time assertion, narration order by manuscript, and reader reveal explicitly unavailable. Fail-closed source-scope validation and React static tests added; new HEAD CI pending. No M1.5, production v6, normal/M3.1 preview IPC, release, or local operator artifact changed. M3.2 remains DRAFT.

## 2026-10-12 M3.2 stage 2: append-only correction candidate; CI pending

M3.1 remains **COMPLETE + MERGED + NORMALIZED**. M3.2 stage-1 head `690656bcd9c148ac7737749cfb6d2a7350df1c7a` completed successful exact-head PR CI #38190352570. New stage-2 candidate adds **test-only**, in-memory decision tables for authored revocation/supersession with immutable history and atomic replacement, not production migrations or GUI/IPC. Old M3.1 precedence cycle guard still blocks historical reverse-edge conflicts even after an edge is revoked; do not claim this candidate offers complete editable chronology. Await new exact-head CI and active-graph policy. Production restored-active v6, M1.5 marker, backups and existing Tauri M3.1 preview unchanged. PR #35 still DRAFT; M3.3+ unauthorized.

## 2026-10-12 — M3.1 COMPLETE + MERGED + NORMALIZED; M3.2 first-stage work authorized

Independent PR #34 had exact-head `pull_request` CI #38178342603 `completed/success` on `34b85316b6520d24e0361a86b49b27f25c6f76e2`, then SHA-guarded merge `f7eabfea74480d307b52d4b053730021efc95352`. Live re-fetch verified `main`, merged PR and strict `Protect main` ruleset. Therefore **M3.1 COMPLETE + MERGED + NORMALIZED** for its bounded candidate schema and controlled isolated v7 read-only launch, not for production v7 activation.

**Current authorized stage: M3.2** — only isolated test-first manual chronology foundation under dedicated branch and draft PR. `src-tauri/src/m32_manual_chronology.rs` remains `#[cfg(test)]` (zero new production IPC and no normal migration). UI/persistent isolated runtime, supersession and Windows operator qualification still pending. Production M1.5 restored-active SQLite v6, backups and activation marker are untouched. See `docs/qualification/M3_2_MANUAL_CHRONOLOGY_STAGE1.md`.

The older M3.1 normalization-pending paragraphs below are historical and superseded.

## Current authority — M3.1 implementation merged; independent normalization pending (2026-10-11)

- **Repository visibility: PUBLIC**, `main` genuinely branch-protected by active repository ruleset [Protect main](https://github.com/LaurentCOLL1/Fabulaxiom/rules/24895490). Rules include deletion/force-push denial, pull request and strict exact-app GitHub Actions check `Windows frontend and Rust checks` (app 15368), with no bypass actors or mandatory external approval (solo developer).
- Implementation PR [#33](https://github.com/LaurentCOLL1/Fabulaxiom/pull/33) **MERGED**, final head `796a4b65e596b9bc05bd00b523b3209f9736524d`, strict required-check [CI #38176139985 attempt 3](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/38176139985) **completed/success** (23 Windows job steps SUCCESS). Guarded implementation merge: `922d155d4f4321ed8b90955d4ea96388751f0daf`; fresh `main` re-fetch confirmed.
- Actual Windows isolated v7 GUI and read-only IPC **PASS** on operator-qualified source `4d520e1825ecd08d20484b0e72d60ffe6ea09e4c`; after controlled exit, **11/11** original and isolated SHA-256 preserved, M1.5 restored-active production v6 marker unchanged, no SQLite sidecars. Second launch worked in medium-integrity standard Windows token after approved, individually backed-up user-SID-only ACL adjustment to existing isolated Tauri identity. No live executable path/PID snapshot was obtained; avoid asserting it.
- PR #33 adds prevention for future elevated Windows `--prepare`, tested with synthetic fail-closed fixtures and a real no-staging Win32 token API smoke check. Normal runtime SQLite remains **v6**, `007` is not in automatic migrations. **A successful isolated preview is not a production v7 migration**.
- **This separate normalization PR is documentary only**, must obtain its OWN terminal exact-head `pull_request` CI and protected SHA-guarded merge. Until then M3.1 is **IMPLEMENTATION MERGED / NORMALIZATION PENDING** and M3.2 remains unauthorized. Detailed gate: `docs/qualification/M3_1_POST_MERGE_NORMALIZATION.md`.

Historical checkpoints below are preserved for audit and must not override this authority.

## Current M3.1 candidate checkpoint (PR #33; not merged)

On Windows (2026-10-11), actual isolated debug-only v7 Tauri GUI and read-only diagnostic IPC **PASS**, then 11/11 protected bytes and restored-active v6 M1.5 pointer **PASS after closure** at qualified operator head `4d520e1825ecd08d20484b0e72d60ffe6ea09e4c`, CI #38160997846 success. The initial WebView2 failure was due to restrictive NTFS access to an elevated-operator-prepared identity; the old ACL was backed up and only the isolated root was granted current-user Modify, with medium-integrity requalification. Detailed evidence: `docs/qualification/M3_1_WINDOWS_OPERATOR_EVIDENCE.md`.

The current PR adds a fail-closed Windows elevated-token guard before any NEW isolated `--prepare`, while leaving the existing qualified identity untouched. Its newer HEAD and CI must be verified **separately**. Earlier milestone notes below are historical main checkpoints, not assertions that M3.1 is merged. **No production v7 migration or 007 automatic migration; M3.1 not yet COMPLETE + MERGED + NORMALIZED; M3.2 unauthorized.**

## Repository

- Repository: `LaurentCOLL1/Fabulaxiom`
- Visibility: **public**
- Default branch: `main`

## Milestone state

### M0 — Environment and architecture qualification

**COMPLETE + MERGED + NORMALIZED**

### M1 — Persistence and project foundation

**COMPLETE + MERGED + NORMALIZED**

#### M1.1 — SQLite foundation and migration runner

**COMPLETE + MERGED + NORMALIZED**

Final normalization merge:

`d99da744fc04303c0c094a8aa6a2daab9983136f`

#### M1.2 — Project hierarchy schema

**COMPLETE + MERGED + NORMALIZED**

Implementation PR:

**#9 — feat: implement M1.2 project hierarchy schema**

Implementation merge:

`91b80e529679d3bc407b5f6ca49e578d86de1d44`

Qualified implementation SHA:

`3d4b2eaf95e13bfa93580a4295ac20e93a076798`

Qualification evidence commit:

`0da679859c77ef231c6b33e9e91c7264c8d7b5f6`

Deterministic exact-head CI:

- workflow: `Fabulaxiom CI`;
- terminal run: `37646868694`;
- result: `completed/success`;
- frontend tests/build: PASS;
- Rust tests: 13/13 PASS;
- `cargo check --locked`: PASS;
- dependency lockfiles unchanged.

Windows production migration qualification:

- schema-v1 production database detected;
- pre-migration SQLite backup created;
- migration v1 → v2: PASS;
- migrations 1 and 2 present exactly once;
- hierarchy tables 5/5 present;
- SQLite STRICT 5/5;
- immutable-ID triggers 5/5;
- foreign keys ON;
- `PRAGMA foreign_key_check`: empty;
- `PRAGMA integrity_check`: `ok`;
- Rust bridge: PASS;
- database status: PASS;
- Ollama local status: PASS;
- worktree clean.

Detailed evidence:

`docs/qualification/M1_2_PROJECT_HIERARCHY_SCHEMA.md`

#### M1.3 — No-AI CRUD service

**COMPLETE + MERGED + NORMALIZED**

Implementation PR:

**#11 — feat: implement M1.3 no-AI CRUD service**

Implementation merge:

`49424f1ecafa1be3c4f47b806231b6644e9c73a4`

Qualified implementation SHA:

`6259bd3b4759b683bf4bb7c2c6efdf693ddfebac`

Qualification evidence commit:

`d9df8151b0c3336e0a12c65a7ba7841cab4e091b`

Terminal exact-head CI:

- workflow: `Fabulaxiom CI`;
- run: `37684422252`;
- result: `completed/success`;
- frontend tests: 8/8 PASS;
- frontend build: PASS;
- Rust tests: 20/20 PASS;
- `cargo check --locked`: PASS;
- dependency lockfiles unchanged.

Windows no-AI CRUD qualification:

- exact implementation source and clean worktree: PASS;
- Ollama process absent and loopback API inaccessible;
- local frontend tests/build: PASS;
- local Rust tests/check: PASS;
- Rust bridge: PASS;
- SQLite schema v2 / foreign keys ON: PASS;
- Ollama status expected unavailable;
- full Universe / Series / Novel / Chapter / Scene CRUD: PASS;
- optional-Series workflow: PASS;
- deterministic reorder: PASS;
- rename at every hierarchy level: PASS;
- cross-Universe Series protection: PASS;
- parent deletion guards with `has_children`: PASS;
- CRUD remained operational with Ollama stopped;
- qualification data cleanup: PASS;
- `PRAGMA foreign_key_check`: empty;
- `PRAGMA integrity_check`: `ok`;
- final worktree clean;
- Ollama remained stopped.

Detailed evidence:

`docs/qualification/M1_3_NO_AI_CRUD_SERVICE.md`

Delivered M1.3 foundation:

- Rust application models/DTOs separate from SQLite rows;
- CRUD service for all five hierarchy levels;
- explicit transaction boundaries for compound mutations;
- deterministic application/Tauri error payloads;
- thin Tauri commands;
- React hierarchy CRUD workspace;
- no Ollama dependency for CRUD;
- preserved M1.1/M1.2 persistence guarantees.

#### M1.4 — Text revisions and provenance foundation

**COMPLETE + MERGED + NORMALIZED**

Implementation PR:

**#13 — feat: implement M1.4 text revisions and provenance foundation**

Implementation merge:

`75ab73b176b481f64b0e7f8c510b4ede0c617e31`

Qualified implementation SHA:

`d62fe92e4c01e5a58a6fbf85bdcf465267b41ea6`

Windows qualification evidence commit:

`e6b3bf13399604a3b4922f9510a1c6761d9e5775`

Terminal exact-head CI:

- workflow: `Fabulaxiom CI`;
- run: `37709917550`;
- result: `completed/success`;
- frontend tests: 10/10 PASS;
- Rust tests: 29/29 PASS;
- frontend build and `cargo check --locked`: PASS;
- lockfiles unchanged.

Windows qualification:

- source exact, worktree clean, Ollama stopped;
- production SQLite schema v2 backed up via SQLite Backup API; SHA256 preserved;
- production migration v2 → v3 PASS;
- two `STRICT` revision tables and three migrations present;
- immutable append-only scene text revisions, lineage and current pointer;
- operator-reported create v1/v2, restore v1 and save v3 scenario PASS;
- persisted three revisions, one current head;
- `PRAGMA foreign_key_check`: empty;
- `PRAGMA integrity_check`: `ok`;
- Ollama remained stopped through qualification.

Detailed evidence:

`docs/qualification/M1_4_TEXT_REVISIONS_PROVENANCE.md`

Delivered M1.4 foundation:

- schema v3 for scene text revisions and explicit current heads;
- immutable revision IDs, database timestamps and per-scene revision ordering;
- parent revision provenance;
- transactional creation and pointer changes;
- guarded scene deletion with existing revision history;
- Rust/Tauri revision commands and React editor/history;
- no dependency on Ollama.

#### M1.5 — Backup and restore baseline

**COMPLETE + MERGED + NORMALIZED**

Implementation PR: **#15 — feat: implement M1.5 safe SQLite backup and restore baseline**

Implementation merge:

`282b325fb6c588a70df08a5128415c8fa0a0f72e`

Windows-qualified implementation SHA:

`7f968075f632843144c9833f61cc51910b538530`

Windows qualification evidence commit:

`152b40e616f40799abc61f9ce8db142e3b19340b`

Terminal exact-head CI:

- workflow: `Fabulaxiom CI`;
- run: `37720676744`;
- result: `completed/success`;
- frontend tests: 13/13 PASS;
- Rust tests: 37/37 PASS;
- frontend production build: PASS;
- `cargo check --locked`: PASS;
- dependency lockfiles unchanged.

Windows qualification:

- exact main/PR HEAD and local worktree clean: PASS;
- SQLite schema v3 and Tauri/Rust bridge PASS;
- Ollama unavailable as intended;
- application-created verified backup: PASS;
- UI-confirmed restore and reload: PASS;
- 1 Universe, 1 Novel, 1 Scene, 3 revisions, 1 current revision head preserved;
- previous active database is not overwritten by the restore design;
- operator historic backups are preserved;
- actual restored database path and independent post-restore integrity PRAGMAs were not supplied as evidence;
- three nonfatal Rust unused-code warnings remain tracked.

Detailed evidence:

`docs/qualification/M1_5_BACKUP_RESTORE_BASELINE.md`

Delivered:

- SQLite-consistent `VACUUM INTO` snapshot to app-owned unique backup files;
- schema owner, migration and integrity validation;
- new non-overwriting database file for restore;
- durable activation marker and old database preservation;
- deterministic Rust/Tauri errors and explicit restore confirmation;
- React backup/list/restore controls without Ollama;
- source preservation, failure and backup/restore automated tests.

### M1 closure

M1.1–M1.5 are all **COMPLETE + MERGED + NORMALIZED**. M1's database, hierarchy, revision history and backup/restore baseline are delivered and qualified. This is **not** a declaration that V1 as a whole is complete.

### M2 — Narrative entities and canonical facts

**COMPLETE + MERGED + NORMALIZED** — M2.5 independent normalization PR #30 protected-merged at `f13b4f8c249866ff60a19d7895b6cfaede56398a` after its exact-head CI #38041908126 (13/13 Windows job steps SUCCESS). M2 is closed; M3 has not been implemented or authorized.

Detailed planning PR #17 merged at `4a9115ec362a0efae696ebc94b5101fa46d7a03a`.

Accepted roadmap: `docs/roadmap/M2_NARRATIVE_ENTITIES_CANONICAL_FACTS.md`.

#### M2.1 — Entity registry schema and migration

**COMPLETE + MERGED + NORMALIZED**

Implementation PR: **#20 — feat: implement M2.1 narrative entity registry schema v4**.

Implementation merge:

`6c58b3bd4f0588436da8ba45adb875f897f426b2`

Qualified implementation SHA:

`c7a663d88ba2538714d42fdd366719cd54fe6f70`

Windows qualification evidence SHA:

`88fa3b22904b92d4ecdcb32ed7fd01dc23e24a4c`

Terminal exact-head CI:

- workflow: `Fabulaxiom CI`;
- run: `37814949619`;
- `completed/success`;
- frontend 13/13, Rust 44/44 tests PASS;
- frontend build, `cargo check --locked` and lockfile check PASS.

Windows production schema-v3 → schema-v4 qualification:

- actual restored active database resolved from M1.5 activation marker, not assumed default;
- source and backup verified before migration, backup SHA256 preserved;
- migration v4 applied by Tauri, four migrations recorded exactly once;
- both new narrative registry/alias tables STRICT;
- four immutable-identity triggers, two indexes;
- six narrative kinds constrained at schema level;
- existing hierarchy, metadata, revision and current-head rows unchanged in logical value;
- three scene text revisions and one current revision head preserved;
- `PRAGMA foreign_key_check` empty and `PRAGMA integrity_check` `ok`;
- no Ollama dependency; final worktree CLEAN;
- original backup and active activation marker unchanged.

Detailed evidence:

`docs/qualification/M2_1_ENTITY_REGISTRY_SCHEMA.md`

Delivered M2.1 scope:
- SQLite schema v4 for Universe-scoped narrative entity registry and aliases;
- immutable IDs, entity kind and Universe ownership; FK restrictions/indexes;
- M1.5 v3/v4 backup and safe legacy-v3 restore compatibility;
- deterministic regression tests;
- **no** entity CRUD UI, fact/canon engine, image/ComfyUI code.

#### M2.2 — No-AI entity and alias CRUD

**COMPLETE + MERGED + NORMALIZED** — normalized after independent post-merge PR acceptance.

Implementation PR: **#23 — feat: implement M2.2 no-AI narrative entity and alias CRUD**.

- Original base `main`: `70beb4f998ba3e587533dd7a90689eadeae4f4c3`.
- Windows-qualified code source: `b54fffd8e1f0224372e3b99cee07cb6df3203973`.
- Targeted React alias crash fix: synchronous `currentTarget.value` capture, per-entity alias drafts, IPC response validation and scoped render error boundary.
- Source-head `Fabulaxiom CI`: `37831790345`, `completed/success`.
- Operator Windows evidence commit: `a96870f823f24cb8962c9b0f43336ccb883ad5c3`.
- Evidence exact-head `Fabulaxiom CI`: run `37864503602`, event `pull_request`, `completed/success`; Windows job and every step successful.
- Protected implementation merge PR #23: `ad7211fa2f292b8bd9812e299dbb6be96214eb89`, with expected head SHA `a96870f823f24cb8962c9b0f43336ccb883ad5c3`.
- The separate normalization PR must have terminal exact-head CI and be merged before this normalized status takes effect.

Real Windows acceptance on qualified source:

- `npm ci`, frontend **21/21** tests, frontend build, Rust **51/51** tests, `cargo check --locked`, lockfile checks: PASS; worktree CLEAN.
- **13/13 operator interactive cases PASS**: six kinds, create/add/rename/delete alias, duplicate rejection, per-entity drafts, same-name distinct character identities, restrictive parent deletion, remaining modules visible with Ollama OFF.
- Actual restored SQLite database resolved through M1.5 active marker, not assumed default.
- Postinteractive schema v4, four migrations, two STRICT tables, four immutable-identity triggers, required indexes, `foreign_key_check=[]`, `integrity_check=ok`: PASS.
- Postinteractive 9 narrative entities and 8 aliases preserved; two same-name character rows have distinct IDs; 3 immutable scene text revisions and 1 current pointer unchanged, with matching pre/post SHA-256 digests.
- Historical pre-M2.1 operator backup SHA-256 preserved; no local database or backup cleanup or restoration performed.
- Nonfatal Rust warnings remain deferred to a separately qualified change.

Detailed evidence: `docs/qualification/M2_2_ENTITY_ALIAS_CRUD.md`.

Delivered M2.2: Rust/Tauri/React no-AI CRUD for six Universe-scoped narrative entity kinds and owner-scoped aliases, deterministic validation/negative paths, stable identity and restrictive deletion. No canon/facts, chronology, search, AI-writing or visual/ComfyUI implementation.

#### M2.3 — Fact registry and exact revision provenance

**COMPLETE + MERGED + NORMALIZED — effective after the independent M2.3 normalization PR passes exact-head CI and is merged.**

Implementation PR #25; Windows-qualified source `4d3b4b6015d477c3a6a5c3750d9743174e9c44a7`; qualification evidence commit `b015f7df80f38d75375a0e2615fd62d4c40ee1b8`; implementation merge on `main` `e6e80c26316f11054348a18a235fd08c600e136e`.

- Exact-source CI `37879358744` and exact-evidence-head CI `37961014980`: both `completed/success`, all Windows job steps PASS.
- Operator Windows local build/tests **21/21 frontend and 61/61 Rust PASS**, Rust check locked and dependency locks unchanged; UI **8/8 PASS**, Ollama OFF.
- Controlled additive SQLite v4→v5 on actual restored-active DB only after verified non-overwriting v4 operator backup SHA256 `c624241080d6e820398cc502b4db206fcaba457405083ce806c302a6ce464976`.
- Read-only postmigration audit **PASS**: migrations 1–5, fact/source STRICT schema, required triggers and indexes, `foreign_key_check=[]` / `integrity_check=ok`; all historical table contents/digests and both historical backup custodial hashes preserved.
- Nine original entities and eight aliases, homonymous character distinct IDs, three immutable scene revisions and current pointer retained exactly. New fact/source tables empty as expected prior to API use.
- Delivered local Rust/Tauri structured fact create/read/list with explicit sourced/unsourced provenance, immutable Scene revision anchors, checked UTF-8 byte spans, same-Universe guards and atomic rollback; **no React fact-entry UI**, canon status/review, AI extraction or ComfyUI implementation.
- Detailed evidence: `docs/qualification/M2_3_IMPLEMENTATION_GATE.md`.

#### M2.4 — Canon status and human review service

**COMPLETE + MERGED + NORMALIZED — effective only after the independent M2.4 normalization PR completes its exact-HEAD CI and protected merge.**

Implementation PR #27 merged into `main` at `3a069572d00e1680c42b0f13b800e28687c5f0eb`; qualified source HEAD `aad56bd59fdb87be5ac1eda99b1969452bf61a26`, qualification evidence HEAD `b53405779b04c16525ba48a266bd096096af7020`. Exact source `Fabulaxiom CI` run `37974831473` and evidence-HEAD run `37989040863`: both terminal SUCCESS, 13/13 Windows steps. Source qualification: 21/21 React, 71/71 Rust; operator real Windows reviewed 8/8 isolated Rust tests plus 8/8 existing-UI non-regression checks, Ollama OFF.

Delivered SQLite **v6**, STRICT append-only `fact_review_events`, explicit seven-state review service via Rust/Tauri, `draft` default, deterministic status transitions, durable audit history, optimistic revision guards, cross-Universe FK, explicit approval and revocation confirmation. Human reviewer name is **self-declared, not authenticated**; no silent AI promotion.

Real restored-active Windows v5→v6 migration occurred **only after** separate non-overwriting consistent pre-v6 v5 backup SHA-256 `db02961d7a30c6a6522bd52faeab8ceb09e26c1a4a6a58be467d142806e22fee`, with older backups intact. Independent read-only postmigration audit of six migrations, STRICT/triggers/indexes, integrity and foreign keys, every previous table digest, nine entities/eight aliases, three scene revisions and one current head: PASS. Isolated Windows Rust review tests **8/8 PASS** with production v6 SQLite logical snapshot unchanged before/after (`67dfd9194ff884762bbffaa39d774df10fadcd74cbc9e6774e36d323e4506fc6`). No production facts or review events inserted.

**Not delivered:** a dedicated React fact/review UI, end-to-end fact-review IPC GUI acceptance, authenticated reviewer identity, AI fact extraction, or ComfyUI. Detailed evidence: `docs/qualification/M2_4_CANON_REVIEW_IMPLEMENTATION_GATE.md`. Existing PR and governance are not authorization to implement the next subdivision before this independent normalization merges.

#### M2.5 — Usable sourced-facts and human review UI

**COMPLETE + MERGED + NORMALIZED.** Implementation PR #29 and independent normalization PR #30 are both protected-merged; the latter passed exact-head `pull_request` CI #38041908126 (13/13 steps).

- Implementation PR **#29** protected-merged on `main` at `f1e7ea99d26ad3390c7c47bfb339f26d730a44f1` from **exact evidence HEAD** `6f55fc3fc7eab6f2288a54619c0bef70e521f47e`. `Fabulaxiom CI` run **38040227617**, event `pull_request`, `completed/success`, **13/13** Windows steps, frontend **32/32**, Rust **72/72**, frontend build, `cargo check --locked`, locks unchanged.
- Qualified implementation source `7eaaf45ae164c9336df7e01c9da6787e4971d59e`, exact-source CI **38017441504** `completed/success`. Windows operator qualified: 8/8 hierarchy fixture actions; 8/8 corrected cross-workspace refreshing (`Aucun univers` blocker fixed); 9/9 sourced/unsourced fact UI cases; 10/10 human-review interaction checklist with no Ollama.
- Read-only SQLite v6 source/provenance/human-review audit: **3 facts / 2 source anchors / 11 immutable review events**, 8+2+1 contiguous review histories, explicit canon approval and revocation, no fabricated source, Unicode citation byte spans `[0,10)` and `[51,66)`, persisted three statuses `draft`, `suggestion`, `unknown`. Corrected mistaken 10-event script expectation: do not delete an actual event.
- Isolated Tauri `com.fabulaxiom.m25qual35fb842c` production-separated v6 test database; operator existing records preserved. Production restored-active v6 snapshot SHA256 `67dfd9194ff884762bbffaa39d774df10fadcd74cbc9e6774e36d323e4506fc6` unchanged. Isolated final logical digest `cff8a04f29ec60757c02ef9ed186be40c806cfcc6a2cfd11fa8072be44f273cb`; isolated pre-fact backup SHA256 `9e738d58519e1a0e3c1750d71726b661132fcbc0211fddea3178f6314bbfc7cf` retained; historical pre-M2.1/v4/v5 backups all hash-verified. An earlier v4 SHA mismatch in a PowerShell script was refuted by independent hashing plus v4 manifest/SQLite integrity, not a corrupted backup.
- New isolated React fact workspace with independent error boundary, Universe/entity and revision synchronization, exact historical UTF-8 citations, optional fictional validity, distinct seven statuses and human-only approval/revocation with append-only review history. Human reviewer label remains **self-declared, not authenticated**. No automatic canon promotion, no cloud or Ollama requirement, no migration after v6.
- Detailed acceptance: `docs/qualification/M2_5_SOURCED_FACTS_REVIEW_UI.md`; independent normalization: `docs/qualification/M2_5_POST_MERGE_NORMALIZATION.md`.

### M2 milestone closure boundary

**M2.1–M2.5 and M2 milestone COMPLETE + MERGED + NORMALIZED** after protected PR #30 merge `f13b4f8c249866ff60a19d7895b6cfaede56398a`, exact normalization CI #38041908126 SUCCESS. This is NOT V1 completion and it does NOT authorize M3 implementation. Next: independently evaluate the proposed bounded M3 roadmap in `docs/roadmap/M3_TIME_KNOWLEDGE_RELATIONSHIPS.md` through a separate planning PR and a separate planning normalization gate. ComfyUI imagery remains an unimplemented proposal (issue #19).

### M3 — Time, knowledge and relationships: planning merged, normalization gate pending

Planning PR **#31** merged with `expected_head_sha=5127ced6c5e175b0919c736c658036382794487e` at `main=68db746754e01b441870e0653f17f10ebfc7be2f`. Its exact-head `pull_request` CI run **38050865413** completed/success (one Windows job, 13/13 steps). Six documentary files only; no M3 code, SQLite v7, dependency or lockfile modification. The accepted proposed divisions are **M3.1** world-time schema, **M3.2** manual chronology UX, **M3.3** directional relationship history, **M3.4** character beliefs/knowledge, **M3.5** narrator/reader reveals, **M3.6** evolving narrative state. Detailed roadmap: `docs/roadmap/M3_TIME_KNOWLEDGE_RELATIONSHIPS.md`.

**Normalization condition:** the plan is `ACCEPTED + MERGED + NORMALIZED` **only after** an independent post-planning normalization PR passes a new terminal exact-head CI and SHA-guarded merge, then `main` is re-fetched. At that point authorize **M3.1 only**, using its own PR and required pre-v7 SQLite backup/Windows qualification; do not authorize M3.2+, AI, ComfyUI or production migration simply from planning. Evidence: `docs/qualification/M3_PLANNING_POST_MERGE_NORMALIZATION.md`.

**GitHub enforcement distinction:** branch API currently reports `main.protected=false`; `expected_head_sha` prevents merging an unexpected PR head but does not create formal branch protection. No change to historical M2 backups, production M1.5 active database, test fixture SQLite v6 or preserved review history is involved in planning.

## Reproducibility contract

- `package-lock.json` committed;
- `src-tauri/Cargo.lock` committed;
- CI uses `npm ci`;
- Rust CI uses Cargo `--locked`;
- dependency-lock mutation is rejected in CI.

## Governance rule

Every subdivision must:

- begin from freshly fetched live `main`;
- use a dedicated branch and pull request;
- preserve deterministic dependency locks;
- pass exact-head CI;
- receive Windows operator qualification when local behavior is part of acceptance;
- be merged and normalized before a dependent subdivision begins.
