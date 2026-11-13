# Fabulaxiom M3.2 — M32-078 V5 : rapport JSON des 11 cas Vitest nominatifs (candidat)

**13 novembre 2026, PAS ENCORE QUALIFIÉ.** Base protégée `main=f70039799a12e27f517cfd08a93852dcaaf39911` après #354 MERGED sous Protect main strict, source CI #43455134802 completed/SUCCESS HEAD `976141af23076dde38e14c18b61bf46d5b2bfb18`. Postmain #354 indépendante [#43470878486](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/43470878486) EN COURS / NON QUALIFIÉE au checkpoint.

## But de preuve inédit

V4 enregistre deux lignes de SUITES « 6 tests » et « 5 tests » dans les journaux GitHub Actions Windows, sans résultats nominatifs ; le nouveau V5 propose une étape CI Windows autonome au-dessus des tests frontend existants :

1. Exécuter `node --test tools/test_m32_named_vitest_report.cjs` sur des rapports JSON inventés. Les contrôles négatifs couvrent titre supplémentaire ou manquant, doublon, résultat failed/pending, mauvais compteur, suite inattendue ou doublonnée, et fausses déclarations de réussite.
2. Exécuter uniquement `src/m32WorldOrderIsolation.test.tsx` et `src/m32WorldOrderBoundaries.test.tsx` avec le reporter JSON officiel Vitest (`--reporter=json --outputFile=...`) dans un fichier temporaire du runner Windows, sans upload de données ni dépendance réseau supplémentaire.
3. Vérifier que les **deux fichiers exacts** ont les **11 titres nominatifs attendus**, leurs statuts `passed`, zéro `failureMessages`, zéro `pending/todo/failed`, les compteurs cohérents, et absence de suite ou cas injecté. Imprimer un marqueur `M32_NAMED_VITEST_CASE_PASS` par titre fixé et un total final seulement si les 11 validations réussissent ; supprimer le rapport temporaire dans un `finally`.

L'objectif est d'obtenir, **si et seulement si la CI prospective termine SUCCESS**, une preuve individuelle des 11 tests React fictifs non montés au SHA exact et à l'étape de job déterminée. La présence de la commande dans la branche n'est pas encore une preuve d'exécution. Le résultat test-nominatif reste **NOT_STARTED / UNQUALIFIED** jusqu'à lecture du log CI. Aucun champ de la matrice v4 ne sera promu avant cette observation.

## Limites de confiance

Un test React fictif réussi n'est pas une attestation de conformité complète M32-075/078/079/080/082/083, ni un résultat d'intégration Tauri/SQLite ou de sécurité Rust/Windows, ni une admission d'opérateur. Même 11 PASS nominatifs n'établissent ni la protection de WAL/SHM, ni les revues humaines, ni l'admission du writer.

**Checklist 104 : 8 closes / 96 ouvertes, M32-078 [ ], M3.2 `IN_PROGRESS_NOT_ACCEPTED` (~45 % estimés).** PRODUCT_FIRST_PARALLEL_SAFETY inchangée ; Writer/R1–R9 NOT_PROVEN, P4 STOP, G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE, historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED, main/WAL/SHM, WAL-index live, ABA NOT_PROVEN, #35/#215 DRAFT, #36/#160 OPEN glib Linux. STOP données v6/v7, M:\\Fabulaxiom, Greenfield, sauvegardes, IPC writer, migration 007, Hello natif et recovery.

Qualification requise : Windows CI HEAD exact terminale, revue des logs nominatifs et tests négatifs, reviews/threads, Protect main ACTIVE strict bypass=[], squash expected_head_sha, postmain indépendante et journal #38 append-only. Aucun gate levé.
