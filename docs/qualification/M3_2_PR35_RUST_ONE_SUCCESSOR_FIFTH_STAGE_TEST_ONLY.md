# M3.2 — one explicitly authored successor (fifth RAM-only stage)

**CANDIDATE_NOT_CI_QUALIFIED** on 22 October 2026. Protected main `61e07deaf10fc393c567e8f1960874b75d81adc4` after PR #119 merged (source CI #39661776335 SUCCESS with 121 Rust tests); post-main CI #39684342539 was IN_PROGRESS at this dated snapshot.

Carry over from historic PR #35 head `41ce7b915e76d22785d53d7fffe288d113dd0bf5` only the `ActivePrecedence` type, `succeed_withdrawn_restatement`, `list_active_precedence_graph`, and unchanged candidate SQL `m3_2_restatement_successors_candidate.sql`. This is loaded after fictive v6/v7/decisions/restatements/withdrawals into `Connection::open_in_memory()` with module `#[cfg(test)]` only. Four new tests check a withdrawn restatement prerequisite, exactly one successor, current anchors, acyclic/unique active partial-order projection and immutable records. No writer IPC or real DB migration.

No successor withdrawal or arbitrary correction chains; no forced total timeline. M3.2 IN_PROGRESS_NOT_ACCEPTED, PR #35 DRAFT, real writer absence NOT_PROVEN, G2B–G6 NOT_AUTHORIZED, real G3 STOP_UNAVAILABLE, historical 21/3/2 evidence missing, prospective baseline NOT_STARTED. No Windows operator actions, production v6/isolated v7 data, ACL, backups, journals, marker, M3.3 or release.
