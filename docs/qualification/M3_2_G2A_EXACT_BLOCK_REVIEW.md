# M3.2 — Bloc PowerShell G2-A exact, uniquement soumis à revue

**STOP : VERSION G2-A CORRIGÉE, NON ENCORE AUTORISÉE À L'EXÉCUTION. NE PAS EXÉCUTER.** Le code ci-dessous est du texte Markdown, pas un fichier .ps1. Il n'est jamais appelé par les tests GitHub : seul l'AST PowerShell est analysé dans la CI Windows ; les scénarios de parenté sont simulés par des fixtures Python, jamais exécutés sur l'ordinateur de l'opérateur.

Il ne consulte aucune base SQLite, aucun fichier de corpus, backup, marqueur, ACL ou worktree. Contrairement à la version précédente, il interroge les métadonnées CIM `Win32_Process` (PID, parent, date de création, nom) lorsqu'un WebView2 est présent. Cela peut solliciter le service WMI/CIM de Windows, sans modifier volontairement les processus ni leur configuration. Aucune élévation, demande UAC, modification, arrêt de processus, écriture de rapport, connexion réseau ou git fetch n'est prévu. whoami /groups interroge les groupes du jeton courant en mémoire ; seul le niveau MEDIUM est publié, jamais les SID ni les identités personnelles.

**Interactions si une autorisation future était donnée :** l'opérateur devrait valider lui-même le collage dans un terminal, typiquement avec Entrée. Le bloc ne demande aucune touche q, aucun mot de passe et n'a pas d'interaction propre. Ne pas le coller aujourd'hui. L'utilisation d'une session PowerShell propre sans profil devra être étudiée et approuvée séparément. Une machine compromise ou les journaux OS échappent à cette preuve source-only.

**Correction du STOP du 19 octobre :** la capture Process Explorer observait `SearchHost.exe` (PID 4740) parent de la famille WebView2 comprenant les six PID communiqués. Ces numéros sont historiques et **ne sont jamais inscrits comme liste blanche dans le code**. Le candidat exige que chaque WebView2 actif se rattache, dans le même inventaire CIM, à `SearchHost.exe` avec une chaîne sans cycle, sans parent manquant et sans parent plus récent que l'enfant. Le nombre et l'identité des processus doivent correspondre à `Get-Process` ; sinon STOP. Un WebView2 rattaché à Fabulaxiom, un parent inconnu ou un PID réutilisé détectable entraînent STOP. Le nom `SearchHost.exe` et la parenté ne prouvent **pas** l'authenticité Microsoft du binaire, l'absence de réutilisation indétectable des PID, ou l'absence d'un écrivain SQLite. Une présence d'Ollama ou Fabulaxiom demeure STOP. Les processus peuvent changer entre deux lectures, ce qui doit rester un risque résiduel explicite. Toute anomalie de locale, token, whoami ou processus entraîne STOP sans exposer de détails privés. Les références GitHub publiques sont contrôlées séparément, jamais en réseau local par ce bloc.

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
    $running = @(Get-Process -ErrorAction Stop)
    $blocked = @($running | Where-Object {
      $_.ProcessName -ieq 'Fabulaxiom' -or $_.ProcessName -ieq 'ollama'
    })
    if ($blocked.Count -ne 0) {
      throw 'RELATED_OR_AMBIGUOUS_PROCESS'
    }
    $edge = @($running | Where-Object { $_.ProcessName -ieq 'msedgewebview2' })

    $stage = 'WEBVIEW2_PARENTAGE'
    $searchHosted = 0
    if ($edge.Count -gt 0) {
      $inventory = @(Get-CimInstance -ClassName Win32_Process -Property Name,ProcessId,ParentProcessId,CreationDate -ErrorAction Stop)
      $byPid = @{}
      foreach ($item in $inventory) {
        $id = [int]$item.ProcessId
        if ($id -le 0 -or $byPid.ContainsKey($id)) {
          throw 'AMBIGUOUS_PROCESS_ID'
        }
        $byPid[$id] = $item
      }
      $cimEdge = @($inventory | Where-Object { $_.Name -ieq 'msedgewebview2.exe' })
      if ($cimEdge.Count -ne $edge.Count) {
        throw 'PROCESS_SNAPSHOT_CHANGED'
      }
      foreach ($item in $edge) {
        if (-not $byPid.ContainsKey([int]$item.Id) -or
            $byPid[[int]$item.Id].Name -ine 'msedgewebview2.exe') {
          throw 'PROCESS_SNAPSHOT_CHANGED'
        }
      }
      foreach ($child in $cimEdge) {
        $cursor = $child
        $seen = @{}
        $foundSearch = $false
        for ($depth = 0; $depth -lt 12; $depth++) {
          $id = [int]$cursor.ProcessId
          if ($seen.ContainsKey($id)) { throw 'PROCESS_ANCESTRY_CYCLE' }
          $seen[$id] = $true
          if ($cursor.Name -ieq 'SearchHost.exe') {
            $foundSearch = $true
            break
          }
          $parentId = [int]$cursor.ParentProcessId
          if ($parentId -le 0 -or -not $byPid.ContainsKey($parentId)) {
            throw 'PROCESS_PARENT_MISSING'
          }
          $parent = $byPid[$parentId]
          if ($null -eq $parent.CreationDate -or
              $null -eq $cursor.CreationDate -or
              $parent.CreationDate -gt $cursor.CreationDate) {
            throw 'PROCESS_PARENT_TIME_INVALID'
          }
          $cursor = $parent
        }
        if (-not $foundSearch) { throw 'PROCESS_PARENT_NOT_SEARCHHOST' }
        $searchHosted++
      }
    }

    Write-Output 'G2A_LOCAL_METADATA: PASS'
    Write-Output "POWERSHELL_VERSION: $version"
    Write-Output "LOCAL_CLOCK: $clock"
    Write-Output "TIMEZONE: $timezone"
    Write-Output 'TOKEN_INTEGRITY: MEDIUM'
    Write-Output 'FABULAXIOM_OLLAMA_PROCESS: NONE_MATCHED'
    Write-Output "WEBVIEW2_SEARCHHOST_LINEAGE: $searchHosted OBSERVED_METADATA_ONLY"
    Write-Output 'WEBVIEW2_OWNERSHIP_AUTHENTICATED: NO'
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

Un PASS attesterait seulement de ces métadonnées locales dans le contexte d'exécution constaté, éventuellement avec `WEBVIEW2_SEARCHHOST_LINEAGE: N OBSERVED_METADATA_ONLY` ; il ne prouverait ni la signature/identité du binaire SearchHost, ni l'absence d'écrivain SQLite. Il ne débloquerait pas G2-B/C/D, G3–G6, ni la lecture d'une base SQLite. Un STOP nécessite une nouvelle revue et non une correction automatique.

**État présent : G2A_EXACT_BLOCK=REVISED_AFTER_STOP_NOT_AUTHORIZED ; G2A_RUNTIME=STOP_FROM_PREVIOUS_VERSION/REVISED_VERSION_NOT_ASSESSED.** Le propriétaire doit examiner les octets exacts, les effets et les éventuelles interactions, puis donner une autorisation explicite distincte. Le simple Continue et une CI verte n'en constituent pas une.

Historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED, PR #35 OPEN/DRAFT, issues #36/#38 OPEN ; M32_SECURITY_PREFLIGHT_STOP et REAL_G3_STOP_UNAVAILABLE inchangés.

Références : https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/whoami ; https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-process ; https://learn.microsoft.com/en-us/windows/win32/secauthz/mandatory-integrity-control .
