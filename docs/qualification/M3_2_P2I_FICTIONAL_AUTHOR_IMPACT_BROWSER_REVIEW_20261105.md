# M3.2 — P2i : revue visuelle d'impact auteur en navigateur fictif (CANDIDAT NON QUALIFIÉ)

**5 novembre 2026.** P2h #287 protégé et fusionné sur `main=0bf6f0ab6753d5ce4bed99adc44494a322347dc9` ; source exacte #42045435790 SUCCESS (320 Rust, 7 Greenfield, 68 inventaire, 183 continuité, 360 Vitest, Chromium 85/85 normal+CSP, 19 blobs). Postmain #42049010729 EN COURS au checkpoint. Parent documentaire #288 DRAFT `f110988770769ffbc65d80a91c97f835a368d40d`, source Windows #42049737060 EN COURS au checkpoint. P2i reste candidat, propre CI Windows requise et la reconstruction après #288 protégée obligatoire.

## Tranche produit, non admission de production

L'objectif est de rendre compréhensible en consultation ce que changerait une correction de chronologie : trois groupes distincts d'arêtes **retirées**, **ajoutées** et **inchangées**. Cette représentation est seulement une projection **inventée en mémoire navigateur**, alignée conceptuellement sur les catégories typées P2h. **Elle ne lit pas le retour Rust P2h**, n'utilise aucun pont IPC, n'enregistre rien et ne prétend pas prouver l'identité WAL/SHM.

Deux nouveaux fichiers TS/React autonomes :
- `src/M32P2iFictionalImpactReview.tsx` : composant lecture seule, jamais importé par `App.tsx`, fonction pure `previewP2iFictionalImpact`, représentation de trois listes sans bouton ni saisie. Provenance requise `fictional_browser_memory_only`, `production_writer_admitted=false`, `real_g3_authorized=false`, univers explicite identique. Comparaison par ID + ancres source/destination + origine, pas par ID seul. Aucune date, ordre total, ordre de narration ou de révélation inféré. Arêtes invalides, univers étranger, doublons, cycle et forge de provenance refusés avant affichage. JSX échappe les chaînes inventées.
- `src/m32P2iFictionalImpactReview.test.tsx` : **7 nouveaux tests Vitest CANDIDATS**, couvrant comparaison stable non destructive, réutilisation d'ID, univers/provenance illégaux, cycle/self/duplicata, lecture seule, refus visible et échappement HTML.

**Résultats attendus mais NON QUALIFIÉS** : 320 Rust, 7 Greenfield, 68 inventaire, 183 continuité, **367 Vitest** (360+7), Chromium 85/85 normal+CSP, 19 Git blobs fictifs. Les CI des parents ou de P2i avant rebase ne se substituent pas à la CI Windows du HEAD final. Confirmer le diff test-only, les reviews/threads et Protect main STRICT bypass=[] avant fusion `expected_head_sha`, puis postmain indépendante.

## Frontières invariables

P2i n'ouvre ni SQLite ni fichiers, n'appelle pas Tauri, Ollama, réseau, stockage ou API opérateur, ne modifie pas les objets d'entrée, n'a aucune commande de validation et n'est pas câblé à l'application. Zéro runtime migration 007, writer, native Hello, sauvegarde/journal, marqueur/recovery. L'interface est une illustration de la future expérience auteur, **pas P4 réel ni une preuve de writer**.

**PRODUCT_FIRST_PARALLEL_SAFETY inchangée** (avertir AVANT un changement de stratégie), M3.2 `IN_PROGRESS_NOT_ACCEPTED`, réel P4/writer/R1–R9 `NOT_PROVEN`, G2B `NOT_ACCEPTED`, G2C `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`. R4–R9 vraie custody atomique main/WAL/SHM, exclusion écrivain adversarial `NOT_PROVEN`. glib 0.18.5 Linux GTK3 issue #160 `OPEN_NOT_REMEDIATED`. Issue #38 append-only. **CI fixtures ≠ admission réelle.**
