# M3.2 — S2 disposable Windows namespace, concurrency, WAL witnesses (28 October 2026)

**Candidate, not CI-qualified.** Previous [PR #206](https://github.com/LaurentCOLL1/Fabulaxiom/pull/206) **MERGED**, final source `2a9fc223a6939ad7dafb68dd6074638d2a17c034`, source Windows CI #40665933754 SUCCESS, protected squash `main=4f998e0cda4fc14897bdc729e9802de51c412004`, independent postmain #40667613911 SUCCESS. Both runs: **194 Rust / 7 Greenfield / 41 SQLite guards / 137 continuity contracts PASS**. Terminal issue #38 comment 6466081026. `Protect main` active and strict. The first source #40664955879 FAILED 5/5 disposable tests due to missing fixture parent; correction and separate CI retained, not erased.

## Authorization and narrow scope

Laurent authorized S1 and S2 **Rust preparation and strictly disposable Windows fixtures only**. This continuation adds three negative/limited witnesses to `src-tauri/src/m32_v7_admission_preflight_tests.rs` behind the existing `#[cfg(all(test, windows))]` module boundary. It does not construct `V7WriterAdmission`, open an operator path, register Tauri State or IPC, touch migration 007, native Windows Hello, backup, marker, journal or sidecars from the operator. Same logical `com.fabulaxiom.greenfield.v1` only, instantiated below a unique fresh runner temp root.

## S2 matrix additions

1. Two synchronized contenders attempt Windows `create_new(true)` on a disposable SQLite filename. Exactly one name reservation succeeds; this **does not** exclude foreign writers after reservation or seal SQLite `xOpen`.
2. Controlled rename of the fixture database parent after `EXISTING_PROFILE` preflight, followed by creation of an identically named replacement directory and main file. Both path preflights may return positive while bytes differ; unbound handoff stays `HandoffNotAtomic`. No reparse/junction guarantee is claimed: those require a separately engineered pinned-ancestor/handle mechanism.
3. Real SQLite WAL on a fresh disposable file, `BEGIN IMMEDIATE` held on one connection, another connection initially receiving a write refusal then succeeding after rollback. The `-wal`/`-shm` preflight refusal is observed while the transaction is live. This illustrates lock coordination **not absence of external writers**, crash recovery or globally sealed sidecars.

The sidecar scanner now treats *all* unexpected metadata errors as refusal, rather than treating anything other than a positive metadata lookup as absence. It is still only a filesystem-level preliminary check, not an authenticated sidecar lineage or crash-safe opener.

## Acceptance boundaries and CI

Expected on new exact SHA: **197 Rust** (194 prior + 3 Windows), **7 Greenfield**, **41 SQLite inventory guards**, **138 continuity contracts** (137 prior + new refusal contract). These are targets, never a PASS before the new Windows CI and independent postmain. Full diff/reviews/threads, active strict `Protect main`, `expected_head_sha` squash and issue #38 append-only source/terminal evidence are mandatory.

**Still not atomic**: neither the namespace path checks nor SQLite transaction locks bind a source-proven handle through `xOpen`, prevent junction/reparse swaps, prove all sidecar recovery/custody, or establish absence of another process writer. This S2 slice does **not** complete runtime admission and does not authorize S3/S4. M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, external writer `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, real G3 `STOP_UNAVAILABLE`, historical `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, #35 OPEN/DRAFT.
