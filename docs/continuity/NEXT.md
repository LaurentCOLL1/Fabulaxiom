# Fabulaxiom — Next Authorized Work

## 2026-10-19 — prochaine reprise depuis living handoff GitHub

Lire `docs/continuity/README.md` puis `HANDOFF_CURRENT.md`, `HANDOFF_CURRENT.json`, `HANDOFF_PROTOCOL.md` et `HANDOFF_HISTORY.md` ; re-fetch les SHA, PRs, CI/ruleset. Nouvelle priorité opérateur : revue du **bloc corrigé #86** (parenté SearchHost via CIM), approbation explicite du code exact, puis exécution manuelle G2-A uniquement si l'utilisateur le confirme. Ne pas réutiliser l'autorisation de l'ancien bloc #85 ni prétendre à une absence d'écrivain SQLite. Sur toute PR future M3.2, mettre à jour MD + JSON du handoff pour satisfaire le garde-fou CI.


## 2026-10-19 — qualifier la correction SearchHost de G2-A et soumettre à consentement neuf

Nouvelle CI `pull_request` au HEAD exact : 25 tests source-only du bloc PowerShell, 14 tests sur arbres de processus purement fictifs, parseur AST PowerShell sans exécuter le candidat, tous les contrôles existants et le marqueur `M32_SECURITY_PREFLIGHT_STOP`. Garder `Get-CimInstance` sous revue : WMI/CIM peut solliciter un service système, et le graphe PID + dates ne constitue pas une preuve d'identité cryptographique. Après CI et fusion protégée, soumettre le **nouveau code exact** au propriétaire pour accord distinct ; ne pas réutiliser l'autorisation de PR #85. Aucune ouverture de SQLite, migration 007, G3/G4/G5/G6 ni release.


## 2026-10-19 — PR #85 : AST syntaxe qualifiée, cardinalité dynamique diagnostique

La CI au HEAD `6dd7e28897d226c02e0d212b2784293ff28606a3` a passé 20 tests Python et la syntaxe PowerShell `Parser.ParseInput`, mais la cardinalité attendue pour les `CommandAst` dynamiques a déclenché un STOP du job avant les régressions. La nouvelle version garde l'inventaire de commandes connues et un seuil de refus conservateur (`>4`), avec un compteur informatif ; les contrôles Python sur le texte restent requis. La liste de refus de sortie mentionne explicitement G3/G4/G5/G6. Le bloc demeure un candidat **non exécuté**, G2-A non autorisé. Nouvelle CI exact-head indispensable ; ancienne preuve FAIL/SKIPPED non réutilisable.


## 2026-10-19 — PR #85 : correction du seul extracteur AST de Markdown

Au HEAD `b14fb8d1bcff1ca28387c65233c4c010268abe6a`, CI `pull_request` Windows a passé les 20 tests source-only du candidat, mais STOP à l'extraction `[regex]::Matches` des délimiteurs Markdown ; aucune exécution du bloc, suites aval ignorées. L'extracteur GitHub CI a été remplacé par comparaison **exacte des deux lignes de clôture**, découpage par IndexOf puis `Parser.ParseInput` (non exécuté). Aucun octet du bloc PowerShell proposé n'est changé. La qualification du nouveau HEAD est obligatoire : CI antérieure FAIL/SKIPPED non réutilisable.


## 2026-10-19 — PR #85 correction du workflow invalide, requalification HEAD neuf

