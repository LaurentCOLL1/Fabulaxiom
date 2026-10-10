# M2.5 — Independent Post-Merge Normalization Gate

**CONDITIONAL — THIS PR IS DOCUMENTARY ONLY.** Status `COMPLETE + MERGED + NORMALIZED` applies **only once this PR has terminal success on its exact HEAD in every required workflow/job, protected merge succeeds with `expected_head_sha`, and the new `main` is re-fetched.** Until then M2 remains **IMPLEMENTATION MERGED / NORMALIZATION PENDING**.

## Exact implementation custody

- Repository: `LaurentCOLL1/Fabulaxiom`; implementation PR [#29](https://github.com/LaurentCOLL1/Fabulaxiom/pull/29).
- Qualified source: `7eaaf45ae164c9336df7e01c9da6787e4971d59e` / exact source `Fabulaxiom CI` run **38017441504**, terminal success, frontend 32/32, Rust 72/72 and all Windows jobs PASS.
- Evidence commit/head: `6f55fc3fc7eab6f2288a54619c0bef70e521f47e`; exact `pull_request` run [38040227617](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/38040227617), `completed/success`, one Windows job **13/13** steps PASS, frontend **32/32**, Rust **72/72**, frontend production build, `cargo check --locked`, unchanged lockfiles.
- Protected implementation merge SHA `f1e7ea99d26ad3390c7c47bfb339f26d730a44f1`. Independent normalizing branch created from freshly fetched exact merged main `f1e7ea99d26ad3390c7c47bfb339f26d730a44f1`.
- No code, schema, migrations, dependencies or lockfiles are allowed in this normalization commit. Scope only: `README.md`, continuity documents, accepted roadmaps and this evidence gate.

## Windows proof carried forward, without rewriting operator history

- Actual M2.5 isolated Windows worktree uses Tauri app ID `com.fabulaxiom.m25qual35fb842c`; it never uses production database identity `com.fabulaxiom.desktop`. Operator real tests: **8/8** narrative hierarchy fixtures, **8/8** automatic/manual React cross-module synchronization after `Aucun univers` bug fix, **9/9** sourced and unsourced fact UI, **10/10** human-review GUI interactions, Ollama stopped.
- SQLite isolated factual evidence **2 Universes / 2 Novels / 2 Chapters / 2 Scenes / 3 immutable text revisions / 2 revision heads / 3 original entities**. No Series were created and no invented third Novel is accepted as evidence.
- Postreview SQLite v6 **3 facts / 2 source anchors / 11 append-only review events**, contiguous 8+2+1 audit chains, accurate UTF-8 excerpts `[0,10)` and `[51,66)` attached to correct original immutable scene revisions; explicit human approve and revoke; final `draft`, `suggestion`, `unknown`. The **11 actual events** must not be altered to fit an erroneous 10-event earlier audit script.
- Full isolated logical digest `cff8a04f29ec60757c02ef9ed186be40c806cfcc6a2cfd11fa8072be44f273cb`; earlier pre-fact v6 isolated consistent backup SHA256 `9e738d58519e1a0e3c1750d71726b661132fcbc0211fddea3178f6314bbfc7cf` with manifest intact. Production *actual restored-active* SQLite v6 logical schema/data SHA256 `67dfd9194ff884762bbffaa39d774df10fadcd74cbc9e6774e36d323e4506fc6` unchanged and M1.5 marker unaffected.
- Preserved production pre-M2.1 v3 backup SHA256 `f8ec1a1f32f97a0b4f39eeb238c307e5a192854cdd6c4206a05a97b6a385c987`, pre-M2.3 v4 backup `c624241080d6e820398cc502b4db206fcaba457405083ce806c302a6ce464976` and pre-M2.4 v5 backup `db02961d7a30c6a6522bd52faeab8ceb09e26c1a4a6a58be467d142806e22fee`. PowerShell earlier v4 hash alert was refuted by independent Python SHA256, original manifest and v4 SQLite integrity; file is not corrupt.
- Review user label is manually *declared*, not authenticated. A source citation does not automatically imply canon. No M3 timeline, AI extraction, ComfyUI code, new runtime dependency or SQLite v7 was introduced.

## Terminal acceptance boundary

1. Re-fetch live main, this PR HEAD, all `pull_request` workflow runs for the **exact current PR SHA**, and every run job/step. Never reuse source/evidence run #38017441504/#38040227617 for this new normalization SHA.
2. Require terminal `completed/success` on all required jobs. If any failed, fix on a new commit and requalify.
3. Protected merge with GitHub `expected_head_sha` matching this **exact** document head. Re-fetch `main` and normalizing document state after merge.
4. Only when 1–3 pass: report **M2.1–M2.5 COMPLETE + MERGED + NORMALIZED** and **M2 milestone COMPLETE + MERGED + NORMALIZED**, without claiming V1 complete.
5. **M3 implementation stays unauthorized until current normalized authorities and an accepted detailed bounded M3 roadmap/planning PR explicitly permit it.** Do not implement M3 or optional visual ComfyUI (issue #19) in this PR.
