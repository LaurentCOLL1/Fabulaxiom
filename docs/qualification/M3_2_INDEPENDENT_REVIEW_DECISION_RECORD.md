# M3.2 — Fiche de décision de revue indépendante (NON SIGNÉE)

**Statut réel : `AWAITING_INDEPENDENT_REVIEW`.** Émise pour examiner une procédure de gouvernance prospective, **pas** pour autoriser son exécution. Aucune identité de relecteur, approbation ou preuve de fichiers Windows n'a été fournie ou vérifiée dans cette fiche.

## 1. Périmètre figé de la revue

| Élément | Valeur connue lors de la préparation | Nature |
| --- | --- | --- |
| Dépôt | `LaurentCOLL1/Fabulaxiom` | Public sur GitHub ; ne pas y publier les données privées |
| `main` de référence | `f7eabfea74480d307b52d4b053730021efc95352` | Doit être re-fetché avant décision |
| PR de gouvernance | [#37](https://github.com/LaurentCOLL1/Fabulaxiom/pull/37), DRAFT / OPEN | La revue doit pointer sur le **HEAD live lors de sa soumission**, jamais reprendre aveuglément le SHA de ce texte |
| Ancien HEAD documentaire qualifié | `87c6d8332fa59c52b763e51932f114dda799c2ca` | [CI Windows #38753395591](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/38753395591), 23/23 sur **ce SHA seulement** |
| PR produit M3.2 | [#35](https://github.com/LaurentCOLL1/Fabulaxiom/pull/35), DRAFT | Aucune autorisation d'intégration réelle |
| Conservation historique | [Issue #36](https://github.com/LaurentCOLL1/Fabulaxiom/issues/36) | `PENDING_EXTERNAL_ATTESTATION` : 21 rôles ancrés / 3 observés / 2 sans ancrage |
| Autorisation de la cérémonie | [Issue #38](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38) | Ouverte, aucune exécution autorisée |
| Référence prospective | `NOT_STARTED` | Aucune sauvegarde ou attestation nouvelle créée |

**Attention :** le HEAD de la PR changera lorsque ce document sera ajouté. Le futur relecteur doit inscrire lui-même son SHA exact et consulter la CI attachée **à son SHA**, ainsi que la liste des fichiers réellement modifiés.

## 2. Risques concrets observés dans le code du `main` de référence

La [matrice d'audit détaillée](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6195335828) examine six composants. Les conclusions suivantes sont des constats **sur le code GitHub**, jamais des faits observés sur les bases Windows de l'opérateur.

| Code existant | Constat | Décision imposée pour la future cérémonie |
| --- | --- | --- |
| `src-tauri/src/database.rs::open_database` | `create_dir_all`, `Connection::open`, `run_migrations` | **Interdit** sur les originaux protégés |
| `src-tauri/src/backup.rs::create_backup` | Utilise l'ouvreur précédent, puis `VACUUM INTO` | **Interdit en réutilisation directe**, malgré la réservation unique existante |
| `src-tauri/src/backup.rs::restore_backup` | Peut créer un nouveau marqueur d'activation | **Interdit** pour une restauration d'essai de conservation |
| `tools/m3_1_v6_backup.py::_snapshot` | `target.exists()` puis `sqlite3.connect(target)` | **Interdit en réutilisation directe** : intervalle contrôle/utilisation |
| `tools/m3_1_v6_audit.py` | Refuse WAL et sidecars avant ouverture, calcule les digests de 14 tables | Référence **conceptuelle seulement**, après preuve du caractère non modifiant de l'ouverture |
| `src-tauri/src/world_time_preflight.rs` | Tests des tables v6, de l'intégrité et des clés étrangères sur connexion déjà ouverte | Critères de validation **réutilisables uniquement sur copie isolée et autorisée** |

## 3. Critères objectifs à vérifier avant un verdict sur le **protocole**

Le relecteur devra répondre, pour chaque point, `PASS`, `FAIL` ou `NOT_ASSESSED`, avec la référence précise de ce qu'il a examiné. Un `NOT_ASSESSED` sur un point obligatoire **bloque toute approbation**.

1. **Sources et privilèges :** les rôles sont correctement distincts (base restaurée de production v6, copie v7 isolée, sept worktrees, ACL, sauvegardes, marqueur d'activation) et aucun code potentiellement écrivant n'ouvre directement les sources protégées.
2. **SQLite WAL/SHM :** aucune promesse que `mode=ro` garantit, à lui seul, zéro écriture de fichier ; ouverture source seulement après examen de ses effets, avec arrêt sur état inconnu. Pas de checkpoint, suppression de sidecars ni `immutable=1` automatique.
3. **Destination :** un nouvel espace privé doit être choisi hors des racines protégées ; examiner sa provenance, ACL, jonctions/reparse points, liens, capacités et risque de course. L'ouverture du **fichier de destination** doit garantir au niveau système qu'un contenu existant ne pourra pas être remplacé. Un simple `exists()` / `Test-Path` est insuffisant.
4. **Mécanisme SQLite :** un nouvel outil indépendant et examiné utilisera une copie transactionnellement cohérente ; ni copie brute d'un `.sqlite3` live ni activation de base. Toute reprise après `BUSY`/`LOCKED` doit être bornée et revue ; échec incomplet = arrêt.
5. **Contrôles de contenu :** SHA-256 des nouveaux fichiers et manifestes, tailles, schéma exact, tables et digests logiques canoniques ; `PRAGMA integrity_check` doit répondre `ok`, `PRAGMA foreign_key_check` doit n'avoir aucune ligne. Ne pas confondre digest du fichier source et digest du snapshot cohérent.
6. **Restauration isolée :** interdiction de basculer le pointeur M1.5 ; restauration uniquement sur destination neuve, puis comparaison logique et nouveaux contrôles. Original inchangé avant/après.
7. **Traçabilité prospective :** dater l'état **nouveau** sans le présenter comme preuve d'octets anciens ; identité du responsable, méthode d'authentification indépendante, conservation privée, gestion des clés et limites historiques documentées.
8. **Arrêt, confidentialité et habilitations :** absence de suppression ou nettoyage automatique des originaux ; ne publier aucun contenu privé, ACL complet, chemin confidentiel ou secret dans GitHub ; chaque phase de lecture puis écriture exige une **autorisation opérateur distincte** et la préparation des interactions clavier/prompts éventuels.

Références techniques : [SQLite Online Backup API](https://www.sqlite.org/backup.html), [SQLite WAL](https://www.sqlite.org/wal.html), [SQLite URI / immutable](https://www.sqlite.org/uri.html), [SQLite PRAGMA](https://www.sqlite.org/pragma.html), [Microsoft CreateFile / CREATE_NEW](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew).

## 4. Compte rendu du relecteur — champs volontairement NON REMPLIS

| Champ à remplir par la personne autorisée | Valeur |
| --- | --- |
| Relecteur / organisation / rôle | **NON FOURNI** |
| Indépendance vis-à-vis de l'auteur et du détenteur des données | **NON VÉRIFIÉE** |
| Date de revue authentifiée | **NON FOURNIE** |
| PR #37 HEAD exact examiné | **À RENSEIGNER AU MOMENT DE LA REVUE** |
| Résultat de CI du même HEAD | **À VÉRIFIER, PAS HÉRITER** |
| Références du diff / documents examinés | **NON RENSEIGNÉES** |
| Huit critères : verdict + références de preuve | **NOT_ASSESSED** |
| Décision explicite | **PENDING** (`APPROVE_PROTOCOL_ONLY` / `CHANGES_REQUIRED` / `REJECT_PROTOCOL`) |
| Mode d'authentification et stockage privé de la décision | **NON DÉFINIS** |
| Autorisation de lire les sources Windows | **NON ACCORDÉE** |
| Autorisation de créer une sauvegarde | **NON ACCORDÉE** |

Un `APPROVE_PROTOCOL_ONLY` authentifié ne vaut **jamais** permission d'exécuter des commandes locales : le plan opérateur **spécifique** de l'issue #38, l'identité des sources privées, la destination, la politique de conservation et la méthode d'ouverture restent à examiner et à autoriser séparément. **Ni ChatGPT, ni la CI GitHub, ni l'auteur du document ne se substituent à un relecteur indépendant.**

## 5. Issue d'une revue non concluante

Si la personne compétente manque, que les chemins/ACL/WAL ne sont pas déterminés, que l'anti-écrasement n'est pas démontré, ou que le verdict contient `FAIL` / `NOT_ASSESSED`, conserver le statut `AWAITING_INDEPENDENT_REVIEW` (ou `CHANGES_REQUIRED`). Ne pas compenser l'absence de preuve par un nouveau SHA, une auto-signature, un rapport de CI ou une recherche GitHub.

**Arrêt obligatoire :** `prospective_baseline=NOT_STARTED`, `operator_execution=NOT_AUTHORIZED`, `M3.2_runtime=NOT_AUTHORIZED`, `historical_custody=PENDING_EXTERNAL_ATTESTATION (21/3/2)`. Aucune migration 007, aucun writer IPC, aucune fusion automatique de PR #35 ou passage à M3.3.
