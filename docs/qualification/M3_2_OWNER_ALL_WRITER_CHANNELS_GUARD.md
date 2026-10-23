# M3.2 — Unmediated SQLite writes: hypothetical owner gate (23 October 2026)

**SCOPE: GITHUB SOURCE-ONLY CONTRACT / NO OPERATOR FILES / NO REAL SOURCE ACCESS.**

PR #137 provided a Rust regression using an invented SQLite database exclusively in RAM: a directly committed update of the same owner connection can bypass `OwnerSlot::edit_fixture()`, leaving a `ToyLease` token and revision unchanged while a later transactionally consistent Online Backup records the new invented value. The prior backup remains consistent. This is a **negative** result about the limits of the toy's protocol, not evidence concerning an operator original.

## Added fail-closed condition

The no-I/O policy `tools/m3_2_g3_owner_runtime_contract.py` now requires the synthetic declaration `all_mutation_entrypoints_mediated` for its hypothetical `EXISTING_OWNER_SERVICE` design review. The field defaults to **False**. Even `owner_access_serialized=True`, a pre-existing owner session, and all other invented declarations being True must yield `STOP_UNPROVEN_CONDITIONS` when this field is False.

Three added pure-data negative tests cover (1) a serialized owner that fails to account for an unmediated writer, (2) the current runtime default being unproved, and (3) an independently hypothetical cold-custody path not being misrepresented as an owner service. A field set to True is **only an untrusted claim**; all-True synthetic declarations still return `HYPOTHETICAL_REVIEW_ONLY` and `real_g3_authorized=False`.

This is not a runtime wiring, writer-inventory mechanism, migration, SQL execution against the operator's database, source opener, IPC, backup or file-access permission. It cannot independently demonstrate that a real application has enumerated every writer. No change to Rust application code or Tauri registration occurs in this PR.

## Engineering consequence

A `Mutex<OwnerSlot>` serializes participants who honor the same owner object, **not** other SQLite connections, data mutation APIs, process-level I/O, or bypass paths. A real protocol would need an independently audited inventory of all code and OS-level writer paths, authenticated source identity, transaction/journal discipline, lifecycle revocation, and explicit operator-specific approval before a genuinely bounded ceremony is even proposed. SQLite Online Backup provides a consistent completed destination under documented constraints, but does not prove those prerequisites: https://sqlite.org/backup.html.

## Authoritative checkpoints

- PR #136 source `ea94377a80001fbd701ec06c7a84b7cba5b95036` with CI #39848398829 SUCCESS; protected merge `d4837f1b292f37ec4b87926bc79a7c1c999d1fbe`, postmain #39849940959 SUCCESS.
- PR #137 source `892a42e9ea0c84ab9af9fb45536d502d99252155` CI #39876891920 SUCCESS (75 Windows, 72 handoff, 132 Rust baseline, Chromium 53/53 in both modes and Rust toy negative test), protected merge `main=4d5a2bcb68dd439fac1846d354f3f808138457f1`. Postmain #39900039763 was **IN_PROGRESS_AT_CHECKPOINT** while drafting; it requires a distinct terminal read. Never rewrite that dated observation.
- This new branch must use its own exact-head CI and protected merge checks.

**Absolute STOP unchanged:** M3.2 `IN_PROGRESS_NOT_ACCEPTED`; G2B globally `NOT_ACCEPTED`; writer absence `NOT_PROVEN`; G2C `NOT_AUTHORIZED`; real G3 `STOP_UNAVAILABLE`; historical `PENDING_EXTERNAL_ATTESTATION(21/3/2)`; prospective `NOT_STARTED`; PR #35 OPEN/DRAFT. No operator Windows commands or protected v6/v7 originals, backups, marker, journals, ACLs, migration 007, new writer IPC, M3.3, ComfyUI or release.
