# M3.2 — Prévisualisation Tauri Windows fictive : variante compilable, lancement interdit à cette étape

**2026-10-17 — étude technique uniquement, sans démarrage d'une fenêtre sur les machines opérateur ni sur CI.**
Autorité initiale : `main=1607f5705f0ec4a18a37542cf3e04d1df89ec2d6` après fusion protégée PR #62 et CI #39054598253 (43/43, Chromium 29/29, React 129/129, Rust 100/100). La PR #35 demeure OPEN/DRAFT ; G3 original `STOP_UNAVAILABLE`.

## Raison : la simple identité distincte est insuffisante

L'application standard `lib.rs` enregistre `database_status`, `create_database_backup`, `restore_database_backup`, les commandes hiérarchie, faits, entités et autres mutations. Changer seulement l'identifiant Tauri ou le titre d'une fenêtre laisserait ces opérations native exposées. L'existant M3.1 `m31-isolated-preview` est, lui, associé à une connexion SQLite v7 d'inspection ; ce n'est pas l'objectif ici.

La nouvelle **feature Rust non-default** `m32-synthetic-preview` active un **troisième chemin de démarrage**, strictement différent du normal et de M3.1 : `tauri::Builder::default().run(context)`, sans aucun `invoke_handler`, plugin ni `State`, donc aucun IPC applicatif enregistré et aucune ouverture, migration, sauvegarde ou restauration SQLite. Elle est interdite en mode release via `compile_error!`, et incompatible avec le flavor M3.1. Une compilation ordinaire, sans feature, garde exactement le démarrage de production actuel.

## Identité et URL verrouillées

Overlay distinct `src-tauri/tauri.m32-synthetic-preview.conf.json` :
- Identifiant `com.fabulaxiom.m32synthetic.preview`, différent de `com.fabulaxiom.desktop` et de toutes les identités M3.1.
- Fenêtre unique `m32-fiction`, titre contenant `FICTIONAL`, `bundle.active=false`.
- `build.devUrl=http://127.0.0.1:1420/m32-browser-lab.html`, page Vite de test contenant uniquement des scénarios littéralement inventés. Aucun montage `App.tsx`.
- `app.security.capabilities=["default"]` : allowlist **explicite et non vide**. `capabilities/default.json` cible uniquement `windows=["main"]` et fournit `core:default` pour cette fenêtre normale. La variante fictive déclare seulement `m32-fiction` et ne correspond donc à aucune capability. Cette sélection empêche aussi le chargement automatique de futurs fichiers `capabilities/` que pourrait déclencher une liste vide.

La validation Rust intervient **avant la construction du runtime** : environnement explicite `FABULAXIOM_M32_PREVIEW_ID` correspondant exactement à l'identifiant et à la configuration effective, URL exacte et **une seule fenêtre** attendue. La validation pure refuse les identités de production/M3.1, chemins d'accueil, URL externes, autre port, fenêtres en surplus, options et configurations non conformes.

## Ce qui est / n'est pas qualifié

Ce lot qualifie uniquement l'architecture **source + compilation debug**. Tests Python source-only sur fichiers du dépôt, tests Rust `m32_synthetic_preview` d'admission, contrôle `cargo check --locked --features m32-synthetic-preview` et exécution des suites Windows existantes. L'overlay est inspecté en JSON ; **son utilisation par la CLI Tauri lors d'un lancement réel n'est pas encore éprouvée**. Une CI réussie ne signifie pas que le WebView2 Windows a été ouvert et validé.

**Aucun lancement utilisateur à cette étape.** Ne pas lancer `tauri dev`, `cargo run` ou installer un exécutable depuis cette PR. Une éventuelle procédure interactive devrait préalablement vérifier l'identité, l'absence de sessions Fabulaxiom de production, l'URL réellement chargée et les droits Windows, puis faire l'objet d'une autorisation distincte. **Ne jamais** utiliser l'environnement ou les fichiers v6/v7 pour ce laboratoire. La simple présence d'un prototype compilable n'autorise aucun changement de source ou migration.

