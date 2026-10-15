# M3.2 Stage 17 — Activation-marker uniqueness and true-hash test hardening

**Source candidate: exact-head Windows CI required. No live operator run approved.**

## Stage 16 accepted authority

PR #35 source `fc1a25e411a0a22a337a5a2eb995f58a70ffff52` passed [Windows pull_request CI #38411230384](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/38411230384), `completed/success`, **29/29 steps**. Protected `main=f7eabfea74480d307b52d4b053730021efc95352` remained unchanged; PR #35 OPEN/DRAFT/unmerged. Stage 16 established source-pinned 26-role, four-root, manifest-free SHA-256 comparisons using 21 independently historically recorded values, 3 recent observations and 2 unanchored records.

## Correctness gap closed

Stage 16 checked the known historical M1.5 activation marker and its selected restored-active v6 database, but did not rule out **an additional or newer activation marker in the same directory**. M1.5 runtime may select a newer matching marker, making the historical marker's SHA comparison insufficient to assert unchanged *effective active selection*. Source-only Stage 17 adds `enforce_activation_inventory` to `tools/m3_2_direct_custody_readonly.py`: inspect original activation directory without writing; refuse any extra `activation-*` or `*.active` entry, require exactly the source-pinned marker filename, and verify it is regular, non-reparse. Repeat this inventory once at the end after hashing and archived JSON checks, so a newly introduced second marker is detected rather than silently ignored.

## Synthetic Windows acceptance

Extend the separate `tools/test_m3_2_direct_custody_readonly.py` suite from 18 to **24** isolated synthetic tests. New cases check a newer valid-shaped marker, an extra `*.active` file, an extra marker introduced between the first and final scans, the exact single-marker success path, a **real file-hash** integration test with solely disposable synthetic digests, and a real-hash extra-marker refusal. Earlier synthetic mock-SHA unit tests remain. No file is written in the protected operator installation; any fixture writes occur only in disposable, self-generated directories during CI.

All protected scope and status boundaries are unchanged: four historical roots, 26 roles, two byte-identical separately named v5 backups, 21 historically pinned hashes, 3 recent observations and 2 unanchored SHA values. Regardless of check outcome, there is **no staging or write approval**; the only non-FAIL status remains `PENDING_EXTERNAL_ATTESTATION` and CLI exit code 2. No create/mkdir, SQLite connection, Tauri launch, live ACL change, migration 007 or production activation.

## Qualification gate

Stage 17 requires its own exact-new-HEAD `pull_request` Windows CI and all steps terminal success. The old 29/29 Stage-16 result is not transferable. Review actual Windows operator preflight independently before any real PC invocation. Evidence for the archived ACL files remains only recently observed, and M1.5 marker and isolated M2.5 v6 remain unanchored; no automatic promotion to historical authority. The app source production cap stays schema v6, PR #35 DRAFT, and M3.3+ blocked.
