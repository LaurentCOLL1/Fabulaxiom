# M3.2 — Bloc PowerShell G2-A exact, uniquement soumis à revue

**STOP : CANDIDAT NON AUTORISÉ. NE PAS EXÉCUTER.** Le code ci-dessous est du texte Markdown, pas un fichier .ps1. Il n'est jamais appelé par les tests GitHub : l'AST PowerShell est seulement analysé dans la CI Windows.

Il ne consulte aucune base SQLite, aucun fichier de corpus, backup, marqueur, ACL ou worktree. Aucune élévation, demande UAC, modification, arrêt de processus, écriture de rapport, connexion réseau ou git fetch n'est prévu. whoami /groups interroge les groupes du jeton courant en mémoire ; seul le niveau MEDIUM est publié, jamais les SID ni les identités personnelles.

**Interactions si une autorisation future était donnée :** l'opérateur devrait valider lui-même le collage dans un terminal, typiquement avec Entrée. Le bloc ne demande aucune touche q, aucun mot de passe et n'a pas d'interaction propre. Ne pas le coller aujourd'hui. L'utilisation d'une session PowerShell propre sans profil devra être étudiée et approuvée séparément. Une machine compromise ou les journaux OS échappent à cette preuve source-only.

**Limites :** msedgewebview2 peut provenir d'autres logiciels ; par prudence sa présence entraîne STOP. L'absence des trois noms n'établit pas l'absence d'un écrivain SQLite. Toute anomalie de locale, token, whoami ou processus entraîne STOP sans exposer de détails privés. Les références GitHub publiques sont contrôlées séparément, jamais en réseau local par ce bloc.

## Code candidat exact — non exécuté

```powershell
& {
  $ErrorActionPreference = 'Stop'
  $stage = 'WINDOWS'
  try {
    if ([Environment]::OSVersion.Platform -ne [PlatformID]::Win32NT) {
      throw 'WINDOWS_REQUIRED'
    }
    $stage = 'POWERSHELL'
    if ($PSVersionTable.PSVersion.Major -lt 5) {
      throw 'POWERSHELL_UNSUPPORTED'
    }
    $version = $PSVersionTable.PSVersion.ToString()
    $stage = 'CLOCK'
    $clock = Get-Date -Format 'yyyy-MM-ddTHH:mm:sszzz'
    $timezone = [TimeZoneInfo]::Local.Id
    $stage = 'TOKEN_INTEGRITY'
    $whoami = Join-Path ([Environment]::SystemDirectory) 'whoami.exe'
    $csv = @(& $whoami /groups /fo csv /nh)
    if ($LASTEXITCODE -ne 0 -or $csv.Count -eq 0) {
      throw 'TOKEN_QUERY_FAILED'
    }
    $groups = @($csv | ConvertFrom-Csv -Header 'Name','Type','SID','Attributes')
    $labels = @($groups | Where-Object { $_.SID -match '^S-1-16-[0-9]+$' })
    if ($labels.Count -ne 1 -or $labels[0].SID -ne 'S-1-16-8192') {
      throw 'MEDIUM_INTEGRITY_REQUIRED'
    }
    $stage = 'PROCESS_NAMES'
    $names = @('Fabulaxiom','ollama','msedgewebview2')
    $present = @(Get-Process -ErrorAction Stop |
      Where-Object { $names -contains $_.ProcessName } |
      Select-Object -ExpandProperty ProcessName -Unique)
    if ($present.Count -ne 0) {
      throw 'RELATED_OR_AMBIGUOUS_PROCESS'
    }
    Write-Output 'G2A_LOCAL_METADATA: PASS'
    Write-Output "POWERSHELL_VERSION: $version"
    Write-Output "LOCAL_CLOCK: $clock"
    Write-Output "TIMEZONE: $timezone"
    Write-Output 'TOKEN_INTEGRITY: MEDIUM'
    Write-Output 'PROCESS_NAMES: NO_MATCH_IN_LIMITED_SET'
    Write-Output 'PROCESS_WRITER_ABSENCE: NOT_PROVEN'
    Write-Output 'PUBLIC_GITHUB_CHECK: NOT_ASSESSED_BY_THIS_BLOCK'
  }
  catch {
    Write-Output 'G2A_LOCAL_METADATA: STOP'
    Write-Output "STOP_STAGE: $stage"
    Write-Output 'STOP_REASON: UNEXPECTED_OR_UNSAFE'
  }
  Write-Output 'G2B_G2C_G2D_G3_G4_G5_G6: NOT_AUTHORIZED'
  Write-Output 'TAURI_RUNTIME: NOT_TESTED'
}
```

## Signification du résultat futur

Un PASS attesterait seulement de ces métadonnées locales dans le contexte d'exécution constaté. Il ne débloquerait pas G2-B/C/D, G3–G6, ni la lecture d'une base SQLite. Un STOP nécessite une nouvelle revue et non une correction automatique.

**État présent : G2A_EXACT_BLOCK=PREPARED_FOR_REVIEW_NOT_AUTHORIZED ; G2A_RUNTIME=NOT_ASSESSED.** Le propriétaire doit examiner les octets exacts, les effets et les éventuelles interactions, puis donner une autorisation explicite distincte. Le simple Continue et une CI verte n'en constituent pas une.

Historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED, PR #35 OPEN/DRAFT, issues #36/#38 OPEN ; M32_SECURITY_PREFLIGHT_STOP et REAL_G3_STOP_UNAVAILABLE inchangés.

Références : https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/whoami ; https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-process ; https://learn.microsoft.com/en-us/windows/win32/secauthz/mandatory-integrity-control .
