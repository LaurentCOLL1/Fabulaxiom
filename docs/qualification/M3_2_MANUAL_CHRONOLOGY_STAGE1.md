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
