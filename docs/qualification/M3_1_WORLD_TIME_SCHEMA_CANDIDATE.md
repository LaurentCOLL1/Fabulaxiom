# M3.1 — Fictional World-Time Schema Candidate (isolated qualification)

**STATUS: CANDIDATE ONLY — NOT RELEASED, NOT OPERATOR-QUALIFIED, NOT REGISTERED AS SQLITE MIGRATION v7.** The current shipped schema and `database::CURRENT_SCHEMA_VERSION` deliberately remain **v6**, and `open_database()` keeps using the six accepted migrations. This prevents a source checkout or unplanned app start from automatically upgrading the operator's resolved active restored SQLite database before backup custody has been qualified.

## Source and governance

- Start from post-planning normalized `main=6506d436357a22ee746ddce8520a4287a47652d8`, after planning PR #31 and independent planning-normalization PR #32 both passed exact-head CI, merged and were re-fetched.
- This is **M3.1 only**, with candidate schema and deterministic in-memory tests. No M3.2 GUI chronology editor, knowledge/relationships, Ollama, ComfyUI, future milestone or release code.
- Candidate: `src-tauri/sql/m3_1_world_time_v7_candidate.sql`.
- Dedicated Rust `#[cfg(test)]` fixture: `src-tauri/src/world_time_schema_tests.rs` (no runtime use and no target-Windows DB access).

## Candidate schema semantics

**`fictional_calendars`**: unique immutable ID, Universe-scoped owner, free-form local calendar unit definition. It is not automatically mapped to a Gregorian epoch. The unit definitions can describe unique fictional calendars, but do not yet supply a machine-validated date parser or a reliable calendar-to-calendar conversion.

**`world_time_anchors`**: immutable ID and Universe, optional same-Universe `event` entity and exact historical scene revision, temporal `time_kind` in `exact / approximate / relative / unknown`. Exact fictional dates use a raw `exact_label` tied to an explicit calendar; approximate windows use a user-entered start/end descriptor and mandatory precision; unknown and relative anchors never manufacture calendar coordinates. No lexicographic or wall-clock comparisons of fictional labels are made.

**`world_time_precedences`**: explicitly asserted and justified before/after edges, same-Universe composite foreign keys, optional immutable source revision of that Universe, stable IDs and append-only assertions. A recursive reachability guard refuses cycles and self-references. This is an authored **partial order**, not an inferred total order; cross-calendar edges, when manually asserted, are *not* treated as conversions. Future M3.2 corrections must use an explicitly governed supersession/revocation model, not mutate existing records silently.

All three tables are **SQLite STRICT** and preserve legacy M2 tables, immutable source evidence and operator backup ownership. Same-Universe source checks use the original revision `scene → chapter → novel → universe` lineage, independent of the current scene head. The event link requires the `event` entity kind, not a display name. Referential actions restrict foreign-key update/delete; no cascade deletion.

## Deterministic candidate tests

- Old v6 runtime stays v6 and has no candidate tables by default.
- Candidate applies only inside a transaction on an in-memory fixture, with three STRICT tables and unchanged legacy facts.
- Fictional exact dates, one-sided approximate windows, relative and unknown states, and invalid shape inputs.
- No implicit total order; no Gregorian parsing or conversion.
- Cross-Universe calendar, anchor and edge validation; event kind guard and same-Universe revision lineage.
- Duplicate edges, self-edges and longer-cycle rejection, plus append-only history.
- Reapplying candidate to the same DB aborts inside a transaction without altering v6 registry or previous records.

**Candidate limitations (must be resolved before final M3.1 acceptance):** no production v7 registration; no customer/operator backup/restore qualification; no explicit calendar conversion engine; no automatic ordering of exact/approximate labels; no time-anchor supersession UI. Validation of mutually impossible exact bounds requires an explicit comparable-calendar contract and/or refusing unsupported comparability rather than inventing dates.

## Exact-head qualification history (do not reuse old SHA results)

- Candidate HEAD `44e2a048f2c1e1a8df90a51a385d2bd676552149`: exact `pull_request` CI **#38071703495 FAILED** (77 Rust PASS, 3 new test failures). Two fixtures attempted calendar insertion before applying the test-only SQL and one mistakenly used `execute` for multiple SQL statements. No migration or production write occurred.
- Corrective HEAD `c1db5b84f937694caf2840e278195d49ab6933ae`: exact `pull_request` CI **#38073397298 completed/success**, **13/13 Windows steps**, **80/80 Rust tests**, frontend tests and build PASS, `cargo check --locked` PASS, unchanged dependency locks. This proves the *isolated candidate at that SHA*, not an operator v7 migration.
- After that success, additional isolated M2 nonregression tests were added: full Unicode UTF-8 source citation, original immutable revision pointer, existing human review/canon event history and same-Universe validation for chronology precedence sources. **The new HEAD requires its own terminal exact-head CI; #38073397298 is no longer sufficient for the current PR.**
- The qualification test source is `src-tauri/src/world_time_schema_tests.rs`; the schema candidate is `src-tauri/sql/m3_1_world_time_v7_candidate.sql`. No runtime registration, no SQLite v7 activation, no operator database access.

## Automatic-upgrade hard stop

The existing v6 runtime now explicitly caps all automatic SQLite migration execution at v6 with `MAX_AUTOMATIC_MIGRATION_VERSION=6` and `ExplicitMigrationRequired` for v7+. It rejects hypothetical unapproved v7 SQL and unexpected already-v7 schema on app startup. **This does not register or apply the candidate v7 SQL and does not change `CURRENT_SCHEMA_VERSION=6`.** The cap cannot substitute for a separately implemented opt-in v7 migration procedure or for operator backup/restore evidence. A new exact-head CI is required after the code and documentation updates.

## Hard gate before registering or running v7

1. Accept and qualify this isolated schema candidate on current exact PR HEAD with all Windows `Fabulaxiom CI` steps and Rust tests. Do not treat a CI PASS as Windows data migration acceptance.
2. Specify the **operator-preflight migration gate** before touching `MIGRATIONS` or changing `CURRENT_SCHEMA_VERSION`, because `database::open_database` currently applies pending migrations on app open. A source-only migration registry edit without a preflight could mutate the production restored-active database on the next launch.
3. Identify the actual M1.5 activated SQLite path, close the app, verify current schema/integrity/all historical backup SHA-256 and take a fresh, consistent non-overwriting pre-v7 backup plus manifest/full-table logical digests before first controlled v7 launch; independently qualify rollback.
4. Only then integrate the reviewed migration into the runner, test empty/populated v6 and controlled operator Windows v6→v7 upgrade in a separately governed acceptance gate, publish exact-source evidence, requalify the new evidence SHA and separately normalize after merge.

**This candidate PR must not be merged as an accepted M3.1 milestone or presented as full v7 implementation.** Preserve production SQLite v6, test fixtures, data pointer and all historic backups intact.
