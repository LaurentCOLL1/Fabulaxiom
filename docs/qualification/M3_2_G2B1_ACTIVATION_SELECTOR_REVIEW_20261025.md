# Fabulaxiom M3.2 — G2-B1 : selector M1.5 metadata and tiny marker read proposal
**25 October 2026 — SOURCE-ONLY PROPOSAL. NOT RUN ON THE OPERATOR'S WINDOWS HOST.**

## Exact bounded scope and authorization boundary

Following the operator-reported B0 result (M1.5 four `.sqlite3` filenames, M2.5 one; `OBSERVED_PARTIAL_ONLY`), the minimum new evidence is to follow **only the M1.5 activation selector** implemented in `src-tauri/src/backup.rs::resolve_active_database_path` and determine whether it resolves to exactly one filename among those four. This does **not** establish authenticity of that SQLite, original historical role, stable file identity, no writer or G2B acceptance.

**New access versus B0:** this candidate **reads the content of one small activation marker file** (up to 256 bytes, size checked first), into memory, to recognize the restored database *filename*. The marker itself is protected material. No SQLite bytes, hashes, ACLs, content rows or source SQL opening. No modification of marker or SQLite, no copying/moving/deleting, no process stop/start, network, escalation, or recording file output. The script lists process names, parent directory attributes and immediate child filenames; checks for known SQLite sidecar names; selects greatest valid activation marker filename, as in the Rust code; validates target against exactly one listed SQLite filename. It outputs **only integer counts and enum labels**, never actual private filenames, paths, marker bytes or user text.

**Environment/interactions:** standard non-admin Windows PowerShell 5+, ordinary non-elevated session; paste once then Enter; no `q`, password or UAC; no termination of processes. If a service, application or writer might still be active, if B0 count drifted, any relevant reparse point/sidecar appears, a marker is ambiguous/bad, or any error occurs: STOP. Do not retry automatically, do not repair anything. OS filesystem telemetry, access-time or journal side effects of metadata/content reads cannot be excluded. The observations are not atomic, and the `Get-Item` / `Get-ChildItem` interface does not retain Win32 FileId-holding handles.

**Informed specific consent required:** the owner's statement authorizing future procedures is a broad intent, not evidence that the owner reviewed this exact marker-content read and its effects. The already consumed B0 consent is not reused. Do not execute merely because this text passes CI. A separate explicit acknowledgment of this specific block and scope must precede the first use.

## Exact operator candidate — review text ONLY, never executed in GitHub CI

