# Fabulaxiom M3.2 — G2-B0 : proposition exacte de revue des métadonnées

**NON EXÉCUTÉ — NE PAS COLLER CE BLOC SANS AUTORISATION SPÉCIFIQUE DE L'OPÉRATEUR.** C'est du texte dans un document GitHub. Les tests de dépôt n'exécutent jamais ce code. Le but est de préparer la **première observation B0** de deux racines connues et non de qualifier la totalité de G2-B.

## Requalification source-only — 25 octobre 2026

**25 octobre 2026 — checkpoint vérifié après PR #169 :** source `67e2b400510fe4bade797a9fd73997f892ded1ad` et CI [#40127450956](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40127450956) SUCCESS ; `main=4ea2c5f9ad380863c5634dae65faac9831b1cec3` et CI postmain indépendante [#40128407418](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40128407418) SUCCESS au SHA exact, 79 étapes Windows, voir [issue #38](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6392307076). G2-B0 demeure `PREPARED_NOT_EXECUTED`, sans consentement nouveau.

**Candidat nouveau source-only :** garde AST PowerShell `tools/m32_g2b0_ast_static_review.ps1` sur runner CI jetable : uniquement `Parser.ParseInput`, analyse de forme et 10 refus fictifs, JAMAIS exécution du bloc opérateur. Contrat #104, seuils non encore prouvés : 80 étapes Windows, 104 contrats, 96 Vitest fictifs, Chromium 82/82 deux modes, 132 Rust. Pas une certification de sûreté OS/TOCTOU/absence d'écrivain. Re-fetch main/PR/CI/diff/reviews/threads/ruleset, `expected_head_sha` après CI terminale exacte, puis postmain indépendante.

