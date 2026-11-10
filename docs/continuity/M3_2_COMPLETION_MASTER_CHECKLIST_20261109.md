# Fabulaxiom — Liste exhaustive de travail restant pour accepter M3.2

**Référence vivante initiale : 9 novembre 2026** · version 1.2 · **104 tâches identifiées : 2 clôturées (M32-001 et M32-002), 102 encore ouvertes**, sans autre déclaration de PASS.

**Source d'autorité vivante, vérifiée au 10/11 :** protected `main=da5c64761159fd8fcc22ba541da04a7c54be6691`, PR [#331](https://github.com/LaurentCOLL1/Fabulaxiom/pull/331) **FUSIONNÉE** sous Protect main strict `bypass_actors=[]` ; source Windows [#42751838279](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/42751838279) SUCCESS SHA exact `fb523abbc05b636d98fd93240872882f4ee57f61` et postmain indépendante [#42754285833](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/42754285833) attempt 1 completed/SUCCESS SHA exact `da5c64761159fd8fcc22ba541da04a7c54be6691` (job #129624924853, 86 succès + 1 étape PR-only ignorée). **M32-001/002 closes, 102 obligations ouvertes ; R1–R9/P4 réel restent STOP.**

**Repère historique conservé (09/11) :** #330 documentaire fusionnée, source `4e04408323af42507fbaf1ef2d474faede503328`, CI Windows #42696145161 SUCCESS, main précédent `bef699511ff18e987a4858c797fde7aa88dfc59b`, postmain #42699790716 SUCCESS ; #331 était alors DRAFT avec source antérieure #42674870251 SUCCESS au SHA `a0a6c3e72656d6b626a50030cf4c63e09f2a4b05`. Cet état est **historique et ne doit plus être présenté comme état courant**.

**Checkpoint du 10 novembre 2026 (nouveau main) :** PR #331 P3n réconciliée, puis FUSIONNÉE sous Protect main, SHA exact source `fb523abbc05b636d98fd93240872882f4ee57f61`, CI Windows #42751838279 attempt 1 completed/SUCCESS, diff 10 chemins, reviews=[] threads=[], squash avec `expected_head_sha`, protected `main=da5c64761159fd8fcc22ba541da04a7c54be6691`. La CI push postmain #42754285833 était **completed/SUCCESS**, attempt 1, SHA exact `da5c64761159fd8fcc22ba541da04a7c54be6691`, job Windows terminé sans échec ; #38 append-only à actualiser. La clôture **M32-002 concerne seulement la réconciliation de #331**, pas R1–R9, P4 réel ni l'acceptation globale. **2 tâches clôturées, 102 ouvertes sur 104** ; ~45 % reste estimation indépendante. Issue #38 historique append-only #6758458130 documente la réconciliation avant fusion ; ajouter séparément la qualification postmain.

**État :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, estimation d'ingénierie **~45 % (40–50 %)**, **PAS** taux de fonctionnalités utilisables sur des données opérateur. Writer réel et **R1–R9 `NOT_PROVEN`**, P4 réel STOP, G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE, G4–G6 NON AUTORISÉS, chaîne historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, baseline prospective `NOT_STARTED`. Atomicité main/WAL/SHM et ABA invisible NOT PROVEN ; glib #160 OPEN_NOT_REMEDIATED.

**Décision maintenue : `PRODUCT_FIRST_PARALLEL_SAFETY`** — développer le produit **uniquement sur fixtures fictives isolées** en parallèle avec les preuves de sûreté. **Informer l'opérateur AVANT de changer de stratégie.** P1 mono-propriétaire choisi ; autres processus du même utilisateur SID considérés coopératifs (pas une preuve de protection face à un même-SID malveillant). Aucun autre compte utilisateur demandé ; Windows Hello pourra confirmer des actes sensibles après autorisation spécifique.

**Légende :** chaque case `[ ]` signifie **obligation encore ouverte pour l'acceptation réelle**, même si certaines sous-preuves *fixture-only* ont déjà PASS. Ne cocher qu'avec une preuve datée, son SHA et sa portée, après décision humaine lorsqu'elle est requise. Ne pas considérer toutes les tâches comme des PR indépendantes. Les sections 0, 1, 2, 3, 4, 5, 7 conditionnent l'acceptation ; la section 6 est une piste sécurité parallèle à qualifier explicitement selon la cible Windows/Linux et la distribution.

**Interdictions actuelles :** originaux v6/v7 opérateur, profil existant `%LOCALAPPDATA%\com.fabulaxiom.greenfield.v1`, sauvegardes/journaux/ACL/marqueur, `M:\Fabulaxiom`, runtime migration 007, IPC writer, Windows Hello natif, nouveau marqueur durable et récupération automatique : **STOP** jusqu'à gate + nouveau consentement adapté. Un test CI synthétique n'est pas une permission locale.

---

## Protocole obligatoire de mise à jour après chaque validation

**Ce fichier est la source canonique et VIVANTE des 104 obligations M3.2**. À chaque nouvelle validation réelle d'une tâche `M32-xxx`, mettre à jour **ce même fichier** dans la PR de qualification correspondante, ou, si la preuve n'existe qu'après fusion (CI postmain), via une PR documentaire indépendante immédiatement après son obtention. Il ne faut jamais repousser l'actualisation à une future conversation. La case passe de `[ ]` à `[x]` seulement si l'ensemble du critère d'acceptation propre à cette tâche est démontré ; renseigner **date (AAAA-MM-JJ), PR, SHA exact, CI/run/attempt et statut terminal, portée de la preuve, référence issue #38, décision opérateur si nécessaire**. Garder toutes les preuves partielles sous case `[ ]`, même lorsque les tests fictifs passent.

