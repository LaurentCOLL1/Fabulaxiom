# M3.2 — G2 opérateur unique : décision à préparer après les copies retrouvées

**24 octobre 2026 — DOCUMENT DE PRÉPARATION UNIQUEMENT. AUCUNE AUTORISATION DE LECTURE WINDOWS OU D'EXÉCUTION.** Ce document consolide les [copies retrouvées](M3_2_RECOVERED_COPIES_RECONCILIATION_20261024.md), les politiques existantes [SOLO](M3_2_PROSPECTIVE_TRUST_BASELINE_DECISION.md) et le [runbook Windows non exécutable](M3_2_PROSPECTIVE_BASELINE_WINDOWS_RUNBOOK_DRAFT.md). Il ne modifie **aucun** de leurs critères, ne contient pas de commandes PowerShell et ne promeut aucune pièce historique.

## Nouveau constat sur la copie détachée M2.5 — portée strictement limitée

La copie privée `fabulaxiom.sqlite3` déjà fournie par le propriétaire dans un chat a été lue **uniquement comme octets de l'upload**, puis chargée dans une connexion SQLite `:memory:` via `deserialize()` ; aucun `sqlite3.connect` vers un chemin de fichier réel, aucun accès aux originaux Windows, aucune écriture. La copie était identique avant/après le contrôle de lecture.

- `PRAGMA integrity_check` a renvoyé exactement `ok`.
- `PRAGMA foreign_key_check` a renvoyé **zéro violation**.
- **14 tables applicatives** ; la table `schema_migrations` contient **1, 2, 3, 4, 5, 6**. Le `user_version` d'en-tête vaut `0` et n'est pas la version du schéma applicatif Fabulaxiom.
- Comptes structuraux **2 univers, 2 romans, 2 chapitres, 2 scènes, 3 révisions de scène, 2 têtes de révision, 3 entités, 3 faits, 2 sources, 11 événements de revue, 0 série, 0 alias**.
- Ces comptes coïncident sur les objets centraux avec [la normalisation M2.5 antérieure](M2_5_POST_MERGE_NORMALIZATION.md), **pas** avec une attestation d'identité d'origine ou l'empreinte logique canonique calculée à l'époque.

**Classification NON modifiée :** `m25/isolated_v6 = UNANCHORED_OBSERVED`. Les trois rôles à SHA observé restent `OBSERVED_SHA256`. La correspondance du marqueur M1.5 à un SHA inscrit dans le JSON pré-réparation est un **lien interne** au dossier opérateur, non une signature tierce. La récupération de cinq rôles en copies n'équivaut pas aux **cinq attestations indépendantes historiques** (`0/5`). Le fichier privé de la base, son SHA actuel et ses octets ne sont **PAS** publiés sur GitHub.

## G2 : grille de décision avant de demander une autorisation opérateur précise

| Étape | Ce qu'il faudra distinguer / observer | STOP explicite |
| --- | --- | --- |
| Rôles et racines | Source **production restaurée M1.5 v6**, espace isolé **M2.5 v6**, copie isolée **M3.1 v7**, deux sauvegardes/manifests M2.4, ACL et activation ; aucune confusion par simple nom ou SHA | Rôle, parent, cible, pointeur ou version indéterminé |
| Identité Windows | Volume et type, ancêtres, File ID/handle/ACL sans réparse/junction/symlink ni fenêtre de substitution | Identité locale seule insuffisante pour revendiquer un témoin historique indépendant ; réparse ou namespace ambigu |
| Quiescence/écrivains | Examiner les processus et détenteurs d'écriture par un mécanisme **préexaminé** ; arrêt applicatif jamais forcé implicitement | Writer absent **NOT_PROVEN**, processus ou handles inconnus |
| Journaux SQLite | Distinguer `-wal`, `-shm`, `-journal` et état de recovery **sans créer, réparer ni effacer** un sidecar | Journal actif/hot/indéterminé ou méthode de lecture pouvant modifier l'original |
| Ouverture source | `database::open_database` et le backup/restore standard restent **refusés** pour la cérémonie : ils peuvent migrer/ouvrir/remplacer | Pas de connexion propriétaire préexistante authentifiée et non migrante ; aucune ouverture de secours improvisée |
| Destination prospective | Nouvel emplacement privé jamais existant, réservation exclusive résistante aux collisions/renames, capacité, contrôle d'identité et politique de non-écrasement | Chemin déjà utilisé, ACL/space ambigu, absence de garantie exclusivité |
| Autorisation | Bloc exact SHA-spécifique, entrées et effets déclarés, personnes/rôles, arrêt sûr, sorties privées, accord explicite distinct à chaque étape | Une approbation générale, un test CI, une copie récupérée ou le présent document ne constituent aucune autorisation |

