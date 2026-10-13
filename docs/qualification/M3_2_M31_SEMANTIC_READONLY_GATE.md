# M3.2 Stage 14 — M3.1 archival manifest semantic cross-check

**NEW SOURCE CANDIDATE; requires own exact-head Windows CI. No real operator execution is approved.**

Stage 13 source head `5e5d76141cbf7fbb69954beefe0acbfb822da6d0` qualified with [pull_request Windows CI #38339487476](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/38339487476), completed/success 27/27 job steps. Protected `main=f7eabfea74480d307b52d4b053730021efc95352` unchanged. The source-anchored four-root custody prototype still returns PENDING_EXTERNAL_ATTESTATION and cannot issue a write authorization.

## Scope of this stage

The existing Stage-13 gate compares file bytes to source-pinned digests and marks five roles as observed or unanchored. Even a file with a historically known SHA is not a substitute for checking its **internal declared relationships**. Stage 14 adds `tools/m3_2_m31_semantic_readonly.py`, an opt-in read-only *additional* check of five previously SHA-pinned archived M3.1 JSON documents:

- M3.1 source v6 backup and separate restore rehearsal `manifest.json`
- M3.1 third-copy candidate v7 `candidate-v7-manifest.json`
- M3.1 fourth-copy forced rollback `rollback-manifest.json`
- Isolated M3.1 preparation `preparation-manifest.json`
- Isolated read-only Tauri `tauri.m31.isolated.conf.json` overlay

All five are checked by exact source-pinned pathname and SHA both before and after JSON reads. Synthetic validator checks the M1.5 restored-active filename and v6 source digest, stable logical v1 algorithm/digest, v6 backup+restore names, expected schema versions, integrity/FK evidence labels, old 14-table count inventory, candidate 007 SQL SHA and third-v7 digest, rollback primary-key error and exact source v6 byte SHA, no production migration/activation and no Tauri launch. It validates that the M3.1 isolated overlay identifier matches the original M3.1 identity, bundle stays inactive and the preparation document points to the source-pinned overlay SHA.

**Evidence distinction:** These are semantics of historical JSON **assertions**, not a fresh SQLite integrity check or a proof that a database is restorable. Stage 14 opens NO SQLite connection. In particular SQLite `PRAGMA integrity_check` does not check foreign keys; any future separately authorized database audit must run `foreign_key_check` as well (SQLite official reference). The backup source is never opened and no WAL sidecar is created/removed. ACL archived bytes and the earlier M2.4 manifest remain observed only, regardless of this result.

## Adversarial and acceptance behavior

New `tools/test_m3_2_m31_semantic_readonly.py` has 16 synthetic cases: valid historical claim chain, altered identities, source SHA, backup/restore and logical digests, negative/non-integer table counts, boolean-vs-integer bypass, third-copy wrong sealed manifest or migrated-production flags, failed-rollback evidence, active Tauri overlay, missing JSON, changed bytes and parent-gate bypass. Tests use only synthetic dicts and disposable temporary files; the workflow adds one dedicated Windows step, without changing lockfiles or Tauri runtime.

Even if all five historical documents are internally consistent, the only outcome is `PENDING_EXTERNAL_ATTESTATION`; CLI returns nonzero 2. It is **not** a failure of synthetic CI, but a deliberate NO-READY barrier for incomplete original-source/ACL provenance. Real operator invocation is NOT approved until new exact-head CI and a separately reviewed manifest-and-Windows preflight ceremony.

Production M1.5 restored SQLite stays at v6; M3.1 read-only copy, M2.5 separate fixture, historical backups and ACLs untouched. No auto-registration of migration 007, no new M3.2 identity, no writable IPC/UI, no PR merge and no M3.3.