```powershell
& {
  $ErrorActionPreference = 'Stop'
  $stage = 'ENVIRONMENT'
  try {
    if ([Environment]::OSVersion.Platform -ne [PlatformID]::Win32NT) { throw 'WINDOWS_REQUIRED' }
    if ($PSVersionTable.PSVersion.Major -lt 5) { throw 'POWERSHELL_UNSUPPORTED' }
    if ([string]::IsNullOrWhiteSpace($env:LOCALAPPDATA)) { throw 'LOCALAPPDATA_MISSING' }
    $stage = 'PROCESS_METADATA'
    $running = @(Get-Process -ErrorAction Stop)
    if (@($running | Where-Object {
      $_.ProcessName -ieq 'Fabulaxiom' -or $_.ProcessName -ieq 'ollama'
    }).Count -gt 0) { throw 'APP_OR_OLLAMA_PRESENT' }

    $stage = 'PRODUCTION_DIRECTORY_METADATA'
    $dir = [IO.Path]::GetFullPath([IO.Path]::Combine(
      $env:LOCALAPPDATA, 'com.fabulaxiom.desktop', 'database'))
    $cursor = $dir
    while ($true) {
      $item = Get-Item -LiteralPath $cursor -Force -ErrorAction Stop
      if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
        throw 'REPARSE_ANCESTOR'
      }
      $parent = [IO.Directory]::GetParent($cursor)
      if ($null -eq $parent) { break }
      $cursor = $parent.FullName
    }
    $root = Get-Item -LiteralPath $dir -Force -ErrorAction Stop
    if (-not $root.PSIsContainer) { throw 'NOT_DIRECTORY' }
    $children = @(Get-ChildItem -LiteralPath $dir -Force -ErrorAction Stop)
    if (@($children | Where-Object {
      ($_.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0
    }).Count -ne 0) { throw 'REPARSE_CHILD' }
    if (@($children | Where-Object {
      $_.Name -match '(?i)\.sqlite3-(wal|shm|journal)$'
    }).Count -ne 0) { throw 'SQLITE_SIDECAR_SEEN' }
    $sqlite = @($children | Where-Object {
      -not $_.PSIsContainer -and $_.Name -match '(?i)\.sqlite3$'
    })
    if ($sqlite.Count -ne 4) { throw 'B0_COUNT_DRIFT' }

    $stage = 'ACTIVATION_DIRECTORY_METADATA'
    $activationDirs = @($children | Where-Object { $_.Name -ceq 'activations' })
    if ($activationDirs.Count -gt 1) { throw 'AMBIGUOUS_ACTIVATION_DIR' }
    $markers = @()
    if ($activationDirs.Count -eq 1) {
      if (-not $activationDirs[0].PSIsContainer) { throw 'ACTIVATION_NOT_DIRECTORY' }
      $activation = [IO.Path]::Combine($dir, 'activations')
      $items = @(Get-ChildItem -LiteralPath $activation -Force -ErrorAction Stop)
      if (@($items | Where-Object {
        ($_.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0
      }).Count -ne 0) { throw 'REPARSE_MARKER' }
      $markers = @($items | Where-Object {
        -not $_.PSIsContainer -and
        $_.Name -cmatch '^activation-[0-9]{32}-[0-9]{10}-[0-9]{10}\.active$'
      } | Sort-Object -Property Name -Descending -CaseSensitive)
    }
    $stage = 'SELECTOR_METADATA'
    $selectedName = 'fabulaxiom.sqlite3'
    $selectorKind = 'DEFAULT'
    if ($markers.Count -gt 0) {
      $marker = $markers[0]
      if ($marker.Length -lt 1 -or $marker.Length -gt 256) { throw 'MARKER_SIZE' }
      # Only the selected tiny activation pointer is read, never SQLite bytes.
      $selectedName = [IO.File]::ReadAllText($marker.FullName).Trim()
      if ($selectedName -cnotmatch '^fabulaxiom-restored-[0-9]{32}-[0-9]{10}-[0-9]{10}\.sqlite3$') {
        throw 'INVALID_MARKER_TARGET'
      }
      $selectorKind = 'RESTORED'
    }
    $matches = @($sqlite | Where-Object { $_.Name -ceq $selectedName })
    if ($matches.Count -ne 1) { throw 'SELECTED_FILENAME_NOT_UNIQUE' }
    if (($matches[0].Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
      throw 'SELECTED_FILE_REPARSE'
    }
    Write-Output "G2B1_PRODUCTION_SQLITE_FILENAME_COUNT: $($sqlite.Count)"
    Write-Output "G2B1_ACTIVATION_MARKER_COUNT: $($markers.Count)"
    Write-Output "G2B1_SELECTOR_KIND: $selectorKind"
    Write-Output 'G2B1_SELECTED_FILENAME_MATCH: ONE_OBSERVED'
    Write-Output 'G2B1_SELECTOR_OBSERVATION: OBSERVED_PARTIAL_ONLY'
  }
  catch {
    Write-Output 'G2B1_SELECTOR_OBSERVATION: STOP'
    Write-Output "STOP_STAGE: $stage"
    Write-Output 'STOP_REASON: UNEXPECTED_OR_UNSAFE'
  }
  Write-Output 'G2B_SOURCE_IDENTITY: PARTIAL_LOCAL_IDENTITY_ONLY'
  Write-Output 'SQLITE_WRITER_ABSENCE: NOT_PROVEN'
  Write-Output 'M25_M31_V7_OTHER_ROLES: NOT_ASSESSED'
  Write-Output 'G2C_G2D_G3_G4_G5_G6: NOT_AUTHORIZED'
  Write-Output 'HISTORICAL: PENDING_EXTERNAL_ATTESTATION(21/3/2)'
  Write-Output 'PROSPECTIVE: NOT_STARTED'
}
```

## Expected private result and limits

- `G2B1_SELECTOR_KIND: RESTORED` with `G2B1_SELECTED_FILENAME_MATCH: ONE_OBSERVED`: the latest syntactically accepted activation marker's **read content** is a restored name present among the observed four SQLite filenames. This does not establish its on-disk version, last modification, object identity or writer exclusion.
- `G2B1_SELECTOR_KIND: DEFAULT`: no syntactically valid marker was selected; the default `fabulaxiom.sqlite3` name appears once, *not* a proof that the restored production role is selected.
- `STOP`: do not rerun, repair, remove journals, change activation, read SQLite or proceed to G2C/G3.
- All outputs including success explicitly retain `G2B_SOURCE_IDENTITY: PARTIAL_LOCAL_IDENTITY_ONLY`, `SQLITE_WRITER_ABSENCE: NOT_PROVEN`, `G2C_G2D_G3_G4_G5_G6: NOT_AUTHORIZED`, historical `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`. M2.5/M3.1 remain unassessed by B1.

**Source alignment:** `MARKER_PREFIX=activation-`, `RESTORED_PREFIX=fabulaxiom-restored-`, `DATABASE_FILENAME=fabulaxiom.sqlite3`; Rust sorts accepted marker filenames descending and reads only the first one, then `trim()` and validates the restored filename pattern. Purely lexical ASCII digit token checks; no numerical token parsing.

**Known limitations:** `Sort-Object` collation is not a proof of exact equivalence to Rust bytewise order for arbitrary names; fixed-width ASCII digits are required for candidate acceptance. A local file/marker can be swapped between listing and the small marker read or after it; the selected name is merely an observed string. The script's visible sidecar checks are instantaneous and cannot prove quiescence. Standard Windows/SQLite source-custody cautions still apply. Official reference: https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew and https://www.sqlite.org/wal.html.

**No automatic promotion:** `G2B1=PREPARED_NOT_EXECUTED`; `G2B=NOT_ACCEPTED`; real G3 `STOP_UNAVAILABLE`; M3.2 `IN_PROGRESS_NOT_ACCEPTED`; PR #35 `OPEN/DRAFT`. No original databases, sidecars or marker read by the CI, which may only parse this text.
