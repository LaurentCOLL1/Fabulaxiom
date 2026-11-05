# Qualification P2f — source et fusion confirmées ; postmain distincte en cours

**Vérification du 5 novembre 2026.** PR #283 source HEAD `d90c584e5e46b4d1b33e4feced3322e57ed3301c`, Windows #41925365662 completed/SUCCESS au SHA exact, job #126908233158 (314 Rust/7 Greenfield/68 inventaire/183 continuité/6 Vitest, Chromium 85/85 normal+CSP stricte, 19 blobs Git fictifs). Les 3 nouveaux tests P2f passent. `Protect main` ACTIVE strict bypass=[], reviews=[] threads=[], squash avec `expected_head_sha` vers `main=3bb2075965202a875150e800ee8aa31285ec2f04`. **Postmain indépendante #41956730569 IN_PROGRESS/NOT QUALIFIED au checkpoint ; confirmer terminalement avant de déclarer #283 complètement qualifiée.** Journal append-only #38 comment #6648211915. La notice historique de candidature plus bas décrit les étapes précédentes, pas le statut actuel.

**Portée exclusivement test-only.** Une seule fixture SQLite v7 RAM préouverte, SQL de correction P2e exécuté sous `BEGIN IMMEDIATE` puis ROLLBACK explicite. Aucun résultat de prévisualisation n'accorde de droit d'écriture ultérieur. Aucun vrai writer/IPC/Tauri ni migration 007 runtime ni données/profil opérateur, backup/journal, Hello natif ou recovery. `PRODUCT_FIRST_PARALLEL_SAFETY` inchangée. **M3.2 IN_PROGRESS_NOT_ACCEPTED ; P4 réel/writer/R1–R9 NOT_PROVEN ; G2B NOT_ACCEPTED ; G2C NOT_AUTHORIZED ; G3 STOP_UNAVAILABLE ; historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED ; glib 0.18.5 Linux GTK3 issue #160 OPEN_NOT_REMEDIATED.** CI de fixture ≠ admission réelle.

---

**04/11 — P2f À REQUALIFIER APRÈS REBASE** : #282 docs source #41922401986 SUCCESS, protected main `97ca0898bdbeb46862c59b3f4ccca3e0cb3f491c`, postmain #41924499980 en cours/non qualifiée au checkpoint. Ancienne P2f #283 CI #41923838226 en cours (SHA précédent), nouvelle CI Windows obligatoire après reconstruction sur main à arbre identique. 314 Rust attendus (+3), aucun résultat nouveau admis. Aperçu P2f de chronologie : sur fixture v7 RAM préouverte, SQL IMMEDIATE teste revoke+restate comme confirmation P2e, puis rollback ; pas de token, revalidation à la confirmation ; Rust `#[cfg(test)]` seulement. **PRODUCT_FIRST_PARALLEL_SAFETY** inchangée, avertir avant changement, Protect main ACTIVE strict bypass=[], expected_head_sha, issue #38 append-only. **STOP** M3.2 IN_PROGRESS_NOT_ACCEPTED, vrai P4/writer/R1–R9 NOT_PROVEN, G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE, historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED ; R4–R9 main/WAL/SHM custody atomique et writer adversarial NOT_PROVEN, glib 0.18.5 Linux GTK3 #160 OPEN_NOT_REMEDIATED. Ni données/profil opérateur, IPC writer, runtime 007, sauvegarde/journal, native Hello, marqueur/recovery. Fixtures CI ≠ admission réelle.

# M3.2 — P2f : aperçu de correction chronologique sans persistance (CANDIDAT NON QUALIFIÉ)

**04/11/2026** — Branche P2f basée sur **#282 documentation DRAFT** au HEAD `00e7cff01274343a6053eb56c4c6fcfcf5d85435`. Dépendance P2e : **#281 fusionnée** sur `main=e58b03c024c644a4eab9bbc40f3f3533ec0caab3`, CI source #41907264072 SUCCESS (311 Rust/7 Greenfield/68 inventaire/183 continuité/6 Vitest/Chromium 85/85 normal+CSP/19 blobs fictifs), postmain indépendante #41921522033 **SUCCESS au même main**. #282 doit être qualifiée/fusionnée et postmain validée avant toute fusion du candidat P2f ; un nouveau SHA source exige sa propre CI. **Aucun résultat P2f n'est acquis à ce checkpoint.**

