# M3.2 — continuité de handle SQLite v7 neuf et contre-exemple de racine remplaçable

**Statut : CANDIDATE TEST-ONLY — NON QUALIFIÉE à son propre SHA avant CI Windows.** Repart de PR #192, source `a061311a4d8ca54b213d134c2affa34defa3f023`, source CI [#40474849956](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40474849956) SUCCESS (147 Rust, 28 gardes, 122 contrats), squash `main=0584291d6dc3c8d2fc8860c8c5084250f4c43ba4`, postmain indépendante [#40476232974](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40476232974) SUCCESS. Aucune preuve de #192 n'est transférable au HEAD de cette candidate.

## Problème et changement borné

La fixture #192 réclamait un nom libre avec `create_new(true)`, **fermait le handle**, puis ouvrait la même chaîne de chemin avec SQLite `READ_WRITE`. Une autre partie capable de renommer le fichier ou son parent pouvait substituer un objet durant cet intervalle. La simple vérification `Path::is_dir` ne prouve pas l'identité d'un répertoire ; `sqlite3_open_v2` prend un nom de fichier, pas le handle déjà revendiqué.

Dans `src-tauri/src/world_time_file_migration_tests.rs` uniquement :

1. La revendication exclusive garde désormais le handle **jusqu'au retour de l'ouverture SQLite**, puis le libère. Sur Windows, `OpenOptionsExt::share_mode(FILE_SHARE_READ | FILE_SHARE_WRITE)` exclut `FILE_SHARE_DELETE`, tout en permettant la seconde ouverture SQLite. Sur les autres plateformes ce test ne revendique **aucun** verrou contre `rename`.
2. Sur Windows, un handle du répertoire parent immédiat, ouvert avec `FILE_FLAG_BACKUP_SEMANTICS` et sans partage `DELETE`, reste lui aussi vivant pendant ce seul handoff. Un test Windows vérifie que deux tentatives de renommage (dossier/fichier) échouent alors que ces handles restent ouverts, puis que SQLite peut ouvrir le fichier neuf.
3. Un test portable renomme un parent de fixture après son contrôle initial et recrée une entrée au même nom. Il démontre que **le chemin seul accepte un autre objet** : c'est un contre-exemple négatif et non une « preuve que le futur ouvreur est sûr ». Les deux répertoires et leurs fichiers restent sous la racine CI exclusivement jetable.

Les ouvertures SQLite recensées restent **18/4/3/2/0/6/0** pour le module test ; aucune invocation SQLite supplémentaire en production. Cibles avant qualification : **149 Rust** (dont un test Windows-only), **30 gardes d'inventaire** et **123 contrats de continuité** ; aucun chiffre n'est déclaré PASS pour cette branche tant que son CI au SHA exact ne l'a pas établi.

## Ce qui reste non démontré

- Propriété du répertoire de profil `com.fabulaxiom.greenfield.v1` et de **tous** ses ancêtres, réparse points/junctions, ACL et FileId/volume : non qualifiés. La fixture `DisposableRoot` n'est pas un mécanisme d'authentification d'arborescence opérateur.
- Correspondance identité du **handle réellement utilisé par SQLite** versus handle OS initial : non établie par une vérification atomique ou un VFS lié au handle. Un verrou de partage pendant l'ouverture réduit une fenêtre Windows mais ne démontre ni identité persistante ni résistance aux adversaires contrôlant les ancêtres.
- Sidecars créés en concurrence, autre processus du même propriétaire, crash/reprise, sélection d'activation et chaîne de garde de sauvegarde : non prouvés. Le code ne devient **pas** un ouvreur v7 Tauri/production.
- Les décisions de chronologie M3.2 en fichier neuf restent expérimentales : pas de CRUD/UX v7 runtime, pas de migration 007 de production, pas de writer IPC, pas de nouvelle destination ou second profil.

**STOP obligatoire avant runtime :** définir l'adversaire et la propriété de tous les ancêtres ; vérifier l'identité et les droits avec des handles natifs stables (y compris FileId sur Windows), établir un passage SQLite non substituable (ou refuser), valider la gestion des sidecars et l'activation dans le profil existant sous protocole séparé. Aucun raccourci « deux checks de chemin » ne constitue la preuve exigée.

Références primaires : [Rust `OpenOptionsExt::share_mode`](https://doc.rust-lang.org/std/os/windows/fs/trait.OpenOptionsExt.html), [Windows partage/handles](https://learn.microsoft.com/en-us/windows/win32/fileio/creating-and-opening-files), [identité des handles Windows](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/ns-fileapi-by_handle_file_information), [SQLite VFS `xOpen`](https://www.sqlite.org/c3ref/vfs.html).

## Gouvernance

Protéger `main` avec le ruleset `Protect main` (required `Windows frontend and Rust checks`), vérifier diff/reviews/threads et nouvelle CI au **HEAD exact**, ne fusionner qu'avec `expected_head_sha`, puis vérifier une CI `push` indépendante au squash et commenter issue #38 **append-only**. Rien dans ces tests ne vaut attestation Windows opérateur ou approbation automatique.

M3.2 `IN_PROGRESS_NOT_ACCEPTED` ; G2B `NOT_ACCEPTED` ; écrivain `NOT_PROVEN` ; G2C `NOT_AUTHORIZED` ; G3 réel `STOP_UNAVAILABLE` ; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)` ; prospective `NOT_STARTED` ; PR #35 `OPEN/DRAFT`. Pas d'accès à `M:\Fabulaxiom`, `%LOCALAPPDATA%`, SQLite active/originale v6/v7, backup, ACL, sidecars/journaux, marqueur, migration 007, writer IPC ni release. Tout bloc PowerShell opérateur éventuel reste soumis à consentement distinct et au wrapper intégral `& { ... }`.
