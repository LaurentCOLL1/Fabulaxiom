# On a disposable CI runner ONLY. The B1 block is NEVER invoked.
$ErrorActionPreference = 'Stop'
$document = Get-Content -LiteralPath 'docs/qualification/M3_2_G2B1_ACTIVATION_SELECTOR_REVIEW_20261025.md' -Raw -Encoding UTF8
$lines = @($document -split '\r?\n')
$opening = ([char]96).ToString() * 3 + 'powershell'
$closing = ([char]96).ToString() * 3
if (@($lines | Where-Object { $_ -ceq $opening }).Count -ne 1 -or
    @($lines | Where-Object { $_ -ceq $closing }).Count -ne 1) {
  throw 'STOP_G2B1: exactly one complete fenced proposal required'
}
$first = [Array]::IndexOf($lines, $opening)
$last = [Array]::IndexOf($lines, $closing, $first + 1)
if ($first -lt 0 -or $last -lt ($first + 2)) { throw 'STOP_G2B1: invalid fence ordering' }
$proposal = $lines[($first + 1)..($last - 1)] -join "`n"
function Test-ProposalSource([string]$source) {
  $tokens = $null
  $errors = $null
  $ast = [System.Management.Automation.Language.Parser]::ParseInput(
    $source, [ref]$tokens, [ref]$errors)
  if ($errors.Count -ne 0) { return $false }
  if (-not $source.TrimStart().StartsWith('& {') -or
      -not $source.TrimEnd().EndsWith('}')) { return $false }
  $allowedCmd = @('Get-Process', 'Where-Object', 'Get-Item', 'Get-ChildItem',
                  'Sort-Object', 'Write-Output')
  $commands = @($ast.FindAll({
    param($node) $node -is [System.Management.Automation.Language.CommandAst]
  }, $true))
  $dynamics = 0
  foreach ($cmd in $commands) {
    $name = $cmd.GetCommandName()
    if ($null -eq $name) { $dynamics++; continue }
    if ($allowedCmd -cnotcontains $name) { return $false }
  }
  if ($dynamics -gt 1) { return $false }
  $expectedMembers = @{
    IsNullOrWhiteSpace = '[string]'
    GetFullPath = '[IO.Path]'
    Combine = '[IO.Path]'
    GetParent = '[IO.Directory]'
    ReadAllText = '[IO.File]'
  }
  $readCount = 0
  $calls = @($ast.FindAll({
    param($node) $node -is [System.Management.Automation.Language.InvokeMemberExpressionAst]
  }, $true))
  foreach ($call in $calls) {
    if ($call.Member -isnot [System.Management.Automation.Language.StringConstantExpressionAst]) {
      return $false
    }
    $name = $call.Member.Value
    if ($name -ceq 'Trim') {
      if ($call.Static) { return $false }
      continue
    }
    if (-not $call.Static -or -not $expectedMembers.ContainsKey($name) -or
        $call.Expression.Extent.Text -cne $expectedMembers[$name]) { return $false }
    if ($name -ceq 'ReadAllText') { $readCount++ }
  }
  if ($readCount -ne 1) { return $false }
  if (@($ast.FindAll({
    param($node) $node -is [System.Management.Automation.Language.RedirectionAst]
  }, $true)).Count -ne 0) { return $false }
  foreach ($required in @(
    "Get-Process -ErrorAction Stop",
    "Get-Item -LiteralPath",
    "Get-ChildItem -LiteralPath",
    "Sort-Object -Property Name -Descending -CaseSensitive",
    "if ($"+"sqlite.Count -ne 4)",
    "if ($"+"marker.Length -lt 1 -or $"+"marker.Length -gt 256)",
    "G2B1_SELECTED_FILENAME_MATCH: ONE_OBSERVED",
    "G2B1_SELECTOR_OBSERVATION: OBSERVED_PARTIAL_ONLY",
    "G2B_SOURCE_IDENTITY: PARTIAL_LOCAL_IDENTITY_ONLY",
    "SQLITE_WRITER_ABSENCE: NOT_PROVEN",
    "G2C_G2D_G3_G4_G5_G6: NOT_AUTHORIZED",
    "M25_M31_V7_OTHER_ROLES: NOT_ASSESSED"
  )) { if (-not $source.Contains($required)) { return $false } }
  return $true
}
if (-not (Test-ProposalSource $proposal)) {
  throw 'STOP_G2B1: candidate source AST did not match static review'
}
$fakeChanges = @(
  $proposal.Replace('Get-Process -ErrorAction Stop', 'Stop-Process -ErrorAction Stop'),
  $proposal.Replace('Get-Item -LiteralPath', 'Set-Item -LiteralPath'),
  $proposal.Replace('Get-ChildItem -LiteralPath', 'Remove-Item -LiteralPath'),
  $proposal.Replace('[IO.File]::ReadAllText', '[IO.File]::WriteAllText'),
  $proposal.Replace('[IO.File]::ReadAllText', '[IO.File]::Delete'),
  $proposal.Replace('Sort-Object -Property Name -Descending -CaseSensitive',
                    'Sort-Object -Property Name -Descending'),
  $proposal.Replace('SQLITE_WRITER_ABSENCE: NOT_PROVEN', 'SQLITE_WRITER_ABSENCE: PROVEN'),
  $proposal.Replace('G2C_G2D_G3_G4_G5_G6: NOT_AUTHORIZED',
                    'G2C_G2D_G3_G4_G5_G6: AUTHORIZED'),
  $proposal.Replace('if ($'+'sqlite.Count -ne 4)', 'if ($'+'sqlite.Count -ne -1)'),
  $proposal.Replace('G2B1_SELECTED_FILENAME_MATCH: ONE_OBSERVED',
                    'G2B1_SELECTED_FILENAME_MATCH: VERIFIED_ORIGINAL')
)
foreach ($fake in $fakeChanges) {
  if (Test-ProposalSource $fake) { throw 'STOP_G2B1: invented unsafe source accepted' }
}
Write-Output "M32_G2B1_AST_STATIC_REVIEW_PASS: $($fakeChanges.Count) invented refusals, no candidate execution"
Write-Output 'M32_G2B1_OPERATOR_PROCEDURE: PREPARED_NOT_EXECUTED'
Write-Output 'M32_G2B1_WINDOWS_OS_SAFETY: NOT_CERTIFIED'
