# M3 — Time, Knowledge and Relationships (Proposed Governed Roadmap)

**PROPOSAL ONLY — NOT ACCEPTED, NO M3 IMPLEMENTATION OR SQLITE MIGRATION AUTHORIZED BY THIS DOCUMENT UNTIL THE PLANNING PR IS QUALIFIED, PROTECTED-MERGED, AND ITS INDEPENDENT NORMALIZATION IS COMPLETED.**

Origin authority: Fabulaxiom V1 roadmap, M3 deliverables after fully normalized M2. Normalized main checkpoint: `f13b4f8c249866ff60a19d7895b6cfaede56398a` (protected merge of M2.5 normalization PR #30). Existing SQLite schema is **v6**, with immutable scene-revision anchors, stable Universe-scoped entities, optional fact validity, human-governed fact statuses and append-only review events.

## Goal

Offer a practical, **manual and offline** representation of *when something occurs*, *who knows or believes what at which point*, and *how relationships or narrative states change*. Never reinterpret prose as truth automatically. Three orders must remain independently queryable:

1. **World chronology** — when an event actually happens in its fictional Universe (possibly unknown or partially ordered).
2. **Narration order** — where a scene is located in a manuscript, not necessarily chronological.
3. **Reader reveal order** — when a reader learns a fact, distinct from both the event and the narrator's belief.

Do not impose a Gregorian epoch; fictional calendars, multiple clocks, approximate periods, "before/after" constraints and undated events are first-class. Facts and human canonical reviews from M2 remain authoritative and must not silently become canon when referenced in M3.

## Nonnegotiable invariants and boundaries

- **Local-first and no Ollama dependency** for every M3 manual workflow; Rust/Tauri/React + existing SQLite, no cloud, external API, FTS5, embeddings, AI extraction or generation.
- All links reference immutable identifiers for Universe, Entity, Scene and (when supported) the exact **immutable revision**; don't key on display name or the current scene-head pointer. Same-name characters remain different identities. The same Universe may span multiple Novels; links across unrelated Universes fail deterministically.
- Preserve existing M1.5 restored-active pointer; migration from v6, if authorized, must be **additive**, transactionally guarded and preceded by a new SQLite-consistent, non-overwritten operator backup + SHA256 manifest and full table-by-table logical digests. Preserve existing historical backups, their digests, scene revisions/heads, facts/sources and review events; never re-run migrations as fresh work.
- Time supports **unknown**, **exact-in-fictional-calendar**, **approximate window**, and **relative ordering**. Keep raw calendar fields and user-declared precision; never call \`Date.parse\` as an implicit fictional timestamp and never fabricate a start/end or a total order where only a partial order is known.
- Explicit **world / narration / reveal** coordinate types must not be interchanged or auto-derived. Relative constraints that form cycles, invalid same-world references or impossible declared exact bounds must be rejected with deterministic errors, without removing old history. An "unknown" state is not a claim of impossibility.
- A person's **knowledge**, **belief**, **lie**, and **reader-visible information** are different assertions. A character may sincerely believe a false statement; that does not rewrite the world's canonical fact. Reviewer self-labels remain unauthenticated; no automatic canon promotion or retcon.
- Relationships are **directional and time-dependent**; \`A trusts B\` is not equivalent to \`B trusts A\`. Changes retain stable actor/object IDs, their human-entered reasons, optional sources, temporal position, and historical revisions. Negations and unknowns must be expressible without inventing certainty.
- Location, possession, injury and life-state change are **manual state transitions with uncertainty**. No auto-inferred contradiction proof or automatic story rewrite (M6); no advanced graphical relationship map or shared multi-novel timeline dashboard (M8).
- Do not add M4 FTS5/embeddings, M5 AI, M6 consistency engine, M7 writing assistance, M8 dashboards or proposed ComfyUI visual atelier (issue #19). ComfyUI remains proposal only, and manual imported imagery stays a separate future scope.

## Sequential proposed subdivisions (one at a time)

### M3.1 — World-time foundation and schema

Scope *only after governance accepts this plan and separate planning normalization*: draft precise schema contract, implement **one additive v6→v7 migration** for time anchors, calendar definitions scoped per Universe and relative precedence constraints; immutable IDs and source/revision links where appropriate; explicit precision/unknown representations, foreign keys, indexes and STRICT tables, cycle constraints mediated by deterministic Rust transactions. No GUI chronology editor, relationships or character knowledge here.

Acceptance: migration unit fixtures for empty and populated v6; migration rollback and idempotence; same-Universe foreign key rejection, no names-as-FKs, no implied Gregorian calendar, no cycles, preserve preexisting row content/SQLite active pointer. CI on exact PR SHA then operator Windows pre-v7 backup, controlled launch and read-only post-v7 audit. Evidence-commit CI, protected merge, separate post-merge normalization.

### M3.2 — Manual chronology and ordering UX

Manual event/time anchor CRUD and relative before/after authoring without AI, including uncertain and undated events. Scene reference retains manuscript position but does not rewrite world-time. The GUI clearly separates world chronology from narration order and read-only reveal order. Deterministic cycle/conflict responses; no destructive cascades or automatic event ordering.

Acceptance: two Universes, multiple Novels, exact/relative/approximate/unknown assertions, contradictory and cyclic test inputs, event references to historical text revisions; offline Windows operator testing; immutable M2 sources and history intact, backups and pointer preserved. Exact-head CI + separate normalization.

### M3.3 — Directional relationship history

Manual directional relationship assertions and change history between stable entities within one Universe, optionally anchored to events/times and immutable sources. Relationship statuses distinguish declared, tentative, unknown and revoked; never infer reciprocity. Preserve earlier relationship states when values change.

Acceptance: A→B not equal to B→A, renamed/homonymous actors remain distinct, cross-Universe rejection, temporal changes are traceable, lifecycle and deletion restrictions, native Windows UI with Ollama OFF. Exact-head CI, protected merge, normalization.

### M3.4 — Character knowledge and beliefs

Manual "character knows", "believes", "suspects", "is mistaken" and "does not know yet" scoped to an event/temporal window, with evidence reference where available, human review separate from the M2 canon registry. Changing a fact's canon status does not rewrite historical character beliefs.

Acceptance: false beliefs, disputed beliefs, unreliable narrators, different characters at the same event, before/after learning, accurate source pointers, deterministic isolation and absence of implicit universal knowledge. Exact-head CI, protected merge, normalization.

### M3.5 — Narrator and reader reveal state

Manual narrator viewpoint and reader exposure/reveal records independently ordered by chapter/scene/revision, including spoiler-sensitive yet unexposed information; distinguish reader knowledge from fictional-world chronology and character beliefs. No AI narrator knowledge extraction, no automatic reveal inferred from word search.

Acceptance: out-of-order narration, delayed exposition and flashback, reader knows before character, narrator withholding, same scene in revised manuscripts, alternate novels within same Universe, deterministic error messages and privacy of unexposed reveals. Exact-head CI, protected merge, normalization.

### M3.6 — Evolving narrative state and integrated UX

Manual transitions for possession, location, injury and life-state. Connect only to approved chronology / relationship / knowledge anchors; show read-only coherent inspection of world time, character perspective and reader reveal without the M8 advanced visualization. Preserve uncertainty and explicit human audit lineage; no automatic inconsistency engine.

Acceptance: multiple changes at same/unknown times, non-owner possessions and location corrections with explicit history, no auto-deletion of dependent sources, revision-safe UI, offline Windows fixture tests, all prior data preserved, full v7+ integrity and rollback/backup custody, exact-head evidence CI and protected merge. Separate M3 milestone normalization required to declare M3 complete.

## Implementation and acceptance discipline

- Each subdivision receives a separate implementation PR, deterministic automated tests, \`Fabulaxiom CI\` terminal success on the **exact current head**, operator Windows functional evidence when applicable, an evidence-document commit **with a new exact-head CI**, protected merge with \`expected_head_sha\`, and an independent normalization PR with its own terminal exact-head CI/merge.
- Before any operator migration, verify the actual M1.5 activation pointer, the **restored active** SQLite v6 database, every historical backup digest (including original pre-M2.1 v3, pre-M2.3 v4 and pre-M2.4 v5) and any isolated test store. Create non-overwriting, consistent v6 pre-v7 backup + manifest; never infer backup corruption from a single script alert. If a hash differs, stop and independently investigate without rewriting the expected digest.
- The M2.5 isolated test database under \`com.fabulaxiom.m25qual35fb842c\` and its 3 facts/2 sources/11 review events remain historical acceptance evidence; **do not purge or reuse it as an empty fixture**. Test new features using a freshly identified separate, owned test database/worktree.
- Manual UI failure or stale data is a blocker even if SQLite/CI succeeds. No automatic merge from historical workflows, no scripted reset-hard, no destructive data cleanup and no implicit calendar assumptions.

## Immediate next work — planning only

This proposal is **not accepted** merely because M2 is normalized. Run exact-head documentation CI, review scope and incompatibilities, protected-merge planning PR and then a separate independent governance-normalization PR. **M3.1 implementation remains blocked until those planning/authority gates explicitly authorize it.** No M3 code, SQLite v7, M4+, release or ComfyUI implementation is authorized by this document alone.