**Chaque PR matérielle** (source, outil, workflow ou dossier de qualification) doit contenir ce fichier dans son diff, **même si aucune case n'est clôturée**. Ajouter alors une note datée « aucune case nouvelle clôturée ; preuves seulement partielles », sans augmenter artificiellement le total. Les deux prompts, HANDOFF_CURRENT.md/json et NEXT/STATE doivent rester cohérents. La CI contrôle la présence du fichier dans ces PR, l'identité de **104 tâches distinctes**, les compteurs, et les preuves des cases fermées. Le rapport de CI n'est ni une attestation humaine ni une validation des données réelles.

**Distinction importante :** une *étape source qualifiée*, une *CI postmain qualifiée*, une *obligation M3.2 clôturée* et la *phase M3.2 ACCEPTED* ne sont pas équivalentes. La progression des cases n'est pas une métrique de pourcentage : l'estimation ~45 % est suivie séparément. Les changements de stratégie `PRODUCT_FIRST_PARALLEL_SAFETY` nécessitent avertissement préalable de l'opérateur.

---

**10/11/2026 — Réconciliation des PR historiques : AUCUNE case nouvelle clôturée.** Re-fetch protected `main=7ffd1fb7ae2091dcba05a7c29860b0e11961a093` postmain Windows #42757811330 SUCCESS. Inventaire [#35/#215](../qualification/M3_2_LEGACY_PR35_PR215_RECONCILIATION_20261110.md) : #35 84 fichiers (5 identiques, 11 différents, 68 noms absents de main), #215 23 (6 identiques, 17 différents, 0 absent) ; module Rust D3b byte-identique de 10 097 caractères entre #215 et main. Le suivi **M32-007 reste [ ]** : les 68 chemins de #35 nécessitent triage avant tout portage/abandon décidé, #215 reste brouillon historique. Cette comparaison de source GitHub n'autorise pas writer/R1–R9 ni P4 réel ; **104 obligations, 2 closes / 102 ouvertes**. Les CI nouvelles seront qualifiées sur SHA exact avant toute nouvelle décision.

**10/11/2026 — Inventaire unitaire de #35, CANDIDAT non qualifié : AUCUNE case nouvelle clôturée.** Parent `main=425cb621d20b86f66a24aac1d6c1f63ffe479b0c`, CI postmain #334 [#42847268108](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/42847268108) attempt 1 completed/SUCCESS SHA exact (job #129938018079, 88 SUCCESS / 1 PR-only SKIPPED). [Matrice des 84 chemins de #35](../qualification/M3_2_PR35_PER_PATH_DISPOSITION_20261110.md) : 5 conserver identiques, 11 divergents à comparer, **68 absents** triés en étude historique, prototype synthétique, test CI jetable potentiel, outil opérateur retenu, ancienne IPC bloquée. **Chaque chemin reçoit une orientation, mais la preuve d'équivalence de chaque fonctionnalité n'est PAS faite** : M32-007 reste `[ ]`, #35/#215 restent DRAFT, aucune fusion transitive ; 104 tâches, 2 closes, 102 ouvertes. Toute validation ultérieure exige vraie preuve datée/CI SHA exact et #38 append-only. Ni writer ni G3 admis.

**10/11/2026 — #335 QUALIFIÉE POSTMAIN ; P3o CANDIDAT, AUCUNE case nouvelle clôturée.** #335 fusionnée sous Protect main (strict, `bypass_actors=[]`) à `main=e997a239f71d726c67880dd4acc07dfcda80482e`, CI PR #42875150735 SUCCESS au SHA `9764b24e95903c69aba74cf6e620ff26c5b36e1a`, CI push postmain #42877389890 attempt 1 completed/SUCCESS au SHA exact (job Windows #130044224664). La matrice des 84 chemins historiques #35 a désormais une CI postmain qualifiée ; **M32-007 reste [ ]**, aucune décision de clôture de PR #35/#215. P3o est un **nouveau lot candidat** ciblant un cycle de deux précédences courantes dans l'aperçu TS fictif (révoquées conservées) : `M3_2_P3O_SYNTHETIC_CURRENT_PRECEDENCE_CYCLE_REFUSAL_20261110.md`. Les cases **M32-058 et M32-080 restent [ ]**, preuve fixture-only partielle avant qualification CI source et postmain P3o, sans preuve writer/P4 réel. **104 obligations, 2 closes / 102 ouvertes, M3.2 IN_PROGRESS_NOT_ACCEPTED (~45 % estimés).** PRODUCT_FIRST_PARALLEL_SAFETY, R1–R9 NOT_PROVEN, G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE, historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED, main/WAL/SHM et ABA invisible NOT_PROVEN, glib #160 OPEN_NOT_REMEDIATED. Issue #38 append-only à mettre à jour à la décision de PR, sans réécrire l'historique.

**10/11/2026 — #336 P3o POSTMAIN QUALIFIÉE ; P3p CANDIDAT, AUCUNE case nouvelle clôturée.** Re-fetch protected `main=7660c96cf9b3eab3a8a958253f35726356420ee4`, PR #336 MERGED ; source HEAD `8a3d0c8e23ae3077fbfd8afd010d640dda08f279`, CI Windows #42894263560 attempt 1 completed/SUCCESS exact HEAD (89 étapes SUCCESS), CI push postmain #42896536877 attempt 1 completed/SUCCESS SHA exact (job #130111014880 : 88 SUCCESS, 1 PR-only SKIPPED), journal #38 [#6778816559](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6778816559). Nouvelle couverture **P3p candidate** : refus des liens `current` sur ancre retirée ou dupliqués avec ID distinct dans le seul décodeur TS fictif, rapport `M3_2_P3P_SYNTHETIC_ACTIVE_ENDPOINT_DUPLICATE_REFUSALS_20261110.md` ; CI P3p future À QUALIFIER. **M32-007, M32-058 et M32-080 restent [ ]** ; checklist **104 obligations, 2 closes / 102 ouvertes**, aucune admission d'opérateur, pas de progrès de gate ou pourcentage recalculé. #35/#215 restent DRAFT. PRODUCT_FIRST_PARALLEL_SAFETY inchangée ; writer/R1–R9 NOT_PROVEN, P4 réel STOP, G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE, historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED, main/WAL/SHM/ABA invisible NOT_PROVEN, glib #160 OPEN_NOT_REMEDIATED. `IN_PROGRESS_NOT_ACCEPTED` (~45 %). Toute case [x] future nécessite preuve datée et portée intégrale ; CI fictive ≠ admission.

