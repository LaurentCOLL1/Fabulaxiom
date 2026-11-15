# P3ac — lot de précédences humaines fictives avec accord explicite

**15 novembre 2026 — CANDIDAT NON QUALIFIÉ, laboratoire navigateur inventé uniquement.** Protected parent `main=c1435a612c45489f1f6e07b557662fac1b6b5245` après PR #364 MERGED ; source Windows [#43620011103](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/43620011103) SUCCESS HEAD exact `533c6389effdd9b55fb725c356562aa171ddca62`, postmain indépendante [#43621231640](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/43621231640) SUCCESS SHA exact. Ce document ne prédit pas la CI propre à P3ac.

## Valeur produit — un parcours cohérent, pas un micro-test

- `src/m32FictionalHumanOrderBatch.ts` vérifie **un lot entier** de 1 à 16 précédences explicitement déclarées par l'auteur ; le résultat n'est retourné qu'après validation de tous les éléments. Relation double, ancre inactive/historique, référence inconnue ou cycle sur la dernière action = **refus du lot complet**, sans mutation du brouillon initial.
- `src/M32FictionalHumanOrderBatchLab.tsx` fournit sélection de deux ancres, justification, ajout/retrait dans le lot, prévisualisation globale et bouton de confirmation distinct. Toute modification du lot invalide la prévisualisation. La confirmation revalide toutes les actions et le brouillon courant, refusant un aperçu périmé ou modifié.
- `src/m32BrowserLab.tsx` expose ce parcours uniquement dans la page de tests navigateur fictive ; si le scénario simulé est cyclique, la page refuse l'accès. Aucun import depuis `App.tsx`, aucune commande Tauri, aucun SQLite, fichier, réseau, IPC ou writer.
- `src/m32FictionalHumanOrderBatch.test.tsx` apporte **18 cas candidats** : refus d'un cycle tardif, dédoublonnage, justification, Universe étranger, bornes, origine fictive, consentement, snapshot périmé, source immuable, échappement HTML, ordre d'insertion non trié et absence de faux succès de persistance.

## Limites obligatoires

L'atomicité est celle **d'un calcul pur du brouillon JavaScript en RAM**. Elle ne représente aucune transaction SQLite, aucune custody atomique `main/WAL/SHM`, aucun rollback disque et aucune garantie de concurrent writer. La vérification humaine du lot ne constitue pas une attestation de provenance d'une scène/roman réel, d'un calendrier, ni un ordre total automatiquement déduit. `real_g3_authorized=false` sur toutes les transitions.

M32-056, 058, 063, 072, 078, 080 restent **OUVERTES** (preuves partielles candidat), M32-020 et R1–R9 writer **NOT_PROVEN**. Checklist **104: 9 closes/95 ouvertes** ; M3.2 **IN_PROGRESS_NOT_ACCEPTED (~45 %)**. PRODUCT_FIRST_PARALLEL_SAFETY et toutes interdictions sur originaux v6/v7, Greenfield, backups, IPC writer, migration 007, Hello, recovery, G2B/G2C/G3 et glib #160 inchangées.

## Travail R4 indépendant

Registre append-only [issue #38](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6885824968) : #297, #309 et #319 preuves R4 Windows jetables ont des source et postmain CI terminales, mais pas d'atomicité des 3 handles ; **M32-020 [ ]** avec writer STOP. Ni cette preuve négative ni P3ac n'acceptent une connexion réelle.

Avant fusion : CI Windows terminal SUCCESS au **HEAD exact P3ac**, diff/reviews/threads, Protect main ACTIVE strict bypass=[], squash `expected_head_sha`, postmain indépendante et #38 append-only.
