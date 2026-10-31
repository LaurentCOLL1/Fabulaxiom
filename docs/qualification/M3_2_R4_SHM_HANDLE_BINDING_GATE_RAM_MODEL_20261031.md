# M3.2 — R4 xShm native HANDLE binding evidence (RAM-only gate model)

**31 October 2026 — CANDIDATE, NOT QUALIFIED until exact-head Windows CI.** Protected parent main `1d06478a161cec35329b4f1ea9a67744fdea0a42` after PR #244. PR #244 source [Windows CI #41124543182](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/41124543182) **completed/SUCCESS**, exact source `ec624aea51cd62e327562721889478230327d223`, **269 Rust / 7 Greenfield / 56 inventory / 166 continuity**. Independent [postmain #41148419366](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/41148419366) was IN_PROGRESS at writing and must be rechecked separately.

## Architectural distinction

R4 stock SQLite Win32 `xShmMap` owns its mapping via mechanisms opaque to the simple test VFS wrapper. PR #244 observes `FileId128` of independent handles opened by name while mapping is alive. This does **not** bind those handles to the actual mapped index; matching name-based FileId128 may be stale or independently observed. SQLite [WAL spec](https://sqlite.org/wal.html) requires VFS shared-memory primitives in NORMAL mode and [WAL-index format](https://www.sqlite.org/walformat.html) explains SHM lock/mapping semantics.

This tranche formalizes a **negative / fail-closed contract** for any future native bundle-opening prototype. New `#[cfg(all(test, windows))]` source file `src-tauri/src/m32_r4_xshm_bound_handle_evidence_toy.rs` is deliberately **entirely RAM**: no `std::fs`, SQLite opens, native OS handle, Tauri IPC or operator resource. A typed `EvidenceBundle` models main, WAL, SHM and the **actual** mapped xShm handle, all with full volume+128-bit identity, provenance, consistent nonzero epoch and live lifecycle.

Ten distinct tests demand REFUSAL on name-only evidence, stock delegation without actual native xShm binding, mismatched mapped identity, cross-epoch/ABA, closed or absent handle, aliases and non-native main. Even when every *toy* input conforms, return is **`TemplateCompleteButRuntimeStillForbidden`**, not an admission capability. This is a model of required evidence, NOT evidence itself.

## Qualified only after CI

**Expected (NOT PASS yet):** 279 Rust / 7 Greenfield / 57 SQLite whole-tree source inventory / 167 living handoff contract tests. Source guard requires zero SQLite opening/flag occurrences in the new Rust file; reviewed test-only module registration in `lib.rs`. Full diff, reviews/threads, strict active `Protect main` bypass=[] and completed exact-head Windows SUCCESS before protected squash with `expected_head_sha`; distinct postmain push CI and issue #38 append-only.

**STOP:** M3.2 IN_PROGRESS_NOT_ACCEPTED ; writer/R1–R9 NOT_PROVEN ; G2B NOT_ACCEPTED ; G2C NOT_AUTHORIZED ; G3 STOP_UNAVAILABLE ; historical PENDING_EXTERNAL_ATTESTATION(21/3/2) ; prospective NOT_STARTED ; D3b-4/5 and D3b-5 STOP, D3c design-only. No operator v6/v7, real profile, backup, WAL/SHM, native Hello, migration 007, durable marker or recovery.

**Next technical gate:** design and test a genuine, validated native xShmMap handle-binding implementation for *new disposable Windows fixtures only*. The existing R3 preopened READ_ONLY VFS still has `xShm*` absent, and a test-only default Win32 forwarding wrapper is insufficient to establish atomic ownership. A future change must retain P1, reparse/ABA/namespace refusal and lifecycle/recovery STOP, not shortcut them.

## First exact-head CI refusal and correction (31 October 2026)

[Source CI #41148832898](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/41148832898) **completed/FAILURE** at initial HEAD `21df6fd0bc670c0c9ed1065facc04614bcf03c21`: the whole-tree SQLite inventory rejected an explicitly inserted all-zero `EXPECTED` entry for this RAM-only file, because `audit_inventory` intentionally records **only nonzero opening-site counts**. The corrected source **removes the impossible zero entry** and requires both `path not in EXPECTED` and `counts(source)==(0,0,0,0,0,0,0)` in test_57. The whole-tree exact-match gate is preserved; no Rust functional change, no operator access or writer admission. Previous failure is not a PASS; re-run at corrected exact HEAD.
