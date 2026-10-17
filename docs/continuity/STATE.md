# Fabulaxiom — Current State

## 2026-10-18 — M3.2 : proposition de qualification du contexte Tauri compilé sans démarrage

La PR #64 (allowlist explicite `["default"]` réservée à `main` et garde-fous source-only) a été protégée fusionnée au nouveau `main=67b223af041436b720e68ce1cf06fad0da9ca920` ; CI Windows exacte #39072739826 terminale 47/47 SUCCESS, tests capability 10/10, frontend 129/129, Chromium 29/29, Rust 100/100. Ce résultat ne prouve pas la résolution native de la CLI ni le runtime. Une nouvelle PR distincte étudie la compilation effective `generate_context!` alimentée par un JSON fictif fusionné en mémoire et teste son contenu par Rust unit test **sans lancer Tauri** ; résultat de cette nouvelle PR EN ATTENTE de CI exacte.

Gates inchangés : `TAURI_RUNTIME_NOT_TESTED`, `OPERATOR_ACCEPTANCE_NOT_PERFORMED`, original G3 `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, réel G3-G6 `NOT_AUTHORIZED`, PR #35 `OPEN/DRAFT`. Aucune écriture réelle, base, migration 007, sauvegarde, activation, writer, M3.3 ou release.

## 2026-10-17 — M3.2 : audit complémentaire de sélection des capabilities Tauri (PR distincte, validation en cours)

Après PR #63 protégée fusionnée (`main=dc6d9559215e175bbf28187da6bc88fe0f1f75a5`; CI `pull_request` #39057235107 46/46 SUCCESS sur HEAD `1deb9ca0b02682a7954a92a8d8e2e6b10e733227`), la documentation Tauri v2 confirme qu'une liste `app.security.capabilities=[]` n'empêche PAS le chargement automatique des fichiers `capabilities/`. L'unique `default.json` présent cible `main` et non `m32-fiction`. Une PR de durcissement séparée propose `["default"]` non vide, des tests négatifs sur la sélection des capabilities, le modèle de fusion JSON, la présence de fichiers de plateforme et le maintien du chemin Rust fictif sans IPC. Résultats de cette nouvelle PR : **NON QUALIFIÉS tant que sa propre CI exacte n'est pas terminale**. La fusion native CLI, les droits effectifs Tauri et tout lancement Windows/WebView2 restent `NOT_TESTED` ; l'acceptation opérateur `NOT_PERFORMED`.

Limites inchangées : historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, original G3 `STOP_UNAVAILABLE`, G3/G4/G5/G6 réels `NOT_AUTHORIZED`, PR #35 `OPEN/DRAFT`. Aucun accès aux originaux v6/v7, sauvegardes/ACL/marqueurs ni migration 007, writer, M3.3 ou release. Voir `docs/qualification/M3_2_SYNTHETIC_TAURI_WINDOWS_PREVIEW.md`.

## 2026-10-17 — M3.2 : chemin Tauri fictif distinct de tout runtime SQLite

`main=1607f5705f0ec4a18a37542cf3e04d1df89ec2d6` protégé après PR #62 fusionnée (CI #39054598253, 43/43 étapes, Chromium 29/29, frontend 129/129, Rust 100/100). Branche nouvelle : feature Rust `m32-synthetic-preview` **opt-in/debug uniquement**, startup Tauri séparé **sans enregistrement d'IPC applicatif** ; overlay à identité `com.fabulaxiom.m32synthetic.preview`, une fenêtre fictive, URL boucle locale du laboratoire, capacités vides, protection `compile_error` release, exclusion mutuelle avec M3.1. **Pas de lancement autorisé** ; seuls tests de validation pure et compilation Windows seront qualifiés avant fusion. Rapport `docs/qualification/M3_2_SYNTHETIC_TAURI_WINDOWS_PREVIEW.md`.

**Autorités identiques** : historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, original G3 `STOP_UNAVAILABLE`, G3/G4/G5/G6 `NOT_AUTHORIZED`, PR #35 `OPEN/DRAFT`. Aucun original, marqueur, backup, migration 007, writer, M3.3 ni release.


## 2026-10-17 — M3.2 : amélioration de lisibilité/accessibilité du seul laboratoire fictif

Base protégée après PR #61 fusionnée : `main=f4da538a5e17ead5cf4ea3b06f2ec6aaf18a1e4a`, CI #39052427503 (43/43 étapes, Chromium 23/23, frontend 123/123, Rust 100/100). Nouvelle PR distincte : région de recherche nommée, annonces atomiques du filtre et des deux identifiants sélectionnés, états `aria-pressed` sur les boutons, CSS **uniquement page Vite fictive** (focus visible, boutons 44 px, cartes repliables). Six nouveaux tests Vitest (total ciblé **28**) et six tests navigateur Chromium (total **29**) proposés ; **pas de PASS avant la CI exacte de cette PR**. Document : `docs/qualification/M3_2_SYNTHETIC_EXPLORER_ACCESSIBILITY.md`. Aucun import `App.tsx`, ni dépendance, ni donnée opérateur.

**Toujours** source réelle `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, G3/G4/G5/G6 `NOT_AUTHORIZED`, PR #35 `OPEN/DRAFT`; pas de 007, activation, writer, M3.3 ni release.


## 2026-10-17 — M3.2 : filtrage et pagination dans l'explorateur fictif

Après PR #60 fusionnée (`main=53c3de511dec6a16da1c5a36e9f5eafee11be900`, CI Windows #39046517029 42/42, Chromium 14/14, frontend 101/101), proposition distincte de consultation sur huit assertions par page, filtre identifiants/libellés fictifs et statut courant/historique, choix explicite de premier/deuxième, chaîne de preuve lisible. Le graphe complet est validé **avant** tout filtre : pas de camouflage de cycle, d'identité historique ni de réattribution silencieuse. Nouveaux tests Vitest 22 et extension Chromium à 23 cas ; propre CI exacte à qualifier avant fusion. Composant **non monté dans App.tsx**, aucun original, IPC ou dépendance modifiés. Rapport `docs/qualification/M3_2_SYNTHETIC_EVENT_EXPLORER.md`.

**G3 source `STOP_UNAVAILABLE` ; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, G3–G6 réels `NOT_AUTHORIZED`, PR #35 `OPEN/DRAFT`.** Pas de 007, marqueur, writer, M3.3 ou release.


## 2026-10-17 — M3.2 : qualification navigateur réelle sur parcours React fictif

