# M3.2 — G2 Windows : dossier de revue avant observation des sources protégées

**STATUT : PLAN_READY_FOR_OWNER_REVIEW — AUCUN BLOC WINDOWS EXÉCUTÉ.**
**Autorité :** `main=b6b4d6d9f6a52638a1ccd004e8a3ed5cc10026f6` au moment de la rédaction ; re-fetch obligatoire au moment du lancement. Ce dossier est documentaire, ne contient pas de script à exécuter et ne constitue pas une autorisation d'accès aux fichiers. Référence prospective `NOT_STARTED`, produit réel M3.2 `NOT_AUTHORIZED`, historique `PENDING_EXTERNAL_ATTESTATION (21/3/2)`. Le propriétaire/opérateur unique peut utiliser la voie prospective `SOLO_OPERATOR_COMPENSATING_CONTROLS` validée par PR #39 puis réconciliée par PR #37. Aucune revue humaine indépendante n'a eu lieu.

## 1. Résultats vérifiés, sans transfert de confiance aux données réelles

- PR #39 politique SOLO MERGED, CI exact-head #38799012304 : 23/23 PASS.
- PR #37 réconciliation prospective MERGED, CI exact-head #38806963562 : 23/23 PASS.
- PR #40 laboratoire de sauvegarde **entièrement synthétique** MERGED, CI exact-head #38808400689 : 24/24 PASS après correction des connexions non fermées sur Windows.
- PR #35 code de chronologie : OPEN/DRAFT, non fusionnée ; pas d'éditeur chronologique réel ni d'IPC writer autorisé.
- [Issue #36](https://github.com/LaurentCOLL1/Fabulaxiom/issues/36) : cinq preuves historiques manquantes, non résolues ; [issue #38](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38) : G2–G6 opérateur non exécutés.
- Les fichiers de production et d'archives ne peuvent PAS être qualifiés par les actions CI ou par le laboratoire fictif. **Aucun chemin privé, identifiant utilisateur, nom de fichier issu de la machine, clé, ACL détaillé, roman ou base n'est publié ici.**

## 2. Rôles Windows distincts à vérifier **localement et en privé**

| Rôle | Attendu et interdit |
| --- | --- |
| `restored_active_v6` | Chemin exact de la SQLite restaurée, sélectionnée actuellement par M1.5 ; ne pas confondre avec sauvegarde historique ou source initiale |
| `m31_isolated_v7_runtime` | Chemin de la SQLite de la véritable identité Tauri isolée v7 ; ne pas confondre avec le candidat v7 de répétition |
| `m31_v7_rehearsal_candidate` | Candidat v7 séparé si toujours présent ; enregistrement distinct, jamais utilisé comme alias de la runtime v7 |
| `m15_activation_marker` | Identité et bytes exacts du marqueur existant ; **aucune bascule** |
| `worktrees_original_7` | Liste réelle des sept worktrees, état et identité ; **aucun déplacement/nettoyage** |
| `historical_custody` | Sauvegardes historiques, manifests, archives ACL et JSON existants : observation uniquement après autorisation expresse, pas de promotion historique |

Ces chemins doivent être ré-identifiés via le poste Windows avant toute conclusion ; les mentions dans des rapports anciens sont des **pistes historiques, pas une preuve d'existence actuelle**. Maintenir localement une feuille de correspondance privée ; ne jamais l'envoyer dans un commentaire GitHub public.

## 3. Séquence obligatoire sans saut

**G2-A — Qualification préalable non-invasive.** Avant toute consultation de fichier protégé, proposer un bloc PowerShell `& { ... }` **individuellement examiné** qui ne fait que relever : jeton Windows / niveau d'intégrité, processus Fabulaxiom/Tauri/Ollama potentiellement actifs (sans les arrêter), version PowerShell, heure locale et références GitHub distantes exactes. Le bloc doit préciser : aucune élévation, aucune touche interactive, aucun arrêt, aucune écriture à un fichier, aucun chargement de SQLite. Aucun `git checkout`, `reset --hard`, `clean`, migration, ou exécution de l'application.

**G2-B — Inventaire des chemins et métadonnées (nécessite un deuxième accord explicite sur le bloc exact).** Examiner sous `-LiteralPath` seulement les chemins **réellement confirmés** par l'opérateur : présence, type, taille, attribut `ReparsePoint`, liens/jonctions des ancêtres, ACL **sans publication**, paire éventuelle `-wal/-shm/-journal`, capacité disque. Aucune ouverture SQL et aucune modification d'ACL. En cas de doute sur un lien, partage réseau, version ou source active : STOP.

**G2-C — Empreintes des sources (autorisation spécifique supplémentaire).** SHA-256 et longueur des **fichiers originaux** uniquement si identités, permissions, absence de concurrence/effet non voulu et état WAL ont été évalués. Le hash d'une `.sqlite3` en WAL **ne représente pas automatiquement** tout l'état logique transactionnel : enregistrer chaque stream observé avec son rôle et son statut. Un SHA actuel reste une observation de 2026-10-16, jamais une attestation historique.

**G2-D — Décision de possibilité de lecture SQLite.** Ne pas ouvrir les bases protégées par défaut ; seule une conception source-safe-open auditable et approuvée pourra permettre la prise d'un snapshot cohérent ultérieur. Si `mode=ro` peut créer `-wal/-shm`, si le journal est incertain ou si une connexion reste active : STOP. Ne pas utiliser `immutable=1` sur une base susceptible d'évoluer. Aucune suppression de WAL/SHM, checkpoint, changement de journal, copie brute ou mutation de la source pour rendre le protocole compatible.

## 4. Bloqueurs dans le code existant (observés sur GitHub, non sur Windows)

- `src-tauri/src/database.rs::open_database` appelle `create_dir_all`, puis `Connection::open` et `run_migrations` : interdit pour le préflight de source.
- `src-tauri/src/backup.rs::create_backup` réutilise cet ouvreur ; interdit en l'état pour une capture de conservation.
- `src-tauri/src/backup.rs::restore_backup` peut activer une copie : interdit pour la répétition de restauration.
- `tools/m3_1_v6_backup.py` vérifie `target.exists()` puis ouvre la destination SQLite : il subsiste une course de réutilisation du fichier cible.
- `tools/m3_1_v6_audit.py` teste les sidecars et un en-tête WAL avant connexion. Étudier cette approche seulement pour **un futur G2-C/G2-D** et valider tous ses effets sur copies séparées. Ne pas l'exécuter automatiquement sur les originaux.
- `tools/m3_2_solo_synthetic_lab.py` ne possède **aucune interface pour fournir un chemin opérateur** et ne garantit pas une capture atomique Windows réelle. Ne jamais l'utiliser à cette fin.

## 5. Conditions de refus et preuves admissibles

Tout `NOT_ASSESSED`, chemin non confirmé, SHA Git mouvant, privilège inattendu, processus écrivain, ACL inattendu, présence/effet WAL inconnu, junction/reparse point, stockage insuffisant, état SQLite incomplet, fichier manquant, différence inexpliquée, ou tentative d'élévation / réparation : **STOP**. Enregistrer uniquement `NOT_AUTHORIZED` / `BLOCKED` ; ne pas « corriger » l'original et ne pas diffuser les détails sensibles.

Le compte-rendu G2 privé devra inclure : date réelle, identité des rôles, source du constat, versions/outils, méthode, preuve avant/après, résultat pour chaque contrôle `PASS|FAIL|NOT_ASSESSED`, raisons des abstentions, signature du propriétaire clairement **non indépendante** et éventuelle décision de poursuivre. Les champs non vérifiés ne deviennent pas `PASS` par défaut.

## 6. G3–G6 expressément hors périmètre de cette PR

Après G2 et **nouvelles décisions distinctes**, prévoir une destination neuve privée à création exclusive **de bout en bout**, SQLite Online Backup cohérent sans altérer source/WAL, contrôle logique + `integrity_check=ok` + `foreign_key_check` vide, restaura­tion sur troisième emplacement isolé, réexamen différé, acceptation personnelle du risque `G5`, puis seulement test React/Tauri v7 **lecture seule** `G6`. Une destination dont le nom a seulement été vérifié par `Test-Path` n'est PAS protégée contre l'écrasement concurrent. Aucun writer IPC, migration production `007`, changement de marqueur, PR #35 merge ou M3.3.

## 7. Avertissements obligatoires avant tout bloc PowerShell

Présenter séparément avant chaque bloc : (1) toutes les interactions clavier prévisibles (notamment `q` ou Entrée), (2) mot de passe / demande UAC éventuelle, (3) processus devant être arrêtés et **consentement spécifique**, (4) lecture/écriture, (5) chemins exacts privés concernés, (6) STOP et nature de la preuve produite. Préférer `& { ... }` ; aucun administrateur sans autorisation.

Références officielles : [SQLite WAL](https://www.sqlite.org/wal.html), [SQLite Online Backup](https://www.sqlite.org/backup.html), [SQLite URI](https://www.sqlite.org/uri.html), [PowerShell Get-Item](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-item), [Get-FileHash](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/get-filehash), [Get-Acl](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.security/get-acl), [Windows CreateFile / reparse points](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew).

**Verdict au terme de la préparation documentaire : `G2-A=PREPARED_NOT_RUN` ; `G2-B/C/D=NOT_AUTHORIZED`; baseline `NOT_STARTED`.**