## 0. Reprise et gouvernance GitHub

**Priorité :** P0. Priorité immédiate ; la documentation et une CI ne confèrent aucune admission de production.

- [x] **M32-001** Qualifier la CI postmain indépendante de la fusion #330 au SHA bef699511ff18e987a4858c797fde7aa88dfc59b  
  **Preuve de clôture :** Run push Windows #42699790716 terminal SUCCESS exact SHA, journal conservé et commentaire #38 append-only.
  **Acquis (2026-11-09) :** #42699790716 terminé/SUCCESS au SHA exact, job Windows 129441151373 86 succès + 1 étape PR-only SKIPPED ; issue #38 #6751823951.
- [x] **M32-002** Réconcilier la PR produit #331 P3n après la fusion #330  
  **Preuve de clôture :** Re-fetch base/main, calcul de divergence, éventuelle requalification sur nouveau HEAD ; source précédente #42674870251 SUCCESS seulement à a0a6c3e7… ; aucune fusion transitive.
  **Acquis (2026-11-10 ; périmètre GitHub/source seulement) :** réconciliation #331 sur #332, branche ahead=14/behind=0, source Windows #42751838279 attempt 1 completed/SUCCESS au HEAD `fb523abbc05b636d98fd93240872882f4ee57f61` ; dix fichiers conformes, reviews=[], threads=[], Protect main strict bypass=[], squash `expected_head_sha` et main `da5c64761159fd8fcc22ba541da04a7c54be6691` ; issue #38 #6758458130. La CI postmain #42754285833 est une preuve distincte, **completed/SUCCESS sur main au SHA exact** ; ne justifie ni writer ni P4 réel.
- [ ] **M32-003** Revoir le diff, les reviews, threads et le ruleset Protect main pour chaque future PR  
  **Preuve de clôture :** Required Windows frontend and Rust checks strict, bypass=[], aucune discussion non résolue, squash expected_head_sha.
- [ ] **M32-004** Éviter que les prompts de reprise et l'historique de handoff divergent  
  **Preuve de clôture :** Modifier les deux RESUME_PROMPT, HANDOFF_CURRENT.md/json et NEXT avec tout changement matériel ; short <3600 octets UTF-8 et R3/D3c/live SQLite WAL-index conservés.
- [ ] **M32-005** Écrire le statut vrai à la date de chaque checkpoint  
  **Preuve de clôture :** Distinguer candidatures, CI source, postmain, preuve produit, gate opérateur, NOT_PROVEN et ACCEPTED ; anciens checkpoints datés non réécrits rétroactivement.
- [ ] **M32-006** Conserver issue #38 comme journal append-only des décisions et refus  
  **Preuve de clôture :** SHA, run ID/attempt, résultats adversariaux, changements de périmètre et échecs ; zéro réécriture d'éléments historiques.
- [ ] **M32-007** Concilier les deux anciennes PR #35 et #215 avant toute décision sur leur devenir  
  **Preuve de clôture :** Vérifier diff de ces brouillons historiques et overlaps avec main ; portage ciblé sur branche actuelle ou clôture explicitement justifiée, jamais merge direct/aveugle.
  **Avancement partiel (2026-11-10 ; non clôturé) :** Inventaire des 107 chemins et preuves D3b dans `M3_2_LEGACY_PR35_PR215_RECONCILIATION_20261110.md`, main `7ffd1fb7ae2091dcba05a7c29860b0e11961a093` / postmain #42757811330 SUCCESS ; #35 a 68 chemins absents, aucun portage ou abandon global autorisé ; #215 reste DRAFT, pas de fusion transitive. La décision sur chaque ancien module est ouverte.
  **Lot de triage détaillé (2026-11-10, toujours NON CLOS) :** `M3_2_PR35_PER_PATH_DISPOSITION_20261110.md` classe individuellement les 84 chemins de #35, avec refus de l'ancienne IPC préflight et des outils opérateur. Les 68 chemins absents restent soumis à comparaison de couverture et à décision motivée ; aucune preuve de writer, P4 ou G2B–G6 n'a été gagnée.
- [ ] **M32-008** Faire autoriser séparément toute opération Windows sur machine opérateur  
  **Preuve de clôture :** Soumettre le script exact, effets possibles et STOP (disque/journaux/UAC/réseau, durée, interaction) puis recueillir un nouvel accord spécifique avant exécution.

## 1. Preuves de sûreté du writer Windows (R1–R9)

**Priorité :** P0 bloquant. P1 mono-acteur choisi par l'utilisateur ; same-SID fiable/cooperatif (pas de défense démontrée contre un acteur same-SID malveillant), P2 broker différé.

- [ ] **M32-009** R1 — fixer le profil/identité/autorité du propriétaire unique  
  **Preuve de clôture :** SID, session, propriétaire/DACL/intégrité, portée NEW_ONLY versus EXISTING_PROFILE ; menace same-SID coopérative explicitement bornée.
- [ ] **M32-010** R1 — tester refus de propriétaire/profil/ACL étranger  
  **Preuve de clôture :** Principal différent, conflit de nom de session, héritage de DACL, mutex non possédé : refus reproductible, fixtures Windows.
- [ ] **M32-011** R2 — protéger l'arborescence ancêtre jusqu'au fichier ouvert  
  **Preuve de clôture :** Répertoires parents tenus et identifiés, reparse/junction/ADS/device path refusés et chemins canoniques ancrés au handle réel.
