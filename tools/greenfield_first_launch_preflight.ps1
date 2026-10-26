# Route C new-projects-only metadata preflight. NO application/database launch.
# Safe intent: read source/config, target entry names and ancestor attributes only.
# PASS here is NOT native identity/ACL/quiescence proof; recheck before first launch.
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^[a-f0-9]{40}$')]
    [string] $ExpectedHead,
    [string] $CiFixtureRoot = ''
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Stop-Greenfield([string] $Reason) {
    Write-Output ("GREENFIELD_PREFLIGHT_STOP: " + $Reason)
    exit 2
}
try {
    if ([Environment]::OSVersion.Platform -ne [PlatformID]::Win32NT) {
        Stop-Greenfield 'Windows only'
    }
    $repo = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
    $normal = Join-Path $repo 'src-tauri/tauri.conf.json'
    $profile = Join-Path $repo 'src-tauri/tauri.greenfield.conf.json'
    if (-not (Test-Path -LiteralPath $normal -PathType Leaf) -or
        -not (Test-Path -LiteralPath $profile -PathType Leaf)) {
        Stop-Greenfield 'expected Tauri configuration source missing'
    }
    $normalConfig = Get-Content -LiteralPath $normal -Raw -Encoding UTF8 | ConvertFrom-Json
    $profileConfig = Get-Content -LiteralPath $profile -Raw -Encoding UTF8 | ConvertFrom-Json
    $defaultId = 'com.fabulaxiom.desktop'
    $greenfieldId = 'com.fabulaxiom.greenfield.v1'
    if ($normalConfig.identifier -cne $defaultId -or
        $profileConfig.identifier -cne $greenfieldId -or
        $normalConfig.identifier -ceq $profileConfig.identifier) {
        Stop-Greenfield 'Tauri identifier drift / protected profile collision'
    }
    if ($profileConfig.bundle.active -ne $false -or
        $profileConfig.app.windows.Count -ne 1 -or
        $profileConfig.app.windows[0].title -cnotmatch 'PROJETS NEUFS') {
        Stop-Greenfield 'development-only visible title and disabled bundle required'
    }
    if ($null -ne $normalConfig.app.PSObject.Properties['appDirectoriesOverride'] -or
        $null -ne $profileConfig.app.PSObject.Properties['appDirectoriesOverride']) {
        Stop-Greenfield 'appDirectoriesOverride is forbidden'
    }
    if ($null -ne $profileConfig.PSObject.Properties['build'] -or
        $null -ne $profileConfig.PSObject.Properties['plugins']) {
        Stop-Greenfield 'greenfield may not override build/plugins'
    }
    foreach ($command in @('git', 'node', 'npm', 'cargo', 'rustc')) {
        if ($null -eq (Get-Command -Name $command -ErrorAction SilentlyContinue)) {
            Stop-Greenfield ("missing required command: " + $command)
        }
    }

    # An exact Git commit must be provided by the independent postmain checkpoint.
    # Disable Git's optional index refresh/write. No checkout, fetch or pull.
    $oldGitOptionalLocks = $env:GIT_OPTIONAL_LOCKS
    try {
        $env:GIT_OPTIONAL_LOCKS = '0'
        $head = [string]((& git -C $repo rev-parse HEAD) | Select-Object -First 1)
        if ($LASTEXITCODE -ne 0 -or $head -cne $ExpectedHead) {
            Stop-Greenfield 'Git checkout is not the approved exact SHA'
        }
        $status = @(& git -C $repo status --porcelain --untracked-files=all)
        if ($LASTEXITCODE -ne 0 -or $status.Count -ne 0) {
            Stop-Greenfield 'working tree is not clean'
        }
    }
    finally {
        $env:GIT_OPTIONAL_LOCKS = $oldGitOptionalLocks
    }

    $fixture = -not [string]::IsNullOrWhiteSpace($CiFixtureRoot)
    if ($fixture) {
        # Only permitted for a disposable GitHub Actions Windows runner fixture.
        if ($env:GITHUB_ACTIONS -cne 'true' -or
            [string]::IsNullOrWhiteSpace($env:RUNNER_TEMP)) {
            Stop-Greenfield 'CI fixture override is unavailable outside GitHub Actions'
        }
        $runnerTemp = [IO.Path]::GetFullPath($env:RUNNER_TEMP).TrimEnd('\', '/')
        $root = [IO.Path]::GetFullPath($CiFixtureRoot).TrimEnd('\', '/')
        if (-not $root.StartsWith(($runnerTemp + '\'), [StringComparison]::OrdinalIgnoreCase) -or
            -not [IO.Path]::GetFileName($root).StartsWith('fabulaxiom-ci-greenfield-preflight-', [StringComparison]::Ordinal)) {
            Stop-Greenfield 'CI fixture root must be a unique child of RUNNER_TEMP'
        }
    }
    else {
        $principal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
        if ($principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
            Stop-Greenfield 'do not use an elevated Windows operator process'
        }
        $root = [Environment]::GetFolderPath([Environment+SpecialFolder]::LocalApplicationData)
        $environmentRoot = [Environment]::GetEnvironmentVariable('LOCALAPPDATA')
        if ([string]::IsNullOrWhiteSpace($root) -or
            [string]::IsNullOrWhiteSpace($environmentRoot) -or
            -not [string]::Equals([IO.Path]::GetFullPath($root).TrimEnd('\', '/'),
                                 [IO.Path]::GetFullPath($environmentRoot).TrimEnd('\', '/'),
                                 [StringComparison]::OrdinalIgnoreCase)) {
            Stop-Greenfield 'LocalApplicationData known-folder and environment mismatch'
        }
        $root = [IO.Path]::GetFullPath($root).TrimEnd('\', '/')
    }
    if ($root -notmatch '^[a-zA-Z]:\\' -or
        -not (Test-Path -LiteralPath $root -PathType Container)) {
        Stop-Greenfield 'local root is not an accessible ordinary drive directory'
    }
    # Refuse links/junctions in EVERY existing ancestor; no recursion or file reads.
    $cursor = $root
    while ($true) {
        $item = Get-Item -LiteralPath $cursor -Force -ErrorAction Stop
        if (-not $item.PSIsContainer -or
            (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0)) {
            Stop-Greenfield 'ancestor is not a plain directory (reparse or file)'
        }
        if ([string]::Equals($cursor, [IO.Path]::GetPathRoot($cursor),
                             [StringComparison]::OrdinalIgnoreCase)) {
            break
        }
        $parent = [IO.Directory]::GetParent($cursor).FullName
        if ([string]::IsNullOrEmpty($parent) -or
            [string]::Equals($parent, $cursor, [StringComparison]::OrdinalIgnoreCase)) {
            break
        }
        $cursor = $parent
    }

    # The immediate directory-entry enumeration catches an existing or dangling
    # Greenfield leaf, including a symlink/junction. No traversal into any entry.
    $entries = @(Get-ChildItem -LiteralPath $root -Force -ErrorAction Stop |
        Where-Object { [string]::Equals($_.Name, $greenfieldId, [StringComparison]::OrdinalIgnoreCase) })
    if ($entries.Count -ne 0) {
        Stop-Greenfield 'Greenfield root entry already exists (including reparse): do not reuse'
    }
    if (@(Get-Process -Name 'fabulaxiom' -ErrorAction SilentlyContinue).Count -gt 0) {
        Stop-Greenfield 'Fabulaxiom process observed; stop it and reassess'
    }
    $driveRoot = [IO.Path]::GetPathRoot($root)
    $freeBytes = ([IO.DriveInfo]::new($driveRoot)).AvailableFreeSpace
    if ($freeBytes -lt 2147483648) {
        Stop-Greenfield 'less than 2 GiB free; stop before development compilation'
    }
    $candidatePath = Join-Path $root $greenfieldId
    Write-Output ("GREENFIELD_PREFLIGHT_METADATA_ONLY_CANDIDATE: " + $ExpectedHead)
    Write-Output ("GREENFIELD_CANDIDATE_PATH: " + $candidatePath)
    Write-Output 'GREENFIELD_SOURCE_IDENTITY: DISTINCT_DEV_ONLY'
    Write-Output 'GREENFIELD_ROOT_ENTRY: ABSENT_AT_SAMPLE_TIME'
    Write-Output 'GREENFIELD_ANCESTOR_REPARSE: NONE_OBSERVED'
    Write-Output 'GREENFIELD_LIMITS: no atomic reservation; no native handle/ACL or future-write guarantee; no Tauri or SQLite opened'
    Write-Output 'GREENFIELD_NEXT: manual WebView2/Build Tools review and separately controlled launch'
}
catch {
    Stop-Greenfield ("inspection error line " + $_.InvocationInfo.ScriptLineNumber + ": " + $_.Exception.GetType().Name + " / " + $_.Exception.Message)
}
