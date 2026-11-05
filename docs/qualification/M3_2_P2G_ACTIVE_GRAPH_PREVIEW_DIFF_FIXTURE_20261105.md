**05/11 — #285 P2g FUSIONNÉE** : source `6852834fe99a15a1719f45a4997641fd3c76ec86`, Windows #41958673635 SUCCESS (317 Rust/7 Greenfield/68 inventaire/183 continuité/6 Vitest/Chromium 85/85 normal+CSP/19 blobs) ; #283 postmain #41956730569 et #284 postmain #41958460615 SUCCESS. Squash protégé `expected_head_sha`, `main=906ad4103a639eaee94f6cb51e55d96cb87f46e0`, issue #38 append-only #6649577095 ; **#285 postmain #41967078610 EN COURS/NON QUALIFIÉE au checkpoint**. P2g test-only v7 RAM préouverte : avant/après actif sous IMMEDIATE avec ROLLBACK, aucun droit writer ni P4. Stratégie PRODUCT_FIRST_PARALLEL_SAFETY inchangée (prévenir AVANT changement). STOP M3.2 IN_PROGRESS_NOT_ACCEPTED, writer/R1–R9 NOT_PROVEN, G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE, historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED ; R4–R9 custody main/WAL/SHM et auteur adverse NOT_PROVEN. glib #160 OPEN_NOT_REMEDIATED. Aucun opérateur, IPC writer, 007, Hello natif, backups/journaux/recovery. CI fictive ≠ admission réelle. Prochain : qualifier #41967078610, PR documentaire CI exacte, R4–R9 parallèle.

# M3.2 — P2g : comparaison avant/après du graphe actif en aperçu RAM (CANDIDAT NON QUALIFIÉ)

**5 novembre 2026.** Parent #283 P2f fusionnée sous Protect main : source `d90c584e5e46b4d1b33e4feced3322e57ed3301c`, CI Windows #41925365662 SUCCESS (314 Rust/7 Greenfield/68 inventaire/183 continuité/6 Vitest/Chromium 85/85 normal+CSP/19 blobs fictifs), nouveau `main=3bb2075965202a875150e800ee8aa31285ec2f04`. Postmain #41956730569 **en attente de qualification terminale**. Parent documentaire #284 DRAFT HEAD `3c55596a6458ec243fad748827053c55149d576f`, CI exacte #41957304748 distincte. **Ce nouveau P2g est candidat, aucune CI acquise.**

## Tranche produit limitée

L'auteur doit comprendre précisément ce que change une proposition de correction chronologique, avant de confirmer. P2f retourne déjà le nouvel ordre proposé après une exécution de test qui finit par ROLLBACK ; P2g ajoute **deux listes d'arêtes actives** à ce résultat non persistant : `active_before` et `active_after`. Ces listes n'infèrent ni date, ni ordre total, ni conversion calendaire. Elles sont des observations contemporaines de la fixture, pas des droits d'écriture.

Dans le seul service `#[cfg(test)]` `src-tauri/src/m32_p2_fixture_chronology_service.rs`, le SQL déjà employé pour visualiser le graphe actif est factorisé dans `query_active_graph(&Connection,universe)`. `preview_atomic_correction` vérifie toujours la présence de l'overlay stage 4, ouvre une transaction `IMMEDIATE`, extrait `active_before`, exécute exactement le même helper de deux INSERT protégés que la confirmation P2e, extrait `active_after` depuis cette transaction puis appelle explicitement `ROLLBACK`. La requête publique du graphe actif reprend le helper commun après garde. Aucune nouvelle table, SQL DDL, ouverture SQLite ou transaction externe.

La file de commandes Rust P2b conserve son enveloppe `PreviewCorrection` et retourne le type `CorrectionPreview` enrichi : **pas de Tauri IPC, pas de WebView2/App.tsx, aucun token d'admission**. L'ancienne assertion A→B reste historique ; le résultat avant/après peut montrer A→B initialement active puis B→A comme reformulation active. Un autre client peut écrire entre prévisualisation et confirmation ; le refus de la confirmation désormais cyclique reste obligatoire.

**Trois nouveaux tests Rust proposés, NON ACQUIS avant CI** :
- Aperçu valide avant/après comprenant une deuxième arête indépendante, conservation de l'ancien graphe après ROLLBACK, zéro décision et zéro restatement persistés, révision historique `r2` et tête narrative `r3` inchangées, `PRAGMA integrity_check=ok`.
- Aperçu échoué (cycle, autre univers) retourne une erreur sans écriture ni modification du graphe initial ; l'univers fictif `u2` reste isolé.
- Acteur mono-propriétaire retourne les deux listes, puis un autre client change la chronologie ; confirmation obsolète refusée, arrêt de l'acteur et refus des clients après fermeture.

**Compte attendu, PAS QUALIFIÉ** : 317 tests Rust (314+3), 7 Greenfield, 68 inventaire, 183 continuité, six Vitest, Chromium 85/85 normal et CSP stricte, 19 blobs Git fictifs. Qualification uniquement depuis la CI Windows au SHA exact de la PR P2g ; ancien succès #283 et CI parent #284 non substituables.

## Limites et STOP

P2g est limité à deux modules Rust `#[cfg(test)]` avec fixture RAM préouverte, sans base/profil opérateur, fichier journal, backup, migration runtime 007, writer IPC, vrai VFS, Hello natif, marqueur ou recovery. Les aperçus ne permettent pas d'admettre le writer ni la provenance main/WAL/SHM ; aucune garantie de stabilité d'une confirmation ultérieure.

Stratégie **PRODUCT_FIRST_PARALLEL_SAFETY** inchangée ; avertir avant changement. **M3.2 IN_PROGRESS_NOT_ACCEPTED** ; P4 réel/writer/R1–R9 **NOT_PROVEN** ; G2B **NOT_ACCEPTED** ; G2C **NOT_AUTHORIZED** ; G3 **STOP_UNAVAILABLE** ; historique **PENDING_EXTERNAL_ATTESTATION(21/3/2)**, prospective **NOT_STARTED** ; D3b-4/5 STOP. R4–R9 custody atomique main/WAL/SHM et écrivain adverse **NOT_PROVEN**. glib 0.18.5 GTK3/Linux issue #160 **OPEN_NOT_REMEDIATED**.

Gates : #283 postmain indépendante terminale, #284 source propre/merge et postmain indépendantes, exact-head CI Windows P2g et logs, reviews/threads, Protect main ACTIVE strict bypass=[], squash `expected_head_sha`, postmain séparée et #38 append-only. **CI de fixture ≠ admission réelle.**