Autorité initiale protégée `main=008761b0778b8ad3dd5e5dd711ef406394bf41d2`, après PR #59 fusionnée et CI #39044031084 41/41 (24/24 nouveaux tests React). Nouvelle qualification distincte : page Vite de laboratoire **non reliée à App.tsx**, scénarios fictifs littéraux, Playwright Chromium headless exécuté **uniquement** sur Windows CI avec package version fixe en `RUNNER_TEMP`; 14 cas de sélecteurs, clavier, remise à zéro, justification avant/après et refus de cycle. Pas de dépendances du projet changées, d'original ouvert, d'IPC, de production 007 ou de marqueur modifié. **CI exacte de cette PR à valider avant toute fusion.** Rapport : `docs/qualification/M3_2_SYNTHETIC_REAL_BROWSER_INTERACTION.md`.

G3 source `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, réel G3–G6 `NOT_AUTHORIZED`, PR #35 `OPEN/DRAFT`, pas de M3.3 ni release.


## 2026-10-17 — M3.2 : parcours React fictif de consultation avec sélection explicite

Après PR #58 protégée fusionnée (`main=125579506e7b7485e9ffab3163fe62193fee321d`, CI #39035926354 40/40, 24/24 nouveaux tests React), une PR indépendante propose une **composition non montée** de `M32ChronologyPreview` et `M32WorldOrderComparison`, avec deux choix explicites d'identifiants actifs, rendu des preuves humaines et veto de graphe même avant sélection. `24` nouveaux tests Vitest synthétiques sont proposés, avec CI exacte à qualifier. Aucun composant injecté dans `App.tsx`, aucune source opérateur, aucune IPC ni écriture. Rapport : `docs/qualification/M3_2_SYNTHETIC_REACT_CONSULTATION_FLOW.md`.

**G3 réel `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, G3-G6 `NOT_AUTHORIZED`, PR #35 `OPEN/DRAFT`.** Pas d'original, migration 007, activation, writer, M3.3 ni release.


## 2026-10-17 — M3.2 : comparaison React autonome d'ordres humains fictifs

`main=20e3176896da325cbbd8683bb7692161cd7ad6f0` vérifié après PR #57 fusionnée et CI #39033928000 39/39 PASS (18/18 nouveaux tests React). Nouvelle proposition : composant **non monté** `M32WorldOrderComparison.tsx`, sur projections fictives seulement, produisant `before/after/same/incomparable` avec chaîne d'arêtes explicitement déclarées ; veto des cycles, références historiques actives et paires répétées. Aucun ordre calendaire ou narratif induit. Qualification Windows sur le HEAD exact **à effectuer** ; pas d'IPC, base, import App ni bouton d'édition. Rapport : `docs/qualification/M3_2_SYNTHETIC_REACT_ORDER_COMPARISON.md`.

**G3 réel reste `STOP_UNAVAILABLE`**, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, G3-G6 `NOT_AUTHORIZED`, PR #35 `OPEN/DRAFT`. Pas de migration 007, original, activation, writer, M3.3 ni release.


## 2026-10-17 — M3.2 : extraction ciblée de la projection React fictive