- [ ] **M32-012** R2 — rejeter substitutions du nom et ABA sur les ancêtres  
  **Preuve de clôture :** Renommage/remplacement entre observation et xOpen, identité parent FileId128 ; toute fenêtre non couverte explicitement NON PROVEN/STOP.
- [ ] **M32-013** R3 — vérifier l'objet SQLite main effectivement délégué  
  **Preuve de clôture :** sqlite3_file.xFileControl / SQLITE_FCNTL_WIN32_GET_HANDLE et FileId128+volume à la frontière xOpen avant succès, aucun contrôle pathname présenté comme atomique.
- [ ] **M32-014** R3 — qualifier verrous Win32 natifs SHARED/RESERVED/PENDING/EXCLUSIVE  
  **Preuve de clôture :** SHARED simultanés, blocages opposés, transitions et release, deux processus, tests Windows jetables.
- [ ] **M32-015** R3 — qualifier fermeture et erreurs de callbacks  
  **Preuve de clôture :** xClose exact-once, handle nul/méthode manquante, close échoué, libération même sur échec et refus d'ouverture sans fuite.
- [ ] **M32-016** R4 — identifier et gérer journal, -wal et -shm comme objets distincts  
  **Preuve de clôture :** Pas de transfert de preuve main vers sidecars ; FileId128 et vie du mapping WAL-index vérifiés pour chaque objet pertinent.
- [ ] **M32-017** R4 — couvrir toutes les primitives SQLite SHM en mode WAL NORMAL  
  **Preuve de clôture :** xShmMap/xShmLock/xShmBarrier/xShmUnmap, régions multiples, verrous, barrières, versions des méthodes et cleanup, sur fixture réelle.
- [ ] **M32-018** R4 — démontrer que le garde main/WAL/SHM résiste aux substitutions contrôlées  
  **Preuve de clôture :** Interleaving de swap/rename/replace et leurres FileId128 sur chacun ; échec sûr sans risque d'assimiler une race non observée à une preuve générale.
- [ ] **M32-019** R4 — qualification en deux processus OS indépendants  
  **Preuve de clôture :** A tient BEGIN IMMEDIATE, B est refusé puis admis selon séquencement ; identité native et conservation du WAL/SHM observées des deux côtés.
- [ ] **M32-020** R4 — établir la frontière atomique ou admettre explicitement la limite  
  **Preuve de clôture :** Binding réel du handle et de l'espace de noms/sidecars au moment pertinent ; aucun chemin démontré = writer STOP, sans raccourci EXCLUSIVE/non-SHM non revu.
- [ ] **M32-021** R5 — prouver provenance SQLite distincte de integrity_check  
  **Preuve de clôture :** Profil, lineage M1.5/v6/v7, schema_migrations, clés, FK, identités immuables, journal état connu ; aucune adoption d'un SQLite seulement « ok ».
- [ ] **M32-022** R5 — refuser ATTACH étrangère, migration implicite et reprise ambiguë  
  **Preuve de clôture :** Cas négatifs de mauvaise version/clé, WAL incohérent, hot journal, ATTACH/migration et correction automatiques interdits.
- [ ] **M32-023** R6 — implémenter une unique session propriétaire avec génération  
  **Preuve de clôture :** Un Rust actor, une seule connexion admissible, registration VFS bornée, autorité privée, mutex/DACL coopératifs explicitement limités.
- [ ] **M32-024** R6 — refuser writer concurrent et commandes périmées  
  **Preuve de clôture :** Processus A/B, génération révoquée, double writer, claim abandonné, timeout/WAIT_ABANDONED, refus dès l'entrée et pas de faux succès.
- [ ] **M32-025** R7 — définir fermeture, checkpoint, crash, restart et transition RECOVERY_REQUIRED  
  **Preuve de clôture :** Fermeture contrôlée, COMMIT/checkpoint/interruption, journal/WAL/SHM, preuve de provenance durable et non auto-fabriquée.
- [ ] **M32-026** R7 — tester matrice de crash à phases bornées et restart jetable  
  **Preuve de clôture :** Crash pendant xOpen/xShm/transaction/close/recovery ; PAS de réadmission au seul motif « SQLite peut récupérer ».
- [ ] **M32-027** R7 — décider et qualifier séparément la récupération native éventuelle  
  **Preuve de clôture :** Recovery permis seulement après preuve de source et autorisation spécifique ; pas de nouveau marqueur durable ni réouverture EXISTING_PROFILE par défaut.
- [ ] **M32-028** R8 — qualifier durée de vie C ABI, VFS et ressources  
  **Preuve de clôture :** pMethods versions, xFileControl, xClose, mémoire/libération, cancellation, queue bornée, races shutdown, échec avec révocation.
- [ ] **M32-029** R8 — bornage des transactions, lectures et requêtes futures  
  **Preuve de clôture :** Pas de lock au travers await ou d'inférence Ollama ; timeout, réponses typées, fail-closed, aucun accès direct SQLite donné à l'UI ou au modèle.
- [ ] **M32-030** R9 — construire dossier d'admission négatif et positif indépendant  
  **Preuve de clôture :** Tests Windows jetables et provenance complète R1–R8, avis contradictoire, CI SHA exact ; aucune assertion « writer prouvé » sans gate formel.
- [ ] **M32-031** R9 — obtenir une décision explicite et nouvelle avant writer runtime  
  **Preuve de clôture :** L'opérateur approuve précisément le périmètre et les risques résiduels ; V7WriterAdmission et IPC interdits avant décision.

## 2. Provenance, sauvegardes et cérémonies G2–G6

**Priorité :** P0 bloquant. G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE, G4–G6 non autorisés ; ne pas demander/ouvrir d'originaux au titre de cette checklist.

- [ ] **M32-032** Résoudre le témoin production/pre_m24_early_manifest  
  **Preuve de clôture :** Source antérieure indépendante authentifiant le rôle et le digest exact ; ne pas confondre avec une sauvegarde SQLite.
