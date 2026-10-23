# Fabulaxiom M3.2 — Rust owner-token unmediated-write negative witness (23 October 2026)

**SOURCE-ONLY / GITHUB CI / TEST-ONLY RAM SQLITE. NO REAL OPERATOR DB ACCESS OR NEW RUNTIME ENDPOINT.**

## Hypothesis falsified

In the existing `src-tauri/src/m32_owner_lifecycle_toy.rs` toy, a `ToyLease` contains a session ID and revision. The `OwnerSlot::edit_fixture()` method increments the revision and correctly invalidates earlier tokens. That protection is **conditional** on all writes passing through the owner interface.

The new synthetic Rust test `m32_owner_lifecycle_unmediated_valid_write_does_not_revoke_old_ticket_negative_witness` deliberately uses the **already-owned invented in-memory SQLite connection** to execute an otherwise valid SQL update *without* `edit_fixture()`. It checks:
1. a snapshot taken before the update still reports `Before`;
2. after an unmediated valid update, the issued lease has **not** changed;
3. a second online backup under the stale lease is still permitted and returns the new invented fact;
4. the owner remains `Ready`; SQLite snapshot consistency does not prove writer exclusion or token provenance.

This is a **negative regression**: its success means an assumption is disproved, not that an original database is safe. No source path, `Connection::open(path)`, marker, backup, file handle, IPC handler, application launch or operator data is involved. The Rust file is already included only through the compile-time `#[cfg(all(test, feature = "m32-g3-owned-ram-toy"))]` guard; default builds and Tauri IPC remain unchanged. The new test executes under the existing Windows CI feature-gated toy test step; the suite total must be verified on the **new exact commit**.

## Consequence for architecture

- A revision token or a `Mutex<OwnerSlot>` enforces sequencing only for participants using the owner protocol; it is **not** a filesystem or cross-process writer-exclusion guarantee.
- SQLite Online Backup guarantees the consistency of its completed destination snapshot under its documented constraints, but does not by itself authenticate a source, prohibit concurrent writers or prove that owner-defined revisions tracked every edit. See [SQLite Backup API](https://www.sqlite.org/backup.html) and [Online Backup API C reference](https://sqlite.org/c3ref/backup_finish.html).
- Before a real G3 proposal, prove independently that the pre-existing non-migrating owner connection is bound to the authenticated protected source and that all relevant mutation paths, lifetimes and journal state are controlled. The current Rust runtime does not establish such a persistent owner.
- Maintain rejection when authentication is absent; **do not use this negative witness to add a real source opener** or authorize a capture attempt.

## Status

The owner-reported metadata/marker/FileId G2-B results remain local, partial, not independently attested. `SOURCE_AUTHENTICATION=PARTIAL_LOCAL_IDENTITY_ONLY`; `SQLITE_WRITER_ABSENCE=NOT_PROVEN`; G2-B global `NOT_ACCEPTED`; G2-C `NOT_AUTHORIZED`; G3 real `STOP_UNAVAILABLE`; M3.2 `IN_PROGRESS_NOT_ACCEPTED`; historical evidence `PENDING_EXTERNAL_ATTESTATION(21/3/2)`; prospective baseline `NOT_STARTED`; PR #35 `OPEN/DRAFT`.

**Checkpoint at drafting:** protected PR #136 merged on `main=d4837f1b292f37ec4b87926bc79a7c1c999d1fbe`, source CI #39848398829 SUCCESS, post-main CI #39849940959 SUCCESS (75/75 Windows steps), confirmed by separate live refetch. The present new candidate is not qualified or merged until its own terminal exact-HEAD CI and protected review.
