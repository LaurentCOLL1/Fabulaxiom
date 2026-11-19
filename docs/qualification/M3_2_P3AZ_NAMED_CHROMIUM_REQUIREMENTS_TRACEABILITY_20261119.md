# M3.2 P3az — traçabilité nommée P3ax/P3ay à périmètre borné (19 novembre 2026)

## But : rendre les preuves existantes utilisables, sans ouvrir de gate

La matrice existante `M3_2_REQUIREMENTS_TEST_EVIDENCE_MATRIX_20261111.json` contient déjà **104 critères** et les neuf clôtures datées de la master checklist. P3az l'enrichit sans créer une seconde matrice concurrente : quatre exigences encore ouvertes ont maintenant une observation nommée de test Chromium, une CI source à HEAD exact, un job Windows et une postmain indépendante, avec SHA, dates et limites de portée. Le contrôle `tools/test_m32_requirements_traceability.py` maintient les 104 lignes, le 9/95, le `NONE_ACCEPTED` pour les ouvertes et le maintien de M32-078 [ ].

| Critère encore ouvert | Cas de navigateur fictif effectivement observé | Source attestée | Postmain indépendante attestée | Ce qui reste non prouvé |
| --- | --- | --- | --- | --- |
| M32-070 formulaire manuel | #109 ancre et source exactes, sélection explicite ; Vitest #19 | PR #392, CI #44412057826, HEAD `c8dce8c150b50d528c04a32779a6e8ded1fbe2c4`, job #135182534955 | #44416272668 sur `38a9dc204f6f1a9d768c6d9e45519b472e420e8c` | calendrier complet, IA absente qualifiée en usage, runtime |
| M32-071 consultation sources | #110 historique détaillé, sélection explicite ; Vitest #20 | PR #393, CI #44453364420, HEAD `bd42eaedfc60bb300cce647013540ab62b3b1013`, job #135322434231 | #44455249407 sur `411d5a677feba151248e3e69c6225dc3a6876aab` | filtres, pagination, profil opérateur, sources authentiques |
| M32-075 échappement / isolement | #111 HTML hostile inerte et changement d'Universe | PR #393, même CI et HEAD | #44455249407 sur `411d5a677feba151248e3e69c6225dc3a6876aab` | parcours complet clavier et hors ligne sur vraie app |
| M32-081 lecture du passé | #110 consultation après retrait, motif et tombstone ; Vitest #21 | PR #393, même CI et HEAD | #44455249407 sur `411d5a677feba151248e3e69c6225dc3a6876aab` | correction/revocation réelle, persistance et invariants de v7 admissibles |

**Nature de la preuve** : le journal Windows de #44453364420 montre les lignes `M32_BROWSER_CASE_PASS 110` et `111`, Chromium 111/111 et CSP strict 98/98 ; le journal de #44412057826 montre le cas 109 et Chromium 109/109. Une réussite de test **fictif non monté** n'est ni la satisfaction intégrale du critère ni l'admission d'un environnement réel. La matrice stocke les observations dans `latest_named_chromium_observation` et conserve `status=OPEN_NOT_ACCEPTED`, `evidence=NONE_ACCEPTED`, `individual_test_step_result=null`, les indicateurs d'admission à `false`. Les CI postmain ont été vérifiées séparément sur leurs propres SHAs. M32-078 elle-même reste ouverte tant que la matrice complète ne documente pas les preuves exhaustives et autorisées exigées.

**Sécurité** : Protect main ACTIVE strict bypass=[] ; parent de P3az `main=411d5a677feba151248e3e69c6225dc3a6876aab`, [PR #393](https://github.com/LaurentCOLL1/Fabulaxiom/pull/393) MERGED, CI source #44453364420 completed/SUCCESS au HEAD `bd42eaedfc60bb300cce647013540ab62b3b1013`, postmain indépendante #44455249407 completed/SUCCESS au SHA exact parent. M3.2 `IN_PROGRESS_NOT_ACCEPTED`, checklist 104=9 closes/95 ouvertes, PRODUCT_FIRST_PARALLEL_SAFETY, #35/#215 DRAFT.

STOP : Writer/R1–R9 NOT_PROVEN ; P4 réel STOP ; G2B NOT_ACCEPTED ; G2C NOT_AUTHORIZED ; G3 STOP_UNAVAILABLE ; PENDING_EXTERNAL_ATTESTATION(21/3/2) prospective NOT_STARTED ; R2 STOP, R3 partiel, D3c conception, D3b-4/5 et D3b-5 STOP ; main/WAL/SHM, live SQLite WAL-index et ABA NOT_PROVEN ; glib #160 OPEN_NOT_REMEDIATED ; STOP v6/v7, M:\\Fabulaxiom, Greenfield, backups, IPC writer, 007, Hello, recovery.

Prochaines portes : CI source P3az HEAD exact, reviews/threads/diff, fusion squash protégée `expected_head_sha`, postmain indépendante, commentaire append-only #38.