- [ ] **M32-033** Résoudre le témoin acl/original_acls  
  **Preuve de clôture :** Preuve antérieure et indépendante du contenu exact et de son rôle, sans reconstruire les octets historiques.
- [ ] **M32-034** Résoudre le témoin acl/pre_repair_json  
  **Preuve de clôture :** Preuve indépendante préalable du JSON, de son digest et de sa chaîne de conservation.
- [ ] **M32-035** Résoudre le témoin production/activation_marker  
  **Preuve de clôture :** Authentifier les octets et l'identité historiques, non seulement le nom ou la description d'un ancien marqueur.
- [ ] **M32-036** Résoudre le témoin m25/isolated_v6  
  **Preuve de clôture :** Prouver l'identité du rôle original, distincte des sauvegardes pré-M2.5 et de leurs manifests.
- [ ] **M32-037** Si des preuves historiques authentiques manquent, enregistrer honnêtement cette limite  
  **Preuve de clôture :** Issue #36 ouverte : PENDING_EXTERNAL_ATTESTATION(21/3/2) ne devient jamais PASS par nouvelle signature.
- [ ] **M32-038** Décider séparément la mise en place d'un baseline prospectif  
  **Preuve de clôture :** SOLO_OPERATOR_COMPENSATING_CONTROLS est une politique documentaire, prospective NOT_STARTED ; le futur baseline n'atteste PAS le passé.
- [ ] **M32-039** G2-B — prouver l'identité de la source et l'absence d'un écrivain concurrent  
  **Preuve de clôture :** G2-A PASS_METADATA_ONLY_OWNER_REPORTED n'est pas la preuve d'absence ; procédure Windows exacte/autorisation nouvelle, positive et adversariale.
- [ ] **M32-040** G2-C — qualifier accord opérateur de source et de périmètre  
  **Preuve de clôture :** Autorisation distincte, source réellement identifiée, aucun remplacement d'un ancien accord par un test GitHub.
- [ ] **M32-041** G2-D — examiner quiescence, sidecars, ACL, chemin de backup et préflight  
  **Preuve de clôture :** Absence d'écrivain, WAL/SHM/hot journal et opérations pouvant écrire examinés ; refuser si source non stable.
- [ ] **M32-042** G3 — obtenir une méthode sûre de capture prospective depuis une source prouvée  
  **Preuve de clôture :** Owner déjà authentifié non migrant avec API Backup cohérente, ou source froide établie ; destination neuve réservée sans collision.
- [ ] **M32-043** G3 — tenir la copie et sa chaîne de conservation  
  **Preuve de clôture :** Source et destination distinctes, aucun close/reopen risqué, ACL et hashes, identité de volume/objet, pas de copie brute de WAL actif.
- [ ] **M32-044** G4 — vérifier l'image isolée et un vrai test de restauration  
  **Preuve de clôture :** integrity_check=ok, foreign_key_check vide, tables/compteurs/digests logiques, v6 et révisions exactes, témoins adversariaux et réouverture.
- [ ] **M32-045** G4 — démontrer absence de modification des originaux  
  **Preuve de clôture :** L'ancien pointer actif M1.5, sauvegardes, ACL, journaux, révisions/canons et activation marker sont préservés et vérifiés indépendamment.
- [ ] **M32-046** G5 — formaliser la décision de risque de l'opérateur unique  
  **Preuve de clôture :** Signature datée prospective, risques résiduels et contrôles compensatoires explicites ; ne jamais la présenter comme une attestation d'un relecteur indépendant.
- [ ] **M32-047** G6 — recette isolée du profil admissible et de la lecture v7  
  **Preuve de clôture :** Périmètre explicitement autorisé, audit Windows Tauri/WebView2, pas de migration ou écriture implicite.
- [ ] **M32-048** Avant toute migration 007 — sauvegarde cohérente non écrasante de v6  
  **Preuve de clôture :** Emplacements neufs, SHA256, digest de toutes les tables et historique des sauvegardes, contrôle du pointer ; autorisation distincte.
- [ ] **M32-049** Séparer une éventuelle activation de production de la seule acceptation d'un projet neuf  
  **Preuve de clôture :** Ne pas fusionner l'admission Greenfield NEW_ONLY avec l'autorité EXISTING_PROFILE ; chaque profil/identité requiert son gate.

## 3. Fonctionnalités Rust/SQLite de chronologie persistante

**Priorité :** P1 produit. P2/P3/Rust test-only, SQLite RAM et v7 jetables déjà largement couverts ; les opérations réelles hors fixtures ne sont pas qualifiées.

- [ ] **M32-050** Réconcilier la PR historique #35 sans la fusionner en bloc  
  **Preuve de clôture :** Porter uniquement les éléments utiles sur base main moderne ; détecter overlaps SQL/lib.rs/workflow, aucun effet runtime implicite.
- [ ] **M32-051** Documenter le contrat de données v7 existant  
  **Preuve de clôture :** Calendriers fictifs scoped Universe, ancres, precedences, précision exacte/approximative/relative/inconnue, STRICT/FK/index, ids immuables.
- [ ] **M32-052** Rendre le service Rust chronologique accessible derrière la seule autorité admise  
  **Preuve de clôture :** API typée pour calendrier, événements, ancres, liens, listes ; refus tant que session gate NON ADMITTED.
- [ ] **M32-053** Compléter création et lecture de calendriers par univers  
  **Preuve de clôture :** Universes isolés, calendrier déclaré et références exactes ; aucune hypothèse de calendrier grégorien.
- [ ] **M32-054** Compléter création et liste d'événements/ancres  
  **Preuve de clôture :** Nom/type, contexte, heure fictive, sources, champs inconnus, pagination/tri déterministe et absence d'horodatage fabriqué.
