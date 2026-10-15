# M3.2 Stage 12 — Four-root custody inventory (SOURCE CANDIDATE)

**NOT YET QUALIFIED by new exact-head CI. NOT AUTHORIZED for operator use.**

Stage 11 at exact PR #35 SHA 2ed947f2d2c13c74e150054a7dfbeb5153186134 passed Windows pull_request CI #38294992362 (completed/success, 25/25). The operator subsequently reported: restored local clean main, medium/non-admin token, unchanged M1.5 active v6 pointer and 11/11 M3.1 protection hashes; pre-M2.1/M2.3 and both distinct named pre-M2.4 v5 backups matched historical SHA; M2.5 isolated pre-fact and app-managed snapshots matched; M3.1 root owner, protected inheritance, single scoped user Modify ACE and four inherited descendants passed without writes.

The two archived ACL file hashes and the earlier pre-M2.4 manifest SHA have **recent observation only**, not an independently authenticated historical hash. Latest scripts did not repeat full SQLite integrity/FK tests or complete manifest semantic checks.

## Source-only four-root inspector

tools/m3_2_multiroot_readonly.py is a separate opt-in --dry-run script; the pre-existing Stage 11 gate is unchanged. It reuses Stage 11's medium Windows token, exact Git, safe-path and streaming SHA-256 helpers.

An operator-supplied pre-existing UTF-8 JSON manifest is required: protocol fabulaxiom_m32_multiroot_custody_v1; expected_head; expected_main; protected_files. Each file record consists of exactly root, role, path, sha256, and authority (historical or observed). The root IDs are production, m25, m31, and acl, mapped via explicit command arguments to these **pre-existing** directory identities:

- production: com.fabulaxiom.desktop, including real M1.5 active marker and restored v6, M2 backups and M3.1 safety/third/fourth copies and manifests
- m25: com.fabulaxiom.m25qual35fb842c, including existing separate isolated v6 and its pre-fact backup/manifest
- m31: com.fabulaxiom.m31launch followed by exactly 32 lowercase hexadecimal digits, including existing isolated candidate v7 and its config/manifest
- acl: Fabulaxiom-M31-ACL-Evidence-4d520e18, separate from application-local data, containing original-acls.txt and pre-repair-evidence.json

The caller must also supply an already independently recorded manifest SHA-256. The tool never makes a trusted checksum from the manifest currently under inspection. However it **cannot independently verify the claimed historical origin of each hash**; this remains an operator governance obligation. In particular, do not promote merely observed ACL hashes to historical just to get a stronger status.

The exact required role set rejects omissions, duplicate roles, duplicate paths and root confusion. Two differently named backups with the same content SHA are legitimate; there is no single-by-hash selection. Every path and ancestor is checked for reparse points, symlinks or junctions. Wrong SHA, sidecars, unsafe paths, wrong Git HEAD, dirty worktree, stale origin/main, mismatched M1.5 selected marker, wrong ACL metadata or occupied proposed M3.2 identity all fail closed.

## Return status and limits

- PENDING_HISTORICAL_AUTHORITY: file digests match but one or more entries have observed-only authority.
- VERIFIED_SCOPE_ONLY: all digests match and all manifest entries claim external historical authority; this remains **NOT staging approval** and is not independently attested by this script.
- FAIL: mandatory source or custody condition failed.

The result always carries m32_staging_authorized=false. No --prepare, no --write, no SQLite connections, no Tauri launch, no ACL modification and no automatic migration 007. The tool cannot itself qualify backup restore fitness, manifest semantics, current Windows ACL history or authenticated external references. No real Windows operator invocation is yet approved.

## Synthetic CI and next gate

tools/test_m3_2_multiroot_readonly.py covers only newly created disposable directories. It tests complete scope, duplicate-content distinct backup filenames, observed authority, failed digest, missing/duplicate role, path traversal, wrong scope, stale source/token, SQLite sidecars, occupied identity, M1.5 pointer and archived ACL metadata. The required Windows workflow gains a dedicated test step; lockfiles and production runtime are unchanged.

Before any operator run: re-fetch PR #35 head/main, obtain new exact-head terminal Windows CI, review its check steps, independently establish archive/manifest authority, and approve a separate read-only Windows gate. Only later may an independently protected new M3.2 candidate v7 copy/rollback preparer be proposed. M3.1 read-only identity is never reused for writing. PR #35 remains DRAFT/unmerged, M3.3+ prohibited.

References: Python 3.12 pathlib Windows junction and stat documentation; Microsoft icacls /save versus /restore and Get-Acl; governed Fabulaxiom M3 roadmap.