**STOP inchangés :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, écrivain `NOT_PROVEN`, origine `PARTIAL_LOCAL_IDENTITY_ONLY`, G2C `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 OPEN/DRAFT. Deux racines M1.5/M2.5 seulement, M3.1 v7 non évalué, aucun accès SQLite originale/backups/ACL/journaux/marker/migration 007/IPC writer ou Windows opérateur.

## Base de décision

- GitHub prérequis : PR #168 source `d1f6db636a09112ace772b734c1a33e81d63d168` et [CI #40117705107](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40117705107) SUCCESS, protected `main=a03cc5dad68aaf4cb78c39520de130960dc565f8`, [postmain #40122346098](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40122346098) SUCCESS indépendamment (79/79 Windows, 102 handoff, 96 Vitest, Chromium 82/82 chacun, 132 Rust). Aucun de ces tests ne qualifie le poste de l'opérateur.
- G2-A est **PASS_METADATA_ONLY_OWNER_REPORTED**, le consentement spécifique précédent **a été consommé**, et l'absence d'écrivain reste `NOT_PROVEN` ([issue #38](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38)).
- Le propriétaire a retrouvé les copies documentées de ses dossiers Tauri. Seuls les emplacements d'identité **`com.fabulaxiom.desktop`** (production M1.5) et **`com.fabulaxiom.m25qual35fb842c`** (isolée M2.5) sont ciblés ici. Cela ne prouve pas qu'ils représentent les fichiers originaux au moment d'une exécution ultérieure. Racine M3.1 v7, activation, sauvegardes, ACL et sept worktrees : **NOT_ASSESSED** par ce bloc.
- `Get-Item -LiteralPath` et `Get-ChildItem -LiteralPath` lisent les métadonnées/entrées sans interpolation de jokers ; cependant `Get-Item` ne constitue pas une preuve de cohérence atomique ni de File ID et les lectures de métadonnées peuvent générer des effets de journalisation OS indépendants de notre script. <https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-item>.

## Effets, prérequis et consentement

**Actions de lecture prévues** : inspection du jeton précédent (référence G2-A non répétée), inventaire instantané des noms de processus Windows en mémoire, analyse des attributs des ancêtres des deux racines, liste non récursive des **noms** de leurs entrées immédiates **en mémoire seulement** et simple détection de `*.sqlite3` ou `*.sqlite3-wal/-shm/-journal`. Aucun nom, chemin absolu, SID, ACL, contenu narratif, empreinte ou valeur SQLite n'est affiché.

**Aucun acte explicite** : pas de `Get-Content`, `Get-FileHash`, `Get-Acl`, `Get-ItemProperty`, `sqlite3`, `Start-Process`, `Stop-Process`, `git`, réseau, élévation, écriture, copie, déplacement, réparation, suppression ou ouverture de base. Un `STOP` ne répare rien.

**Interactions** : un collage et éventuellement Entrée dans PowerShell Windows standard, sans mot de passe/UAC, touche `q` ou arrêt interactif. Pré-requis : opérateur sur sa propre machine, dossiers ci-dessus vérifiés **en privé**, script exact et effets acceptés ; ne jamais exécuter depuis un compte administrateur ou environnement hostile. Une instance active de Fabulaxiom/Ollama, une racine absente, un ancêtre reparse/junction, une entrée dangereuse, un sidecar observé, une inspection incomplète ou un processus inattendu = **STOP**, sans escalade G2.

## Bloc candidat exact — TEXTE uniquement, NON autorisé

```powershell
& {
  $ErrorActionPreference = 'Stop'
  $stage = 'ENVIRONMENT'
  try {
    if ([Environment]::OSVersion.Platform -ne [PlatformID]::Win32NT) {
      throw 'WINDOWS_REQUIRED'
    }
    if ($PSVersionTable.PSVersion.Major -lt 5) { throw 'POWERSHELL_UNSUPPORTED' }
    if ([string]::IsNullOrWhiteSpace($env:LOCALAPPDATA)) {
      throw 'LOCALAPPDATA_MISSING'
    }
    $stage = 'PROCESS_METADATA'
    $running = @(Get-Process -ErrorAction Stop)
    if (@($running | Where-Object {
      $_.ProcessName -ieq 'Fabulaxiom' -or $_.ProcessName -ieq 'ollama'
    }).Count -gt 0) { throw 'APP_OR_OLLAMA_PRESENT' }
    $stage = 'PATH_METADATA'
    $roots = [ordered]@{
      PRODUCTION_M15 = [IO.Path]::Combine($env:LOCALAPPDATA, 'com.fabulaxiom.desktop', 'database')
      ISOLATED_M25 = [IO.Path]::Combine($env:LOCALAPPDATA, 'com.fabulaxiom.m25qual35fb842c', 'database')
    }
    $results = @()
    foreach ($role in $roots.Keys) {
      $path = $roots[$role]
      if (-not [IO.Path]::IsPathRooted($path)) { throw 'RELATIVE_PATH' }
      $cursor = [IO.Path]::GetFullPath($path)
      while ($true) {
        $current = Get-Item -LiteralPath $cursor -Force -ErrorAction Stop
        if (($current.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
          throw 'REPARSE_ANCESTOR'
        }
        $parent = [IO.Directory]::GetParent($cursor)
        if ($null -eq $parent) { break }
        $cursor = $parent.FullName
      }
      $dir = Get-Item -LiteralPath $path -Force -ErrorAction Stop
      if (-not $dir.PSIsContainer) { throw 'NOT_DIRECTORY' }
      $children = @(Get-ChildItem -LiteralPath $path -Force -ErrorAction Stop)
      if (@($children | Where-Object {
        ($_.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0
      }).Count -gt 0) { throw 'REPARSE_CHILD' }
      $sidecars = @($children | Where-Object {
        $_.Name -match '(?i)\.sqlite3-(wal|shm|journal)$'
      })
      if ($sidecars.Count -gt 0) { throw 'SQLITE_SIDECAR_SEEN' }
      $dbFiles = @($children | Where-Object {
        -not $_.PSIsContainer -and $_.Name -match '(?i)\.sqlite3$'
      })
      $results += [pscustomobject]@{ Role=$role; SqliteFileCount=$dbFiles.Count }
    }
    foreach ($r in $results) {
      Write-Output "G2B0_ROLE: $($r.Role) SQLITE_FILENAME_COUNT: $($r.SqliteFileCount)"
    }
    Write-Output 'G2B0_METADATA_OBSERVATION: OBSERVED_PARTIAL_ONLY'
  }
  catch {
    Write-Output 'G2B0_METADATA_OBSERVATION: STOP'
    Write-Output "STOP_STAGE: $stage"
    Write-Output 'STOP_REASON: UNEXPECTED_OR_UNSAFE'
  }
  Write-Output 'M31_V7_AND_OTHER_ROLES: NOT_ASSESSED'
  Write-Output 'G2B_SOURCE_IDENTITY: PARTIAL_LOCAL_IDENTITY_ONLY'
  Write-Output 'SQLITE_WRITER_ABSENCE: NOT_PROVEN'
  Write-Output 'G2C_G2D_G3_G4_G5_G6: NOT_AUTHORIZED'
  Write-Output 'HISTORICAL: PENDING_EXTERNAL_ATTESTATION(21/3/2)'
  Write-Output 'PROSPECTIVE: NOT_STARTED'
}
```

## Limites et décision

Même `OBSERVED_PARTIAL_ONLY` **ne constitue ni G2B PASS complet, ni garantie d'absence de writer, ni authentification Win32/File ID, ni absence de concurrence entre les observations**. L'absence apparente de `-wal/-shm/-journal` est un instantané, pas une preuve de froid/absence de writer. **Ne pas poursuivre automatiquement**. Les informations sensibles du poste et les éventuels détails d'erreur doivent rester en privé.

**Verdict tant que l'opérateur n'a pas donné son accord spécifique et exécuté le bloc examiné :** `G2-B0=PREPARED_NOT_EXECUTED`, `G2-B/C/D=NOT_AUTHORIZED`, `WRITER=NOT_PROVEN`, `G3=STOP_UNAVAILABLE`, `HISTORICAL=PENDING_EXTERNAL_ATTESTATION(21/3/2)`, `PROSPECTIVE=NOT_STARTED`.

Références : [SQLite WAL](https://www.sqlite.org/wal.html) : une ouverture WAL en lecture seule peut dépendre de sidecars ou les créer ; [Microsoft File ID](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-getfileinformationbyhandleex) : la véritable identité par handle exige une autre autorisation et un protocole Win32 dédié.