- [ ] **M32-055** Compléter édition métier non destructive d'ancre  
  **Preuve de clôture :** Supersession ou révision append-only avec motif humain ; ancien objet toujours consultable.
- [ ] **M32-056** Compléter création de précédence « A avant/après B »  
  **Preuve de clôture :** IDs exacts de même Universe ; limites de portée, erreurs déterministes, pas d'ordre global inventé.
- [ ] **M32-057** Compléter révocation et correction des précédences  
  **Preuve de clôture :** Lien précédent conservé, révocation datée dans l'histoire, rollback et diff exacts ; pas de suppression en cascade.
- [ ] **M32-058** Traiter les conflits et cycles sur graphe actif  
  **Addendum P3p (2026-11-10, NON close) :** P3o CI HEAD #42894263560 et postmain #42896536877 SUCCESS exact SHA ; P3p ajoutera des refus actifs pour ancres historiques et paires dupliquées sur données fictives. CI P3p À QUALIFIER. Pas de preuve writer/production.
  **Preuve partielle P3o (2026-11-10, NON close) :** décodeur TS read-only fictif refuse les cycles entre relations `current`, préserve les liens historiques, test Vitest ciblé ; CI HEAD P3o et postmain À QUALIFIER. Aucune preuve runtime/writer ni acceptation globale.
  **Preuve de clôture :** Détecter cycles, auto-lien, duplicata, contradictions, bornes impossibles ; afficher témoins directs sans réécriture de la chronologie.
- [ ] **M32-059** Traiter dates et incertitudes en quatre modes  
  **Preuve de clôture :** Exact calendrier fictif, plage approximative, relatif, inconnu ; bornes/precision saisies et restituées sans coercition Date.parse.
- [ ] **M32-060** Traiter la comparaison entre calendriers fictifs  
  **Preuve de clôture :** Mapping créé explicitement par auteur ; sans mapping = INDETERMINATE, jamais conversion automatique.
- [ ] **M32-061** Lier un événement à scène et révision historique immuable  
  **Preuve de clôture :** Novel, Scene, revision ID ; HEAD actuelle distincte de la révision source ; aucune invalidation lors d'édition de scène.
- [ ] **M32-062** Gérer plusieurs romans dans un Universe et plusieurs Universes distincts  
  **Preuve de clôture :** Contraintes cross-novel dans même Universe, rejet cross-Universe avant modification, identités homonymes distinctes.
- [ ] **M32-063** Garantir transactions atomiques et refus cohérents  
  **Preuve de clôture :** BEGIN IMMEDIATE/commit/rollback, corrections idempotentes, aucun succès partiel après une erreur.
- [ ] **M32-064** Garantir persistance sur v7 neuve puis réouverture  
  **Preuve de clôture :** Parcours create/correct/revoke/list/restart sur fichier jetable : conservation de l'histoire et de toutes les autres données.
- [ ] **M32-065** Maintenir la v6 restaurée et migration 007 non exécutée sans gate  
  **Preuve de clôture :** Aucune élévation automatique au premier démarrage ; code de version et routage de stockage auditables.

## 4. Interface React/Tauri et usage quotidien

**Priorité :** P1 produit. P3n filtre par propriété et P3m provenance des écarts sont testés sur laboratoire, pas activés sur une base opérateur.

- [ ] **M32-066** Définir le parcours opérateur d'un projet Greenfield réellement neuf  
  **Preuve de clôture :** Sélection Universe/Novel/Scene, calendrier, ancre, lien et sauvegarde, avec identité NEW_ONLY séparée, Ollama désactivable.
- [ ] **M32-067** Intégrer à une vraie navigation l'atelier chrono aujourd'hui isolé  
  **Preuve de clôture :** L'atelier P3/P4 React fictif n'est pas une fonction App.tsx ; brancher seulement une fois la frontière admise.
- [ ] **M32-068** Relier l'UI à des commandes Tauri Rust typées et bornées  
  **Preuve de clôture :** Aucun accès direct DB/path/SQL/admission token, vérification par session/génération, pas de commande de writer avant R9.
- [ ] **M32-069** Distinguer visuellement les trois ordres indépendants  
  **Preuve de clôture :** Chronologie du monde modifiable, position de narration distincte, ordre de révélation en lecture seule (M3.2) ; aucune conversion silencieuse.
- [ ] **M32-070** Concevoir formulaires calendrier et événement utilisables sans IA  
  **Preuve de clôture :** Création, saisie précision, validité, estimation, source, révision ; messages explicites sans obligation Ollama.
- [ ] **M32-071** Concevoir liste/consultation et inspection des sources historiques  
  **Preuve de clôture :** Filtres Universe/Novel/personnage, versions, pagination, affichage IDs et date fictive, source exacte et statut.
- [ ] **M32-072** Concevoir éditeur humain de précédence avant/après  
  **Preuve de clôture :** Choix de deux ancres, aperçu de l'impact et témoin de cycle avant confirmation, explication des erreurs.
- [ ] **M32-073** Concevoir correction/supersession/révocation réversible  
  **Preuve de clôture :** Motif humain, prévisualisation, confirmation, historique inspectable et annulation sans effacer les anciennes lignes.
- [ ] **M32-074** Préserver la séparation brouillon/proposé/canon existante  
  **Preuve de clôture :** Aucun texte de scène, fiche ou assertion M2 n'est promu canon par l'UI chronologique.
- [ ] **M32-075** Garantir accessibilité/échappement et comportement hors ligne  
  **Preuve de clôture :** Navigation clavier, libellés et messages, absence de fuite par HTML hostile, aucune requête externe ni dépendance à Ollama.
- [ ] **M32-076** Ne jamais afficher un faux succès de persistance  
  **Preuve de clôture :** État « fictif/non persisté » tant que fixture ; si refus du writer, affichage explicite et aucune modification prétendue.