**Portée de la preuve** : le flavor Rust n'enregistre aucun IPC applicatif. L'absence de commandes ne remplace pas une preuve générale d'absence de toutes les API Tauri de base, de capacités chargées, de messages IPC internes ou d'effets secondaires du runtime OS ; ces éléments doivent rester sujets de qualification lors d'une vraie prévisualisation. Les identités distinctes n'attestent pas la provenance des originaux, qui ne sont jamais ouverts ici.


## Audit complémentaire : la liste vide n'était PAS une isolation explicite

La documentation officielle Tauri v2 précise que `security.capabilities` **absent ou vide** entraîne par défaut la sélection des fichiers sous `src-tauri/capabilities/`. La version de la PR #63 passait `[]`, ce qui ne constituait donc pas une liste d'interdiction. Dans les sources examinées, l'unique capability `default.json` ciblait `main` exclusivement : aucune attribution directe à `m32-fiction` n'a été trouvée, mais cet état était dépendant d'une découverte automatique non désirée.

**Durcissement proposé dans une PR distincte** : remplacer `[]` par `["default"]` (sélection explicite du seul fichier existant, toujours réservé à `main`). Les tests `tools/test_m3_2_tauri_capability_boundary.py` modélisent l'override JSON `tauri.conf.json` + overlay, vérifient le seul fichier de capabilities et l'absence de `tauri.windows.conf.json`/overrides de plateforme dans la source actuelle. Ils rejettent les glob patterns, fenêtres supplémentaires, capabilities distantes, nouveaux fichiers et permissions inattendues. Ce modèle est **source-only**, pas la sortie réelle du parseur CLI Tauri, et n'exécute pas de WebView2.

**Restent expressément non qualifiés** : résolution par la CLI et par `generate_context!` au binaire exact ; variables d'environnement de lancement (`TAURI_DEV_HOST`, `FABULAXIOM_M32_PREVIEW_ID`, `TAURI_CONFIG` le cas échéant), lancement du serveur Vite (hérité : `npm run dev`), contenu chargé puis navigation WebView, processus/ports déjà occupés, CSP héritée `null`, permissions et interfaces du noyau Tauri indépendantes des commandes applicatives, version des outils et binaires réellement utilisés. Les assertions Python ne sont pas une preuve indépendante de l'implémentation du merge Tauri. Toute première ouverture Windows nécessite une pré-vérification, un plan d'arrêt/quarantaine sans original et une **autorisation opérateur explicite** avant de fournir ou d'exécuter toute commande démarrant Tauri/WebView2.

**Statuts obligatoires jusqu'à une qualification propre de la nouvelle PR** : SOURCE_ONLY `PENDING`, WINDOWS_CI `PENDING`, TAURI_RUNTIME `NOT_TESTED`, OPERATOR_ACCEPTANCE `NOT_PERFORMED`, G3 source `STOP_UNAVAILABLE`. Pas de promotion sur simple ajout de tests.

Documentation Tauri : https://v2.tauri.app/reference/config/ ; https://v2.tauri.app/security/capabilities/ ; https://v2.tauri.app/reference/cli/ .

### Sources officielles
- [Tauri v2 — Configuration et devUrl](https://v2.tauri.app/reference/config/)
- [Tauri v2 — Runtime Authority](https://v2.tauri.app/security/runtime-authority/)
- [Tauri v2 — CLI, --config et --features](https://v2.tauri.app/reference/cli/)
- [Tauri v2 — Capabilities](https://v2.tauri.app/security/capabilities/)
- [Tauri Utils Rust — BuildConfig.dev_url](https://docs.rs/tauri-utils/latest/tauri_utils/config/struct.BuildConfig.html)

**Gates inchangés** : historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, original G3 `STOP_UNAVAILABLE`, G3/G4/G5/G6 réels `NOT_AUTHORIZED`, PR #35 `OPEN/DRAFT`. Aucun original SQLite, sidecar, sauvegarde, manifeste, ACL, marqueur d'activation, migration 007, writer IPC, M3.3 ou release.
