# Voie C — répertoires Windows utiles au développement (observations du 26 octobre 2026)

Ce mémo recense **les emplacements communiqués par l'opérateur** et les sous-chemins déductibles de l'arborescence du dépôt, pour rendre la reprise pratique. Ce n'est **ni une découverte automatique du disque, ni une autorisation d'inspecter des fichiers privés**. Les chemins sont propres à ce poste ; un changement de lecteur ou de profil doit être vérifié explicitement avant toute commande. Ne jamais confondre la base neuve Greenfield avec les SQLite historiques protégées.

## Racine du code et sous-dossiers

| Chemin sur le Windows opérateur | Usage | Statut de connaissance |
| --- | --- | --- |
| `M:\Fabulaxiom` | Clone Git de travail ; `git`, `package.json`, `package-lock.json`, `vite.config.*` | Racine explicitement communiquée ; `main` propre à SHA `39725a020a8656b8d0488628bc208fcf104c058c` lors du test |
| `M:\Fabulaxiom\src` | Code React/TypeScript ; `RevisionWorkspace.tsx`, `revisions.ts`, `revisions.test.ts` | Sous-chemins vérifiés dans GitHub, existence locale dérivée du clone exécuté |
| `M:\Fabulaxiom\src-tauri` | Projet Tauri/Rust ; `Cargo.toml`, `Cargo.lock`, `tauri.greenfield.conf.json` | Sous-chemins vérifiés dans GitHub, configuration Greenfield effectivement lancée |
| `M:\Fabulaxiom\src-tauri\src` | Rust du pont et des révisions : `lib.rs`, `revision_commands.rs`, `revisions.rs` | Sous-chemins vérifiés dans GitHub |
| `M:\Fabulaxiom\src-tauri\src\database.rs` et `M:\Fabulaxiom\src-tauri\sql` | Schéma v6 et candidats SQL versionnés : **lecture du code uniquement**, pas d'exécution de migration 007 | Fichier/dossier vérifiés dans GitHub, **pas des bases de l'opérateur** |
| `M:\Fabulaxiom\tools` | Scripts et contrats, notamment `greenfield_first_launch_preflight.ps1` et tests Python | Sous-chemins vérifiés dans GitHub ; le préflight **premier lancement** n'est pas à relancer sur un profil déjà existant |
| `M:\Fabulaxiom\docs\continuity` | `RESUME_PROMPT_SHORT.md`, `RESUME_PROMPT.md`, handoffs, état, NEXT, protocole et présent mémo | Sous-chemins vérifiés dans GitHub |
| `M:\Fabulaxiom\docs\qualification` | Runbook de lancement et dossier d'archivage Greenfield | Sous-chemins vérifiés dans GitHub |
| `M:\Fabulaxiom\docs\roadmap` | `ROADMAP_STATUS_CURRENT.md`, `FABULAXIOM_ROADMAP_V1.md` | Sous-chemins vérifiés dans GitHub |
| `M:\Fabulaxiom\.github\workflows` | Définition CI, `m0-ci.yml` | Sous-chemins vérifiés dans GitHub |
| `M:\Fabulaxiom\node_modules` | Dépendances npm **locales** du clone | Chemin dérivé d'une installation npm et d'un lancement Tauri/Vite réussis ; ne pas effacer automatiquement |
| `M:\Fabulaxiom\src-tauri\target\debug\fabulaxiom.exe` | Exécutable Rust/Tauri **de développement** | Chemin relatif `target\debug\fabulaxiom.exe` observé dans la sortie Rust, résolu sous `src-tauri` ; non une release |

## Données de test neuves de l'opérateur — hors Git

| Chemin Windows | Usage et limites |
| --- | --- |
| `%LOCALAPPDATA%\com.fabulaxiom.greenfield.v1` | Racine du **profil neuf** rapportée par le préflight et le lancement ; l'opérateur a confirmé une application « PROJETS NEUFS » sans données historiques |
| `%LOCALAPPDATA%\com.fabulaxiom.greenfield.v1\database\fabulaxiom.sqlite3` | SQLite **neuve v6** des projets inventés, persistance et préférences d'archivage ; chemin rapporté par l'opérateur, à **ne jamais committer** ni manipuler par script documentaire |

La variable `%LOCALAPPDATA%` évite de publier le nom du compte Windows dans le GitHub public. La base Greenfield **n'est pas** le clone, n'est pas un jeu de fixtures du dépôt, et ce mémo n'autorise aucune lecture SQL, copie, restauration ou modification. Ses sauvegardes éventuelles ne sont **pas localisées ni qualifiées sur le poste** ; ne pas en inventer le chemin.

Les emplacements des **originales historiques** M1.5 v6, M3.1 v7, M2.5 isolée, sauvegardes, ACL, journaux, marqueur et writer IPC sont volontairement **non indiqués / non autorisés**. Les comptages de noms B0/B1 n'en établissent pas une identité sûre.

## Ce qui a réellement été essayé

- Git local `main` à `39725a020a8656b8d0488628bc208fcf104c058c`, profil Tauri de développement `com.fabulaxiom.greenfield.v1`, commande de démarrage Vite/Tauri : journal de build Rust terminé et `TAURI_DEV_EXIT_CODE: 0`, 8 warnings non bloquants.
- **Déclaration opérateur du 26 octobre** : cinq contrôles d'archivage/masquage réversible réussis (archiver une révision non courante, afficher les archivées avec texte intact, désarchiver, persistance après fermeture/réouverture, révision courante toujours visible/non archivable). `OWNER_REPORTED_GREENFIELD_REVISION_ARCHIVE_5_OF_5_PASS`, [issue #38](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6417653782) ; **pas d'attestation indépendante**.
- PR [#183](https://github.com/LaurentCOLL1/Fabulaxiom/pull/183) fusionnée ; CI source [#40309445029](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40309445029) au SHA `7879f2b052944d68ca367537809b0af8e05bca04` et postmain [#40310982760](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40310982760) au SHA `39725a020a8656b8d0488628bc208fcf104c058c` : `SUCCESS` indépendants.

## Interdictions et prochaine étape

Pas de suppression des révisions immuables ; l'archivage Greenfield utilise des préférences dans `app_metadata` v6, pas une migration. Aucune autorité d'écriture sur les historiques, leurs backups, marqueurs, journaux ou ACL. M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, original writer `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective historique `NOT_STARTED`, PR #35 OPEN/DRAFT.

Après ce checkpoint **documentaire**, travailler sur la sauvegarde/restauration **des nouveaux projets uniquement**, d'abord en source/fixtures isolées ; une procédure sur le profil local existant, surtout restauration ou écrasement, exige un périmètre et un contrôle de risque explicites. À chaque nouvelle PR, refetch live, revue/diff/threads, CI source SHA exact, `expected_head_sha`, postmain indépendante et commentaire append-only #38. Toute commande PowerShell proposée à l'opérateur doit être **entièrement encapsulée dans `& { ... }`**.
