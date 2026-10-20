# M3.2 — G2-A PASS metadata / écrivain SQLite : analyse des preuves manquantes (source-only)

**SOURCE-ONLY — AUCUNE COMMANDE WINDOWS — PAS D'AUTORISATION G2-B/G3.** Document daté du 20 octobre 2026, à revérifier avec GitHub avant toute action. Aucun fichier SQLite de l'opérateur n'a été ouvert ou inspecté.

## Faits observés, et leur portée

L'opérateur a exécuté **une seule fois**, avec accord explicite, le bloc G2-A PID 0 de [PR #89](https://github.com/LaurentCOLL1/Fabulaxiom/pull/89) ; il a rapporté le 20 octobre 2026 à 01:31:24 +02:00 : `G2A_LOCAL_METADATA: PASS`, token `MEDIUM`, processus Fabulaxiom/Ollama absents par recherche de noms, six WebView2 descendants du processus nommé SearchHost selon les métadonnées. Ces observations sont **déclaratives** et non attestées indépendamment.

La même sortie a explicitement maintenu `WEBVIEW2_OWNERSHIP_AUTHENTICATED: NO`, `PROCESS_WRITER_ABSENCE: NOT_PROVEN`, `TAURI_RUNTIME: NOT_TESTED`, `G2B_G2C_G2D_G3_G4_G5_G6: NOT_AUTHORIZED`. Un PASS des **métadonnées** n'est ni un PASS de l'absence d'écrivain, ni un PASS G2-B, ni l'autorisation d'une capture G3.

## Matrice : signal versus garantie

| Signal ou méthode envisageable | Ce qu'il permettrait d'observer | Ce qu'il NE démontre PAS |
| --- | --- | --- |
| Absence des noms Fabulaxiom/Ollama dans Get-Process | Aucun nom correspondant dans un instantané de processus au niveau d'intégrité MEDIUM | Absence de connexion SQLite tenue par un autre processus, service, script, handle hérité ou PID remplacé |
| Six WebView2 descendants de SearchHost selon Win32_Process | Compatibilité d'une ascendance de processus à l'instant observé | Identité/signature cryptographique de SearchHost, absence de toute autre connexion ou de writer SQLite |
| Absence de `-wal`, `-shm` ou `-journal` dans une énumération | État des noms de fichiers sur un instantané, si ultérieurement autorisé | Qu'aucune transaction ou connexion ne puisse écrire ; l'absence de sidecar n'est pas une exclusion de writer |
| Empreintes SHA-256 stables à deux instants | Même contenu sur les instants mesurés | Absence de writer pendant ou après ces instants ; absence de remplacement entre mesures |
| Obtention hypothétique d'un handle fichier `CreateFileW` à partage contrôlé | Conflit éventuel détecté par le noyau avec des handles incompatibles, tant que ce handle reste ouvert | Historique d'écrivains, identités de tous les acteurs, état de l'API SQLite, de toutes les familles de journaux et garanties de provenance |
| `GetFileInformationByHandleEx(FileIdInfo)` hypothétique | Couple identifiant de volume et identifiant du fichier sur un handle validé | Authenticité d'une chaîne historique, absence de rename/ABA ailleurs, absence de writer à lui seul |
| `PRAGMA query_only` / `mode=ro` | Politique locale de lecture d'une **connexion correctement ouverte** | Qu'un autre client n'écrit pas, qu'une ouverture est sans effets secondaires, ou que les originaux sont sûrs |
| `immutable=1` sur source mutable | Ne doit PAS être utilisé pour masquer les verrous | SQLite ignore verrous/détection de changement et peut retourner des résultats incorrects si le fichier change |

**Aucune combinaison de ces observations isolées n'autorise G3.** Les verrous SQLite font partie d'un protocole cohérent DB + journaux et peuvent coexister avec des lecteurs/écrivains. Même un handle exclusif sur la DB seule n'authentifie pas rétroactivement l'état de la connexion SQLite ni la chaîne de conservation des originaux.

## Écart de l'architecture réelle de Fabulaxiom à `main=45ce1511aa616fce9664dfc08cea39f290d2273d`

