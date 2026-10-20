# M3.2 — Historique condensé des qualifications (référence, pas CI réutilisable)

Les détails exhaustifs restent dans [STATE.md](STATE.md) et les PR GitHub. **Toujours re-fetch les HEAD ; CI d'un commit A non transférable à B.**

| Tranche | Avancée fusionnée | Preuve et limite |
| --- | --- | --- |
| [#79](https://github.com/LaurentCOLL1/Fabulaxiom/pull/79) | Modèle source-only des capabilities Tauri | fenêtre fictive `m32-fiction` distincte de `main`, sans ACL runtime |
| [#80](https://github.com/LaurentCOLL1/Fabulaxiom/pull/80) | Matcher `RuntimeAuthority` natif sur ACL fictive | aucune fenêtre opérateur |
| [#81](https://github.com/LaurentCOLL1/Fabulaxiom/pull/81) | `Resolved::resolve` natif sur manifeste inventé | pas la vraie ACL Core |
| [#82](https://github.com/LaurentCOLL1/Fabulaxiom/pull/82) | Manifestes Core produits par `tauri-build` en CI | aucune exécution Tauri/WebView2 |
| [#83](https://github.com/LaurentCOLL1/Fabulaxiom/pull/83) | Registre d'autorité historique 21/3/2 et tests de refus | statut documentaire |
| [#84](https://github.com/LaurentCOLL1/Fabulaxiom/pull/84) | Proposition inerte G2-A, tests de consentement | aucune commande fournie |
| [#85](https://github.com/LaurentCOLL1/Fabulaxiom/pull/85) | Bloc PowerShell exact en Markdown, parser AST uniquement | exécuté manuellement ensuite : STOP PROCESS_NAMES |
| [#86](https://github.com/LaurentCOLL1/Fabulaxiom/pull/86) | Correction de détection WebView2 rattaché à SearchHost | CI source-only PASS ; exécution opérateur ultérieure : STOP `WEBVIEW2_PARENTAGE`, cause fine inconnue |
| [#87](https://github.com/LaurentCOLL1/Fabulaxiom/pull/87) | Handoff de reprise versionné et obligation CI de le rafraîchir pour les PR matérielles | CI PR #39271702661 et `main` #39273165266 SUCCESS ; les exécutions G2-A ont été documentées ensuite |
| [#88](https://github.com/LaurentCOLL1/Fabulaxiom/pull/88) | Historique du STOP corrigé et hypothèse PID 0 documentés | CI PR #39303355912 au HEAD `0b7c55f3...` SUCCESS, fusion protégée ; G2-A reste STOP |
| [#89](https://github.com/LaurentCOLL1/Fabulaxiom/pull/89) | Nouveau candidat Markdown PID 0, 22 fixtures, 11 tests exact-source, AST parse-only | CI PR #39339365546 SUCCESS, 68 étapes au HEAD `e188a980...`, fusion protégée `main=f14e5991d34350682647ef6f0bd67b1d2055f41a`; qualification source-only ; exécution opérateur autorisée et effectuée **après fusion**, résultat PASS des métadonnées seulement |

**20 octobre 2026 — incrément produit fictif (nouvelle PR) :** PR #97 fusionnée à `main=a839953f73f17379aa7c5ccde69d807b5b99a2f6`, CI PR #39426793283 et push #39428345389 SUCCESS. Les treize tests Vitest proposés couvrent l'édition directe des assertions de chronologie sur fixture avec graphe acyclique, versions inconnues, conservation par supersession et révocation. Accessible seulement dans le laboratoire navigateur ; UI de production / SQLite et acceptation opérateur non livrées, G2B–G6 STOP.

**20 octobre 2026 — revue complète de roadmap V1 (nouvelle PR documentaire) :** PR #96 fusionnée, main e35b7c92441c517d4f0fcacb829711c4d1e9da97, CI exacte #39414915855 (73/73) et push main #39416303498 SUCCESS. M3.1 bien normalisée PR #34 ; M3.2 seulement en cours, PR #35 DRAFT, fonctionnalités CRUD GUI et acceptation réelle manquantes. Index et matrice transversale des cinq documents roadmap ajoutés, 9 tests CI source-only, aucune promotion G2/G3.

**20 octobre 2026 — étape expérimentale sur RAM partagée (PR nouvelle) :** PR #95 fusionnée sous règles sur `main=a8578b8e128af2264e85a7341a96e13d0e086b23` ; CI PR #39406700987 SUCCESS (72/72) au SHA exact. Douze tests Python utilisant deux connexions à la même RAM imaginaire démontrent que `query_only` et `total_changes` du lecteur ne bloquent ni ne recensent les writes de l'autre connexion. Pas de code de production ni procédure opérateur, G2-B/G3 toujours STOP.

**20 octobre 2026 — Rust RAM-only candidate (PR nouvelle à qualifier) :** PR #94 fusionnée sur main 632e6d6d985affa6989bb220ddec99911e6ba1e6 après CI #39394068343 SUCCESS (71 étapes). Prototype purement fictif empruntant une connexion SQLite déjà ouverte en RAM sous feature opt-in TEST-ONLY, 13 scénarios de lecture sans migration et refus query_only/ATTACH/dérive. Aucune application modifiée au runtime, G3 réel STOP.

**20 octobre 2026 — nouvelle tranche source-only :** PR #93 fusionnée sur main 15c91039243206dc61190fec5668f32a87f3faf0, CI PR #39391766661 SUCCESS (70 étapes). Inventaire textuel élargi des 25 modules Rust Tauri : baseline des 20 fichiers avec marqueurs SQLite, 18 tests adversariaux pour détecter les nouveaux sites. Aucune analyse Rust exhaustive ni preuve d'absence d'écrivain. PR à qualifier sur nouveau SHA, sans commande opérateur.

**20 octobre 2026 — source-only :** PR #92 fusionnée sur main `8e358d61b7f5438b893a416aa8f82d884569c5da`, CI PR #39388988034 terminale SUCCESS au HEAD `cb5e1eaeaaf64bd684be6a80c9cc3b85fc56492b` (70 étapes). Ajout dans une nouvelle tranche de `M3_2_GATE_DECISION_CURRENT.md` pour distinguer le résultat G2-A du 20 octobre du snapshot G2 entier daté du 19. Toutes les autorisations G2B–G6 restent fermées.

**20 octobre 2026 — garde-fou nouveaux points d'entrée G3, source-only (nouvelle PR) :** après PR #91 protégée fusionnée (main=fb4625450439ecf236cc9065f434eda002f71533, CI exact-head #39376628743 SUCCESS), inventaire textuel de six fonctions SQLite Rust actuelles et 18 tests de refus. Les tests détectent les dérives des chemins existants, mais ne sont ni un parseur Rust complet ni une autorisation de capture réelle. G2-A reste PASS métadonnées ; absence d'écrivain non prouvée, G3 STOP.

**20 octobre 2026 — analyse writer source-only (nouvelle PR à qualifier) :** revue de `src-tauri/src/database.rs`, `lib.rs`, `backup.rs` et des documents primaires SQLite/Microsoft ; ajout d'une matrice de preuve négative sans commande opérateur, avec tests fictifs. Aucune promotion G2-B/G3, source/owner/writer toujours non attestés. La fusion précédente [#90](https://github.com/LaurentCOLL1/Fabulaxiom/pull/90) a gardé le PASS G2-A borné, CI #39342493152 SUCCESS au HEAD exact ; `main=45ce1511aa616fce9664dfc08cea39f290d2273d` après fusion.

**Observation opérateur 2026-10-20 01:31:24 +02:00 :** bloc PID 0 de PR #89, autorisation distincte consommée, sortie `G2A_LOCAL_METADATA: PASS`, token MEDIUM, aucun Fabulaxiom/Ollama détecté, 6 WebView2 descendants SearchHost (`OBSERVED_METADATA_ONLY`), propriétaire du binaire NON authentifié, écrivain SQLite NON exclu ; `G2B_G2C_G2D_G3_G4_G5_G6: NOT_AUTHORIZED`, `TAURI_RUNTIME: NOT_TESTED`. **Cette déclaration de l'opérateur n'est pas une attestation indépendante et ne confirme pas la cause du STOP précédent.** Aucune réexécution implicite autorisée.

**Observation opérateur 2026-10-19, après PR #86 et autorisation explicite spécifique :** bloc exact collé manuellement, sortie assainie `G2A_LOCAL_METADATA: STOP`, `STOP_STAGE: WEBVIEW2_PARENTAGE`, `STOP_REASON: UNEXPECTED_OR_UNSAFE`, `G2B_G2C_G2D_G3_G4_G5_G6: NOT_AUTHORIZED`, `TAURI_RUNTIME: NOT_TESTED`. Sous-cause inconnue, aucune attribution causale certaine. Déclaration de l'opérateur, pas une preuve d'absence d'écrivain SQLite ; aucun autre essai local autorisé. Cette actualisation figure dans la PR #88, initialement DRAFT en attente de nouvelle CI exact-head.

**Travail source-only du 20 octobre (PR nouvelle à qualifier) :** nouveau fichier exact `docs/qualification/M3_2_G2A_PID_ZERO_CANDIDATE_REVIEW.md` ; ancien bloc PR #86 non modifié. Une exception étroite pour un unique PID 0 `System Idle Process` évite le rejet systématique de l'entrée Idle, sans autoriser ce PID comme ancêtre ; les tests fictifs et la CI AST doivent être qualifiés avant toute revue humaine. Ce travail ne fournit aucun PASS Windows.

L'échec du premier G2-A ne doit pas être « corrigé » en arrêtant la recherche Windows. Les relations parent/enfant changent avec le temps ; les PID visibles dans une ancienne capture ne sont pas une liste blanche. Microsoft note que les PID peuvent être réutilisés et que les horodatages aident à détecter les relations incohérentes.

Les blocages externes (issues #36/#38) demeurent. Les détails techniques de la préparation du snapshot SQLite et du contrôle d'ACL ne sont **pas** requalifiés par ce registre condensé.