## Produit : lire avant de confirmer

P2e sait enregistrer une révocation et une reformulation atomiques, mais un auteur a besoin de **prévisualiser** le sens de la correction sans altérer sa chronologie. P2f ajoute une commande `PreviewCorrection` au même acteur Rust mono-propriétaire et une méthode `preview_atomic_correction` au service de fixture existant, **exclusivement `#[cfg(test)]`**. La méthode partage un unique helper `stage_atomic_correction` avec la commande de confirmation P2e pour éviter des validations contradictoires.

L'aperçu ouvre une transaction SQLite `IMMEDIATE` sur **la connexion v7 RAM fictive déjà ouverte**, tente exactement les deux INSERT immuables (décision `revoke` puis reformulation stage4), applique les gardes de cycle, d'univers, d'ancres, de révision et d'unicité, puis appelle **toujours `tx.rollback()` en cas de succès**. En cas d'échec SQL, la transaction de `rusqlite` est abandonnée et rollbackée ; les deux enregistrements ne sont jamais conservés. Le résultat typé `CorrectionPreview` indique l'ID de relation originale et l'assertion proposée avec origine `restatement`, sans conférer de droit d'écriture.

## Tests Rust nouveaux (3) — ATTENDUS, NON QUALIFIÉS

1. Un aperçu valide B→A renvoie la correction proposée alors que la relation ancienne A→B reste **active** et que les tables décision/reformulation restent vides. Une commande de confirmation explicite ultérieure avec les mêmes IDs réussit ; `r2` reste l'historique et `r3` la tête narrative.
2. Overlay absent, création d'un cycle, univers erroné et révision inconnue refusés ; aucun enregistrement partiel, aucune modification des assertions, `PRAGMA integrity_check=ok`.
3. Acteur à client concurrent : un aperçu B→A initialement valide ne vaut **pas** permission de confirmation. Un autre client ajoute A→C et C→B, puis la confirmation ultérieure B→A est rejetée comme cycle, sans retrait de l'ancien A→B. Arrêt du worker et clients déconnectés vérifiés.

**Comptes attendus (NON ACQUIS)** : 314 Rust = 311+3 ; 7 Greenfield ; 68 inventaire ; 183 continuité ; six Vitest ; Chromium 85/85 modes normal et CSP stricte ; 19 blobs fictifs exactement liés au HEAD Git. Exiger les logs complets au SHA exact.

## Frontière de sécurité

La prévisualisation n'est **ni** réservation de version, **ni** verrou persistant, **ni** garantie qu'une future confirmation réussira : la base peut changer entre les deux commandes ; seul l'INSERT à la confirmation revalide le graphe. Aucune consultation ou modification des données opérateur, profil existant, fichiers/journaux/sauvegardes, aucun Tauri IPC, SQL migration 007 de production, Windows Hello natif, marqueur/recovery, writer runtime ou gate P4. Les anciens triggers v7 et leurs contraintes UNIQUE sont intacts. Les générateurs de texte/Ollama ne reçoivent aucune capacité de modification réelle. Aucune preuve de custody atomique OS des fichiers SQLite main/WAL/SHM ni d'exclusion d'écrivains Windows adversariaux.

Stratégie **PRODUCT_FIRST_PARALLEL_SAFETY** inchangée ; avertir le propriétaire **AVANT** tout changement. **M3.2 IN_PROGRESS_NOT_ACCEPTED**, P4 réel/writer/R1–R9 **NOT_PROVEN**, G2B **NOT_ACCEPTED**, G2C **NOT_AUTHORIZED**, G3 **STOP_UNAVAILABLE**, historique **PENDING_EXTERNAL_ATTESTATION(21/3/2)**, prospective **NOT_STARTED**, D3b-4/5 STOP. glib 0.18.5 Linux GTK3 #160 **OPEN_NOT_REMEDIATED**.

**Gates** : re-fetch main/PR/CI/reviews/threads/Protect main ACTIVE strict bypass=[], qualification exacte Windows source, squash protégé `expected_head_sha`, CI postmain indépendante, commentaire #38 append-only ; #282 parent doit être terminée avant la fusion P2f. **Fixtures/CI ≠ admission réelle.**

Références externes pour la mécanique transactionnelle seulement : https://www.sqlite.org/lang_transaction.html et https://docs.rs/rusqlite/latest/rusqlite/struct.Transaction.html ; ces références ne prouvent pas notre writer.
