# M3.2 — Manual Chronology and Ordering UX: Stage 1 Service Contract

**CURRENT STATE: IMPLEMENTATION CANDIDATE / DRAFT PR.** Do not confuse these isolated domain tests with an operator-accepted Windows GUI, a complete CRUD interface, or authorization for production v7 migration.

## Authorization verified before stage 1

- Fresh normalized `main=f7eabfea74480d307b52d4b053730021efc95352`, after M3.1 implementation PR #33 and independent normalization PR #34 both passed their own exact-head `pull_request` CI, merged via `expected_head_sha`, and `main` was re-fetched.
- M3.1 controlled Windows isolated v7 read-only diagnostic and independent 11/11 post-close custody PASS. Existing production remains restored-active SQLite v6 with its M1.5 activation marker.
- Scope limited to M3.2; M3.3+, M4+, AI, ComfyUI and release excluded.

## Stage 1: test-only manual model, not a production IPC

`src-tauri/src/m32_manual_chronology.rs` is included in `lib.rs` only under `#[cfg(test)]`. Its parameterized insert/select functions operate on temporary **in-memory** SQLite databases, explicitly upgraded from v6 only inside test fixtures with the exact M3.1 candidate SQL.

- Human-authored fictional calendars, four time kinds `exact`, `approximate`, `relative`, `unknown`; raw fictional labels and optional precision, never Gregorian parsing or inferred dates.
- Universe-scoped event entities and exact immutable scene-revision provenance; no link by display name or current revision head.
- Human-authored before/after edges form a **partial** order, with deterministic rejection of cross-Universe links, self-edges, duplicates and cycles by existing v7 SQL constraints.
- Anchor and edge list operations are sorted by **immutable ID only** for stable rendering; this is explicitly not a world-time, narration or reader reveal ordering.
- Existing M3.1 v7 tables reject UPDATE/DELETE by triggers. Consequently complete `CRUD` correction, supersession/revocation semantics, durable service registration and the chronology GUI are **not yet implemented**. No fake deletion, no rewriting historical data.
- Normal runtime `CURRENT_SCHEMA_VERSION=6`, `MAX_AUTOMATIC_MIGRATION_VERSION=6`; default Tauri IPC unchanged; debug-only `m31-isolated-preview` IPC remains strictly read-only. No Windows process, operator database, backup, or active pointer touched.

## Test acceptance for this first stage

Tests cover four time states, explicit calendars, two Universes, multiple Novels, historical revision IDs, event-kind guards, cross-Universe rejection, stable human precedence order, cycle/duplicate/self-edge veto, and immutable history. Candidate still requires new exact-head GitHub CI. Tests are fixtures only and cannot substitute for Windows operator acceptance of M3.2.

## Next M3.2 gates (not pre-accepted)

1. Current-head `pull_request` Windows CI of this source; diagnose and fix any failure without resetting the protected worktree.
2. Design governed supersession/revocation (rather than bypassing the M3.1 immutable triggers), and provide explicit manual event/time anchor correction semantics and separate narration/reveal read-only panes.
3. Implement an isolated writable M3.2 runtime/IPC/UI with a **new, deliberately authorized**, non-production Tauri identity and fresh protected v7 copy; never extend the M3.1 *read-only* preview with write commands.
4. Add fail-closed operator backup, rollback, exact-source, offline Windows GUI/IPC and post-close digest evidence. No automatic v7 migration of the normal M1.5 production database.
5. Complete acceptance, evidence-commit exact-head CI, protected merge, then **separate normalization PR and CI** before M3.3.

**This document and source are a first milestone of implementation, not M3.2 COMPLETE.**


## Stage 2 — Append-only decisions candidate (2026-10-12)

Stage 1 exact source `690656bcd9c148ac7737749cfb6d2a7350df1c7a`, `pull_request` CI #38190352570 **completed/success**. This qualifies only the stage-1 test model; the current stage-2 change needs fresh exact-head CI.

