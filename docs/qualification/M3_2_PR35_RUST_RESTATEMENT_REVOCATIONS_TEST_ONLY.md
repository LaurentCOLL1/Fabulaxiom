# M3.2 — append-only withdrawal of a human restatement (test-only)

**CANDIDATE_NOT_CI_QUALIFIED.** PR #118 merged at `a0942b9566d6de21cf73e55dce47c3797dcb7c81`, source exact-head CI #39658544037 SUCCESS. Main push CI #39660168071 was IN_PROGRESS when this snapshot was written; it must be re-fetched before claiming terminal success.

Only `revoke_restatement`, `list_restatement_history`, and historic PR35 candidate `m3_2_restatement_revocations_candidate.sql` are added to the **`#[cfg(test)]` Rust module**. The SQL executes only after fake v6+v7+decision+restatement SQL inside `Connection::open_in_memory()`. Four Rust tests verify retained history, duplicate/cross-Universe rejection, immutable revocation records, and no silent reinstatement of the original precedence. The stage-four graph guards can remain conservatively restrictive even after revocation. This change grants no additional authorship chain.

No migration 007, no production IPC or SQLite file. M3.2 IN_PROGRESS_NOT_ACCEPTED; real writer absence NOT_PROVEN, G2B–G6 NOT_AUTHORIZED, G3 real STOP_UNAVAILABLE, historical custody 21/3/2 unresolved, prospective baseline NOT_STARTED. No Windows operator, backups, ACL/sidecars/markers, M3.3, ComfyUI or release.

**Initial CI #39661237200 FAILED** at three stale historical handoff assertions comparing root live CI to PR112/113/114 snapshots. Test assertions now check their own historical objects. No SQLite/Rust change. A new source-head CI is required.
