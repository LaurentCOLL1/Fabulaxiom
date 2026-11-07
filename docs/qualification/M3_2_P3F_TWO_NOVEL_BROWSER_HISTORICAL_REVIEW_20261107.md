# M3.2 P3f — revue de deux romans et de leurs sources historiques dans l'atelier navigateur fictif

7 novembre 2026 — **CANDIDAT NON QUALIFIÉ** (CI Windows finale obligatoire). Parent protégé `main=e3b82c1f1d6ca6b3de1ac889936433306eb3f88d` (PR #312), postmain indépendante #42410803859 à qualifier. Décision `PRODUCT_FIRST_PARALLEL_SAFETY` inchangée (informer AVANT toute réorientation).

## Tranche produit

- `src/M32P3fTwoNovelFictionalReview.tsx` : réunit deux sources *déclarées et entièrement inventées* (roman/scène/ancre/révision historique distincte de sa HEAD fictive) avec les composants déjà testés P2m (assertions directes communes / propres) et P2l (quatre directions directes). Modes de consultation en lecture seule, boutons sans sauvegarde, pas d'inférence de date, d'ordre total, de narration ou de révélation. La correspondance source→roman est une **assertion de fixture**, non une preuve SQLite.
- `src/m32BrowserLab.tsx` : un nouvel accès explicite à cet atelier isolé ; la comparaison est indépendante de l'état du reste des travaux fictifs du navigateur. Autre Univers ou graphe cyclique = refus sans afficher les données du premier Univers. Composant toujours non importé par `App.tsx`.
- `src/m32P3fTwoNovelFictionalReview.test.tsx` : six nouveaux Vitest, vérifiant les révisions historiques r2/r4 distinctes des HEAD r3/r5, le tri des assertions directes, les STOP de provenance, les Univers/IDs illégitimes, les cycles/doublons, l'immuabilité des entrées et l'échappement JSX.
- `tools/m32_browser_interaction.cjs` : trois nouveaux scénarios Chromium sur navigateur réel, y compris deux sources, bascule des directions et refus des Univers étrangers/cycliques sous CSP normale et stricte. L'assertion finale passe de 85 à **88 cas**, avec marqueurs historiques conservés.

**Résultats attendus, NON encore PASS avant CI au HEAD exact : 330 Rust, 7 Greenfield, 69 inventaire SQLite, 183 continuité, 402 Vitest (396+6), 88/88 Chromium normal+CSP, 25 blobs exacts fictifs.** Aucun accès SQL ni pont Rust/TS par P3f, et sa fixture React ne prétend pas provenir du scénario Rust P2n.


## Manifestes exacts de sécurité Chromium

Le manifeste source fictif fermé de 19 fichiers est étendu à **25 chemins précis** : P3f, P2m, P2l, P2k, P2j et P2i. Les deux listes indépendantes `tools/m32_ci_fixture_stage.cjs` et `tools/m32_ci_git_source_binding.cjs` restent identiques, ne couvrent pas `App.tsx`, et refusent tout autre import, fichier, lien symbolique, dérive Git, chemin hors famille ou package externe. Les tests de liaison Git exigent 25 blobs exacts sans assouplir les contrôles négatifs ; le témoin historique P3a de 19 reste documenté. Aucun accès runtime n'est ajouté.

## STOP et qualification

Ce n'est pas une interface opérateur et ce n'est pas une admission du writer. Pas d'App.tsx, Tauri State/IPC, source de base SQLite, chemin disque, profil Greenfield existant, sauvegarde/journal, migration 007 de production, Hello natif, marqueur ou recovery. Données `fictional_browser_memory_only`, `production_writer_admitted=false`, `real_g3_authorized=false`.

M3.2 `IN_PROGRESS_NOT_ACCEPTED` (~45 % ingénierie, estimation 40–50 %) ; writer/R1–R9 `NOT_PROVEN`, P4 réel STOP, G2B `NOT_ACCEPTED`, G2C `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE` ; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`; custody atomique main/WAL/SHM et absence d'ABA invisible `NOT_PROVEN`. glib #160 `OPEN_NOT_REMEDIATED`. Décision produit-first + sécurité parallèle préservée et prévenance obligatoire avant changement.

Gates : qualifier postmain #312 au SHA exact, CI Windows source au HEAD final, inspecter diff / reviews / threads, `Protect main` ACTIVE strict bypass=[], squash avec `expected_head_sha`, postmain indépendant et commentaire append-only #38. **Fixtures CI ≠ autorisation d'utiliser les données réelles.**