- [ ] **M32-077** Gérer erreurs de session et de fichiers sans corruption  
  **Preuve de clôture :** Collision, BUSY, source étrangère, timeout, annulation, fermeture/relance : UI refuse et indique l'action possible.

## 5. Recettes de non-régression et d'acceptation Windows

**Priorité :** P1 preuve. Les 332 Rust / 7 Greenfield / 69 inventory / 183 continuité / 427 Vitest / 88+88 Chromium / 25 blobs sont déjà des résultats CI P3n uniquement, pas ces recettes réelles.

- [ ] **M32-078** Construire une matrice exigences→tests→preuves à jour  
  **Preuve de clôture :** Chaque ligne présente nom du test, SHA, date, fixture/Windows réel, attentes, logs et résultat ; pas de PASS hérité d'un HEAD ancien.
- [ ] **M32-079** Valider les quatre temporalités sur deux Universes et plusieurs romans  
  **Preuve de clôture :** Calendrier exact/approx/relative/inconnu, dates sans mapping, undated et scènes anciennes.
- [ ] **M32-080** Valider prévention des cycles et conflits déterministes  
  **Addendum P3p (2026-11-10, NON close) :** P3o CI HEAD #42894263560 et postmain #42896536877 SUCCESS exact SHA ; P3p ajoutera des refus actifs pour ancres historiques et paires dupliquées sur données fictives. CI P3p À QUALIFIER. Pas de preuve writer/production.
  **Preuve partielle P3o (2026-11-10, NON close) :** décodeur TS read-only fictif refuse les cycles entre relations `current`, préserve les liens historiques, test Vitest ciblé ; CI HEAD P3o et postmain À QUALIFIER. Aucune preuve runtime/writer ni acceptation globale.
  **Preuve de clôture :** Chemins cycliques, doublons, exclusions et opposition avant/après ; rollback et données intactes.
- [ ] **M32-081** Valider revocations, corrections et lecture du passé  
  **Preuve de clôture :** Ancres/revisions historiques demeurent consultables après modifications, sans modifier HEAD des scènes.
- [ ] **M32-082** Valider isolation Universe et IDs homogènes  
  **Preuve de clôture :** Homonymes, mauvais foreign keys, cross-Universe et anciennes révisions étrangères refusés.
- [ ] **M32-083** Valider monde/narration/révélation indépendants  
  **Preuve de clôture :** Flashbacks et divulgations différées sans conversion ni ordre total inféré.
- [ ] **M32-084** Valider tests négatifs de fichiers et des droits Windows  
  **Preuve de clôture :** TOCTOU, symlinks/reparse, WAL/SHM, ATTACH, processus concurrents, tampering, stale generation et crash.
- [ ] **M32-085** Valider sauvegarde/restauration à destination neuve et pointeur v6 inchangé  
  **Preuve de clôture :** Digests avant/après, manifests, WAL cohérent, copie jetable restaurée, aucune suppression d'originaux.
- [ ] **M32-086** Tester usage hors ligne avec Ollama éteint  
  **Preuve de clôture :** Aucune dépendance sur moteur LLM, cloud, FTS/embedding, M4–M7 ; UI chrono manuelle fonctionnelle.
- [ ] **M32-087** Tester réouverture et récupération selon périmètre autorisé  
  **Preuve de clôture :** Reboot, clôture propre, coupure/crash ; toute récupération incertaine STOP, jamais réparation silencieuse.
- [ ] **M32-088** Valider intégration Rust–Tauri–React Windows hors laboratoire après gate  
  **Preuve de clôture :** Identité de profil, fenêtres WebView2, navigation, erreurs et persistance réelle d'un projet autorisé.
- [ ] **M32-089** Réaliser une recette opérateur sur un profil NEUF admis  
  **Preuve de clôture :** Protocole de tests observés par propriétaire, preuves offline, sauvegardes distinctes, absence de perte ; seulement avec consentement spécifique.
- [ ] **M32-090** Réaliser une recette distincte sur copie authentifiée des données historiques si autorisée  
  **Preuve de clôture :** G3–G6 et R1–R9 préalablement franchis ; aucune déduction depuis un projet neuf.
- [ ] **M32-091** Auditer absence de réseau non voulu et stabilité mémoire/fichiers  
  **Preuve de clôture :** CSP/Vite, handles Win32, shutdown, file descriptors, compat Tauri et traces d'audit sans fuite de récits.

## 6. Sécurité dépendances et décisions latérales

**Priorité :** P1 parallèle / hors gate produit direct. Cette piste continue en parallèle ; correction glib/Linux et distribution V1 sont distinctes de la recette des seules fonctionnalités M3.2.

- [ ] **M32-092** Traiter séparément les alertes Dependabot Vite/launch-editor  
  **Preuve de clôture :** Issue #160, inventorier avis, correctifs réellement compatibles, npm lock authentique et npm ci/TS/Chromium; aucune réécriture de lock arbitraire.
- [ ] **M32-093** Traiter le problème glib 0.18.5 de la chaîne Linux GTK3  
  **Preuve de clôture :** Suivre une migration intégrée Tauri/WRY GTK4/WebKit6 ou correctif validé ; ne jamais forcer glib 0.20 seule dans gtk 0.18.
- [ ] **M32-094** Qualifier Windows et Linux comme deux expositions distinctes  
  **Preuve de clôture :** Audit de graphe Windows vs Linux, build Linux jetable si distribution envisagée ; ne pas affirmer exploitabilité Windows sans preuve.
- [ ] **M32-095** Documenter décisions de sécurité restantes avant distribution  
  **Preuve de clôture :** Ne pas masquer/dismiss une alerte, justifier le périmètre de déploiement, garder #160 OPEN_NOT_REMEDIATED jusqu'au correctif qualifié.
- [ ] **M32-096** Tenir Windows Hello comme confirmation future des actes sensibles  
  **Preuve de clôture :** L'utilisateur ne veut pas de comptes supplémentaires ; pas d'intégration native Hello avant gate propre, ne pas assimiler Hello à une provenance SQLite.

