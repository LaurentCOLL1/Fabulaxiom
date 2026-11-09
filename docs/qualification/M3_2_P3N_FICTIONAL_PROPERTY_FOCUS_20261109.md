> **INCIDENT CI SOURCE P3n — 09/11.** Première exécution Windows [#42674233301](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/42674233301) au HEAD `dda02f8f61650267c8b33638ac33481f033f819d` terminée **FAILURE**, et l'API GitHub retourne `total_count=0` jobs (aucun job ni étape de test observable). La cause n'est **PAS PROUVÉE** : ne pas la déclarer transitoire, ne pas inférer de résultat Rust/Vitest, ne pas désactiver de gate. Ce commit ajoute seulement la traçabilité de l'incident ; la CI à son nouveau SHA est à qualifier indépendamment. Maintenir PR DRAFT et tous les STOP.

# M3.2 P3n — filtre de propriété littérale dans la revue de deux romans fictifs

9 novembre 2026 — **CANDIDAT / DRAFT / NON QUALIFIÉ**.

## Valeur produit et preuve limitée

P3i–P3m distingue des accords littéraux, des différences à examiner et des faits unilatéraux, avec leurs sources historiques **inventées**. P3n ajoute une consultation par `property_key` après le filtre P3k par personnage. La propriété n'est choisie **qu'après validation intégrale** des deux romans, scènes, témoins de révision, sources historiques et assertions : une propriété inconnue, hors du personnage sélectionné ou adossée à une révision falsifiée provoque un refus avant sélection. Les compteurs restent cohérents dans les quatre catégories (accords/différences/premier seul/second seul). Les identifiants ou littéraux HTML hostiles sont échappés par React. Aucun arbitrage canonique, aucune date ni ordre narratif inventés.

## Diff autorisé

- `src/M32P3fTwoNovelFictionalReview.tsx` : `previewP3nFictionalPropertyFocus` pur, vérification de la propriété dans le catalogue préalablement validé, sélection de propriété dans le seul laboratoire navigateur.
- `src/m32P3fTwoNovelFictionalReview.test.tsx` : trois tests Vitest nouveaux : #25 classifications et compteurs avec révisions préservées, aucune mutation ; #26 propriété inconnue/étrangère et HEAD falsifiée refusées avant révélation ; #27 contrôle accessible, HTML hostile échappé, entrée inchangée.
- Fichiers de qualification et prompts de reprise uniquement. **Aucun changement** d'`App.tsx`, IPC Tauri, Rust/SQL runtime, writer, workflow, dépendances, lockfile, bases opérateur, profil Greenfield existant, backups/journaux, migration 007, Hello natif, marqueur/recovery.

## Checkpoints, CI et admission

Parent protégé `main=a8ff505bc11bf88021ac2a6a1d620a101449217b` (#329), indépendant postmain Windows #42648352409 **SUCCESS exact SHA**. La PR documentaire #330 reste **DRAFT/incomplète** (9 documents ; `STATE.md` précédemment bloqué par contrôle de sécurité, sans contournement). P3n n'efface ni ne remplace ce blocage.

**Attendus exclusivement, NON QUALIFIÉS avant CI Windows du HEAD source final** : 332 Rust, 7 Greenfield, 69 inventaire SQLite, 183 continuité, **427 Vitest** (424+3), Chromium 88/88 normal et CSP stricte, 25 blobs Git fictifs exacts. Exiger CI source terminale SHA exact, fichiers/reviews/threads, Protect main ACTIVE strict bypass=[], squash `expected_head_sha` seulement après gates, puis postmain indépendant SHA exact et issue #38 append-only. Une CI réussie **ne donne aucune admission writer/P4**.

PRODUCT_FIRST_PARALLEL_SAFETY inchangée : prévenir AVANT tout changement de stratégie. M3.2 IN_PROGRESS_NOT_ACCEPTED (~45 % estimation), writer/R1–R9 NOT_PROVEN, P4 réel STOP, G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE ; historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED ; main/WAL/SHM custody atomique et ABA invisible NOT PROVEN ; glib #160 OPEN_NOT_REMEDIATED. STOP v6/v7 opérateur, profil Greenfield existant, sauvegardes/journaux, IPC writer, 007 runtime, Hello natif, marqueur/recovery.