Autorité initiale `main=f4011f03842af249cf4df5114b0a62b01eafef98` (PR #56 fusionnée, CI Windows #39030884718 38/38 PASS). La PR #35 demeure OPEN/DRAFT, 84 fichiers non fusionnés. Un composant React **strictement non monté** (`src/M32ChronologyPreview.tsx`) est repris indépendamment comme laboratoire de chronologie mondiale, ordre narratif et révélation lecteur non renseignée, avec contrôle d'Univers, identités, dates fictives et refus des projections invalides. **18 tests Vitest synthétiques** sont proposés. La qualification Windows exacte de cette nouvelle PR reste exigée : aucun PASS anticipé, aucun IPC Tauri ni original ouvert. Rapport : `docs/qualification/M3_2_SYNTHETIC_REACT_CHRONOLOGY_VIEW.md`.

**Gates inchangés :** G3 source `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, G3/G4/G5/G6 réels `NOT_AUTHORIZED` ; pas de 007, marqueur, writer, M3.3, release ou fusion de PR #35.


## 2026-10-17 — M3.2 G3 : frontière de provenance SQLite/Win32 après PR #55

L'autorité protégée initiale est `main=e159b994b2ae09f852416540d3243b3a0d35dec3` après PR #55 fusionnée (CI Windows #39029700107 : 37/37 étapes ; acteur Rust RAM 11/11 tests PASS). La qualification suivante recense les raccourcis invalides pour obtenir une provenance : chemin `sqlite3_db_filename`, objet `SQLITE_FCNTL_FILE_POINTER`, pointeur SQLite brut, handle Win32 **différent** de celui du propriétaire SQLite, URI `immutable=1` et réouverture migrante. Une matrice pure négative et un contrôle des sources Rust publiques interdisent toute promotion automatique G3. Rapport : `docs/qualification/M3_2_G3_SOURCE_IDENTITY_API_BOUNDARIES.md`. **Nouvelle PR non qualifiée tant que sa propre CI sur HEAD exact n'a pas réussi.** Pas d'original ouvert, de source publiée ni de Tauri runtime modifié.

**Vérité inchangée** : source réelle authentifiée `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, G3/G4/G5/G6 réels `NOT_AUTHORIZED`, PR #35 `OPEN/DRAFT`, pas de 007 production, bascule, writer, M3.3 ou release.


## 2026-10-17 — M3.2 G3 : transfert de propriétaire Rust RAM entre threads (qualification séparée)

Après PR #54 fusionnée (`main=8cbb8671194afee48d96194aae7863ddd46e9b3d` ; Windows CI #39020636502 36/36, nouveaux audits 9/9), la prochaine expérience reproduit uniquement le transfert par valeur d'une connexion SQLite **inventée en RAM** vers un thread Rust dédié, avec canal borné, réponses sans handle, refus des clés étrangères orphelines et révocation/poison/arrêt définitifs. Tests sous `cfg(test)` et feature `m32-g3-owned-ram-toy` hors builds normaux ; aucune commande Tauri ni source opérateur. Qualification sur nouveau HEAD Windows `pull_request` exigée, **non encore acquise**. Rapport : `docs/qualification/M3_2_G3_RUST_RAM_OWNER_HANDOFF_ACTOR_TOY.md`.

**Aucun propriétaire source réel authentifié démontré : `STOP_UNAVAILABLE`**, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, G3/G4/G5/G6 réels `NOT_AUTHORIZED`, PR #35 `OPEN/DRAFT`. Pas de source ouverte, 007, marqueur, writer, M3.3 ni release.


## 2026-10-17 — M3.2 G3 : analyse de frontière Tauri, source uniquement (PR séparée en qualification)

La revue du code Rust sur `main=3d6b69cb52e235af06cfea019cb0ec820a6ccaf0` constate l'absence de propriétaire SQLite persistant et authentifié dans les deux runners Tauri. Les commandes `database_status`, `hierarchy`, `entity` passent par des ouvertures migrantes, et la sauvegarde applicative ne conserve pas la réservation exclusive de sortie durant l'opération `VACUUM INTO`. Une qualification distincte examine cette topologie et ses dérives futures via des tests lisant le code public du dépôt, sans accès aux bases opérateur. Rapport : `docs/qualification/M3_2_G3_TAURI_OWNER_INTEGRATION_AUDIT.md`. **PR non encore qualifiée ; ne pas déclarer PASS avant sa propre CI exacte.** Aucun Tauri State, service runtime, source ouverte ni nouvelle commande n'est ajouté.

**Réel : `STOP_UNAVAILABLE`.** Historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, G3/G4/G5/G6 réels `NOT_AUTHORIZED`, PR #35 `OPEN/DRAFT` ; aucune migration 007, activation, writer ni M3.3.


## 2026-10-17 — M3.2 G3 : contrat de service propriétaire non migrant, code uniquement

Autorité initiale `main=fd2149131c61ef94180de28c6144e18a5c76deb5` après PR #52 fusionnée : **18/18 tests Rust RAM** et CI Windows **34/34** (SHA corrigé `335ca8f...`). La suite autorisée est une spécification de service de connexion persistante **sans accès aux originaux** : source attestée indépendamment, connexion préexistante, absence de migrations, révocation, sérialisation, photographie SQLite transactionnelle, publication exclusive et restauration isolée. Le modèle `m3_2_g3_owner_runtime_contract.py` ne donne jamais d'autorisation G3 réelle. La CI lit uniquement le code Rust du dépôt pour confirmer que les chemins actuels `open_database`, `database_status`, `create_backup` restent à effets et interdits comme procédure G3. Aucun nouveau runtime, Tauri command ni chemin de base n'est créé.

**Verrous inchangés :** `historical=PENDING_EXTERNAL_ATTESTATION(21/3/2)`, `prospective=NOT_STARTED`, `real_G3/G4/G5/G6=NOT_AUTHORIZED`, PR #35 OPEN/DRAFT, pas de migration 007, marqueur d'activation, IPC writer ni M3.3.


## 2026-10-17 — M3.2 Rust : propriétaire de connexion fictif et cycle de vie révoquable

À partir du `main=d01c7a55b6b7abb7db6228d4d266da03610df9f7` (PR #51 fusionnée, 33/33 CI Windows et 13/13 tests Rust RAM), la nouvelle expérience `m32_owner_lifecycle_toy` ajoute un cycle de vie fictif de connexion SQLite déjà ouverte : `OwnerSlot` non clonable, jeton de session/révision expérimental, copie transactionnelle RAM, révocation définitive, verrou `Mutex` et refus des réutilisations périmées. Le module reste strictement derrière le `cfg(test)`/feature flag existant, sans commande Tauri, entrée fichier, ni nouvelles dépendances. Les jetons fictifs **ne constituent pas** une identité/provenance de fichier réel. Contrats et risques : `docs/qualification/M3_2_G3_RUST_OWNER_LIFECYCLE_TOY.md`.

**Interdictions inchangées :** `G3/G4/G5/G6 réels=NOT_AUTHORIZED`, `prospective=NOT_STARTED`, `historical=PENDING_EXTERNAL_ATTESTATION(21/3/2)`, PR #35 OPEN/DRAFT, pas de production 007, marker, IPC writer ou M3.3.


## 2026-10-17 — Prototype rusqlite Online Backup strictement tests Rust en RAM

Après PR #50 fusionnée depuis `main=e1039395fb720b0e7624b066191db7a34984d063`, l'expérience suivante est `m32-g3-owned-ram-toy` : activer `rusqlite/backup` uniquement via un **feature flag hors configuration par défaut**, ajouter une erreur de compilation hors `cfg(test)`, puis vérifier sur un schéma fictif créé exclusivement par `Connection::open_in_memory()` la copie transactionnelle de la connexion source déjà ouverte vers une seconde connexion RAM. Aucune création de fichier ni chemin de base n'est possible par ces fonctions de test. Les commandes actuelles `open_database`, `database_status`, `create_backup` restent migrantes ou à effets et **interdites** sur les originaux M3.2. Laboratoire Rust distinct du laboratoire Python #50.

**Vérité réelle inchangée :** `G3/G4/G5/G6=NOT_AUTHORIZED`, `prospective=NOT_STARTED`, `historical=PENDING_EXTERNAL_ATTESTATION(21/3/2)`, PR #35 OPEN/DRAFT, pas de 007, activation, IPC writer ou M3.3.


## 2026-10-17 — G3 : prototype transactionnel Python fictif depuis connexion déjà ouverte

Après PR #49 fusionnée sur `main=aaa8550dacfc88ac3f335598f66dd2928709e35e`, la voie choisie reste une **connexion applicative déjà ouverte et identifiée** suivie de SQLite Online Backup vers RAM. Le travail autorisé suivant n'est qu'un laboratoire : génération interne de schémas inventés v6/v7, connexion fictive créée avant capture, snapshot transactionnel RAM, contrôle `schema_migrations`/intégrité/FK, publication exclusive dans un dossier temporaire neuf et restauration isolée. La source réelle ne possède **aucune** connexion de provenance attestée ; le module Rust courant `open_database` migre et reste interdit pour G3. Les essais WAL peuvent nécessiter une normalisation `VACUUM` **en RAM uniquement** : aucune fidélité binaire aux fichiers historiques n'est revendiquée.

**Réel :** `G3/G4/G5/G6=NOT_AUTHORIZED`, `prospective=NOT_STARTED`, `historical=PENDING_EXTERNAL_ATTESTATION(21/3/2)`, PR #35 DRAFT, pas de migration 007, writer IPC, bascule d'activation ni M3.3.


## 2026-10-16 — G3 : stratégie transactionnelle choisie, origine réelle toujours NON accessible

Le checkpoint d'autorité est `main=74933c49229ab9efeae5e7c017a61b28525d3fd3`, après la fusion de PR #48 (30/30 CI Windows, 11/11 tests ABA fictifs). Préférence d'architecture : SQLite Online Backup API à partir d'une **connexion applicative déjà ouverte, détenue et authentifiée** ; ne jamais démarrer l'application ni ouvrir une base originale uniquement pour produire cette connexion sans une nouvelle autorisation. Alternative conditionnelle : acquisition froide uniquement après preuve de quiescence de tous les writers, identité du source et des ancêtres, et journaux entièrement résolus. Les deux routes sont actuellement indisponibles sur les originaux. La politique pure `tools/m3_2_g3_source_strategy_policy.py` refuse toute autorisation réelle, même avec tous les indicateurs synthétiques vrais. Dossier : `docs/qualification/M3_2_G3_SOURCE_ACQUISITION_DECISION.md`.

**Statuts immuables :** `G3/G4 réels=NOT_AUTHORIZED`, `prospective=NOT_STARTED`, `historical=PENDING_EXTERNAL_ATTESTATION(21/3/2)`, PR #35 OPEN/DRAFT ; pas de migration 007, bascule d'activation, IPC writer ou M3.3.


## 2026-10-16 — PR #47 G3/G4 fictif fusionnée ; anti-ABA reste non démontré

L'autorité GitHub pour cette nouvelle qualification part du `main=106c48fe3b2fd8b16bd038d29c15c99ef9e5f5db` exact : PR #47 fusionnée après CI Windows #38947114710 **29/29 SUCCESS**, dont **16/16 tests** synthétiques G3→G4. Les copies ont été créées exclusivement sous répertoires temporaires fictifs, sans fichier ou chemin opérateur. L'ancien échec Win32 de PR #46 (#38943063529, renommage autorisé malgré absence de FILE_SHARE_DELETE) reste une découverte de sécurité significative. Le présent travail autorise uniquement une **expérience de contre-exemple ABA** : un renommage/restauration entre deux observations peut être invisible, même lorsque les empreintes de fin semblent valides. Les préflights G2-A/B/C/D et G3 destination sont des observations ponctuelles, pas une capture transactionnelle.

**Vérité inchangée :** `historical=PENDING_EXTERNAL_ATTESTATION(21/3/2)` ; `prospective=NOT_STARTED` ; `G3/G4 réels=NOT_AUTHORIZED` ; PR #35 OPEN/DRAFT ; aucun fichier SQLite, marqueur, sauvegarde ou worktree opérateur touché par GitHub.


## 2026-10-16 — G2 opérateur contrôlé, G3 laboratoire Win32 terminé, capture réelle NON commencée

État exact GitHub vérifié à la création de cette note : `main=b2d8249002cbea8b11edcaedaa9602bd946a62c7`. PR #42 (sauvegarde exclusive image mémoire) fusionnée après CI Windows #38914716036 **25/25 PASS**, incluant 14 tests fictifs. PR #43 (verrou de lecture Win32 et refus de journaux dangereux sur bases fictives) fusionnée après CI Windows #38917979449 **26/26 PASS**, incluant 12 tests fictifs. PR #35 chronologie M3.2 reste OPEN/DRAFT et non fusionnée.

Les observations de l'opérateur du 16 octobre : G2-A jeton moyen non administrateur, processus WebView2 reliés à Windows Search sans prouver la quiescence globale ; G2-B quatre rôles privés identifiés, 7/7 worktrees protégés reconnus, marqueur pointant vers la v6 restaurée ; G2-C doubles SHA-256 physiques stables pour les quatre fichiers, les deux v7 identiques octet-à-octet ; G2-D corrigé, en-têtes des trois SQLite `ROLLBACK`, pages 4096, `user_version=0` (le schéma Fabulaxiom s'obtient de `schema_migrations`). G3 préflight destination opérateur : volume NTFS fixe, jeton standard, parents sans reparse observés, ACL lisible, **191,13 Gio libres**, dossier futur absent. **Aucun répertoire G3 créé, aucune source SQLite ouverte en SQL, aucune capture ni restauration réelle.** Les preuves locales restent privées ; ne pas publier les chemins, octets, SHA de fichiers privés ou ACL sur GitHub.

Les essais CI prouvent seulement les propriétés de **fixtures synthétiques** ; aucun contrôle n'établit encore la correspondance atomique stable entre le chemin d'une source réelle et un handle Windows, l'absence de writers/concurrences, la sûreté des ancêtres contre substitution, l'identité de la destination, ni la cohérence logique réelle. Historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, G3–G6 réels `NOT_AUTHORIZED`. Jamais de migration 007 en production, d'IPC writer, de bascule M1.5, de fusion PR #35 ou M3.3.


## 2026-10-16 — G2 préflight Windows : plan préparé, aucun original touché

Après re-fetch de protected `main=b6b4d6d9f6a52638a1ccd004e8a3ed5cc10026f6`, #39/#37/#40 sont fusionnées après leurs CI exactes ; #35 est OPEN/DRAFT. La nouvelle note `docs/qualification/M3_2_G2_WINDOWS_SOURCE_IDENTITY_PREFLIGHT_PLAN.md` fixe la séparation G2-A (processus/jeton/Git sans fichier protégé), G2-B (métadonnées des chemins privés), G2-C (hash sources), G2-D (évaluation d'une éventuelle ouverture SQLite), chacune avec son accord opérateur exact. Des chemins historiquement fournis existent dans des échanges privés mais leur état **courant** doit être vérifié exclusivement sur l'hôte Windows ; **aucun chemin privé n'est publié ici**. `prospective=NOT_STARTED`, `M3.2_runtime=NOT_AUTHORIZED`, historique 21/3/2 `PENDING_EXTERNAL_ATTESTATION`. Aucun PowerShell local exécuté, aucun G2 déclaré PASS, aucun writer/007/activation/merge #35.


## 2026-10-15 — PR #39 gouvernance SOLO fusionnée ; PR #37 en réconciliation, pas d'exécution

La proposition documentaire SOLO de PR #39 a été protégée-fusionnée sur `main=86d1773ff32e710b719ed0ec35fb7a734de3cd75` après CI pull_request #38799012304 23/23 SUCCESS. L'opérateur a autorisé la démarche en quatre étapes dans ChatGPT ; ce n'est ni une signature indépendante ni le consentement à un bloc Windows précis. PR #37 propose **séparément** de remplacer le reviewer obligatoire **pour la seule baseline prospective**, tout en laissant la fiche de revue humaine `AWAITING_INDEPENDENT_REVIEW` et les cinq rôles historiques `PENDING_EXTERNAL_ATTESTATION` 21/3/2. L'adoption de ce protocole après CI/fusion ne crée pas de backup : prospective `NOT_STARTED`, M3.2 réel `NOT_AUTHORIZED` ; aucun G2–G6 effectivement qualifié, pas de production 007, writer, merge #35 ou M3.3.


## 2026-10-15 — Proposition opérateur unique, PAS d'exception appliquée

Une PR documentaire **distincte** propose `docs/qualification/M3_2_SOLO_OPERATOR_COMPENSATING_CONTROLS.md` et une fiche de décision. Elle envisage des vérifications techniques diversifiées, contradictoires, répétées et une **acceptation explicite du risque par le propriétaire** ; ce ne sont **pas** des revues humaines indépendantes. Elle ne modifie PAS la PR #37 ni sa condition `AWAITING_INDEPENDENT_REVIEW`, qui demeure bloquante jusqu'à une **future adoption explicite et réconciliation** des documents d'autorité. Historique `PENDING_EXTERNAL_ATTESTATION` 21/3/2, prospective `NOT_STARTED`, M3.2 réel `NOT_AUTHORIZED`. Aucune opération sur les données Windows, aucune migration 007, aucun writer, aucune fusion de PR #35, aucun M3.3.


## Current authority — M3.1 implementation merged; independent normalization pending (2026-10-11)

- **Repository visibility: PUBLIC**, `main` genuinely branch-protected by active repository ruleset [Protect main](https://github.com/LaurentCOLL1/Fabulaxiom/rules/24895490). Rules include deletion/force-push denial, pull request and strict exact-app GitHub Actions check `Windows frontend and Rust checks` (app 15368), with no bypass actors or mandatory external approval (solo developer).
- Implementation PR [#33](https://github.com/LaurentCOLL1/Fabulaxiom/pull/33) **MERGED**, final head `796a4b65e596b9bc05bd00b523b3209f9736524d`, strict required-check [CI #38176139985 attempt 3](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/38176139985) **completed/success** (23 Windows job steps SUCCESS). Guarded implementation merge: `922d155d4f4321ed8b90955d4ea96388751f0daf`; fresh `main` re-fetch confirmed.
- Actual Windows isolated v7 GUI and read-only IPC **PASS** on operator-qualified source `4d520e1825ecd08d20484b0e72d60ffe6ea09e4c`; after controlled exit, **11/11** original and isolated SHA-256 preserved, M1.5 restored-active production v6 marker unchanged, no SQLite sidecars. Second launch worked in medium-integrity standard Windows token after approved, individually backed-up user-SID-only ACL adjustment to existing isolated Tauri identity. No live executable path/PID snapshot was obtained; avoid asserting it.
- PR #33 adds prevention for future elevated Windows `--prepare`, tested with synthetic fail-closed fixtures and a real no-staging Win32 token API smoke check. Normal runtime SQLite remains **v6**, `007` is not in automatic migrations. **A successful isolated preview is not a production v7 migration**.
- **This separate normalization PR is documentary only**, must obtain its OWN terminal exact-head `pull_request` CI and protected SHA-guarded merge. Until then M3.1 is **IMPLEMENTATION MERGED / NORMALIZATION PENDING** and M3.2 remains unauthorized. Detailed gate: `docs/qualification/M3_1_POST_MERGE_NORMALIZATION.md`.

Historical checkpoints below are preserved for audit and must not override this authority.

## Current M3.1 candidate checkpoint (PR #33; not merged)

On Windows (2026-10-11), actual isolated debug-only v7 Tauri GUI and read-only diagnostic IPC **PASS**, then 11/11 protected bytes and restored-active v6 M1.5 pointer **PASS after closure** at qualified operator head `4d520e1825ecd08d20484b0e72d60ffe6ea09e4c`, CI #38160997846 success. The initial WebView2 failure was due to restrictive NTFS access to an elevated-operator-prepared identity; the old ACL was backed up and only the isolated root was granted current-user Modify, with medium-integrity requalification. Detailed evidence: `docs/qualification/M3_1_WINDOWS_OPERATOR_EVIDENCE.md`.

The current PR adds a fail-closed Windows elevated-token guard before any NEW isolated `--prepare`, while leaving the existing qualified identity untouched. Its newer HEAD and CI must be verified **separately**. Earlier milestone notes below are historical main checkpoints, not assertions that M3.1 is merged. **No production v7 migration or 007 automatic migration; M3.1 not yet COMPLETE + MERGED + NORMALIZED; M3.2 unauthorized.**

## Repository

- Repository: `LaurentCOLL1/Fabulaxiom`
- Visibility: **public**
- Default branch: `main`

## Milestone state

### M0 — Environment and architecture qualification

**COMPLETE + MERGED + NORMALIZED**

### M1 — Persistence and project foundation

**COMPLETE + MERGED + NORMALIZED**

#### M1.1 — SQLite foundation and migration runner

**COMPLETE + MERGED + NORMALIZED**

Final normalization merge:

`d99da744fc04303c0c094a8aa6a2daab9983136f`

#### M1.2 — Project hierarchy schema

**COMPLETE + MERGED + NORMALIZED**

Implementation PR:

**#9 — feat: implement M1.2 project hierarchy schema**

Implementation merge:

`91b80e529679d3bc407b5f6ca49e578d86de1d44`

Qualified implementation SHA:

`3d4b2eaf95e13bfa93580a4295ac20e93a076798`

Qualification evidence commit:

`0da679859c77ef231c6b33e9e91c7264c8d7b5f6`

Deterministic exact-head CI:

- workflow: `Fabulaxiom CI`;
- terminal run: `37646868694`;
- result: `completed/success`;
- frontend tests/build: PASS;
- Rust tests: 13/13 PASS;
- `cargo check --locked`: PASS;
- dependency lockfiles unchanged.

Windows production migration qualification:

- schema-v1 production database detected;
- pre-migration SQLite backup created;
- migration v1 → v2: PASS;
- migrations 1 and 2 present exactly once;
- hierarchy tables 5/5 present;
- SQLite STRICT 5/5;
- immutable-ID triggers 5/5;
- foreign keys ON;
- `PRAGMA foreign_key_check`: empty;
- `PRAGMA integrity_check`: `ok`;
- Rust bridge: PASS;
- database status: PASS;
- Ollama local status: PASS;
- worktree clean.

Detailed evidence:

`docs/qualification/M1_2_PROJECT_HIERARCHY_SCHEMA.md`

#### M1.3 — No-AI CRUD service

**COMPLETE + MERGED + NORMALIZED**

Implementation PR:

**#11 — feat: implement M1.3 no-AI CRUD service**

Implementation merge:

`49424f1ecafa1be3c4f47b806231b6644e9c73a4`

Qualified implementation SHA:

`6259bd3b4759b683bf4bb7c2c6efdf693ddfebac`

Qualification evidence commit:

`d9df8151b0c3336e0a12c65a7ba7841cab4e091b`

Terminal exact-head CI:

- workflow: `Fabulaxiom CI`;
- run: `37684422252`;
- result: `completed/success`;
- frontend tests: 8/8 PASS;
- frontend build: PASS;
- Rust tests: 20/20 PASS;
- `cargo check --locked`: PASS;
- dependency lockfiles unchanged.

Windows no-AI CRUD qualification:

- exact implementation source and clean worktree: PASS;
- Ollama process absent and loopback API inaccessible;
- local frontend tests/build: PASS;
- local Rust tests/check: PASS;
- Rust bridge: PASS;
- SQLite schema v2 / foreign keys ON: PASS;
- Ollama status expected unavailable;
- full Universe / Series / Novel / Chapter / Scene CRUD: PASS;
- optional-Series workflow: PASS;
- deterministic reorder: PASS;
- rename at every hierarchy level: PASS;
- cross-Universe Series protection: PASS;
- parent deletion guards with `has_children`: PASS;
- CRUD remained operational with Ollama stopped;
- qualification data cleanup: PASS;
- `PRAGMA foreign_key_check`: empty;
- `PRAGMA integrity_check`: `ok`;
- final worktree clean;
- Ollama remained stopped.

Detailed evidence:

`docs/qualification/M1_3_NO_AI_CRUD_SERVICE.md`

Delivered M1.3 foundation:

- Rust application models/DTOs separate from SQLite rows;
- CRUD service for all five hierarchy levels;
- explicit transaction boundaries for compound mutations;
- deterministic application/Tauri error payloads;
- thin Tauri commands;
- React hierarchy CRUD workspace;
- no Ollama dependency for CRUD;
- preserved M1.1/M1.2 persistence guarantees.

#### M1.4 — Text revisions and provenance foundation

**COMPLETE + MERGED + NORMALIZED**

Implementation PR:

**#13 — feat: implement M1.4 text revisions and provenance foundation**

Implementation merge:

`75ab73b176b481f64b0e7f8c510b4ede0c617e31`

Qualified implementation SHA:

`d62fe92e4c01e5a58a6fbf85bdcf465267b41ea6`

Windows qualification evidence commit:

`e6b3bf13399604a3b4922f9510a1c6761d9e5775`

Terminal exact-head CI:

- workflow: `Fabulaxiom CI`;
- run: `37709917550`;
- result: `completed/success`;
- frontend tests: 10/10 PASS;
- Rust tests: 29/29 PASS;
- frontend build and `cargo check --locked`: PASS;
- lockfiles unchanged.

Windows qualification:

- source exact, worktree clean, Ollama stopped;
- production SQLite schema v2 backed up via SQLite Backup API; SHA256 preserved;
- production migration v2 → v3 PASS;
- two `STRICT` revision tables and three migrations present;
- immutable append-only scene text revisions, lineage and current pointer;
- operator-reported create v1/v2, restore v1 and save v3 scenario PASS;
- persisted three revisions, one current head;
- `PRAGMA foreign_key_check`: empty;
- `PRAGMA integrity_check`: `ok`;
- Ollama remained stopped through qualification.

Detailed evidence:

`docs/qualification/M1_4_TEXT_REVISIONS_PROVENANCE.md`

Delivered M1.4 foundation:

- schema v3 for scene text revisions and explicit current heads;
- immutable revision IDs, database timestamps and per-scene revision ordering;
- parent revision provenance;
- transactional creation and pointer changes;
- guarded scene deletion with existing revision history;
- Rust/Tauri revision commands and React editor/history;
- no dependency on Ollama.

#### M1.5 — Backup and restore baseline

**COMPLETE + MERGED + NORMALIZED**

Implementation PR: **#15 — feat: implement M1.5 safe SQLite backup and restore baseline**

Implementation merge:

`282b325fb6c588a70df08a5128415c8fa0a0f72e`

Windows-qualified implementation SHA:

`7f968075f632843144c9833f61cc51910b538530`

Windows qualification evidence commit:

`152b40e616f40799abc61f9ce8db142e3b19340b`

Terminal exact-head CI:

- workflow: `Fabulaxiom CI`;
- run: `37720676744`;
- result: `completed/success`;
- frontend tests: 13/13 PASS;
- Rust tests: 37/37 PASS;
- frontend production build: PASS;
- `cargo check --locked`: PASS;
- dependency lockfiles unchanged.

Windows qualification:

- exact main/PR HEAD and local worktree clean: PASS;
- SQLite schema v3 and Tauri/Rust bridge PASS;
- Ollama unavailable as intended;
- application-created verified backup: PASS;
- UI-confirmed restore and reload: PASS;
- 1 Universe, 1 Novel, 1 Scene, 3 revisions, 1 current revision head preserved;
- previous active database is not overwritten by the restore design;
- operator historic backups are preserved;
- actual restored database path and independent post-restore integrity PRAGMAs were not supplied as evidence;
- three nonfatal Rust unused-code warnings remain tracked.

Detailed evidence:

`docs/qualification/M1_5_BACKUP_RESTORE_BASELINE.md`

Delivered:

- SQLite-consistent `VACUUM INTO` snapshot to app-owned unique backup files;
- schema owner, migration and integrity validation;
- new non-overwriting database file for restore;
- durable activation marker and old database preservation;
- deterministic Rust/Tauri errors and explicit restore confirmation;
- React backup/list/restore controls without Ollama;
- source preservation, failure and backup/restore automated tests.

### M1 closure

M1.1–M1.5 are all **COMPLETE + MERGED + NORMALIZED**. M1's database, hierarchy, revision history and backup/restore baseline are delivered and qualified. This is **not** a declaration that V1 as a whole is complete.

### M2 — Narrative entities and canonical facts

**COMPLETE + MERGED + NORMALIZED** — M2.5 independent normalization PR #30 protected-merged at `f13b4f8c249866ff60a19d7895b6cfaede56398a` after its exact-head CI #38041908126 (13/13 Windows job steps SUCCESS). M2 is closed; M3 has not been implemented or authorized.

Detailed planning PR #17 merged at `4a9115ec362a0efae696ebc94b5101fa46d7a03a`.

Accepted roadmap: `docs/roadmap/M2_NARRATIVE_ENTITIES_CANONICAL_FACTS.md`.

#### M2.1 — Entity registry schema and migration

**COMPLETE + MERGED + NORMALIZED**

Implementation PR: **#20 — feat: implement M2.1 narrative entity registry schema v4**.

Implementation merge:

`6c58b3bd4f0588436da8ba45adb875f897f426b2`

Qualified implementation SHA:

`c7a663d88ba2538714d42fdd366719cd54fe6f70`

Windows qualification evidence SHA:

`88fa3b22904b92d4ecdcb32ed7fd01dc23e24a4c`

Terminal exact-head CI:

- workflow: `Fabulaxiom CI`;
- run: `37814949619`;
- `completed/success`;
- frontend 13/13, Rust 44/44 tests PASS;
- frontend build, `cargo check --locked` and lockfile check PASS.

Windows production schema-v3 → schema-v4 qualification:

- actual restored active database resolved from M1.5 activation marker, not assumed default;
- source and backup verified before migration, backup SHA256 preserved;
- migration v4 applied by Tauri, four migrations recorded exactly once;
- both new narrative registry/alias tables STRICT;
- four immutable-identity triggers, two indexes;
- six narrative kinds constrained at schema level;
- existing hierarchy, metadata, revision and current-head rows unchanged in logical value;
- three scene text revisions and one current revision head preserved;
- `PRAGMA foreign_key_check` empty and `PRAGMA integrity_check` `ok`;
- no Ollama dependency; final worktree CLEAN;
- original backup and active activation marker unchanged.

Detailed evidence:

`docs/qualification/M2_1_ENTITY_REGISTRY_SCHEMA.md`

Delivered M2.1 scope:
- SQLite schema v4 for Universe-scoped narrative entity registry and aliases;
- immutable IDs, entity kind and Universe ownership; FK restrictions/indexes;
- M1.5 v3/v4 backup and safe legacy-v3 restore compatibility;
- deterministic regression tests;
- **no** entity CRUD UI, fact/canon engine, image/ComfyUI code.

#### M2.2 — No-AI entity and alias CRUD

**COMPLETE + MERGED + NORMALIZED** — normalized after independent post-merge PR acceptance.

Implementation PR: **#23 — feat: implement M2.2 no-AI narrative entity and alias CRUD**.

- Original base `main`: `70beb4f998ba3e587533dd7a90689eadeae4f4c3`.
- Windows-qualified code source: `b54fffd8e1f0224372e3b99cee07cb6df3203973`.
- Targeted React alias crash fix: synchronous `currentTarget.value` capture, per-entity alias drafts, IPC response validation and scoped render error boundary.
- Source-head `Fabulaxiom CI`: `37831790345`, `completed/success`.
- Operator Windows evidence commit: `a96870f823f24cb8962c9b0f43336ccb883ad5c3`.
- Evidence exact-head `Fabulaxiom CI`: run `37864503602`, event `pull_request`, `completed/success`; Windows job and every step successful.
- Protected implementation merge PR #23: `ad7211fa2f292b8bd9812e299dbb6be96214eb89`, with expected head SHA `a96870f823f24cb8962c9b0f43336ccb883ad5c3`.
- The separate normalization PR must have terminal exact-head CI and be merged before this normalized status takes effect.

Real Windows acceptance on qualified source:

- `npm ci`, frontend **21/21** tests, frontend build, Rust **51/51** tests, `cargo check --locked`, lockfile checks: PASS; worktree CLEAN.
- **13/13 operator interactive cases PASS**: six kinds, create/add/rename/delete alias, duplicate rejection, per-entity drafts, same-name distinct character identities, restrictive parent deletion, remaining modules visible with Ollama OFF.
- Actual restored SQLite database resolved through M1.5 active marker, not assumed default.
- Postinteractive schema v4, four migrations, two STRICT tables, four immutable-identity triggers, required indexes, `foreign_key_check=[]`, `integrity_check=ok`: PASS.
- Postinteractive 9 narrative entities and 8 aliases preserved; two same-name character rows have distinct IDs; 3 immutable scene text revisions and 1 current pointer unchanged, with matching pre/post SHA-256 digests.
- Historical pre-M2.1 operator backup SHA-256 preserved; no local database or backup cleanup or restoration performed.
- Nonfatal Rust warnings remain deferred to a separately qualified change.

Detailed evidence: `docs/qualification/M2_2_ENTITY_ALIAS_CRUD.md`.

Delivered M2.2: Rust/Tauri/React no-AI CRUD for six Universe-scoped narrative entity kinds and owner-scoped aliases, deterministic validation/negative paths, stable identity and restrictive deletion. No canon/facts, chronology, search, AI-writing or visual/ComfyUI implementation.

#### M2.3 — Fact registry and exact revision provenance

**COMPLETE + MERGED + NORMALIZED — effective after the independent M2.3 normalization PR passes exact-head CI and is merged.**

Implementation PR #25; Windows-qualified source `4d3b4b6015d477c3a6a5c3750d9743174e9c44a7`; qualification evidence commit `b015f7df80f38d75375a0e2615fd62d4c40ee1b8`; implementation merge on `main` `e6e80c26316f11054348a18a235fd08c600e136e`.

- Exact-source CI `37879358744` and exact-evidence-head CI `37961014980`: both `completed/success`, all Windows job steps PASS.
- Operator Windows local build/tests **21/21 frontend and 61/61 Rust PASS**, Rust check locked and dependency locks unchanged; UI **8/8 PASS**, Ollama OFF.
- Controlled additive SQLite v4→v5 on actual restored-active DB only after verified non-overwriting v4 operator backup SHA256 `c624241080d6e820398cc502b4db206fcaba457405083ce806c302a6ce464976`.
- Read-only postmigration audit **PASS**: migrations 1–5, fact/source STRICT schema, required triggers and indexes, `foreign_key_check=[]` / `integrity_check=ok`; all historical table contents/digests and both historical backup custodial hashes preserved.
- Nine original entities and eight aliases, homonymous character distinct IDs, three immutable scene revisions and current pointer retained exactly. New fact/source tables empty as expected prior to API use.
- Delivered local Rust/Tauri structured fact create/read/list with explicit sourced/unsourced provenance, immutable Scene revision anchors, checked UTF-8 byte spans, same-Universe guards and atomic rollback; **no React fact-entry UI**, canon status/review, AI extraction or ComfyUI implementation.
- Detailed evidence: `docs/qualification/M2_3_IMPLEMENTATION_GATE.md`.

#### M2.4 — Canon status and human review service

**COMPLETE + MERGED + NORMALIZED — effective only after the independent M2.4 normalization PR completes its exact-HEAD CI and protected merge.**

Implementation PR #27 merged into `main` at `3a069572d00e1680c42b0f13b800e28687c5f0eb`; qualified source HEAD `aad56bd59fdb87be5ac1eda99b1969452bf61a26`, qualification evidence HEAD `b53405779b04c16525ba48a266bd096096af7020`. Exact source `Fabulaxiom CI` run `37974831473` and evidence-HEAD run `37989040863`: both terminal SUCCESS, 13/13 Windows steps. Source qualification: 21/21 React, 71/71 Rust; operator real Windows reviewed 8/8 isolated Rust tests plus 8/8 existing-UI non-regression checks, Ollama OFF.

Delivered SQLite **v6**, STRICT append-only `fact_review_events`, explicit seven-state review service via Rust/Tauri, `draft` default, deterministic status transitions, durable audit history, optimistic revision guards, cross-Universe FK, explicit approval and revocation confirmation. Human reviewer name is **self-declared, not authenticated**; no silent AI promotion.

Real restored-active Windows v5→v6 migration occurred **only after** separate non-overwriting consistent pre-v6 v5 backup SHA-256 `db02961d7a30c6a6522bd52faeab8ceb09e26c1a4a6a58be467d142806e22fee`, with older backups intact. Independent read-only postmigration audit of six migrations, STRICT/triggers/indexes, integrity and foreign keys, every previous table digest, nine entities/eight aliases, three scene revisions and one current head: PASS. Isolated Windows Rust review tests **8/8 PASS** with production v6 SQLite logical snapshot unchanged before/after (`67dfd9194ff884762bbffaa39d774df10fadcd74cbc9e6774e36d323e4506fc6`). No production facts or review events inserted.

**Not delivered:** a dedicated React fact/review UI, end-to-end fact-review IPC GUI acceptance, authenticated reviewer identity, AI fact extraction, or ComfyUI. Detailed evidence: `docs/qualification/M2_4_CANON_REVIEW_IMPLEMENTATION_GATE.md`. Existing PR and governance are not authorization to implement the next subdivision before this independent normalization merges.

#### M2.5 — Usable sourced-facts and human review UI

**COMPLETE + MERGED + NORMALIZED.** Implementation PR #29 and independent normalization PR #30 are both protected-merged; the latter passed exact-head `pull_request` CI #38041908126 (13/13 steps).

- Implementation PR **#29** protected-merged on `main` at `f1e7ea99d26ad3390c7c47bfb339f26d730a44f1` from **exact evidence HEAD** `6f55fc3fc7eab6f2288a54619c0bef70e521f47e`. `Fabulaxiom CI` run **38040227617**, event `pull_request`, `completed/success`, **13/13** Windows steps, frontend **32/32**, Rust **72/72**, frontend build, `cargo check --locked`, locks unchanged.
- Qualified implementation source `7eaaf45ae164c9336df7e01c9da6787e4971d59e`, exact-source CI **38017441504** `completed/success`. Windows operator qualified: 8/8 hierarchy fixture actions; 8/8 corrected cross-workspace refreshing (`Aucun univers` blocker fixed); 9/9 sourced/unsourced fact UI cases; 10/10 human-review interaction checklist with no Ollama.
- Read-only SQLite v6 source/provenance/human-review audit: **3 facts / 2 source anchors / 11 immutable review events**, 8+2+1 contiguous review histories, explicit canon approval and revocation, no fabricated source, Unicode citation byte spans `[0,10)` and `[51,66)`, persisted three statuses `draft`, `suggestion`, `unknown`. Corrected mistaken 10-event script expectation: do not delete an actual event.
- Isolated Tauri `com.fabulaxiom.m25qual35fb842c` production-separated v6 test database; operator existing records preserved. Production restored-active v6 snapshot SHA256 `67dfd9194ff884762bbffaa39d774df10fadcd74cbc9e6774e36d323e4506fc6` unchanged. Isolated final logical digest `cff8a04f29ec60757c02ef9ed186be40c806cfcc6a2cfd11fa8072be44f273cb`; isolated pre-fact backup SHA256 `9e738d58519e1a0e3c1750d71726b661132fcbc0211fddea3178f6314bbfc7cf` retained; historical pre-M2.1/v4/v5 backups all hash-verified. An earlier v4 SHA mismatch in a PowerShell script was refuted by independent hashing plus v4 manifest/SQLite integrity, not a corrupted backup.
- New isolated React fact workspace with independent error boundary, Universe/entity and revision synchronization, exact historical UTF-8 citations, optional fictional validity, distinct seven statuses and human-only approval/revocation with append-only review history. Human reviewer label remains **self-declared, not authenticated**. No automatic canon promotion, no cloud or Ollama requirement, no migration after v6.
- Detailed acceptance: `docs/qualification/M2_5_SOURCED_FACTS_REVIEW_UI.md`; independent normalization: `docs/qualification/M2_5_POST_MERGE_NORMALIZATION.md`.

### M2 milestone closure boundary

**M2.1–M2.5 and M2 milestone COMPLETE + MERGED + NORMALIZED** after protected PR #30 merge `f13b4f8c249866ff60a19d7895b6cfaede56398a`, exact normalization CI #38041908126 SUCCESS. This is NOT V1 completion and it does NOT authorize M3 implementation. Next: independently evaluate the proposed bounded M3 roadmap in `docs/roadmap/M3_TIME_KNOWLEDGE_RELATIONSHIPS.md` through a separate planning PR and a separate planning normalization gate. ComfyUI imagery remains an unimplemented proposal (issue #19).

### M3 — Time, knowledge and relationships: planning merged, normalization gate pending

Planning PR **#31** merged with `expected_head_sha=5127ced6c5e175b0919c736c658036382794487e` at `main=68db746754e01b441870e0653f17f10ebfc7be2f`. Its exact-head `pull_request` CI run **38050865413** completed/success (one Windows job, 13/13 steps). Six documentary files only; no M3 code, SQLite v7, dependency or lockfile modification. The accepted proposed divisions are **M3.1** world-time schema, **M3.2** manual chronology UX, **M3.3** directional relationship history, **M3.4** character beliefs/knowledge, **M3.5** narrator/reader reveals, **M3.6** evolving narrative state. Detailed roadmap: `docs/roadmap/M3_TIME_KNOWLEDGE_RELATIONSHIPS.md`.

**Normalization condition:** the plan is `ACCEPTED + MERGED + NORMALIZED` **only after** an independent post-planning normalization PR passes a new terminal exact-head CI and SHA-guarded merge, then `main` is re-fetched. At that point authorize **M3.1 only**, using its own PR and required pre-v7 SQLite backup/Windows qualification; do not authorize M3.2+, AI, ComfyUI or production migration simply from planning. Evidence: `docs/qualification/M3_PLANNING_POST_MERGE_NORMALIZATION.md`.

**GitHub enforcement distinction:** branch API currently reports `main.protected=false`; `expected_head_sha` prevents merging an unexpected PR head but does not create formal branch protection. No change to historical M2 backups, production M1.5 active database, test fixture SQLite v6 or preserved review history is involved in planning.

## Reproducibility contract

- `package-lock.json` committed;
- `src-tauri/Cargo.lock` committed;
- CI uses `npm ci`;
- Rust CI uses Cargo `--locked`;
- dependency-lock mutation is rejected in CI.

## Governance rule

Every subdivision must:

- begin from freshly fetched live `main`;
- use a dedicated branch and pull request;
- preserve deterministic dependency locks;
- pass exact-head CI;
- receive Windows operator qualification when local behavior is part of acceptance;
- be merged and normalized before a dependent subdivision begins.
