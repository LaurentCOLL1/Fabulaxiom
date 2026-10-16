# M3.2 G3 — Transient Windows namespace ABA counterexample (synthetic only)

**Status: TOY COUNTEREXAMPLE; NOT AN AUTHORIZATION FOR G3.** Based on protected `main=106c48fe3b2fd8b16bd038d29c15c99ef9e5f5db`, after PR #47 CI Windows 29/29 successful (16/16 fictional G3→G4 integration tests). No operator file path, source, backup, marker or worktree is used.

The purpose of this experiment is intentionally **negative**: a before-and-after file identity comparison can observe the *same* identity even when the path refers to something different between those observations (ABA: A→B→A). The Windows original #46 run #38943063529 demonstrated a directory rename could succeed despite an open handle without FILE_SHARE_DELETE, so treating rename denial as guaranteed is incorrect.

The toy test hooks into a **disposable** G3 source observation while a test directory and test source handle are held. It attempts a temporary rename of that test root and a restoration of its original name before the next identity checkpoint. If Windows refuses the rename, the test records that result. If Windows permits it, the test demonstrates that checkpoint-only monitoring may still return `TOY_ONLY_PASS` after the folder is restored. Neither outcome proves a real ancestor path cannot be substituted. A second test creates and deletes a **fictional sidecar sentinel**, demonstrating absence at two timestamps is not proof of continuous absence. **No real hot SQLite journal is produced or recovered.**

Deterministic, OS-independent policy tests compare identical endpoints for a truly stable history versus an ABA history. A prospective authority helper always rejects real G3, without bypass for a claimed `attested` string. This is not an authentication protocol; it explicitly does **not** solve provenance.

## Production veto after this PR

- Checkpoint identity comparisons **cannot** constitute a continuous anti-rename guarantee or independent custody; parent and ancestor directories/ACL may change between checks.
- A Win32 read handle does identify the bytes that *that particular handle* reads, but it does not independently establish that the file is the intended historic source.
- In-memory `deserialize` validates a captured byte image but **cannot** establish safe physical copying during live concurrent SQLite writes. A coherent snapshot of a live database requires SQLite's transaction-aware backup APIs or an independently qualified quiescent/snapshot process.
- The former G3 NTFS destination preflight established only metadata at the observation time; no real write was carried out. No operator G3 or G4 is authorized.
- No normal production migration `007`, pointer switch, writer IPC, PR #35 merge or M3.3 until authorized gates. Historical `PENDING_EXTERNAL_ATTESTATION(21/3/2)`; prospective `NOT_STARTED`.

**Next approach:** write a bounded feasibility/veto decision for protected originals: either prove a new trust boundary (cooperating app shutdown, independently validated file handles and a snapshot mechanism, Windows directory ACL/identity policy and no conflicting writers), or keep G3 blocked. Test any alternative only on *fictional* sources before separate operator consent. Do not attempt to 'fix' ABA by just taking more path snapshots.

References: [Microsoft CreateFileW](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew), [SQLite Online Backup API](https://www.sqlite.org/backup.html), [SQLite rollback hot journals](https://sqlite.org/lockingv3.html).