New file: `src-tauri/sql/m3_2_chronology_decisions_candidate.sql`, **applied only in the same fresh in-memory Rust test fixture AFTER the M3.1 v7 SQL**. It creates STRICT append-only `world_time_anchor_decisions` and `world_time_precedence_decisions`, each with immutable decision identity, original author assertion, universe, `revoke` or `supersede`, optional replacement, mandatory human reason, optional immutable same-Universe text revision, and creation timestamp. All decisions are INSERT-only; no UPDATE, DELETE, cascades or automatic schema registration. An original assertion can have one terminal decision; the replacement must not already have a terminal decision, preventing replacement loops/forks. Foreign-Universe originals, replacements and source revisions are rejected. New precedence insertion referring to an already superseded/revoked anchor is refused.

Rust stage-2 service includes parameterized anchor/precedence decision commands, a transactional create-and-supersede anchor operation (rollback on decision failure), immutable historical lists, separate *current* lists with no false chronology sorting, and explicit decision history. It has no Tauri IPC or GUI registration: it remains compiled exclusively under `#[cfg(test)]`. Tests exercise real revocation, replacement, transaction rollback, immutable history, same-Universe source lineage, and cycle/duplicate veto.

**Known limitation, fail-closed:** the original M3.1 SQL cycle guard scans all historical precedences; revoking an edge does not allow insertion of a contradictory reverse edge using the old `world_time_precedences` table. This stage deliberately tests that rejection and does NOT silently drop or weaken the historical SQL trigger. A separately reviewed replacement *active-graph* representation and conflict rule, with provable rollback and legacy lineage preservation, is required before implementing complete chronology edge correction UI. A GUI CRUD claim would be premature.

Next: exact-head CI; then define active-graph disagreement handling and independent narration/reveal read-only views; only afterward a dedicated writable isolated M3.2 Tauri identity, IPC and target Windows custody. Normal application remains restored-active v6 with no registered 007 or mandatory Ollama.


## Stage 3 — Unmounted read-only React coordinate projection (2026-10-12)

