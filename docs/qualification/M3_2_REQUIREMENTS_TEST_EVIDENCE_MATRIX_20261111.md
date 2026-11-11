# M3.2 — matrice d'exigences, tests cibles et preuves (104 entrées)

**11 novembre 2026 — CANDIDAT SOURCE-ONLY, NON QUALIFIÉ.** Parent `main=b2b032c0010a9d879103718cfa0786a827c5ac56`, #343 source CI #43101935892 et postmain #43103763204 SUCCESS SHA exact ; journal #38 #6809111466. Aucun fichier opérateur lu, aucune CI candidate qualifiée à ce stade.

La matrice liée `M3_2_REQUIREMENTS_TEST_EVIDENCE_MATRIX_20261111.json` donne une ligne par M32-001 à M32-104 avec exigence, état vivant de la checklist, test ou vérification **cible**, preuve de clôture existante pour les sept cases [x], et preuve encore **requise** pour 97 tâches ouvertes. La présence d'un chemin de test n'est PAS un PASS et n'accorde aucun droit sur SQLite réel.

**Piste indépendante M32-078 :** nouveau contrat CI vérifiant correspondance 104/104, statuts, chemins locaux, preuves fermées uniquement avec SHA et run exacts, aucune fausse preuve pour ouverts, et limites de gate. **M32-078 reste [ ]** jusqu'à qualification complète ; toute PR qui clôt une case doit mettre aussi la matrice à jour.

**Piste indépendante M32-104 :** voir `M3_2_SCOPE_BOUNDARY_20261111.md` ; vérifie les exclusions explicites M3.3–M9. **M32-104 reste [ ]**. Les deux travaux sont indépendants du writer et ne changent ni P4 réel, ni G2B/G2C/G3, ni la distribution.

Checklist 104 / 7 closes / 97 ouvertes ; M3.2 IN_PROGRESS_NOT_ACCEPTED (~45% estimés), PRODUCT_FIRST_PARALLEL_SAFETY inchangée. R1–R9/writer NOT_PROVEN, P4 STOP, G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE ; historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED ; atomicité main/WAL/SHM, WAL-index et ABA NOT_PROVEN ; glib #160 OPEN_NOT_REMEDIATED.
