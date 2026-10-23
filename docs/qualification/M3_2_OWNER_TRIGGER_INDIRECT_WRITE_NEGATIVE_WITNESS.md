# M3.2 — Indirect trigger writer bypass: invented SQLite RAM negative witness (23 October 2026)

**TEST-ONLY / SOURCE-ONLY. NO ORIGINAL SQLITE, OPERATOR MACHINE, FILE I/O, RUNTIME IPC OR NEW MIGRATION.**

## Question tested

A token assigned by `OwnerSlot::lease()` is updated by `edit_fixture()`, but does not inherently observe writes performed by unmediated SQLite statements. The PR #137 negative test directly updated a fictional table on the same in-memory owner connection. This separate extension tests an **indirect mutation channel**: inserting into a second invented table fires a SQLite `AFTER INSERT` trigger whose body updates `invented_facts`.

The entire operation uses the existing `OwnerSlot::new_invented(6)` fixture created with `Connection::open_in_memory()`. A pre-mutation snapshot remains `Before`; after trigger execution, the old token still equals the lease and is accepted for a second Online Backup containing the changed invented value. The owner is still `Ready`, the source is in autocommit, and the destination passes the toy SQLite validation. All values and schema names are fictitious.

## Why it matters

A reviewer cannot infer that all SQLite writers participate in revision invalidation from the presence of a mutex and an audited direct update method. Indirect trigger effects must be explicitly accounted for, as must any other relevant mutation path. A completed SQLite backup provides transactional consistency, **not** an independent source provenance attestation or proof of writer exclusion.

The hypothetical `all_mutation_entrypoints_mediated=False` default added in PR #138 remains **False** and no real owner connection is authenticated. Even all-True invented policy declarations continue to yield `HYPOTHETICAL_REVIEW_ONLY` and `real_g3_authorized=False`.

## Qualification and safety

**At drafting:** PR #139 source `f9d28610bac2a97f517a39e9bceb5b0b4d85a96e`, source CI #39915173862 SUCCESS, merged protected `main=26e533c97d34ae36d25226730c7f74a7f0ee2e3f`; post-main CI #39916772343 was QUEUED_AT_CHECKPOINT. This new trigger test is a **candidate** until its exact new HEAD has a terminal CI and protected review/merge. Do not recycle #39915173862 as qualification for this new code.

M3.2 `IN_PROGRESS_NOT_ACCEPTED`; G2B global `NOT_ACCEPTED`; `SOURCE_AUTHENTICATION=PARTIAL_LOCAL_IDENTITY_ONLY`; `SQLITE_WRITER_ABSENCE=NOT_PROVEN`; G2C `NOT_AUTHORIZED`; real G3 `STOP_UNAVAILABLE`; G2B–G6 `NOT_AUTHORIZED`; historical `PENDING_EXTERNAL_ATTESTATION(21/3/2)`; prospective `NOT_STARTED`; PR #35 `OPEN/DRAFT`. No operator Windows procedure, original v6/v7 open, marker, backup, ACL, sidecar, migration 007, writer IPC, M3.3 or release.

References: [PR #137](https://github.com/LaurentCOLL1/Fabulaxiom/pull/137), [PR #138](https://github.com/LaurentCOLL1/Fabulaxiom/pull/138), [PR #139](https://github.com/LaurentCOLL1/Fabulaxiom/pull/139), [SQLite triggers](https://sqlite.org/lang_createtrigger.html), [SQLite backup API](https://sqlite.org/backup.html).
