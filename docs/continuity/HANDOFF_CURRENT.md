# Fabulaxiom M3.2 — Reprise opérationnelle courte

**Checkpoint du 20 octobre 2026 après PR #97. Instantané documentaire : re-fetch GitHub obligatoire. Aucune autorisation Windows, SQLite ou G2-B/G3 créée.**

## 2026-10-20 — incrément produit M3.2 : édition de chronologie en navigateur fictif (candidat)

- Après [PR #97](https://github.com/LaurentCOLL1/Fabulaxiom/pull/97) fusionnée sur `main=a839953f73f17379aa7c5ccde69d807b5b99a2f6`, CI PR #39426793283 SUCCESS (74 étapes) au HEAD `00defd8fb25891f4cffb7f2acdd7871ef005cccc`; CI push main #39428345389 terminale SUCCESS. La roadmap V1 est désormais assortie d'une matrice de suivi et de neuf tests.
- Nouveau [laboratoire manuel fictif](../qualification/M3_2_SYNTHETIC_MANUAL_CHRONOLOGY_LAB.md) en candidat : formulaire de création des quatre dates, ajout de relation `avant/après` avec veto de cycle, révocation explicite, remplacement append-only préservant les sources anciennes et journal dans l'état mémoire. `src/m32BrowserLab.tsx` seul expose l'atelier ; **pas** `App.tsx` ni Tauri production, aucune DB, fichier, IPC ou donnée opérateur.
- 13 nouveaux tests Vitest de contrat fonctionnel et refus, à faire qualifier par la **nouvelle CI au SHA final** avant toute fusion. Les contrôles d'historique M2, identité, chronologie monde/narration/révélation restent inconditionnels ; le caractère synthétique ne constitue PAS le CRUD réellement accepté.
- M3.2 **IN_PROGRESS_NOT_ACCEPTED** ; PR #35 toujours DRAFT, UI native Windows et preuve de préservation réelles absentes. G2A PASS metadata-only déjà autorisé/consommé ; absence écrivain `NOT_PROVEN`, G2B/C/D et G3–G6 `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, historique 21/3/2 non attesté, prospective NOT_STARTED. Protection v6/v7, WAL, sidecars, ACL, sauvegardes, marqueur, migration 007, writer IPC, M3.3 et release inchangée.

## 2026-10-20 — audit intégral des cinq roadmaps V1, M3.2 encore non livrée

- Re-fetch `main=e35b7c92441c517d4f0fcacb829711c4d1e9da97`, PR #96 fusionnée sous ruleset, CI PR #39414915855 au HEAD `5ac35ff196b27ca85b79f73296c33082044c0d98` SUCCESS (73/73) ; CI push main #39416303498 terminale SUCCESS (72 étapes), sans effet sur les gates.
- Audit des **cinq** fichiers de `docs/roadmap/`, avec [index de suivi](../roadmap/README.md) et [matrice actuelle](../roadmap/ROADMAP_STATUS_CURRENT.md). M0–M2 `COMPLETE + MERGED + NORMALIZED` ; M3.1 aussi (PR #33 implémentation, PR #34 normalisation) ; M3.2 `IN_PROGRESS_NOT_ACCEPTED`, PR #35 DRAFT. M3.3–M3.6, M4–M9 non autorisés ; ComfyUI proposition issue #19 OPEN.
- **Écart produit** : les tests de sécurité G2/G3 et fixtures permettent de préparer M3.2, mais **ne remplissent pas** son CRUD manuel chronologique, l'UX acceptée et l'audit Windows de données. Les plans historiques « M3 planning pending » / « M3 unauthorized » sont explicitement datés, non une règle courante.
- Ajout de 9 tests **source-only** `tools/test_m32_roadmap_traceability.py` en CI : présence des cinq plans, états acceptés, livrables restant, interdictions et ComfyUI. La roadmap **n'accorde jamais** une autorisation locale.
- G2-A `PASS_METADATA_ONLY_OWNER_REPORTED` (consentement consommé), writer réel `NOT_PROVEN`, G2-B/C/D et G3–G6 `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`, historique 21/3/2, prospective NOT_STARTED. Aucune action PC/SQLite v6/v7, backup, ACL, sidecar, marker, migration 007, writer IPC, PR #35 merge, M3.3, release.

## 2026-10-20 — autre écrivain SQLite malgré query_only : contre-exemples sur RAM fictive

- PR #95 fusionnée sur `main=a8578b8e128af2264e85a7341a96e13d0e086b23`, HEAD qualifié `29bae8aee7e6985e20bfd1ebda34f7a5b2c8732d`, CI PR #39406700987 SUCCESS (72/72) et CI push main #39407869929 SUCCESS recontrôlée. Les 13 tests Rust précédents sont donc intégrés, mais leur effet reste exclusivement local à une connexion fictive.
- Nouvelle [preuve négative en RAM partagée](../qualification/M3_2_SHARED_RAM_EXTERNAL_WRITER_NEGATIVE_PROOF.md) : deux connexions SQLite Python distinctes, URI figée `mode=memory&cache=shared` validée par chemin principal vide, sans aucun fichier opérateur. Douze tests source-only montrent qu'une deuxième connexion peut écrire malgré le `query_only=ON` de la première et que `total_changes` du lecteur ne change pas.
- `PRAGMA data_version` peut signaler une modification externe passée, mais ne prouve pas une quiescence continue ni une identité de propriétaire. Le test n'est pas un mécanisme à déployer : shared-cache uniquement pour l'expérience fictive.
- **Décision inchangée** : G2-A `PASS_METADATA_ONLY_OWNER_REPORTED`, absence de writer réel `NOT_PROVEN`, G2-B/C/D/G3/G4/G5/G6 `NOT_AUTHORIZED`, vrai G3 `STOP_UNAVAILABLE` ; historique 21/3/2 et prospective NOT_STARTED ; consentement G2-A consommé. Aucune commande Windows, ni original v6/v7, sidecars, backups, ACL, marqueur, migration 007, IPC writer, PR #35 ou release.

## 2026-10-20 — lecture préouverte query-only en RAM fictive, Rust TEST-ONLY

- Re-fetch GitHub : PR #94 fusionnée sur `main=632e6d6d985affa6989bb220ddec99911e6ba1e6` après CI [#39394068343](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39394068343) SUCCESS au HEAD `74395428c185198632cc2cd2c19eec4b7132e4ad` (71 étapes). La CI post-merge de main doit être revérifiée avant de déclarer un succès terminal ; cette qualification ne déverrouille aucun gate.
- Nouveau [prototype Rust fictif](../qualification/M3_2_PREOPENED_QUERY_ONLY_RAM_READER_TOY.md) : seule une connexion `&Connection` déjà ouverte sur une base RAM **inventée** est empruntée ; la fixture seule fait `Connection::open_in_memory`, puis PRAGMA `query_only=ON`. 13 tests négatifs vérifient lecture sans migration, refus des écritures, schémas ATTACH supplémentaires et dérives de la même connexion. Feature non défaut + `cfg(test)` ; aucune API de production/Tauri/IPC.
- La surveillance source-only élargie reconnaît maintenant 26 fichiers Rust, dont 21 comportent des marqueurs SQLite. Son test des comptes textuels est ajusté pour la nouvelle fixture, sans reconnaître de droit de lecture sur les originaux.
- **Limits** : query_only et total_changes ne concernent que cette connexion ; aucun écrivain externe Windows authentifié ou exclu. G2-A reste `PASS_METADATA_ONLY_OWNER_REPORTED` (consentement consommé), writer SQLite absent `NOT_PROVEN`, G2-B/C/D et G3–G6 `NOT_AUTHORIZED`, `REAL_G3=STOP_UNAVAILABLE`, historique 21/3/2, prospective NOT_STARTED. Ne rien exécuter localement, ne pas ouvrir v6/v7, sidecars, backups, ACL, marqueurs, migration 007, writer IPC ou PR #35.

## 2026-10-20 — inventaire élargi de tous les modules Rust Tauri (source-only)

- Re-fetch GitHub : PR #93 fusionnée sur `main=15c91039243206dc61190fec5668f32a87f3faf0`, CI PR [#39391766661](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39391766661) SUCCESS au HEAD `dcad1a905d8f21cf0a18a03e2cfc2c95050cf100` (70 étapes). CI push main #39393215542 EN COURS au checkpoint.
- Nouvel [inventaire textuel complet des sites SQLite Rust](../qualification/M3_2_WIDE_RUST_SQLITE_SITE_INVENTORY.md) : 25 fichiers `.rs` du dépôt, 20 contenant les motifs retenus ; garde-fou CI + 18 tests sur modifications fictives. La seule présence de nouveaux noms/calls force réévaluation des empreintes textuelles, sans lire un seul fichier SQLite privé.
- Limite : le scanner ne comprend pas les macros/alias Rust ni les appels dynamiques ; plusieurs substitutions compensatoires peuvent préserver les compteurs. C'est un **tripwire de maintenance**, jamais une preuve de sécurité runtime ni une autorisation de G2B-G6.
- G2-A `PASS_METADATA_ONLY_OWNER_REPORTED` (accord unique consommé) ; `PROCESS_WRITER_ABSENCE=NOT_PROVEN`, owner non migrant non attesté, G3 `STOP_UNAVAILABLE`, provenance historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`. Aucune commande sur Windows ou accès aux originales v6/v7/journaux/backups/ACL/markers, migration 007, writer IPC, PR #35, M3.3/release.

## 2026-10-20 — décision courante des gates distincte de l'historique

- Main `8e358d61b7f5438b893a416aa8f82d884569c5da` après fusion protégée de [PR #92](https://github.com/LaurentCOLL1/Fabulaxiom/pull/92), HEAD `cb5e1eaeaaf64bd684be6a80c9cc3b85fc56492b`, CI [#39388988034](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39388988034) SUCCESS (70 étapes). La CI push `main` #39391283127 était EN COURS au checkpoint et ne constitue pas un PASS terminal.
- [Table de décision G2–G6 actuelle](M3_2_GATE_DECISION_CURRENT.md) : **G2-A PASS exclusivement de métadonnées** (déclaration opérateur), G2-B/C/D NON AUTORISÉS ; G3 réel STOP, G4-G6 NON AUTORISÉS. Writer SQLite absent : `NOT_PROVEN` ; aucun owner non migrant attesté, aucune source froide quiescente qualifiée.
- [Snapshot précédent](M3_2_GATE_SNAPSHOT.md) explicitement historique au 19 octobre : ne pas confondre son `G2: NOT_AUTHORIZED` de l'époque avec le résultat G2-A du 20. Le nouveau document **ne remplace ni les preuves historiques ni le runbook de capture**.
- Consentement unique au bloc G2-A consommé ; nouveau script Windows soumis à revue intégrale et approbation spécifique distincte AVANT exécution. Pas de bases v6/v7, sidecars, ACL, backups, marqueurs, migration 007, IPC writer, PR #35, M3.3 ou release.

## 2026-10-20 — garde-fou textuel des points d'entrée SQLite (source-only)

- PR #91 fusionnée sur main=fb4625450439ecf236cc9065f434eda002f71533 après CI #39376628743 SUCCESS au HEAD 94c9886e4e362867cab86c39efc5b13125a94dac (69 étapes Windows). G2-A PASS métadonnées UNIQUEMENT, absence d'écrivain SQLite NOT_PROVEN, G3 réel STOP.
- [Audit source-only des points d'entrée Rust](../qualification/M3_2_G3_RUNTIME_ENTRYPOINT_SOURCE_AUDIT.md) : open_database peut créer le dossier et ouvrir avec READ_WRITE|CREATE puis migrer ; database_status et create_backup appellent cette fonction ; backup réserve un nouveau fichier puis ferme son handle avant VACUUM INTO ; une lecture READ_ONLY n'atteste pas la non-modification de sidecars WAL.
- Nouveau garde-fou examine seulement trois fichiers Rust publics ; ses 18 tests sur modifications fictives exigent une nouvelle revue en cas de dérive, même si le changement serait une amélioration. **Ce n'est pas une preuve exhaustive de sécurité Rust**, ni une procédure opérateur.
- Interdictions inchangées : G2B/G2C/G2D/G3/G4/G5/G6, originaux v6/v7, sidecars/ACL/backups/markers, migration 007, writer IPC, PR #35, M3.3/release. Aucune commande locale autorisée sans procédure entière et nouvel accord explicite.

## 2026-10-20 — écart de preuve SQLite writer après G2-A PASS (source-only)

- Re-fetch `main=45ce1511aa616fce9664dfc08cea39f290d2273d` après fusion protégée [PR #90](https://github.com/LaurentCOLL1/Fabulaxiom/pull/90), PR head `9c53d06c94cfbae62215c2407e4e146e7a344773`, CI PR #39342493152 SUCCESS (68 étapes Windows). Aucun nouveau résultat opérateur après G2-A PASS_METADATA_ONLY.
- Nouvelle [matrice source-only d'absence d'écrivain SQLite](../qualification/M3_2_G2A_WRITER_ABSENCE_GAP_SOURCE_REVIEW.md) : noms de processus absents, hashes, sidecars, noms de fichiers, verrous ponctuels ou fixtures `already-open` ne prouvent pas la quiescence du writer réel. Aucune ouverture de fichier/handle SQLite local.
- Audit public ciblé : `database::open_database` peut créer le parent et exécuter `run_migrations`, `lib.rs::database_status` l'utilise, `backup::create_backup` l'utilise puis `VACUUM INTO`. Ces chemins **ne sont pas des commandes G3 autorisées** pour les originaux protégés.
- Deux stratégies futures théoriques restent indisponibles sur originaux réels : propriétaire déjà ouvert non migrant et vérifiable, ou protocole cold-source avec origine/ancêtres authentifiés, quiescence continue et journaux résolus. Tests de refus sur fixtures fictives (aucune vraie connexion).
- **STOP invariant :** `G2A_LOCAL_METADATA=PASS_METADATA_ONLY` ; `PROCESS_WRITER_ABSENCE=NOT_PROVEN` ; `REAL_G3=STOP_UNAVAILABLE` ; `G2B/C/D/G3/G4/G5/G6=NOT_AUTHORIZED`. Pas de manipulation des DB prod v6/v7, sidecars, ACL, sauvegardes, marqueurs, migration 007, IPC writer ou release. Une nouvelle opération Windows demande code exact, effets et autorisation propre.

## 2026-10-20 01:31:24 +02:00 — G2-A PID 0 : PASS de métadonnées (déclaration opérateur)
  
- Le propriétaire a examiné le bloc exact PR #89 et donné un **nouvel accord explicite limité à une exécution**. Sortie communiquée : `G2A_LOCAL_METADATA: PASS`, `TOKEN_INTEGRITY: MEDIUM`, `FABULAXIOM_OLLAMA_PROCESS: NONE_MATCHED`, `WEBVIEW2_SEARCHHOST_LINEAGE: 6 OBSERVED_METADATA_ONLY`, `WEBVIEW2_OWNERSHIP_AUTHENTICATED: NO`, `PROCESS_WRITER_ABSENCE: NOT_PROVEN`, `PUBLIC_GITHUB_CHECK: NOT_ASSESSED_BY_THIS_BLOCK`, `G2B_G2C_G2D_G3_G4_G5_G6: NOT_AUTHORIZED`, `TAURI_RUNTIME: NOT_TESTED`. PowerShell 5.1.26100.9587 ; fuseau Romance Standard Time. Preuve déclarative de l'opérateur, non attestée indépendamment.
- **Le PASS porte exclusivement sur l'observation locale G2-A.** Le contrôle n'authentifie pas SearchHost et ne démontre pas l'absence d'écrivain SQLite ; la cause détaillée de l'ancien STOP PR #86 reste **inconnue**, même si le nouveau script corrige son rejet théorique du PID 0.
- Une seule exécution de ce nouveau texte a été approuvée et effectuée. **Consentement consommé** : ni deuxième exécution, ni G2-B/C/D, ni G3/G4/G5/G6 sans approbation distincte du propriétaire.
- GitHub `main=f14e5991d34350682647ef6f0bd67b1d2055f41a`, [PR #89](https://github.com/LaurentCOLL1/Fabulaxiom/pull/89) fusionnée ; CI push main #39341197526 recontrôlée SUCCESS et CI PR #90 #39341376262 était SUCCESS à son **ancien** HEAD avant cette modification. Toute CI de PR #90 au HEAD nouveau doit être entièrement requalifiée.
- Production SQLite v6 et v7 isolée, sidecars, sauvegardes, ACL, marqueur, migration 007, writer IPC, PR #35, M3.3 et release restent interdits. Provenance historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, issues #36/#38 OPEN.

## 20 octobre 2026 — checkpoint AVANT l'exécution locale G2-A (historique)

- `main=f14e5991d34350682647ef6f0bd67b1d2055f41a` (fusion [PR #89](https://github.com/LaurentCOLL1/Fabulaxiom/pull/89)), CI `pull_request` [#39339365546](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39339365546) terminale SUCCESS sur le HEAD `e188a98090112551b6a35dd78e8327914c0e9965` ; **68 étapes Windows SUCCESS**, dont 22 fixtures fictives, 11 tests source-only et parser AST PowerShell sans exécution. CI `push main` #39341197526 EN COURS au checkpoint, non qualifiée PASS.
- Le nouveau [bloc PID 0 exact](../qualification/M3_2_G2A_PID_ZERO_CANDIDATE_REVIEW.md) est intégré en Markdown, **jamais exécuté sur Windows et NON AUTORISÉ pour l'opérateur**. Le bloc PR #86 reste distinct, intact, et son unique essai autorisé a déjà retourné `STOP_WEBVIEW2_PARENTAGE`.
- Les causes exactes de ce STOP restent inconnues. Correction PID 0 = hypothèse de défaut de source, **pas confirmation runtime**. Tous les G2-B à G6, bases privées v6/v7, sauvegardes, ACL, markers, sidecars, migration 007, IPC writer, PR #35, M3.3 et release restent bloqués.
- Prochaine frontière : présenter au propriétaire le **code intégral du nouveau bloc** avec effets (PowerShell, CIM/WMI, Entrée, pas de q/UAC prévu, journaux OS possibles) et solliciter son accord explicite distinct. Aucun `Continue` n'autorise à lui seul l'exécution.

## Reprise au 20 octobre 2026 — bloc candidat PID 0 SOURCE-ONLY

- Après re-fetch GitHub : PR #88 fusionnée sur `main=6d9d9ff52459873347180f509717180ccccd0d5f` ; CI PR #88 [#39303355912](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39303355912) terminale SUCCESS au HEAD exact `0b7c55f30f0a7967270e9a58be7beae25087fec5` ; CI push `main` #39338867733 initialement EN COURS, ne pas la présenter comme PASS.
- Une branche technique DISTINCTE propose [un nouveau bloc exact](../qualification/M3_2_G2A_PID_ZERO_CANDIDATE_REVIEW.md), **non exécuté et non autorisé**. La version PR #86 réellement exécutée et son blob `ebeb8800f9f8e8cd9918579fca7e32c9e5231622` demeurent inchangés.
- Diff intentionnel : un seul PID 0 admis seulement s'il est nommé exactement `System Idle Process`, non ajouté aux ancêtres. Deux PID 0, nom atypique, PID négatif, PID parent zéro WebView2 et tous les veto antérieurs continuent STOP. Tests adversariaux sur fixtures, garde de diff exact et analyse PowerShell AST **sans exécuter**.
- La cause réelle du STOP `WEBVIEW2_PARENTAGE` n'est **pas identifiée** ; le PID 0 est une hypothèse techniquement plausible, pas une preuve sur le PC. Ancienne autorisation entièrement consommée. Aucune nouvelle commande Windows, SQLite, ACL, backup, marqueur ou Tauri.
- G2-B/G2-C/G2-D/G3/G4/G5/G6, migration 007, IPC writer, PR #35, M3.3 et release restent `NOT_AUTHORIZED`.

## Vérification de reprise du 19 octobre 2026

Lecture GitHub (sans exécution sur le PC opérateur) : `main`, PR #86/#87/#35, issues #36/#38, runs/actions et ruleset #24895490 `Protect main` revérifiés. Ruleset actif, check `Windows frontend and Rust checks` de l'app 15368 exigé, branche `main` sous PR, interdiction de suppression et de non-fast-forward, `bypass_actors=[]`. La lecture REST historique de protection de branche renvoie 403 pour cette intégration ; cela **n'annule pas** le ruleset lu directement. Un résultat opérateur nouveau existe : `G2A_LOCAL_METADATA: STOP`, `STOP_STAGE: WEBVIEW2_PARENTAGE`, `STOP_REASON: UNEXPECTED_OR_UNSAFE` sur le candidat exact PR #86. Le consentement spécifique à cet unique essai est consommé ; toute autre commande exige une nouvelle revue et un nouvel accord. Le sous-motif précis est inconnu. Les métadonnées de processus ne prouvent jamais l'absence d'un écrivain SQLite. Cette mise à jour documentaire n'ouvre aucun gate.

## Dernier état effectivement vérifié

- Dépôt : https://github.com/LaurentCOLL1/Fabulaxiom
- `main` observé : `f14e5991d34350682647ef6f0bd67b1d2055f41a` (merge [PR #89](https://github.com/LaurentCOLL1/Fabulaxiom/pull/89), après PR #88/#87/#86).
- PR #86 : correction du filtre G2-A `SearchHost.exe` / `msedgewebview2.exe` **fusionnée** ; CI Windows PR #39241294071 terminale SUCCESS et CI `main` #39242342744 SUCCESS.
- PR #87 : continuité versionnée et garde-fou de fraîcheur **fusionnés** ; CI Windows PR #39271702661 au HEAD `287c178063a4d2719742bac96d3bc57a8fa515bc` SUCCESS (62 étapes, contrôle same-PR PASS) ; CI `main` #39273165266 au SHA ci-dessus SUCCESS (62 étapes dont contrôle PR-only SKIPPED, attendu).
- PR #35 : **OPEN / DRAFT**. Issues [#36](https://github.com/LaurentCOLL1/Fabulaxiom/issues/36) et [#38](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38) : **OPEN**. Ruleset Protect main #24895490 actif, sans bypass (au checkpoint).
- Application : Windows, React + Tauri v2 + Rust + SQLite. Production SQLite v6 protégée, v7 isolée ; **aucune ouverture/migration des fichiers opérateur**. Pas de migration 007.
- Historique de provenance : `PENDING_EXTERNAL_ATTESTATION(21/3/2)` (21 ancrés, 3 empreintes observées seulement, 2 non ancrés). Politique compensatoire opérateur unique documentaire, baseline prospective `NOT_STARTED`.

## Incident G2-A et correctif

Le bloc G2-A de PR #85 a été exécuté manuellement après autorisation et a retourné **`G2A_LOCAL_METADATA: STOP`, `STOP_STAGE: PROCESS_NAMES`**. Une capture de Process Explorer montrait six processus WebView2 sous `SearchHost.exe`, compatible avec la recherche Windows. **Ce n'est pas une preuve d'absence de processus écrivain SQLite**.

La PR #86 a préparé [le nouveau bloc exact](../qualification/M3_2_G2A_EXACT_BLOCK_REVIEW.md) **en Markdown uniquement**, qui examine `Win32_Process` (PID, PID parent, date de création, nom), compare les inventaires et refuse parent absent, cycle, chronologie incohérente, Fabulaxiom/Ollama actif ou WebView2 d'origine incertaine. Une parenté SearchHost cohérente peut être observée sans stopper les processus. La vérification PowerShell AST en CI est **syntaxique uniquement**, et les parentés sont testées sur fixtures fictives.

**Résultat opérateur du 19 octobre 2026 après revue du bloc exact et autorisation distincte :** `G2A_LOCAL_METADATA: STOP`, `STOP_STAGE: WEBVIEW2_PARENTAGE`, `STOP_REASON: UNEXPECTED_OR_UNSAFE`, `G2B_G2C_G2D_G3_G4_G5_G6: NOT_AUTHORIZED`, `TAURI_RUNTIME: NOT_TESTED`. Ce compte-rendu est fourni par l'opérateur, pas un audit indépendant. L'ancien STOP `PROCESS_NAMES` reste dans l'historique. Le script masque volontairement le motif interne : parent absent, changement d'instantané, chronologie invalide ou échec CIM ne sont pas individuellement prouvés. **Ne pas relancer ce script ni un nouveau diagnostic sans revue et autorisation distinctes.** Aucune commande PowerShell exécutée automatiquement depuis ChatGPT.

**Hypothèse de défaut source identifié sans essai sur Windows :** le bloc PR #86 refuse tout `ProcessId <= 0` pendant la construction de la table complète `Win32_Process`, alors que cette classe peut retourner `System Idle Process` avec `ProcessId=0`. Si cet enregistrement figure dans l'inventaire, `AMBIGUOUS_PROCESS_ID` provoque le STOP avant tout parcours WebView2. Les 14 fixtures antérieures n'incluent aucun PID 0. Ce mécanisme est une **cause possible forte, non confirmée par la sortie opérateur** car le catch masque le sous-motif ; il faut des tests fictifs PID 0 et une future proposition explicite sans réexécution implicite. Références : https://learn.microsoft.com/en-us/powershell/module/cimcmdlets/get-ciminstance et https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-process .

## STOP historique PR #86 et interdictions toujours applicables

- `G2A_REVISED_RUNTIME=STOP_WEBVIEW2_PARENTAGE` (compte-rendu opérateur), `STOP_REASON=UNEXPECTED_OR_UNSAFE` ; cause fine inconnue. Le précédent `STOP_PROCESS_NAMES` reste historique. Aucun PASS de ce bloc historique PR #86 (le nouveau bloc PR #89 a ensuite produit un PASS de métadonnées).
- `G2-B/G2-C/G2-D/G3/G4/G5/G6=NOT_AUTHORIZED`, `REAL_G3_STOP_UNAVAILABLE`.
- `CLI_CONFIG_RESOLUTION_NOT_TESTED`, `TAURI_RUNTIME_NOT_TESTED`, `OPERATOR_ACCEPTANCE_NOT_PERFORMED`.
- Interdits : originales SQLite (v6 prod/v7 isolée), sidecars, ACL, sauvegardes, marker d'activation, migration 007, IPC writer, fusion PR #35, M3.3, release. Aucun reset Git destructeur ni faux relecteur indépendant.

## Prochaine action concrète

**Priorité actuelle au 20 octobre après le PASS local :** conserver le PASS limité aux métadonnées, requalifier la CI au nouveau HEAD documentaire, poursuivre seulement l'analyse source-only de l'absence d'écrivain SQLite NON PROUVÉE ; toute autre commande Windows nécessite un accord explicite neuf. Les étapes précédentes ci-dessous sont historiques.


1. Préserver ce nouveau STOP sans arrêter SearchHost/WebView2 ni répéter les observations locales.
2. Étudier sur sources et fixtures fictives une proposition DISTINCTE de diagnostic fail-closed produisant seulement un code de motif non personnel (`PROCESS_SNAPSHOT_CHANGED`, parent manquant, chronologie invalide, échec CIM, etc.), sans commande Windows aujourd'hui. Les métadonnées de parenté ne prouvent jamais l'absence de writer SQLite.
3. Avant tout script différent ou réexécution, afficher code intégral, interactions et effets ; obtenir un nouvel accord explicite. Aucun accès v6/v7, sidecars, G2-B/G2-C/G2-D ni G3–G6.
4. Re-fetch exact main/PR/CI/ruleset, mettre à jour MD+JSON à chaque PR significative ; requalifier CI au nouveau SHA après commit.

Se reporter à [HANDOFF_PROTOCOL.md](HANDOFF_PROTOCOL.md) pour les invariants détaillés, sans réutiliser les anciennes CI après un nouveau commit.
