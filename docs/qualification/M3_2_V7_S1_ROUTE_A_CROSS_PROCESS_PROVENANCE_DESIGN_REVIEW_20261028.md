# M3.2 v7 S1 — Route A cross-process provenance design review (28 October 2026)

## Authority and boundary

Document-only review. User authorized S1/S2 preparatory Rust and strictly disposable Windows fixtures, **not** a persistent marker, production journal, operator DB, S3/S4 or IPC. Base #210 terminal: source `9ecc7cb01e7ce31df1e50351d16ff38bfc5b3cf2`, source CI #40685565243 SUCCESS, protected `main=1607523d89093a5c5641b03f5905a1b9a744b92d`, independent postmain #40687117028 SUCCESS, both **203 Rust / 7 Greenfield / 41 SQLite guards / 141 continuity contracts**, issue #38 comment 6469065076. This proposal is **NOT** an admission protocol and adds **no code or operator action, no persistent marker, no Handoff authorization**.

## Why `CleanlyClosed` cannot cross a process boundary yet

An in-memory witness returned by a successful `Connection::close()` is lost when the process exits. On restart, the absence of `-wal`, `-shm` or `-journal` is not a durable close attestation: WAL cleanup/recovery can need locks and may preserve files, and the presence/absence of a file name is not the identity of the handle eventually opened by SQLite. `PRAGMA integrity_check=ok` checks structural consistency, not Fabulaxiom ownership; SQLite documents that it does not check foreign keys (separate `foreign_key_check`). A migration/user_version or owner string is also not an unforgeable signature. All such observations are inputs to a **refusal** decision, never proof of sole writer.

Official references: [SQLite WAL](https://www.sqlite.org/wal.html), [SQLite PRAGMAs](https://www.sqlite.org/pragma.html), [SQLite open flags and xOpen boundary](https://www.sqlite.org/c3ref/c_open_autoproxy.html), [SQLite transactions](https://www.sqlite.org/lang_transaction.html).

## Explicit alternatives under Route A

| Option | Evidence achievable | Unresolved assumption / risk | Decision now |
|---|---|---|---|
| **A0 — no durable evidence** | In-process clean close observation only | Cross-process EXISTING_PROFILE cannot be proven from it; restart must refuse | **Current safe default** |
| **A1 — app-owned clean-stop marker/manifest** | Might record lifecycle generation and expected schema/identity | Not authorized to implement; ordering+fsync, crash recovery, spoofing and ABA, marker/SQLite divergence, signature/key provenance unresolved | **DESIGN ONLY, authorization required** |
| **A2 — OS claim/lock over controlled private namespace** | Might coordinate cooperating Fabulaxiom processes | Lock does not bind SQLite's delegated xOpen handle or exclude privileged/foreign writers; crash release differs from proof of clean close | **DESIGN ONLY, no claim of atomicity** |
| **A3 — SQLite-owned schema/lineage and recovery checks** | Can refuse foreign schema, broken FK and some corrupted fixtures after opening | Opening precedes authentication; values can be forged, WAL recovery and sidecars require separate handling; no atomic pre-open identity | **May supplement refusals, never sole admission** |

## Conservative S1 decision contract (no code yet)

1. `NEW_ONLY`: only under a fixture-owned, controlled namespace; exclusive new-file claim must still be bound to the eventual SQLite file and sidecars. A `create_new` success by itself is insufficient.
2. `EXISTING_PROFILE` for **the same** `com.fabulaxiom.greenfield.v1`: until a separately reviewed provenance/recovery procedure exists, cross-process `CleanlyClosed` is **UNAVAILABLE_NOT_PROVEN**, even if the main DB is present and every simple path check succeeds.
3. Unknown prior exit, ambiguous WAL/SHM/journal, foreign schema/key, unexpected path/reparse, lock contention or inability to bind the real SQLite handle => **fail closed**. A single SQLite `BEGIN IMMEDIATE` may serialize a transaction, not prove exclusion of every external writer.
4. No transition to `V7WriterAdmission`, `PreparedV7Writer` runtime, Tauri State or writer IPC is permitted based on these observations. These rules **do not solve TOCTOU**, identity of the delegated `xOpen` handle, recovery authenticity or absence of other writers.

## Decision gate before further implementation

Request a distinct **design authorization** to select or combine A1/A2/A3 and define the trusted creator of the namespace, persistence ordering, crash reconciliation, exact sidecar policy, threat actor boundaries and the point where SQLite's actually-open file identity could be attested. A design authorization would **not** authorize writing an operator marker or touching live SQLite. A further **implementation authorization** would be needed for any persistent marker/protocol, followed by S1/S2 *disposable-only* tests and an independent security review before any consideration of S3/S4. Without those decisions, leave `EXISTING_PROFILE` admission STOP; do not generate another series of positive fixture PASSes interpreted as proof.

## STOP unchanged

M3.2 `IN_PROGRESS_NOT_ACCEPTED`; G2B `NOT_ACCEPTED`; external writer `NOT_PROVEN`; G2C `NOT_AUTHORIZED`; real G3 `STOP_UNAVAILABLE`; historical `PENDING_EXTERNAL_ATTESTATION(21/3/2)`; prospective `NOT_STARTED`; #35 OPEN/DRAFT. No operator execution, SQLite v6/v7, backup, ACL, sidecar, journal or marker; no migration 007, native Hello, S3/S4, Tauri IPC/CRUD. A CI pass on this document cannot qualify actual admission.
