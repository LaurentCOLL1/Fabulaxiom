# M3.2 Stage 11 — Post-restart Windows operator read-only gate

**SOURCE CANDIDATE / new exact-head Windows CI required.** This stage
introduces `tools/m3_2_operator_readonly_gate.py` and ONLY a `--dry-run`
operation. There is **NO --prepare or --write option**. There is no copy,
no SQLite connection, no directory creation, no Tauri launch, no user-data
migration, no local environment alteration, and no permissions change.

## Why separate from M3.1?

M3.1's existing preparer uses the `com.fabulaxiom.m31launch...` identity
and a read-only preview contract, so it must **never** be repurposed as an
M3.2 editor. The M3.2 stage-10 source feature is still a stateless
one-command-only preflight and has NO writable IPC. After a reboot, Windows
token/drive/process state is not presumed to persist.

## Mandatory live checks before any operator action

1. In Windows, **Win+R → `cmd.exe /d` → Enter**, NOT Ctrl+Shift+Enter;
   then in cmd run
   `"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -NoLogo`.
   Verify effective token not admin and integrity SID `S-1-16-8192`,
   no High SID `S-1-16-12288`. Stop if uncertain.
2. Re-fetch GitHub `main`, PR #35 and its exact HEAD/checks before any
   changes. The local clean detached/feature source worktree must match
   both the expected source HEAD and current origin/main tracking SHA.
3. Confirm Tauri/Fabulaxiom truly stopped (and independently inspect Ollama
   if later relevant). Check restored M1.5 v6 active pointer and all old
   protected backups with an **already independent, pre-recorded** SHA
   manifest. Do not compute expected hashes from damaged inputs.
4. Proposed `com.fabulaxiom.m32gate<32 lowercase hex>` must NOT already
   exist. No M3.1 identifier and no production identifier are acceptable.
   The source-only dry-run checks availability; it NEVER reserves it.
5. The protected SHA manifest is an operator-owned UTF-8 JSON object:
   `{"protocol":"fabulaxiom_m32_protected_sha_manifest_v1",
       "protected_files":[
         {"path":"database/fabulaxiom.sqlite3","sha256":"<independently recorded 64 lowercase hex>"},
         {"path":"activation-marker.json","sha256":"<independently recorded 64 lowercase hex>"}
       ]}`
   These paths are **illustrative only**, not a claim that real files
   exist with those names. Before use, identify the actual filenames and
   include the active DB, marker and *all* protected custody artifacts.
   Paths are strictly relative to the genuine `com.fabulaxiom.desktop`
   app-local-data root and may not escape it. Any external custody root
   requires a separately governed enhancement; this gate does not verify
   files outside its approved scope.
6. Run the gate with explicit paths/hashes/HEAD and `--ack-app-stopped
   --dry-run`. Missing or mismatched files/SHA, unsafe path links/junctions,
   elevated/non-medium token, dirty source, stale origin/main and reused
   identity produce **FAIL**. READY only reports read-only eligibility for
   a future separate operator preparation review; it is NOT write approval.
7. On a future operator request, first provide a full non-admin PowerShell
   `& { ... }` preflight. Warn before interactive controls (`q`,
   `Ctrl+C`, UAC prompts); none are expected for this source-only gate.
   No local PowerShell execution is needed now.

## Synthetic CI acceptance

The new Windows test suite uses only disposable directory fixtures,
mocked Git identity and mocked Windows token results; it verifies success
has no file mutation and failure leaves old files untouched for elevated
tokens, stale/dirty refs, SHA mismatch, unsafe paths, duplicate/missing
manifests, or an occupied identity.

The source HEAD for stage 10 `4d3f571443ed31105b351ee0e0427efc20bf569e`
was already qualified by [Windows CI #38293132998](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/38293132998),
24/24 steps SUCCESS. **Stage 11 requires a new exact-head CI.**
No production v7 activation, app writes, real Windows operator identity,
M3.1 preview updates, M3.3 or implementation PR merge is authorized.
