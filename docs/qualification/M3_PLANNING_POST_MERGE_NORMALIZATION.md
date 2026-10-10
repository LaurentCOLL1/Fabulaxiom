# M3 — Independent Planning Post-Merge Normalization Gate

**DOCUMENTARY ONLY — not M3.1 implementation, not SQLite v7 authorization for operator Windows.**

## Fresh source authority and planning merger

- Private repository: `LaurentCOLL1/Fabulaxiom`.
- M2 fully normalized baseline: `f13b4f8c249866ff60a19d7895b6cfaede56398a` (PR #30).
- Planning PR: **#31 — docs: plan bounded M3 time, knowledge and relationships**.
- Exact planning HEAD: `5127ced6c5e175b0919c736c658036382794487e`, branch `docs/m3-time-knowledge-relationships-plan-20261010`.
- Exact PR-triggered `Fabulaxiom CI`: run **38050865413**, `completed/success`, one Windows job and **13/13 successful steps**. The job and check-run were independently inspected and tied to the same SHA.
- Merge: `68db746754e01b441870e0653f17f10ebfc7be2f`, via GitHub `merge_pull_request(expected_head_sha=5127ced6c5e175b0919c736c658036382794487e)`.
- Post-merge re-fetch confirmed `main=68db746754e01b441870e0653f17f10ebfc7be2f`, #31 merged and no remaining open PR at that checkpoint.

Planning changed **only** `README.md`, `docs/continuity/STATE.md`, `docs/continuity/NEXT.md`, `docs/roadmap/FABULAXIOM_ROADMAP_V1.md`, `docs/roadmap/M2_NARRATIVE_ENTITIES_CANONICAL_FACTS.md` and new `docs/roadmap/M3_TIME_KNOWLEDGE_RELATIONSHIPS.md`. No source, lockfile, migration, database, release or ComfyUI modification.

## Technical and semantic review

The accepted *plan*, not functionality, governs six sequential subdivisions:

1. **M3.1 — World-time foundation and schema**: independent fictional calendars, imprecise/relative/unknown time and additive schema; explicit cross-calendar mappings only, without fake Gregorian timestamps; deterministic cycle rejection.
2. **M3.2 — Manual chronology and ordering UX**: distinct world, manuscript and reader-reveal orders; historical immutable revision anchors and partial chronology.
3. **M3.3 — Directional relationship history**: separate A→B and B→A statements and append-only or otherwise durable history, with uncertainty.
4. **M3.4 — Character knowledge and beliefs**: knowledge, misconceptions, doubts and deliberate lies never silently change canonical world facts.
5. **M3.5 — Narrator and reader reveal state**: delayed exposure, potentially unreliable narration and revision-specific records, without automatic spoiler inference.
6. **M3.6 — Evolving narrative state and integrated UX**: manual possession, place, injury and life-state transitions, without the M6 contradiction engine or M8 visual map.

Review specifically requires immutable identity, same-Universe references, optional exact scene-revision provenance, no automatic human-canon promotion, no inferred total order, deterministic failures and conservative treatment of unknown facts. M2 remains the authoritative human-reviewed canon source. No Ollama requirement for manual CRUD. The separate ComfyUI visual atelier, issue #19, remains a proposal, not an implemented feature.

## Data custody and operator boundary

- Production is **SQLite v6**, and actual active DB comes from M1.5 activation marker, not a guessed default pathname.
- Reference production v6 logical SHA-256: `67dfd9194ff884762bbffaa39d774df10fadcd74cbc9e6774e36d323e4506fc6`.
- Isolated M2.5 qualification v6 logical digest: `cff8a04f29ec60757c02ef9ed186be40c806cfcc6a2cfd11fa8072be44f273cb`, preserving 3 facts / 2 sources / 11 immutable review events.
- Isolated pre-fact backup SHA-256: `9e738d58519e1a0e3c1750d71726b661132fcbc0211fddea3178f6314bbfc7cf`.
- Preserve all historic pre-M2.1/v4/v5 backups and worktrees. The earlier PowerShell v4 hash alarm was a **historical script issue**, not proven corruption; independently re-verify instead of rewriting expected hashes.
- This PR does **not access or alter any Windows SQLite files**, their active pointers, backups or test fixtures.

**Important GitHub branch-policy truth:** GitHub reported `main.protected=false`. Its private-repository rulesets endpoint returned HTTP 403 with a plan-upgrade restriction. The merge used a strict `expected_head_sha` compare-and-swap guard and exact-head CI inspection, **not formally enforced GitHub branch protection**. Do not describe these as equivalent.

## Separate normalization acceptance and next authority

1. Inspect this normalization PR's current SHA and precisely bounded documentary diff. Re-fetch `main`, all other PRs and any reviews.
2. Require fresh `pull_request` `Fabulaxiom CI` **`completed/success` for this normalization HEAD**, with all actual jobs and steps passing. The planning run #38050865413 does not qualify the new normalization commit.
3. Merge this PR using `expected_head_sha` only if the current PR is mergeable and its diff remains documentary; then re-fetch `main`, `STATE.md`, `NEXT.md`, V1 roadmap and this evidence.
4. **Only after 1–3** declare M3 **planning** `ACCEPTED + MERGED + NORMALIZED` and authorize work on **M3.1 only** in its own exact-source branch/PR. M3.1 code, SQLite v7 and operator migration are *not* delivered by this document.
5. Before any future operator v6→v7 launch, separately qualify a new non-overwriting, consistent v6 backup of the resolved active database (and all prior historical backup hashes), full-table logical snapshots, schema/integrity preflights, operator app closure, rollback and controlled Windows UI/SQLite evidence. Do not run production migration by default.

**Do not start M3.2–M3.6, M4+, ComfyUI or a release** simply because planning is normalized.
