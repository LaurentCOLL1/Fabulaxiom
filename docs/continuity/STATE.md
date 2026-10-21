# Fabulaxiom — Current State

## 2026-10-21 — nouvelle tranche produit candidate, deux romans fictifs dans l'atelier navigateur

Ajout d'une deuxième scène et d'une révision historique appartenant à un autre roman **du même Univers inventé** sur le banc d'essai `m32BrowserLab.tsx`. Tests proposés : 4 Vitest (36 total) et 2 Chromium (38 total) couvrant le filtrage strict des révisions par scène et l'absence d'ordre du monde/révélation déduit des positions de manuscrit. Nouvelle CI au head exact à obtenir : état actuel **CANDIDAT**, non une preuve de succès. Aucune intégration dans App.tsx, SQLite original, Tauri IPC ou Windows ; PR #35 DRAFT, M3.2 IN_PROGRESS_NOT_ACCEPTED, G2B–G6 STOP et écrivain réel NOT_PROVEN.


## 21 octobre 2026 — état après PR #100 fusionnée

GitHub vérifié : PR [#100](https://github.com/LaurentCOLL1/Fabulaxiom/pull/100) MERGED, `main=bf59b28b437470a4759a5971968e8f00f9fa895c`, head PR `95e2e0385979e2b226aa1d6289e12250c6e6e19d`, CI PR #39533766395 SUCCESS et CI main #39534698504 SUCCESS, terminales sur leurs SHA respectifs. Aucun nouveau commit ne peut réutiliser ces CI. Preview des chemins qui créeraient un cycle, blocage des corrections avant révocation humaine, 32 Vitest et 36 Chromium : **uniquement un atelier sur données fictives**, ni produit accepté ni preuve Windows.

M3.1 COMPLETE/MERGED/NORMALIZED ; **M3.2 IN_PROGRESS_NOT_ACCEPTED**, PR #35 OPEN/DRAFT. Étape produit suivante : UX des trois ordres monde/narration/révélation sur fixtures sans persistance et tests neufs. G2A PASS metadata-only, accord consommé ; écrivain SQLite réel NOT_PROVEN, G2B–G6 NOT_AUTHORIZED, G3 réel STOP_UNAVAILABLE, historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED. Aucun original v6/v7, journaux/sidecars, sauvegardes, ACL, marqueur, migration007, writer IPC, M3.3, ComfyUI ou release. Nouveau script Windows uniquement avec texte intégral/effets/interactions et accord explicite.

---


## 2026-10-21 — historique du candidat PR #100, depuis fusionné

PR #99 fusionnée avec `main=205a328150c90bf1fb4f52abd7fb8c04f3959468`, CI PR #39480662913 SUCCESS (74/74), push #39482419125 SUCCESS. Un candidat d'UX ajoute `previewFictionalPrecedence` (chemin-témoin d'un cycle au lieu d'une simple erreur), `previewFictionalCorrection` (relations actives devant être révoquées, référence exacte de révision historique conservée), visibles dans `M32ManualChronologyLab.tsx`. Rien dans `App.tsx`, Tauri, SQLite ou IPC ; aucun chemin disque ou réseau. 10 nouveaux tests Vitest (32) et 2 Chromium (36), CI à qualifier au HEAD exact. Roadmap M3.2 IN_PROGRESS_NOT_ACCEPTED ; PR #35 DRAFT ; absence de writer réel NOT_PROVEN ; G2B–G6 STOP ; historique PENDING 21/3/2 et prospective NOT_STARTED.


## 2026-10-20 — identité de révision historique dans l'atelier manuel fictif

`main=7477001cd0ebc69d4701f21eddbda898f94c79c5` après fusion de PR #98, CI PR #39447951647 SUCCESS 74/74, CI push main #39449601527 SUCCESS. Candidat `m32FictionalManualChronology.ts` / `M32ManualChronologyLab.tsx` : catalogue littéral de scènes+révisions inventées, sélection explicite d'une ancienne révision, vérifications Universe/novel/scene/exact revision, hériter la référence lors d'une correction par supersession. Références source non authentifiées puisque inventées ; aucune lecture du texte réel, de SQLite, du head actuel ou de l'IPC. Nouveaux tests : 22 Vitest et 34 Chromium à vérifier dans la CI fraîche. Roadmap M3.2 non acceptée, PR #35 brouillon, provenance 21/3/2 et baseline prospective NOT_STARTED, G2B–G6 STOP. Base v6 active, v7 isolée, journaux, sauvegardes, ACL, migration007, writer IPC et release non touchés.


## 2026-10-20 — amélioration produit fictive, toujours aucun accès à la production

PR #97 fusionnée sur `main=a839953f73f17379aa7c5ccde69d807b5b99a2f6`, CI PR #39426793283 SUCCESS (74/74), push main #39428345389 SUCCESS. Nouveau réducteur TS sans persistance `src/m32FictionalManualChronology.ts`, formulaires `src/M32ManualChronologyLab.tsx` exposés seulement dans `m32BrowserLab.tsx` et 13 tests Vitest. Saisie des quatre temporalités, précédence `avant/après` acyclique, refus des références douteuses, supersession append-only et révocation humaine. Aucun chemin SQL, aucune migration 007, aucune modification App.tsx/Tauri ou vraie DB. Nouveau HEAD CI à qualifier, état M3.2 IN_PROGRESS_NOT_ACCEPTED, G2B–G6 STOP, absence writer réel non prouvée, provenance 21/3/2 et prospective NOT_STARTED.


## 2026-10-20 — revue des cinq roadmaps de V1 et écart M3.2

PR #96 protégée fusionnée à `main=e35b7c92441c517d4f0fcacb829711c4d1e9da97`, CI #39414915855 SUCCESS 73/73 et CI push main #39416303498 SUCCESS 72/72. Audit direct GitHub des cinq fichiers `docs/roadmap/` : le master V1 et M2 avaient des déclarations historiques « M3 non autorisée » malgré PR #33+PR #34 prouvant M3.1 fusionnée et normalisée. Nouveau `docs/roadmap/ROADMAP_STATUS_CURRENT.md` et `docs/roadmap/README.md`, bannière de statut daté en tête de chaque roadmap. M3.2 pas encore acceptée : manque CRUD chrono/GUI manuel offline, préservation opérateur et normalisation ; PR #35 DRAFT, G2B–G6 toujours STOP. 9 tests source-only de cohérence sont ajoutés en CI, qualification exacte du nouveau PR à faire. M3.3–M3.6/M4–M9 et ComfyUI restent en attente. Aucun changement SQLite, Tauri, production v6, iso v7, sauvegarde, ACL, sidecar, migration 007, writer IPC ou release.


## 2026-10-20 — expérience négative d'un second écrivain sur RAM inventée

PR #95 fusionnée `main=a8578b8e128af2264e85a7341a96e13d0e086b23`, CI PR #39406700987 au HEAD 29bae8aee7e6985e20bfd1ebda34f7a5b2c8732d SUCCESS (72/72), CI push main #39407869929 SUCCESS. Suite : tests source-only en Python avec deux connexions à la même RAM imaginaire (mode=memory, uri=True, cache=shared), démontrant écriture indépendante sous query_only du lecteur et compteur total_changes inchangé malgré modification externe. Aucun original, WAL/SHM, sauvegarde, ACL, marqueur, migration 007, writer IPC, release ou Tauri touché. G2A metadata-only PASS opérateur, absence de writer réel NOT_PROVEN, G2B–G6 pas autorisés, historique PENDING 21/3/2 et prospective NOT_STARTED. Nouvelle CI exact-head avant fusion.


## 2026-10-20 — PR #94 fusionnée ; nouveau prototype de lecteur RAM fictif

PR #94 fusionnée sous règles main, SHA 632e6d6d985affa6989bb220ddec99911e6ba1e6, CI PR #39394068343 SUCCESS (71 étapes sur HEAD 74395428c185198632cc2cd2c19eec4b7132e4ad). Nouveau module test-only `m32_preopened_query_only_toy.rs` : emprunt d'une connexion fictive `&Connection` déjà ouverte, mode query_only vérifié et non activé par l'API de lecture, version 6/7 entièrement inventée, database_list sans chemin, 13 tests sur absence de migration et refus d'écriture/attaches/versions/état modifié. Aucun runtime Tauri/IPC ni base de production. Nouvelle CI exigée au SHA final de la PR. Aucun writer original attesté ; G3 réel toujours STOP, v6/v7 et sauvegardes/journaux/ACL/activation markers protégés, PR #35 DRAFT, provenance 21/3/2, prospective NOT_STARTED et release non autorisée.


## 2026-10-20 — nouveaux tests de couverture du Rust source-only

Après PR #93 fusionnée sur main 15c91039243206dc61190fec5668f32a87f3faf0, CI #39391766661 SUCCESS au HEAD dcad1a905d8f21cf0a18a03e2cfc2c95050cf100 (70 étapes), nouvel inventaire de 25 fichiers .rs Rust/Tauri sur les seuls textes du dépôt GitHub. Vingt fichiers présentent les signatures retenues ; le nouveau scanner `tools/m32_rust_sqlite_open_inventory.py` fige les comptes de base par fichier, bloque les écarts et n'autorise jamais G3 réel ; 18 tests fictifs ajoutés en CI. Ne pas confondre le tripwire textuel avec une preuve d'absence de writer ni une vérification exhaustive des macros Rust. Historique 21/3/2 toujours en attente, prospective NOT_STARTED, G2B–G6/SQLite originaux/migration 007/writer IPC/PR35/release INTERDITS. Prochain contrôle : CI exact-head au SHA de la nouvelle PR.


## 2026-10-20 — décision documentaire G2–G6 à jour, sans promotion

PR #92 fusionnée sur `main=8e358d61b7f5438b893a416aa8f82d884569c5da` après CI PR #39388988034 SUCCESS (70 étapes au HEAD `cb5e1eaeaaf64bd684be6a80c9cc3b85fc56492b`). Le nouveau `docs/continuity/M3_2_GATE_DECISION_CURRENT.md` sépare G2-A PASS uniquement métadonnées (opérateur, 01:31:24+02:00) des G2-B/C/D/G3/G4/G5/G6, tous non autorisés. Ancien snapshot G2 global du 19 octobre conserve ses constats datés. Writer SQLite absent non prouvé, accès original toujours STOP, provenance 21/3/2, prospective NOT_STARTED. La correction documentaire n'autorise aucun script Windows ni accès à la production v6, à v7 isolée, aux sidecars/ACL/backups/markers, à migration 007, writer IPC ou à PR #35/release.


## 2026-10-20 — inventaire des six chemins SQLite et tests de dérive sans exécution

PR #91 fusionnée sur main fb4625450439ecf236cc9065f434eda002f71533, CI #39376628743 au HEAD 94c9886e4e362867cab86c39efc5b13125a94dac SUCCESS (69 étapes), writer réel non prouvé. Source-only nouveau : `tools/m32_g3_runtime_entrypoint_source_audit.py` vérifie les séquences existantes des chemins open_database, database_status, create_backup, vacuum_copy, reserve_unique_file, read_validated_database sur fichiers Rust publics seulement ; 18 tests de refus imposent un nouveau review si le code change. Scanner textuel limité aux signatures connues, non exhaustif, non permission G3. Aucun original local v6/v7, sidecar, backup, ACL, activation marker, migration 007 ou writer IPC manipulé. STOP G2B–G6, PR #35 et M3.3/release. Prochaine étape : CI au nouveau SHA et fusion gouvernée si conformité.


## 2026-10-20 — blocage restant : writer SQLite NON PROUVÉ (audit public source-only)

Après fusion PR #90 sur `main=45ce1511aa616fce9664dfc08cea39f290d2273d`, PASS G2-A metadata-only de 01:31:24 conservé ; re-fetch repository `src-tauri/src/database.rs::open_database` (crée parent si requis, `Connection::open`, migrations), `lib.rs::database_status` (appel direct), `backup.rs::create_backup` (source via open_database, `VACUUM INTO`). Ces chemins ne conviennent **pas** à une capture G3 protégée. Nouvelle revue source-only `docs/qualification/M3_2_G2A_WRITER_ABSENCE_GAP_SOURCE_REVIEW.md` avec 13 tests purement inventés refusant toute promotion de G3 même en présence de tous les signaux simulés. Aucune interaction locale ni vrai handle/DB. Identité/provenance/cold-source journal/owner SQLite non migrant restent manquants. STOP G2-B à G6, PR #35 fusion, M3.3, migration 007 et release. Prochaine action sûre : CI exact-head de la nouvelle PR et documenter sans commande opérateur.


## 2026-10-20 01:31 — G2-A nouvelle version PID 0 : PASS_METADATA_ONLY opérateur

L'utilisateur a donné une autorisation explicite, distincte et limitée à l'exécution manuelle du code exact dans `docs/qualification/M3_2_G2A_PID_ZERO_CANDIDATE_REVIEW.md`, après CI PR #89 SUCCESS. Sortie assainie : `G2A_LOCAL_METADATA: PASS`, `POWERSHELL_VERSION: 5.1.26100.9587`, `LOCAL_CLOCK: 2026-10-20T01:31:24+02:00`, `TIMEZONE: Romance Standard Time`, `TOKEN_INTEGRITY: MEDIUM`, `FABULAXIOM_OLLAMA_PROCESS: NONE_MATCHED`, `WEBVIEW2_SEARCHHOST_LINEAGE: 6 OBSERVED_METADATA_ONLY`, `WEBVIEW2_OWNERSHIP_AUTHENTICATED: NO`, `PROCESS_WRITER_ABSENCE: NOT_PROVEN`, `PUBLIC_GITHUB_CHECK: NOT_ASSESSED_BY_THIS_BLOCK`, `G2B_G2C_G2D_G3_G4_G5_G6: NOT_AUTHORIZED`, `TAURI_RUNTIME: NOT_TESTED`. Consentement unique consommé, pas de réexécution sans une nouvelle autorisation. Ce PASS atteste **uniquement** des métadonnées observées ; pas d'identité Microsoft vérifiée, ni absence d'écrivain SQLite, ni admission d'autres gates. L'ancien STOP PR #86 reste historique et sa cause fine inconnue ; le correctif PID 0 ne prouve pas qu'il en était la cause. Le dépôt GitHub a été interrogé en dehors de ce script. Aucun fichier opérateur, processus Windows ou SQLite n'a été manipulé depuis ChatGPT. CI PR #90 à revérifier au HEAD neuf avant toute fusion.


## 2026-10-20 — PR #89 fusionnée, AST et fixtures PASS, G2-A toujours STOP

Après re-fetch anti-course de `main` et HEAD, CI #39339365546 au HEAD exact `e188a98090112551b6a35dd78e8327914c0e9965` terminale SUCCESS, 68 étapes Windows. Ruleset Protect main #24895490 actif sans bypass, required check app 15368 validé, zéro discussion non résolue/demande de changements, diff borné. PR #89 protégée fusionnée : `main=f14e5991d34350682647ef6f0bd67b1d2055f41a`. Nouveau candidat exact PID 0 Markdown seulement, non exécuté/non approuvé sur Windows. Historique STOP `WEBVIEW2_PARENTAGE` inchangé, cause fine inconnue. Prochaine étape : présenter au propriétaire le nouveau texte intégral et obtenir son autorisation explicite avant tout essai local ; ne pas poursuivre G2-B/G6 ni toucher SQLite/ACL/backup/sidecars/migration 007/writer IPC.


## 2026-10-20 — PR #88 fusionnée ; correction candidate PID 0 préparée sans runtime

CI PR #88 #39303355912 à la source exacte `0b7c55f30f0a7967270e9a58be7beae25087fec5` : SUCCESS, puis fusion protégée `main=6d9d9ff52459873347180f509717180ccccd0d5f`. Le nouveau candidat dans `docs/qualification/M3_2_G2A_PID_ZERO_CANDIDATE_REVIEW.md` est DISTINCT et NON EXÉCUTÉ ; exception bornée à un `System Idle Process` PID 0, rejet du double zéro, des alias et des PID invalides, maintien des ancêtres hors zéro. Script #86 historique conservé. Qualification à mener sur le SHA final de sa propre PR (Python fictif, exact-source guard, AST Windows seulement). Aucun élargissement G2–G6, SQLite, migration 007, IPC writer, release. Le STOP réel WEBVIEW2_PARENTAGE est maintenu, la cause exacte non démontrée.


## 2026-10-19 — deuxième essai G2-A, code PR #86 : STOP WEBVIEW2_PARENTAGE

Le propriétaire a relu le texte complet du bloc corrigé, accordé une autorisation spécifique et communiqué ensuite cinq lignes : `G2A_LOCAL_METADATA: STOP`, `STOP_STAGE: WEBVIEW2_PARENTAGE`, `STOP_REASON: UNEXPECTED_OR_UNSAFE`, `G2B_G2C_G2D_G3_G4_G5_G6: NOT_AUTHORIZED`, `TAURI_RUNTIME: NOT_TESTED`. La condition fine à l'intérieur de `WEBVIEW2_PARENTAGE` est masquée par le catch ; ne pas inférer parent manquant, PID réutilisé, dérive d'instantané ou défaillance CIM. Une lacune **du code source** est toutefois identifiée : la validation brute `$id -le 0` refuse aussi le `System Idle Process` de PID 0, qui peut être fourni dans l'inventaire CIM ; ce seul fait produirait `AMBIGUOUS_PROCESS_ID` et donc STOP. Il s'agit d'une hypothèse plausible, non d'une preuve sur les données Windows réelles. Les fixtures source-only 14/14 n'avaient pas de PID zéro. Autorisation consommée, pas de réexécution implicite. Avant ce checkpoint, l'ancien essai #85 s'était arrêté à `PROCESS_NAMES`. Historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 OPEN/DRAFT, issues #36/#38 OPEN, G2-B/C/D à G6 NON AUTORISÉS ; aucune commande émise ici visant la production v6 ou la v7 isolée. Une éventuelle nouvelle proposition diagnostique doit être étudiée en source-only et soumise intégralement à autorisation distincte. Les notices historiques « jamais exécuté » ci-dessous reflètent leur date antérieure.


## 2026-10-19 — continuité durable M3.2 (point d'entrée « living handoff »)

Après PR #86 protégée (main observé `6d9650ee09d6f8a695a9b71a9ef1e1118f7229c9`, CI PR #39241294071 SUCCESS), introduction d'un [README de reprise](README.md), d'un [état courant court](HANDOFF_CURRENT.md), de sa [forme JSON](HANDOFF_CURRENT.json), d'un [protocole](HANDOFF_PROTOCOL.md), d'un [historique](HANDOFF_HISTORY.md) et d'un [prompt minimal](RESUME_PROMPT.md). Chaque nouvelle PR technique M3.2 devra modifier les fichiers MD et JSON de handoff dans la même PR ; tests CI source-only et contrôle du diff empêchent les oublis. Les références sont datées, jamais lues comme autorisations réelles. Correctif SearchHost de PR #86 **fusionné mais jamais exécuté sur le PC opérateur**. L'accord de principe doit être confirmé sur les octets exacts avant essai G2-A ; G2-B/C/D et G3–G6 restent STOP.


## 2026-10-19 — G2-A : correction proposée après STOP PROCESS_NAMES, aucune exécution autorisée

Observation opérateur du bloc PR #85 : `G2A_LOCAL_METADATA: STOP`, `STOP_STAGE: PROCESS_NAMES`. Capture Process Explorer : six WebView2 sous SearchHost (PID 4740 à l'instant de capture, non utilisé dans le code). PR nouvelle : modifier le bloc PowerShell **en Markdown uniquement** pour distinguer l'arbre SearchHost des WebView2 étrangers, via `Get-CimInstance Win32_Process`, comparaison des PID de deux instantanés, vérification de l'ordre des dates de création et du parcours des parents (cycle, parent manquant, incohérence => STOP). Aucun processus n'est arrêté. Les vingt tests de texte sont actualisés et cinq contrôles ajoutés ; quatorze scénarios purement synthétiques vérifient les verdicts. L'AST Windows reste parser-only. Un PASS de ce futur bloc n'authentifiera ni le binaire SearchHost, ni l'absence d'un writer SQLite. Le bloc initial reste la seule version approuvée jusqu'à nouvel accord explicite. G2-A réel reste STOP, G2-B/C/D et G3–G6 non autorisés, Tauri/WebView2 opérateur non testé, PR #35 DRAFT, #36/#38 OPEN.


## 2026-10-19 — PR #85 : AST syntaxe qualifiée, cardinalité dynamique diagnostique

La CI au HEAD `6dd7e28897d226c02e0d212b2784293ff28606a3` a passé 20 tests Python et la syntaxe PowerShell `Parser.ParseInput`, mais la cardinalité attendue pour les `CommandAst` dynamiques a déclenché un STOP du job avant les régressions. La nouvelle version garde l'inventaire de commandes connues et un seuil de refus conservateur (`>4`), avec un compteur informatif ; les contrôles Python sur le texte restent requis. La liste de refus de sortie mentionne explicitement G3/G4/G5/G6. Le bloc demeure un candidat **non exécuté**, G2-A non autorisé. Nouvelle CI exact-head indispensable ; ancienne preuve FAIL/SKIPPED non réutilisable.


## 2026-10-19 — PR #85 : correction du seul extracteur AST de Markdown

Au HEAD `b14fb8d1bcff1ca28387c65233c4c010268abe6a`, CI `pull_request` Windows a passé les 20 tests source-only du candidat, mais STOP à l'extraction `[regex]::Matches` des délimiteurs Markdown ; aucune exécution du bloc, suites aval ignorées. L'extracteur GitHub CI a été remplacé par comparaison **exacte des deux lignes de clôture**, découpage par IndexOf puis `Parser.ParseInput` (non exécuté). Aucun octet du bloc PowerShell proposé n'est changé. La qualification du nouveau HEAD est obligatoire : CI antérieure FAIL/SKIPPED non réutilisable.


## 2026-10-19 — PR #85 correction du workflow invalide, requalification HEAD neuf

La première version `16de4a37a8bb09d7208925859aa761014ba81352` a produit un workflow YAML invalide, détecté par GitHub avant création de job (run #39215639069 `failure`, `push`, zéro job). Cause : remplacement de texte Javascript interprétant `$'` dans l'expression régulière et insérant une copie du reste du workflow. Le workflow a été reconstruit **à partir du main vérifié**, avec insertion contrôlée par callback et préflight d'unicité des étapes. Aucun test ancien à recycler ; la **nouvelle CI pull_request au SHA nouveau** sera la seule preuve. Le bloc PowerShell G2-A reste INERTE/NON AUTORISÉ et n'est jamais exécuté.


## 2026-10-19 — M3.2 G2-A : PowerShell exact préparé comme texte, non exécuté

Base `main=9d058362a6804d642aad75cdb29cd6d7540e35cf`, PR #84 fusionnée et CI Windows #39211774008 60/60. Nouveau [candidat G2-A](../qualification/M3_2_G2A_EXACT_BLOCK_REVIEW.md) contenant un seul bloc PowerShell `& { ... }` non exécutable automatiquement, avec contrôle SID d'intégrité medium, version/horloge et noms de processus. Aucune lecture SQLite, ACL, backup, chemin opérateur, sortie de SID, Git local ou réseau ; absence de processus ne prouve PAS absence d'écrivain. Les tests Windows ajoutent 20 refus Python sur le texte et l'analyse AST PowerShell (ParseInput, **sans exécution**). Aucun `.ps1`, aucun lancement opérateur, approbation G2-A NON ACCORDÉE. CI nouvelle exact-head obligatoire, tous STOP maintenus.


## 2026-10-19 — M3.2 G2-A consentement : nouvelle proposition INERTE, aucune observation Windows

Sur `main=41259a088c7d85fe7eda2ad5086964f464f93ff8` après PR #83 (CI Windows #39205535763 SUCCESS 59/59), ajout d'un [dossier G2-A de revue](../qualification/M3_2_G2A_OPERATOR_REVIEW_PROPOSAL.md), de son JSON non exécutable, d'un validateur strict et de 24 tests adversariaux dans la CI. Le contrat spécifie seulement une future inspection du jeton courant, de PowerShell, de l'horloge, des présences de processus et des références GitHub publiques. Aucun bloc PowerShell ni script de collecte n'est livré. G2-A reste `NOT_ASSESSED/NOT_AUTHORIZED`. Toute commande réelle devra être publiée séparément et recevoir **autorisation spécifique sur son contenu exact** avec avertissement sur les interactions/élévation/effets. Aucun ACL, SQLite, sidecar, chemin ou worktree privé observé ; G2-B/G3 non autorisés. Requalification au SHA exact impérative avant fusion.


## 2026-10-19 — M3.2 : consolidation des autorités et blocages (preuve CI à qualifier)

À partir de `main=f9e6b18236fd70674849f6e956c7cff410dcef2c`, synthèse datée dans [M3_2_GATE_SNAPSHOT.md](M3_2_GATE_SNAPSHOT.md) et JSON compagnon. Les PR #77 à #82 ayant été fusionnées avec leurs CI exactes, le haut des documents de continuité devait distinguer les confirmations récentes des anciennes sections « qualification en attente ». Ajout d'un **contrôle de refus source-only** à 20 cas adversariaux couvrant la vérité historique 21/3/2, les cinq rôles non résolus, la politique SOLO, la PR #35, les issues #36/#38, l'absence de permission G2–G6, et le caractère compile-only/synthétique des CI. Ce contrôle *ne donne jamais une permission Windows ou runtime*. Nouvelle CI obligatoire au HEAD de la PR de consolidation ; pas de promotion implicite. `M32_SECURITY_PREFLIGHT_STOP` conservé, opérateur et SQLite hors périmètre.


## 2026-10-19 — PR #82 : séparation des lectures Core après veto source-only

CI initiale au HEAD `585d797fed1c811233535063e1c321a581dd7e77` : FAIL en étape `M3.2 fictional Tauri preview source-only policy` (`test_12_no_real_custody_or_automatic_migration_in_new_module`), parce que le module `m32_synthetic_preview.rs` contenait `fs::`. Les étapes suivantes, dont les tests des manifests Core, ont été SKIPPED. Correction **sans affaiblir le veto** : transfert des quatre tests Core dans `src-tauri/src/m32_generated_core_acl_tests.rs`, inclusion `#[cfg(test)]` dans le module M3.2, préservation de l'interdiction `fs::` dans la prévisualisation, et nouveau test Python `test_13` exigeant la séparation, les gardes CI/Windows, les lectures bornées et l'absence d'écriture/processus. Le fichier de manifest généré est seulement lu sur le runner. Aucun original opérateur.

Le nouveau commit doit avoir sa **propre** CI Windows `pull_request` terminale au SHA exact ; aucune preuve avant sa réussite. `M32_SECURITY_PREFLIGHT_STOP`, `CLI_CONFIG_RESOLUTION_NOT_TESTED`, `TAURI_RUNTIME_NOT_TESTED`, `OPERATOR_ACCEPTANCE_NOT_PERFORMED`, `REAL_G3_STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, G3–G6 réels `NOT_AUTHORIZED` demeurent inchangés.


## 2026-10-19 — M3.2 : contrôle des manifestes Core réellement générés par Tauri (PR en qualification)

Après fusion protégée de [PR #81](https://github.com/LaurentCOLL1/Fabulaxiom/pull/81), `main=5bbaf9cfb6412329106cfa4ac8e37e0a228089b6`. Cette tranche Windows CI seule lit les **vrais** artefacts `src-tauri/gen/schemas/acl-manifests.json` et `capabilities.json` générés dans le checkout éphémère par `tauri-build` (pas de copie du PC opérateur ; fichiers ignorés par Git). Quatre nouveaux tests Rust `#[cfg(test)]` contrôlent (1) l'identité de `default.json` avec le `default` généré et les familles `core:app` à `core:window`, (2) `Resolved::resolve` sur les **vrais manifests Core** générés, permissions sur `main` et refus de *toutes* les commandes Core obtenues sur la fenêtre fictive `m32-fiction`, (3) un contrefactuel wildcard **en mémoire seulement** qui permet volontairement l'accès, (4) le refus d'une permission Core inexistante. Lecture bornée au répertoire du checkout CI, refus des symlinks de destination, `CI=true` et `RUNNER_OS=Windows` obligatoires, aucun `TAURI_CONFIG` / `TAURI_DEV_HOST` hérité.

Le fichier généré `acl-manifests.json` est écrit par le build script dans `gen/schemas`, puis copié dans `OUT_DIR`, et Tauri codegen le lit pour résoudre les permissions. Cela donne une preuve plus forte que le manifest `m32fixture` inventé dans PR #81. **Limite maintenue :** les manifests proviennent de la génération locale du checkout CI et la résolution est recomposée via API publique ; elle n'inspecte toujours pas le champ privé `Context.runtime_authority`, ni `CLI --config`, ni l'autorité du WebView2 réel. Aucune signature indépendante ni validation opérateur. Nouvelle CI HEAD exact indispensable. `M32_SECURITY_PREFLIGHT_STOP`, `CLI_CONFIG_RESOLUTION_NOT_TESTED`, `TAURI_RUNTIME_NOT_TESTED`, `OPERATOR_ACCEPTANCE_NOT_PERFORMED`, `REAL_G3_STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, G3–G6 réels `NOT_AUTHORIZED` restent inchangés. PR #35 DRAFT, issues #36/#38 OPEN, aucune SQLite originale/backup/ACL/marker, migration 007, writer IPC, M3.3 ni release.


## 2026-10-19 — M3.2 : résolution native d'une capability jusqu'à l'ACL (fixtures Rust seulement, CI à qualifier)

Après fusion PR #80 : `main=4dca61266bf781cf74f37a3454d1bc58a75bd7a9`, CI Windows #39176860661 56/56 terminal SUCCESS. Nouvelle tranche limitée aux tests Rust de `m32_synthetic_preview.rs` et à une étape Windows : quatre tests `native_resolve_` invoquent l'API réelle `tauri::utils::acl::resolved::Resolved::resolve` sur une **manifestation intégralement inventée** `m32fixture:allow-consult` et une commande `plugin:m32fixture|consult`. Le test lit les octets du vrai `default.json` (label `main` et permission source `core:default`), puis **remplace la permission uniquement dans sa copie en mémoire**, jamais dans la configuration. Il construit ensuite `RuntimeAuthority` et teste la séparation `main`/ `m32-fiction`, un refus d'origine distante, les contre-exemples wildcard et le cumul de capabilities, les permissions introuvables et la priorité d'un deny même si son sélecteur de fenêtre est différent. Aucune ACL réelle `core:default` n'est résolue dans cette tranche.

Selon Tauri, `generate_context!` incorpore la configuration et l'ACL calculée mais `Context` n'offre pas de getter public stable sur son `runtime_authority`. Ne pas forcer les champs privés, ne pas utiliser `Builder::run`, de codegen opérateur, ni prétendre à l'inspection de l'ACL réellement générée. Exiger nouvelle CI `pull_request` HEAD exact : quatre tests natifs, marqueur `M32_NATIVE_ACL_MANIFEST_RESOLVE_TOY_PASS`, source-only PR #79, tests ACL PR #80, Chromium 29/29 x2, HTTP/IPC, frontend, Rust, G3 fictifs. `M32_SECURITY_PREFLIGHT_STOP`, `CLI_CONFIG_RESOLUTION_NOT_TESTED`, `TAURI_RUNTIME_NOT_TESTED`, `OPERATOR_ACCEPTANCE_NOT_PERFORMED`, `REAL_G3_STOP_UNAVAILABLE`, `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, G3–G6 réels `NOT_AUTHORIZED` restent inchangés. PR #35 DRAFT, issues #36/#38 OPEN, aucune SQLite v6/v7 opérateur, sauvegarde, ACL réelle, migration 007, writer, M3.3 ou release.


## 2026-10-19 — M3.2 : résolution de labels par le moteur ACL Tauri dans des tests Rust fictifs (qualification en attente)

Départ : `main=e61e938717cf47b416f397c09ede09df0684d4eb`, PR #79 protégée fusionnée, CI Windows #39174869386 55/55 SUCCESS. Tranche nouvelle : quatre tests Rust supplémentaires **unitaires** dans le module `m32_synthetic_preview.rs`, tous sous `#[cfg(test)]`. Ils construisent une commande **inventée** `plugin:app|version` via un `ResolvedCommand` synthétique, puis appellent le mécanisme réel `tauri::ipc::RuntimeAuthority::resolve_access` : `main` est autorisé par un sélecteur tiré des octets publics de `capabilities/default.json`, `m32-fiction` est refusé ; des contre-exemples `m32-*`, `*`, une liste `webviews` et une commande inconnue vérifient le matcher natif. Un nouveau job Rust cible exactement ces tests dans la CI, sans `Builder::build/run`, WebView2, CLI, fichier privé ni SQLite. Le modèle Python PR #79 reste en place.

**Limite explicite :** les tests emploient l'implémentation native du filtrage fenêtre/WebView mais construisent un `Resolved` artificiel — ce n'est **ni** la résolution complète des manifests `core:default`, **ni** l'autorité réellement générée/chargée par Fabulaxiom. La `devCsp` Tauri candidate demeure inactive. Nouvelle CI HEAD exact requise ; `M32_SECURITY_PREFLIGHT_STOP`, `CLI_CONFIG_RESOLUTION_NOT_TESTED`, `TAURI_RUNTIME_NOT_TESTED`, `OPERATOR_ACCEPTANCE_NOT_PERFORMED`, `REAL_G3_STOP_UNAVAILABLE`, historique 21/3/2 `PENDING_EXTERNAL_ATTESTATION`, prospective `NOT_STARTED`, G3–G6 `NOT_AUTHORIZED`, PR #35 OPEN/DRAFT, issues #36/#38 OPEN inchangés. Aucun original SQLite v6/v7, sauvegarde, manifest, ACL opérateur, marqueur, sidecar, migration 007, writer, M3.3 ou release.


## 2026-10-19 — M3.2 : matrice négative des permissions Tauri natives dans les sources (qualification en attente)

Après PR #78 protégée et [CI #39172462470](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39172462470) terminale 54/54, re-fetch `main=c8eafadeef909efdac1e29078a73ca32f3efdc3f`. Tranche indépendante **source-only, sans lancement** : modéliser les deux fichiers de configuration Tauri fictifs (preview 1420 et candidat statique inactif 14279), l'unique `default.json`, le `build.rs` Rust et le seul builder fictif `lib.rs`. Les sources référencent explicitement `default`, mais cette capability cible seulement `main`, jamais `m32-fiction`. `core:default` est **non vide** : Tauri lui associe neuf familles de permissions Core (app/event/image/menu/path/resources/tray/webview/window) sur les fenêtres correspondantes. Les nouvelles assertions doivent refuser nouveaux fichiers, windows/globs/webviews, capabilities en union, plugins/permissions supplémentaires, `remote`, `AppManifest`, handlers, plugins ou SQLite dans le builder fictif. Les essais adversariaux restent entièrement en mémoire et inspectent uniquement les sources Git publiques du runner Windows.

**Aucune preuve d'ACL à l'exécution** : le calcul source ne remplace ni le resolver natif Tauri, ni la CLI `--config`, ni WebView2/permissions système. Attention : les commandes Rust applicatives `invoke_handler` sont une frontière distincte de `core:default` ; le builder fictif actuel n'en installe aucune. Exiger CI nouvelle au HEAD exact et `M32_SECURITY_PREFLIGHT_STOP` inchangé. `CLI_CONFIG_RESOLUTION_NOT_TESTED`, `TAURI_RUNTIME_NOT_TESTED`, `OPERATOR_ACCEPTANCE_NOT_PERFORMED`, `REAL_G3_STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, G3–G6 réels `NOT_AUTHORIZED`, PR #35 OPEN/DRAFT, issues #36/#38 OPEN. Aucun lancement, SQLite, migration 007, writer, M3.3 ni release.


## 2026-10-19 — M3.2 : association serveur fictif ↔ processus enfant CI (qualification en attente)

Après fusion protégée [PR #77](https://github.com/LaurentCOLL1/Fabulaxiom/pull/77), re-fetch `main=b8eac5a77b90f815e9b8fc157e4d7560d928d63e`. Nouveau contrôle strictement *Windows CI et fictif* : le pilote Chromium doit attendre un signal IPC transmis par **son propre processus enfant Node** seulement après un `listen()` effectif sur `127.0.0.1:14279`, avec PID identique et nonce éphémère passé en mémoire via l'environnement du child (jamais diffusé par HTTP). La simple réponse 200 du port n'est plus suffisante. Le serveur refuse un démarrage sans canal IPC et nonce, l'identité du child incorrecte, le doublon ou le signal tardif. Une suite de 7 tests Node adversariaux contient un essai de collision sur **port éphémère fictif du runner**, sans toucher au port opérateur ; le navigateur doit confirmer `M32_CI_OWNED_STATIC_CHILD_READY_PASS`. Les 29 interactions Chromium sur chacun des modes, la CSP, l'identité Git/RAM, les tests Tauri compile-only et G3 restent requis.

Un signal IPC Node valide atteste seulement l'association immédiate parent/enfant **dans ce runner**, pas une identité OS signée, une provenance Git indépendante, une absence universelle de course réseau, ni l'identité d'un éventuel serveur opérateur. Aucun Tauri/WebView2 lancé, pas de source SQLite opérateur. `M32_SECURITY_PREFLIGHT_STOP`, `CLI_CONFIG_RESOLUTION_NOT_TESTED`, `TAURI_RUNTIME_NOT_TESTED`, `OPERATOR_ACCEPTANCE_NOT_PERFORMED`, `REAL_G3_STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, G3–G6 réels `NOT_AUTHORIZED`, PR #35 DRAFT et issues #36/#38 OPEN restent obligatoires. CI nouvelle au HEAD exact avant tout PASS/fusion.


## 2026-10-18 — M3.2: contrôles des en-têtes HTTP bruts du serveur fictif (PR À QUALIFIER)

Après la PR #76 protégée, `main=a1ada14ccffd99fbe38494d90fe9a81a0e0d724c`. Tranche limitée au serveur précompilé de fixtures CI : inspection obligatoire de `req.rawHeaders`, refus des doublons Host/Origin/Sec-Fetch-Site même si `req.headers` conserve une valeur normale, des métadonnées proxy et de toute incohérence entre en-têtes bruts et normalisés. Quatre nouveaux tests adversariaux Node (10 au total) et trois requêtes HTTP brutes TCP sur loopback doivent être exécutés en plus des quatre refus déjà qualifiés, des deux séries 29/29 Chromium, 129 frontend, 100 Rust et des préflights historiques. Node peut éliminer des Host dupliqués lors de la normalisation ; les octets bruts permettent de vérifier ce cas particulier sans prétendre résoudre toutes les ambiguïtés HTTP.

**AUCUNE preuve anticipée** : CI nouvelle au HEAD final impérative. Ceci ne crée aucun processus serveur opérateur, aucune authentification indépendante, aucun accès SQLite, aucun runtime Tauri/WebView2 et aucune promotion du candidat 14279. `M32_SECURITY_PREFLIGHT_STOP`, `CLI_CONFIG_RESOLUTION_NOT_TESTED`, `TAURI_RUNTIME_NOT_TESTED`, `OPERATOR_ACCEPTANCE_NOT_PERFORMED`, `REAL_G3_STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, G3–G6 réels `NOT_AUTHORIZED`, PR #35 DRAFT et issues #36/#38 OPEN restent inchangés.


## 2026-10-18 — M3.2 : refus Host/Origin du serveur HTTP fictif CI (en attente de CI)

Autorité re-fetch : `main=2fa18dc879305ec7be39691bdb34ac4275cc8f60` après fusion PR #75 (liaison aux blobs Git des sept fichiers fictifs). **Cette liaison au checkout ne constitue pas une attestation externe ou indépendante de provenance.** La tranche actuelle durcit seulement le serveur HTTP *fictif de GitHub Actions* : refus avant routage des requêtes dont le `Host` diffère de `127.0.0.1:14279`, `Origin` (s'il est présent) diffère de `http://127.0.0.1:14279`, en-têtes de forwarding/proxy, métadonnées `Sec-Fetch-Site` non locales ou cibles de requête absolues/scheme-relative. Six tests adversariaux Node et quatre requêtes HTTP négatives dans Chromium doivent confirmer ce refus. L'écoute reste uniquement sur 127.0.0.1, les ressources restent figées en RAM, la CSP stricte et 29/29 cas Chromium dans les deux modes restent requis.

**Limite** : un contrôle Host/Origin ne prouve ni la provenance de l'application, ni la validité des signatures, ni la résistance à un logiciel local malveillant, ni la sécurité native Tauri. La CI au HEAD nouveau doit être terminale avant tout PASS ou fusion. `M32_SECURITY_PREFLIGHT_STOP`, `TAURI_RUNTIME_NOT_TESTED`, `OPERATOR_ACCEPTANCE_NOT_PERFORMED`, `REAL_G3_STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, G3–G6 réels `NOT_AUTHORIZED`, PR #35 OPEN/DRAFT, issues #36/#38 OPEN. Pas de bases SQLite protégées, backup, ACL, marqueurs, migration 007, IPC writer, M3.3 ou release.

## 2026-10-18 — M3.2 : liaison des sept sources fictives aux blobs du checkout Git (PR EN COURS)

Autorité re-fetch avant la tranche : `main=415390a5e1c3ff29964234c2faf714c2b5c51331`, après PR #74 protégée et CI Windows terminale #39124457270 (51/51 étapes, 8/8 tests snapshot, 29/29 Chromium ×2, 129 tests frontend, 100 Rust). PR #35 OPEN/DRAFT et issues #36/#38 OPEN. Une comparaison des empreintes HTTP de la PR #74 prouve la cohérence des ressources dans le processus CI, **pas leur provenance authentifiée**.

Nouveau travail **strictement CI-only** : `tools/m32_ci_git_source_binding.cjs` vérifie que `git rev-parse HEAD` égale `GITHUB_SHA`, restreint exactement le jeu de **sept fichiers fictifs** autorisés, compare les octets locaux à ceux extraits par `git cat-file blob <HEAD>:<path>`, puis fige des copies de ces blobs pour le staging. Le contrôle accepte les octets bruts égaux au blob Git ou exclusivement l'expansion des fins de ligne LF→CRLF effectuée par un checkout Windows ; les dix tests adversariaux refusent toute autre modification, et le staging conserve les octets originaux du blob. Les fichiers de travail modifiés, SHA incohérents, entrées inattendues, imports normaux, symlinks, et changements d'identité pendant les lectures doivent échouer sans fallback. Un manifest SHA256 associe un nom de chemin, une taille, l'empreinte et le commit Git. **Il s'agit uniquement d'une correspondance avec les objets Git du runner, PAS d'une signature, d'une validation du serveur GitHub distant ou d'une attestation indépendante d'origine.** Un nouveau test Node exécute des cas adversariaux sur de minuscules dépôts fictifs sous `RUNNER_TEMP` ; la CI ne modifie pas le dépôt source ni les fichiers opérateur.

Une nouvelle CI complète Windows `pull_request` au HEAD exact doit qualifier cette PR. Même en cas de succès, `M32_SECURITY_PREFLIGHT_STOP`, `CLI_CONFIG_RESOLUTION_NOT_TESTED`, `TAURI_RUNTIME_NOT_TESTED`, `OPERATOR_ACCEPTANCE_NOT_PERFORMED`, source réelle G3 `STOP_UNAVAILABLE`, G3-G6 réels `NOT_AUTHORIZED`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`. Aucun lancement Tauri/WebView2, aucune base v6/v7 ou backup opérateur, aucun sidecar/ACL/marqueur, migration 007, writer, M3.3 ou release.

## 2026-10-18 — M3.2 : instantané RAM des octets fictifs CI, source uniquement, qualification EN ATTENTE

Autorité GitHub re-fetch initiale : `main=4a0ddd518af0459fa8f5e905eea6b09dd5e08d37` après PR #73 protégée fusionnée (CI Windows #39116241141 **50/50 SUCCESS**, 129 frontend, 100 Rust, 29 Chromium x2, 10 adversariaux candidat `devCsp`, deux contextes Tauri compilés sans lancement). Le candidat statique `tools/m32_static_tauri_candidate.json` reste **inactif** et refusé par le lanceur.

La nouvelle tranche améliore uniquement le **serveur HTTP fictif de GitHub Actions Windows** : `tools/m32_ci_static_byte_snapshot.cjs` inventorie de façon restrictive le résultat éphémère de compilation Vite, refuse les liens symboliques, les sorties supplémentaires, les fichiers vides et les scripts inline, puis fige **en RAM** les octets de chaque fichier HTML/JS/CSS autorisé avant tout `listen()`. Les réponses HTTP proviennent désormais exclusivement de cet instantané en mémoire, avec un en-tête `X-M32-Local-SHA256` recalculable. Des tests adversariaux sur **fixtures temporaires du runner** vérifient le refus des chemins normaux et des fichiers ajoutés, l'immuabilité des octets servis après modification/suppression des originaux de **test**, et la résistance à une modification des buffers retournés. Les vrais tests Chromium doivent aussi comparer les empreintes aux octets HTML et JS reçus, tout en conservant 29/29 dans chacun des deux modes.

**Portée limitée :** digest SHA-256 = identité **interne à une exécution CI**, non preuve de provenance authentifiée, de signature, d'intégrité de la chaîne de compilation, ou de protection générale contre toutes les courses du filesystem. Aucun fichier opérateur n'est inspecté, ouvert ou modifié ; le serveur statique fictif reste réservé à la CI et le lanceur Tauri n'est pas touché. Toute nouvelle CI doit qualifier le HEAD exact ; aucun PASS anticipé. La variante Tauri reste interdite au lancement : `M32_SECURITY_PREFLIGHT_STOP`, `CLI_CONFIG_RESOLUTION_NOT_TESTED`, `TAURI_RUNTIME_NOT_TESTED`, `OPERATOR_ACCEPTANCE_NOT_PERFORMED`, G3 réel `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, G3-G6 réels `NOT_AUTHORIZED`, PR #35 OPEN/DRAFT, issues #36/#38 OPEN. Aucun original SQLite v6/v7, backup, sidecar, marqueur, ACL, migration 007, writer IPC, M3.3 ou release.

## 2026-10-18 — M3.2 : candidate Tauri statique CSP stricte, uniquement compilation CI, AUCUN lancement

`main=5cbc42e02090bb49257a9c172c9481dd5662e20c` re-fetch à l'ouverture de cette tranche, après PR #72 fusionnée avec CI Windows `pull_request` #39111458766 `49/49 SUCCESS`, 129 frontend, 100 Rust et **29/29 Chromium sur chacun de deux laboratoires** : Vite fictif de développement et bundle fictif précompilé avec CSP sans `unsafe-inline`. La CI a confirmé `M32_CI_PRECOMPILED_STRICT_CSP_BROWSER_PASS` tout en maintenant `M32_SECURITY_PREFLIGHT_STOP`.

La nouvelle branche n'active **aucune configuration Tauri**. Un document de test `tools/m32_static_tauri_candidate.json` (en dehors de `src-tauri`) décrit un futur candidat fictif avec identité `com.fabulaxiom.m32synthetic.preview`, fenêtre `m32-fiction`, devUrl `http://127.0.0.1:14279/m32-browser-lab.html`, hooks/ressources hérités supprimés (RFC 7396), capability explicitement `["default"]` ciblant uniquement la fenêtre `main` et `devCsp` strict **identique à la CSP HTTP effectivement qualifiée du serveur CI**. Aucun `devCsp` n'est ajouté au véritable overlay `src-tauri/tauri.m32-synthetic-preview.conf.json`, dont l'URL reste à `127.0.0.1:1420`. Le validateur de lancement Rust `validate_launch()` doit donc **toujours refuser** le candidat `14279` ; cette distinction est un contrôle de sécurité, pas un défaut à contourner.

Une suite Python compare exactement les directives CSP au serveur statique CI, rejette les dérives (URLs externes/ports/host, `unsafe-inline`, commandes héritées, capabilities vides/wildcard, fenêtre `main`, modifications du bundle). Un test Rust `generate_context!(test=true)` **ignoré dans la suite normale** inspecte la configuration candidate chargée sous `TAURI_CONFIG` en runner Windows CI sans `Builder::run`, ni WebView2, ni SQLite. Ce test doit vérifier la présence effective de `dev_csp` dans le contexte compilé et le refus de cette URL par le lanceur existant. Le premier contexte Tauri historique reste testé séparément ; une nouvelle CI complète au HEAD final est obligatoire.

**Non prouvé / strictement interdit** : CLI `--config` réelle, CSP injectée dans WebView2, permissions noyau, fonctionnement de Tauri avec ce bundle, processus/ports opérateur, source originale G3 `STOP_UNAVAILABLE`, G3–G6 réels `NOT_AUTHORIZED`, migration 007, base v6/v7, backup, ACL, manifeste, sidecar, marqueur, writer IPC, M3.3 ou release. `TAURI_RUNTIME_NOT_TESTED`, `OPERATOR_ACCEPTANCE_NOT_PERFORMED`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 OPEN/DRAFT, issues #36/#38 OPEN.

## 2026-10-18 — M3.2 : bundle fictif précompilé et CSP sans inline (CI uniquement ; qualification en attente)

Autorité re-fetch : `main=c8fe034040af157f2101c1dd88093267637f4d75`. La PR #71 a été protégée fusionnée après CI `pull_request` #39109033373 au HEAD exact `d6bb950b12c3a672e8a32e258ce347f388e72d3f` (49/49 Windows SUCCESS ; 129 frontend, 29 Chromium inventé, 100 Rust, CSP HTTP expérimentale et refus de connexion distante). Cette CSP Vite *dev* comportait encore `unsafe-inline` et **ne constitue pas un `devCsp` Tauri**.

Une tranche indépendante ajoute **seulement sur GitHub Actions Windows** la compilation Vite des sept fichiers fictifs du staging jetable, sans `index.html` normal, et un serveur Node HTTP test-only écoutant exclusivement `127.0.0.1:14279`, sans exploration de fichiers ni fallback. Son allowlist refuse toutes les routes hormis `/m32-browser-lab.html` et les fichiers JS/CSS précompilés générés dans le répertoire neuf. La réponse HTML/JS/CSS emploie une CSP stricte **sans `unsafe-inline` ni `unsafe-eval`** (`script-src 'self'`, `style-src 'self'`, `connect-src 'none'`) ; le bundle doit ne contenir ni `<script>` inline ni référence à l'application normale. Les 29 scénarios Chromium fictifs sont rejoués à l'identique une seconde fois avec ce bundle statique ; des refus réseau externe et d'exécution inline sont exigés. Le premier scénario Vite/HMR CI de PR #71 est conservé : pas de régression cachée.

Une nouvelle CI Windows au HEAD exact est obligatoire ; **aucun PASS anticipé**. Ce test peut démarrer les deux *serveurs de fixtures jetables* de GitHub Actions, sans lancer de Tauri/WebView2, ni utiliser une base, des sauvegardes ou chemins privés de l'opérateur. Il ne valide pas la `devCsp` native Tauri, le merge CLI `--config`, les IPC/capabilities runtime ou les ports/processus du PC opérateur. `M32_SECURITY_PREFLIGHT_STOP`, `CLI_CONFIG_RESOLUTION_NOT_TESTED`, `TAURI_RUNTIME_NOT_TESTED`, `OPERATOR_ACCEPTANCE_NOT_PERFORMED`, `REAL_G3_STOP_UNAVAILABLE`. Historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, G3–G6 réels `NOT_AUTHORIZED`, PR #35 OPEN/DRAFT, issues #36/#38 OPEN, pas M3.3/release.

## 2026-10-18 — M3.2 : CSP/connexion HMR du laboratoire fictif CI — PR à qualifier

Autorité re-fetch avant branche : `main=0413fd838a27e0643e5621c3391b4ba708f7e62f`, PR #70 protégée fusionnée après CI exacte Windows #39106878684 (49/49 SUCCESS ; 7 fichiers fictifs, 6 routes normales refusées, 29/29 Chromium). Le laboratoire navigateur jetable dispose maintenant d'un Vite séparé, mais sa configuration Tauri fictive reste hors runtime et sans `devCsp` autorisée.

La nouvelle tranche **test-only** configure une CSP HTTP sur le **Vite isolé de GitHub Actions uniquement** : `default-src 'none'`, ressources scripts/styles du même site, connexions à l'origine fictive et WebSocket exact `ws://127.0.0.1:14279`, refus d'object/frame/base/form/worker et en-têtes `nosniff`/`no-referrer`. Le rafraîchissement React injecte en développement du script inline : la politique expérimentale contient donc **`script-src 'unsafe-inline'`**, concession explicitement NON satisfaisante comme politique de production/XSS. Un nouveau test Chromium contrôle les en-têtes reçus puis prouve un refus `connect-src` d'une tentative vers `https://example.invalid` sans requête réseau distante effective. L'ancienne CI 29/29 doit rester réussie.

Ceci n'établit PAS `devCsp` Tauri, ni la CSP réellement appliquée par WebView2, ni la résolution `--config` de la CLI Tauri. Les risques détectés sur `vite.config.ts` **normal** (racine partagée, `TAURI_DEV_HOST` wildcard) restent et `M32_SECURITY_PREFLIGHT_STOP` doit demeurer. Une CI nouvelle au HEAD exact est obligatoire ; aucun PASS anticipé. `TAURI_RUNTIME_NOT_TESTED`, `OPERATOR_ACCEPTANCE_NOT_PERFORMED`, réel G3 `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, G3–G6 réels non autorisés, PR #35 OPEN/DRAFT, issues #36/#38 OPEN. Aucune donnée, base, sauvegarde, manifeste, ACL, marqueur, 007, writer, M3.3 ou release.

## 2026-10-18 — M3.2 : racine Vite fictive éphémère exclusivement sur Windows CI (PR à qualifier)

Autorité GitHub relue : `main=4741c6b3a48185d14a4a988bfda2f25bef9266dd` après fusion protégée de PR #69. Le diagnostic de cette PR reste correct : le Vite *normal* partage `index.html` et `m32-browser-lab.html`, accepte une valeur `TAURI_DEV_HOST` dangereuse et la variante Tauri fictive conserve une CSP non configurée. Le statut **`M32_SECURITY_PREFLIGHT_STOP` ne peut donc être retiré.**

Une PR technique isolée propose de faire exécuter les **29 tests Chromium fictifs existants**, sur le runner Windows jetable, avec `vite.m32-ci-isolated.config.mts` et un staging inédit `.m32-fixture-only-*` contenant seulement sept fichiers React/HTML/CSS fictifs nommés explicitement. Le copieur est désactivé hors de `CI=true` et `RUNNER_OS=Windows`, refuse les imports hors graphe déclaré, les symlinks et les variables `TAURI_DEV_HOST` / `__VITE_ADDITIONAL_SERVER_ALLOWED_HOSTS`. Le Vite spécifique fixe `host=127.0.0.1`, `strictPort=true`, `appType=mpa`, `publicDir=false`, `fs.strict` et `fs.allow` restreints au staging et au dossier de dépendances. Les tests HTTP doivent démontrer le refus des routes normales `/`, `/index.html`, `/src/App.tsx`, `/src/main.tsx` et des chemins `/@fs/` hors staging, puis confirmer les 29 interactions Chromium sur la page fictive.

**Limites strictes** : ces tests démarrent uniquement le serveur Vite de fixtures dans GitHub Actions, comme les scénarios Chromium déjà qualifiés, sans `tauri dev`, `cargo run`, Tauri ni WebView2. Cette preuve **ne remplace pas** l'isolation du serveur futur sur le PC opérateur. La CSP Tauri `null`, la fusion réelle `--config` CLI, les commandes natives, la navigation et l'occupation des ports Windows sont encore non testées ; le dossier de staging n'est jamais une source opérateur. Nouveau HEAD -> CI Windows propre requise, aucun PASS anticipé.

`TAURI_RUNTIME_NOT_TESTED`, `OPERATOR_ACCEPTANCE_NOT_PERFORMED`, original G3 `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, réel G3–G6 `NOT_AUTHORIZED`; PR #35 OPEN/DRAFT et issues #36/#38 OPEN. Aucune base v6/v7, copie, backup, sidecar, ACL, manifeste, marqueur, migration 007, writer, M3.3 ou release.

## 2026-10-18 — M3.2 : préflight Vite/CSP fail-closed proposé, AUCUN lancement

Autorité re-fetch : `main=0903739b3ffc242d6d98032dc154cebcca37032d` après PR #68 documentaire protégée fusionnée, CI Windows #39092434467 48/48 SUCCESS sur HEAD exact `d8b15904aa709290835040c696ef92e34d73a9c8`. PR #35 toujours OPEN/DRAFT et issues #36/#38 OPEN. Nouveau périmètre de test **sans lancement** : `tools/m32_vite_csp_nonlaunch_audit.mjs` exploite l'API Vite 8 `resolveConfig` (aucun `createServer`/`listen`) sur le vrai `vite.config.ts` sous trois environnements CI jetables, et confirme que `TAURI_DEV_HOST=0.0.0.0` pourrait élargir l'écoute tandis que `host=false` n'établit pas la correspondance stricte à `127.0.0.1`. Les refus de ports/HMR incohérents sont adversariaux. L'overlay Tauri M3.2 hérite encore de `app.security.csp=null` sans `devCsp`. Le même projet Vite contient `index.html` (entrée application normale) et `m32-browser-lab.html` (entrée fictive). **La présence simultanée des deux pages dans la racine servie ne prouve pas une isolation complète**, même si la WebView est configurée pour charger seulement la page fictive.

Le script doit donc réussir ses contrôles de diagnostic tout en déclarant explicitement `M32_SECURITY_PREFLIGHT_STOP`. Il ne doit JAMAIS être interprété comme `TAURI_RUNTIME_PASS` ou permission de démarrer Tauri/Vite. Nouvelle PR et CI Windows au HEAD exact requises avant qualification. Aucune mutation de `vite.config.ts`, `App.tsx`, permissions Tauri, bases SQLite opérateur ou sources. `CLI_CONFIG_RESOLUTION_NOT_TESTED`, `TAURI_RUNTIME_NOT_TESTED`, `OPERATOR_ACCEPTANCE_NOT_PERFORMED`, original G3 `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, G3–G6 réels NOT_AUTHORIZED, pas M3.3 ni release.

## 2026-10-18 — M3.2 : patch RFC 7396 des hooks/ressources fictifs qualifié et fusionné

**Autorité post-fusion re-fetch : `main=1735fc0edf0e457f7b41a06a99a6aa19fd22591f`.** PR #67 protégée fusionnée après CI Windows `pull_request` #39091761744 terminée **48/48 SUCCESS**, au HEAD exact `b711212126e8e72034ed0d8c993480cbc527a969` ; contrôle GitHub Actions obligatoire `Windows frontend and Rust checks` (intégration 15368) PASS, frontend 129/129, Chromium fictif 29/29, Rust général 100/100, sources Tauri + capacités 12/12 et tous les garde-fous G3 synthétiques réussis. La vérification native du contexte `generate_context!(test=true)` a produit `M32_NATIVE_OVERLAY_CONTEXT_PASS` sans lancement Tauri/WebView2. Le diff qualifié est restreint à huit fichiers overlay/tests/doc, sans dépendances ou routes applicatives modifiées.

**Ce qui a été prouvé** : les valeurs `null` de l'overlay M3.2 sont des suppressions RFC 7396 de `beforeDevCommand`, `beforeBuildCommand`, `frontendDist`, qui étaient hérités de l'application normale. Les tests source vérifient le patch brut et les réintroductions adversariales ; en soumettant précisément cet overlay brut sous `TAURI_CONFIG` dans la CI jetable, le générateur natif Tauri confirme que `frontend_dist=None` dans le contexte compilé. Les hooks sont forcés à `None` par le codegen quelle que soit la configuration : seule la vérification du patch brut et du modèle source borne leur absence. **Historique négatif préservé** : CI #39091221081 et #39091333950 échouées car le pilote avait transmis un JSON déjà fusionné sans marqueurs `null`, permettant de récupérer `../dist`. Aucune ancienne CI n'a été réutilisée.

**Restent STOP/non testés :** fusion réelle de la CLI `--config`, capacités noyau effectives au runtime, CSP `null`, `TAURI_DEV_HOST`, navigation/ports WebView2 et toute acceptation opérateur. `TAURI_RUNTIME_NOT_TESTED`, `OPERATOR_ACCEPTANCE_NOT_PERFORMED` et `REAL_G3_STOP_UNAVAILABLE`. Historiquement `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, réel G3–G6 `NOT_AUTHORIZED`, PR #35 OPEN/DRAFT, issues #36/#38 OPEN. Aucune base, copie, ACL, backup, sidecar, marqueur ou migration 007, writer, M3.3 ou release.

## 2026-10-18 — M3.2 : réduction des héritages frontend de la variante fictive (qualification EN ATTENTE)

Autorité re-fetch avant branche : `main=334482c912a0e70db4108e326616d66af96e885e` après PR #66 documentaire qualifiée et fusionnée. La CLI Tauri 2.12.1 documentée ne propose pas de commande `inspect` exportant l'intégralité du JSON `--config` résolu **sans** lancer `dev`/`build` ; cette voie reste `CLI_CONFIG_RESOLUTION_NOT_TESTED`, sans exécution spéculative d'une CLI susceptible de démarrer des processus. L'overlay M3.2 conserve l'identité et URL de fixture mais déclare désormais `beforeDevCommand: null`, `beforeBuildCommand: null`, `frontendDist: null`, en complément de `capabilities: ["default"]` réservé à la fenêtre normale `main`. Avec JSON Merge Patch RFC 7396, ces valeurs nulles retirent les trois propriétés héritées ; `default.json` ne cible toujours pas `m32-fiction`.

Les tests Python valident explicitement la suppression RFC 7396, son effet sur les hooks/dist et des mutations adversariales. Le test Rust vérifie les marqueurs de suppression `null` de l'overlay fictif **brut fourni sous `TAURI_CONFIG`**, puis vérifie `frontend_dist=None` dans le contexte compilé par le merge interne de Tauri. La première CI #39091221081 a justement échoué car l'ancien pilote transmettait un JSON déjà fusionné sans marqueur `null` : Tauri a réintroduit le `frontendDist` de la base. Cet échec est conservé et une nouvelle CI au HEAD correctif reste obligatoire. **La génération du contexte force elle-même les champs de hooks à `None`, même si l'entrée en contenait : ces deux champs ne constituent PAS une preuve d'absence d'héritage à partir du seul contexte compilé.** **Nouveau HEAD, CI Windows propre exigée : aucun PASS anticipé.** `TAURI_DEV_HOST`, la CSP héritée `null`, les droits natifs Tauri, les chargements et navigations WebView2 restent des sujets séparés non qualifiés. Un futur serveur Vite fictif exigerait une autorisation et un démarrage explicite, pas un hook hérité. Ni `tauri dev`, `cargo run`, ni backend/operator SQLite, sauvegarde, ACL, sidecar, marqueur ou migration ne sont autorisés.

Gates : historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, G3 original `STOP_UNAVAILABLE`, G3-G6 réels `NOT_AUTHORIZED`, PR #35 OPEN/DRAFT, #36/#38 OPEN. `TAURI_RUNTIME_NOT_TESTED` et `OPERATOR_ACCEPTANCE_NOT_PERFORMED`. Pas de M3.3/release.

## 2026-10-18 — M3.2 : capacités explicites + contexte Tauri compilé, qualifiés et fusionnés (runtime NON testé)

**Autorité GitHub re-fetched : `main=1f61eaff968b33038a3513d8b5d5dbc82f3de8a1`**, après fusion protégée de la PR #65, HEAD exact `960e3806de5ead8230c1f86f81b90b7d0096019e`. CI Windows `pull_request` #39074890614 terminale **48/48 SUCCESS**, contrôle obligatoire `Windows frontend and Rust checks` de GitHub Actions app `15368`, 129/129 frontend, 29/29 Chromium synthétique, 100/100 Rust général, 10/10 tests capabilities source-only, 12/12 source Tauri. Le nouveau Rust `compiled_fictional_context_no_runtime` **PASS** et le marqueur `M32_COMPILED_CONTEXT_PASS: true` est présent dans les journaux. Un ancien HEAD de la PR #65 avait échoué `E0283` (type runtime de Context non explicite) ; cet échec est conservé comme preuve historique et **n'a pas été utilisé** pour la fusion. PR #64 précédente (allowlist `["default"]` spécifique à la fenêtre `main`) avait déjà été qualifiée/fusionnée au checkpoint `67b223af041436b720e68ce1cf06fad0da9ca920`.

**Limite exacte :** le test natif compile `tauri::generate_context!(test=true)` avec un JSON fictif déjà fusionné par notre modèle en mémoire, puis lit sa configuration ; aucun appel `Builder::run`, `tauri dev`, WebView2 ou base opérateur. Ce n'est PAS une qualification du merge `--config` réel de la CLI Tauri, de l'autorité ACL native au runtime, des permissions noyau, de la navigation WebView, du CSP hérité ni de `TAURI_DEV_HOST`. États actuels : `SOURCE_ONLY_PASS`, `WINDOWS_CI_PASS`, `CHROMIUM_SYNTHETIC_PASS`, `TAURI_COMPILE_PASS` et `COMPILED_CONTEXT_PASS` (borné) ; `TAURI_RUNTIME_NOT_TESTED`, `OPERATOR_ACCEPTANCE_NOT_PERFORMED`, `REAL_G3_STOP_UNAVAILABLE`.

**Gouvernance inchangée** : historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, réel G3/G4/G5/G6 `NOT_AUTHORIZED`, PR #35 OPEN/DRAFT et issues #36/#38 ouvertes. Ni original SQLite v6/v7, sauvegarde, sidecar, manifeste, ACL, marqueur d'activation, migration 007, writer IPC, lancement interactif, M3.3 ni release. Voir issue #38 pour les preuves de fusion après qualification.

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
