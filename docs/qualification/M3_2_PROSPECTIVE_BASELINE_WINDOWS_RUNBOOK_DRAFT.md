# M3.2 — Runbook Windows prospectif SOLO (NON EXÉCUTABLE)

**DRAFT D'EXÉCUTION / AUCUNE COMMANDE WINDOWS AUTORISÉE.** Ce texte est un cahier des charges, non un script PowerShell. Politique adoptée dans [PR #39](https://github.com/LaurentCOLL1/Fabulaxiom/pull/39), réconciliation documentaire portée par PR #37 ; seul le périmètre prospectif peut relever de l'assurance `SOLO_OPERATOR_COMPENSATING_CONTROLS`. Aucune revue humaine indépendante n'a eu lieu. Les preuves historiques demeurent `PENDING_EXTERNAL_ATTESTATION` 21/3/2, la référence nouvelle `NOT_STARTED`.

## Avant G2 : cadrage et refus

L'opérateur doit confirmer **dans un registre privé, jamais dans GitHub** les chemins réels de la SQLite **production restaurée M1.5 v6**, de la **copie isolée M3.1 v7**, des sept worktrees et de tous les backups/manifests/ACL/marqueurs à préserver. Ne jamais deviner les chemins. Exiger identité logique/ACL/token standard, absence de writer, état des sidecars et place disponible. Les chemins exacts et les répertoires nouveaux seront approuvés avec un bloc de commande **spécifique**, après avertissement sur les touches interactives, les demandes d'élévation, les arrêts éventuels de processus, les effets lecture/écriture et tous les veto. Pas de privilège administrateur non autorisé.

**Ne jamais appeler sur les sources protégées :** `src-tauri/src/database.rs::open_database` (peut créer répertoires/migrations), `src-tauri/src/backup.rs::create_backup` (utilise cet ouvreur), `src-tauri/src/backup.rs::restore_backup` (peut changer le pointeur M1.5), ni `tools/m3_1_v6_backup.py` sans correction TOCTOU. `tools/m3_1_v6_audit.py` et `src-tauri/src/world_time_preflight.rs` sont des références **à adapter d'abord sur copies isolées**.

## G2 — Observation exclusivement si individuellement autorisée

1. Re-fetch GitHub : `main`, PR #35, PR #37, PR de l'outil et CI **sur SHA exact** ; source opérateur propre, aucun worktree modifié. Fixer la liste locale des rôles et le contrôle pré/post.
2. Préflight OS : jeton Windows d'intégrité moyenne, app Tauri/Fabulaxiom arrêtée si nécessaire et **séparément autorisé**, état des processus et du stockage, réparse/symlink/junction/ACL. Toute ambiguïté = STOP.
3. Qualifier le mécanisme de lecture SQLite **sans écrire sur l'original**. Une connexion `mode=ro` n'est pas suffisante pour promettre l'absence de création ou modification `-wal/-shm`. **STOP** si le mécanisme n'est pas démontré non mutant sur cet état. Pas de checkpoint, migration, journal rewrite, copie brute, suppression sidecars, ni `immutable=1` inventé.
4. Noter seulement les observations effectivement permises : hash/longueur/identité/roles et présence des sidecars, plus un état source pré/post. Aucune lecture persistante de roman/secret dans un rapport public.

## G3 — Capture nouvelle, si individuellement autorisée

1. Destination **privée entièrement nouvelle** en dehors des sources, aucun déplacement, aucun réemploi, ACL et espace disque validés. Refuser symlink/reparse point et collision concurrente.
2. Protection de non-écrasement de **bout en bout** : mécanisme démontré de réservation exclusive du nom/de l'identité du nouveau fichier et du répertoire ; vérifier les effets de SQLite Online Backup API (elle pourrait remplacer une cible) ; `exists()`/`Test-Path` seuls sont insuffisants. Un échec n'autorise pas une reprise qui remplacerait un original.
3. Ouvrir source via la méthode G2 préalablement autorisée ; backup cohérent transactionnel par base ; ne pas supposer un snapshot global atomique entre deux SQLite différentes. Abort sur `SQLITE_BUSY`, `SQLITE_LOCKED`, source mutable de façon non contrôlée, échec de fermeture ou disk-full.
4. Manifeste nouveau prospectif (date de génération, version source/code/SQLite/OS, rôle, schéma, nom logique, taille, SHA-256, méthode/état, empreinte de manifest) en stockage **privé séparé**. Une auto-signature n'est pas un témoin indépendant.

## G4 — Copies seules : contrôle et restauration

- Deux procédures d'audit technique différentes autant que possible, sur copies sorties du nouvel emplacement et sur destination de restauration **entièrement neuve**.
- Vérifier `PRAGMA integrity_check` exactement `ok`, `PRAGMA foreign_key_check` zéro violation, `user_version`, schéma, noms/tables/comptages, lignage de révisions de texte/heads, faits, sources, événements de revue, digests logiques déterministes versionnés.
- Tests adversariaux prévus sur **fixtures synthétiques** : mauvais rôle, hash falsifié, collision, FK orpheline, révision mutilée, base v6/v7 substituée, WAL incohérent, entrée malformée, nouveau chemin manquant.
- Refaire les checks sur une restauration **isolée non activée**, comparer aux preuves de G3 ; gel, puis **réexamen différé** sur sorties propres. Contrôler à nouveau que sources originales, sidecars, ACL, pointeur, sept worktrees et backups sont inchangés.
- Un `FAIL` ou `NOT_ASSESSED` sur contrôle obligatoire interdit l'acceptation. Aucune suppression ou réparation automatique des originaux ; mise en quarantaine uniquement de nouveaux fichiers et sous règle explicitement autorisée.

## G5 — Décision personnelle / G6 — logiciel

À G5, l'opérateur peut signer en son seul nom une fiche [risque SOLO](M3_2_SOLO_OPERATOR_RISK_DECISION_TEMPLATE.md) liant nouveau manifest, preuves, SHA, risques non éliminés, durée et périmètre ; jamais `INDEPENDENTLY_REVIEWED`. Statut potentiel `ACCEPTED_SOLO_FOR_LIMITED_FUTURE_REFERENCE` seulement si les contrôles du protocole et la restauration réelle ont réussi.

G6 nécessite **encore une décision différente** pour tester React/Tauri/SQLite M3.2 v7 en **lecture seule** sur copie isolée, avec cycle/contradiction/identités historiques/GUI et post-exit custody. Aucun test ne modifie la base de production ; pas de writer, migration de production `007`, fusion de #35, M3.3 ni release par le seul succès de G5.

## États

`NOT_STARTED` : pas de preuve prospective ; `PREPARED` : plan accepté seulement ; `COLLECTED_UNDER_AUTHORIZATION` : nouvelle copie produite mais non qualifiée ; `SOLO_CONTROLS_VERIFIED` : contrôles G4 réellement réussis ; `OWNER_RISK_ACCEPTED_FOR_SCOPE` : acceptation G5 signée par l'opérateur ; `ACCEPTED_SOLO_FOR_LIMITED_FUTURE_REFERENCE` : permet seulement de **demander** G6 ; `REJECTED/INCONCLUSIVE` : arrêt.

Sources techniques : https://www.sqlite.org/backup.html ; https://www.sqlite.org/wal.html ; https://www.sqlite.org/uri.html ; https://www.sqlite.org/pragma.html ; https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew .
