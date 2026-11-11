# M3.2 — P3q : borne de sélection Unicode des ancres, rapprochement Stage 25/26

**11 novembre 2026 — QUALIFIÉ SOURCE ET POSTMAIN (périmètre fictif seul ; contexte initial ci-dessous).**
Parent protected `main=95cfc9d779af8e5c564d508eb08d84b5cc2d682f` ;
PR #338 sécurité fusionnée sous Protect main ACTIVE/strict `bypass_actors=[]`.
CI source #42918580459 attempt 1 completed/SUCCESS au SHA
`4ce78747f151dbbaf7709708e6ce1e8fd07c7460` (90 étapes SUCCESS).
CI postmain indépendante #42920031454 attempt 1 **completed/SUCCESS** sur
le SHA exact `95cfc9d779af8e5c564d508eb08d84b5cc2d682f`,
job Windows #130192247420 (89 SUCCESS, 1 PR-only SKIPPED, aucun échec).
Aucune régression historique de #338 revendiquée fermée pour Dependabot :
Vite `8.1.7`, Rolldown `1.1.7` dans `main`, issue #160 et
`glib 0.18.5` Linux toujours OPEN_NOT_REMEDIATED.

## Écart précis avec l'ancienne PR #35

Sur la PR #35 (DRAFT, jamais fusionnée), le Stage 25
`tools/m3_2_chronology_comparison_reference.py` refuse explicitement un
`left_anchor_id` ou `right_anchor_id` de plus de **256 caractères Unicode**
(`len(identifier) > 256`), sans lire la production. Le Stage 26
`tools/m3_2_chronology_witness_reference.py` réutilise ce sélecteur.
Sur `main`, le composant TS `src/M32WorldOrderComparison.tsx`, isolé et
non monté dans `App.tsx`, refusait les sélections vides, inexistantes,
historiques ou étrangères, mais **pas la longueur >256**.

P3q ajoute la même borne **sur les deux identifiants explicitement
sélectionnés seulement**, avant la recherche des témoins. La longueur est
comptée en points de code Unicode (équivalent de `len` Python), et non en
unités UTF-16 JavaScript ; le parcours est interrompu dès le 257e point
de code pour ne pas matérialiser de tableau arbitrairement long.
Aucune troncature, substitution d'ancre, interprétation de libellé ou
permission d'accès n'est introduite.

Test Vitest ciblé : 256 ASCII **et** 256 caractères astraux sont acceptés,
257 sont refusés dans chaque position y compris même source/destination,
aucun motif humain ni identifiant contesté ne transparaît dans l'affichage
en refus. Les autres témoins P3o/P3p de cycle, doublon et ancre retirée
restent inchangés.

## Différences volontairement NON traitées

- L'ancien témoin Python choisit une preuve de même longueur suivant
  **l'ordre d'insertion** ; le composant TS choisit de façon stable par
  **identifiants de relation**. Ce contrat de présentation devra recevoir
  une décision explicite avant toute prétention d'équivalence globale.
- L'ancien Stage 26 permet une sélection ciblée dans un univers de
  plus de 512 ancres sans créer de panneau ; la projection TS complète
  plafonne à 512 ancres. Le lot P3q ne modifie pas cette limite, ne crée
  aucune API de pagination ni aucun service Rust réel.
- Les filtres Stage 25 ne sont pas portés par la comparaison TS actuelle ;
  aucune option de filtre n'est fabriquée par ce lot.

## Checklist / autorisations

**104 obligations, M32-001/002 clôturées, 102 ouvertes ; AUCUNE case
supplémentaire clôturée.** `M32-007 [ ]` rapprochement #35, `M32-058 [ ]`
contrats historiques, `M32-080 [ ]` consultation produit : preuves partielles
uniquement, pas de recette opérateur. CI HEAD et postmain **P3q À QUALIFIER**.
Journal #38 append-only et références SHA exact obligatoires.

`PRODUCT_FIRST_PARALLEL_SAFETY` maintenue, avertir **AVANT** changement ;
M3.2 `IN_PROGRESS_NOT_ACCEPTED` (~45 % estimés) ; writer/R1–R9
`NOT_PROVEN`, P4 réel STOP, G2B `NOT_ACCEPTED`, G2C `NOT_AUTHORIZED`,
G3 `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`,
prospective `NOT_STARTED`, main/WAL/SHM et ABA invisible `NOT_PROVEN`.
STOP données v6/v7 et backups opérateur, `M:\\Fabulaxiom`,
profil Greenfield existant, IPC writer, migration 007, Hello, recovery.
La CI synthétique ne qualifie pas une admission.

## Qualification indépendante — 11 novembre 2026

[PR #339](https://github.com/LaurentCOLL1/Fabulaxiom/pull/339) MERGED, `expected_head_sha=ae24d7f57c023fbd8ea2c4c963e5b9f5c73b1bcb`, Protect main ACTIVE strict `bypass_actors=[]`, reviews=[]/threads=[]. [CI source #42962049860](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/42962049860) attempt 1 completed/SUCCESS (HEAD exact, 90 étapes) ; main `1c657aa6584bcea1b11f5937728950614d2afed8` ; [CI postmain #42963106729](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/42963106729) attempt 1 completed/SUCCESS sur SHA exact, job Windows #130334040310 (89 SUCCESS, 1 PR-only SKIPPED). [#38 #6787709872](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6787709872) déjà enregistré.

**P3q qualifiée pour l'aperçu fictif seulement** ; tie-break, filtres, >512, intégration, R1–R9/P4 et acceptation M3.2 restent ouverts. Checklist 104 : 2 closes, 102 ouvertes, aucun nouveau [x].
