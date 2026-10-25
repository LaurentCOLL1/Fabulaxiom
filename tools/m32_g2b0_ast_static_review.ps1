# CI runner ONLY. This script NEVER executes the G2-B0 candidate.
# Synthetic mutations are strings passed to Parser.ParseInput, not executable commands.
$ErrorActionPreference = 'Stop'
$reviewPath = 'docs/qualification/M3_2_G2B0_METADATA_ONLY_OPERATOR_REVIEW_20261024.md'
$doc = Get-Content -LiteralPath $reviewPath -Raw -Encoding UTF8
$lines = @($doc -split '\r?\n')
$open = ([char]96).ToString() * 3 + 'powershell'
$close = ([char]96).ToString() * 3
if (@($lines | Where-Object { $_ -ceq $open }).Count -ne 1 -or
    @($lines | Where-Object { $_ -ceq $close }).Count -ne 1) {
  throw 'STOP_G2B0: expected exactly one candidate code fence'
}
$first = [Array]::IndexOf($lines, $open)
$last = [Array]::IndexOf($lines, $close, $first + 1)
if ($first -lt 0 -or $last -le ($first + 1)) {
  throw 'STOP_G2B0: invalid candidate code fence ordering'
}
$candidate = ($lines[($first + 1)..($last - 1)] -join "`n")

function Test-G2B0SourceAstShape([string]$source) {
  # Data ONLY: Parser.ParseInput constructs an AST; it does not invoke the source.
  $tokens = $null
  $parseErrors = $null
  $ast = [System.Management.Automation.Language.Parser]::ParseInput(
    $source, [ref]$tokens, [ref]$parseErrors)
  if ($parseErrors.Count -ne 0) { return $false }
  if (-not $source.TrimStart().StartsWith('& {') -or
      -not $source.TrimEnd().EndsWith('}')) { return $false }
  $commands = @($ast.FindAll({
    param($n) $n -is [System.Management.Automation.Language.CommandAst]
  }, $true))
  $allowedCommands = @('Get-Process', 'Get-Item', 'Get-ChildItem',
                       'Where-Object', 'Write-Output')
  $dynamicCount = 0
  foreach ($command in $commands) {
    $name = $command.GetCommandName()
    if ($null -eq $name) {
      $dynamicCount++
    } elseif ($allowedCommands -notcontains $name) {
      return $false
    }
  }
  # At most the enclosing '& { ... }'; no additional dynamic invocation.
  if ($dynamicCount -gt 1) { return $false }
  $calls = @($ast.FindAll({
    param($n) $n -is [System.Management.Automation.Language.InvokeMemberExpressionAst]
  }, $true))
  $allowedMethods = @('IsNullOrWhiteSpace', 'Combine', 'IsPathRooted',
                      'GetFullPath', 'GetParent')
  foreach ($call in $calls) {
    if ($call.Member -isnot [System.Management.Automation.Language.StringConstantExpressionAst] -or
        $allowedMethods -cnotcontains $call.Member.Value) {
      return $false
    }
  }
  $redirections = @($ast.FindAll({
    param($n) $n -is [System.Management.Automation.Language.RedirectionAst]
  }, $true))
  if ($redirections.Count -ne 0) { return $false }
  foreach ($needed in @('Get-Process -ErrorAction Stop',
                         'Get-Item -LiteralPath',
                         'Get-ChildItem -LiteralPath',
                         'REPARSE_ANCESTOR', 'REPARSE_CHILD',
                         'SQLITE_SIDECAR_SEEN',
                         'G2B0_METADATA_OBSERVATION: OBSERVED_PARTIAL_ONLY',
                         'SQLITE_WRITER_ABSENCE: NOT_PROVEN',
                         'G2B_SOURCE_IDENTITY: PARTIAL_LOCAL_IDENTITY_ONLY',
                         'G2C_G2D_G3_G4_G5_G6: NOT_AUTHORIZED',
                         'M31_V7_AND_OTHER_ROLES: NOT_ASSESSED',
                         'PENDING_EXTERNAL_ATTESTATION(21/3/2)',
                         'PROSPECTIVE: NOT_STARTED')) {
    if (-not $source.Contains($needed)) { return $false }
  }
  return $true
}
if (-not (Test-G2B0SourceAstShape $candidate)) {
  throw 'STOP_G2B0: current candidate AST source shape not reviewed'
}
# All negatives are fictional strings, NEVER evaluated. No Windows operator I/O.
$mutations = @(
  $candidate.Replace('Get-Process -ErrorAction Stop', 'Stop-Process -ErrorAction Stop'),
  $candidate.Replace('Get-Item -LiteralPath', 'Set-Item -LiteralPath'),
  $candidate.Replace('Get-ChildItem -LiteralPath', 'Remove-Item -LiteralPath'),
  $candidate.Replace('Get-Process -ErrorAction Stop', 'Invoke-Expression -ErrorAction Stop'),
  ($candidate + "`n[IO.File]::WriteAllText('invented.txt', 'invented')"),
  ($candidate + "`n& ([scriptblock]::Create('Write-Output invented'))"),
  ($candidate + "`nWrite-Output 'unterminated"),
  ($candidate + "`nWrite-Output invented > invented.txt"),
  $candidate.Replace('SQLITE_SIDECAR_SEEN', 'SIDE_CAR_IGNORED'),
  $candidate.Replace('SQLITE_WRITER_ABSENCE: NOT_PROVEN', 'SQLITE_WRITER_ABSENCE: PROVEN')
)
foreach ($mutated in $mutations) {
  if (Test-G2B0SourceAstShape $mutated) {
    throw 'STOP_G2B0: a synthetic negative source was accepted'
  }
}
Write-Output "M32_G2B0_AST_STATIC_REVIEW_PASS: $($mutations.Count) invented refusals; candidate NEVER executed"
Write-Output 'M32_G2B0_OPERATOR_AUTHORIZATION: NOT_GRANTED'
Write-Output 'M32_G2B0_WINDOWS_OS_SAFETY: NOT_CERTIFIED'
