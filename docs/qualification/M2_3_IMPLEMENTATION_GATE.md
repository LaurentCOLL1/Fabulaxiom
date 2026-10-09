# M2.3 — Windows qualification evidence

**WINDOWS QUALIFIED; PR #25 MERGE AND NORMALIZATION PENDING**

Exact implemented and locally tested HEAD: `4d3b4b6015d477c3a6a5c3750d9743174e9c44a7`. Exact-source `Fabulaxiom CI` run `37879358744`: `completed/success` on `pull_request`, every Windows job step successful. Frontend 21/21, Rust 61/61, frontend build, cargo check locked, dependency locks PASS. Operator local re-run also PASS; worktree CLEAN.

## Windows SQLite v4 → v5

With Fabulaxiom and Ollama stopped, the operator resolved the M1.5 actual restored-active SQLite using its existing activation marker and independently created a consistent v4 backup and manifest before the application-driven migration.

Backup SHA-256: `c624241080d6e820398cc502b4db206fcaba457405083ce806c302a6ce464976`; backup size 176128 bytes. Historical pre-M2.1 backup SHA-256 `f8ec1a1f32f97a0b4f39eeb238c307e5a192854cdd6c4206a05a97b6a385c987` also preserved. No restore, deletion or overwrite.

After controlled application startup: SQLite schema v5 reported without error, **8/8 operator UI checks PASS**, hierarchy and six entity kinds visible, 9 entities and 8 aliases preserved including two homonymous characters with distinct IDs, 3 immutable scene revisions and 1 current head available, Ollama unavailable without disruption, no React blank screen.

The independent **read-only post-migration audit PASS**: migrations 1–5, new `narrative_facts` and `fact_sources` STRICT, required triggers/indexes, empty fact/source tables as expected, `PRAGMA foreign_key_check=[]`, `PRAGMA integrity_check=ok`, and every preexisting table count/content digest equal to the pre-v5 manifest. Current activation pointer unchanged and local source CLEAN.

Revision history SHA-256 before/after: `b5af6edaba9fc143d0c319b9408316aa61b934ed7e123241a7a43010536f71e3`.
Current head SHA-256 before/after: `8fe7aeb570f121c05083aa3cee06f95bf5fb6c98922c3357f00327ef8c708ce0`.

The fact create/read/list API and UTF-8 citation validations have passed Rust tests; **no fact editing React UI has been implemented or manually qualified**, and no canon promotion occurs.

## Remaining governance

New documentary commit invalidates historical SHA CI; require fresh terminal successful exact-head PR CI before protected implementation merge with `expected_head_sha`. Next, separate post-merge normalization PR and new exact-head CI. M2.4+, ComfyUI and AI fact extraction remain unauthorized.
