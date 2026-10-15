# M3.2 — Isolated IPC Preflight Contract (Stage 10)

**Status: SOURCE CANDIDATE / NEW EXACT-HEAD CI REQUIRED.** This is a
non-production **preflight only**, with **ZERO write commands and NO database
access**, not an interactive editor or approval to operate on the Windows PC.

## Authority and safety boundary

- Stage 9 exact head `d1a14aeb0703a9eb0c225ecd89be2a56d4b8b7c8` has required
  Windows [CI #38269738499](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/38269738499)
  `completed/success` (23 successful steps), confirmed on exact SHA.
- PR #35 remains open/draft/unmerged on protected `main=f7eabfea74480d307b52d4b053730021efc95352`.
- New Cargo feature `m32-isolated-preflight` is **off by default** and
  `compile_error!` forbids release builds and simultaneous M3.1 preview.
  Normal app behavior and its existing IPC command handler remain unchanged.
- The sole new Tauri command is `m32_isolated_preflight_status`, which returns
  static metadata: no SQLite handle, filesystem access, user data, Ollama or
  staging mutation. No M3.2 manual editing command is registered.
- Rust `run()` validates the effective Tauri config identity exactly matches
  `FABULAXIOM_M32_PREFLIGHT_ID` plus explicit acknowledgement
  `FABULAXIOM_M32_PREFLIGHT_ACK=M32_READONLY_PREFLIGHT_NO_DATABASE_WRITES`.
  Identity must be `com.fabulaxiom.m32gate` followed by **32 lowercase hex chars**.
  Production `com.fabulaxiom.desktop` and M3.1 `com.fabulaxiom.m31launch...`
  are rejected. This is not permission to generate or copy any operator data.
- `build.rs` uses the Tauri v2 `AppManifest` to allow exactly the one status
  command in this **feature-specific** compilation. This is necessary because
  `src-tauri/capabilities/default.json` scopes core APIs and **does not by itself
  restrict registered custom application commands**. See the official
  Tauri v2 Capabilities and Runtime Authority documentation.
- Dedicated GitHub Actions stage compiles/tests this feature under the existing
  Windows required check. No lockfile or dependencies modified.

## Explicit next gates; NOT performed in stage 10

1. Design a completely separate operator preparer using **unique** M3.2
   identity, new isolated app-local-data root, operator medium-integrity
   effective token check, symlink/reparse prevention, explicit source SHA,
   manifest digests and rollback custody; dry-run must be read-only.
2. Qualify closed consistent v7 copy, complete M3.2 schema staging on only
   a NEW isolated copy, and independent backup/digest/rollback before proposing
   a write-capable build. Never reuse an M3.1 v7 readonly identity or the
   active M1.5 restored production v6 database.
3. Add separately governed **minimal write IPC**, guarded transactions, Universe
   scope and source-revision checks, explicit non-production capability
   isolation and React manual UX. Tests should prove rejected IPC on all
   other windows and ensure Tauri command manifest matches exactly.
4. Real medium-integrity Windows debug-only launch, user acceptance,
   SQLite integrity, operator-verified post-exit digests of ALL protected
   originals plus new isolated copy, no unexpected sidecars/processes.
5. Evidence-head CI, exact-SHA guarded merge, independent M3.2 normalization.
   M3.3 and production v7 activation remain unauthorized.

**Stop conditions:** absent/mismatched config identity or operator acknowledgement,
release build, simultaneous M3.1/M3.2 features, any attempt to write before
operator custody, changed main SHA, or source CI failure. No local PowerShell
command is required to accept this source-only preflight.