- `src-tauri/src/database.rs::open_database` crée potentiellement le répertoire, appelle `Connection::open`, puis `run_migrations`. **Non autorisé** comme entrée d'observation G3 des originaux v6/v7 protégés.
- `src-tauri/src/lib.rs::database_status` utilise cette ouverture susceptible de migrer.
- `src-tauri/src/backup.rs::create_backup` utilise également `database::open_database` et `VACUUM INTO` ; ce n'est **pas** un mécanisme de capture préservant G3.
- Les fixtures Python/Rust précédentes ont qualifié des scénarios fictifs de propriétaire `already-open`, transfert vers RAM, verrouillage, rejet de sources ambiguës, sortie new-only et restauration tierce. Elles **n'établissent pas** l'identité ni la disponibilité d'un propriétaire non migrant **sur l'original réel**.
- PR #35 DRAFT ; issue #36 : cinq rôles de provenance non authentifiés ; issue #38 : baseline prospective NOT_STARTED, auteur unique sans relecteur indépendant. Ces blocages sont **distincts** du PASS G2-A.

## Deux stratégies éventuelles, NON validées et non exécutées

**A — Propriétaire SQLite existant, identifié, durable et non migrant** : il faudrait *au préalable* des preuves indépendantes de provenance, de l'identité de la source et du propriétaire, une connexion déjà ouverte et non migrante dont la durée de vie soit contrôlée/révocable, l'absence d'ATTACH non qualifiés, une politique de concurrence/journal documentée, une copie cohérente vers RAM puis publication nouvelle et restauration distincte. **Le runtime actuel n'offre pas un tel propriétaire attesté : STOP.** Ne pas ouvrir les originaux pour le fabriquer.

**B — Source froide réellement quiescente** : à concevoir séparément seulement si l'identité réelle de la DB, des ancêtres et des sidecars/journaux est authentifiée, que toute écriture et remplacement sont exclus pendant la fenêtre de capture par un protocole d'exclusivité vérifiable, et que le modèle de crash/recovery et la conservation de provenance sont résolus. Une simple absence de processus, un handle ponctuel, ou un hash ne satisfont pas ces conditions. **À ce jour : STOP.**

N'importe quelle proposition future demandant accès à un chemin privé, inspection des locks, handle, SQLite, ACL, sauvegardes ou process Windows exige d'abord une **procédure intégrale distincte** détaillant effets, interactions, sorties privées et mode d'arrêt, puis une **approbation explicite propre à cette procédure**. Les stratégies A/B ne sont pas des scripts ni des mandats.

## Décision et prochain travail autorisé

- `G2A_LOCAL_METADATA=PASS_METADATA_ONLY_OWNER_REPORTED` : conserver ce résultat borné.
- `PROCESS_WRITER_ABSENCE=NOT_PROVEN` ; `TRUSTED_NON_MIGRATING_OWNER=NOT_ESTABLISHED` ; `COLD_QUIESCENCE_AND_JOURNALS=NOT_ESTABLISHED`.
- `HISTORIC_CUSTODY=PENDING_EXTERNAL_ATTESTATION(21/3/2)`, `PROSPECTIVE_BASELINE=NOT_STARTED`.
- `REAL_G3=STOP_UNAVAILABLE`, `G2B/G2C/G2D/G3/G4/G5/G6=NOT_AUTHORIZED`.
- Aucun original v6/v7, sidecar, ACL, backup, activation marker, migration 007, IPC writer, PR #35, M3.3 ou release autorisé.
- Travail permis : audit source-only des chemins `open_database`/write, documentation des invariants et essais sur fixtures fictives **sans création de moyen d'accès aux bases de l'opérateur**. Re-fetch GitHub et CI au HEAD exact avant fusion de tout travail.

## Sources primaires

- Microsoft `Win32_Process` et réutilisation PID : https://learn.microsoft.com/fr-fr/windows/win32/cimwin32prov/win32-process
- Microsoft `CreateFile`, partage et verrouillage : https://learn.microsoft.com/en-us/windows/desktop/FileIO/creating-and-opening-files
- Microsoft `FILE_ID_INFO` : https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_id_info
- SQLite WAL et sidecars : https://www.sqlite.org/wal.html et https://www.sqlite.org/walformat.html
- SQLite Online Backup : https://www.sqlite.org/backup.html
- SQLite `immutable` et ses dangers : https://www.sqlite.org/uri.html