Le protocole préexistant [G3 source acquisition](M3_2_G3_SOURCE_ACQUISITION_DECISION.md) privilégie une connexion **déjà ouverte, authentifiée, non migrante** vers un backup transactionnel RAM. **Cette connexion n'est pas démontrée disponible** dans le runtime courant ; cette route demeure `UNAVAILABLE`. Une capture à froid exige **indépendamment** writer réellement absent, journaux résolus et source/ancêtres identifiés. Il n'y a **aucun fallback automatique** entre les deux.

## G3–G6, si G2 a été approuvé et passé ultérieurement

1. **G3 séparé :** snapshot cohérent depuis une source dûment prouvée, sortie privée nouvelle *new-only*, pas de réouverture remplaçable, pas de copie brute active et aucune migration 007.
2. **G4 :** vérifications `integrity_check` + `foreign_key_check` + migration/table/counts/empreintes sur **nouvelles copies**, restauration indépendante dans un troisième emplacement et contrôle des originaux inchangés ; garder les journaux en place.
3. **G5 :** choix explicite du propriétaire et fiche de risque des contrôles compensatoires **SOLO** ; **jamais** prétendre qu'un relecteur humain indépendant a signé, ni marquer le passé comme attesté.
4. **G6 :** nouveau périmètre autorisé pour tester l'application en lecture seule **sur une copie isolée**, pas sur production ; PR #35 ne devient pas fusionnable automatiquement.
5. **Option distincte :** la copie privée M2.5 détachée pourrait être un *jeu de test local et isolé* après décision confidentialité/périmètre. **Cela ne constitue ni G2B ni G3 sur la source historique**, et aucun fichier/texte narratif n'entre dans la CI GitHub publique.

## Preuve documentaire et limites

Le dossier détaillé avec empreintes demeure **uniquement privé dans la conversation**, jamais dans le dépôt. Il est interdit d'y recopier SID, chemins privés absolus, SHA nouvellement calculé de la base, SQL rows, contenu romanesque, WAL et ACL. Les **conditions d'acceptation historiques** de l'[issue #36](https://github.com/LaurentCOLL1/Fabulaxiom/issues/36) restent inchangées. L'[issue #38](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38) gouverne la nouvelle baseline prospective `NOT_STARTED` et ses futures autorisations spécifiques.

**STOP MAINTENUS :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, identité `PARTIAL_LOCAL_IDENTITY_ONLY`, writer `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 `OPEN/DRAFT`. Aucun programme ni commande opérateur Windows exécuté.

Références officielles : [SQLite integrity et foreign_key checks](https://www.sqlite.org/pragma.html), [SQLite WAL et contraintes de lecture](https://www.sqlite.org/wal.html), [SQLite Online Backup API](https://www.sqlite.org/backup.html).

**Autorité CI antérieure distincte :** PR #167 source `819dbb0a1d80a07e9c19b3e7eacff761dce8dc9b`, [CI source #40115530223](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40115530223) SUCCESS, squash protégé `main=533bdb27480a2b6dbed630b148501eeaf3c34b1e`, [postmain #40116658246](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40116658246) SUCCESS séparément au même SHA ; 79 étapes Windows, 101 contrats, 96 Vitest fictifs, Chromium 82/82 deux modes et 132 Rust. Le nouveau candidat demande sa **propre CI**.