## 7. Acceptation finale, normalisation et sorties de périmètre

**Priorité :** P0 final. Critère de fin : usage manuel réellement opérable et preuves de protection des données ; les multiples tests fictifs et les pourcentages ne sont pas des gates.

- [ ] **M32-097** Prendre une décision d'admission writer formelle basée sur R1–R9  
  **Preuve de clôture :** R1–R9 vérifiés ou risque résiduel explicite accepté après revue humaine ; aucune admission par succès CI seul.
- [ ] **M32-098** Prendre décisions explicites G2B–G6 et provenance  
  **Preuve de clôture :** Issue #36 traitée honnêtement, baseline prospective vérifiée, G3/G4/G5/G6 attestées selon leurs critères ; sinon M3.2 reste NOT_ACCEPTED.
- [ ] **M32-099** Accepter les parcours produit complets, pas seulement un démonstrateur  
  **Preuve de clôture :** CRUD chronologie persistant, corrections historiques, ordre monde/narration/révélation, UX offline et Windows operator acceptance.
- [ ] **M32-100** Qualifier la PR d'implémentation finale au HEAD exact et sous Protect main  
  **Preuve de clôture :** CI Windows terminal SUCCESS, logs, diff, reviews/threads, bypass=[], squash expected_head_sha ; zéro modification des originaux avant consentement.
- [ ] **M32-101** Effectuer contrôle postmain indépendant de chaque merge  
  **Preuve de clôture :** Run push exact nouveau SHA, résultat terminal, registre #38 ; faux succès et flake non occultés.
- [ ] **M32-102** Fusionner une PR séparée de normalisation documentaire de M3.2  
  **Preuve de clôture :** ROADMAP_STATUS, gate decision, STATE/NEXT/HANDOFF MD+JSON/historique/prompts, critères et provenance à jour, nouvelle CI exacte et postmain.
- [ ] **M32-103** Prononcer explicitement M3.2 ACCEPTED + MERGED + NORMALIZED  
  **Preuve de clôture :** Seulement avec signature et synthèse de toutes les preuves, aucun gate STOP ni risque inexpliqué transformé en PASS.
- [ ] **M32-104** Conserver M3.3–M3.6, M4–M9, Ollama créatif, cohérence IA et ComfyUI hors M3.2  
  **Preuve de clôture :** Aucun lancement implicite de subdivision suivante, pas de release/production générale attribuée à cette seule étape.

---

## Ordre de travail recommandé (chemin critique sans changer la stratégie)

1. **Immédiat** : #334 postmain #42847268108 est SUCCESS au SHA exact 425cb621d20b86f66a24aac1d6c1f63ffe479b0c ; qualifier le nouveau lot de triage #35 sur CI HEAD exact, puis porter UN test fictif ciblé seulement si nécessaire ; maintenir checklist, prompts, handoffs et issue #38 à CHAQUE obligation validée.
2. **En parallèle** : finaliser les preuves P1 R2–R4 sur fichiers Windows jetables et R5–R9 mono-propriétaire ; rechercher les cinq témoins de #36 sans créer de fausse attestation ; suivre #160.
3. **Après un nouveau consentement explicite** : G2B/C/D, puis une source réellement attestée, G3–G5, sauvegarde cohérente et restauration isolée, puis G6.
4. **Seulement après les gates correspondants** : admission de session et writer runtime, intégration React/Tauri/Rust, parcours de projet neuf/fixture puis recette opérateur, migration contrôlée seulement si approuvée.
5. **Fin** : matrice de tests/acceptation Windows complète, PR de fonctionnalité source CI, merge protégé, postmain, puis PR séparée de normalisation et décision M3.2 ACCEPTED.

## Références d'autorité et portée

- [Roadmap détaillée M3 : contrats et acceptation M3.2](../roadmap/M3_TIME_KNOWLEDGE_RELATIONSHIPS.md)
- [État courant roadmap V1](../roadmap/ROADMAP_STATUS_CURRENT.md)
- [Mesure M3.2 et six tâches regroupées](../qualification/M3_2_PROGRESS_ASSESSMENT_20261105.md)
- [Contrat P1 writer R1–R9](../qualification/M3_2_V7_PRODUCTION_WRITER_CUSTODY_DESIGN_STUDY_20261028.md)
- [Preuves P1 R1–R9 et transitions de session](../qualification/M3_2_V7_P1_SINGLE_OWNER_SESSION_PROOF_PLAN_20261028.md)
- [G2–G6 et politique solo prospective](../qualification/M3_2_PROSPECTIVE_TRUST_BASELINE_DECISION.md)
- [Inventaire des briques produit existantes](../qualification/M3_2_PRODUCT_VERTICAL_SLICE_EXISTING_CODE_MATRIX_20261101.md)
- [Réconciliation #35](../qualification/M3_2_PR35_SAFE_RECONCILIATION_PLAN.md)
- [Gate decision courante](M3_2_GATE_DECISION_CURRENT.md)
- [Issue #36 : cinq attestations historiques](https://github.com/LaurentCOLL1/Fabulaxiom/issues/36), [#38 : journal append-only](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38), [#160 : vulnérabilités](https://github.com/LaurentCOLL1/Fabulaxiom/issues/160).

**Non inclus dans M3.2** : M3.3 histoire des relations, M3.4 savoir/croyances, M3.5 révélations narrateur/lecteur éditables, M3.6 états narratifs évolutifs, M4 récupération, M5 Ollama auteur, M6 cohérence automatique, M7 écriture assistée, M8 visualisations, M9 distribution et ComfyUI. M3.2 doit cependant présenter les trois ordres distincts et une vue de révélation **read-only**.

*Cette liste est une feuille de route de preuves et de livraison, pas une autorisation d'exécuter une commande ou d'ouvrir des données privées.*