La première version `16de4a37a8bb09d7208925859aa761014ba81352` a produit un workflow YAML invalide, détecté par GitHub avant création de job (run #39215639069 `failure`, `push`, zéro job). Cause : remplacement de texte Javascript interprétant `$'` dans l'expression régulière et insérant une copie du reste du workflow. Le workflow a été reconstruit **à partir du main vérifié**, avec insertion contrôlée par callback et préflight d'unicité des étapes. Aucun test ancien à recycler ; la **nouvelle CI pull_request au SHA nouveau** sera la seule preuve. Le bloc PowerShell G2-A reste INERTE/NON AUTORISÉ et n'est jamais exécuté.


## 2026-10-19 — qualifier syntaxe et refus du bloc G2-A pour revue humaine

Exiger 20 tests source-only de mutations sur le bloc Markdown et l'analyse AST Windows par `Parser.ParseInput` sans l'exécuter ; marqueur `M32_G2A_AST_PARSE_ONLY_PASS`. Requalifier les contrôles antérieurs, inspecter CI obligatoire SHA exact, diff/ruleset/reviews/threads et main anti-course avant fusion. Même après fusion, présenter code et avertissements à l'opérateur, puis demander autorisation **spécifique** avant toute commande Windows. G2-A=NOT_ASSESSED/NOT_AUTHORIZED, G2-B/C/D et G3–G6 inchangés.


## 2026-10-19 — qualifier le dossier G2-A de revue sans script

Exiger les 24 nouveaux tests `test_m32_g2a_consent_contract.py` : absence de commandes et chemins privés, absence d'accord/planification, zéro ouverture SQLite, élévation/arrêt/ACL/sidecar/Git local interdits, `G2A_RUNTIME=NOT_ASSESSED`. Garder les 20 tests du registre d'autorité précédent, tous les tests Rust et Chromium, `M32_SECURITY_PREFLIGHT_STOP`. Une CI terminale au HEAD nouveau + analyse de diff, reviews, ruleset, re-fetch avant toute fusion. Après fusion, **G2-A n'est pas effectué** : présenter séparément à l'opérateur un bloc examiné et obtenir accord explicite avant exécution. Maintenir G2-B/G2-C/G2-D/G3–G6 `NOT_AUTHORIZED`.


## 2026-10-19 — prochaine qualification : registre M3.2 de refus et préparation G2 documentaire

Qualifier au SHA exact le JSON [M3_2_GATE_SNAPSHOT.json](M3_2_GATE_SNAPSHOT.json), sa documentation et les 20 tests Python adversariaux dans la CI Windows obligatoire, puis vérifier toutes les régressions et `M32_SECURITY_PREFLIGHT_STOP`. Le registre est daté et requiert un re-fetch GitHub pour toute nouvelle PR/fusion ; il ne qualifie pas lui-même les sources ou attestations de l'opérateur. Après une fusion protégée, seules la recherche de preuves historiques indépendantes (#36) et la préparation d'un runbook G2 soumis à **autorisation spécifique** (#38) sont envisageables ; G2–G6, Tauri/WebView2 réel et G3 opérateur demeurent bloqués. Ne pas ouvrir les SQLite originales, ni déclencher migration 007, IPC writer, PR #35 ou release.


## 2026-10-19 — PR #82 : nouvelle qualification HEAD exact obligatoire

Ne pas réutiliser la CI initiale FAIL/SKIPPED. Exiger 13 tests source-only de la preview, quatre tests Rust `native_generated_core_` dans un fichier distinct compilé sous `#[cfg(test)]`, les marqueurs `M32_NATIVE_GENERATED_CORE_SOURCE_BINDING_PASS` et `M32_NATIVE_GENERATED_CORE_LAB_DENIAL_PASS`, puis toutes les régressions antérieures. Re-vérifier logs, contrôle GitHub Actions app 15368, ruleset #24895490, reviews/threads, diff, re-fetch anti-course avant fusion `expected_head_sha`. Aucun Tauri/WebView2 opérateur ni SQLite originale.


## 2026-10-19 — qualifier les véritables manifests Core générés par Tauri (CI sans runtime)

Exiger la CI Windows `pull_request` au HEAD exact de la nouvelle PR : quatre tests Rust `native_generated_core_` lisant uniquement les artefacts `gen/schemas` produits par `tauri-build` sur le runner, marqueurs `M32_NATIVE_GENERATED_CORE_SOURCE_BINDING_PASS` et `M32_NATIVE_GENERATED_CORE_LAB_DENIAL_PASS`, commande témoin `plugin:app|version` autorisée pour `main` et toutes les commandes Core refusées sur `m32-fiction`. Vérifier le mutant wildcard en mémoire et l'erreur sur permission inconnue. Conserver tests natifs précédents, les tests Python ACL, 29/29 Chromium ×2, 129 frontend, 100 Rust, tests HTTP et G3 fictifs, et `M32_SECURITY_PREFLIGHT_STOP`. Revoir logs/CI app 15368, ruleset #24895490, PR diff, reviews/threads, re-fetch anti-course avant fusion `expected_head_sha`. Ne pas présenter les artefacts générés comme une preuve d'autorité Tauri **runtime**. Aucun lancement, ni accès aux données opérateur.


## 2026-10-19 — qualifier le résolveur ACL natif sur manifest fictif

Attendre la CI Windows `pull_request` terminale et SUCCESS **au nouveau SHA exact**. Exiger quatre tests `native_resolve_` (source `default.json` relue sans altérer `core:default`, permission fictive `m32fixture`, vérifications source main/lab, wildcard et union, deny inter-fenêtres, manifest/permission absents), ainsi que `M32_NATIVE_ACL_MANIFEST_RESOLVE_TOY_PASS`. Confirmer tous les tests antérieurs : 12 Python permissions source-only, 4 Rust `native_acl_`, 29/29 Chromium x2, tests HTTP/IPC, 129 frontend, 100 Rust généraux, contextes générés compile-only, G3 et G4 fictifs, STOP Tauri. Revoir diff, logs, reviews/threads, ruleset #24895490/app Actions 15368 et `main` par re-fetch avant fusion `expected_head_sha`. Cela teste **le moteur natif sur un manifest inventé**, pas l'ACL Core réelle du contexte Tauri. Ne pas lancer Tauri/WebView2 ou accéder aux fichiers SQLite opérateur.


## 2026-10-19 — qualifier les tests Rust du matcher ACL natif fictif

Au HEAD exact de la nouvelle PR, exiger la CI Windows obligatoire `Windows frontend and Rust checks` terminale SUCCESS : quatre tests `native_acl_` Rust sur une commande totalement inventée, marqueur `M32_NATIVE_ACL_TOY_MAIN_WINDOW_VETO_PASS`, source de `capabilities/default.json`, contre-exemples wildcard et webview, commande inconnue refusée. Conserver 12 tests source-only PR #79, 29/29 Chromium ×2, 129 frontend, 100 Rust généraux, les contextes `generate_context!` sans lancement, tests Node IPC/HTTP et G3 jouets. Contrôler logs, HEAD, reviews/threads, ruleset #24895490/app 15368, diff et anti-course sur main, puis fusion protégée `expected_head_sha` seulement si tout est vert. Le succès valide seulement un matcher Rust sur ACL inventée, **pas** l'ACL réelle du contexte Tauri et ne débloque pas G3 ni Windows opérateur.


## 2026-10-19 — qualifier matrice Tauri capabilities/Core source-only

Exiger une nouvelle CI Windows `pull_request` terminale au HEAD exact : 12 tests Python adversariaux pour prouver *uniquement dans les sources* que `core:default` n'est sélectionné que pour `main` et ne correspond pas à `m32-fiction` dans les deux overlays. Refuser un wildcard, `webviews`, `remote`, nouvelle capability, permissions natives additionnelles, `AppManifest`, handler/plugin d'application. Maintenir les tests Chromium 29/29 ×2, 7/7 IPC enfant, 10 tests Host/Origin, 129 frontend, 100 Rust, codegen Tauri et toutes fixtures G3. Examiner logs, SHA exact, reviews, threads, ruleset #24895490 et re-fetch anti-course avant fusion `expected_head_sha`. **Ne pas convertir ce modèle en qualification du resolver Tauri réel.** Les STOP opérateur/G3 sont inchangés.


## 2026-10-19 — qualifier association IPC parent/enfant et port fictif occupé

Exiger CI Windows `pull_request` terminale au HEAD final de la branche de contrôle : 7 tests source/port fictif (y compris EADDRINUSE), marqueur `M32_CI_OWNED_STATIC_CHILD_READY_PASS` émis seulement après IPC reçu du child qui a ouvert le serveur sur 127.0.0.1:14279. Garder les 10 tests bruts Host/Origin, 7 requêtes réelles négatives, les 29/29 ×2 scénarios Chromium, 129 tests frontend, 100 Rust, codegen Tauri fictif compile-only et les essais G3 synthétiques. Inspecter logs, checks GitHub Actions app 15368, revue/diff, ruleset, commentaires/threads et main anti-course avant une fusion protégée `expected_head_sha`. Aucune validation native Windows/Tauri, aucune permission d'ouvrir G3 réel ou une base. `M32_SECURITY_PREFLIGHT_STOP` demeure.


## 2026-10-18 — qualification à faire : en-têtes HTTP bruts/dupliqués fictifs

Attendre le Windows `pull_request` au HEAD exact de la nouvelle tranche : 10 tests Node d'autorité, ancien marqueur quatre refus HTTP, nouveau `M32_CI_HTTP_RAW_DUPLICATE_DENIAL_PASS` pour trois requêtes TCP brutes réelles, deux laboratoires Chromium 29/29, ensemble des tests Git/RAM/Tauri/fixtures G3, `M32_SECURITY_PREFLIGHT_STOP` préservé. Lire les logs, vérifier ruleset, checks de l'intégration 15368, reviews/threads, diff et re-fetch anti-course de main avant fusion avec `expected_head_sha`. Aucun lancement Tauri/WebView2 ni opérations opérateur. Une fusion ne vaut pas permission de lancement ni G3 réel.


## 2026-10-18 — qualifier les refus Host/Origin sur le laboratoire fictif CI

Exiger nouvelle CI `pull_request` Windows terminale sur HEAD exact : six tests Node `test_m32_ci_http_authority.cjs`, marqueur `M32_CI_HTTP_AUTHORITY_DENIAL_PASS` issu de quatre requêtes réelles, 10 tests de liaison Git, 8 tests snapshot RAM, deux séries Chromium 29/29, 129 frontend, 100 Rust, deux contextes Tauri compile-only et tous les tests G3 fictifs. Vérifier dans les logs le maintien de `M32_SECURITY_PREFLIGHT_STOP`. Revalider la protection de `main`, les reviews et threads, la comparaison du diff et l'absence de nouvelle commit avant `expected_head_sha`. Ne jamais convertir le succès du test serveur CI en autorisation de lancement réel Windows. `TAURI_RUNTIME_NOT_TESTED`, `OPERATOR_ACCEPTANCE_NOT_PERFORMED`, G3 réel STOP, historique 21/3/2 non attesté, prospective NOT_STARTED, PR #35 DRAFT et issues #36/#38 OPEN ; aucun accès opérateur, migration 007, M3.3 ou release.

## 2026-10-18 — qualifier la liaison Git des sources imaginaires du runner

Exiger une CI Windows `pull_request` terminale **sur le nouveau HEAD exact** avec 10 cas Node, dont la conversion LF→CRLF autorisée sur Windows et le refus des autres altérations sur des dépôts Git **fictifs** (HEAD attendu, altération du worktree, disparition, ajout/duplication au manifest, changement de commit, immuabilité des buffers). Le staging Chromium doit afficher `M32_CI_GIT_SOURCE_BINDING_PASS` deux fois (Vite dev et bundle statique), et continuer à réussir `M32_CI_FIXTURE_STAGE_EXACT_PASS`, 29/29 Chromium ×2, 129 frontend, 100 Rust, deux contextes natifs compilés, tests G3 fictifs, `M32_SECURITY_PREFLIGHT_STOP` inchangé. Examiner logs, risques de confidentialité, diff, SHA du contrôle GitHub Actions app 15368, ruleset, reviews et discussions ; vérifier `main` anti-course puis fusion protégée avec `expected_head_sha` uniquement si tout a réellement réussi.

Même qualifiée, cette liaison *ne prouve que la cohérence avec le commit effectivement extrait* : elle ne vérifie aucune signature indépendante ni identité opérateur. Ne pas traiter le SHA seul, un nom de chemin ou des fixtures comme une attestation historique 21/3/2. Ne pas activer le candidat Tauri 14279 ni toucher au lanceur M3.2 1420. Toute ouverture réelle Tauri/WebView2 réclame une **autorisation utilisateur préalable et explicite**. `TAURI_RUNTIME_NOT_TESTED`, `OPERATOR_ACCEPTANCE_NOT_PERFORMED`, G3 réel STOP, PR #35 DRAFT, issues #36/#38 OPEN ; pas de base réelle, migration 007, M3.3 ou release.

## 2026-10-18 — qualifier instantané RAM des assets inventés avant toute future passerelle native

Sur la PR dédiée au durcissement du serveur CI : exiger au HEAD exact et avec CI Windows `pull_request` terminal `SUCCESS` les **huit tests Node** du snapshot local, le marqueur `M32_CI_STATIC_BYTES_PINNED_PASS` lors du serveur, `M32_CI_STATIC_HTTP_DIGEST_PASS` lors du test HTTP des ressources fictives, les deux séries Chromium 29/29, frontend 129/129, Rust 100/100, les deux tests Tauri compile-only, les tests source/adversariaux et toutes les fixtures G3. Un script doit démontrer que les octets renvoyés sont les mêmes après modification de fichiers **de test créés par le runner** ; il ne doit jamais accéder au PC de l'opérateur. Vérifier logs, aucun secret privé, diff, ruleset `main`, reviews, threads, statut GitHub Actions de l'app 15368 et re-fetch anti-course avant éventuelle fusion `expected_head_sha`.

Même si tout réussit, les SHA256 calculés depuis le bundle de CI ne sont **pas** une attestation indépendante de provenance, et l'isolation du navigateur Chromium ne constitue pas une qualification native Tauri/WebView2. Préparer ultérieurement une voie d'identité de source opérateur distincte sans contourner les autorisations ; la cible Tauri candidate 14279 reste inactivée, le lanceur actif 1420 inchangé. Exiger un **accord utilisateur explicite préalable** avant toute commande lançant une application ou fenêtre Tauri/WebView2. `M32_SECURITY_PREFLIGHT_STOP`, réel G3 STOP, historique 21/3/2 `PENDING_EXTERNAL_ATTESTATION`, prospective NOT_STARTED, PR #35 DRAFT, issues #36/#38 OPEN, G3–G6 réels non autorisés, pas 007, writer, M3.3 ou release.

## 2026-10-18 — qualification d'un candidat `devCsp` Tauri INACTIF

Obtenir un `pull_request` Windows terminal `SUCCESS` sur le HEAD final de la branche candidate : suite adversariale `test_m3_2_static_tauri_candidate.py`, présence d'une CSP exactement égale aux directives du serveur statique déjà qualifié, refus `unsafe-inline`/`unsafe-eval`/IPC/origines distantes et des identités, ports, hooks, windows et capabilities non autorisés. Sur le même runner, faire passer les deux anciens laboratoires Chromium (29 + 29), les 129 tests frontend, 100 Rust, tous les garde-fous G3 fictifs et **deux tests Rust compile-only sous `TAURI_CONFIG`** : overlay M3.2 actif inchangé, puis candidat source-only strict, sans appeler `Builder::run`. Marqueurs visés : `M32_NATIVE_OVERLAY_CONTEXT_PASS` et `M32_STATIC_CANDIDATE_CODEGEN_PASS`, `M32_SECURITY_PREFLIGHT_STOP` maintenu.

Examiner journaux, diff, secrets, ruleset, checks GitHub Actions intégration 15368, reviews/threads, provenance des fichiers et anti-course sur `main`; fusion protégée sous `expected_head_sha` uniquement en cas de réussite à ce HEAD. **Ne pas transférer le candidat dans `src-tauri/`, modifier l'URL autorisée dans Rust, ou lancer Tauri/WebView2.** La compilation de `devCsp` ne prouve pas l'exécution Windows, la navigation ou les ACL natives. Un futur passage du candidat à une variante exécutable requerra une nouvelle tranche source-only, un preflight opérateur `PASS/FAIL/STOP`, et **l'autorisation explicite préalable** pour tout lancement Windows.

G3 réel STOP ; historique 21/3/2 `PENDING_EXTERNAL_ATTESTATION` ; prospective `NOT_STARTED`, G3–G6 réels `NOT_AUTHORIZED`, PR #35 OPEN/DRAFT, issues #36/#38 OPEN, aucune base/sauvegarde/migration/sidecar/ACL originale, aucun M3.3/release.

## 2026-10-18 — qualifier le bundle statique fictif sans `unsafe-inline` (GitHub CI uniquement)

Au nouveau HEAD, exiger `pull_request` Windows terminal `SUCCESS` avec les deux modes de tests Chromium : ancien Vite/HMR inventé **29/29**, nouveau build Vite fiction-only **29/29** sur serveur de fichiers statiques à routes allowlist (sans les fichiers normaux). Inspecter `M32_CI_PRECOMPILED_FICTION_ONLY_BUILD_PASS`, `M32_CI_PRECOMPILED_NO_INLINE_CSP_HEADER_PASS`, `M32_CI_PRECOMPILED_INLINE_SCRIPT_DENIED_PASS`, `M32_CI_PRECOMPILED_STRICT_CSP_BROWSER_PASS: 29/29`, négatifs HTTP, en plus de 129 tests frontend, 100 Rust, Tauri compilé et garde-fous G3 fictifs. Lire les journaux et vérifier que le contrôle préexistant `M32_SECURITY_PREFLIGHT_STOP` demeure. Relire le diff, le ruleset et les reviews, re-fetch `main` avant fusion `expected_head_sha` seulement si toutes les preuves sont terminales au SHA exact.

**Définition de preuve** : réussite signifie que Chromium applique un CSP HTTP strict à un bundle imaginaire précompilé, dans un runner jetable, **pas** que Tauri/WebView2 pourrait le charger. La `devCsp` Tauri reste `null`, `devUrl` M3.2 demeure à 127.0.0.1:1420 non lancé, le serveur normal et `TAURI_DEV_HOST` restent à risque. Tranche ultérieure à concevoir dans une autre PR : interface de distribution fictive strictement séparée, CSP native Tauri inspectable et vérification d'URL/ports, sans lancer Windows ou ouvrir une base. Accord opérateur préalable **obligatoire** avant toute commande démarrant Tauri/WebView2. `CLI_CONFIG_RESOLUTION_NOT_TESTED`, `TAURI_RUNTIME_NOT_TESTED`, G3 original STOP, historique 21/3/2, prospective NOT_STARTED, PR #35 DRAFT, G3-G6 réels non autorisés, pas migration 007, writer, M3.3 ou release.

## 2026-10-18 — CI browser CSP expérimentale (pas de promotion d'autorité)

Qualifier la PR indépendante au HEAD exact avec un `pull_request` Windows terminal : serveur Vite jetable basé sur les sept fichiers fictifs, CSP HTTP présente et en-têtes vérifiés, HMR ciblant `127.0.0.1:14279`, Chromium montrant **29/29 cas normaux** et une connexion externe refusée par `securitypolicyviolation` effective. Tous les checks de l'historique Rust/frontend/G3 doivent réussir, avec le contrôle obligatoire de l'app GitHub Actions 15368. Revoir diff, règles de `main`, reviews, threads et anti-course ; fusionner uniquement sous `expected_head_sha`.

Même avec un succès : **`M32_SECURITY_PREFLIGHT_STOP` inchangé.** La CSP isolée autorise `script-src 'unsafe-inline'` pour le preamble React/Vite en développement : elle ne constitue pas une politique satisfaisante pour Tauri/WebView2 ni une preuve XSS complète. Prochaine tranche séparée : préconiser puis qualifier un `devCsp` Tauri réellement applicable, une stratégie d'injection nonce/hash pour supprimer `unsafe-inline`, un lancement limité au bon serveur fictif avec isolation URL/ports, mais **aucune commande Tauri/Windows sans autorisation expresse**. Garder la CLI `--config`, les permissions noyau et la réception opérateur `NOT_TESTED`. G3 original STOP, historique 21/3/2, prospective NOT_STARTED, PR #35 DRAFT ; aucune migration 007 ni M3.3/release.

## 2026-10-18 — qualifier une racine de navigateur fictif CI réellement distincte

Exiger `pull_request` Windows terminal sur HEAD exact de la PR de staging fictif : sept fichiers explicitement copiés, analyse et refus des imports supplémentaires, aucune entrée React normale, Vite propre `host=127.0.0.1`, port strict et `fs.allow` restreint, tests HTTP négatifs sur `/`, `index.html`, `App.tsx`, `main.tsx` et `/@fs/`, puis **29/29 vrais scénarios Chromium** toujours verts. Inspecter précisément les journaux `M32_CI_FIXTURE_STAGE_EXACT_PASS`, `M32_CI_VITE_NORMAL_ROUTES_DENIED_PASS` et `M32_CI_FIXTURE_ONLY_BROWSER_PASS`, suites frontend/Rust/G3, reviews, threads, ruleset, comparaison diff et HEAD anti-course avant fusion protégée. Aucun Tauri/WebView2 opérateur.

Après qualification, mener **une PR distincte** pour CSP `devCsp`/en-têtes, l'URL exacte et HMR sans affaiblir `M32_SECURITY_PREFLIGHT_STOP`. La racine de CI n'est pas une configuration d'utilisation opérateur. `CLI_CONFIG_RESOLUTION_NOT_TESTED`, `TAURI_RUNTIME_NOT_TESTED`, `OPERATOR_ACCEPTANCE_NOT_PERFORMED`, G3 source `STOP_UNAVAILABLE`, PR #35 DRAFT, historique 21/3/2 en attente et prospective NOT_STARTED, G3–G6 réels non autorisés. Ne pas créer de migration 007, writer, M3.3 ou release.

## 2026-10-18 — qualifier la détection non lançante des refus Vite/CSP

Qualifier au HEAD exact la nouvelle PR source-only : Vite 8 `resolveConfig` sur config existante, sans `createServer`, sans `listen`, sans commande Tauri. Exiger preuve et log de trois cas : `TAURI_DEV_HOST` absent, IPv4 `127.0.0.1`, wildcard `0.0.0.0`. Refuser toute équivalence abusive entre `host=false` (résolution `localhost` potentiellement variable) et écoute assurée `127.0.0.1`. Les valeurs externes et HMR inadéquat doivent être veto en tests adversariaux. Confirmer CSP development réellement non configurée et cohabitation des entrées normales/fictives à la racine Vite : statut `M32_SECURITY_PREFLIGHT_STOP` attendu, même si l'audit source PASS. Vérifier toutes les CI Windows, GitHub ruleset, traces, diff, reviews/threads, HEAD exact et anti-course avant fusion éventuelle.

Après preuve, tranche future séparée uniquement : concevoir un serveur de fixtures réellement isolé et un CSP/HMR adapté, sans navigation vers l'application normale, avec tests statiques et navigateur jetables. Ne pas activer par défaut ni lancer un Tauri/WebView2 opérateur sans autorisation explicite et un préflight `PASS/FAIL/STOP`. `CLI_CONFIG_RESOLUTION_NOT_TESTED`, `TAURI_RUNTIME_NOT_TESTED`, `OPERATOR_ACCEPTANCE_NOT_PERFORMED`, G3 source `STOP_UNAVAILABLE`, PR #35 DRAFT, historique 21/3/2 en attente, prospective NOT_STARTED, G3–G6 réels non autorisés. Aucune base, migration 007, writer, M3.3 ou release.

## 2026-10-18 — après PR #67 : CSP, URL et CLI ; aucun lancement autorisé

État vérifié : `main=1735fc0edf0e457f7b41a06a99a6aa19fd22591f` après PR #67 protégée fusionnée ; CI Windows #39091761744 48/48 SUCCESS, `M32_NATIVE_OVERLAY_CONTEXT_PASS` compile-only. Les trois héritages frontend normaux `beforeDevCommand`, `beforeBuildCommand`, `frontendDist` sont écartés pour la variante fictive au moyen des marqueurs `null` RFC 7396. Deux CI échouées de mise au point #39091221081/#39091333950 sont inéligibles comme preuves. **Ne pas modifier ce checkpoint sans nouvelle CI au nouveau HEAD.**

Poursuite M3.2 autorisée **uniquement en conception/source/fixtures** : analyser CSP dev `null`, `TAURI_DEV_HOST`, URL/port/redirect et l'autorité native Tauri, tout en distinguant merge interne `generate_context!` du véritable traitement `--config` par la CLI 2.12.1. Aucune commande CLI inspect documentée ne fournit une exportation complète de ce merge sans effets de `dev`/`build`; conserver `CLI_CONFIG_RESOLUTION_NOT_TESTED` tant qu'une méthode sûre et testée n'existe pas. Une prévisualisation Windows demandera un préflight `PASS/FAIL/STOP` et **autorisation expresse, indépendante et préalable** avant de fournir un quelconque bloc démarrant serveur ou Tauri/WebView2.

`TAURI_RUNTIME_NOT_TESTED`, `OPERATOR_ACCEPTANCE_NOT_PERFORMED`, G3 original `STOP_UNAVAILABLE`, historique 21/3/2, prospective NOT_STARTED, PR #35 DRAFT, issues #36/#38 OPEN, G3–G6 réels NOT_AUTHORIZED. Pas d'ouverture d'original, copie, ACL, marqueur, backup, 007, writer IPC, M3.3, M4 ou release.

## 2026-10-18 — qualifier l'overlay fictif sans commandes frontend héritées

Sur la branche indépendante, obtenir le terminal `pull_request` Windows au HEAD exact : modèles RFC 7396 (`null` supprime les clés, tableaux remplacés, aucune mutation d'entrée), refus des trois valeurs normalement héritées `beforeDevCommand`, `beforeBuildCommand`, `frontendDist`, contrôle de l'overlay **brut** transmis via `TAURI_CONFIG` et de ses trois marqueurs `null`, puis `generate_context!(test=true)` confirmant `frontend_dist=None` après merge interne Tauri (ancien JSON déjà fusionné refusé) (les hooks y sont systématiquement effacés par Tauri), et maintien de la seule fenêtre `m32-fiction` sans capability appliquée. Vérifier CI Rust, Chromium fictif, frontend, scripts G3, revue diff, ruleset, reviews, threads, locks et anti-course main avant éventuelle fusion `expected_head_sha`. Un changement de HEAD annule toute CI précédente. Aucune action Windows opérateur.

Après ce correctif, poursuivre **uniquement** l'audit de conception non lançant du traitement CLI `--config`, CSP, variable `TAURI_DEV_HOST` et des droits noyau. Sans interface officielle d'export de config résolue, conserver `CLI_CONFIG_RESOLUTION_NOT_TESTED` ; ne pas la remplacer par `tauri dev`/`build`. Tout lancement futur nécessite une autorisation interactive distincte. PR #35 OPEN/DRAFT, issues #36/#38 OPEN, historique 21/3/2 et prospective NOT_STARTED, G3 réel STOP, aucune migration 007, writer, M3.3 ou release.

## 2026-10-18 — prochaine tranche autorisable : preuve CLI sans lancement, puis décision opérateur distincte

Après PR #65 protégée fusionnée au `main=1f61eaff968b33038a3513d8b5d5dbc82f3de8a1` (CI exacte #39074890614 48/48 SUCCESS), le test `generate_context!` avec `TAURI_CONFIG` *déjà fusionné par modèle Python* est qualifié, mais **le merge CLI réel `--config` reste NON testé**. La prochaine tranche GitHub doit cibler seulement une preuve native, non-lançante et jetable du traitement de la configuration par la version **verrouillée** `@tauri-apps/cli 2.12.1` / `tauri-utils 2.10.1`, ou documenter un `STOP` si aucune interface de résolution inspectable ne peut être appelée sans démarrer Tauri. Ne pas utiliser `tauri dev`, `cargo run`, installation ou un démarrage caché comme raccourci. Préserver une liste d'entrée exacte (base, overlay, configurations plateforme, capabilities), les variables d'environnement, le `frontendDist` et `beforeDevCommand` hérités, le CSP `null`, l'URL fictive loopback et les permissions du noyau; distinguer la configuration parsée de l'ACL réellement appliquée.

Avant une première prévisualisation interactive Windows, obtenir **une autorisation explicite et distincte** de l'opérateur après présentation du préflight `PASS/FAIL/STOP` et de l'arrêt contrôlé. Aucune commande de lancement ne doit être fournie avant cette approbation. `TAURI_RUNTIME_NOT_TESTED`, `OPERATOR_ACCEPTANCE_NOT_PERFORMED`, original G3 `STOP_UNAVAILABLE`, historique 21/3/2 et prospective NOT_STARTED, G3–G6 réels `NOT_AUTHORIZED`, PR #35 DRAFT, issues #36/#38 OPEN. Aucun original/migration 007/ACL/backup/activation/writer, M3.3 ou release.

## 2026-10-18 — qualifier le contexte généré par Tauri sans runtime

Sur la PR indépendante `m32_tauri_codegen_ci`, exiger CI Windows `pull_request` complète au HEAD exact avec nouveaux tests Rust `generate_context!(test=true)` ciblés sous `TAURI_CONFIG` *fictif seulement* ; le pilote refuse l'exécution hors Windows CI et ne fait que `cargo test --lib`. Vérifier que l'overlay explicite sélectionne `["default"]` et que `default.json` ne vise que `main`, sans `tauri dev/build`, `cargo run`, `Builder::run` ou fichier opérateur. Lire les logs de tests réels, diff, ruleset et reviews, rerécupérer main ; fusionner uniquement si exact HEAD et succès terminal.

Ne pas confondre ce contrôle du contexte généré avec la **fusion des configurations par la CLI** : celle-ci n'est pas prouvée par le modèle JSON Python. Préparer ultérieurement un audit CLI sans lancement avant toute autorisation de Tauri Windows. `TAURI_RUNTIME_NOT_TESTED` et acceptation opérateur non réalisée, historique 21/3/2, prospective NOT_STARTED, G3 STOP, PR #35 DRAFT, pas de migration 007, writer, M3.3, release.

## 2026-10-17 — prochaine qualification : frontière des capabilities de la prévisualisation fictive

Sur la branche indépendante de la PR de durcissement, qualifier au **HEAD exact** : allowlist Tauri non vide `["default"]`, capability `default.json` exclusivement associée à `main`, unique fenêtre `m32-fiction`, absence de surcharge plateforme implicite et tests adversariaux `tools/test_m3_2_tauri_capability_boundary.py` sous Windows CI ; conserver les 12 tests précédents, Rust debug feature, frontend, Chromium et tous les contrôles G3. Lire le compte rendu, vérifier la règle protégée `Windows frontend and Rust checks` / GitHub Actions 15368, re-fetch main et relire diff/reviews avant une éventuelle fusion `expected_head_sha`. Toute mutation du HEAD impose une nouvelle CI.

**Étape ultérieure distincte, non autorisée maintenant** : prévoir une résolution réelle de la configuration par la CLI, vérifier `TAURI_DEV_HOST`, URL, commandes noyau et navigation WebView2, puis présenter une procédure Windows `PASS/FAIL/STOP`, à approuver explicitement avant toute commande lançant Tauri. Ne pas conclure `TAURI_RUNTIME_PASS` à partir de `cargo check` ou d'un modèle Python de merge. L'acceptation opérateur et G3 réels restent bloqués, PR #35 DRAFT, historique 21/3/2 et prospective NOT_STARTED, aucun original/migration/écriture/release.

## 2026-10-17 — Qualification source et compilation d'un Tauri fictif sans données réelles

Qualifier la PR `m32-synthetic-preview` au HEAD exact : 12 tests Python source-only, 5 Rust pour identifiant exact, URL de fixture et fenêtre unique, `cargo check --locked --features m32-synthetic-preview` Windows/debug, tout `npm`/Chromium/Rust/G3 préexistant. Vérifier que le chemin normal est non compilé avec cette feature, zéro commande applicative enregistrée, feature exclue de release, overlay distinct et sans capability, `App.tsx` intact, locks immuables. Re-vérifier main/PR/CI avant fusion. La CI ne lance **pas** Tauri/WebView2 : pas de prétention d'acceptation Windows, de provenance G3 ni de permission d'opérer. Toute procédure interactive future nécessite préflight et autorisation explicite. PR #35 reste DRAFT, source réelle G3 `STOP_UNAVAILABLE`, 21/3/2 en attente ; aucune migration, marker, backup ou release.


## 2026-10-17 — Qualifier la lisibilité/accessibilité de l'explorateur fictif

Vérifier la nouvelle PR au HEAD exact : suite Vitest ciblée **28/28**, Chromium réel **29/29** avec rôles de recherche/statuts, aria-pressed, focus visible, cible >=44 px et largeur de 375 px ; suite frontend complète, build TypeScript, Rust et tous garde-fous G3, diff, locks inchangés, règles de branche et SHA anti-course. La CSS n'est importée que depuis `src/m32BrowserLab.tsx` et **pas** depuis `App.tsx`. Ces tests ne valent pas réception Windows/Tauri ou audit WCAG exhaustif. Si l'une des assertions échoue, corriger sur branche, changer le HEAD et requalifier entièrement. PR #35 demeure brouillon, G3 `STOP_UNAVAILABLE`, historique 21/3/2 externe non résolu, pas d'original ouvert, 007, writer, M3.3 ou release.


## 2026-10-17 — Qualifier l'explorateur fictif M3.2 filtrable

Contrôler le HEAD exact de la PR indépendante d'exploration : 22 tests `m32SyntheticEventExplorer`, 23 vrais scénarios Chromium `M32_BROWSER_REAL_CHROMIUM_PASS`, TypeScript/Vite, toutes les suites Rust/Python antérieures, diff et strict statut GitHub avant fusion. Le filtrage ne masque jamais un graphe invalide, les historiques ne deviennent pas sélectionnables, la pagination n'invente aucun événement ni ordre. Les composants restent absents de `App.tsx` ; la base opérateur et le runtime Tauri sont exclus. PR #35 brouillon, source G3 `STOP_UNAVAILABLE`, 21/3/2 externes en attente, pas de G3 réel, migration 007, activation, writer, M3.3 ni release.


## 2026-10-17 — Qualifier l'interaction réelle du laboratoire navigateur M3.2

Vérifier la PR Chromium synthétique au HEAD exact : 14 cas `M32_BROWSER_REAL_CHROMIUM_PASS`, accès HTTP strictement boucle locale, reset d'Univers, clavier, sélecteurs, preuves, refus de cycles ; conserver `npm ci`, tests React/Vitest, build Vite et contrôles Rust/Python. Vérifier aucune importation dans `App.tsx`, aucune dépendance lock ou données opérateur. Nouveau navigateur uniquement sur runner Windows jetable. Fusion protégée seulement après CI `pull_request` terminée SUCCESS, diff, règles de branche et SHA anti-course. **Ne pas confondre ces tests avec l'acceptation du bureau Tauri sur une vraie v7** ; G3 `STOP_UNAVAILABLE`, historique en attente (21/3/2), prospective `NOT_STARTED`, PR #35 DRAFT et aucun G3 réel, 007, marqueur, writer ou release.


## 2026-10-17 — Qualification du parcours React M3.2 fictif

Qualifier sur le HEAD exact le nouveau flux `M32ChronologyConsultation` : `24` tests ciblés (deux sélections HTML natives, cohérence d'Univers, transition sans défaut implicite, preuves de précédence, refus global des cycles), `npm run test:ci`, `npm run build`, anciennes suites Rust/Python et garde G3, diff, protections de `main`. La sélection reste **uniquement en mémoire fictive**, non montée dans `App.tsx` et sans données utilisateur. Ne pas fusionner PR #35 ni autoriser G3, une migration 007 ou une nouvelle connexion opérateur. Après validation, envisager une qualification de rendu plus proche d'une interaction navigateur sur des fixtures fictives, mais sans l'assimiler à une réception Windows réelle.


## 2026-10-17 — Qualification de comparaison chronologique React fictive

Qualifier le HEAD exact de la nouvelle PR `M32WorldOrderComparison.tsx` : tests dédiés de précédence, témoins d'ordre humain, cycle et non-comparabilité, `npm run test:ci`, `npm run build`, Rust et contrôles G3 conservés, diff et règle de protection. Vérifier le composant **non importé par `App.tsx`** et strictement sans IPC ni données opérateur. Après fusion éventuelle, choisir une autre tranche UI/test sans monter de source réelle non attestée, sans fusionner PR #35. G3 `STOP_UNAVAILABLE`, 21/3/2 externe toujours en attente, prospective `NOT_STARTED`, pas de production v7, writer, activation, M3.3 ou release.


## 2026-10-17 — Suite autorisée : qualification frontend M3.2 fictive, isolée

Qualifier au HEAD exact la PR du composant `M32ChronologyPreview` hors runtime : **18 tests Vitest dédiés**, `npm run test:ci`, TypeScript/Vite build, tests Windows Rust/Python, diff de six fichiers, branche protégée et SHA anti-race. Vérifier que `App.tsx` n'importe pas le composant et qu'aucune opération SQLite/Tauri n'y est introduite. Après une fusion qualifiée éventuelle, poursuivre seulement les composantes M3.2 sur données inventées et réexaminer les comparaisons humaines explicites sans inventer de dates ni de révélation. PR #35 OPEN/DRAFT, G3 `STOP_UNAVAILABLE`, original intact, pas d'activation 007, writer IPC, M3.3 ou release.


## 2026-10-17 — Après transfert Rust RAM : statuer sur identité d'une source

Qualifier sur le HEAD exact de la PR distincte la matrice de refus `m3_2_g3_source_identity_boundaries`, son audit des APIs Rust et les autres étapes Windows ; lire les journaux, diff, règles et fusionner seulement avec PASS terminal. Ensuite **ne pas ouvrir les originaux** : seule une nouvelle proposition de VFS dédié ou d'une connexion préouverte, authentifiée **de manière indépendante**, peut être étudiée sur données entièrement inventées puis soumise à autorisation opérateur. Si le lien sûr entre handle SQLite, fichier original, ancêtres, journaux et garantie de non-mutation demeure absent, conserver `STOP_UNAVAILABLE` et faire progresser M3.2 uniquement sur environnement isolé. Ne pas fusionner PR #35 ni déclencher G3/G4 réels, 007, activation, writer, M3.3 ou release.


## 2026-10-17 — Qualification acteur RAM à propriétaire unique, puis décision de provenance

Vérifier que la PR expérimentale `m32_owner_handoff_actor_toy` conserve exclusivement `Connection::open_in_memory`, `cfg(test)` et la compilation interdite hors tests. Attendre sur **son SHA exact** le workflow Windows `pull_request` terminal et ses **11 nouveaux tests** d'admission, transfert, concurrence, revocation, poison et arrêt ; contrôler aussi les tests existants, le diff, le statut GitHub et la protection de `main`. Après une fusion qualifiée éventuelle, ne pas fabriquer une preuve d'original à partir de tickets RAM ; s'il n'existe aucune source réelle authentifiée et déjà ouverte, rester `STOP_UNAVAILABLE` pour G3. Étudier à part une procédure de provenance qui serait soumise à un accord opérateur spécifique avant toute ouverture réelle. Pas de PR #35 fusionnée, aucune production 007, activation ou writer.


## 2026-10-17 — Après revue de faisabilité Tauri / provenance (aucune donnée opérateur)

Vérifier la nouvelle PR d'audit d'intégration sur son HEAD exact (diff, source Rust, CI Windows `pull_request`, chaque étape). Cette qualification constate seulement la topologie courante ; elle ne résout pas la provenance d'une connexion propriétaire. Après fusion protégée éventuelle, rechercher une **méthode démontrable, explicitement autorisée et indépendante du chemin** pour transférer une source déjà ouverte sans rouvrir les originaux. À défaut, garder `STOP_UNAVAILABLE` et poursuivre les travaux de conception non migrants ou les sous-parties M3.2 hors données opérateur. Ne pas préparer ni exécuter de cérémonie G3 réelle sur la base d'une CI verte.


## 2026-10-17 — Après contrat G3 : étude d'intégration sans source opérateur

Qualifier au HEAD exact les tests du contrat `M3_2_G3_OWNER_RUNTIME_CONTRACT.md`. Réétudier ensuite la faisabilité d'une vraie connexion source persistante **sans en ouvrir une sur les originaux** : cycle de vie, provenance indépendante, gestion des migrations, source snapshot, WAL/journaux et garde Win32. Si aucune telle connexion n'existe, conserver `STOP_UNAVAILABLE` ; ne pas utiliser les commandes migrantes existantes ni la fonctionnalité de tests Rust pour fabriquer cette preuve. Toute implémentation Tauri sur des fichiers réels nécessite une autorisation distincte, des opérations précises et des critères d'arrêt documentés.


## 2026-10-17 — Étape autorisée : cycle de vie Rust RAM avant toute connexion Tauri réelle

Qualifier `m32_owner_lifecycle_toy` sur le HEAD exact de sa PR Windows. Le prototype utilise exclusivement `Connection::open_in_memory`; il doit refuser une session périmée, un propriétaire révoqué ou empoisonné, un budget insuffisant, des migrations/FK défectueuses et les accès non synchronisés. Si la CI réussit, rédiger une étude d'architecture **sans aucune ouverture de source réelle**, afin de définir comment une future connexion persistante pourrait être créée et prouvée non migrante, avec source/provenance et approbation spécifique. Ne pas ajouter de commande Tauri G3 et ne pas libérer les verrous réels sur la base de tests synthétiques.


## 2026-10-17 — Qualification Rust source préexistante → RAM, sans runtime

Faire passer la qualification **sur CI Windows liée au SHA exact** de la PR Rust expérimentale, puis seulement si elle réussit établir une étude de cycle de vie/provenance d'une connexion non migrante *sans la créer sur les originaux*. La suite de 13 tests ne prouvera pas l'identité réelle d'une source, la sécurité des chemins Windows ou un mécanisme de restauration. Ne pas activer `m32-g3-owned-ram-toy` dans les builds normaux. Tout projet de commande Tauri G3 requiert une autorisation nouvelle et séparée ; pour l'instant G3 réel STOP, PR #35 draft, 007/marker/writer/M3.3 interdits.


## 2026-10-17 — Après la qualification du laboratoire SQLite Owner→RAM

Exécuter les tests du nouveau prototype uniquement sur bases fictives avec CI Windows `pull_request` **liée au SHA exact**. En cas de succès, analyser **sans exécuter les commandes Tauri/SQLite sur la machine opérateur** si le Rust actuel conserve une connexion source préexistante, sûre et non migrante (sur la base de l'architecture/code et de tests synthétiques). Aucune preuve réelle de source owner n'existe aujourd'hui. La voie G3 réelle doit rester STOP et toute future lecture doit être soumise à un accord détaillé, indépendant des résultats CI. Conserver les découvertes #46/48 sur les changements temporaires de chemin et l'historique 21/3/2. Aucune fusion PR #35, migration 007, activation, writer IPC, M3.3.


## 2026-10-16 — Veto sur les commandes de sauvegarde applicatives actuelles

L'audit du code Rust sur `main=74933c49229ab9efeae5e7c017a61b28525d3fd3` montre que `database::open_database` appelle `run_migrations`, que `database_status` et `backup::create_backup` utilisent cette ouverture, et que `backup::vacuum_copy` utilise `VACUUM INTO` après libération du fichier réservé. **Ne pas invoquer ces fonctions sur les originaux pour G3.** Une future route doit être dédiée, non migrante et sans réouverture de cible existante, qualifiée seulement sur données fictives. Pas de création d'un nouveau handle sur les originaux via une commande de statut.

## 2026-10-16 — G3 : qualifier le choix transactionnel sans ouvrir d'original

Après la PR documentaire/politique sur la stratégie G3, ne poursuivre que sur des **fixtures entièrement fictives** avec Windows CI exact-head : démontrer SQLite Online Backup API depuis une connexion **préexistante** authentifiée dans le laboratoire, vers SQLite RAM, puis sérialisation et création exclusive de la destination fictive ; tests de conflits, snapshot cohérent, mémoire, collisions, et restauration. En parallèle, évaluer techniquement si Fabulaxiom pourrait disposer d'une telle connexion sûre **sans** démarrer ou migrer l'original ; si non, conserver `NO_ELIGIBLE_STRATEGY_STOP` et documenter la limite. Ne pas remplacer ce veto par `sqlite3.connect(original, mode=ro)`, `immutable=1`, une copie brute sous writers, ni une opération opérateur. G3 réel exige un accord séparé et une procédure validée. PR #35, 007, activation, writer et M3.3 interdits jusqu'aux autorités requises.


## 2026-10-16 — Expérimentation ABA fictive : éviter toute promotion abusive de G3

À partir de `main=106c48fe3b2fd8b16bd038d29c15c99ef9e5f5db`, après qualification G3/G4 synthétique de PR #47, tester **uniquement en CI Windows** les substitutions transitoires de répertoires/sidecars dans une fixture. Même avec un résultat de test vert, conserver la décision `real_G3=NOT_AUTHORIZED` tant que les chemins d'origine, l'identité des ancêtres, l'exclusion des writers et la cohérence SQLite n'ont pas une preuve indépendante, non ponctuelle. La méthode de sauvegarde physique par un seul handle reste expérimentale ; l'Online Backup API est recommandée pour une base réellement active. Documenter les hypothèses qu'un contrôle avant/après ne peut pas prouver, y compris un A→B→A invisible. Ne pas poursuivre les originales et ne pas fusionner PR #35, ni migrer 007.


## 2026-10-16 — G3 : qualifier un flux via un SEUL handle source Win32 avant toute cérémonie Windows

À partir du `main=b2d8249002cbea8b11edcaedaa9602bd946a62c7` et des PR #42/#43 qualifiées (CI exact-head 25/25, 26/26), prochaine action autorisée **uniquement sur fixtures entièrement synthétiques** : prototyper une capture physique de base en mode ROLLBACK depuis un **handle source Win32 unique** (pas de seconde ouverture SQLite par chemin), sous partage lecture seulement, avec identification Windows volume + file index depuis le handle, comparaisons avant/après, détection de WAL/journaux et refus de courses. Valider le résultat en mémoire par `sqlite3.Connection.deserialize` + contrôles logiques de tables/migrations fictives, puis seulement un write de destination `O_EXCL` en un handle (PR #42). Suivre le [dossier d'architecture proposé](../qualification/M3_2_G3_STABLE_HANDLE_CANDIDATE_DESIGN.md) : **le document n'autorise pas cette approche sur les bases opérateur.**

Ensuite seulement : nouveau contrôle spécifique de source-safe-open pour Windows réel, protection des répertoires/ACL/chemins contre substitution, budget mémoire, comparaison réelle de `schema_migrations`, cohérence logique et destination privative nouvellement réservée. Nécessite un bloc opérateur exact, une explication complète des effets et une autorisation séparée pour chaque opération. Ne pas exécuter `open_database`, `restore_backup`, `create_backup` ni le laboratoire synthétique sur un original. Pas de G3 réel, G4 restauration, G5 signature, G6 GUI tant que les verrous restent. Historique 21/3/2 non promu.


## 2026-10-16 — G2-A : proposer un bloc Windows limité, attendre la preuve opérateur

Re-fetch `main` et les PR, qualifier le diff documentaire G2 sur le HEAD exact. Présenter à l'opérateur **un bloc PowerShell `& { ... }` détaillé, sans ouverture SQLite ni accès aux fichiers protégés**, limité à jeton/processus/références. Expliquer préalablement interactions éventuelles, privilèges, processus, lectures/écritures, conditions STOP. Puis seulement après résultat et nouvel accord explicite, étudier G2-B avec les chemins locaux confirmés et leur politique de non-mutation. Ne pas lancer directement `open_database`, `create_backup`, `restore_backup` ou `m3_1_v6_backup.py`. Pas de cérémonie G3 réelle, restauration G4, signature G5, GUI G6, production 007, writer, fusion PR #35 ou M3.3. Baseline prospective `NOT_STARTED`.


## 2026-10-15 — réconciliation solo puis laboratoire synthétique (pas Windows protégé)

Qualifier PR #37 **après** réconciliation avec la politique SOLO fusionnée par #39, sur le nouveau HEAD et ses étapes CI ; vérifier le diff documentaire, contrôler la protection de main et fusionner seulement si toutes les barrières sont satisfaites. Ensuite créer une PR distincte **strictement laboratoire synthétique** pour preuves de création exclusive / backup / restauration / checks contradictoires et tests adversariaux. Les données Windows réelles exigent le préflight G2 exact et un plan G3 distinct validant chemins, ACL, source WAL/SHM et destination neuve ; ne pas proposer de script opérateur exécutable avant cela. Historique 21/3/2 `PENDING_EXTERNAL_ATTESTATION`, prospective `NOT_STARTED`, M3.2 applicative non autorisée ; aucun 007 prod, writer ou PR #35 merge.


## 2026-10-15 — Qualifier la PR documentaire d'exception SOLO avant toute décision d'autorité

Re-fetch `main`, les PR #35/#37 et la nouvelle PR distincte ; vérifier le diff documentaire et le **workflow pull_request sur son HEAD exact**. Soumettre au propriétaire **la décision explicite d'adopter ou rejeter seulement la politique**, puis préparer **séparément** une réconciliation de la PR #37, de sa fiche de revue indépendante et des issues #36/#38. **Aucune exception en vigueur tant que ces étapes ne sont pas approuvées et appliquées.** Les phases Windows observation, acquisition, restauration, risque et tests applicatifs demandent chacune une autorisation future séparée. Historique 21/3/2 non attesté, baseline prospective `NOT_STARTED`, M3.2 réel `NOT_AUTHORIZED`. Aucun PowerShell de fichiers protégés, migration 007, writer, merge #35 ni M3.3.


## Current authorization — normalize M3.1 before M3.2 (2026-10-11)

M3.1 implementation PR #33 is **MERGED** at `main=922d155d4f4321ed8b90955d4ea96388751f0daf`, from qualified final head `796a4b65e596b9bc05bd00b523b3209f9736524d`; required `pull_request` CI #38176139985, attempt 3, terminal SUCCESS. Main is really protected by active no-bypass ruleset. Operator target Windows v7 read-only *isolated* GUI/IPC PASS + post-exit 11/11 SHA and M1.5 active v6 custody PASS. Elevated preparation is now fail-closed in source.

**Only authorized next work:** qualify this independent documentary-only M3.1 normalization PR (new exact HEAD + GitHub Actions status, review documents/changed paths, protected SHA-guarded merge, re-fetch `main`). **Until this succeeds, M3.2 is not authorized.**

After terminal normalized merge, M3.1 may be declared **COMPLETE + MERGED + NORMALIZED** for its bounded, explicit *isolated candidate schema + read-only controlled-start* scope. Then and only then authorize **M3.2 manual chronology and ordering UX** in a fresh, separately governed branch/PR. Normal end-user executable is still schema **v6**; any production v6→v7 migration needs an entirely separate operator-authorized backup, verified activation pointer and safe release gate; it is **not** implicit in M3.1 normalization, M3.2 authorization or GUI preview. No M4+, ComfyUI or release.

Old NEXT records below are historical.

## Current exact-head gate — M3.1 PR #33

Bounded Windows debug-only isolated Tauri v7 read-only GUI, IPC, and post-close 11/11 custody **PASS** on operator-qualified source `4d520e1825ecd08d20484b0e72d60ffe6ea09e4c`. Next: obtain terminal SUCCESS for the **new security/preparation guard + documentary evidence HEAD** on PR #33; re-fetch actual `main`, PR/branch, all exact-head checks and scope; explicitly assess isolated controlled-launch satisfaction versus still-unapproved production v7 activation; then only when all gates pass, SHA-guarded implementation merge, re-fetch main, **independent** documentary normalization PR/CI/merge. Do not unlock M3.2 until normalized. No auto-007, production v7, M4+, ComfyUI or release.

Older next-work and planning records below are retained for historical continuity, not current authorization.

## Completed milestone

**M1 — Persistence and project foundation: COMPLETE + MERGED + NORMALIZED**

M1.1 through M1.5 are qualified, merged, and post-merge normalized.

Final implementation PR:

**#15 — feat: implement M1.5 safe SQLite backup and restore baseline**

Implementation merge:

`282b325fb6c588a70df08a5128415c8fa0a0f72e`

Exact-head implementation evidence SHA:

`152b40e616f40799abc61f9ce8db142e3b19340b`

Terminal `Fabulaxiom CI`:

- run `37720676744`;
- `completed/success`;
- 13/13 frontend and 37/37 Rust PASS;
- frontend build, `cargo check --locked`, dependency locks PASS.

Real Windows qualification:

- clean source and exact Git SHAs;
- SQLite v3 and Tauri bridge PASS;
- Ollama OFF;
- app backup and controlled restore with UI reload PASS;
- 1 Universe, 1 Novel, 1 Scene, 3 revisions, 1 current head retained.

Evidence: `docs/qualification/M1_5_BACKUP_RESTORE_BASELINE.md`.

## Completed milestone — M2

**M2 — Narrative entities and canonical facts: COMPLETE + MERGED + NORMALIZED**, after PR #30 merge `f13b4f8c249866ff60a19d7895b6cfaede56398a` and exact normalization CI #38041908126 (13/13 success).

Detailed planning PR: **#17 — docs: plan M2 and authorize M2.1 schema after acceptance**.

Planning merge: `4a9115ec362a0efae696ebc94b5101fa46d7a03a`.

Planning exact SHA: `44669d9070870624b845ab0825ebd555eef0dcbc`.

Terminal `Fabulaxiom CI` run `37722657799`: `completed/success`.

Accepted plan: `docs/roadmap/M2_NARRATIVE_ENTITIES_CANONICAL_FACTS.md`.

## Completed subdivision

**M2.1 — Entity registry schema and migration: COMPLETE + MERGED + NORMALIZED**

Implementation PR: #20.

Implementation merge: `6c58b3bd4f0588436da8ba45adb875f897f426b2`.

Windows-qualified source SHA: `c7a663d88ba2538714d42fdd366719cd54fe6f70`.

Evidence SHA: `88fa3b22904b92d4ecdcb32ed7fd01dc23e24a4c`.

Terminal exact-head `Fabulaxiom CI`: run `37814949619`, `completed/success`, frontend 13/13, Rust 44/44, build/check/lockfiles PASS.

Real Windows v3 → v4 qualification: PASS. Source data/scene revisions/head preserved, migration 1–4, STRICT registry tables, triggers/indexes, foreign keys/integrity PASS, backup and active marker unchanged.

Evidence: `docs/qualification/M2_1_ENTITY_REGISTRY_SCHEMA.md`.

## Completed subdivision — M2.2

**M2.2 — No-AI entity and alias CRUD: COMPLETE + MERGED + NORMALIZED** — takes effect only after this separate normalization PR merges and `main` is re-fetched.

- Implementation PR: **#23**; Windows-qualified source: `b54fffd8e1f0224372e3b99cee07cb6df3203973`.
- Qualified code CI `37831790345` and evidence-head CI `37864503602` on `a96870f823f24cb8962c9b0f43336ccb883ad5c3`: both `completed/success`, exact `pull_request` SHA confirmed.
- Protected implementation merge: `ad7211fa2f292b8bd9812e299dbb6be96214eb89`.
- Real Windows: **13/13 interactive cases**, **21/21 frontend** and **51/51 Rust** tests, `cargo check --locked` / frontend build / lockfiles: PASS; Ollama OFF.
- SQLite v4 after interactive tests: 9 entities, 8 aliases, one duplicate-name character pair with distinct IDs, 3 scene revisions / 1 pointer preserved, valid STRICT/migrations/FK/integrity, active restored database and historical backup preserved.
- Evidence: `docs/qualification/M2_2_ENTITY_ALIAS_CRUD.md`.

## Completed subdivision — M2.3

**M2.3 — Fact registry and exact revision provenance: COMPLETE + MERGED + NORMALIZED**, effective when the separate normalization PR is terminal-CI-qualified and merged.

Implementation PR #25 merged into `main=e6e80c26316f11054348a18a235fd08c600e136e` from evidence HEAD `b015f7df80f38d75375a0e2615fd62d4c40ee1b8`, after Windows-qualified source `4d3b4b6015d477c3a6a5c3750d9743174e9c44a7`.

Source CI `37879358744` and evidence CI `37961014980`: terminal SUCCESS, all Windows steps PASS. Local 21/21 frontend, 61/61 Rust and 8/8 UI checks PASS with Ollama OFF. Real SQLite v4→v5 migration on M1.5 restored-active DB and independent read-only audit PASS: five exact migrations, STRICT fact/source tables, FK/integrity, full prior row digests, nine entities, eight aliases, three revisions, one head and all historical backup custodial hashes preserved. Evidence: `docs/qualification/M2_3_IMPLEMENTATION_GATE.md`.

## Completed subdivision — M2.4

**M2.4 — Canon status and human review service: COMPLETE + MERGED + NORMALIZED** only after this separate documentation normalization PR is fully exact-HEAD-CI qualified and protected-merged.

Implementation PR #27 protected-merged at `main=3a069572d00e1680c42b0f13b800e28687c5f0eb`. Windows qualified source `aad56bd59fdb87be5ac1eda99b1969452bf61a26`; evidence HEAD `b53405779b04c16525ba48a266bd096096af7020` had its exact `pull_request` run `37989040863` terminal success (13/13 Windows CI steps); source CI `37974831473` success (21/21 frontend, 71/71 Rust).

Real Windows migration to SQLite v6 and full existing data/backup integrity PASS, with pre-v6 verified backup SHA-256 `db02961d7a30c6a6522bd52faeab8ceb09e26c1a4a6a58be467d142806e22fee`, 8/8 existing GUI controls (Ollama OFF), 8/8 isolated Rust human-review tests and unchanged production v6 DB snapshot SHA-256 `67dfd9194ff884762bbffaa39d774df10fadcd74cbc9e6774e36d323e4506fc6`. Exact history/current head and nine entities/eight aliases preserved. The reviewer label is self-declared and **not** an authenticated identity. There is no Windows E2E React fact-review screen or E2E IPC invocation acceptance yet; no production fact rows created. See `docs/qualification/M2_4_CANON_REVIEW_IMPLEMENTATION_GATE.md`.

## M2.5 — COMPLETE + MERGED + NORMALIZED

- PR #29 successfully protected-merged at `f1e7ea99d26ad3390c7c47bfb339f26d730a44f1` from evidence HEAD `6f55fc3fc7eab6f2288a54619c0bef70e521f47e`, after source qualification `7eaaf45ae164c9336df7e01c9da6787e4971d59e`. Exact evidence-head `pull_request` CI **38040227617**: `completed/success`, 13/13 Windows steps, frontend 32/32, Rust 72/72, `cargo check --locked`, locks unchanged.
- Real Windows operator qualification: hierarchy 8/8, stale-Universe sync correction 8/8, sourced/unsourced fact entry and exact UTF-8 historical citations 9/9, explicit human review interaction checklist 10/10. Independent v6 SQLite read-only audit: **3 facts, 2 exact source anchors, 11 append-only review events**; source revision and prior narrative contents preserved. Earlier 10-event audit script incorrect; actual 11 rows must remain untouched.
- Production restored-active v6 logical digest `67dfd9194ff884762bbffaa39d774df10fadcd74cbc9e6774e36d323e4506fc6` unchanged. Isolated v6 test database digest `cff8a04f29ec60757c02ef9ed186be40c806cfcc6a2cfd11fa8072be44f273cb`. Verified isolated pre-fact backup `9e738d58519e1a0e3c1750d71726b661132fcbc0211fddea3178f6314bbfc7cf`, all historic pre-M2.1/v4/v5 backups intact.
- Reviewer identity self-declared, not authenticated. No AI extraction, no automatic canon promotion, no new dependencies or SQLite v7. Evidence: `docs/qualification/M2_5_SOURCED_FACTS_REVIEW_UI.md`.

**CURRENT AUTHORIZATION GATE: independent post-planning M3 normalization.** Planning PR #31 merged as `68db746754e01b441870e0653f17f10ebfc7be2f` from `5127ced6c5e175b0919c736c658036382794487e`, after exact-head `pull_request` run `38050865413` (`completed/success`; one Windows job, 13/13 steps). Its six changed paths are exclusively documentary. **Only after** this separate normalization PR's new exact-head CI, SHA-guarded merge, and fresh `main` re-fetch may work begin on **M3.1 alone**. M3.2–M3.6, M4+, ComfyUI and any unqualified production v7 migration remain unauthorized.

**Next exact step:** qualify/merge `docs/qualification/M3_PLANNING_POST_MERGE_NORMALIZATION.md` and the associated authority updates. The governed M3 roadmap is `docs/roadmap/M3_TIME_KNOWLEDGE_RELATIONSHIPS.md`. After normalization, M3.1 may be implemented in its own PR, without authorizing M3.2 or running SQLite migration on an operator machine before the separate backup/Windows qualification. The ComfyUI atelier remains a future unimplemented proposal (issue #19).

## Branch-protection truth

GitHub reports `main.protected=false` for this private repository; repository ruleset access returned a plan restriction (HTTP 403). Existing merges use a **SHA compare-and-swap guard (`expected_head_sha`)**, not a formally enforced protected branch. Continue the exact-head CI, scope, and re-fetch gates without misrepresenting the repository configuration.

## Governance and distribution

Keep the source-based release state unchanged. No release is authorized as part of this documentary normalization. No data migration or target-machine action is required. Preserve Tauri app identity in production, M1.5 active pointer, all existing operator backups, SQLite v6 data/history, deterministic lockfiles and independent local-only test worktrees. Never reuse CI from an earlier commit.