Stage-2 exact head `27b4c60b8c304dd29bdf7c1f03efa2cd3c6b7551` obtained [CI #38198727275](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/38198727275) **completed/success, 23/23 Windows steps**. This is an isolated SQLite/Rust decision-contract PASS, not an IPC/UI acceptance.

New `src/M32ChronologyPreview.tsx` is a **non-mounted** read-only React component accepting an explicit `M32ChronologyProjection`. It displays **three clearly separate sections**: (1) raw fictional world-time anchors and explicitly authored precedence statements, including revoked/superseded history; (2) original **manuscript order** within each novel by chapter/scene positions, explicitly no invented cross-novel order; (3) reader-reveal state **unavailable/not authored**, never inferred from a source scene or world timestamp. Its input decoder refuses missing/mixed Universe, duplicate anchor/edge/scene IDs, invalid time/status values or broken precedence endpoints; invalid projections fail closed, not partial/mixed rendering.

`src/m32ChronologyPreview.test.tsx` uses React static rendering to verify coordinate separation, manuscript positions, revocation labels, absence of buttons/IPC and automatic reveal inference, cross-Universe rejection and HTML escaping. **No `App.tsx` import, no visible production feature or write controls, no automatic v7 migration and no new Tauri IPC**. This is presentation-contract groundwork; the real offline user-facing GUI and a separate isolated write-capable M3.2 identity remain pending explicit operator qualification.

Current HEAD after this change needs its OWN new CI; prior stage-2 success cannot accept it.


## Stage 4 — Active-graph restatements candidate (2026-10-12)

Stage-3 HEAD `ecdf04627bdb40fc948b1b7c7f2d3abec57952b0` earned [Windows CI #38199285576](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/38199285576) `completed/success`. The subsequent stage-4 HEAD must have its own CI.

New **test-only** SQL `src-tauri/sql/m3_2_active_precedence_candidate.sql` adds an immutable STRICT table `world_time_precedence_restatements`. A replacement edge must explicitly cite a revoked M3.1 original precedence from the **same Universe**, provide a human-authored reason, and only connect current same-Universe anchors. It is not written into the immutable legacy v7 table, so a safe reversal can be represented without removing history or relaxing the old cycle trigger. A given original may have **at most one restatement** in this initial bounded protocol. The restatement source revision is optionally linked to the exact historical text revision and its Universe is checked.

SQLite INSERT triggers reject self-links, non-revoked/missing originals, cross-Universe links, mismatched source revisions, duplicate active edges and directed cycles in the **combined active partial graph** (non-revoked legacy edges plus restatements). A second trigger prevents later raw v7 INSERTs from bypassing the new active-graph cycle check. The old M3.1 raw-history cycle constraint remains intact and can veto an otherwise active-safe legacy insertion; authoring a correction therefore uses the explicit restatement route. Current projection lists retain stable ID display ordering, not inferred chronological ranking or automatic Gregorian conversion.

Four isolated in-memory Rust fixture scenarios qualify reversed edges after revocation, preserved legacy history, duplicate/same-Universe/retired-endpoint checks, current-graph cycles, later raw-insert backdoor, and database-level immutability. No normal Tauri IPC, new app runtime, automatic migration or target-PC operation exists in this stage.

**Remaining limitation:** The new restatement table has no governed append-only revocation/supersession of restatements yet; full recursively correctable chronology CRUD still requires an additional policy and test matrix. It is not authorized to expose this interface to production or operator databases. M3.2 remains OPEN/DRAFT pending fresh CI and later isolated Windows acceptance.


## Stage 5 — Withdraw a previous restatement, without rewriting history (2026-10-12)

Stage-4 exact-head `dc2fa5b2cbcb4d91b8c3d3e26a30e27093534cdd` passed [CI #38199955357](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/38199955357) **23/23 Windows steps SUCCESS**. This stage-5 candidate requires a new exact-head CI.

New **test-only** `src-tauri/sql/m3_2_restatement_revocations_candidate.sql`, applied exclusively after M3.1 v7 and M3.2 decisions/restatements in a **new in-memory** database, creates `world_time_restatement_revocations` STRICT. Each row permanently records one identified restatement's withdrawal, its source Universe, mandatory author reason, optional same-Universe immutable scene revision, UTC creation timestamp. Foreign Universes, duplicates, nonexistent IDs, blank reasons and changes to past decisions fail closed. The original historical v7 edge and the earlier restatement are **never edited or deleted**.

`revoke_restatement`, `list_restatement_history` and the amended `list_active_precedence_graph` distinguish auditable history from current valid assertions: revoked restatements disappear from the active display but remain linked to their withdrawal and reason. Rust tests validate double-revocation veto, source-revision ownership, absence of archive mutations, foreign-key and SQLite integrity, and normal runtime's schema ceiling 6.

**Important limitation, deliberately not hidden:** stage-4 SQLite insertion guards still consider withdrawn restatement rows and can conservatively reject subsequent edges that would be valid in the reduced active graph. The unique `revoked_precedence_id` link also prohibits a second restatement of the same original, even after withdrawal. That is a **fail-closed reauthoring gap**, not a claim of complete correction-chain CRUD. A future separately tested version-chain and active-graph trigger redesign must resolve it before writable M3.2 Tauri UI/IPC. No operator Windows data, real activation marker, production SQLite, auto-v7 migrations, Rust runtime, `App.tsx` or M3.1 read-only preview modified by this stage.

## Stage 6 — One successor after a withdrawn restatement (2026-10-12)

The stage-5 head `7cd198493b32645025d7a34ca30735d2ef99579e` passed exact-head [CI #38200842678](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/38200842678) **completed/success, 23/23 Windows steps**. Stage 6 requires its **own new exact-head CI**.

Test-only candidate `src-tauri/sql/m3_2_restatement_successors_candidate.sql`, executed **only after v7, decisions, restatements and restatement revocations within a fresh SQLite in-memory fixture**, introduces a STRICT, immutable `world_time_restatement_successors` table for exactly **one** new human-authored relation after an initial correction is explicitly withdrawn. Its original v7 assertion, first correction and withdrawal remain inspectable. IDs, Universe, predecessor, current endpoints, mandatory reason and optional immutable same-Universe source revision are enforced by foreign keys and triggers. `prior_restatement_id` is unique, so this stage intentionally **cannot** branch or recursively correct the new successor.

`m32_active_precedence_projection` is the common **read-only** current-graph SQL VIEW used by the Rust listing and *new* write guards. It filters revoked original assertions, withdrawn initial restatements and retired anchors; then unions still-active legacy edges, initial restatements and the new successor, without inventing a total order or Gregorian timestamps. Candidate-only triggers guard successor insertion, **future legacy v7 raw** edge insertions and initial-restatement insertions against duplicates and graph cycles that would otherwise be invisible to earlier guards. Recursive reachability uses `UNION` to stop revisiting cycles. Original M3.1 triggers stay unchanged and are allowed to reject more cases conservatively.

Rust tests cover first-restatement withdrawal → second authored correction, immutable lineage, no extra fork/foreign-Universe, cycle rejection, backdoor checking on both original tables, retired endpoints, missing reason, foreign-key and integrity checks. New tests and SQL stay under `#[cfg(test)]`; no normal app, IPC registration, Tauri identity, M1.5 activation, production v6/v7 migration, or protected operator files are affected.

**Stop boundary:** successors are not themselves revocable here; deeper correction chains, concurrent operator writes, GUI editing and source-lineage generalization require separately qualified design, CI and Windows operator acceptance. M3.2 **NOT COMPLETE**.

## Stage 7 — Explicit, immutable withdrawal of one successor (2026-10-12)

Stage-6 head `4119fc5b5a49a84fc05a3770cc57216e7638c603` passed its own [Windows CI #38259258644](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/38259258644) **completed/success, 23/23 steps**. The NEW stage-7 HEAD requires its own exact-head CI.

New **test-fixture only** `src-tauri/sql/m3_2_successor_revocations_candidate.sql` creates STRICT immutable table `world_time_successor_revocations` with one terminal withdrawal decision per authored stage-6 successor, explicit Universe and mandatory human reason, optional exact immutable scene revision restricted to same Universe, and UTC audit timestamp. No original M3.1 v7 assertion, previous restatement, its withdrawal, or successor is modified/deleted.

Within the **same freshly built in-memory fixture**, this stage **rebuilds only** the derived `m32_active_precedence_projection` SQL view to exclude withdrawn successors, in addition to already revoked legacy and initial restatement edges. The existing stage-6 triggers reference that stable view name and therefore use the updated active graph on later insertions; they remain conservative wherever original M3.1 or stage-4 guards are stricter. Rust `revoke_successor` and `list_successor_history` expose guarded append-only decisions and full correction ancestry for tests. New tests verify status transitions, cross-Universe and source-revision vetoes, duplicate/blank decision refusal, immutable audit history, foreign-key and SQLite integrity, no new successor fork, and normal schema ceiling v6.

**Scope limit:** successor withdrawal is terminal; the author cannot insert another successor in that correction chain. Unlimited-depth correction/revoke loops, refactoring conservative predecessor triggers, true operator-accessible editing, concurrent writes, and a separate writable M3.2 Tauri identity are not solved by this stage. No production IPC, `App.tsx` mount, automatic migration 007, M1.5 pointer, backup or real operator SQLite is touched. M3.2 remains **OPEN/DRAFT**, not COMPLETE.

## Stage 8 — Generic append-only correction chain candidate (2026-10-12)

Stage-7 exact-head `31e2078cfeedf5f0d755fc0fc0c940685d3cb4f0` passed [CI #38262070398](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/38262070398) **completed/success, 23/23 Windows steps**, required GitHub Actions app check. The new stage-8 HEAD must earn its own CI.

New file `src-tauri/sql/m3_2_recursive_chain_candidate.sql` is test-only: applied AFTER the previous v7 + M3.2 stages to a fresh SQLite in-memory fixture. STRICT `world_time_chain_links` and `world_time_chain_revocations` provide a **linear, append-only correction lineage without a fixed maximum generation count**. Each new link points to exactly one already-withdrawn same-Universe **stage-6 successor** or earlier chain link; UNIQUE parent-link keys ban competing child corrections; immutable history and one revocation per link are enforced. Every node has explicit author reason and optional exact immutable same-Universe text revision. Child endpoints must remain current same-Universe anchors. Historical IDs are never reinterpreted as Gregorian time.

The same `m32_active_precedence_projection` name now includes only non-revoked chain nodes, alongside non-revoked legacy, first-restatement and successor rows. New SQL insert guard rejects cycles and duplicate active edges using recursive reachability over this shared current projection; prior stage-6/7 triggers use that projection automatically when inserting raw v7 or first-restatement edges. Historical M3.1 triggers remain conservative and unchanged. A separate SQL trigger ensures any chain withdrawal references a same-Universe node and optional same-Universe source revision.

Rust `append_chain_correction`, `revoke_chain_correction`, `list_chain_history` are `#[cfg(test)]` only via the containing module. Deterministic in-memory tests cover five successive chain nodes, mandatory withdrawal before linking, missing/dual parent veto, fork prevention, cycle and duplicate veto, raw-v7 insert backdoor, strict immutable audit, universe/source-revision checks, SQLite foreign-key and integrity checks. **This is not an interactive or operator-accepted data editor.**

**Important acceptance boundary:** generic lineage is structurally supported, but a full concurrency/adversarial cross-connection and rollback proof, correction of current anchors, integration with 3-pane React UX, a new isolated write-capable Tauri identity and target-Windows operator GUI/IPC/backup custody are all still pending. Nothing changes production SQLite v6, M1.5 restored activation, M3.1 read-only preview, regular Tauri IPC, normal schema migration ceiling, or preserved Windows backup manifests. PR #35 stays DRAFT; M3.3 not authorized.

## Stage 9 — Two independent SQLite connections: rollback, locking, isolation (2026-10-12)

Stage-8 exact-head `eb9f6486567fdcb65ba5556b2861593c7b18bca0` earned required [Windows CI #38263839166](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/38263839166) `completed/success`, 23/23 steps, no bypass. Stage 9 requires a **NEW exact-head CI**, not the old result.

New `#[cfg(test)]` file `src-tauri/src/m32_sqlite_concurrency_tests.rs` tests a fresh **uniquely and exclusively created** SQLite file under the runner's temporary directory, never the Windows operator app root, historical backup or activation pointer. A scoped RAII guard removes the synthetic scratch file and its sidecars after both independent SQLite handles close. This deliberately uses two normal PRIVATE-cache connections with WAL for committed-read isolation, rather than the SQLite-deprecated shared-cache mode. No new Cargo dependency, Tauri IPC registration, automatic v7 migration, feature flag or frontend change.

Both connections verify the *same* candidate v6→v7 schema and all M3.2 test-only SQL stages, with fake Universe/anchors and a withdrawn second-generation correction. Exact test scenarios:
1. A writer starts `BEGIN IMMEDIATE` and authors an uncommitted chain node. The second connection sees **zero** uncommitted active edges and its contending write fails `SQLITE_BUSY` or `SQLITE_LOCKED`. After rollback, a retry succeeds, while a competing fork from the other handle is forbidden by UNIQUE parent lineage.
2. A withdrawal and its child correction are tentatively authored together. The second connection sees the old committed edge and no partial withdrawal. Full rollback preserves that state; a subsequent single transaction commits both operations, which the reader observes atomically.
3. A second connection cannot bypass active-only cycle guards by inserting through the old raw v7 table. Setting `PRAGMA query_only=ON` on that handle blocks attempted writes without changing active history.

All tests enforce `PRAGMA integrity_check=ok`, zero `foreign_key_check` failures and normal automatic migration ceiling v6. These are controlled **test-runner scratch file** simulations, **not** target-PC or live Windows operator custody. The database never contains sensitive user data. The main app, M3.1 read-only preview, production M1.5 marker and all historical backups remain untouched.

**Next gates:** qualify the stage-9 exact HEAD; then independently design the isolated writable M3.2 Tauri flavor with new identity, strict IPC allowlist, explicit backups/rollback and an interactive chronology editor. M3.2 remains DRAFT; no merge or authorization of M3.3.
