# M3.2 — Candidat distinct G2-A : PID 0 « System Idle Process »

**REVUE SOURCE UNIQUEMENT — NE PAS EXÉCUTER.** La version PR #86 réellement exécutée est conservée, inchangée, dans `M3_2_G2A_EXACT_BLOCK_REVIEW.md` (blob Git `ebeb8800f9f8e8cd9918579fca7e32c9e5231622`). Ce document contient une **nouvelle proposition**, jamais exécutée.

## Modification exacte et portée

Dans le parcours de l'inventaire complet `Win32_Process`, autoriser **un seul** enregistrement `ProcessId=0` dont le `Name` est strictement `System Idle Process` ; ne jamais placer ce PID dans la table des ancêtres. Refuser tout second PID zéro, PID zéro sous un autre nom, doublon positif ou PID négatif. Un WebView2 dont la chaîne ancestrale rejoint PID 0 reste STOP (`PROCESS_PARENT_MISSING`). Les autres veto SearchHost, cycle, ordre des dates, snapshots divergents et processus Fabulaxiom/Ollama restent inchangés.

La sortie opérateur #86 était `G2A_LOCAL_METADATA: STOP`, `STOP_STAGE: WEBVIEW2_PARENTAGE`, `STOP_REASON: UNEXPECTED_OR_UNSAFE`. La sous-cause étant masquée, **PID 0 reste une hypothèse technique, pas une cause démontrée sur ce PC**.

L'analyse est uniquement textuelle et par fixtures fictives. Le runner CI analysera l'AST mais **n'exécutera pas ce bloc**. Aucun accès voulu à une base SQLite, sauvegarde, sidecar, ACL, marqueur, worktree, réseau ou fichier, et aucune élévation, UAC, fermeture/lancement de processus ni écriture. `Get-CimInstance` peut solliciter WMI/CIM et le système d'exploitation peut journaliser. Une éventuelle utilisation locale demanderait un collage dans PowerShell suivi éventuellement d'Entrée, sans mot de passe ni `q`. **Aucune autorisation pour cette version : ne pas la coller.**

## Script exact — non autorisé

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
      $idleSeen = $false
      foreach ($item in $inventory) {
        $id = [int]$item.ProcessId
        if ($id -eq 0) {
          if ($idleSeen -or $item.Name -cne 'System Idle Process') {
            throw 'AMBIGUOUS_PROCESS_ID'
          }
          $idleSeen = $true
          continue
        }
        if ($id -lt 0 -or $byPid.ContainsKey($id)) {
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

## Conditions permanentes

Un PASS futur n'authentifierait pas SearchHost et ne prouverait pas l'absence d'un writer SQLite : les PID peuvent être réutilisés et les processus changent pendant l'inventaire. Tout autre PID anormal ou parent inconnu reste STOP. `G2B_G2C_G2D_G3_G4_G5_G6: NOT_AUTHORIZED` ; production v6, v7 isolée, migrations 007, IPC writer et release interdits. `TAURI_RUNTIME: NOT_TESTED`, `REAL_G3_STOP_UNAVAILABLE`, PR #35 DRAFT. L'ancienne approbation a été consommée ; **nouvel accord explicite sur les octets exacts indispensable avant tout essai**.

Sources : https://learn.microsoft.com/en-us/powershell/scripting/samples/managing-processes-with-process-cmdlets ; https://learn.microsoft.com/en-us/powershell/module/cimcmdlets/get-ciminstance ; https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-process .
